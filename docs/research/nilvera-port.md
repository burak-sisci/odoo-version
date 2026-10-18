# 19.0 → 20.0 Port Maliyeti (Nilvera ve OCA)

Son güncelleme: 2026-10-18
Araştırma tarihi: 2026-10-18
İlgili kararlar: D-006, D-010, D-011, D-019 (DECISIONS.md)
İlgili görev: T1.2 (PLAN.md)

> **Sonuç (2026-10-18):** D-011 doğrulandı: **20.0'da kal.**
> - MVP'nin 19 modülünden 13'ü, 21 tür küçük uyarlamayla 20.0'da kuruluyor ve testlerinin tamamını ya da büyük kısmını geçiyor (§4).
> - Uyarlamaların çoğu mekanik. Elle değişiklik: 36 dosya, +96/−145 satır.
> - Büyük kalem bir tane: `account_financial_report`, 20.0'da kaldırılan `account.group` modeline dayanıyor (T5.4).
> - 19.0'da kalmak port işini yok etmiyor, yalnız erteliyor. Nilvera 20.0'dan itibaren Enterprise'da; 19.0'ın desteği Eylül 2028'de bitiyor. Ertelenen iş o tarihe kadar kendi kodumuzla ve müşteri veritabanlarıyla birlikte büyüyor (§7).
> - Bu belge kontrol tarihindeki durumu anlatır. Port görevleri (T4.x, T5.x, T6.4) başlarken ölçüm yeniden yapılır.

## 1. Soru

D-011 20.0'ı seçti. O sırada MVP'nin OCA modülüne ihtiyacı olmadığı varsayılmıştı. D-018 ile MVP'ye OCA modülleri girdi ve bu varsayım bozuldu. Ayrıca Türkiye e-Belge modülleri (Nilvera) 20.0'da Community'den çıktı.

Soru: 19.0'daki bu modülleri 20.0'a taşımak ne kadar tutar? 19.0'a dönmek daha mı ucuz?

## 2. Yöntem

Ölçüm, modüllerin gerçekten kurulup test edilmesiyle yapıldı. Tahmin değil, deneme.

- **Ortam:** Windows 11, Python 3.12.10, PostgreSQL 18.6 (T1.3).
  - Odoo 20.0 Community, commit `afbcf79d` (2026-10-18).
  - Şablon veritabanı: `account, account_edi_ubl_cii, l10n_tr, stock, stock_account, contacts, board`, demo verili.
  - Her modül, şablonun kopyasında `-i <modül> --test-enable --test-tags /<modül>` ile kuruldu.
