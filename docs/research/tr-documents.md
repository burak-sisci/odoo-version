# Türkçe Belge Çıktıları

Son güncelleme: 2026-11-05
Araştırma tarihi: 2026-11-05
İlgili kararlar: D-006, D-010 (DECISIONS.md); USER_TASKS K18, K25
İlgili görev: T3.7 (PLAN.md); sonuçları kullanan görevler T4.x (e-Fatura, e-İrsaliye), T9.4

> **Sonuç (2026-11-05, öneri):** upstream 20.0'ın teklif, sipariş, proforma, irsaliye, fatura ve ödeme makbuzu şablonları Türkçe basılıyor ve müşterinin adı, adresi, vergi dairesi ve VKN'si çoğunda var. Eksikler (§4):
> - şirketin MERSİS ve ticaret sicil numarası, web adresi (TTK 39);
> - irsaliyede belge adı, düzenleme ve fiili sevk tarihi, alıcının VKN'si (VUK 230/5);
> - "tutar yazıyla" yalnız faturada ve kapalı; Türkçede "İki" yerine "Iki" yazıyor;
> - makbuzların adı ("Ödeme Makbuzu", "Ödeme Bildirimi").
>
> Çözüm modüllerle (§5), uygulandı ve ölçüldü (§5.1): `ov_l10n_tr` (şirket bilgileri, fatura, makbuz, tutar yazıyla), `ov_l10n_tr_sale` ve `ov_l10n_tr_stock` (kendiliğinden kurulan köprüler). Belge içeriğindeki varsayımlar USER_TASKS **K25**'te ve açık (öneri). Kâğıt irsaliyenin yasal geçerliliği mali müşavire sorulacak (§6). PDF denetimi kaldı (K18).

## 1. Soru

Nexus'un ilk satış paketindeki ticari belgeler (teklif, sipariş, proforma, irsaliye, tahsilat ve tediye makbuzu) Türkiye'de beklenen bilgileri taşıyor mu? Eksikler çekirdeğe dokunmadan (D-010) nasıl tamamlanır?

Fatura burada yalnız kâğıt/PDF görünümüyle ele alınıyor. Yasal fatura e-Fatura/e-Arşiv'dir (T4.x, `docs/research/e-fatura.md`).

## 2. Yasal içerik (birincil kaynaklar)

### 2.1 Fatura ve sevk irsaliyesi — 213 sayılı Vergi Usul Kanunu

