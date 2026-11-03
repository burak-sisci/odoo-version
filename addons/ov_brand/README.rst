=====
Marka
=====

Web istemcisinde kullanıcının gördüğü ürün adını, simgeleri ve rengi ürünün kendi
markasıyla değiştirir. Varsayılan ürün adı **Nexus**.

Neleri değiştirir
=================

* Web istemcisinin adresi ``/app``. Altyapının eski adresleri, e-postalardaki
  bağlantılar da dahil, oraya yönlendirilir.
* Tarayıcı sekmesinin başlığı ve simgesi.
* PDF belgelerinin başlığı; sunucunun yazdığı PDF dosyalarında üretici adı.
* Giriş ekranının altbilgisi ve paylaşılan bağlantıların önizlemesi.
* Tarayıcıdan kurulan uygulamanın adı, rengi ve simgeleri; çevrimdışı sayfası.
* Gezinme çubuğunun ve ana düğmelerin rengi.
* Pencere ve hata başlıkları, oturum süresi doldu bildirimi.
* Ayarlar ekranındaki "Hakkında" bölümü: ürün adı ve sürüm. Altyapının telif ve
  lisans satırı korunur, yanına ürünün GNU AGPL lisans bağlantısı eklenir.
* Kullanıcı menüsündeki "Yardım" öğesi destek adresini açar; adres girilmemişse
  öğe gizlenir.
* Ücretli sürümün uygulamaları Uygulamalar ekranında listelenmez, Ayarlar'daki
  ücretli sürüm özellikleri gizlenir (OCA'nın bu iş için yazdığı modülle).
* Ayarlar ekranındaki "?" bağlantıları yayıncının belge sitesine gidiyorsa
  gösterilmez.
* Uygulamalar ekranı yayıncının uygulama mağazasına bağlanmaz: "Sektörler"
  süzgeci, "Tema Mağazası" ve "Üçüncü Taraf Uygulamaları" menüleri gizlenir.
* Erişim hakları formundaki yayıncı belge sitesi bağlantısı gösterilmez.

Metinlerdeki ürün adı
=====================

Altyapının metinlerinde geçen eski ürün adı, kullanıcıya gösterilirken ürünün
adıyla değiştirilir: menüler ve eylemler, alan adları ve yardım metinleri, seçim
listeleri, hata ve bilgi mesajları, ekranlar, raporlar, sayfalar, gruplar ve
modül adları. İngilizce ve Türkçe dahil bütün diller için geçerlidir.

* Türkçe ekler ürün adına uydurulur (ör. "...'ta", "...'un", "...'a").
* Yayıncının şirket adı, ücretli sürümü, sürüm numaraları ve diğer ürünlerinin
  adları değiştirilmez.
* Örnek adreslerde yayıncının alan adı yerine ``example.com`` yazılır.
* Kayıtlı metinler değişmez; değişiklik yalnız gösterimdedir. Kullanıcıların
  girdiği veriler değiştirilmez.

Bir sızıntı testi, kurulu bütün modüllerde kullanıcıya görünen metinleri İngilizce
ve Türkçe olarak tarar; izin verilen istisnalar gerekçeleriyle testin yanında
listelenir.

Ayarlar
=======

Sistem parametreleri (geliştirici modunda Ayarlar > Teknik > Sistem Parametreleri):

``ov_brand.name``
    Ürün adı. Boşsa varsayılan ad kullanılır.

``ov_brand.support_url``
    "Yardım" öğesinin açacağı adres. Boşsa öğe gizlenir.

Genel Ayarlar'da bir uygulama adı girilmişse tarayıcıdan kurulan uygulama o adı
kullanır.

Kaldırılan çevrim içi hizmetler
===============================

Yayıncının çevrim içi hizmetleri (uygulama içi satın alma kredileri ve abonelik
sayfası) her yeni veritabanına kendiliğinden kurulur. Bu modül onları, onlara
bağlı modüllerle birlikte kaldırır:

* SMS gönderimi,
* iş ortağı otomatik tamamlama,
* aday zenginleştirme ve aday üretme,
* posta ile gönderim,
* "Aboneliğim" sayfası.

Bu modüller Uygulamalar ekranından kurulamaz; Ayarlar ekranındaki kutuları
gösterilmez. Komut satırından kurulsalar da kurulumun sonunda yeniden kaldırılır.

Bilinen sınırlar
================

* Veritabanı yöneticisi veritabanı olmadan çalışır ve bu modülü görmez. Üretimde
  kapalı tutulur (``list_db = False``).
* E-posta, rapor ve portal altbilgileri ayrı modüllerde ele alınır.
* Ürün adı değiştirildiğinde ekranlar hemen güncellenir. Sunucu birden çok süreçle
  çalışıyorsa sunucu tarafı mesajlar her süreçte ilk sayfa yüklemesiyle güncellenir.
* SMS gönderimi için yerli bir sağlayıcıyla ayrı bir modül gerekir.
