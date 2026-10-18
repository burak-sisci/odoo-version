# Odoo Analizi (kaynak kod + dokümantasyon)

Son güncelleme: 2026-10-18
Araştırma tarihi: 2026-10-16 / 2026-10-18
İncelenen sürüm: `odoo/odoo` 20.0 dalı, commit `1740e969d23e6e3e299e5f367a1b0fcc6d2170fe` (2026-10-16)

> Bu belge tarihli bir araştırma kaydıdır. Bir bulgu yeniden doğrulanır ya da değişirse bu belge güncellenir ve tarih değiştirilir.

## 1. Odoo nedir?

Odoo S.A. (Belçika) tarafından geliştirilen, web tabanlı, modüler bir iş uygulamaları paketidir (ERP).
Uygulamalar (CRM, satış, satın alma, stok, üretim, POS, fatura, proje, İK, web sitesi, e-ticaret, pazarlama…)
tek bir veritabanını paylaşır ve tek başına ya da birlikte kullanılabilir.

İki sürümü vardır:

| Sürüm | Lisans | Not |
|---|---|---|
| Community | LGPL-3 | Açık kaynak, `github.com/odoo/odoo` |
| Enterprise | Odoo Enterprise Edition License v1.0 (özel mülk) | Community'nin üzerine kurulan ek modüller. Abonelik olmadan kullanılamaz; kopyalanamaz, dağıtılamaz |

Destek politikası: Odoo son 3 ana sürümü destekler (Ekim 2026 itibarıyla 18, 19, 20). Ana sürümler her yıl Eylül/Ekim'de çıkar.

## 2. Kod tabanı ölçüleri (20.0, Community)

| Ölçü | Değer |
|---|---|
| Toplam dosya | 50.484 |
| Modül | 657 (`addons/` 641 + `odoo/addons/` 16) |
| Uygulama (`application: True`) | 34 |
| Ülke yerelleştirmesi (`l10n_*`) | 229 |
| Lisans | 657 modülün tamamı LGPL-3 |
| Python | ~1,37 milyon satır (~680 bin satırı test) |
| JavaScript | ~1,19 milyon satır (`/lib/` hariç) |
| XML | ~565 bin satır |
| Çekirdek `odoo/` Python (test modülleri hariç) | ~132 bin satır |
| ORM (`odoo/orm`) | ~21,7 bin satır |
| Web istemcisi (`addons/web/static/src`) | ~124 bin satır JS |

Bu sayılara Enterprise kodu dahil değildir.

## 3. Mimari

Üç katmanlı:

