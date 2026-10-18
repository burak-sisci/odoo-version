# Modül Matrisi

Son güncelleme: 2026-10-18
İlgili kararlar: D-002, D-006, D-008, D-011, D-012, D-016, D-017, D-018, D-019

Bu matris D-002'nin (tüm Odoo uygulamaları) uygulama planıdır. Her uygulamanın edinme yolu, önceliği ve durumu burada tutulur. Görevler ve sıralama `PLAN.md`'de.

**Öncelik (D-018):**
- **P0:** M8 kapısı (satışa hazır sürüm) için zorunlu
- **P1:** hedef segmentler için değerli; M8'den önce yapılabilir ama kapıyı bekletmez (PLAN F11)
- **P2–P4:** sonraki sürümler (küçük sayı = önce)
- **P5:** ertelendi (bütçe ya da dış servis gerektiriyor)

**Paket (D-018):** T = Ticaret (küçük işletme), Ü = Üretim (orta ölçekli fabrika), — = MVP paketlerinde yok.

**Durum:** `plan` → `inceleniyor` → `geliştiriliyor` → `test` → `tamam`

OCA sayıları: ilgili OCA deposundaki `__manifest__.py` sayısı, 18.0 / 19.0 / 20.0 dalları, 2026-10-18.
- 20.0 sayısına henüz taşınmamış yer tutucular (`installable: False`, sürümü 19.0) dahildir. Ör. `mis-builder` 20.0'daki 3 modülün hiçbiri kurulamaz.
- Kurulabilir 20.0 modülleri ve port ölçümü: `docs/research/nilvera-port.md` (T1.2).
- Ortak bağımlılıklar hazır (T1.11): `date_range` (resmî 20.0, `vendor/oca/server-ux`) ve `report_xlsx` (port, `ports/oca/reporting-engine`). Mali raporlar (`account_financial_report`) ve `mis_builder` bu ikisine dayanıyor.

## A. Community'de hazır gelenler (upstream, LGPL-3)

Bu uygulamalar için iş: marka katmanı + Türkçe çeviri + Türkiye yerelleştirmesi + paket ön ayarları + test.

| Uygulama (modül) | Paket | Öncelik | Durum |
|---|---|---|---|
| Fatura / Invoicing (`account`) + Türkiye hesap planı (`l10n_tr`) | T, Ü | P0 | plan |
| Kişiler (`contacts`), Discuss (`mail`), Takvim (`calendar`) | T, Ü | P0 | plan |
| Satış (`sale_management`), CRM (`crm`) | T, Ü | P0 | plan |
| Satın Alma (`purchase`), Stok (`stock`) | T, Ü | P0 | plan |
| Üretim (`mrp`), Fason üretim (`mrp_subcontracting`), Bakım (`maintenance`) | Ü | P0 | plan |
| Onarım (`repair`) | Ü | P1 | plan |
| Dashboard görüntüleme (`spreadsheet_dashboard`) | T, Ü | P1 | plan |
| Çalışanlar (`hr`), İzin (`hr_holidays`), Devam (`hr_attendance`) | — | P1 | plan |
| POS (`point_of_sale`), Restoran (`pos_restaurant`) — önce yeni nesil ödeme kaydedici cihaz araştırması (PLAN T11.9) | — | P2 | plan |
| Proje (`project`), To-Do (`project_todo`), Zaman çizelgesi temel (`hr_timesheet`) | — | P2 | plan |
| Masraf (`hr_expense`), İşe Alım (`hr_recruitment`), Yetkinlik (`hr_skills`) | — | P2 | plan |
| Web sitesi (`website`), e-Ticaret (`website_sale`), e-Öğrenme (`website_slides`), Etkinlik (`website_event`), İş ilanları (`website_hr_recruitment`) | — | P2 | plan |
| E-posta/SMS pazarlama (`mass_mailing`, `mass_mailing_sms`), Anket (`survey`), Canlı sohbet (`im_livechat`), Marketing Card (`marketing_card`) | — | P2 | plan |
| Ödeme sağlayıcısı iyzico (`payment_iyzico`) — self-servis SaaS tahsilatı (PLAN F10) | — | P2 | plan |
| Filo (`fleet`), Yemek (`lunch`), Veri temizleme (`data_recycle`) | — | P3 | plan |

## B. Türkiye uyum katmanı

