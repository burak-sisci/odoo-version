# `l10n_tr` (20.0) Analizi

Son güncelleme: 2026-11-03
Araştırma tarihi: 2026-11-03
İlgili kararlar: D-006, D-008, D-010, D-011 (DECISIONS.md)
İlgili görev: T3.1 (PLAN.md); sonuçları kullanan görevler T3.2–T3.8, T4.3, T5.8, T6.2, T7.1

> **T3.3 sonucu (2026-11-03):** `ov_l10n_tr` 20.0.1.1.0 kimlik numarası eksiklerini kapattı (G16–G18; §3.4, §4).
> - TCKN'li iş ortağı gerçek kişi, VKN'li iş ortağı şirket; kural yalnız Türkiye için. e-Belge mükellef türü `res.partner._ov_l10n_tr_tax_id_type()`.
> - Ülke etiketi "VKN/TCKN"; yer tutucu ve geçersiz numara hatası Türkçe.
> - MERSİS 16 hane denetleniyor. İç yapısı (0 + VKN + 5 hane) yalnız ikincil kaynaklarda geçtiği için denetlenmiyor.

> **T3.2 sonucu (2026-11-03):** `ov_l10n_tr` modülü ad, hesap ve vergi eksiklerini kapattı (G1–G4, G6–G8 vergi kısmı, G11, G13, G24; §4).
> - Ölçüm (`ov_demo`, Türkçe bağlam): sorunlu ad sayısı 86'dan 0'a indi. Kapsam: 366 hesap, 15 vergi grubu, 46 vergi, 8 mali pozisyon.
> - Kalıcı ad testi upstream'in 400 Türkçe adından 35'ini işaretliyor; T1.6'da elle görülen örneklerin hepsi bunların içinde.
> - T3.2'de üç yeni hata bulundu (G27–G29, §3.6):
>   - şirketin özel hesapları plan dışı 999 kodlu hesaplara bağlanıyordu;
>   - kira stopajı 191 İndirilecek KDV hesabına kaydediliyordu;
>   - 193 ve 360 alacak/borç hesabı türünde olduğu için bu hesaplara vergi kaydedilemiyordu.
> - %10/%1 oranlı tevkifat ve istisna tanımları (G9, G10) T4.3'e taşındı: GİB kod listeleriyle (T4.2) birlikte tanımlanacaklar.
> - Mali müşavire sorulacak üç hesap eşlemesi `USER_TASKS.md` K20'de.

> **Sonuç (2026-11-03):** Upstream `l10n_tr` (20.0) temel yapıyı veriyor. Ek veri seti gerektirmeyen kısımlar:
> - Tekdüzen hesap planı: 347 kayıt, 261 üç haneli hesap;
> - 44 vergi, 8 mali pozisyon, vergi raporu ve damga vergisi raporu;
> - 1.046 vergi dairesi: 81 ilin hepsini kapsıyor, ilsiz kayıt yok, (il, kod) tekrarı yok;
> - VKN/TCKN sağlaması (çekirdekte), MERSİS/ticaret sicil/şube numarası alanları;
> - Türkçe dil ayarları (gg.aa.yyyy, ondalık virgül, hafta başı Pazartesi) ve TRY.
>
> Eksikler 26 maddede toplandı (§4). Çoğu **ad ve çeviri hatası**:
> - 19 hesabın Türkçe adı yok, yaklaşık 25 hesap adında büyük harf ya da yazım hatası var.
> - Yanlış çeviriler: "Sales WH" → "SATIŞ NOKTASI", "Purchases WH" → "SATIN ALIMLAR NE ZAMAN", 7 tevkifat vergi grubu → "ne zaman %-20".
> - 44 verginin 31'i Türkçe ekranda İngilizce kısaltmayla görünüyor ("WH 20% (2/10)").
> - KDV tevkifatına "stopaj" deniyor.
>
> İşlevsel eksikler:
> - TCKN girilen gerçek kişi şirket sayılıyor;
> - tevkifat yalnız %20 KDV için tanımlı;
> - istisna ve gelir vergisi stopajı tanımları eksik;
> - ilçe ve resmî tatil verisi, TCMB kuru yok;
> - vergi raporu beyanname düzeninde değil.
>
> Her eksik bir göreve bağlandı. Çoğu T3.2–T3.4'te, rapor T5.8'de, e-Belge kodları T4.3'te ele alınacak. T1.6'da elle görülen ad hataları T3.2'de **kalıcı teste** dönüşür (§5).

