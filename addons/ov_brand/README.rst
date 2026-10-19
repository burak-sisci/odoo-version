=====
Marka
=====

Web istemcisinde kullanıcının gördüğü ürün adını, simgeleri ve rengi ürünün kendi
markasıyla değiştirir. Varsayılan ürün adı **Nexus**.

Neleri değiştirir
=================

* Tarayıcı sekmesinin başlığı ve simgesi.
* Giriş ekranının altbilgisi ve paylaşılan bağlantıların önizlemesi.
* Tarayıcıdan kurulan uygulamanın adı, rengi ve simgeleri; çevrimdışı sayfası.
* Gezinme çubuğunun ve ana düğmelerin rengi.
* Pencere ve hata başlıkları, oturum süresi doldu bildirimi.
* Ayarlar ekranındaki "Hakkında" bölümü: ürün adı ve sürüm. Altyapının telif ve
  lisans satırı korunur, yanına ürünün GNU AGPL lisans bağlantısı eklenir.
* Kullanıcı menüsündeki "Yardım" öğesi destek adresini açar; adres girilmemişse
  öğe gizlenir.

Ayarlar
=======

Sistem parametreleri (geliştirici modunda Ayarlar > Teknik > Sistem Parametreleri):

``ov_brand.name``
    Ürün adı. Boşsa varsayılan ad kullanılır.

``ov_brand.support_url``
    "Yardım" öğesinin açacağı adres. Boşsa öğe gizlenir.

Genel Ayarlar'da bir uygulama adı girilmişse tarayıcıdan kurulan uygulama o adı
kullanır.

Bilinen sınırlar
================

* Veritabanı yöneticisi veritabanı olmadan çalışır ve bu modülü görmez. Üretimde
  kapalı tutulur (``list_db = False``).
* E-posta, rapor ve portal altbilgileri ayrı modüllerde ele alınır.
