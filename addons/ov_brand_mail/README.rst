===============
E-posta Markası
===============

E-postalardan ve sohbet ekranlarından yayıncının adını kaldırır, yayıncıya haftada bir
gönderilen veritabanı raporunu kapatır.

Neleri değiştirir
=================

* Bildirim e-postalarının altındaki "Powered by" satırı ve yayıncının bağlantısı
  kaldırılır; takibi bırakma bağlantısı kalır.
* E-posta şablonlarındaki yayıncı logosu (ör. e-fatura bildirimleri) gönderilen
  e-postadan çıkarılır.
* Otomatik mesajların yazarı ve sohbet botu ürünün adını, simgesini ve örnek bir
  e-posta adresini taşır. Ürün adı değişince bu ad da değişir.
* Bağlantıyla paylaşılan sohbet kanalının sayfa başlığı ve simgesi.
* E-posta şablonlarının konu ve gövdelerinde geçen eski ürün adı, gönderilen
  e-postada ve e-posta yazma penceresinde ürünün adıyla değiştirilir. Şablonların
  kayıtlı metni değişmez.
* Güvenlik uyarısı e-postasındaki iki adımlı doğrulama bağlantısı (yayıncının belge
  sitesi) kaldırılır; cümle kalır.
* Yazarı olmayan mesajların tarayıcı bildirimleri ürünün simgesini taşır.

Yayıncıya giden rapor
=====================

Bu rapor veritabanı kimliğini, kullanıcı sayılarını, kurulu uygulamaları ve şirketin
adını, e-posta adresini ve telefonunu içerir. Modül kurulduğunda rapor hiç gönderilmez
ve raporu hazırlayan zamanlanmış iş pasif olur.

Gmail ve Outlook hesapları
==========================

Gmail ve Outlook hesapları, Ayarlar'a girilen kendi istemci kimliğiniz ve gizli
anahtarınızla bağlanır. Bu bilgiler hesap bağlandıktan sonra silinirse oturum
anahtarı yayıncının aracı sunucusundan istenmez (istense oturum yenileme anahtarı
oraya gönderilirdi). Bunun yerine bilgilerin yeniden girilmesini isteyen bir hata
gösterilir.

E-posta modülü kurulu olan her veritabanına kendiliğinden kurulur.