## 1. Soru ve yöntem

Soru: Upstream 20.0 `l10n_tr` modülü Türkiye'deki bir ticaret veya üretim işletmesinin e-Belge dışı ihtiyaçlarının ne kadarını karşılıyor? Eksikler hangi göreve gidiyor?

Yöntem:
- Kaynak kod: `upstream/odoo` commit `afbcf79d` (2026-10-18), `addons/l10n_tr` (sürüm 1.3, LGPL-3) ve çekirdekteki Türkiye'ye özgü kod.
- Ölçüm: yerel `ov_demo` veritabanında (`l10n_tr` kurulu, "TR Company" şirketi) Odoo kabuğuyla, Türkçe (`tr_TR`) bağlamda. Veritabanına yazılan deneme kayıtları geri alındı.
- Çeviri kapsamı: upstream `i18n/tr.po` dosyaları `polib` ile sayıldı (çevrilmiş giriş / toplam giriş; eskimiş girişler hariç).
- Mevzuat karşılaştırması: Tekdüzen hesap planının resmî kaynağı Muhasebe Sistemi Uygulama Genel Tebliği (Sıra No: 1, RG 26.12.1992, 21447 mükerrer). Bu çalışmada tebliğ metninin kendisine ulaşılamadı. İkincil kaynaklarla doğrulanan eksik hesaplar "doğrulandı", diğerleri "doğrulanacak" diye işaretlendi. Vergi oranlarının ve kodlarının güncel mevzuatla tek tek karşılaştırması T3.2 ve T4.3'tedir.

Hukuki görüş değildir (T9.4).

## 2. Upstream `l10n_tr` içeriği

| Bileşen | İçerik (ölçüm) |
|---|---|
| Hesap planı | 347 hesap. Kod uzunluğu: 9 tek haneli sınıf, 57 iki haneli grup, 261 üç haneli hesap, 20 altı haneli alt hesap. 76 hesap pasif: sınıf ve grup başlıkları ile 7/B seçeneğinin 790–799 hesapları. Kasa (100) ve banka (102) hesapları günlükle birlikte açılır (`cash_account_code_prefix`, `bank_account_code_prefix`). |
| Vergiler | 44 vergi, hepsi etkin (§3.2). |
| Vergi grupları | 14 grup: KDV %0, %1, %10, %18, %20, %-20; tevkifat %-4…%-20 (7 grup); damga vergisi. |
| Mali pozisyonlar | 8: Yurt İçi; Tevkifat 2/10, 3/10, 4/10, 5/10, 7/10, 9/10, 10/10. Türkçe adları doğru. |
| Raporlar | "Vergi Raporu" (36 satır), "Damga Vergisi Raporu" (10 satır). |
| Vergi daireleri | `l10n_tr.tax.office` modeli, 1.046 kayıt (576 malmüdürlüğü, 470 vergi dairesi). 81 ilin hepsinde en az bir kayıt var, ilsiz kayıt yok, (il, kod) tekrarı yok. Kodlar 101–81261. İş ortağında ve şirkette "Vergi Dairesi" alanı. |
| Şirket varsayılanları | Ülke TR, para birimi TRY, satış/alış vergisi %20, gelir 600, alıcılar 120, satıcılar 320, kur farkı 646/656, peşin ödenen gider/ertelenmiş gelir 180/380, gider ve stok hesabı 150, yuvarlama satır bazında. |
| Satış iadesi | Müşteri iade faturalarında ürün veya günlükteki iade hesabı (varsayılan 610) kullanılıyor; tek testi bu. |
| Liste görünümleri | Oturum bilgisine şirketin mali ülke kodu ekleniyor; ülkeye özgü düğmeler için (JS). |

Çekirdekte (`base`, `account`) Türkiye'ye özgü olanlar:

