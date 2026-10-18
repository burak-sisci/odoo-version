# Planlama Girdileri

Son güncelleme: 2026-10-18
Araştırma tarihi: 2026-10-18
İlgili kararlar: D-011, D-017, D-018, D-019, D-020 (DECISIONS.md)

> Bu belge PLAN.md'yi besleyen bulguları ve kaynaklarını toplar. e-Belge bulguları `e-fatura.md` §6'da, barındırma bulguları `hosting.md`'de.
> Kontrol tarihindeki durumu anlatır. OCA dalları ve çeviri oranları hızla değişir; ilgili görevde yeniden ölçülür.

## 1. OCA 20.0 durumu (D-019)

Kontrol yöntemi: OCA GitHub depolarının 18.0 / 19.0 / 20.0 dallarındaki modül klasörleri.

| Modül | OCA deposu | 20.0 | 19.0 | Bizim için |
|---|---|---|---|---|
| `l10n-turkey` (depo) | l10n-turkey | boş | boş | Türkiye yerelleştirmesi OCA'da yok; kendimiz yazarız (PLAN F3, F4) |
| `account_statement_base`, `account_statement_import_file`, `account_statement_import_sheet_file` | bank-statement-import | yok | var | Port (T5.2) |
| `account_reconcile_oca` | account-reconcile | yok | var | Port (T5.3) |
| `account_financial_report` | account-financial-reporting | yok | var | Port (T5.4) |
| `account_tax_balance` | account-financial-reporting | yok | var | Port (T5.4, T5.8) |
| `partner_statement` | account-financial-reporting | yok | var | Port (T5.6) |
| `mis_builder`, `mis_builder_budget` | mis-builder | **var** | var | Doğrudan `vendor/` (T5.5) |
| `currency_rate_update` | currency | yok | var | TCMB için kendi modülümüz yeterli olabilir (T3.5'te karar) |
| `quality_control_oca` | manufacture | yok | var | Port (T6.4) |
| `mrp_multi_level` | manufacture | yok | var | Port (T11.2) |
| `account_asset_management` | account-financial-tools | yok | var | Port (T11.1) |
| `stock_barcodes` | stock-logistics-barcode | yok | yok | 20.0 için ayrı değerlendirme (T11.3) |
| `web_responsive` | web | yok | var | 20.0'da gerekip gerekmediği T7.5'te ölçülür |
| `queue_job` | queue | **var** | var | Gerekirse doğrudan `vendor/` |
| `remove_odoo_enterprise` | server-brand | **var** | var | Marka katmanında kullanılabilir (T2.3) |
| `disable_odoo_online` | server-brand | yok | var | Port veya kendi kodumuz (T2.3) |
| `base_technical_user`, `module_auto_update` | server-backend, server-tools | yok | var | Gerekirse port |

**Sonuç:**
- Ticaret ve Üretim paketlerinin ihtiyaç duyduğu OCA modüllerinin çoğu yalnız 19.0'da var.
- Bu, D-011'deki "MVP OCA'ya muhtaç değil" varsayımını geçersiz kıldı. D-011 bu yüzden T1.2'de yeniden değerlendirilecek: 20.0'da kalıp port etmek mi, 19.0'a dönmek mi daha ucuz?
- Port kuralları: D-019 (orijinal ad, lisans ve yazarlar korunur; resmî 20.0 sürümü çıkınca `vendor/`'a geçilir).

## 2. Türkçe çeviri kapsamı (20.0, `i18n/tr.po`)

Ölçüm: çevrilmiş `msgstr` sayısı / toplam `msgid` (yaklaşık). Ölçüm aracı ve eşik: PLAN T3.6.

| Modül | Kapsam |
|---|---|
| `base` | %84 |
| `web` | %81 |
| `account` | %87 |
| `sale` | %79 |
| `purchase` | %82 |
| `stock` | %85 |
| `mrp` | %82 |
| `crm` | %85 |
| `maintenance` | %93 |
| `project` | %78 |
| `point_of_sale` | %67 |
| `hr` | %69 |
| `hr_holidays` | %68 |
| `mail` | %68 |
| `website` | %71 |
| `l10n_tr` | %33 |
| `l10n_latam_check` | çeviri dosyası yok |

**Sonuç:** Ticaret ve Üretim paketlerinin çekirdek modülleri %79–93 aralığında. Eksikler ve terim tutarlılığı T3.6'da tamamlanır. `l10n_tr` ve çek/senet tabanı (T5.7) en zayıf noktalar.

## 3. Yerel 20.0 kontrolleri

İnceleme kopyası: Odoo 20.0, commit `1740e969d23e6e3e299e5f367a1b0fcc6d2170fe`.

- `mrp_subcontracting` (fason üretim) Community'de var → T6.7.
- `l10n_latam_check` (üçüncü taraf çekleri) Community'de var, LGPL-3 → çek/senet modülünün tabanı olarak uyarlanabilir (T5.7).
- `payment_iyzico` Community'de var → online tahsilat için ileride (P2).
- `hr_attendance` Community'de var → T11.6.
- Stok izlenebilirliği (lot/seri, izlenebilirlik raporu) Community'de var → T6.6.
- Python bağımlılıklarında `num2words` 0.5.13 (Türkçe "yalnız ... TL" yazısı için) ve `python-stdnum` (VKN/TCKN doğrulamasına yardımcı olabilir; T3.3'te kontrol edilir) var.
- `l10n_tr` ~1.046 vergi dairesi kaydı içeriyor (`e-fatura.md` §6).

## 4. Ücretsiz kaynaklar (D-020)

| Kaynak | Bulgu | Kaynak bağlantısı |
|---|---|---|
| GitHub Actions | Public depolarda standart GitHub-hosted runner kullanımı ücretsiz | GitHub Actions faturalandırma belgesi |
| GitHub Pages | Ticari iş, e-ticaret veya SaaS barındırmak için kullanılamaz. Site ≤ 1 GB, ~100 GB/ay esnek bant genişliği sınırı | GitHub Pages sınırları belgesi |
| Cloudflare Quick Tunnel | Hesap ve alan adı gerekmez. Yalnız test/geliştirme içindir; 200 eşzamanlı istek sınırı; SSE desteklenmez; her açılışta rastgele adres | Cloudflare TryCloudflare belgesi |
| GitHub Student Developer Pack | Örnekler: Azure kredisi (100 $), Heroku (24 ay boyunca aylık 13 $), Codespaces Pro, Namecheap `.me` alan adı, Name.com, `.TECH` alan adı, JetBrains, Sentry. DigitalOcean teklifi 31 Temmuz 2026'da sona ermiş (ikincil kaynak). Kullanıcı başvurusu gerekir (PLAN K1) | GitHub Education, Capital and Compute |
| TÜBİTAK 2209-A | 2026 çağrısı yayımlandı; son başvuru 11 Kasım 2026. Destek tutarı ve koşullar duyurudan kontrol edilmeli (**tutar doğrulanmadı**). İsteğe bağlı (PLAN K2) | TÜBİTAK çağrı duyurusu ve başvuru tarihleri sayfası |

## 5. Veri kaynakları

| Veri | Kaynak | Lisans / not | Görev |
|---|---|---|---|
| Döviz kurları | TCMB günlük XML: `https://www.tcmb.gov.tr/kurlar/today.xml` | Kamuya açık | T3.5 |
| İl / ilçe listesi | `siberfx/turkiye-address` (MIT) ve GitHub `turkiye-il-ilce-listesi` konusu altındaki depolar | Lisans T3.4'te yeniden kontrol edilir; seçilen kaynak COMPLIANCE §5 lisans envanterine yazılır | T3.4 |
| Vergi daireleri | 20.0 `l10n_tr` | LGPL-3 (upstream) | T3.1 |

## 6. Pazar referansları

- Odoo Enterprise: 2026'da kullanıcı başına aylık ~31,10 $ (Brussels Times, ecosire; ikincil kaynaklar). Fiyat araştırması T8.9'da yapılır.
- e-Belge sağlayıcıları muhasebe programı entegrasyonunu ücretli ek hizmet olarak satıyor (ör. Faturaport–Luca entegrasyonu, yıllık 1.000 TL). MVP'deki mali müşavire aktarım (T5.9) bu ihtiyaca karşılık gelir.

## Kaynaklar

- GitHub Actions faturalandırma: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- GitHub Pages sınırları: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Cloudflare Quick Tunnel (TryCloudflare): https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/
- GitHub Student Developer Pack: https://education.github.com/pack
- Student Pack 2026 özeti (ikincil): https://capitalandcompute.net/blog/github-student-developer-pack-2026/
- TÜBİTAK 2209-A 2026 çağrı duyurusu: https://tubitak.gov.tr/sites/default/files/2026-10/2209-A_2026_Yili_Cagri_Duyurusu.pdf
- TÜBİTAK 2209-A başvuru tarihleri: https://www.tubitak.gov.tr/tr/burslar/lisans/burs-programlari/2209-a/icerik-basvuru-tarihleri
- TCMB günlük kurlar: https://www.tcmb.gov.tr/kurlar/today.xml
- `siberfx/turkiye-address`: https://packagist.org/packages/siberfx/turkiye-address
- GitHub `turkiye-il-ilce-listesi` konusu: https://github.com/topics/turkiye-il-ilce-listesi
- Odoo fiyat artışı (Brussels Times): https://www.brusselstimes.com/business/2332306/odoo-announces-e10-billion-valuation-and-a-partial-price-increase
- Odoo sürüm ve fiyat özeti (ecosire): https://ecosire.com/blog/latest-odoo-version
- Faturaport–Luca entegrasyonu: https://faturaport.com/blog/e-donusum/faturaport-a-luca-entegrasyonu-eklendi
- Odoo 19.0 Türkiye yerelleştirme dokümanı: https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/turkiye.html
- OCA depoları: https://github.com/OCA
