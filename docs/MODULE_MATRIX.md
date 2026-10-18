# Modül Matrisi

Son güncelleme: 2026-10-18
İlgili kararlar: D-002, D-006, D-008, D-011, D-012, D-016

Bu matris D-002'nin (tüm Odoo uygulamaları) uygulama planıdır. Her uygulamanın edinme yolu, önceliği ve durumu burada tutulur.

**Öncelik:**
- **P0:** satılabilir ilk ürün (MVP) için zorunlu
- **P1:** ilk ticari sürüm
- **P2–P4:** sonraki sürümler (küçük sayı = önce)
- **P5:** ertelendi (bütçe ya da dış servis gerektiriyor)

**Durum:** `plan` → `inceleniyor` → `geliştiriliyor` → `test` → `tamam`

OCA sayıları: ilgili OCA deposundaki `__manifest__.py` sayısı, 18.0 / 19.0 / 20.0 dalları, 2026-10-18.

## A. Community'de hazır gelenler (upstream, LGPL-3)

Bu uygulamalar için iş: marka katmanı + Türkçe çeviri kontrolü + Türkiye yerelleştirmesi + test.

| Uygulama (modül) | Öncelik | Durum |
|---|---|---|
| Fatura / Invoicing (`account`) + Türkiye hesap planı (`l10n_tr`) | P0 | plan |
| Kişiler (`contacts`), Discuss (`mail`), Takvim (`calendar`) | P0 | plan |
| Satış (`sale_management`), CRM (`crm`) | P0 | plan |
| Satın Alma (`purchase`), Stok (`stock`) | P0 | plan |
| POS (`point_of_sale`), Restoran (`pos_restaurant`) | P1 | plan |
| Üretim (`mrp`), Onarım (`repair`), Bakım (`maintenance`) | P1 | plan |
| Proje (`project`), To-Do (`project_todo`), Zaman çizelgesi temel (`hr_timesheet`) | P1 | plan |
| Çalışanlar (`hr`), İzin (`hr_holidays`), Devam (`hr_attendance`), Masraf (`hr_expense`), İşe Alım (`hr_recruitment`), Yetkinlik (`hr_skills`) | P1 | plan |
| Web sitesi (`website`), e-Ticaret (`website_sale`), e-Öğrenme (`website_slides`), Etkinlik (`website_event`), İş ilanları (`website_hr_recruitment`) | P2 | plan |
| E-posta/SMS pazarlama (`mass_mailing`, `mass_mailing_sms`), Anket (`survey`), Canlı sohbet (`im_livechat`), Marketing Card (`marketing_card`) | P2 | plan |
| Filo (`fleet`), Yemek (`lunch`), Veri temizleme (`data_recycle`) | P3 | plan |
| Ödeme sağlayıcısı iyzico (`payment_iyzico`) | P1 | plan |
| Dashboard görüntüleme (`spreadsheet_dashboard`) | P2 | plan |

## B. Türkiye uyum katmanı

| Uygulama | Yol | Kaynak | Lisans | Öncelik | Durum |
|---|---|---|---|---|---|
| e-Fatura + e-Arşiv (entegratörden bağımsız çekirdek) | 19.0 LGPL koddan port + kendi tasarım | odoo/odoo 19.0 `l10n_tr_nilvera_einvoice(_extended)` | LGPL-3 | P0 | plan |
| Nilvera adaptörü | 19.0 LGPL port | odoo/odoo 19.0 `l10n_tr_nilvera` | LGPL-3 | P0 | plan |
| e-İrsaliye | 19.0 LGPL port | odoo/odoo 19.0 `l10n_tr_nilvera_edispatch` | LGPL-3 | P1 | plan |
| Diğer entegratör adaptörleri | Kendimiz | Entegratör API dokümanları | D-016 | P2 | plan |
| e-Defter | Kendimiz | GİB e-Defter kılavuzları | D-016 | P3 | plan |
| Türkiye bordrosu (SGK, gelir vergisi, damga vergisi, e-Bildirge) | OCA payroll + kendimiz | OCA/payroll (6/1/0) | LGPL-3 (OCA payroll) | P3 | plan |
| Türk SMS sağlayıcısı (IAP yerine) | Kendimiz | Sağlayıcı API'si | D-016 | P1 | plan |

## C. Enterprise'a özel uygulamalar → eşdeğer (clean-room, D-006)