| Konu | Durum (ölçüm) |
|---|---|
| VKN/TCKN | `res.partner.check_vat_tr`: python-stdnum 1.19 `tr.vkn` ya da `tr.tckimlik`. Sağlaması tutmayan numara kayıtta reddediliyor (ölçüldü: `12345`, `9999999999`). Hata iletisi "VKN/TCKN" etiketiyle. |
| Ek kimlikler | `TR_MERSIS`, `TR_TICARET_SICIL`, `TR_SUBE`, `TR_EN` (`odoo/tools/partner_identifiers.py`). Biçim denetimi yok; Türkçe çevirileri boş. |
| Kişi / şirket | `is_company` = "kendi ticari varlığı ve VKN alanı dolu" (`_compute_is_company`). Türkiye'ye özel kural yok. |
| Ülke | Adres biçimi `sokak / sokak 2 / şehir il posta kodu / ülke`; ilçe alanı yok. İl zorunlu değil, posta kodu "zorunlu" (alanın varsayılanı). |
| Dil | `tr_TR`: tarih `%d.%m.%Y`, saat `%H:%M:%S`, ondalık `,`, binlik `.`, gruplama `[3,0]`, hafta başı 1 (Pazartesi). |
| Para birimi | TRY: `₺` tutardan sonra, yuvarlama 0,01, birim "Lira", alt birim "Kuruş". Yazıyla tutar (num2words): `1234,56` → "Binikiyüzotuzdört Lira ve Ellialtı Kuruş". |
| Döviz kuru | Community'de kur sağlayıcı modülü yok. |
| Resmî tatiller | Veri yok: kaynaksız `resource.calendar.leaves` kaydı 0. |

## 3. Bulgular

### 3.1 Hesap planı

- **Türkçe adı olmayan 19 hesap** Türkçe ekranda İngilizce görünüyor: 111, 112, 221, 295, 540, 612, 671, 772; bordro alt hesapları 320100–320500 ve 702000–702500. `account` modülünün açtığı "Profit or Loss Appropriation" hesabı da İngilizce (toplam 20, ölçüldü).
- **Büyük harf hataları:** Türkçe olmayan büyük harf dönüşümü "i" harfini "I" yapmış. Örnekler:
  - 102997 "TAHSIL EDILMEYEN ÖDEMELER", 102998 "TASDIK EDILMEMIŞ ÖDEMELER", 102999 "BANKA GEÇICI MUALLAK HESABI";
  - 224 "KAZANILMAMIŞ FINANSAL KIRALAMA FAIZ GELIRLERI(-)", 301/401 "FINANSAL KIRALAMA İŞLEMLERINDEN BORÇLAR", 302;
  - 336 "DIĞER ÇEŞITLI BORÇLAR", 35/350 "…HAKEDIŞLERİ";
  - 646/656 "KAMBIYO…", 647/657 "REESKONT FAIZ…", 648/658 "ENFLASYON DÜZELTMESI…".
- **Yazım hataları:**
  - 76 ve 760 "PAZARLAMA SATIŞ **YE** DAĞITIM";
  - 247 "DÜŞÜKLÜ**G**Ü", 721 "İŞ**C**İLİK";
  - 397 ve 492 adlarının sonunda dipnot artığı "(1)";
  - "KÂR" yazımı tutarsız (57/570 "KÂRLARI", 645/646/648 "KARLARI").
- **Yanlış çeviriler:**
  - 391004 "Sales WH" → "SATIŞ NOKTASI";
  - 391005 "Purchases WH" → "SATIN ALIMLAR NE ZAMAN" ("WH" sözcüğü "when" diye çevrilmiş);
  - 391 "Vat Calculated" (İngilizce ad büyük/küçük harf hatalı; Türkçesi doğru).
- **Eksik hesaplar:**
  - Doğrulanan: 480 Gelecek Yıllara Ait Gelirler, 481 Gider Tahakkukları, 523 İştirakler Yeniden Değerleme Artışları.
  - T3.2'de doğrulandı (MSUGT Sıra No 12, §6): 17 Yıllara Yaygın İnşaat ve Onarım Maliyetleri grubu ve 170, 178, 179 hesapları; 502/503 sermaye düzeltmesi olumlu/olumsuz farkları. Hepsi T3.2'de eklendi.
- **Varsayılan gider ve stok hesabı 150** (İlk Madde ve Malzeme), maliyet hesapları 710/713 (7/A).
  - Üretim işletmesine uygun.
  - Ticaret işletmesinde beklenen 153 Ticari Mallar / 621 Satılan Ticari Mallar Maliyeti. Bu, paket ön ayarıdır.
- Bordro alt hesapları (3201xx, 7020xx) ana planın içinde; 702 Tekdüzen'de bir ana hesap değil. Bordro P3 (T11.13); dokunulmaz, yalnız adları Türkçeleşir.

