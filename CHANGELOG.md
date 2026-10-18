# Değişiklik Günlüğü

Son güncelleme: 2026-10-18

Her adımın kaydı en üste, tarih başlığıyla eklenir. Bir karar değiştiğinde **eski metni ve değişiklik nedeni** buraya yazılır (DECISIONS.md yalnız güncel hali tutar).
Kategoriler: **Kararlar**, **Belgeler**, **Kod**, **Ortam**, **Araştırma**.

## 2026-10-18

### Adım: GitHub Actions CI (T1.10) — otonom mesai 1

**Kod**
- `.github/workflows/ci.yml`: her push'ta, pull request'te ve elle (`workflow_dispatch`) çalışır. İki iş paralel:
  - `checks`: `check_docs.py` → `pre-commit run --all-files` → gitleaks 8.30.1 ile tüm geçmiş (arşivin SHA-256'sı doğrulanır) → `sync_skills.py --check`.
  - `tests`: Ubuntu 24.04, Python 3.12, PostgreSQL 18 servisi. `.venv` ve `requirements-dev.txt`; `.env` ve `odoo.conf` yerel araçlarla üretilir.
    - Şablondan `ov_ci_sample` üretilir; modül kuralları, ruff ve pylint-odoo'dan geçirilir.
    - `addons/` ve `ports/` altındaki bütün modüller örnekle birlikte tek veritabanında test edilir (`run_tests.py -v`). Hata olursa günlüğün sonu yazdırılır.
    - Elle çalıştırmada `modules` girdisindeki modüller ayrıca test edilir (Linux referans sonucu).
  - Güvenlik: yalnız okuma yetkisi, eylemler commit SHA'sıyla sabit, `persist-credentials: false`, elle girilen modül listesi kabuğa ortam değişkeniyle geçer.
  - Aynı dalda yeni push eski çalıştırmayı iptal eder.
- `.github/actions/upstream/action.yml`: `upstream/odoo` alt modülünü sığ çeker; git nesneleri upstream commit'ine göre önbellekte.
- `tools/check_secrets.py`: staged değişikliklerde `.env` değerlerini arar (en az 8 karakter; host, port, kullanıcı adı hariç). Pre-commit kancası. Mesai başından beri oturum klasöründe kullanılan betiğin depoya alınmış hali; `.env` yoksa (CI) atlar.
- `tools/run_tests.py`: `-v` gerçek hataların traceback'ini yazar.

**Doğrulama**
- İlk çalıştırma (geçici `ci-setup` dalı): iki iş de yeşil. `checks` 1 dk 14 sn, `tests` 2 dk 11 sn.
  - Örnek modül kuruldu, 1 test, `RESULT: OK`. gitleaks: 13 commit, sızıntı yok. Rehber kopyası upstream'le aynı.
- Negatif deneme (geçici `ci-negative` dalı): bilerek başarısız testli `ov_ci_negative` modülü.
  - `tests` kırmızı: `FAIL: TestOvCiNegative.test_module_installed`, `RESULT: FAILED (1)`, traceback günlükte. `checks` yeşil (lint temiz).
  - Commit kancaları atlanmadı; lint hatalı commit yerel kanca tarafından zaten engellenir (T1.9 negatif denemesi).
- `check_secrets.py` negatif denemesi (yerel): `.env` değeri içeren geçici dosya staged iken hata verdi; dosya silindi.
- gitleaks yerelde de çalıştırıldı (Windows sürümü, sağlama doğrulandı): sızıntı yok.
- Önbellek: GitHub önbellekleri dala bağlı; iki geçici dal birbirinin önbelleğini göremedi. `main`'de oluşan önbellek bütün dallarda kullanılır. Önbelleksiz sığ upstream çekimi 20–50 sn.
- Geçici dallar `main`'e tek commit olarak alındı (squash) ve GitHub'dan silindi.

**Belgeler**
- CLAUDE.md (Ortam: CI; Komutlar: gizli bilgi denetimi, CI), ARCHITECTURE.md (§2 ağacı, §5 CI), PLAN.md (T1.10, pano), README.md (CI rozeti, durum), COMPLIANCE.md (gizli bilgi denetimi; §5 gitleaks, GitHub eylemleri, PostgreSQL imajı), state.json.

### Adım: Modül şablonu ve kod kalite araçları (T1.9) — otonom mesai 1

**Kod**
- `tools/new_module.py`: `addons/ov_<ad>/` iskeleti üretir.
  - Manifest: sürüm `20.0.1.0.0`, lisans `AGPL-3` (ya da `--license LGPL-3`), yazar, `security/ir.access.csv`.
  - `README.rst`, boş `models/`, yalnız başlık satırlı `security/ir.access.csv`, `i18n/tr.po` başlığı, kurulumu doğrulayan ilk test (`post_install`).
- `tools/check_modules.py`: proje kuralları, yalnız standart kütüphane.
  - `ov_` öneki; lisans AGPL-3 veya LGPL-3 (D-016); sürüm `20.0.x.y.z`; yazar; `description` anahtarı yok.
  - Manifest adı, özeti ve README'de "Odoo" geçmez (D-007, D-014).
  - `README.rst`, `tests/test_*.py`, `i18n/tr.po` var. OCA portları kapsam dışı (D-019).
- `ruff.toml`: upstream `ruff.toml`'u genişletir. `upstream/`, `vendor/`, `ports/` hariç (portların lint düzeni T1.11'de); `tools/` için `print` serbest.
- `.pylintrc`: pylint-odoo'nun Odoo denetimleri (`disable=all`, `enable=odoolint`). Geçerli sürüm 20.0, izinli lisanslar AGPL-3 ve LGPL-3, zorunlu yazar.
- `.pre-commit-config.yaml`: ruff (v0.16.10), pylint-odoo (v10.0.12, yalnız `addons/`), modül kuralları, belge denetimi. Yerel depoda kanca kuruldu.
- `requirements-dev.txt`: `pylint-odoo==10.0.12`, `pre-commit==4.7.0`.
- `tools/pg.py`: iki `subprocess.run` çağrısına `check=False` (ruff PLW1510).

