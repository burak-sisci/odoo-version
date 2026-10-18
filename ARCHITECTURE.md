# Mimari

Son güncelleme: 2026-10-18

> **Durum: Hedef mimari.**
> - Dayandığı Geçerli kararlar:
>   - D-010 (yaklaşım **B**), D-011 (sürüm **20.0**; T1.2'de doğrulandı), D-014 (önek `ov_`);
>   - D-016 (lisans **AGPL-3**, LGPL türevleri LGPL-3), D-018 (paketler ve teslim biçimi), D-019 (OCA portları), D-020 (ücretsiz altyapı).
> - Üretim barındırma yeri D-013 ile ertelendi (§4).
> - Henüz kod yok. Bu belge kurulacak yapıyı tanımlıyor. Görevler `PLAN.md`'de.

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
├── .github/workflows/       # CI (henüz yok — T1.10)
├── docs/
│   ├── COMPLIANCE.md        # lisans, clean-room, marka, KVKK
│   ├── MODULE_MATRIX.md     # tüm uygulamaların planı ve durumu
│   ├── specs/               # Enterprise eşdeğerleri için clean-room işlev tanımları
│   └── research/            # tarihli araştırma kayıtları
├── tools/
│   └── check_docs.py        # belge tutarlılık denetimi (+ ileride modül şablonu, UBL doğrulama, çeviri ölçümü)
├── upstream/odoo/           # Odoo Community 20.0, sığ git submodule, sabit commit (state.json → upstream)
├── vendor/oca/<depo>/       # OCA'nın resmî 20.0 depoları, git submodule, sabit commit (henüz yok — T1.11)
├── ports/oca/<depo>/<modül>/  # OCA 19.0 modüllerinin bizim 20.0 portlarımız (henüz yok — D-019)
├── addons/                  # bizim modüllerimiz, önek ov_ (henüz yok)
└── deploy/                  # kurulum aracı, odoo.conf örneği, ters vekil, yedek betikleri (henüz yok — T1.6, T8.4)
```

Kurallar:
- `upstream/` ve `vendor/` altındaki dosyalar elle düzenlenmez (D-010). Değişiklik `addons/` ve `ports/` altında.
- Addons yolu sırası: `upstream/odoo/addons`, `upstream/odoo/odoo/addons`, `vendor/oca/*`, `ports/oca/*`, `addons`.
- Sürüm yükseltme = sabit commit'i ilerletmek + testler.
- Depo public (D-015): gizli bilgi, müşteri verisi, yerel yapılandırma (`odoo.conf`, `.env`) depoya girmez.

### OCA port düzeni (D-019)

- OCA'nın resmî 20.0 sürümü varsa `vendor/oca/<depo>` kullanılır.
- Yoksa 19.0 sürümü `ports/oca/<depo>/<modül>` altına kopyalanıp 20.0'a taşınır:
  - teknik ad, lisans, yazarlar ve telif notları korunur;
  - kaynak commit modül klasöründeki bir notta ve lisans envanterinde yazılır;
  - OCA'nın taşıma kurallarına uyulur.
- OCA resmî 20.0 sürümünü yayımlayınca port silinir ve `vendor/`'a geçilir. Teknik ad aynı olduğu için veritabanı göçü gerekmez.
- Ayrıntılı port prosedürü T1.11'de bu bölüme eklenecek.

## 3. Modül katmanları

Önek: `ov_` (D-014). Markadan bağımsızdır; marka değişince modül adları değişmez.

| Katman | Modül adı kalıbı | Görev | Lisans (D-016) |
|---|---|---|---|
| Marka | `ov_brand`, `ov_brand_website`, `ov_brand_mail` | Ad, logo, favicon, başlıklar, giriş ekranı, e-posta ve rapor altbilgileri, PWA manifest, kullanıcı menüsü bağlantıları; odoo.com'a giden çağrıların (yayıncı garantisi, IAP) kapatılması | AGPL-3 |
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
- **CI (D-020):** GitHub Actions, Ubuntu runner + PostgreSQL servisi. Her push'ta çalışır:
  - belge denetimi;
  - lint;
  - gizli bilgi taraması;
  - `addons/` ve `ports/` modül testleri;
  - özel testler: marka sızıntısı, dış istek, UBL-TR doğrulama, çeviri kapsamı, kurulum.
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