| Enterprise uygulaması | Yol (aday) | OCA kaynağı (18/19/20) | OCA lisansı (örnek) | Öncelik | Durum |
|---|---|---|---|---|---|
| Muhasebe: banka mutabakatı | OCA port veya kendimiz | account-reconcile (19/4/0) | AGPL-3 (`account_reconcile_oca`) | P1 | plan |
| Muhasebe: mali raporlar (mizan, büyük defter, bilanço, gelir tablosu) | OCA port veya kendimiz | account-financial-reporting (8/5/0), mis-builder (3/3/3) | AGPL-3 | P1 | plan |
| Muhasebe: sabit kıymet / amortisman | OCA port veya kendimiz | account-financial-tools (41/23/0) | AGPL-3 (`account_asset_management`) | P1 | plan |
| Muhasebe: bütçe | OCA port veya kendimiz | account-budgeting (1/1/0) | doğrulanmadı | P2 | plan |
| Onaylar (Approvals) | OCA port | server-ux (35/17/1) — `base_tier_validation` adayı | doğrulanmadı | P2 | plan |
| Helpdesk | OCA port veya kendimiz | helpdesk (32/15/0) | AGPL-3 (`helpdesk_mgmt`) | P2 | plan |
| Dokümanlar (Documents) | OCA port | dms (7/1/0) | LGPL-3 (`dms`) | P2 | plan |
| Barkod | OCA port | stock-logistics-barcode (7/3/0) | AGPL-3 (`stock_barcodes`) | P2 | plan |
| Abonelik (Subscriptions) | OCA port | contract (34/12/0) | AGPL-3 (`contract`) | P2 | plan |
| Mobil uygulama | PWA (Community'de manifest + service worker var) | — | LGPL-3 | P2 | plan |
| Zaman çizelgesi ızgarası / onay | OCA port | timesheet (34/17/0) | doğrulanmadı | P3 | plan |
| Spreadsheet düzenleme (BI) | OCA port | spreadsheet (5/4/0) | AGPL-3 (`spreadsheet_oca`) | P3 | plan |
| Bilgi Bankası (Knowledge) | OCA port | knowledge (15/11/0) | AGPL-3 (`document_page`) | P3 | plan |
| e-İmza (Sign) | OCA port | sign (4/1/0) | AGPL-3 (`sign_oca`) | P3 | plan |
| Saha Servisi (Field Service) | OCA port | field-service (39/34/0) | AGPL-3 (`fieldservice`) | P3 | plan |
| Kalite | OCA port veya kendimiz | management-system (35/26/0), manufacture (57/20/0) | doğrulanmadı | P3 | plan |
| Planlama (Planning) | Kendimiz | — | — | P3 | plan |
| Randevu (Appointments) | Kendimiz | — | — | P3 | plan |
| Kiralama (Rental) | Kendimiz | vertical-rental (0/0/0) | — | P3 | plan |
| Studio (uygulama oluşturucu) | Kendimiz (uzun vadeli) | — | — | P4 | plan |
| PLM, MPS, Atölye (Shop Floor) | OCA port veya kendimiz | manufacture (57/20/0) | doğrulanmadı | P4 | plan |
| Değerlendirme (Appraisals), Referans (Referrals) | OCA port veya kendimiz | hr (31/11/0) | doğrulanmadı | P4 | plan |
| Pazarlama otomasyonu, Sosyal pazarlama | Kendimiz | — | — | P4 | plan |
| VoIP | OCA port | connector-telephony (3/1/0) | doğrulanmadı | P4 | plan |
| IoT | OCA port | iot (4/0/0) | doğrulanmadı | P4 | plan |
| WhatsApp | OCA veya kendimiz | social (16/1/0) | doğrulanmadı | P5 (Meta API ücretli) | plan |
| AI ajanları, OCR (fatura/masraf okuma) | Kendimiz | — | — | P5 (LLM/OCR servisi ücretli) | plan |
| ESG, Amazon bağlayıcısı | Kendimiz | — | — | P5 | plan |
| Banka senkronizasyonu (online) | Kendimiz | — | — | P5 (banka API anlaşmaları) | plan |

## Notlar

- **AGPL uyarısı (D-008/4):** D-016 kapalı lisansa izin verirse, AGPL OCA modülüne bağımlı modüllerimiz kapalı kaynak olamaz. Bir OCA AGPL modülü kullanılacaksa ya modül olduğu gibi (AGPL) dağıtılır, ya da işlev kendi tasarımımızla sıfırdan yazılır. Karar her modülde ayrı verilir ve DECISIONS.md'ye işlenir.
- "doğrulanmadı" = lisans veya modülün uygunluğu henüz kontrol edilmedi. İlgili adım başlarken kontrol edilecek.