**Araştırma**
- Modül açıklaması: Odoo 20.0, manifestte `description` yoksa README'yi kullanır ve uzantısına bakmadan reStructuredText olarak işler (`ir_module.py`). Bu yüzden modül README'si `README.rst`; Markdown başlıkları ekranda düz metin görünürdü. pylint-odoo da `description` anahtarını eskimiş sayıyor.
- Manifestte `author` yoksa Odoo uyarı verip boş bırakıyor, `license` yoksa LGPL-3 varsayıyor. Şablonda ikisi de açıkça yazılı.
- T1.6'da not edilen 14 ruff bulgusu depo yapılandırması olmadan, ruff'ın kendi kurallarıyla bulunmuştu. Upstream kural setiyle yalnız ikisi geçerli (`pg.py`, PLW1510); düzeltildi.

**Doğrulama**
- Kabul: `python tools/new_module.py ov_sample` → `python tools/run_tests.py ov_sample`: modül kuruldu, 1 test, `RESULT: OK` (14 sn). Boş `ir.access.csv` sorunsuz yüklendi. `pre-commit run --all-files` temiz.
- `README.rst`, Odoo'nun docutils ayarlarıyla doğru başlık ve paragraf üretiyor; yönerge satırları HTML yorumu olarak kalıyor.
- Negatif denemeler:
  - lisansı `OPL-1`, sürümü `1.0`, yazarı yanlış, adı ve README'si "Odoo" içeren, SQL birleştiren modül: `check_modules.py` 8 sorun; pylint-odoo C8101, C8103, C8105, C8106, C8108, E8103;
  - pre-commit üzerinden: ruff (tek satırda çoklu import), pylint-odoo (lisans, sürüm) ve modül kuralları kancaları başarısız, commit engellenirdi.
- Örnek modül depoya girmedi; şablon CI'da üretilen örnek modülle denetlenecek (T1.10).

**Kullanıcıya soru**
- K12 (USER_TASKS): modüllerde yazar olarak görünecek ad. Varsayım `burak-sisci`.

**Belgeler**
- CLAUDE.md (Odoo geliştirme kuralları "Her modülde", Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 lint), PLAN.md (T1.9, pano, T1.10'a lint ve şablon adımları, §8), USER_TASKS.md (K12), COMPLIANCE.md §5 (pylint-odoo, pylint, pre-commit), README.md, state.json.

### Adım: Test çalıştırma komutları (T1.8) — otonom mesai 1

**Kod**
- `tools/run_tests.py`: modül testlerini temiz bir veritabanında çalıştırır ve günlüğü özetler.
  - `db init --force` ile test veritabanı (demo yok, `en_US`), ardından `-i <modüller> --test-enable --test-tags /<modül>`. `--reuse` veritabanını korur ve `-u` kullanır.
  - Testler ayrı HTTP portunda (8079): Odoo test modunda HTTP sunucusunu her zaman açıyor; geliştirme sunucusuyla çakışmaz.
  - Günlükteki `ERROR:`/`FAIL:` bloklarını ve `X failed, Y error(s) of Z tests` satırını okur.
  - Windows'ta test sınıflarının filestore temizliği hataları (traceback'te `_gc_file_store_unsafe` + `PermissionError` ya da `.__gc` dosyası `AssertionError`) ayrı sayılır, çıkış kodunu etkilemez. `setUpClass`'ta da çıkıyor; ilk sürüm yalnız `tearDownClass`'ı tanıyordu, düzeltildi.
  - Özet satırı yoksa (kurulum çöktü) hata sayılır.

**Ortam**
- Doğrulama:
  - `l10n_tr`: 3 test, hata yok, `RESULT: OK` (38 sn).
  - `account_edi_ubl_cii` (negatif deneme): 230 test, 3 failed + 29 error. 27'si Windows gc hatası (24 `tearDownClass`, 3 `setUpClass`). Kalan 5 gerçek hata: T1.2'deki çekirdek test hatası (`deferred_start_date`), satır açıklaması içe aktarma testi, PDF motoru olmadığı için 2 PDF üretim testi, gömülü PDF testinde `LocalBinaryFile` TypeError. Sonuç `RESULT: FAILED (5)`, çıkış kodu 1.

**Belgeler**
- CLAUDE.md Komutlar (test komutları), ARCHITECTURE.md (§2 ağacı, §5 yerel testler), PLAN.md (T1.8, pano, T1.9 kabulüne komut), README.md, state.json.

### Adım: Odoo AI rehberleri (T1.7) — otonom mesai 1

**Kod**
- `.claude/skills/`: upstream `skills/` klasörünün değiştirilmemiş kopyası (24 dosya): `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`, `odoo-review`, `odoo-git`. Yanında `LICENSE` (upstream kopyası) ve `SOURCE.md` (kaynak commit).
- `tools/sync_skills.py`: kopyalar; `--check` upstream'le farkı denetler (CI için). Windows'ta upstream çalışma kopyası CRLF olduğundan karşılaştırma satır sonundan bağımsız; kopyalar LF.