- **Kaynak kod:**
  - Odoo 19.0 Community, commit `53ec5874` (2026-10-17): Nilvera ailesi.
  - OCA depolarının 19.0 dalları (2026-08-31 ile 2026-10-14 arası son commit'ler).
  - OCA'nın 20.0 dalı, yalnız 20.0'a gerçekten taşınmış modüller için (`date_range`).
  - Bağımlılıklar dahil 19 modül.
- **Clean-room (D-006):** 20.0 Enterprise'daki Nilvera modüllerine bakılmadı. Yalnız 19.0 LGPL kod ve 20.0 Community kullanıldı.
- **Üç ağaç:**
  1. `raw`: 19.0 kodu. Değişiklik yalnız manifest sürümü (`19.0.` → `20.0.`) ve `base_vat` bağımlılığı (20.0'da `base`'e katıldı).
  2. `upg`: `raw` + Odoo 20.0'ın kendi otomatik dönüştürücüsü (`odoo-bin upgrade_code`).
  3. `fix`: `upg` + elle uyarlamalar. Her uyarlama kayıt altında (§5).
- **Zaman sınırı:** Elle uyarlama, büyük bir yeniden tasarım gerektiren ilk noktada durduruldu. Kalan iş §6'da tahmin olarak yazıldı.
- Deneme dosyaları depoya girmedi. Hepsi geçici çalışma alanındaydı; ölçümün tekrarı için yöntem yeterli.

## 3. Modül boyutları (19.0)

| Modül | Kaynak | Python | Test (Python) | XML | JS |
|---|---|---:|---:|---:|---:|
| `l10n_tr_nilvera` | Odoo 19.0 (LGPL) | 455 | 0 | 251 | 0 |
| `l10n_tr_nilvera_base_vat` | Odoo 19.0 (LGPL) | 29 | 0 | 0 | 0 |
| `l10n_tr_nilvera_einvoice` | Odoo 19.0 (LGPL) | 1305 | 597 | 684 | 0 |
| `l10n_tr_nilvera_einvoice_extended` | Odoo 19.0 (LGPL) | 1370 | 130 | 1643 | 0 |
| `l10n_tr_gib_invoice_scenarios` | Odoo 19.0 (LGPL) | 853 | 74 | 462 | 0 |
| `l10n_tr_nilvera_edispatch` | Odoo 19.0 (LGPL) | 718 | 102 | 670 | 126 |
| `account_statement_base` | OCA account-reconcile | 103 | 92 | 299 | 0 |
| `account_reconcile_oca` | OCA account-reconcile | 2500 | 2400 | 1195 | 1291 |
| `account_statement_import_base` | OCA bank-statement-import | 108 | 0 | 25 | 0 |
| `account_statement_import_file` | OCA bank-statement-import | 445 | 152 | 116 | 0 |
| `account_statement_import_sheet_file` | OCA bank-statement-import | 796 | 429 | 193 | 0 |
| `account_financial_report` | OCA account-financial-reporting | 7714 | 2792 | 4884 | 115 |
| `account_tax_balance` | OCA account-financial-reporting | 484 | 323 | 186 | 0 |
| `partner_statement` | OCA account-financial-reporting | 2861 | 1301 | 818 | 0 |
| `mis_builder` | OCA mis-builder | 5117 | 3009 | 1344 | 293 |
| `quality_control_oca` | OCA manufacture | 860 | 289 | 1007 | 0 |
| `report_xlsx` | OCA reporting-engine | 351 | 85 | 14 | 51 |
| `report_xlsx_helper` | OCA reporting-engine | 1102 | 30 | 0 | 0 |
| `date_range` | OCA server-ux (**20.0'da var**) | 721 | 574 | 311 | 454 |
| **Toplam** | | **27 892** | **12 379** | **14 102** | **2 330** |

Satır sayıları boş satırlar dahil. Python sütunu testleri içermez.

## 4. Sonuçlar

| Modül | `raw` | `upg` | `fix` | Kalan sorun |
|---|---|---|---|---|
| `date_range` | 19/19 | 19/19 | — | Yok (OCA 20.0) |
| `report_xlsx` | kurulamaz | kurulamaz | **4/4** | — |
| `report_xlsx_helper` | kurulamaz | kurulamaz | **1/1** | — |
| `account_statement_base` | kurulamaz | kurulamaz | **1/1** | — |
| `account_statement_import_base` | kurulamaz | kurulamaz | kurulur (testi yok) | — |
| `account_statement_import_file` | kurulamaz | kurulamaz | **3/3** | — |
| `account_statement_import_sheet_file` | kurulamaz | kurulamaz | **15/15** | — |
| `account_tax_balance` | kurulamaz | **4/4** | — | — |
| `mis_builder` | kurulamaz | kurulamaz | **98/98** | — |
| `partner_statement` | kurulamaz | kurulamaz | **36/36** | Yalnız Windows'a özgü test temizliği hatası (§8) |
| `account_reconcile_oca` | kurulamaz | kurulamaz | **44/47** | 3 dövizli mutabakat testi: kur farkı davranışı değişmiş |
| `l10n_tr_nilvera` | kurulamaz | kurulamaz | kurulur (testi yok) | — |
| `l10n_tr_nilvera_base_vat` | kurulamaz | kurulamaz | kurulur (testi yok) | 20.0'da `l10n_tr_nilvera`'ya katılabilir |
| `l10n_tr_nilvera_einvoice` | kurulamaz | kurulamaz | **17/18** | 1 test: 20.0 çekirdeğindeki UBL içe aktarma hatası (§8) |
| `l10n_tr_nilvera_einvoice_extended` | kurulamaz | kurulamaz | 1/9 | Test beklentileri: kişi/şirket ayrımı (5), vade tarihi (3) |
| `l10n_tr_gib_invoice_scenarios` | kurulamaz | kurulamaz | 0/2 | Test beklentileri: kişi/şirket ayrımı |
| `l10n_tr_nilvera_edispatch` | kurulamaz | kurulamaz | 0/1 | Gelen irsaliyeden sevkiyat oluşmuyor; incelenmedi |
| `quality_control_oca` | kurulamaz | kurulamaz | kurulur, 0/10 | Yetki hatası (20.0 yetki modeli); incelenmedi |
| `account_financial_report` | kurulamaz | kurulamaz | kurulamaz | `account.group` modeli 20.0'da yok (§6) |

`n/m`: kurulur, m testten n'i geçer. "—": o ağaçta yeniden denenmedi.

Özet:
- `raw`: 1/19 modül kuruluyor (`date_range`, zaten 20.0 sürümü).
- `upg`: 2/19. Otomatik dönüştürücü tek başına yetmiyor; asıl engeller dönüştürücünün kapsamı dışında.
- `fix`: 18/19 kuruluyor. 9 modül tüm testlerini geçiyor, 3 modülün test dosyası yok.
- Toplam test: 268 testin 243'ü geçiyor (`account_financial_report` hariç).

## 5. Uyarlama kataloğu

### 5.1 Otomatik dönüştürücü (`upgrade_code`)

| Betik | Değişen dosya |
|---|---:|
| `19.1-00-t-call` | 7 |
| `19.4-00-ir-access` (`ir.model.access.csv` → `ir.access.csv`, kayıt kuralları dahil) | 40 |
| `19.5-00-tuple-rec_names_search` | 1 |
| `owl3-migration` (JS) | 15 |
| Diğer 5 betik | 0 |

Toplam: 63 dosya, +316/−361 satır.

Windows'ta dönüştürücünün kendisi düzgün çalışmıyor. Ölçüm için sarmalayıcı betik yazıldı; T1.11'de araç olarak depoya alındı (`tools/port_oca.py upgrade`). `account_financial_report` denemesinde sonuç bu ölçümle aynı.
- Yol denetimleri `/static/` gibi POSIX ayırıcıları bekliyor. Windows'ta `owl3-migration` hiçbir dosya görmüyor, `t-call` betiği statik şablonları da değiştiriyor.
- Varsayılan kodlama cp1252: `PYTHONUTF8=1` gerekiyor.
- `--from` seçeneği silinen dosyalarda çöküyor.
- `ir-access` betiği çekirdek modülleri de yolda istiyor ve çekirdek dosyalarına yazıyor. Çekirdek kopyası sonradan geri alındı.

### 5.2 Elle uyarlamalar

| # | Tür | 20.0 değişikliği → uyarlama | Modüller | Dosya | Satır |
|---:|---|---|---|---:|---:|
| 1 | Python API | `odoo.http` paket oldu: `content_disposition` → `odoo.http.stream`, `serialize_exception` → `odoo.http.dispatcher` | report_xlsx, report_xlsx_helper | 2 | 4 |
| 2 | Alan | `account.move.checked` (Boolean) → `review_state` (Selection): arama filtresi | account_statement_base | 1 | 1 |
| 3 | Alan | `ir.actions.report.report_file` kaldırıldı | report_xlsx, account_financial_report, partner_statement, mis_builder | 7 | 30 |
| 4 | Python API | `base.models.res_bank` → `base.models.res_partner_bank` | account_statement_import_* | 2 | 2 |
| 5 | Model | `res.bank` kaldırıldı, banka alanları `res.partner.bank`'ta; `acc_number` → `account_number` | account_statement_import_*, account_reconcile_oca, l10n_tr_nilvera_einvoice | 10 | 42 |
| 6 | Binary API | Binary alanlar `BinaryValue` tutuyor: base64 bayt yazılamaz, okuma `.content`; `ir.attachment.datas` → `raw` | account_statement_import_*, l10n_tr_nilvera_edispatch | 5 | 9 |
| 7 | Alan | `checked` → `review_state`: model, kanban, form | account_reconcile_oca | 2 | 7 |
| 8 | Python API | `Query` `odoo.models`'e taşındı; kurucu `Query(model)` | account_reconcile_oca | 2 | 8 |
| 9 | Python API | `odoo.tools.sql.pg_varchar` kaldırıldı | account_reconcile_oca | 1 | 2 |
| 10 | Görünüm | Görünüm arch'ında `t-esc` yasak → `t-out` | account_reconcile_oca, quality_control_oca | 2 | 9 |
| 11 | Python API | `Query.order` doğrudan `SQL` alıyor | account_reconcile_oca | 1 | 1 |
| 12 | Test altyapısı | `WebSuite`/`CrossModule`: test yöntemi `modules` parametresi alıyor | account_reconcile_oca | 1 | 5 |
| 13 | Python API | `odoo.api.deprecated` kaldırıldı; 19.0'da zaten kullanım dışı yardımcı yöntem silindi | l10n_tr_nilvera_einvoice | 1 | 13 |
| 14 | Python API | `_auto = False` modellerde `_table_query` → `_table_sql` (`SQL`) | account_reconcile_oca | 1 | 3 |
| 15 | Test | Testlerde `checked` → `review_state` | account_reconcile_oca | 1 | 6 |
| 16 | Python API | `ir.config_parameter` `get_param`/`set_param` → tipli `get_str`/`set_str` | l10n_tr_nilvera_einvoice | 1 | 3 |
| 17 | Test | `attachment.raw` artık `BinaryValue`: `.content.startswith` | l10n_tr_nilvera_einvoice | 1 | 2 |
| 18 | Davranış | `is_company` artık VKN varlığından hesaplanıyor; Türkiye için 11 haneli TCKN → kişi (`_compute_is_company`) | l10n_tr_nilvera | 1 | 9 |
| 19 | Python API | `odoo.tools.safe_eval` paket oldu: iç işlevler `safe_eval.evaluation`'da | mis_builder | 1 | 1 |
| 20 | Test altyapısı | `odoo.tools.test_reports` → `odoo.tests.reports` | mis_builder, account_financial_report | 2 | 3 |
| 21 | Python API | Domain operatörü `<>` kaldırıldı → `!=` | mis_builder | 2 | 4 |

Dosya ve satır sütunları uyarlamanın kendi kaydı. `upg` → `fix` farkının ölçümü: 36 dosya, +96/−145 satır.

Gözlemler:
- 21 türün 16'sı bir veya iki satırlık, aranıp bulunabilen değişiklik. Gelecek portlarda bir kontrol listesi ve arama betiğiyle hızlanır.
- Gerçek davranış değişikliği bir tane: #18. 20.0'da `is_company`, kişinin elle seçtiği bir kutu değil; vergi numarasından hesaplanıyor. e-Faturada `cac:Person` düğümü buna bağlı. Türkiye kuralı (10 hane VKN = tüzel kişi, 11 hane TCKN = gerçek kişi) bizim e-Belge çekirdeğine (T4.3) girmeli.

### 5.3 20.0 API değişiklikleri (port kontrol listesi)

Yukarıdaki uyarlamalardan ve denemede görülen hatalardan derlenen liste:

- `odoo.http` artık paket. Yalnız `request`, `Response`, `Controller`, `route` doğrudan alınabiliyor.
- `odoo.tools.Query` yok: `from odoo.models import Query`, kurucu `Query(model, alias=None, table=None)`.
- `odoo.tools.safe_eval` paket; `odoo.tools.test_reports` → `odoo.tests.reports`.
- `odoo.api.deprecated` yok.
- `odoo.tools.sql.pg_varchar` yok.
- `_table_query` yok; SQL görünüm modelleri `_table_sql` özelliğini `SQL` olarak döndürüyor.
- `ir.config_parameter`: tipli `get_str/get_int/get_float/get_bool` ve `set_*`.
- Binary alanlar `BinaryValue` döndürüyor; `ir.attachment.datas` yok.
- `res.bank` yok; banka bilgileri `res.partner.bank`'ta, `acc_number` → `account_number`.
- `account.move.checked` yok; `review_state` var ("kontrol edilecek" = `todo` veya `anomaly`).
- `account.group` yok; hesap hiyerarşisi `account.account.parent_id` ile (`_parent_store`).
- `ir.actions.report.report_file` yok.
- `base_vat` `base`'e katıldı; `check_vat_tr` `base`'te.
- Vergi daireleri `l10n_tr`'de `l10n_tr.tax.office` modeli olarak var (1046 kayıt). 19.0'daki `l10n_tr_nilvera_einvoice_extended` kendi vergi dairesi modelini getiriyordu; port çekirdeğinkini kullanmalı (T4.3).
- `ir.model.access.csv` + `ir.rule` → `ir.access.csv`.
- Görünüm arch'ında yalnız belirli QWeb yönergeleri serbest; `t-esc` yasak.
- Domain operatörü `<>` yok.
- `is_company` hesaplanan alan (bkz. #18).
- Manifest sürümü `20.0.` ile başlamak zorunda.

## 6. Kalan iş ve emek tahmini

Boyutlar PLAN.md'deki ölçekle (S ≈ 1 oturum, M ≈ 2–3, L ≈ 4–8).

| Kalem | Görev | Tahmin | Not |
|---|---|---|---|
| §5.2'deki mekanik uyarlamaların gerçek port dalında yeniden yapılması | T4.1, T5.1 | S | Kontrol listesi hazır |
| `account_financial_report`: `account.group` → hesap hiyerarşisi | T5.4 | L | 12 dosyada 115 atıf; mizan ve muavin gruplaması yeniden yazılır |
| `account_reconcile_oca`: 3 dövizli test, OWL3 arayüzün elle denetimi | T5.3 | M | Testlerin dışında arayüz denetimi gerekli; JS'in 15 dosyası otomatik dönüştürüldü |
| `quality_control_oca`: yetki hatası | T6.4 | S | 10 testin hepsi aynı hatayla düşüyor |
| Nilvera ailesi: test beklentileri, e-İrsaliye mal kabulü | T4.3–T4.8 | S–M | Bu modüller zaten yeniden yapılandırılacak (çekirdek + adaptör); port emeği bu görevlerin içinde |
| 20.0 çekirdek hatası (UBL içe aktarma) | T4.7 | — | Upstream düzeltmesi beklenir; olmazsa modülde geçici çözüm |

**Toplam ek emek:** yaklaşık 9–15 oturum. Bu iş zaten var olan port görevlerinin (T4.x, T5.2–T5.6, T6.4) içinde; plana yeni görev eklemek gerekmiyor.

OCA bu modüllerin bir kısmını o tarihe kadar 20.0'a taşıyabilir (§9). Taşınanlar `vendor/`'a alınır, port emeği düşer (D-019).

## 7. 19.0'a dönmenin bedeli

19.0'da bugün port işi yok. Ama:

- **Destek süresi bir yıl kısa.** 19.0'ın standart desteği Eylül 2028'de bitiyor, 20.0'ınki Eylül 2029'da. Güvenlik düzeltmeleri yalnız standart destek boyunca çıkıyor.
- **Göç ertelenmiş olur, ortadan kalkmaz.** Eylül 2028'den önce tüm müşteriler 20.0 veya 21.0'a taşınmalı.
  - O gün taşınacaklar: §5'teki aynı modüller, artı o tarihe kadar 19.0 üzerinde yazılmış bütün `ov_` modüllerimiz, artı her müşterinin veritabanı.
  - Community'de Odoo'nun ücretli sürüm yükseltme hizmeti yok. Veritabanı göçü OpenUpgrade ile ya da kendi betiklerimizle yapılır.
- **Nilvera yine port edilecek.** 20.0'dan itibaren Community'de Türkiye e-Belge modülü yok. 19.0'da Odoo'nun bakımını yaptığı LGPL modülleri kullanmak bugün kolay, ama 2028'de bu modüller bizim sorumluluğumuza geçiyor.
- **19.0'ın avantajı:** OCA modülleri bugün kurulabilir; Nilvera modüllerinin bakımı 2028'e kadar Odoo'da.

Değerlendirme: 19.0'ın avantajı kısa vadeli. Bugünkü port emeği (9–15 oturum) MVP takviminde küçük. 2028'deki göç ise müşteri veritabanlarıyla birlikte daha pahalı ve riskli.

## 8. Denemede görülen diğer bulgular

- **20.0 henüz taze.** Denenen commit'te Community çekirdeğinde hata var:
  - `account_edi_ubl_cii`, satır değerlerine yalnız Enterprise'da olan `deferred_start_date` alanını koyuyor. Community'de UBL fatura içe aktarma bu yüzden hata veriyor.
  - Çekirdeğin kendi testleri de bu ortamda tam geçmiyor: `account_edi_ubl_cii` 230 testten 199'u geçiyor. Hataların çoğu aşağıdaki Windows sorunu; bir kısmı bu çekirdek hatası ve yerelde PDF motoru (wkhtmltopdf) olmaması.
  - Linux referansı (CI, 2026-10-18, upstream `afbcf79d`): `l10n_tr` + `account_edi_ubl_cii` 233 test, 4 hata:
    - `test_invoice_deferred_dates`: test, Enterprise alanı `deferred_start_date`'i yazıyor;
    - `test_import_ubl_21_line_description`: içe aktarılan faturada satır yok (nedeni incelenmedi);
    - PDF motoru olmadığı için 2 PDF üretim testi. Windows'taki 27 gc hatası ve `LocalBinaryFile` hatası Linux'ta yok.
  - Önlem: upstream sabit commit'te tutulur (T1.4) ve düzenli güncellenir. Çekirdek yamalanmaz (D-010). Gerekirse kendi modülümüzde geçici çözüm.
- **Windows'ta test temizliği hatalı.** 20.0, filestore dosyalarını salt okunur yazıyor. Testlerin sonundaki çöp toplama, Windows'ta bu dosyaları silemiyor (`PermissionError`) ve `tearDownClass` hatası üretiyor. Linux'ta bu sorun beklenmiyor.
  - Önlem: test sonuçlarının referansı Linux CI (T1.10). Yerel test komutları (T1.8) bu hatayı ayırt edecek şekilde yazılır.
- **PDF motoru.** 20.0 PDF için hâlâ wkhtmltopdf kullanıyor; yerelde ve CI'da kurulu değil. T1.6'da incelendi, seçim T2.5'te.

## 9. OCA'nın geçiş gecikmesi

Ölçüm: OCA, modülü yeni dala taşırken modülün bütün geçmişini o dala getiriyor. Bu commit'lerin "committer" tarihi, modülün dala girdiği tarih. GitHub API'den modülün o daldaki en eski committer tarihi alındı.

Odoo ana sürüm çıkışları: 17.0 Kasım 2023, 18.0 Ekim 2024, 19.0 Eylül 2025.

| Modül | 17.0 | 18.0 | 19.0 |
|---|---|---|---|
| `report_xlsx` | 2023-11-22 | 2024-10-25 | 2025-10-13 |
| `date_range` | 2023-11-26 | 2024-10-15 | 2025-11-05 |
| `account_statement_base` | 2023-12-15 | 2024-11-07 | 2025-10-21 |
| `account_tax_balance` | 2023-11-26 | 2024-12-06 | 2025-11-12 |
| `account_financial_report` | 2024-01-24 | 2024-11-29 | 2025-11-24 |
| `account_statement_import_file` | 2024-05-08 | 2024-12-17 | 2025-11-05 |
| `account_reconcile_oca` | 2024-02-07 | 2025-02-25 | 2026-03-06 |
| `partner_statement` | 2024-06-25 | 2025-07-22 | 2026-01-13 |
| `account_statement_import_sheet_file` | 2024-05-15 | 2025-12-17 | 2026-03-10 |
| `quality_control_oca` | 2024-05-14 | 2025-07-29 | 2026-05-13 |

`mis_builder` ve `queue_job` bu yöntemle ölçülemedi (geçmişleri dala yeniden yazılmamış).

Okuma:
- Altyapı ve temel muhasebe modülleri sürümden sonraki 0–3 ay içinde geliyor.
- Banka mutabakatı, cari ekstre ve kalite kontrol 4–14 ay sürüyor.
- 20.0 Eylül 2026'da çıktı. Bu desenle F5'e gelindiğinde (T5.x) bir kısım modül resmî 20.0 sürümüyle `vendor/`'a alınabilir. T5.1 bunu o tarihte yeniden ölçer.

## 10. Kaynaklar

- Odoo 20.0 Community kaynak kodu, commit `afbcf79d` (2026-10-18): `odoo/upgrade_code/*`, `odoo/orm/*`, `odoo/http/*`, `odoo/tools/*`, `addons/account*`, `addons/l10n_tr`.
- Odoo 19.0 Community kaynak kodu, commit `53ec5874` (2026-10-17): `addons/l10n_tr_nilvera*`, `addons/l10n_tr_gib_invoice_scenarios`.
- OCA depoları, 19.0 ve 20.0 dalları (2026-10-18 kontrolü): account-financial-reporting, account-reconcile, bank-statement-import, manufacture, mis-builder, reporting-engine, server-ux.
- OCA geçiş tarihleri: GitHub REST API, `repos/OCA/<depo>/commits?sha=<dal>&path=<modül>` (2026-10-18).
- Destek süreleri: odoo/documentation deposu, `content/administration/standard_extended_support.rst`.
