"""Run a Python script with a record of its outbound network connections (T2.7).

Usage: python tools/netguard.py RECORD SCRIPT [ARG...]

Installs an audit hook (PEP 578) and runs SCRIPT as `python SCRIPT ARG...`
would. Every name lookup of a host outside the local network is appended to
RECORD (JSON lines), whatever the library: requests, urllib, http.client and
smtplib all resolve the host first (`socket.getaddrinfo`), IP addresses
included. Lookups of the publisher's domains are refused as well, so that a
test run never reaches them.

tools/run_tests.py runs Odoo through it: the record covers the installation,
the scheduled jobs and the tests, also the code paths the test framework does
not watch. The browser is another process; its requests are in the Odoo log.
"""
import ipaddress
import json
import os
import runpy
import socket
import sys
import threading
import traceback

# Same list as odoo.addons.ov_brand.tests.external_requests
PUBLISHER_DOMAINS = ("odoo.com", "odoocdn.com", "odoo.sh")
LOOKUP_EVENTS = {
    "socket.getaddrinfo",  # (host, port, family, type, protocol)
    "socket.gethostbyname",  # (host,)
    "socket.gethostbyname_ex",  # (host,)
}
STACK_DEPTH = 8


def normalize(host):
    if isinstance(host, (bytes, bytearray)):
        host = host.decode("ascii", "replace")
    return str(host or "").strip("[]").rstrip(".").lower()


def is_publisher(host):
    return any(host == domain or host.endswith(f".{domain}") for domain in PUBLISHER_DOMAINS)


def is_local(host, local_names):
    if not host or host in local_names or host.endswith(".localhost"):
        return True
    try:
        address = ipaddress.ip_address(host.split("%")[0])
    except ValueError:
        return False
    return address.is_loopback or address.is_private or address.is_link_local or address.is_unspecified


def caller_stack():
    """The innermost frames of the caller, outside the standard library and
    the installed packages, to tell which code made the request."""
    frames = traceback.extract_stack()[:-2]
    ours = [frame for frame in frames if "site-packages" not in frame.filename
            and not frame.filename.startswith((sys.base_prefix, "<")) and frame.filename != __file__]
    return [f"{frame.filename}:{frame.lineno} {frame.name}" for frame in ours[-STACK_DEPTH:]]


def install(record):
    lock = threading.Lock()
    busy = threading.local()
    seen = set()
    local_names = {"localhost", normalize(socket.gethostname())}

    def hook(event, args):
        if event not in LOOKUP_EVENTS or getattr(busy, "active", False):
            return
        host = normalize(args[0])
        if is_local(host, local_names):
            return
        busy.active = True
        try:
            publisher = is_publisher(host)
            port = args[1] if event == "socket.getaddrinfo" else None
            stack = caller_stack()
            key = (host, port, tuple(stack))
            with lock:
                if key not in seen:
                    seen.add(key)
                    entry = {"host": host, "port": port, "publisher": publisher,
                             "thread": threading.current_thread().name, "stack": stack}
                    with open(record, "a", encoding="utf-8") as fh:
                        fh.write(json.dumps(entry) + "\n")
        finally:
            busy.active = False
        if publisher:
            raise socket.gaierror(socket.EAI_NONAME, f"{host}: publisher's domain, refused by tools/netguard.py")

    sys.addaudithook(hook)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    record, script, *args = sys.argv[1:]
    install(os.path.abspath(record))
    sys.argv = [script, *args]
    sys.path[0] = os.path.dirname(os.path.abspath(script))
    runpy.run_path(script, run_name="__main__")


if __name__ == "__main__":
    main()