**Araştırma**
- Rehberlerin tamamı okundu; zararlı veya gizli talimat yok.
- Lisans: klasörde ayrı lisans dosyası yok; deponun LGPL-3 lisansı ve `COPYRIGHT` notu geçerli. Envantere yazıldı.
- Proje kurallarıyla çelişenler (CLAUDE.md'ye öncelik kuralı olarak yazıldı):
  - `odoo-git`: `[TAG] kapsam: özet` commit biçimi, rebase ve `--force-with-lease`. Yalnız upstream/OCA katkısında geçerli sayıldı.
  - `odoo-review`: değişikliğin Enterprise'daki "diğer yarısına" bakma adımı. Clean-room (D-006) gereği uygulanmaz.
  - `odoo-web-guidelines`: `patch()` Odoo içinde önerilmiyor, Odoo dışı kod için uygun; kendi modüllerimizde serbest.
  - `comments`: kod yorumları, kullanıcı metinleri ve commit mesajlarında yalnız ASCII noktalama. Markdown belgelerimiz kapsam dışı.

**Belgeler**
- CLAUDE.md:
  - Odoo geliştirme kuralları: rehberler ve öncelik kuralları; görünüm kalıtımı kuralı rehberle uyumlu yazıldı.
  - Eski metin: "görünüm kalıtımı XPath ile". Yeni metin: ada bağlı kalıtım (kısa `field` biçimi, gerekirse XPath), konuma göre asla. Neden: `odoo-guidelines` kısa biçimi tercih ediyor.
  - Komutlar bölümüne `tools/sync_skills.py` eklendi.
- ARCHITECTURE.md §2 ağacı, COMPLIANCE.md §5, PLAN.md (T1.7, pano, T1.10'a rehber denetimi), README.md, state.json.

### Adım: Odoo'nun yerelde çalıştırılması (T1.6) — otonom mesai 1

**Kod**
- `deploy/odoo.conf.example`: yerel geliştirme yapılandırma şablonu.
  - Addons yolu ARCHITECTURE §2 sırasıyla, glob kalıplarıyla (`vendor/oca/*`, `ports/oca/*`, `addon[s]`): henüz olmayan klasörler uyarısız atlanır.
  - Veri klasörü `OV_HOME/odoo-data`, `workers = 0`, yalnız `127.0.0.1`.
- `tools/odoo_conf.py`: şablondan depo kökündeki `odoo.conf`'u üretir (git'e girmez). Veritabanı bilgileri `.env`'den; veritabanı yöneticisi ana şifresi ilk çalıştırmada `.env`'ye üretilir (`ODOO_ADMIN_PASSWD`).
- `ruff check tools/` (henüz depo yapılandırması yok, 0.16 varsayılanları): `odoo_conf.py` temiz; `check_docs.py` ve `pg.py`'de 14 bulgu (çoğu `re.M` → `re.MULTILINE`). Lint yapılandırmasıyla birlikte T1.9'da ele alınır.

**Ortam**
- Demo veritabanı `ov_demo`: `odoo-bin db init --with-demo --language tr_TR --country TR` (20 sn), ardından `-i account,l10n_tr` (37 sn).
- Günlükte tek uyarı: `markdown2` kurulu değil. Upstream'in hiçbir bağımlılık dosyasında yok; posta eklerinde markdown gösterimi için isteğe bağlı.
- Kabul:
  - giriş sayfası Türkçe (`Giriş`, `Şifre`, `E-posta`); admin oturumu `tr_TR`, `Europe/Istanbul`;
  - başsız Chrome ile (geçici profil) fatura listesi ve hesap planı ekranları açıldı, JS hatası yok, başlıklar `Faturalar` ve `Hesap Planı`;
  - `TR Company`: ülke TR, para birimi TRY, hesap planı `tr` (ekranda 343 satır), 44 vergi, Türkçe yevmiyeler (`Satışlar`, `Satınalma`, `Banka`, `Kasa` …), 1.046 vergi dairesi.
- Upstream demo düzeni: ana şirket (`YourCompany`, ülke TR) genel hesap planıyla ve USD ile gelir; Türk hesap planı ayrı demo şirketi `TR Company`'de. Kendi demo verimiz (T8.3) Türk şirketiyle başlayacak.

**Araştırma**
- PDF motoru: 20.0'da eklentili.
  - `base_report_wkhtmltox` kendiliğinden kurulur, ama wkhtmltopdf GitHub deposu arşivde (son push 2022-11-22).
  - `base_report_paper_muncher` Odoo'nun yeni motoru (LGPL-3, son sürüm v0.9.0, 2026-10-06); yalnız Linux paketleri var.
  - Yerelde kurulmadı; seçim T2.5'e not edildi.
- `l10n_tr` veri kalitesi gözlemleri T3.1'e not edildi: Türkçe büyük harf hatası, İngilizce kalan hesap ve vergi adları, çevrilmemiş sütun başlığı.
- Marka: giriş sayfasının başlığı `Odoo` (T2.2 kapsamında).

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 yerel Odoo), PLAN.md (T1.6, pano, T2.5 ve T3.1 notları), README.md, state.json.
- ARCHITECTURE §2 ağacında T1.3'te eklenen `tools/pg.py` eksikti; eklendi.

### Adım: Python sanal ortamı (T1.5) — otonom mesai 1

**Kod**
- `requirements-dev.txt` eklendi: upstream `requirements.txt`'yi içerir (`-r upstream/odoo/requirements.txt`), üstüne `ruff==0.16.10` (upstream `ruff.toml` 0.16 için yazılmış) ve `websocket-client==1.9.2` (HttpCase tarayıcı testleri `odoo/tests/common.py` içinde `websocket` içe aktarıyor).