1. **Veri katmanı:** yalnızca PostgreSQL (20.0 için en az 16 — `odoo/release.py: MIN_PG_VERSION = 16`).
2. **Mantık katmanı:** Python (3.12–3.14). Kendi ORM'i (`odoo/orm`: models, fields, domains, registry, environments), Werkzeug tabanlı HTTP katmanı (`odoo/http`), CLI (`odoo/cli`: server, shell, scaffold, db, module, i18n, upgrade_code, neutralize, obfuscate…).
3. **Sunum katmanı:** Odoo'nun kendi JS framework'ü **Owl** (20.0'da `3.0.0-alpha.49`). Görünümler: list, form, kanban, calendar, pivot, graph, card, hierarchy (`addons/web/static/src/views`).

Her şey modüldür. Modül yapısı:

```
modul_adi/
  __manifest__.py      # ad, bağımlılıklar, veri dosyaları, assets, lisans
  __init__.py
  models/              # Python iş nesneleri (ORM sınıfları)
  views/               # XML arayüz tanımları
  security/            # ir.access.csv (20.0) + gruplar
  data/ demo/          # XML/CSV veri
  controllers/         # HTTP uç noktaları
  static/              # JS (Owl), SCSS, görseller
  report/ wizard/ tests/ i18n/
```

Örnek model (`addons/fleet/models/fleet_vehicle_model.py`):

```python
class FleetVehicleModel(models.Model):
    _name = 'fleet.vehicle.model'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'avatar.mixin']
    name = fields.Char('Model name', required=True, tracking=True)
    brand_id = fields.Many2one('fleet.vehicle.model.brand', 'Manufacturer', required=True)
```

Genişletme modeli: başka modüller `_inherit` ile modelleri, XPath ile XML görünümlerini, `patch()` ile JS bileşenlerini değiştirebilir. Çekirdeğe dokunmadan çok derin değişiklik yapılabilmesinin nedeni budur.

## 4. Odoo 20'de öne çıkan değişiklikler

- **Yetkiler:** kayıt kuralları (record rules) kaldırıldı; `ir.access` erişim hakkı doğrudan domain alıyor (`security/ir.access.csv`, sütunlar: `id,name,model_id,group_id/id,operation,domain`).
- Çevrimdışı mod (kayıt oluşturma/düzenleme).
- Yeni PDF motoru modülü `base_report_paper_muncher` (wkhtmltopdf ayrı modüle taşındı: `base_report_wkhtmltox`).
- Mail: takip değerleri anlık üretiliyor.
- AI özellikleri IAP kredisi gerektiriyor (Enterprise/IAP).
- Repo kökünde **`skills/`** klasörü: AI ajanları (Claude Code dahil) için Odoo geliştirme rehberleri — `odoo-guidelines`, `odoo-review`, `odoo-security`, `odoo-web-guidelines`, `odoo-git`.
- `odoo-bin upgrade_code`: modül kaynak kodunu yeni sürüme otomatik dönüştüren betikler (`odoo/upgrade_code/*.py`).
- Türkiye: Nilvera e-Fatura/e-Arşiv/e-İrsaliye entegrasyonu **Enterprise'a taşındı** (19.0'da Community'de LGPL idi). Bkz. `e-fatura.md`.

## 5. Community'deki 34 uygulama

account (Invoicing), calendar, contacts, crm, data_recycle, fleet, hr (Employees), hr_attendance, hr_expense,
hr_holidays (Time Off), hr_recruitment, hr_skills, im_livechat, lunch, mail (Discuss), maintenance,
marketing_card, mass_mailing, mass_mailing_sms, mrp, point_of_sale, pos_restaurant, project, project_todo,
purchase, repair, sale_management, stock (Inventory), survey, website, website_event, website_hr_recruitment,
website_sale (eCommerce), website_slides (eLearning).

Not: `account` Community'de "Invoicing" (fatura ve ödeme). Tam muhasebe (banka mutabakatı ekranı, mali raporlar, sabit kıymet, bütçe) Enterprise'dadır.

## 6. Community'de bulunmayan (Enterprise) modüller — repo kontrolü

20.0 Community deposunda **yok**: account_accountant, account_reports, account_asset, account_budget, helpdesk,
documents, sign, knowledge, web_studio, planning, appointment, approvals, quality_control, mrp_plm, mrp_mps,
mrp_workorder, hr_payroll, sale_subscription, sale_renting, industry_fsm, social, marketing_automation, voip,
iot, whatsapp, hr_appraisal, hr_referral, ai, esg, stock_barcode, spreadsheet_edition, timesheet_grid,
web_mobile, account_online_synchronization.

Community'de **var**: spreadsheet, spreadsheet_dashboard (görüntüleme), hr_timesheet (temel).

## 7. Marka izleri (yeniden markalama için)

- XML/JS dosyalarından 372'si (test, `lib`, `l10n_*`, `i18n` hariç) "Odoo" geçiyor.
- Python'da lisans başlığı dışında ~1.091 satırda "Odoo" geçiyor.
- Web istemcisi URL'i: `/odoo`, `/odoo/<path>` (`addons/web/controllers/home.py:49`); web istemcisi JS'inde 7 dosya `/odoo` yoluna başvuruyor.
- PDF rapor varsayılan başlığı: `'Odoo Report'` (`addons/web/views/report_templates.xml`).
- "Powered by" metinleri: web, website, portal, mail şablonları.
- Python paket adı `odoo`; Community addons içinde 5.984 Python dosyası `odoo` paketini içe aktarıyor (paket adını değiştirmek tüm ekosistemi kırar).

## 8. odoo.com'a bağlanan bileşenler (ürünümüzde kapatılmalı/değiştirilmeli)

- Yayıncı garantisi / "phone-home": `addons/mail/models/update.py` (veritabanı bilgilerini Odoo sunucularına gönderir).
- IAP (Odoo S.A.'dan kredi satın alınan servisler): `iap`, `iap_crm`, `iap_mail`, `sms` (IAP üzerinden), `snailmail`,
  `partner_autocomplete`, `crm_iap_enrich`, `crm_iap_mine`, `website_crm_iap_reveal`, `pos_partner_autocomplete`.
- Alternatifler Community'de mevcut: `sms_twilio` (IAP'siz SMS), `payment_iyzico` (Türk ödeme sağlayıcısı).

## 9. Ekosistem

- **OCA (Odoo Community Association):** 272 açık depo. Modüllerin çoğu AGPL-3, bir kısmı LGPL-3.
  Ekim 2026 itibarıyla OCA 20.0 dalları neredeyse boş; 19.0 kısmen, 18.0 en olgun. Ayrıntı: `../MODULE_MATRIX.md`.
- **OCA/OCB:** Odoo Community'nin küçük düzeltmelerle sürekli senkron tutulan çatalı (17.0–20.0 dalları var).
- **OCA/OpenUpgrade:** Community veritabanlarını ana sürümler arasında taşıma betikleri (17.0–20.0 dalları var; 20.0 kapsamı doğrulanmadı). Odoo S.A.'nın yükseltme hizmeti Enterprise içindir.
- **Odoo dokümantasyonu** (`github.com/odoo/documentation`): **CC BY-SA 4.0** lisanslı; Enterprise özelliklerini de anlatır → clean-room işlev tanımı için yasal kaynak (bkz. `../COMPLIANCE.md`).

## Kaynaklar

- https://github.com/odoo/odoo (20.0 dalı, yukarıdaki commit)
- https://www.odoo.com/documentation/master/developer/tutorials/server_framework_101/01_architecture.html
- https://www.odoo.com/documentation/master/legal/licenses.html
- https://www.odoo.com/odoo-20-release-notes
- https://github.com/odoo/documentation (lisans: CC-BY-SA-4.0)
- https://github.com/OCA (depo sayısı GitHub API, 2026-10-16)
- https://ecosire.com/blog/latest-odoo-version (desteklenen sürümler — ikincil kaynak)
