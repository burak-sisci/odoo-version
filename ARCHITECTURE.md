# Mimari

Son güncelleme: 2026-10-18

> **Durum: Hedef mimari.**
> - Dayandığı kararlar: D-010 (yaklaşım **B**), D-011 (sürüm **20.0**), D-014 (önek `ov_`). Üçü de Geçerli.
> - Barındırma yeri D-013 ile ertelendi (§4). Kendi modüllerimizin lisansı D-016 ile açık (§3).
> - Henüz kod yok. Bu belge kurulacak yapıyı tanımlıyor.

## 1. Genel bakış

Ürün = **değiştirilmemiş Odoo Community** + **seçilmiş OCA modülleri** + **kendi modül katmanlarımız** + **SaaS işletim altyapısı**.

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
│  │ SaaS yönetimi (kiracı oluşturma, abonelik, yedek, izleme)      │  │
│  └───────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│ Seçilmiş OCA modülleri (vendor/oca/) — sabit commit, lisans envanterli│
├─────────────────────────────────────────────────────────────────────┤
│ Odoo Community (upstream/odoo) — sabit commit, DEĞİŞTİRİLMEZ          │
└─────────────────────────────────────────────────────────────────────┘
```

**Değişiklik yöntemi (D-010, B):** upstream'in hiçbir dosyası değiştirilmez, yama kuyruğu yoktur. Her değişiklik `addons/` altındaki modüllerle yapılır:
- model kalıtımı (`_inherit`);
- görünüm kalıtımı (XPath);
- JS `patch()` ve asset paketinde dosya değiştirme (`replace`);
- controller override;
- gerekirse modül içinden monkey-patch (gerekçesi kodda yazılı).

Modülle çözülemeyen bir durum kullanıcıya yeni karar olarak getirilir.

## 2. Depo yerleşimi (planlanan)

```
odoo-version/
├── CLAUDE.md  README.md  ARCHITECTURE.md  DECISIONS.md  ROADMAP.md  CHANGELOG.md  state.json
├── .gitignore  .gitattributes   # gizli bilgiler ve yerel veriler depoya girmez; satır sonu LF
├── docs/
│   ├── COMPLIANCE.md        # lisans, clean-room, marka, KVKK
│   ├── MODULE_MATRIX.md     # tüm uygulamaların planı ve durumu
│   ├── specs/               # Enterprise eşdeğerleri için clean-room işlev tanımları
│   └── research/            # tarihli araştırma kayıtları
├── tools/
│   └── check_docs.py        # belge tutarlılık denetimi
├── upstream/odoo/           # Odoo Community 20.0, git submodule, sabit commit (henüz yok — T1.3)
├── vendor/oca/<depo>/       # kullanılan OCA depoları, git submodule, sabit commit (henüz yok)
├── addons/                  # bizim modüllerimiz, önek ov_ (henüz yok)
└── deploy/                  # sunucu, ters vekil, yedek yapılandırmaları (henüz yok)
```

Kurallar:
- `upstream/` ve `vendor/` altındaki dosyalar elle düzenlenmez (D-010). Tüm değişiklik `addons/` altında.
- Sürüm yükseltme = sabit commit'i ilerletmek + testler.
- Depo public (D-015): gizli bilgi, müşteri verisi, yerel yapılandırma (`odoo.conf`, `.env`) depoya girmez.

## 3. Modül katmanları

Önek: `ov_` (D-014). Markadan bağımsızdır; marka değişince modül adları değişmez.

| Katman | Modül adı kalıbı | Görev | Lisans |
|---|---|---|---|
| Marka | `ov_brand`, `ov_brand_website`, `ov_brand_mail` | Ad, logo, favicon, başlıklar, giriş ekranı, e-posta ve rapor altbilgileri, PWA manifest, kullanıcı menüsü bağlantıları; odoo.com'a giden çağrıların (yayıncı garantisi, IAP) kapatılması | D-016 (açık; öneri AGPL-3) |
| Türkiye uyumu | `ov_l10n_tr_edi` (çekirdek), `ov_l10n_tr_edi_nilvera` (adaptör), `ov_l10n_tr_edispatch` … | UBL-TR üretimi, senaryolar, fatura tipleri, mükellef sorgulama, durum takibi; entegratör adaptörleri | **LGPL-3** (19.0 LGPL koddan türetildiği için, D-008/2) |
| Enterprise eşdeğerleri | `ov_<uygulama>` | MODULE_MATRIX.md §C | D-016 (açık). AGPL modüle bağımlıysa AGPL (D-008/4) |
| SaaS yönetimi | `ov_saas_*` | Kiracı yaşam döngüsü, plan/abonelik, kullanım ölçümü | D-016 (açık) |

Bağımlılık yönü: üst katman alt katmana bağımlı olabilir, tersi olamaz. D-016 kapalı modüle izin verirse, kapalı modüller AGPL modüllere bağımlı olamaz (D-008/4).

## 4. Çalışma zamanı mimarisi (üretim SaaS)

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
- **Konum:** D-013 ile ertelendi (karar noktası T6.3). Ön öneri Türkiye'de bir sunucu (e-Belge saklama + KVKK).
- **Sağlayıcıdan bağımsızlık (D-013 kısıtı):**
  - yalnız standart Linux, PostgreSQL, ters vekil ve cron/systemd kullanılır;
  - bulut sağlayıcısına özel yönetilen servis kullanılmaz;
  - e-Belge saklama yeri ve yedek hedefi yapılandırmayla değişir.

  Böylece sunucu, karar verildiğinde herhangi bir sağlayıcıya taşınabilir.

## 5. Geliştirme ortamı (planlanan, ROADMAP Faz 1)

- Windows 11 + Python 3.12 sanal ortam (`.venv`) + yerel PostgreSQL 16+.
- Odoo `upstream/odoo/odoo-bin` ile; addons yolu: `upstream/odoo/addons,upstream/odoo/odoo/addons,vendor/oca/...,addons`.
- Üretim Linux olacağı için kritik testler ileride Linux'ta da (WSL2 veya CI) çalıştırılacak.

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