**Ortam**
- Depoda `.venv` (Python 3.12.10, git'e girmez). Kurulum: `pip install --prefer-binary -r requirements-dev.txt`; `pip check` temiz.
- Kabul: `odoo-bin --version` → `Odoo Server 20.0`.
- Windows'ta upstream işaretleri yüzünden `gevent`, `greenlet`, `python-magic`, `python-ldap` kurulmaz. Yerel geliştirme iş parçacıklı sunucuyla yapılır; gevent/çok süreçli mod ve LDAP Linux'ta (CI, üretim) sınanır.

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md §5, COMPLIANCE.md §5 (ruff MIT, websocket-client Apache-2.0, upstream Python bağımlılıkları notu), PLAN.md (T1.5, pano, T8.4'e lisans dökümü notu), README.md, state.json.

### Adım: Upstream Odoo submodule (T1.4) — otonom mesai 1

**Kod**
- Odoo 20.0 Community `upstream/odoo` altına sığ git submodule olarak eklendi. Sabit commit `afbcf79d` (2026-10-18), T1.2 denemesinin yapıldığı commit.
  - `.gitmodules`: `branch = 20.0`, `shallow = true`, adres GitHub.
  - İndirme süresini kısaltmak için ilk klon yerel inceleme kopyasından alındı, sonra adres GitHub'a çevrildi (`git submodule set-url`, `sync`).
  - Kabul: depo temiz bir klasöre klonlandı; `git -c core.longpaths=true submodule update --init --depth 1` GitHub'dan sabit commit'i sığ olarak getirdi, çalışma ağacı temiz.
  - İlk deneme `-c core.longpaths=true` olmadan "Filename too long" ile düştü: süper depodaki `core.longpaths` ayarı alt modülün klonuna geçmiyor. CLAUDE.md komutu buna göre yazıldı.
- Yerel depoda `core.longpaths` açıldı (Windows yol uzunluğu, R11).

**Belgeler**
- docs/COMPLIANCE.md §5: lisans envanterine ilk satır (Odoo Community 20.0, LGPL-3, değiştirilmedi).
- CLAUDE.md: "Ortam" (upstream durumu) ve "Komutlar" (yeni klonda submodule komutu).
- ARCHITECTURE.md §2: `upstream/odoo` satırı. README.md: durum.
- PLAN.md: T1.4 `[x]`; F1 4/11; toplam 12/114; şu anki görev T1.5.
- state.json: `upstream` (yol, commit, tarih, `in_project: true`); T1.4 bitenlere eklendi.

### Adım: Sürüm doğrulaması (T1.2) — otonom mesai 1

19.0'daki Nilvera ve OCA modülleri 20.0'da gerçekten kurulup test edildi. Üç ağaç ölçüldü: değişmemiş kod, Odoo'nun otomatik dönüştürücüsü (`upgrade_code`) ve elle uyarlama.

**Araştırma**
- Yeni: `docs/research/nilvera-port.md`. Sonuçlar:
  - 19 modülden 18'i 21 tür küçük uyarlamayla kuruluyor; 268 testin 243'ü geçiyor. Elle değişiklik 36 dosya, +96/−145 satır.
  - Otomatik dönüştürücü tek başına 2/19 modülü kurulabilir yapıyor; Windows'ta düzgün çalışmıyor (yol ayırıcı, kodlama).
  - En büyük kalan kalem `account_financial_report`: 20.0'da `account.group` modeli yok (T5.4).
  - Gerçek davranış farkı: `is_company` artık vergi numarasından hesaplanıyor; Türkiye'de 11 haneli TCKN gerçek kişi sayılmalı (T4.3).
  - Kalan ek emek yaklaşık 9–15 oturum; mevcut port görevlerinin içinde.
  - 20.0 taze: Community çekirdeğinde UBL içe aktarma hatası (`deferred_start_date`) görüldü.
  - Windows'ta 20.0 test temizliği salt okunur filestore dosyalarını silemiyor; referans test ortamı Linux CI.
  - OCA geçiş gecikmesi (17.0–19.0): altyapı modülleri 0–3 ay, banka mutabakatı, cari ekstre ve kalite 4–14 ay.

**Kararlar**
- **D-011** Geçerli kaldı (**20.0**). Gerekçesine ölçüm sonucu eklendi; kabul edilen bedele `account_financial_report` ve 20.0'ın tazeliği eklendi.
  - Eski "Yeniden değerlendirme" satırı: "T1.2. İlk tahmin, MVP'nin OCA modülüne ihtiyacı olmadığı varsayımına dayanıyordu. D-018 ile bu varsayım değişti. Port maliyeti, upstream eklenmeden önce ölçülür. 20.0'ın maliyeti çok yüksek çıkarsa 19.0 seçeneği yeniden açılır."
  - Yeni hali: planlı nokta yok; yalnız 20.0 çekirdeğinde MVP'yi engelleyen, modülle aşılamayan ve upstream'de üç ay içinde düzelmeyen bir hata olursa yeniden açılır.
  - Neden: port maliyeti ölçüldü ve küçük çıktı. 19.0'da kalmak işi yalnız Eylül 2028'deki zorunlu göçe erteliyor.

**Belgeler (düzeltme)**
- Planlama adımındaki "`mis_builder`, `mis_builder_budget` ve `queue_job` 20.0'da var" bilgisi yanlıştı. Bu modüller OCA'nın 20.0 dalında yalnız yer tutucu (`installable: False`, sürüm 19.0).
  - Eski metin (planning-inputs.md §1): "`mis_builder`, `mis_builder_budget` | mis-builder | **var** | var | Doğrudan `vendor/` (T5.5)" ve "`queue_job` | queue | **var** | var | Gerekirse doğrudan `vendor/`".
  - Eski metin (PLAN.md T5.5): "OCA `mis_builder` (20.0'da mevcut) ile Tekdüzen şablonları".
  - Eski metin (MODULE_MATRIX.md): bilanço satırı "OCA (20.0 resmî)", bütçe satırı "`mis_builder_budget`, 20.0'da var".
  - Neden: o sayım OCA dallarındaki klasörlere bakıyordu; kurulabilirlik denetlenmemişti. Düzeltilen yerler: planning-inputs.md §1 (düzeltme notu ve tablo), MODULE_MATRIX.md (not ve iki satır), PLAN.md T5.5.
  - Ayrıca `account_statement_base`'in deposu düzeltildi: bank-statement-import değil, account-reconcile.
- PLAN.md: T1.2 `[x]`; F1 3/11; toplam 11/114; şu anki görev T1.4. R1 riski ölçüme göre güncellendi (olasılık D, etki O). T1.8, T4.3, T5.4 ve T5.5'e T1.2 bulguları eklendi.
- ARCHITECTURE.md: D-011 "T1.2'de doğrulandı". README.md: durum ve sıradaki görev.
- state.json: T1.2 bitenlere eklendi; şu anki görev T1.4; D-011'den `revisit` kaldırıldı; belge listesine `nilvera-port.md`.

### Adım: PostgreSQL kurulumu (T1.3) — otonom mesai 1

Otonom mesai 1 başladı (D-021). T1.3, T1.2'den önce yapıldı: T1.2'deki port denemesi (19.0 modüllerini 20.0'da kurup test etmek) çalışan bir PostgreSQL gerektiriyor.

**Ortam**
- PostgreSQL 18.6 kuruldu. Yönetici izni gerektirmeyen yol: EDB'nin Windows taşınabilir ikili zip'i, depo dışında `%LOCALAPPDATA%\odoo-version` (`OV_HOME`) altında.
  - Küme: UTF-8, `C.UTF-8` yerleşik yerel ayar, scram-sha-256 kimlik doğrulama, yalnız `localhost:5432`.
  - Sunucu kullanıcı hesabında çalışır. Windows hizmeti değildir; bilgisayar yeniden başlayınca `python tools/pg.py start` gerekir.
  - Rol `odoo` (LOGIN CREATEDB). Bağlantı bilgileri depodaki `.env` dosyasında (git'e girmez, D-015).
  - Kabul doğrulandı: `psql --version` 18.6; `odoo` rolüyle bağlantı kuruldu.
- Sürüm seçimi 18: Odoo 20.0'ın alt sınırı 16 (`odoo/release.py`); 18, CI ve olası Ubuntu sunucusunun paket sürümleriyle uyumlu.
- T1.2 için depo dışında inceleme kopyaları indirildi (`OV_HOME/src`): Odoo 20.0 (sığ klon, `afbcf79`), Odoo 19.0'ın yalnız `l10n_tr*` modülleri, ilgili OCA depolarının 19.0 ve 20.0 dalları.

**Kod**
- Yeni: `tools/pg.py` — yerel kümenin kurulumu ve yönetimi (`init`, `start`, `stop`, `status`).
  - Sunucu, çağıranın çıktı kanallarını devralmayacak biçimde başlatılır. Aksi halde çıktıyı bekleyen kabuk sunucu kapanana kadar takılıyordu (ilk denemede görüldü).

**Belgeler**
- PLAN.md: T1.3 `[x]`; F1 2/11; toplam 10/114.
- CLAUDE.md: "Ortam" (PostgreSQL) ve "Komutlar" (`tools/pg.py`).
- ARCHITECTURE.md §5: yerel PostgreSQL düzeni.
- docs/COMPLIANCE.md §5: depoya girmeyen geliştirme araçları tablosu; PostgreSQL satırı.
- state.json: `environment.postgresql`, T1.3 bitenlere eklendi.

### Adım: commit yazarlığı, kullanıcı belgesi, mesai türleri ve görev kategorileri

Kullanıcı istekleri:
- GitHub'da tek katkıcı kullanıcı olacak; Claude ortak yazar olarak yazılmayacak. Kural CLAUDE.md'ye girecek.
- Kullanıcıdan beklenenler için ayrı bir belge.
- İki mesai türü: standart (birlikte) ve otonom (Claude tek başına, kullanıcı ekran başında değil).
- Görevlerin tümü üç kategoride: kullanıcının yapacakları, birlikte yapılacaklar, Claude'un yapacakları.

**Kararlar**
- **D-015** güncellendi. Eski hali: commit yazarlığı hakkında kural yoktu; ilk iki commit'e `Co-Authored-By: Claude` satırı eklenmişti. Yeni hali: commit yazarı kullanıcının git kimliği; Claude'u yazar veya ortak yazar gösteren satır yazılmaz. Neden: kullanıcı bunu hata olarak bildirdi. Geçmiş iki commit'in temizlenmesi force-push gerektirdiği için kullanıcı kararına bırakıldı (USER_TASKS K10).
- **D-003** güncellendi. Eski hali: mesai türleri yoktu. Yeni hali: çalışma standart ve otonom mesailerle yürür; otonom mesaide sorular `USER_TASKS.md`'ye yazılır.
- **D-021** yeni, Geçerli: mesai türleri ve görev kategorileri (K / B / C); otonom mesai kuralları. Mesai türleri ve kategoriler kullanıcıdan, otonom kuralların ayrıntısı Claude'dan.

**Belgeler**
- Yeni: **`USER_TASKS.md`** — kullanıcı eylemleri, kararları ve onayları; K ve B görevlerinde kullanıcının payı; mesai türleri özeti.
  - PLAN.md §10'daki K1–K5, K8, K9 buraya taşındı.
  - K6 (müşteri listesi) ve K7 (yasal yapı) kaldırıldı; aynı işi anlatan T9.1 ve T9.3 görevleri kullanıldı.
  - Yeni: K10 (geçmiş commit'lerdeki ortak yazar satırı), K11 (`Claude-Session:` satırı).
- PLAN.md:
  - "Sorumlu" alanı "Kategori" oldu: C+K → **B**; K ve C aynı.
  - T10.4 C → B (ödeme sağlayıcısı hesabı kullanıcıda).
  - Yeni görev **T7.9 Kullanıcı kabul turu** (B). F7 kabulündeki elle tur bu göreve bağlandı. Toplam 113 → 114 görev.
  - Panoya "K · B · C" sütunu ve toplam satırına kategori sayıları eklendi: Kullanıcı 3 · Birlikte 13 · Claude 98.
  - T1.3: "gerekirse kullanıcıdan yönetici izni" yerine yönetici izni gerektirmeyen kurulum yolu.
  - §10 artık `USER_TASKS.md`'ye yönlendiriyor.
- CLAUDE.md: kural 8 (commit yazarlığı); "Mesai türleri" bölümü; belge haritasında `USER_TASKS.md`; protokol adım 3 ve 8.
- state.json: `session` alanı (otonom mesai 1), `project.user_tasks`, `project.commit_author`, D-021, belge listesinde `USER_TASKS.md`.
- README.md, ARCHITECTURE.md: `USER_TASKS.md` eklendi.
- `tools/check_docs.py`: görev kategorisi denetimi (K/B/C); panodaki ve toplam satırındaki kategori sayıları; `USER_TASKS.md`'deki K/B görev listesinin ve işaretlerinin PLAN ile aynılığı; tanımsız `K<n>` atıfları.

### Adım: detaylı planlama (T0.8)

Kullanıcı D-016'yı onayladı ve planlama kararlarını Claude'a bıraktı. Verdiği perspektif şöyle:
- öğrenci projesi, sıfır bütçe;
- bütçesiz, desteksiz ve müşterisiz alınabilecek tüm ilerleme alınınca müşteri arayışı;
- ilk müşteriler küçük işletmeler ve orta ölçekli fabrikalar; her satıştan sonra bir üst ölçek.

**Kararlar**
- **D-016** Açık → **Geçerli: AGPL-3.**
  - Eski hali: seçenekler A (AGPL-3) / B (LGPL-3) / C (kapalı) / D (karma), Claude önerisi "A, gerekirse D"; karar noktası T2.2.
  - Neden: kullanıcı öneriyi onayladı; depo ileride private yapılabilir, şimdilik AGPL-3.
  - Eklenenler: depo kökünde `LICENSE`; LGPL türevleri LGPL-3; OCA portları orijinal lisansla; private'a geçişin sınırları; dış katkı şimdilik kabul edilmiyor.
- **D-011** (20.0 kaldı, gerekçe ve tetikleyici değişti).
  - Eski metin: "MVP'nin (P0) hiçbir OCA modülüne ihtiyacı yok." Yeniden değerlendirme T3.1 (Nilvera port analizi). Submodule T1.3'te.
  - Yeni hali: bu varsayım D-018 ile geçersiz kaldı (mali raporlar, mutabakat, ekstre, kalite modülleri OCA'da yalnız 19.0'da). Yeniden değerlendirme **T1.2**: port maliyeti upstream eklenmeden önce ölçülür. Submodule T1.4'te. Gerekçeye "ilk müşteriler büyük olasılıkla 2027'de" eklendi.
- **D-012** (kullanıcının onayladığı kapsam genişletildi).
  - Eski metin: "MVP kapsamı: e-Fatura + e-Arşiv. e-İrsaliye MVP sonrası (P1), e-Defter ileride." Yeniden değerlendirme T6.1.
  - Yeni hali: MVP = e-Fatura + e-Arşiv + **e-İrsaliye** (P0). e-Defter P1 (T11.4); MVP'de mali müşavire aktarım (T5.9). Diğer e-Belgeler P3. Mimariye sahte (mock) adaptör eklendi. Yeniden değerlendirme **T8.1**.
  - Neden: hedef segmentteki orta ölçekli fabrikalar için e-İrsaliye zorunlu (e-Fatura mükellefi ve hasılat ≥ 10 Milyon TL); sevkiyat ve fason üretim e-İrsaliye gerektiriyor.
- **D-013** (Ertelendi kaldı, kapsamı daraldı).
  - Eski başlık: "Barındırma ve dağıtım modeli". Karar noktası T6.3.
  - Yeni başlık: "**Üretim barındırma yeri**". Teslim biçimi D-018'e taşındı. Karar noktası **T9.5**. "İlk müşteri on-prem seçerse daha da ertelenebilir" eklendi.
- **D-014**: yeniden değerlendirme T6.1 → **T8.1**; kalıcı adın uygulanması T8.2. OCA portları için teknik ad istisnası eklendi (D-019).
- **D-017** yeni, Geçerli: hedef müşteriler ve aşama stratejisi; müşteri arayışı kapısı M8. Yeniden değerlendirme T9.8.
- **D-018** yeni, Geçerli: MVP tanımı (Ticaret ve Üretim paketleri), öncelik tanımları (P0–P5), MVP dışı liste, teslim biçimi (yönetilen kurulum; self-servis SaaS F10). Yeniden değerlendirme T8.1.
- **D-019** yeni, Geçerli: OCA modülleri — resmî 20.0 `vendor/oca/`, yoksa 19.0'dan port `ports/oca/` (orijinal ad, lisans ve yazarlar).
- **D-020** yeni, Geçerli: ücretsiz altyapı — GitHub Actions, GitHub Pages (yalnız açık kaynak belgeler), Cloudflare Quick Tunnel (demo), Nilvera test portalı, Student Pack (isteğe bağlı).
- Küçük metin güncellemeleri:
  - **D-002:** "İlk satışa çıkan kapsam D-018'dedir" eklendi.
  - **D-005:** "Ücretsiz kaynaklar D-020'de" eklendi.
  - **D-008/3** eski metin: "AGPL-3 OCA modülleri ayrı tutulur. Değiştirilirse, SaaS kullanıcılarına değiştirilmiş kaynak sunulur." Yeni hali: 20.0 portları da (D-019) bu kapsamda.
  - **D-008/4** eski metin: "Kapalı kaynak (kendi lisansımızla) modüllerimiz AGPL modüllere bağımlı olamaz. Kapalı modül olup olmayacağı D-016'ya bağlı." Yeni hali: şu an kapalı modül yok; kendi modüllerimiz AGPL-3.
  - **D-008/5** eski metin: "her 3. parti modül". Yeni hali: "her 3. parti kod ve veri".
  - **D-010:** OCA portlarının yeri (`ports/`) eklendi.
  - DECISIONS.md giriş notu: tetikleyiciler artık "ROADMAP görevine" değil, "PLAN.md'deki bir göreve" bağlanır.

**Belgeler**
- `ROADMAP.md` → **`PLAN.md`** (yeniden adlandırıldı ve baştan yazıldı). İçerik:
  - ilerleme panosu;
  - strateji, paketler ve Türkiye gereksinimleri;
  - 12 faz (F0–F11), 113 görev; her görevde büyüklük, sorumlu ve kabul ölçütleri;
  - sürekli işler, ücretsiz kaynaklar, test stratejisi, risk kaydı, kullanıcı eylemleri (K1–K9).
- Eski → yeni görev numaraları:
  - eski T0.8 → T0.8 (tamamlandı);
  - eski T1.2–T1.7 → T1.3, T1.4, T1.5, T1.6, T1.7, T1.8; yeni T1.2 (sürüm doğrulaması), T1.9 (modül şablonu ve lint), T1.10 (CI), T1.11 (`vendor/` ve `ports/`);
  - eski T2.1–T2.4 → aynı numaralar; yeni T2.5–T2.7;
  - eski Faz 3 (e-Belge) → F4: eski T3.1 → T4.1, T3.2 → T4.3, T3.3 → T4.5, T3.4 → T4.6, T3.5 (e-İrsaliye, P1) → T4.8 (P0); eski T3.6 (SMS) → T11.5. Yeni F3: Türkiye temel yerelleştirmesi;
  - eski Faz 4 (Enterprise eşdeğerleri) → F5 (muhasebe P0 kısmı), F11 (T11.1 sabit kıymet, T11.10–T11.12 P2–P4 paketleri);
  - eski Faz 5 (SaaS) → F10 (T10.1–T10.7); eski T5.3 yedekleme → T8.5 (yönetilen kurulum için) + T10.5;
  - eski T6.1 → T8.1, T6.2 → T9.4, T6.3 → T9.5, T6.4 → T9.6.
- `LICENSE` eklendi (GNU AGPL v3, gnu.org resmî metni).
- DECISIONS.md: yukarıdaki kararlar; özet tablo; "Açık kararlar" bölümü boşaldığı için kaldırıldı.
- state.json: faz F1, şu anki görev T1.2; T0.8 tamamlandı; lisans, plan, hedef segmentler ve kilometre taşları; karar değerleri ve tetikleyicileri; `modules.ported`; yeni belge `docs/research/planning-inputs.md`.
- CLAUDE.md: proje özeti (paketler, lisans), belge haritasında PLAN.md, protokol 8 adım (PLAN işaretleri ve pano), kurallar 3–5 ve 7, ortam ve komutlarda yeni görev numaraları.
- README.md: durum, paketler, PLAN bağlantısı, lisans ve katkı bölümleri.
- ARCHITECTURE.md: durum notu, `vendor/` + `ports/` düzeni (D-019), modül tablosunda lisans sütunu ve yeni satırlar, teslim biçimi (D-018), geliştirme ortamı ve CI bölümü.
- docs/COMPLIANCE.md: lisans satırları AGPL-3; görev atıfları (T9.4, T8.2, T2.3, T2.7, T1.4); public depo kuralları (Nilvera bilgileri, GİB paketleri, CI gizli bilgi taraması, depo lisansı).
- docs/MODULE_MATRIX.md: yeni öncelik tanımları ve Paket sütunu; öncelikler paketlere göre yeniden belirlendi (ör. mrp, fason, bakım P0; e-İrsaliye P0; POS P2).
- docs/research/e-fatura.md: sonuç notu (e-İrsaliye MVP'de, e-Defter P1); §5 değerlendirme tablosu; yeni §6 "Planlama için ek bulgular"; kaynaklar; görev atıfları T6.1/T6.2 → T8.1/T9.4.
- docs/research/hosting.md: D-013'ün yeni başlığı ve kapsamı; Quick Tunnel sınırları; on-prem satırı (D-018); görev atıfları T6.2/T6.3 → T9.4/T9.5.
- docs/research/approach-b-vs-c.md: "ROADMAP T2.4" → "PLAN T2.4".
- Yeni: docs/research/planning-inputs.md (OCA 20.0 durumu, çeviri kapsamı, yerel 20.0 kontrolleri, ücretsiz kaynaklar, veri kaynakları, pazar referansları).
- `tools/check_docs.py`: ROADMAP yerine PLAN.md; yinelenen görev numarası, faz başlığı işaretleri, pano satırları, toplam satırı, "Şu anki görev" satırı ve `phase.id` denetimleri.

**Araştırma**
- OCA 20.0: `l10n-turkey` 18.0/19.0/20.0'da boş. Muhasebe, mutabakat, ekstre, kalite, MRP planlama ve sabit kıymet modülleri yalnız 19.0'da; `mis_builder`, `queue_job`, `remove_odoo_enterprise` 20.0'da var.
- 20.0 Türkçe çeviri kapsamı ölçüldü: çekirdek modüller %79–93; `l10n_tr` %33.
- Ücretsiz kaynakların koşulları: GitHub Actions, GitHub Pages (ticari kullanım yasağı), Cloudflare Quick Tunnel sınırları, Student Pack, TÜBİTAK 2209-A (son başvuru 11 Kasım 2026).
- e-Belge: Nilvera kamuya açık test ortamı; GİB doğrudan testi mali mühür gerektiriyor; 2026 UBL-TR paket güncellemeleri; Ba-Bs formlarının Eylül 2024'ten itibaren kaldırılması; e-Defter geçiş kuralı (ikincil kaynaklar).
- Veri kaynakları: TCMB günlük kur XML; il/ilçe listesi (MIT lisanslı aday).

### Adım: kullanıcı kararları (T0.7) ve git/GitHub deposu (T1.1)

**Kararlar**
- **D-010** Açık → Geçerli: **B** (kullanıcı). Eski hali: seçenekler B / C / B+, Claude önerisi B+. Neden: kullanıcı yama kuyruğu olmayan B'yi seçti; `patches/` kaldırıldı. Modülle çözülemeyen durum yeni karar olarak gelecek.
- **D-011** Açık → Geçerli: **20.0**. Eski hali: seçenekler 20.0 / 19.0 / 18.0, öneri 20.0. Neden: kullanıcı kararı Claude'a bıraktı. Yeniden değerlendirme T3.1'e bağlandı.
- **D-012** Açık → Geçerli. Eski hali (öneri): e-Fatura + e-Arşiv MVP, özel entegratör API, Nilvera 19.0 port. Neden: kullanıcı kapsamı ve yöntemi onayladı ve "MVP sonunda tekrar ele alırız" dedi. Yeniden değerlendirme T6.1'e bağlandı.
- **D-013** Açık → **Ertelendi**. Eski hali (öneri): aşamalı SaaS (lokal → ücretsiz demo → Türkiye VPS; on-prem ileride). Neden: kullanıcı "hemen karar vermeli miyiz?" diye sordu. Cevap: hayır, gerçek müşteri verisine kadar gerekmiyor. Karar noktası T6.3. Geçici düzen: lokal geliştirme ve sağlayıcıdan bağımsız mimari.
- **D-014** Açık → Geçerli. Eski hali: marka adı ve önek belirlenmemiş. Neden: kullanıcı çalışma adını `odoo-version` olarak verdi (MVP sonunda değişecek). Claude öneki markadan bağımsız ve kalıcı `ov_` olarak seçti. Yeniden değerlendirme T6.1.
- **D-015** Açık → Geçerli. Eski hali (öneri): yerel git, push yalnız onayla. Neden: kullanıcı public GitHub deposu ve her görev sonunda commit + push istedi; push önceden onaylı hale geldi.
- **D-016** yeni, Açık: kendi modüllerimizin lisansı. Neden: public depo, kod yayımlanmadan önce lisans seçimini gerektiriyor. Öneri AGPL-3 (+ gerekirse private depo). Karar noktası T2.2.
- **D-003** güncellendi. Eski metin: "dışa dönük işlemler (yayınlama, paylaşma, uzak depoya push)" kullanıcıya sorulur. Yeni hali: proje deposuna push D-015 ile önceden onaylı; yayınlama, paylaşma ve depo ayarları yine sorulur.
- **D-008/1** güncellendi. Eski metin: "Upstream Odoo Community (LGPL-3) değiştirilirse değişiklikler LGPL-3 kalır." Yeni hali: upstream değiştirilmez (D-010). Madde 4'e D-016 bağlantısı eklendi.
- Karar durumlarına **Ertelendi** eklendi. `**Karar noktası:**` ve `**Yeniden değerlendirme:**` satırları ROADMAP görevlerine bağlandı.

**Belgeler**
- DECISIONS.md yeniden yazıldı (yukarıdaki kararlar).
- ROADMAP.md:
  - T0.7 ve T1.1 tamamlandı.
  - Yeni T0.8: detaylı planlama.
  - Faz 6 yeniden numaralandı. Yeni T6.1 MVP sonu değerlendirmesi; eski T6.1 → T6.2 (hukuki inceleme), eski T6.2 → T6.3 (artık "Üretim barındırma kararı (D-013) ve üretim sunucusu"), eski T6.3 → T6.4.
  - T2.4 B'ye göre yeniden yazıldı.
  - Faz başlıklarındaki karar ön koşulları güncellendi.
- ARCHITECTURE.md:
  - Durum notu: B / 20.0 / `ov_` Geçerli.
  - `patches/` kaldırıldı.
  - Önek `ov_`; lisans sütunu D-016'ya bağlandı.
  - Konum ertelendi ve sağlayıcıdan bağımsızlık kısıtı eklendi.
  - `.gitignore` / `.gitattributes` eklendi.
- CLAUDE.md:
  - proje özeti;
  - protokol adım 3 (karar noktası görevleri) ve adım 7 (commit + push);
  - kurallar 2–7;
  - ortam (gh, git deposu) ve komutlar.
- COMPLIANCE.md: kendi modüllerimizin lisansı → D-016; çalışma adı ve marka notu; public depo kuralları; T6.1 → T6.2.
- MODULE_MATRIX.md: "Karar verilecek" lisanslar → D-016; AGPL notu.
- research/approach-b-vs-c.md, research/e-fatura.md: başa "Sonuç" notu eklendi; T6.1 → T6.2.
- research/hosting.md:
  - "Sonuç", "Karar ne zaman gerekli?" ve "Benzer platformlar nerede çalışıyor?" bölümleri eklendi;
  - "Öneri" başlığı "Ön öneri" oldu;
  - T6.1 → T6.2.
- README.md: durum, çalışma adı, lisans notu.
- `tools/check_docs.py`:
  - "Ertelendi" durumu;
  - ertelenmiş kararda karar noktası zorunluluğu;
  - karar noktası veya yeniden değerlendirme görevi tamamlanmışsa hata;
  - belgelerde (CHANGELOG hariç) ROADMAP'te olmayan görev numarasına atıf denetimi.

**Araştırma**
- Benzer platformların barındırma yerleri incelendi:
  - Odoo Online / Odoo.sh: OVHcloud, Google Cloud, AWS; Türkiye bölgesi yok.
  - Frappe Cloud: AWS ve Oracle Cloud; Türkiye bölgesi yok.
  - Paraşüt aydınlatma metni: yurt dışı aktarım açık rızayla.
  - Logo: Cloud + Edge karma modeli.

**Ortam**
- Git deposu başlatıldı (`main`), `.gitignore` ve `.gitattributes` eklendi.
- Public GitHub deposu oluşturuldu: https://github.com/burak-sisci/odoo-version

### Adım: ilk belgeler (T0.1–T0.6)

**Kararlar**
- Geçerli olarak eklendi: D-001 ürün hedefi, D-002 kapsam, D-003 ekip/çalışma modeli, D-004 dokümantasyon protokolü (kullanıcı); D-005 sıfır bütçe (kullanıcı, 2026-10-16); D-006 clean-room, D-007 marka, D-008 lisans uyumu (hukuki zorunluluk); D-009 dil (Claude varsayılanı).
- Açık olarak eklendi (Claude önerileriyle): D-010 yaklaşım (öneri B+), D-011 sürüm (öneri 20.0), D-012 e-Belge stratejisi, D-013 barındırma, D-014 marka adı/önek, D-015 git/commit yetkisi.

**Araştırma**
- B / C yaklaşım karşılaştırması (marka izleri envanteri, Flectra örneği).
- e-Fatura / e-Arşiv / e-İrsaliye: GİB 509 Tebliğ güncel metni (589 değişiklikleri dahil) incelendi. Önemli bulgu: 1/1/2026'dan itibaren bilanço esaslı mükellefler tutardan bağımsız e-Arşiv/e-Fatura düzenlemek zorunda.
- Odoo 20.0'da Nilvera e-Belge modüllerinin Enterprise'a taşındığı, 19.0'da LGPL olduğu doğrulandı.
- OCA modül sayıları 18.0 / 19.0 / 20.0 dalları için çıkarıldı; OCA lisans örnekleri (çoğu AGPL-3).
- Barındırma seçenekleri; KVKK m.9 (7499 sayılı Kanun) ve e-Belge yurt içi saklama kuralı.

**Belgeler**
- Oluşturuldu: CLAUDE.md, README.md, ARCHITECTURE.md, DECISIONS.md, ROADMAP.md, CHANGELOG.md, state.json, docs/COMPLIANCE.md, docs/MODULE_MATRIX.md, docs/research/{odoo-analysis, approach-b-vs-c, e-fatura, hosting}.md.
- Belge tutarlılık denetimi eklendi: `tools/check_docs.py`.

## 2026-10-16

**Araştırma**
- Odoo 20.0 Community kaynak kodu indirildi ve incelendi (commit `1740e969`): 657 modül, 34 uygulama, tamamı LGPL-3; mimari, ORM, web istemcisi, `skills/` klasörü.
- Lisanslar (Community LGPL-3, Enterprise özel lisans) ve edinme yolları (sıfırdan klon / Community + modüller / çatal / kendi küçük ERP'miz) değerlendirildi.
