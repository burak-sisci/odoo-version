=======================
Türkiye Yerelleştirmesi
=======================

Türk hesap planı (Tekdüzen Hesap Planı) ve vergi tanımlarındaki ad, hesap ve vergi
hatalarını düzeltir; VKN/TCKN ve MERSİS numaralarını Türkiye kurallarıyla işler.
Adreslerde il ve ilçe listeden seçilir. Fatura ve makbuzlar Türk belge
düzeninde basılır. Türkiye muhasebe paketiyle birlikte kendiliğinden kurulur.

Hesap planı
===========

* Türkçe adı olmayan hesaplar (menkul kıymetler, yasal yedekler, bordro alt
  hesapları ve diğerleri) Türkçe ad alır.
* Büyük harf ve yazım hataları düzeltilir: "TAHSİL EDİLMEYEN", "KAMBİYO KÂRLARI",
  "PAZARLAMA SATIŞ VE DAĞITIM" gibi.
* Yanlış çevrilmiş ya da karışmış adlar düzeltilir: 326 Alınan Depozito ve
  Teminatlar, 437 Diğer Borç Senetleri Reeskontu, 438 Kamuya Olan Ertelenmiş veya
  Taksitlendirilmiş Borçlar, 690 Dönem Kârı veya Zararı, 391 alt hesapları.
* Eksik hesaplar eklenir: 170, 178, 179 (yıllara yaygın inşaat), 480, 481
  (gelecek yıllara ait gelirler, gider tahakkukları), 502, 503 (sermaye düzeltmesi
  farkları), 523 (iştirakler yeniden değerleme artışları).
* 193 Peşin Ödenen Vergiler ve Fonlar ile 360 Ödenecek Vergi ve Fonlar alacak/borç
  hesabı türünden çıkarılır. Bu türdeki bir hesaba fatura üzerinden vergi
  kaydedilemiyordu. Hesapta kayıt varsa türü değiştirilmez.

Şirket ayarları
===============

Yeni kurulan şirkette aşağıdaki hesaplar plan dışı 999 kodlu hesaplar yerine
Tekdüzen hesaplarına bağlanır:

* erken ödeme indirimi: verilen 611 Satış İskontoları, alınan 649 Diğer Olağan
  Gelir ve Kârlar;
* kasa farkı: fazla 679 Diğer Olağandışı Gelir ve Kârlar, eksik 689 Diğer
  Olağandışı Gider ve Zararlar;
* cari yıl kârı veya zararı: 590 Dönem Net Kârı.

Daha önce kurulmuş bir şirket kendi 999999 hesabını korur; bu hesap Türkçe ad alır.

Vergiler
========

* Vergi ve vergi grubu adları Türkçe yazılır: "%20", "%20 Tevkifatlı 2/10",
  "Satış Tevkifatı 2/10 (%-4)", "Tevkifat %-4", "DV %0,948" gibi. İngilizce
  kısaltmalar ve makine çevirileri ("ne zaman %-20", "%0 satın al") kalkar.
* KDV tevkifatı açıklamalarında "stopaj" yerine "tevkifat" kullanılır.
* Gelir vergisi stopajı için iki yeni alış vergisi: "Kira Stopajı %-20" ve
  "Serbest Meslek Stopajı %-20". Kesilen tutar 360 Ödenecek Vergi ve Fonlar
  hesabına kaydedilir.
* Eski kira stopajı vergisi kesintiyi 191 İndirilecek KDV hesabına kaydediyordu.
  Pasif yapılır; geçmiş kayıtlar değişmez.

Kimlik numaraları
=================

* TCKN (11 hane) girilen kişi gerçek kişi sayılır, şirket sayılmaz. Şahıs
  işletmeleri de TCKN ile vergilendirildiği için gerçek kişidir. VKN (10 hane)
  girilen kayıt şirkettir.
* Vergi numarası alanının adı "VKN/TCKN"; örnek metni "2222222222 (VKN) veya
  11111111111 (TCKN)".
* Hatalı numarada ileti Türkçedir ve VKN'nin 10, TCKN'nin 11 hane olduğunu
  söyler.
* MERSİS numarası 16 hane olmalıdır; boşluk ve tire girilebilir, kayıtta
  yalnız rakamlar kalır.
* MERSİS No, Ticaret Sicil No ve Şube No alanları Türkçe adlarıyla görünür.

Adres
=====

* 81 ilin 973 ilçesi yüklüdür: İçişleri Bakanlığı Mülki İdare Bölümleri
  Envanteri'ndeki 922 ilçe ile büyükşehir olmayan 51 ilin merkez ilçesi
  ("Merkez").
* Kişi formunda ilçe seçilince il ve şehir alanı kendiliğinden dolar. İl
  seçiliyse ilçe listesi o ilin ilçeleriyle sınırlıdır: Ereğli yazınca Konya'da
  Konya'nın, Zonguldak'ta Zonguldak'ın Ereğli'si gelir.
* Müşteri portalında ve e-ticaret adres formunda da ilçe, seçilen ilin
  listesinden seçilir.
* İl zorunlu, posta kodu isteğe bağlıdır.
* Adres Türkiye düzeninde yazılır: "34710 Kadıköy/İstanbul". İlçe ya da il boşsa
  tek başına eğik çizgi kalmaz.

Belgeler
========

Türk şirketinin bastığı belgelerde:

* Şirket bilgilerinde vergi numarasının adı türüne göre "VKN" ya da "TCKN"
  yazılır; MERSİS No, Ticaret Sicil No ve web sitesi de basılır (Türk Ticaret
  Kanunu md. 39). Numaralar şirketin kişi kaydındaki kimlik numaraları
  bölümünden gelir.
* Faturada müşterinin numarası "VKN: …" ya da "TCKN: …" diye yazılır.
* Tutar yazıyla yazılır: "Yalnız: Binikiyüzotuzdört Türk Lirası Ellialtı
  Kuruş". Sayılar bitişik yazılır, baş harf Türkçe kurala uyar ("İkibin").
  Türk hesap planıyla kurulan şirkette faturada kendiliğinden açıktır.
* Ödeme makbuzu gelen ödemede "Tahsilat Makbuzu", giden ödemede "Tediye
  Makbuzu" adını alır ve tutarı yazıyla da gösterir.

Satış belgeleri (teklif, sipariş, proforma) ve sevk irsaliyesi için ayrı
modüller vardır; satış ve stok uygulamalarıyla birlikte kendiliğinden kurulurlar.

Mevcut şirketler
================

Modül kurulduğunda Türk hesap planını kullanan şirketler de güncellenir: yeni
hesaplar ve vergiler eklenir, adlar düzeltilir, faturada tutarın yazıyla
yazılması açılır. Daha önce TCKN'yle kaydedilmiş
kişiler de gerçek kişi olur. Şehir alanına ilçe adı yazılmış Türk kişiler, ad
tek bir ilçeyi gösteriyorsa o ilçeye bağlanır: il seçiliyse o ilin ilçesi, il
adının kendisi yazılmışsa o ilin merkez ilçesi, il seçili değilse yalnız tek
ilde bulunan bir ilçe adı. Belirsiz kayıtlar olduğu gibi kalır. Kullanıcının
değiştirdiği bir ad
korunur; yalnız hâlâ eski haliyle duran ya da hiç Türkçesi olmayan adlar
değişir.