| Uygulama | Yol | Kaynak | Lisans | Paket | Öncelik | Durum |
|---|---|---|---|---|---|---|
| Temel yerelleştirme (`ov_l10n_tr`): vergi/tevkifat eksikleri, VKN/TCKN, il/ilçe, Türkiye varsayılanları | Kendimiz, `l10n_tr` üzerine | `l10n_tr` (20.0), python-stdnum, açık lisanslı ilçe verisi | AGPL-3 | T, Ü | P0 | plan |
| TCMB döviz kurları (`ov_l10n_tr_tcmb`) | Kendimiz | TCMB kamuya açık XML | AGPL-3 | T, Ü | P0 | plan |
| Türkçe çeviri tamamlama | Kendimiz | Upstream `tr.po` dosyaları | LGPL-3 (upstream metinlerinin çevirisi) | T, Ü | P0 | plan |
| Türkçe belge çıktıları (teklif, sipariş, irsaliye, makbuz; tutar yazıyla) | Kendimiz | — | AGPL-3 | T, Ü | P0 | plan |
| Resmî tatiller ve çalışma takvimi | Kendimiz | — | AGPL-3 | T, Ü | P0 | plan |
| Çek ve senet (`ov_l10n_tr_check`) | Kendimiz; Community `l10n_latam_check` incelenerek | Community 20.0 | AGPL-3; türetme olursa LGPL-3 | T, Ü | P0 | plan |
| Banka ekstresi içe aktarma + Türk bankası şablonları | OCA 19.0 port + kendi şablonlarımız | OCA `account_statement_import_file`, `account_statement_import_sheet_file` | AGPL-3 (OCA) | T, Ü | P0 | plan |
| Tekdüzen bilanço ve gelir tablosu (`ov_l10n_tr_mis_reports`) | Kendimiz | OCA `mis_builder` (19.0'dan port, T5.5) | AGPL-3 | T, Ü | P0 | plan |
| KDV hazırlık raporu | Kendimiz | `l10n_tr` vergi raporu | AGPL-3 | T, Ü | P0 | plan |
| Mali müşavire aktarım (muhasebe fişleri) | Kendimiz | Muhasebe programlarının kamuya açık içe aktarma biçimleri | AGPL-3 | T, Ü | P0 | plan |
| e-Fatura + e-Arşiv (entegratörden bağımsız çekirdek) | 19.0 LGPL port + kendi tasarım | odoo/odoo 19.0 `l10n_tr_nilvera_einvoice(_extended)`, `l10n_tr_gib_invoice_scenarios` | LGPL-3 | T, Ü | P0 | plan |
| Nilvera adaptörü | 19.0 LGPL port | odoo/odoo 19.0 `l10n_tr_nilvera` | LGPL-3 | T, Ü | P0 | plan |
| e-İrsaliye | 19.0 LGPL port | odoo/odoo 19.0 `l10n_tr_nilvera_edispatch` | LGPL-3 | T, Ü | P0 | plan |
| Sahte (mock) entegratör adaptörü | Kendimiz | — | AGPL-3 | — | P0 | plan |
| e-Defter | Kendimiz veya entegratör üzerinden (önce araştırma, PLAN T11.4) | GİB e-Defter kılavuzları | AGPL-3 | Ü | P1 | plan |
| Türk SMS sağlayıcısı (IAP yerine) | Kendimiz | Sağlayıcı API'si | AGPL-3 | — | P1 | plan |
| Enflasyon düzeltmesi (güncel kapsam araştırılacak) | Kendimiz | Mevzuat | AGPL-3 | — | P1 | plan |
| Diğer entegratör adaptörleri | Kendimiz | Entegratör API dokümanları | AGPL-3 | — | P2 | plan |
| Türkiye bordrosu (SGK, gelir vergisi, damga vergisi, e-Bildirge) | OCA payroll + kendimiz | OCA/payroll (6/1/0) | LGPL-3 (OCA payroll) | — | P3 | plan |

## C. Enterprise'a özel uygulamalar → eşdeğer (clean-room, D-006)

OCA modülleri D-019'a göre: resmî 20.0 sürümü varsa `vendor/oca/`, yoksa 19.0'dan port `ports/oca/`.

| Enterprise uygulaması | Yol (aday) | OCA kaynağı (18/19/20) | OCA lisansı (örnek) | Öncelik | Durum |
|---|---|---|---|---|---|
| Muhasebe: banka mutabakatı | OCA port | account-reconcile (19/4/0) | AGPL-3 (`account_reconcile_oca`) | P0 | plan |
| Muhasebe: mali raporlar (mizan, muavin, yaşlandırma) | OCA port | account-financial-reporting (8/5/0) | AGPL-3 (`account_financial_report`) | P0 | plan |
| Muhasebe: bilanço / gelir tablosu altyapısı | OCA port (resmî 20.0 çıkınca `vendor/`) | mis-builder (3/3/3; 20.0'dakiler yer tutucu) | AGPL-3 (`mis_builder`) | P0 | plan |
| Muhasebe: cari ekstre | OCA port veya kendimiz | account-financial-reporting (8/5/0) | AGPL-3 (`partner_statement`) | P0 | plan |
| Kalite | OCA port | manufacture (57/20/0) — `quality_control_oca` | doğrulanmadı | P0 | plan |
| Mobil uygulama | PWA (Community'de manifest + service worker var) | — | LGPL-3 | P0 | plan |
| Muhasebe: sabit kıymet / amortisman | OCA port | account-financial-tools (41/23/0) | AGPL-3 (`account_asset_management`) | P1 | plan |
| Çok seviyeli MRP planlama | OCA port | manufacture (57/20/0) — `mrp_multi_level` | doğrulanmadı | P1 | plan |
| Barkod | OCA 18.0 port veya kendimiz | stock-logistics-barcode (7/3/0) | AGPL-3 (`stock_barcodes`) | P1 | plan |
| Muhasebe: bütçe | OCA port veya kendimiz | account-budgeting (1/1/0), mis-builder (`mis_builder_budget`, 20.0'da yer tutucu) | doğrulanmadı | P2 | plan |
| Onaylar (Approvals) | OCA port | server-ux (35/17/1) — `base_tier_validation` adayı | doğrulanmadı | P2 | plan |
| Helpdesk | OCA port veya kendimiz | helpdesk (32/15/0) | AGPL-3 (`helpdesk_mgmt`) | P2 | plan |
| Dokümanlar (Documents) | OCA port | dms (7/1/0) | LGPL-3 (`dms`) | P2 | plan |
| Abonelik (Subscriptions) | OCA port | contract (34/12/0) | AGPL-3 (`contract`) | P2 | plan |
| Zaman çizelgesi ızgarası / onay | OCA port | timesheet (34/17/0) | doğrulanmadı | P3 | plan |
| Spreadsheet düzenleme (BI) | OCA port | spreadsheet (5/4/0) | AGPL-3 (`spreadsheet_oca`) | P3 | plan |
| Bilgi Bankası (Knowledge) | OCA port | knowledge (15/11/0) | AGPL-3 (`document_page`) | P3 | plan |
| e-İmza (Sign) | OCA port | sign (4/1/0) | AGPL-3 (`sign_oca`) | P3 | plan |
| Saha Servisi (Field Service) | OCA port | field-service (39/34/0) | AGPL-3 (`fieldservice`) | P3 | plan |
| PLM, MPS, Atölye (Shop Floor) | OCA port veya kendimiz | manufacture (57/20/0) | doğrulanmadı | P3 | plan |
| Planlama (Planning) | Kendimiz | — | — | P3 | plan |
| Randevu (Appointments) | Kendimiz | — | — | P3 | plan |
| Kiralama (Rental) | Kendimiz | vertical-rental (0/0/0) | — | P3 | plan |
| Studio (uygulama oluşturucu) | Kendimiz (uzun vadeli) | — | — | P4 | plan |
| Değerlendirme (Appraisals), Referans (Referrals) | OCA port veya kendimiz | hr (31/11/0) | doğrulanmadı | P4 | plan |
| Pazarlama otomasyonu, Sosyal pazarlama | Kendimiz | — | — | P4 | plan |
| VoIP | OCA port | connector-telephony (3/1/0) | doğrulanmadı | P4 | plan |
| IoT | OCA port | iot (4/0/0) | doğrulanmadı | P4 | plan |
| WhatsApp | OCA veya kendimiz | social (16/1/0) | doğrulanmadı | P5 (Meta API ücretli) | plan |
| AI ajanları, OCR (fatura/masraf okuma) | Kendimiz | — | — | P5 (LLM/OCR servisi ücretli) | plan |
| ESG, Amazon bağlayıcısı | Kendimiz | — | — | P5 | plan |
| Banka senkronizasyonu (online) | Kendimiz | — | — | P5 (banka API anlaşmaları) | plan |

## Notlar

- **Lisans (D-016):** kendi modüllerimiz AGPL-3 olduğu için AGPL OCA modüllerine serbestçe bağımlı olabilir. Kapalı kaynak modül yoktur; olursa AGPL modüle bağımlı olamaz (D-008/4).
- **Port edilen OCA modülleri** orijinal teknik ad ve lisanslarını korur (D-019). Port başlarken lisans ve bağımlılıklar doğrulanır (PLAN T5.1).
- "doğrulanmadı" = lisans veya modülün uygunluğu henüz kontrol edilmedi. İlgili görev başlarken kontrol edilecek.
