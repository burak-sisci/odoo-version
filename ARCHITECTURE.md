# Mimari

Son güncelleme: 2026-10-19

> **Durum: Hedef mimari.**
> - Dayandığı Geçerli kararlar:
>   - D-010 (yaklaşım **B**), D-011 (sürüm **20.0**; T1.2'de doğrulandı), D-014 (önek `ov_`);
>   - D-016 (lisans **AGPL-3**, LGPL türevleri LGPL-3), D-018 (paketler ve teslim biçimi), D-019 (OCA portları), D-020 (ücretsiz altyapı).
> - Üretim barındırma yeri D-013 ile ertelendi (§4).
> - Kendi modüllerimiz `addons/` altında (T2.2'den beri; güncel liste `state.json` → `modules.ours`). OCA depoları `vendor/oca/server-ux` (T1.11) ve `vendor/oca/server-brand` (T2.3), ilk OCA portu `ports/oca/reporting-engine/report_xlsx` (T1.11).
> - Bu belge kurulacak yapıyı tanımlıyor. Görevler `PLAN.md`'de.

## 1. Genel bakış

Ürün = **değiştirilmemiş Odoo Community** + **seçilmiş OCA modülleri (resmî veya bizim 20.0 portumuz)** + **kendi modül katmanlarımız** + **kurulum ve işletim araçları**.

```
┌─────────────────────────────────────────────────────────────────────┐
│ Bizim katmanlarımız (addons/)                                       │
│  ┌───────────────┐ ┌──────────────────┐ ┌───────────────────────┐   │
│  │ Marka katmanı │ │ Türkiye uyumu    │ │ Enterprise eşdeğerleri│   │
│  │ (debranding,  │ │ (e-Fatura,       │ │ (muhasebe, helpdesk,  │   │
│  │  phone-home   │ │  e-Arşiv,        │ │  onaylar, ... —       │   │
│  │  kapatma)     │ │  e-İrsaliye ...) │ │  clean-room)          │   │
│  └───────────────┘ └──────────────────┘ └───────────────────────┘   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ SaaS yönetimi (kiracı oluşturma, abonelik, yedek, izleme)     │  │
│  └───────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│ OCA modülleri: vendor/oca/ (resmî, dokunulmaz) + ports/oca/ (port)  │
├─────────────────────────────────────────────────────────────────────┤
│ Odoo Community (upstream/odoo) — sabit commit, DEĞİŞTİRİLMEZ        │
└─────────────────────────────────────────────────────────────────────┘
```

**Değişiklik yöntemi (D-010, B):** upstream'in hiçbir dosyası değiştirilmez, yama kuyruğu yoktur. Her değişiklik `addons/` altındaki modüllerle (OCA portları için `ports/`) yapılır:
- model kalıtımı (`_inherit`);
- görünüm kalıtımı (XPath);
- JS `patch()` ve asset paketinde dosya değiştirme (`replace`);
- controller override;
- gerekirse modül içinden monkey-patch (gerekçesi kodda yazılı).

Modülle çözülemeyen bir durum kullanıcıya yeni karar olarak getirilir.

## 2. Depo yerleşimi (planlanan)

```
odoo-version/
├── CLAUDE.md  README.md  PLAN.md  USER_TASKS.md  ARCHITECTURE.md  DECISIONS.md  CHANGELOG.md  state.json
├── LICENSE                  # GNU AGPL v3 (D-016)
├── .gitignore  .gitattributes   # gizli bilgiler ve yerel veriler depoya girmez; satır sonu LF
├── ruff.toml  .pylintrc  .pre-commit-config.yaml   # lint kuralları ve commit öncesi denetimler (T1.9)
├── .github/                 # CI (T1.10): workflows/ci.yml; actions/submodules/ (alt modüller ve önbelleği, T1.11)
├── .claude/skills/          # Odoo'nun AI rehberleri, upstream'den değiştirilmeden kopya (LGPL-3, T1.7)
├── docs/
│   ├── COMPLIANCE.md        # lisans, clean-room, marka, KVKK
│   ├── MODULE_MATRIX.md     # tüm uygulamaların planı ve durumu
│   ├── specs/               # Enterprise eşdeğerleri için clean-room işlev tanımları
│   └── research/            # tarihli araştırma kayıtları
├── tools/
│   ├── check_docs.py        # belge tutarlılık denetimi (ileride ayrı araçlar: UBL doğrulama, çeviri ölçümü)
│   ├── pg.py                # yerel PostgreSQL kümesi: init, start, stop, status (T1.3)
│   ├── odoo_conf.py         # yerel odoo.conf'u şablondan ve .env'den üretir (T1.6)
│   ├── sync_skills.py       # upstream skills/ → .claude/skills/ kopyası ve fark denetimi (T1.7)
│   ├── run_tests.py         # temiz veritabanında modül testleri, Windows gc hatalarını ayırır (T1.8)
│   ├── new_module.py        # addons/ altında yeni modül iskeleti (T1.9)
│   ├── check_modules.py     # modüllerimizin proje kuralları: önek, lisans, sürüm, yazar, marka (T1.9)
│   ├── check_secrets.py     # staged değişikliklerde .env değerleri; pre-commit kancası (T1.10)
│   └── port_oca.py          # OCA modülünü ports/'a alır, upgrade_code'u porta uygular, kaynakla fark (T1.11)
├── upstream/odoo/           # Odoo Community 20.0, sığ git submodule, sabit commit (state.json → upstream)
├── vendor/oca/<depo>/       # OCA'nın resmî 20.0 depoları, sığ git submodule, sabit commit (server-ux T1.11, server-brand T2.3)
├── ports/oca/<depo>/<modül>/  # OCA 19.0 modüllerinin bizim 20.0 portlarımız, her birinde PORT.md (ilk: reporting-engine/report_xlsx)
├── addons/                  # bizim modüllerimiz, önek ov_ (liste: state.json → modules.ours; iskelet tools/new_module.py)
└── deploy/                  # odoo.conf.example (T1.6); kurulum aracı, ters vekil, yedek betikleri (henüz yok — T8.4)
```

Kurallar:
- `upstream/` ve `vendor/` altındaki dosyalar elle düzenlenmez (D-010). Değişiklik `addons/` ve `ports/` altında.
- Addons yolu sırası: `upstream/odoo/addons`, `upstream/odoo/odoo/addons`, `vendor/oca/*`, `ports/oca/*`, `addons`.
- Sürüm yükseltme = sabit commit'i ilerletmek + testler.
- Depo public (D-015): gizli bilgi, müşteri verisi, yerel yapılandırma (`odoo.conf`, `.env`) depoya girmez.

### OCA port düzeni (D-019)

- OCA'nın resmî 20.0 sürümü varsa `vendor/oca/<depo>` kullanılır:
  - depo sığ git submodule olarak eklenir (`.gitmodules`: `branch = 20.0`, `shallow = true`), sabit commit'te durur, dokunulmaz;
  - ekleme: `git clone --depth 1 --branch 20.0 <url> vendor/oca/<depo>` → `git submodule add -b 20.0 <url> vendor/oca/<depo>` → `git submodule absorbgitdirs`. Doğrudan `git submodule add --depth 1 -b 20.0` dalı bulamıyor (sığ klon yalnız varsayılan dalı çekiyor).
- Yoksa 19.0 sürümü `ports/oca/<depo>/<modül>` altına kopyalanıp 20.0'a taşınır:
  - teknik ad, lisans, yazarlar ve telif notları korunur;
  - kaynak commit modül klasöründeki `PORT.md` notunda ve lisans envanterinde yazılır;
  - OCA'nın taşıma kurallarına uyulur. Ör. ilk sürüm `20.0.1.0.0`: OCA'nın resmî sürümü ve göç betikleri portun ardından boşluksuz gelir.
- OCA resmî 20.0 sürümünü yayımlayınca port silinir ve `vendor/`'a geçilir. Teknik ad aynı olduğu için veritabanı göçü gerekmez.

**Port prosedürü (T1.11, `tools/port_oca.py`):**
1. Ön kontrol:
   - modül OCA'nın 20.0 dalında kurulabilir durumda mı (öyleyse `vendor/`);
   - bağımlılıkları addons yolunda mı (değilse önce onlar);
   - OCA'da açık taşıma PR'ı var mı: `gh pr list -R OCA/<depo> --base 20.0 --search <modül>`.
2. `python tools/port_oca.py fetch <depo> <modül>`:
   - OCA deposu geçici klasöre sığ ve seyrek klonlanır, yalnız modül kopyalanır. İndirilen dosyalardan hiçbiri çalıştırılmaz.
   - Manifest sürümü `20.0.1.0.0` olur, `PORT.md` yazılır (kaynak depo, dal, commit, lisans, yazarlar).
   - Lisans AGPL-3 veya LGPL-3 değilse araç durur (önce `docs/COMPLIANCE.md`).
3. `python tools/port_oca.py upgrade ports/oca/<depo>/<modül>`:
   - Odoo'nun `upgrade_code` betikleri (kaynak dalından sonraki sürümler ve Owl 3) yalnız porta uygulanır.
   - T1.2'de bulunan Windows sorunları araçta çözülür: yollar `/` ile, dosyalar UTF-8, yazma yalnız port klasörüne. `ir-access` betiği bağımlılık modüllerini okur, onlara yazılmaz.
   - Değişen dosya sayısı ve elle bakılacak uyarılar `PORT.md`'ye yazılır.
4. Elle uyarlamalar, `python tools/run_tests.py <modül>` geçene kadar:
   - her değişiklik `PORT.md` → "Değişiklikler" altında bir satır;
   - açık taşıma PR'ı varsa uyarlamalar onunla karşılaştırılır.
5. Python bağımlılığı upstream `requirements.txt`'de yoksa `requirements-dev.txt`'ye ve lisans envanterine eklenir.
6. Kayıt: `docs/COMPLIANCE.md` §5 satırı (kaynak commit, lisans, "değiştirildi"), `state.json` → `modules.ported`.
7. Gözden geçirme: `python tools/port_oca.py diff ports/oca/<depo>/<modül> [--stat]` kaynakla farkın tamamını gösterir.

- **Lint:** `vendor/` ve `ports/` OCA'nın kod biçiminde kalır. ruff, pylint-odoo ve modül kuralı denetimlerimiz yalnız `addons/` (T1.9). OCA'ya katkıda (K8) OCA'nın kendi pre-commit'i çalıştırılır.
- **Testler:** CI, `ports/` altındaki her modülün testlerini çalıştırır. `vendor/` modülleri yalnız bağımlılık olarak kurulur; testleri OCA'nın CI'ında.

## 3. Modül katmanları

Önek: `ov_` (D-014). Markadan bağımsızdır; marka değişince modül adları değişmez.

| Katman | Modül adı kalıbı | Görev | Lisans (D-016) |
|---|---|---|---|
| Marka | `ov_brand`, `ov_brand_website`, `ov_brand_mail` | Ad, logo, favicon, başlıklar, giriş ekranı, e-posta ve rapor altbilgileri, PWA manifest, kullanıcı menüsü bağlantıları; odoo.com'a giden çağrıların (yayıncı garantisi, IAP) kapatılması. Envanter: `docs/research/brand-inventory.md` | AGPL-3 |
| Türkiye temeli | `ov_l10n_tr`, `ov_l10n_tr_tcmb`, `ov_l10n_tr_mis_reports`, `ov_l10n_tr_check` … | Vergi/tevkifat eksikleri, VKN/TCKN, il/ilçe, TCMB kurları, belge çıktıları, Tekdüzen mali tablolar, çek/senet | AGPL-3. LGPL koddan türetilen kısım varsa (ör. `l10n_latam_check` uyarlaması) LGPL-3 |
| e-Belge | `ov_l10n_tr_edi` (çekirdek), `ov_l10n_tr_edi_nilvera` (adaptör), `ov_l10n_tr_edispatch` … | UBL-TR üretimi, senaryolar, fatura tipleri, mükellef sorgulama, durum takibi; entegratör adaptörleri; sahte adaptör | **LGPL-3** (19.0 LGPL koddan türetildiği için, D-008/2) |
| OCA portları | Orijinal OCA adları (`ports/oca/`) | Mali raporlar, banka mutabakatı, ekstre içe aktarma, kalite kontrol … | Orijinal lisans (çoğu AGPL-3) |
| Paketler | `ov_pack_ticaret`, `ov_pack_uretim` | Paket bağımlılıkları ve ön ayarlar, kurulum sihirbazı, roller | AGPL-3 |
| Enterprise eşdeğerleri | `ov_<uygulama>` | MODULE_MATRIX.md §C | AGPL-3 |
| SaaS yönetimi | `ov_saas_*` | Kiracı yaşam döngüsü, plan/abonelik, kullanım ölçümü (PLAN F10) | AGPL-3 |

Bağımlılık yönü: üst katman alt katmana bağımlı olabilir, tersi olamaz. Kapalı kaynak modül yoktur; olursa AGPL modüllere bağımlı olamaz (D-008/4).

## 4. Çalışma zamanı mimarisi (üretim)

**Teslim biçimi (D-018):**
- İlk müşterilerde yönetilen kurulum. Her müşterinin ayrı veritabanı olur.
- Kurulum müşterinin sunucusunda (on-prem) ya da bizim yönettiğimiz bir sunucuda yapılır. İkisi de aynı kurulum aracını kullanır (`deploy/`, PLAN T8.4).
- Self-servis SaaS (kayıt, otomatik tahsilat, otomatik kiracı oluşturma) daha sonra gelir (PLAN F10).
- Aşağıdaki şema bizim sunucumuzdaki çok müşterili düzeni gösterir. On-prem kurulum aynı şemanın tek müşterili halidir.

```
İnternet ──HTTPS──▶ Ters vekil (Caddy/nginx, wildcard TLS - Let's Encrypt)
                       │  musteri1.<marka-alanadi> → veritabanı "musteri1"
                       ▼
               Odoo sunucusu (Linux)
                 ├─ HTTP işçileri (prefork, workers = 2×CPU+1 başlangıç)
                 ├─ gevent/websocket (bildirimler, canlı sohbet)
                 └─ cron işçileri
                       │
        ┌──────────────┼──────────────────────┐
        ▼              ▼                      ▼
  PostgreSQL ≥16   Filestore             Dış servisler
  (kiracı başına   (kiracı başına        - e-Belge entegratör API'si (Nilvera …)
   ayrı veritabanı) ayrı klasör)         - SMTP (e-posta), SMS sağlayıcı
                                         - iyzico (ödeme)
```

- **Kiracı ayrımı:** veritabanı başına kiracı, `dbfilter = ^%d$`, `list_db = False`, veritabanı yöneticisi kapalı.
- **Yedekleme:** her kiracı için `pg_dump` + filestore. Yedeklerin bir kopyası farklı bir yerde (ikincil arşiv yurt dışında olabilir, `docs/research/hosting.md`).
- **Konum:** D-013 ile ertelendi (karar noktası T9.5). Ön öneri Türkiye'de bir sunucu (e-Belge saklama + KVKK).
- **Sağlayıcıdan bağımsızlık (D-013 kısıtı):**
  - yalnız standart Linux, PostgreSQL, ters vekil ve cron/systemd kullanılır;
  - bulut sağlayıcısına özel yönetilen servis kullanılmaz;
  - e-Belge saklama yeri ve yedek hedefi yapılandırmayla değişir.

  Böylece sunucu, karar verildiğinde herhangi bir sağlayıcıya taşınabilir.

## 5. Geliştirme ortamı ve CI (planlanan, PLAN F1)

- Windows 11 + Python 3.12 sanal ortam (`.venv`) + yerel PostgreSQL 16+.
- **Python ortamı (T1.5, kurulu):** depodaki `.venv` (git'e girmez). `requirements-dev.txt` upstream `requirements.txt`'yi içerir, üstüne test ve lint araçlarını ekler; ürünle dağıtılmaz. Ürün bağımlılıkları upstream'in sabit commit'iyle belirlenir.
- **Yerel PostgreSQL (T1.3, kurulu):** 18.6, EDB taşınabilir ikili dosyalar; yönetici izni gerekmez.
  - Depo dışında `OV_HOME` = `%LOCALAPPDATA%\odoo-version`: `pgsql/` ikili dosyalar, `pgdata/` küme (UTF-8, `C.UTF-8` yerleşik yerel ayar, scram-sha-256), `pglog/` günlük.
  - Kullanıcı hesabında çalışır, yalnız `localhost` dinler. Yönetim: `tools/pg.py`. Bağlantı bilgileri `.env` dosyasında (git'e girmez).
  - Sürüm seçimi: Odoo 20.0'ın alt sınırı 16; 18, CI ve olası üretim sunucusunun (Ubuntu) paket sürümleriyle uyumlu.
- Odoo `upstream/odoo/odoo-bin` ile; addons yolu §2'deki sırayla.
- **Yerel Odoo (T1.6, çalışıyor):** depo kökündeki `odoo.conf` (git'e girmez) `deploy/odoo.conf.example`'dan `tools/odoo_conf.py` ile üretilir.
  - Addons yolu glob kalıplarıyla yazılır (`vendor/oca/*`, `ports/oca/*`, `addon[s]`); henüz olmayan klasörler uyarısız atlanır.
  - Veri klasörü `OV_HOME/odoo-data`. Tek süreç (`workers = 0`), yalnız `127.0.0.1`.
  - Demo veritabanı `ov_demo` (Türkçe, TR, `ov_brand` + `account` + `l10n_tr`).
- **Yerel testler (T1.8):** `tools/run_tests.py` her çalıştırmada temiz test veritabanı açar (demo yok), ayrı HTTP portu (8079) kullanır. Windows'a özgü filestore temizliği hatalarını ayrı sayar; referans sonuç Linux CI'dır.
  - Hedef modüller `ov_brand`'e bağlıysa `ov_brand` önce testsiz kurulur (T2.3). Kurulumu çevrim içi hizmet modüllerini kaldırıyor; modül kaldıran bir çalıştırmada Odoo `post_install` testlerini başlatmaz. Onunla gelen hedef modüller ikinci çalıştırmada güncellenir, testleri de çalışır.
- **Lint ve commit öncesi denetimler (T1.9):** `.pre-commit-config.yaml` her commit'te çalışır; CI'da `pre-commit run --all-files` (T1.10).
  - `ruff.toml`: upstream `ruff.toml`'u genişletir; `upstream/`, `vendor/`, `ports/` hariç.
  - `.pylintrc`: pylint-odoo'nun Odoo denetimleri (yalnız `addons/`): sürüm 20.0, lisans AGPL-3/LGPL-3, zorunlu yazar, SQL enjeksiyonu, yöntem adları.
    - Modül içi içe aktarmalar upstream gibi mutlak (ruff TID252). Tersini isteyen `odoo-addons-relative-import` denetimi pre-commit kanca argümanıyla kapalı (T2.2).
  - `tools/check_modules.py`: proje kuralları (önek, lisans, sürüm, yazar, kullanıcıya görünen metinlerde marka, `README.rst`, test, `tr.po`).
- **CI (T1.10, çalışıyor; D-020):** GitHub Actions, `.github/workflows/ci.yml`. Her push'ta, pull request'te ve elle (`workflow_dispatch`) çalışır. İki iş paralel:
  - **Belgeler, lint, gizli bilgi** (`checks`): belge denetimi → `pre-commit run --all-files` → gitleaks (tüm geçmiş) → `sync_skills.py --check`.
  - **Modül testleri** (`tests`): Ubuntu 24.04, Python 3.12, PostgreSQL 18 servisi.
    - Şablondan örnek modül üretilir, modül kuralları, ruff ve pylint-odoo'dan geçirilir (depoya girmez).
    - `addons/` ve `ports/` altındaki bütün modüller örnekle birlikte tek veritabanında test edilir (`run_tests.py -v`).
    - Elle çalıştırmada `modules` girdisindeki modüller (ör. upstream) ayrıca test edilir: Linux referans sonucu.
  - Önbellekler: alt modüllerin git nesneleri (upstream ve `vendor/` sabit commit'lerine göre; biri değişince son önbellek geri yüklenir, yalnız yeni commit'ler çekilir), pip, pre-commit ortamları. GitHub önbellekleri dala bağlıdır; `main`'dekiler her dalda kullanılır.
  - Güvenlik: yalnız okuma yetkisi; eylemler commit SHA'sıyla sabit; gitleaks arşivi SHA-256 ile doğrulanır.
  - Planlanan özel testler: marka sızıntısı, dış istek, UBL-TR doğrulama, çeviri kapsamı, kurulum.
- Üretim Linux olduğu için CI aynı zamanda Linux uyumluluk testidir.

## 6. Sürüm yükseltme stratejisi

- **Küçük güncellemeler** (aynı ana sürüm, güvenlik/hata düzeltmeleri): upstream sabit commit'ini ilerlet → testler → yayın.
- **Ana sürüm** (yılda bir):
  1. Modüllerimizi taşı (`odoo-bin upgrade_code` yardımcı).
  2. Kiracı veritabanlarını OCA OpenUpgrade ile taşı (Odoo S.A.'nın yükseltme hizmeti yalnız Enterprise içindir).
  3. Hazırlık ortamında deneme → üretim.
- Odoo her yıl son 3 ana sürümü destekler. Bir ana sürümde en fazla ~2 yıl kalınır.

## 7. Dış bağımlılık ilkeleri

- Ürün, odoo.com sunucularına çalışma zamanında bağımlı olmamalı (IAP, yayıncı garantisi, odoo.com bağlantıları kapatılır/değiştirilir).
- Her dış servis bir adaptör arkasında. Sağlayıcı değiştirilebilir.
- Ücretli dış servislerin maliyeti müşteriye ait (D-005).