### 3.2 Vergiler

| Grup | Vergiler |
|---|---|
| KDV satış | %1, %10, %20; ihracat %0 ("0% EX"); "İhracat Kayıtlı Satış KDV'si" (-%20, `tr_wh_s_20`) |
| KDV alış | %0, %1, %10, %20 |
| KDV tevkifatı (satış ve alış) | %20 KDV için 2/10, 3/10, 4/10, 5/10, 7/10, 9/10, 10/10. Her biri bir grup vergi (KDV + eksi tevkifat) ve aynı oranlı mali pozisyon. |
| Gelir vergisi stopajı | Yalnız alışta kira stopajı %20 ("PR WH 20%") |
| Damga vergisi | Satış ve alışta %0,948, %0,759, %0,189 |

Bulgular:
- **Adlar:** 44 verginin 31'inin Türkçe adı boş, ekranda İngilizce kısaltma görünüyor: "WH 20% (2/10)", "0% EX", "PR WH 20%". Damga vergileri "DV …" olarak çevrilmiş.
  - Tevkifatın çocuk vergisi ile grup vergisi aynı adı taşıyor. 14 ad ikişer kez geçiyor, seçim listesinde ayırt edilemiyor.
- **Vergi grupları:**
  - 7 tevkifat grubunun Türkçe adı "ne zaman %-20" … "ne zaman %-4". "WH" kısaltması "when" diye makine çevirisinden geçmiş.
  - "KDV %18" grubu artık kullanılmıyor (oran 2023'te değişti; vergisi yok).
- **Terim:** KDV tevkifatı açıklamalarda "Stopajlı Satış KDV'si", vergi raporunda "Satış Stopajı", "Alımlarda Stopaj" olarak geçiyor.
  - Stopaj gelir vergisi kesintisidir; KDV'de doğru terim tevkifattır.
  - Ayrıca "Stopajlı KDV %20 (Mutlak 4/10)", "%0 satın al" gibi bozuk açıklamalar ve "Tevkif" / "Tevkifat" tutarsızlığı var.
- **Kapsam:**
  - Tevkifatlı vergiler yalnız %20 KDV için. %10 ve %1 oranlı bir işlem tevkifata tabiyse tanım yok.
  - Tevkifat oranları ve işlem türleri (e-Belge'de 6xx kodları) güncel tebliğe göre T4.3'te doğrulanacak (T3.2'den taşındı: oranlar kodlarla birlikte tanımlanır). Kaynak: GİB UBL-TR kod listeleri, T4.2'de indirilir.
- **İstisnalar:** Yalnız ihracat (%0) ve ihraç kaydıyla satış var. İstisna nedenleri ve kodları yok; e-Belge'de satır bazında istenir.
  - "İhraç kayıtlı satış" vergisinin -%20 bir satış vergisi olarak kurgulanması e-Belge'nin IHRACKAYITLI tipiyle birlikte T4.3'te incelenir (T3.2'de yalnız adı düzeltildi).
- **Diğer vergiler:** Serbest meslek vb. gelir vergisi stopajları, ÖTV, ÖİV ve konaklama vergisi yok. Stopajlar ticaret ve üretim paketinde de görülür; diğerleri sektörel, MVP dışı.
- Damga vergisi oranlarının güncelliği T3.2'de doğrulandı: değişmedi (§3.6).

### 3.3 Raporlar

- "Vergi Raporu": satış ve alış KDV'si oran bazında, tevkifat 2/10–10/10, net KDV, ödenecek KDV.
  - Beyanname (KDV-1, KDV-2) düzeninde değil.
  - Tevkifat satırlarında "stopaj" terimi; "KDV Ödenmesi", "Toplanan Toplam Satış Vergisi" gibi çeviri kokan başlıklar.
- "Damga Vergisi Raporu": başlıklar "Satış Vergisi" / "Alım Vergisi", yani damga vergisi yerine genel "vergi".
- Vergi raporunun beyanname düzenine yaklaştırılması zaten T5.8'in kapsamında.

### 3.4 Kişiler, adres, kimlik

- **Kişi/şirket ayrımı (ölçüldü):** Geçerli bir TCKN girilen "Ayşe Örnek" `is_company = True` oldu.
  - e-Belge'de alıcı türü (kişi / kurum), adın biçimi ve e-Arşiv ayrımı buna bağlı.
  - 19.0 Nilvera modülleri bu ayrımı yapıyordu (`docs/research/nilvera-port.md` §5.2, madde 18).
  - T3.3'te kapandı: TCKN'li iş ortağı `is_company = False` (`ov_demo`'da ölçüldü).
- **VKN/TCKN sağlaması:** Çekirdekte var ve çalışıyor (§2). Eksikler:
  - Biçim yer tutucusu "11111111111 (NIN) or 2222222222 (VKN)": İngilizce kısaltma, Türkçesi yok.
  - Ülkenin `vat_label` alanı boş.
- **MERSİS / ticaret sicil / şube no:** Alanlar var, biçim denetimi yok. MERSİS 16 hanedir. Etiketlerin Türkçesi boş.
  - T3.3'te kapandı: MERSİS'te 16 hane denetleniyor; etiketler Türkçe ("MERSİS No", "Ticaret Sicil No", "Şube No"). Yer tutucu ve ülke etiketi de Türkçe.
- **Vergi dairesi:** Veri tam (§2). Ek veri seti gerekmiyor; PLAN §4'teki "T3.1'de doğrulanır" notu kapanır.
- **Adres:**
  - İlçe alanı ve verisi yok.
  - İl zorunlu değil.
  - Posta kodu zorunlu (çekirdek varsayılanı; Türkiye için ayarlanmamış).
  - e-Belge'de il (CityName) ve ilçe (CitySubdivisionName) beklenir.

### 3.5 Dil, para birimi, belgeler

- Tarih, sayı biçimi ve hafta başı upstream'de doğru. PLAN T3.2'deki "tarih biçimi, hafta başı Pazartesi" maddesi gereksiz. Saat dilimi T3.2'de denetlendi (aşağıda); TRY hesap planıyla şirket para birimi oluyor.
- Yazıyla tutar "Binikiyüzotuzdört Lira ve Ellialtı Kuruş" çıkıyor. Türk belgelerinde "Türk Lirası" ve "Yalnız" öneki beklenir (T3.7).
- **Çeviri kapsamı** (upstream `tr.po`, çevrilmiş / toplam):

  | Modül | Kapsam |
  |---|---|
  | `l10n_tr` | 7/21 (%33,3) |
  | `base` | 3065/3555 (%86,2) |
  | `account` | 2926/3392 (%86,3; 45 belirsiz) |
  | `sale` | 676/903 (%74,9; 42 belirsiz) |
  | `purchase` | 551/656 (%84,0) |
  | `stock` | 1616/1919 (%84,2; 15 belirsiz) |
  | `mrp` | 958/1167 (%82,1) |
  | `mail` | 1784/2519 (%70,8) |
  | `web` | 4250/5178 (%82,1) |
  | `contacts` | 16/22 (%72,7) |

  Hesap ve vergi adları `.po`'da değil, hesap planı CSV'lerindeki `@tr` sütunlarındadır. Bu yüzden §3.1–3.2'deki eksikler çeviri aracıyla değil T3.2'deki veri düzeltmesiyle kapanır.
- **Saat dilimi (T3.2'de ölçüldü):** `resource` modülü şirketin saat dilimini ülkesinden hesaplıyor; Türkiye tek dilimli olduğu için `Europe/Istanbul` (`ov_demo`'daki iki şirkette ölçüldü). Kullanıcının dilimi tarayıcısından gelir; tarayıcıyla uyuşmazsa web istemcisi uyarır. Ek iş gerekmez (G24).

### 3.6 T3.2'de bulunanlar

Hesap adları (T3.1'deki kurallara takılmayan, THP listesiyle karşılaştırınca görülen):
- 437 ve 438 kaymış: 437'nin Türkçe adı 438'in adı ("KAMUYA OLAN ERTELENMİŞ…"), 438'inki 436'nın adı ("DİĞER ÇEŞİTLİ BORÇLAR"). İngilizce adlar doğru.
- 326 (borç hesabı) "VERİLEN DEPOZİTO VE TEMİNATLAR"; THP'de 326 Alınan Depozito ve Teminatlar. İngilizcesi de "Given".
- 690 ve 692 aynı adı taşıyor ("DÖNEM NET KÂRI (ZARARI)", İngilizcesi de aynı); THP'de 690 Dönem Kârı veya Zararı, 692 Dönem Net Kârı veya Zararı.
- 54 "BİRİKMİŞ KARLAR"; THP'de 54 Kâr Yedekleri.
- 195 "İŞ AVANSLAR" (ek eksik), 152 ve 620 "MAMÜL" (doğrusu "mamul"), 631'de "(-)" eksik.
- 391001–391003 "20% KDV": yüzde işareti Türkçede sayının önünde ("%20").

Hesap ve vergi ayarları (işlevsel):
- **G27 — özel hesaplar plan dışı:** `account` modülü, Türk hesap planı bunları vermediği için erken ödeme indirimi, kasa farkı ve cari yıl kârı/zararı için 999 kodlu beş hesap açıyor ("Cash Discount Loss" vb.). Tekdüzen'de karşılıkları var: 611, 649, 679, 689, 590.
- **G28 — kira stopajı yanlış hesapta:** upstream'in "PR WH 20%" vergisi kesilen gelir vergisini 191 İndirilecek KDV hesabına kaydediyor. Stopaj vergi dairesine ödenecek bir borçtur (360). Vergi ayrıca KDV tevkifatı grubunda duruyor.
- **G29 — 193 ve 360'a vergi kaydedilemiyor:** iki hesap alacak/borç (cari) hesabı türünde. 20.0, alış belgesinde borç hesabına vadesiz satır yazılmasını reddediyor ("must have a due date"); bu yüzden 360'a kaydeden bir stopaj vergisi fatura onayında hata veriyordu (ölçüldü, T3.2 testi). İkisi de cari hesap değil, vergi hesabıdır.

Mevzuat doğrulaması:
- Damga vergisi oranları (binde 9,48, 7,59 ve 1,89) 2026'da değişmedi; yalnız maktu tutarlar ve üst sınır her yıl güncelleniyor (§6). Oranlar doğru (G13).
- Gelir vergisi stopajı: kira (GVK 94/5-a) ve serbest meslek ödemeleri (GVK 94/2-b) için %20 (§6).
- Alışta tevkif edilen KDV upstream'de 391005'e, satıştaki damga vergisi 391006'ya (391 altında), alıştaki damga vergisi 770'e kaydediliyor. Uygulamada tevkif edilen KDV genellikle 360'ta izlenir. Bunlar muhasebe tercihi; mali müşavire sorulacak (`USER_TASKS.md` K20), değiştirilmedi.

## 4. Eksik listesi ve hedef görevler

| # | Eksik | Etki | Hedef |
|---|---|---|---|
| G1 | 20 hesabın Türkçe adı yok | Türkçe ekranda İngilizce hesap | T3.2 — kapandı |
| G2 | ~25 hesap adında büyük harf ve yazım hatası ("TAHSIL EDILMEYEN", "SATIŞ YE DAĞITIM", "(1)") | Görünüm, güven | T3.2 + kalıcı test — kapandı |
| G3 | 391004/391005 yanlış çeviri ("SATIŞ NOKTASI", "SATIN ALIMLAR NE ZAMAN") | Yanlış hesap anlamı | T3.2 — kapandı |
| G4 | Eksik THP hesapları: 480, 481, 523; 17 grubu ve 170, 178, 179; 502/503 (hepsi doğrulandı) | Uzun vadeli tahakkuk ve sermaye hesapları elle açılıyor | T3.2 — kapandı |
| G5 | Varsayılan gider/stok hesabı 150; ticaret için 153/621 | Ticari mal alımları yanlış hesaba | T7.1 (ticaret paketi), T6.2/T6.3 (üretim, 7/A) |
| G6 | 31 verginin Türkçe adı yok; tevkifat çocuk ve grup vergileri aynı adlı | Vergi seçimi karışıyor | T3.2 — kapandı |
| G7 | 7 tevkifat grubunun adı "ne zaman %-…"; kullanılmayan "KDV %18" grubu | Fatura toplamlarında yanlış başlık | T3.2 — kapandı. "KDV %18" grubu kalır: vergi grubu pasif yapılamıyor, vergisi olmadığı için seçimde görünmüyor |
| G8 | KDV tevkifatına "stopaj" deniyor; bozuk açıklamalar ("Mutlak 4/10", "%0 satın al") | Yanlış terim | T3.2 (vergiler) — kapandı; T5.8 (rapor) |
| G9 | Tevkifat yalnız %20 KDV için; oran ve işlem türü listesi doğrulanmamış | %10/%1 oranlı tevkifatlı işlem kesilemiyor | T4.3: oranlar ve 6xx kodları birlikte (T3.2'den taşındı) |
| G10 | İstisna tanımları ve nedenleri yok (ihracat dışında) | İstisnalı satış doğru vergilenemiyor | T4.3: vergiler ve 3xx kodları birlikte (T3.2'den taşındı) |
| G11 | Gelir vergisi stopajı yalnız kira | Serbest meslek alımları elle | T3.2 — kapandı (kira ve serbest meslek %20) |
| G12 | ÖTV, ÖİV, konaklama vergisi yok | Sektörel | MVP dışı; pilot ihtiyacında yeni görev |
| G13 | Damga vergisi oranlarının güncelliği doğrulanmadı | — | T3.2 — doğrulandı, değişiklik yok |
| G14 | Vergi raporu beyanname düzeninde değil, "stopaj" terimi | Beyanname hazırlığı elle | T5.8 |
| G15 | Damga vergisi raporu başlıkları ("Satış Vergisi") | Görünüm | T5.8 |
| G16 | TCKN girilen gerçek kişi şirket sayılıyor (ölçüldü) | e-Belge alıcı türü, ad biçimi | T3.3 — kapandı |
| G17 | VKN/TCKN yer tutucusu İngilizce ("NIN"); ülkenin VKN etiketi boş | Görünüm | T3.3 — kapandı |
| G18 | MERSİS biçim denetimi yok; MERSİS/ticaret sicil/şube etiketleri çevrilmemiş | Hatalı MERSİS belgeye gider | T3.3 — kapandı (denetim ve çeviri) |
| G19 | Adreste ilçe yok, il zorunlu değil, posta kodu zorunlu | e-Belge adres alanları | T3.4 |
| G20 | TCMB kuru yok | Dövizli işlem elle | T3.5 |
| G21 | Çeviri kapsamı: `l10n_tr` %33, paket modülleri %71–86 | Türkçe arayüzde İngilizce metin | T3.6 |
| G22 | Yazıyla tutar "Lira", "Yalnız" öneki yok | Belge alışkanlığı | T3.7 |
| G23 | Resmî tatil verisi yok | İş merkezi ve izin takvimi | T3.8 |
| G24 | Saat dilimi varsayılanı (kullanıcıda tarayıcıdan) | Zamanlanmış işler ve belge saatleri | T3.2 — gerekmiyor: şirket dilimi ülkeden `Europe/Istanbul` (§3.5) |
| G25 | `l10n_tr`'de tek test (satış iadesi) | Yerelleştirme hataları fark edilmiyor | T3.2–T3.4 testleri, T3.9 (T3.2: 9, T3.3: 10 test) |
| G26 | Vergi daireleri: güncellik (kapanan/birleşen daireler) yalnız upstream'le gelir | e-Belge'de eski daire adı | T4.3 (e-Belge testleri); şimdilik ek veri yok |
| G27 | Erken ödeme indirimi, kasa farkı ve cari yıl kârı için plan dışı 999 kodlu hesaplar (§3.6) | Tekdüzen dışı hesaplar, mizanda yabancı kalem | T3.2 — kapandı (611, 649, 679, 689, 590) |
| G28 | Kira stopajı 191 İndirilecek KDV'ye kaydediliyor (§3.6) | Ödenecek vergi, indirilecek KDV görünüyor | T3.2 — kapandı (360'a kaydeden yeni vergiler; eskisi pasif) |
| G29 | 193 ve 360 alacak/borç hesabı türünde; vergi kaydedilemiyor (§3.6) | 360'a kaydeden vergi fatura onayında hata | T3.2 — kapandı (kayıtsız hesaplarda tür değişir) |

## 5. T3.2 için uygulama notları

- Upstream'e dokunulmaz (D-010). Düzeltmeler `ov_l10n_tr` içinde, `@template('tr', <model>)` uzantılarıyla yalnız değişen alanları yazar.
  - Örnek: hesap `name@tr`, vergi `name`/`name@tr`/`description@tr`, vergi grubu `name@tr`.
  - Kurulu şirketlerde hesap planı verisi yeniden yüklenerek güncellenir; adı kullanıcı tarafından değiştirilmiş kayıtların korunması denenir.
- Lisans: hesap adları resmî tebliğden (kamu metni), düzeltmeler bizim yazdığımız veri; modül AGPL-3 kalır. Upstream CSV'sinden toplu kopya yapılırsa LGPL-3 olur (D-008).
- **Kalıcı test** (kullanıcı tercihi: elle görülen hata ölçülebilir teste döner). Türkçe bağlamda bütün hesap, vergi, vergi grubu ve mali pozisyon adları için:
  - İngilizce ad kalmamalı (Türkçe ad İngilizceyle aynı ve harf içeriyorsa hata);
  - "WH", "EX", "PR" gibi İngilizce kısaltma olmamalı;
  - yasak sözcük listesi: "ne zaman", "NOKTASI" (391xxx'te), "Stopaj" (KDV tevkifatında);
  - Türkçe büyük harf denetimi: büyük harfli adlarda, ince ünlüden (E, İ, Ö, Ü) sonra gelen "I" harfi hata sayılır (Türkçe ek uyumu). Kök sözcüklerdeki hatalar ("TAHSIL", "FAIZ") için bir düzeltme sözlüğü kullanılır.
  - Eşik: T1.6'da görülen örneklerin (`TAHSIL EDILMEYEN ÖDEMELER`, `Private Sector Bonds, Shares And Notes`, `WH 20% (2/10)`) hepsi bu testte yakalanmalı.
- Satış iadesi hesabı (610) ve mevcut mali pozisyonlar doğru çalışıyor; korunur.

## 6. Kaynaklar

- Odoo 20.0 Community kaynak kodu, commit `afbcf79d` (2026-10-18):
  - `addons/l10n_tr/**`;
  - `odoo/addons/base/models/res_partner.py` (`check_vat_tr`, `_compute_is_company`, `_run_vat_checks`);
  - `odoo/tools/partner_identifiers.py`;
  - `odoo/addons/base/data/res.lang.csv`, `res_country_data.xml`, `res.country.state.csv`.
- python-stdnum 1.19: `stdnum.tr.vkn`, `stdnum.tr.tckimlik`.
- MERSİS numarası (16 hane; iç yapı yalnız ikincil kaynaklarda; T3.3):
  - Ticaret Bakanlığı, ticaret sicili sık sorulan sorular: https://ticaret.gov.tr/ic-ticaret/sikca-sorulan-sorular/ticaret-sicili
  - https://www.halkbank.com.tr/tr/blog/mersis-no-nedir
  - https://www.parasut.com/blog/mersis-numarasi-nedir
- Muhasebe Sistemi Uygulama Genel Tebliği (Sıra No: 1), Resmî Gazete 26.12.1992, 21447 mükerrer (Tekdüzen hesap planı). Tebliğin kendisine ulaşılamadı; atıf ikincil kaynaktan: https://www.alomaliye.com/2015/08/30/tek-duzen-hesap-plani/
- Tekdüzen hesap planı listesi (ikincil, 480/481/523 doğrulaması): https://www.muhasebetr.com/tekduzenhesapplani
- Muhasebe Sistemi Uygulama Genel Tebliği Sıra No 12 (enflasyon düzeltmesi hesapları: 178, 358, 502/503, 697; T3.2): https://www.alomaliye.com/2004/05/05/muhasebe-sistemi-uygulama-genel-tebligi-sira-no12/
- Damga vergisi 2026 oran ve tutarları (ikincil, T3.2): https://faturaport.com/blog/vergi/2026-yili-damga-vergisi-oran-ve-tutarlari-nelerdir
- Gelir vergisi stopaj oranları 2026, GVK 94 (ikincil, T3.2): https://musavirlerkulubu.com.tr/makale/stopaj-uygulamalari-rehberi-2026-vergi-kesintisi-oranlar-ve-beyanname-sureci
- e-Belge kod listeleri (tevkifat 6xx, istisna 3xx): GİB UBL-TR kod listeleri kılavuzu. İndirme ve sürüm sabitleme T4.2'de (`docs/research/e-fatura.md` §6).
- Ölçüm betikleri bu araştırma için geçici yazıldı; kalıcı denetim T3.2 testine taşındı (`addons/ov_l10n_tr/tests/turkish_names.py`, `test_turkish_chart.py`).
