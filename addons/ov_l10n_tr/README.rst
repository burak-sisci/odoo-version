=============================
Türkiye Muhasebe Düzeltmeleri
=============================

Türk hesap planı (Tekdüzen Hesap Planı) ve vergi tanımlarındaki ad, hesap ve vergi
hatalarını düzeltir. Türkiye muhasebe paketiyle birlikte kendiliğinden kurulur.

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

Mevcut şirketler
================

Modül kurulduğunda Türk hesap planını kullanan şirketler de güncellenir: yeni
hesaplar ve vergiler eklenir, adlar düzeltilir. Kullanıcının değiştirdiği bir ad
korunur; yalnız hâlâ eski haliyle duran ya da hiç Türkçesi olmayan adlar
değişir.