Kaynak: mevzuat.gov.tr, 213 sayılı Kanun metni (2026-11-05'te indirildi).

- **VUK 230** — faturada en az şunlar bulunur:
  1. düzenlenme tarihi, seri ve sıra numarası;
  2. düzenleyenin adı, varsa ticaret unvanı, iş adresi, bağlı olduğu vergi dairesi ve hesap (vergi) numarası;
  3. müşterinin adı, ticaret unvanı, adresi, varsa vergi dairesi ve hesap numarası;
  4. malın veya işin nev'i, miktarı, fiyatı ve tutarı;
  5. satılan malların teslim tarihi ve irsaliye numarası.
- **VUK 230/5** — malın taşınmasında sevk irsaliyesi düzenlenir. Mükellefin iş yerleri arasında ya da komisyoncuya gönderilen mal da irsaliyeye bağlanır.
  - İrsaliyeye 230 ve 231. maddeler "fiyat ve bedel ile ilgili bilgiler hariç" uygulanır. Yani düzenleme tarihi, seri-sıra numarası, iki tarafın adı, adresi, vergi dairesi ve numarası, malın cinsi ve miktarı.
  - "İrsaliyelerde malın nereye ve kime gönderildiği ayrıca belirtilir."
- **VUK 231/5** — fatura, teslimden itibaren en geç yedi gün içinde düzenlenir.
- Kanunun belge maddelerinde (229–242: fatura, perakende satış vesikaları, gider pusulası, müstahsil makbuzu, serbest meslek makbuzu, ücret bordrosu, sevk irsaliyesi) **tahsilat makbuzu, tediye makbuzu ve proforma yok**. Bunlar işletmenin iç belgeleri ya da ticari teklif belgeleridir; biçimleri yasayla belirlenmemiş.

### 2.2 Ticari belgeler — 6102 sayılı Türk Ticaret Kanunu

Kaynak: mevzuat.gov.tr, 6102 sayılı Kanun metni (2026-11-05'te indirildi).

- **TTK 39/2:** tacirin ticari mektuplarında ve ticari defterlere yapılan kayıtların dayandığı belgelerde şunlar gösterilir:
  - sicil numarası;
  - ticaret unvanı;
  - işletmesinin merkezi;
  - internet sitesi kurma yükümlülüğü varsa tescilli internet sitesinin adresi.
- Teklif, sipariş, irsaliye ve makbuz bu kapsamdadır. MERSİS numarası sicil kaydının numarasıdır. Eski ticaret sicil numarası da kullanılıyor; belgede ikisi birlikte yazılabilir (K25).

### 2.3 Tutarın yazıyla yazılışı — TDK Yazım Kuralları

Kaynak: tdk.gov.tr, "Sayıların Yazılışı" (2026-11-05).

- Kural 2: birden fazla kelimeden oluşan sayılar ayrı yazılır.
- Kural 3: **"Para ile ilgili işlemlerle senet, çek vb. ticari belgelerde geçen sayılar bitişik yazılır."**
- Belgelerdeki "yazıyla" tutar bu yüzden bitişik yazılır: "binikiyüzotuzdört". num2words'ün Türkçe çıktısı bu kurala uyuyor.
- Para biriminin adı Türk Lirası, alt birimi kuruştur (5083 sayılı Kanun).

### 2.4 Kâğıt irsaliye ve e-İrsaliye (ikincil kaynaklar, doğrulanacak)

- Kâğıt sevk irsaliyesi, Maliye ile anlaşmalı matbaalarda seri ve sıra numarasıyla bastırılan belgeye düzenlenir. Bilgisayarla düzenlenen irsaliye de bu matbu forma basılır.
- e-İrsaliye kapsamındaki mükellef (509 sıra no. VUK Genel Tebliği) kâğıt irsaliye kullanamaz. Yalnız sistem arızası gibi istisnai durumlarda kâğıt belgeye izin verilir.
- Kaynaklar muhasebe yayınları ve TÜRMOB e-Dönüşüm SSS sayfalarıdır, birincil tebliğ metni değildir. Mali müşavirle doğrulanacak (§6).
- Sonuç: Nexus'un ürettiği irsaliye PDF'i tek başına yasal sevk irsaliyesi sayılmayabilir. Ya anlaşmalı matbaanın formuna basılır ya da e-İrsaliye (T4.x) gönderilir; PDF iç kullanım ve yedek içindir.

## 3. Upstream 20.0'ın ölçümü

Ortam: `ov_t37` veritabanı. Kurulu olanlar: Türkçe dil, ülke TR, `ov_brand`, `sale_management`, `sale_stock`, `purchase_stock`, `mrp`, `l10n_tr`, `ov_l10n_tr`, `ov_i18n_tr`; hesap planı `tr`.

Kurgusal veri:
- satıcı: şirket, VKN, vergi dairesi, MERSİS, sicil numarası, web adresi;
- müşteriler: VKN'li bir şirket ve TCKN'li bir kişi;
- belgeler: iki ürünlü teklif → sipariş → teslimat → fatura → tahsilat, ve bir tedarikçi ödemesi.

Her rapor HTML olarak basıldı, metni çıkarılıp okundu.

| Belge | Var | Eksik / hatalı |
|---|---|---|
| Ortak üst bilgi (şirket) | unvan, adres ("34710 Kadıköy/İstanbul"), vergi dairesi, VKN | MERSİS, sicil numarası, web adresi yok. Numaranın etiketi "VKN/TCKN" (hangisi olduğu belli değil). Alt bilgi, kullanıcı belge düzenini kaydetmedikçe boş. |
| Teklif, sipariş | müşterinin adı, adresi, vergi dairesi, "VKN/TCKN: …", tarih, geçerlilik, satırlar, KDV, toplam | tutar yazıyla yok |
| Proforma | başlık "Proforma Fatura No", "Düzenlenme Tarihi" | tutar yazıyla yok |
| İrsaliye | teslimat adresi, vergi dairesi, sipariş no, "Sevkiyat Tarihi", ürün ve miktar | belge adı "Teslimat Notu"; alıcının VKN'si yok; düzenleme tarihi ile fiili sevk tarihi (VUK 230/5) ayrı değil, saat yok |
| Fatura (PDF görünümü) | müşterinin bilgileri, fatura, vade ve teslim tarihi, kaynak sipariş | tutar yazıyla şirket ayarıyla açılıyor, varsayılan kapalı |
| Tahsilat | müşteri, tarih, tutar, faturalar | adı "Ödeme Makbuzu"; tutar yazıyla yok; ödeme yöntemi "Manual Payment" (çevrilmemiş kayıt) |
| Tediye | tedarikçi, tarih, tutar | adı "Ödeme Bildirimi"; tutar yazıyla yok |

Tutar yazıyla (`res.currency.amount_to_text`, dil `tr_TR`):
- 1.234,56 → "Binikiyüzotuzdört Lira ve Ellialtı Kuruş";
- 2.000 → **"Ikibin Lira"**: upstream sözcükleri Python'un `str.title()` işleviyle büyütüyor. Bu işlev Türkçe "i → İ" kuralını bilmiyor; "iki" ile başlayan her tutar yanlış yazılıyor (2, 200, 2.000, 2.500 …).

## 4. Bulgular

- **B1 — şirketin sicil bilgileri (TTK 39):** MERSİS ve ticaret sicil numarası iş ortağının ek kimliklerinde (`additional_identifiers`: `TR_MERSIS`, `TR_TICARET_SICIL`) tutuluyor, belgede görünmüyor. Web adresi de yok.
- **B2 — numaranın adı:** ülkenin vergi numarası etiketi "VKN/TCKN" (T3.3). Belgede numaranın türü belli: 10 hane VKN, 11 hane TCKN.
- **B3 — irsaliye (VUK 230/5):** belge adı, alıcının vergi bilgileri, düzenleme tarihi ile fiili sevk tarihinin ayrı yazılması.
- **B4 — tutar yazıyla:** "Iki" hatası. Teklif, sipariş, proforma ve makbuzlarda gösterilmiyor; faturada varsayılan kapalı. Türk belgelerindeki alışkanlık "Yalnız: … Türk Lirası … Kuruş".
- **B5 — makbuz adları:** Türk muhasebesinde para girişinin belgesi tahsilat makbuzu, çıkışının belgesi tediye makbuzu.
- **B6 — çeviri:** ödeme yöntemi satırının adı ("Manual Payment"), hesap planı yüklenirken çevrilmeden kopyalanıyor. Bu bir çeviri işidir (T3.6 yöntemi, `ov_i18n_tr`); ayrıca ele alınır.

## 5. Çözüm (öneri; T3.7)

Çekirdeğe dokunulmaz (D-010). Şablonlar ada bağlı kalıtımla genişletilir. Değişikliğin neye bağlı olduğu:
- şirket bloğu, makbuz adı, makbuz ve satış belgelerinde tutar yazıyla, irsaliye: şirketin mali ülkesi TR;
- faturada müşterinin numara satırı: müşterinin ülkesi TR ve numarası var (yabancı şirketin Türk müşterisine kestiği faturada da);
- tutarın Türkçe yazılışı: belgenin dili Türkçe (hangi şirket basarsa bassın; diğer dillerde upstream'in yazılışı).

- `ov_l10n_tr` (`account` düzeyi):
  - Tutar yazıyla, Türkçe: bitişik, Türkçe büyük harf ("İkibin"), "ve"siz: "Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş". Birim adları para biriminin çevrilmiş etiketlerinden.
  - Şirket bloğu: "VKN" ya da "TCKN" etiketi; MERSİS No, Ticaret Sicil No ve web adresi girilmişse.
  - Faturada müşterinin numarası "VKN: …" / "TCKN: …"; TR şirketlerinde tutar yazıyla varsayılan açık ve "Yalnız:" ile.
  - Makbuz adı: para girişinde "Tahsilat Makbuzu", çıkışında "Tediye Makbuzu"; tutar yazıyla.
- `ov_l10n_tr_sale` (`sale` + `ov_l10n_tr`, kendiliğinden kurulur): teklif, sipariş ve proformada numara etiketi ve "Yalnız: …".
- `ov_l10n_tr_stock` (`stock` + `ov_l10n_tr`, kendiliğinden kurulur), çıkış irsaliyesinde:
  - belge adı "Sevk İrsaliyesi";
  - alıcının unvanı, adresi, vergi dairesi ve numarası;
  - düzenleme tarihi;
  - fiili sevk tarihi ve saati: işlem tamamlanmamışsa elle doldurulacak boş satır.
- Doğrulama: her belge için testte metin denetimi (beklenen etiketler ve değerler, yabancı şirkette değişiklik yok); tutar yazıyla için sayı tablosu. PDF olarak iki motorla basılması CI'da (K18).

### 5.1 Uygulama ve ölçüm (2026-11-05)

- Yukarıdaki çözüm uygulandı. Aynı kurgusal şirket ve müşteriyle sekiz belge (teklif, proforma, sipariş, irsaliye, fatura, tahsilat ve tediye makbuzu, gerçek kişiye teklif) değişiklikten önce ve sonra HTML olarak basılıp metni karşılaştırıldı:
  - yedi belgede "Yalnız: … Türk Lirası … Kuruş" (irsaliyede tutar yok);
  - sekiz belgede MERSİS No, Ticaret Sicil No ve web adresi;
  - irsaliyede "Sevk İrsaliyesi", Müşteri bloğunda VKN, Düzenleme Tarihi ve saatli Fiili Sevk Tarihi.
- Kalıcı testler: `ov_l10n_tr` 11 (tutar yazıyla 7 satırlık tablo, numara satırı, makbuz adları, şirket bloğu, yabancı şirket), `ov_l10n_tr_sale` 4, `ov_l10n_tr_stock` 5.
- "Türk Lirası": TRY'nin birim adının upstream çevirisi "Lira"; düzeltme `ov_i18n_tr` katmanında. Bu kayıt müşterinin değiştirebileceği (noupdate) bir kayıt olduğu için katman düzeltmesi yeni veritabanında da uygulanmıyordu. `ov_i18n_tr` kurulurken çeviri hâlâ upstream'in değeriyse artık katmanınki yazılıyor (ölçüm: yeni Türkçe veritabanında uygulanmayan katman kayıt terimi 6/259 → 5/259; kalan 5 terim belgelerle ilgisiz, CHANGELOG 2026-11-05).
- Faturadaki "Yazı ile toplam tutar" etiketi `ov_i18n_tr` katmanında "Yalnız:" oldu.
- Kalan: PDF olarak iki motorla basılması (CI, K18).

## 6. Açık sorular (mali müşavir)

- Kâğıt irsaliyenin geçerliliği (§2.4): müşteri anlaşmalı matbaa formu mu kullanacak, yoksa e-İrsaliye mi? Nexus'un PDF'i hangi durumda yedek olarak kullanılabilir?
- Tutar yazıyla biçimi: "Yalnız: Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş" yaygın biçim mi, "TL/Kr." kısaltması mı tercih edilir?
- MERSİS ve eski ticaret sicil numarasının ikisi de mi yazılmalı?

## 7. Kaynaklar

- 213 sayılı Vergi Usul Kanunu, md. 229–242 (özellikle 230, 231): https://www.mevzuat.gov.tr/mevzuatmetin/1.4.213.pdf
- 6102 sayılı Türk Ticaret Kanunu, md. 39: https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6102.pdf
- TDK, Yazım Kuralları — Sayıların Yazılışı: https://tdk.gov.tr/icerik/yazim-kurallari/sayilarin-yazilisi/
- TÜRMOB e-Dönüşüm, e-İrsaliye SSS (ikincil): https://www.turmob.org.tr/e-donusum/eirsaliye/sss
- Upstream 20.0: `sale/report/ir_actions_report_templates.xml`, `stock/report/report_deliveryslip.xml`, `account/views/report_invoice.xml`, `account/views/report_payment_receipt_templates.xml`, `web/views/report_templates.xml` (`company_address_list`), `base/models/res_currency.py` (`amount_to_text`).
