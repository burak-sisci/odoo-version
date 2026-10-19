# Marka İzleri Envanteri (Odoo 20.0 Community)

Son güncelleme: 2026-10-19
Araştırma tarihi: 2026-10-18
İlgili kararlar: D-006, D-007, D-010, D-014 (DECISIONS.md)
İlgili görev: T2.1 (PLAN.md); sonuçları kullanan görevler T2.2–T2.7

> **Sonuç (2026-10-18):**
> - Kullanıcıya görünen Odoo izleri dört grupta toplanıyor:
>   - web istemcisi kabuğu: başlık, favicon, giriş ekranı, PWA, hata pencereleri, ayarlar (T2.2);
>   - odoo.com'a giden çağrılar ve Enterprise reklamları (T2.3);
>   - e-posta, PDF rapor ve portal altbilgileri (T2.5);
>   - çeviri metinleri ve veritabanı kayıtları (T2.6'nın tarayacağı alan).
> - İncelenen yüzeylerin hepsi modülle değiştirilebiliyor: şablon kalıtımı, JS `patch()`, model veya controller override, veri kaydı. Çekirdeğe dokunmak gerektiren yüzey bulunmadı. `/odoo` URL yolu ayrı görevde (T2.4).
> - MVP modülleriyle kurulan veritabanında 97 modül kurulu. Bunların 40'ında 253 çevrilebilir metin "odoo" içeriyor (§7).
> - Veri gönderen bir zamanlanmış iş varsayılan olarak açık: yayıncı garantisi (`mail.ir_cron_module_update_notification`, haftalık). Veritabanı kimliği, kullanıcı sayıları, kurulu uygulamalar, şirket adı, e-postası ve telefonu `services.odoo.com`'a gidiyor (§4.1). KVKK açısından T2.3'ün ilk işi.
> - Müşteriye giden belgelerde de iz var: faturadaki QR kodun ortasında Odoo logosu, PDF üst verisinde `Creator/Producer: Odoo`, e-posta altbilgisinde "Powered by Odoo" (§6).
> - T2.2 (2026-10-19): §3'teki web istemcisi yüzeyleri `ov_brand` ile değişti. Kalan üç JS metni T2.6'da (§3).
> - T2.3 (2026-10-19, bitti): yayıncı garantisi kapandı; IAP ve `mysubscription` modülleri bağlı modülleriyle kaldırıldı; Enterprise reklamları, dokümantasyon bağlantıları, metin düzenleyicinin hizmetleri ve uygulama mağazası kapandı (§4).
> - Bu belge kontrol tarihindeki upstream commit'ini anlatır (`afbcf79d`). T2.6'daki otomatik test, upstream ilerledikçe yeni izleri yakalamak için var.

## 1. Soru ve kapsam

Soru: Odoo 20.0 Community'de son kullanıcının, yöneticinin veya müşterinin (e-posta, PDF, portal) gördüğü "Odoo" adı, logosu ve odoo.com bağlantıları nerede? Her biri hangi yöntemle ve hangi görevde değiştirilir?

Kapsam:
- MVP paketlerinin modülleri (D-018) ve onların kendiliğinden kurulan (auto_install) bağımlılıkları.
- Web sitesi, POS, IoT gibi MVP dışı modüller yalnız sayımlarda ve "sonra" notlarıyla geçer.
- Clean-room (D-006): yalnız Community kodu ve OCA kodu incelendi. Enterprise koduna, Enterprise deneme örneklerine bakılmadı.

## 2. Yöntem

- **Kaynak kod taraması:** `upstream/odoo` (commit `afbcf79d`).
  - XML şablonları, Python ve JS dosyalarında "Odoo" ve `odoo.com` aramaları; görünüm kimlikleri şablon başına çıkarıldı.
  - Çevrilebilir metinler: 603 modülün `.pot` dosyalarındaki 100.284 `msgid` sayıldı.
- **Deneme veritabanı:** `ov_brand_scan` (tr_TR, TR). Kurulan modüller:
  - `account, l10n_tr, contacts, mail, calendar, sale_management, crm, purchase, stock, mrp, mrp_subcontracting, maintenance, repair, spreadsheet_dashboard`;
  - kendiliğinden kurulanlarla toplam 97 modül.
  - Veritabanında "Odoo" geçen görünüm, e-posta şablonu, ipucu ve iş ortağı kayıtları sayıldı; açık zamanlanmış işler listelendi.
- **HTTP denetimi:** aynı veritabanında yerel sunucu açılıp oturumsuz sayfalar çekildi: `/web/login`, `/web/database/selector`, `/web/database/manager`, `/web/manifest.webmanifest`, `/odoo/offline`.
- **OCA:** `server-brand` deposunun 19.0 ve 20.0 dalları (lisans, bağımlılık, açık port PR'ları).

## 3. Web istemcisi kabuğu (T2.2)

| Yüzey | Görünen | Kaynak | Değiştirme yöntemi |
|---|---|---|---|
| Sekme başlığı (sunucu) | `Odoo` | `web.layout`: `title or 'Odoo'`; `web/controllers/utils.py` varsayılan başlıklar | Şablon kalıtımı; başlık marka ayarından |
| Sekme başlığı (istemci) | `Odoo` | `title_plugin.js` (`defaultTitle`) | JS `patch()` |
| Favicon | Odoo simgesi | `web.layout` → `/web/static/img/favicon.ico`; ayrıca `discuss_public_templates`, veritabanı yöneticisi | Şablon kalıtımı; marka favicon'u için bir rota |
| Giriş ekranı | "Hazırlayan Odoo" (www.odoo.com bağlantısı) | `web.login_layout` → `web.brand_promotion_message` | Şablon kalıtımı |
| Giriş ekranı üst verisi | `og:site_name` = Odoo, `twitter:site` = @Odoo, Odoo sloganı (`og:description`), `og_image.png`; başlık yedeği `Odoo` (`web/controllers/utils.py`) | `web.login` (yalnız `/odoo` yönlendirmeli bağlantı önizlemesinde) | Şablon kalıtımı |
| iOS ana ekran simgesi | `odoo-icon-ios.png` | `web.webclient_bootstrap`, `webmanifest.py` | Şablon kalıtımı, controller override |
| PWA manifesti | ad `Odoo`, renk `#714B67`, `odoo-icon-192/512` | `web/controllers/webmanifest.py` (`/web/manifest.webmanifest`; tek uygulama kurulumu için `scoped_app_manifest`) | Ad zaten ayarlı: `web.web_app_name` parametresi. Renk ve simge için controller override |
| PWA çevrimdışı sayfası | "Odoo logosu", "… Odoo yüklenecektir." | `web.webclient_offline` | Şablon kalıtımı |
| Pencere varsayılan başlığı | `Odoo` | `core/dialog/dialog.js` | JS `patch()` |
| Hata pencereleri | "Odoo Hatası", "Odoo Müşteri Hatası", "Odoo Ağ Hatası", "Odoo Sunucu Hatası", "Odoo Uyarısı" | `core/errors/error_dialogs.js` | JS `patch()` (başlıklar marka adından) |
| Oturum süresi doldu bildirimi | "Odoo Session Expired" | `public/error_notifications.js` | JS `patch()` |
| Diğer istemci mesajları | barkod tarayıcının kamera izni mesajı, güvensiz bağlam uyarısı (yalnız konsolda), rapor işçileri uyarısı | `core/barcode/barcode_video_scanner.js`, `start.js`, `webclient/actions/reports/utils.js` | Metinler yöntem gövdesinde; `patch()` bütün yöntemi kopyalamayı gerektirir. T2.2'de değişmedi, metin düzeyinde değişiklik T2.6'da |
| Kullanıcı menüsü: Destek | `https://www.odoo.com/buy` | `web/models/ir_http.py` → `session.support_url` | `ir.http` oturum bilgisi override: marka destek adresi ya da öğe kaldırılır |
| Kullanıcı menüsü: Aboneliğim | "My Subscription" | `mysubscription` (kendiliğinden kurulur) | T2.3 (§4.3) |
| Ayarlar → "hakkında" | "Odoo 20.0 (Community Edition)", "Copyright © 2004 Odoo S.A. GNU LGPL Licensed" | `settings_form_view/widgets/res_config_edition.xml` | Owl şablon kalıtımı. Başlık marka adı ve sürümü olur. **Telif satırı kalır** (CLAUDE.md kural 2); yanına kendi AGPL notumuz eklenir |
| Ayarlar → PWA adı alanı | yer tutucu `Odoo`, açıklamada "Odoo" | `base_setup` `res_config_settings_view_form` | Görünüm kalıtımı |
| OdooBot | ad "OdooBot", `odoobot.webp` avatarı | `mail/data/res_partner_data.xml` (`base.partner_root`); `mail_bot` | Veri kaydıyla ad ve avatar; bot mesajları `mail_bot` metinlerinde. `mail`'e bağlı olduğu için T2.5'te (`ov_brand_mail`). Sekme başlığında da görülüyor: `mail` kuruluyken açılıştaki Discuss uygulaması başlığa "OdooBot" yazabiliyor (T2.3 testlerinde, 2026-10-19) |
| Veritabanı yöneticisi | başlık `Odoo`, `logo2.png`, "Odoo online services", odoo.com gizlilik bağlantısı | `web/static/src/public/database_manager.qweb.html` | Üretimde `list_db = False` ile kapalı (müşteri görmez). Veritabanı olmadan çalışan rotalar yalnız sunucu genelinde yüklü modülleri (`server_wide_modules`) görür; `ov_brand` buraya ulaşamaz |

Notlar:
- Topbar ve gezinme çubuğu rengi `$o-community-color` (`#71639e`), SCSS değişkeni (`primary_variables.scss`). Marka rengi `ov_brand` asset'inde değişkenle verilir.
- 20.0 Community kullanıcı menüsünde dokümantasyon ve "odoo.com hesabım" öğeleri yok. `auth_oauth` kurulursa `accounts.odoo.com` sağlayıcısı gelir (§4).

## 4. odoo.com'a giden çağrılar (T2.3)

Kurulu sütunu MVP denemesindeki durumu gösterir (§2).

| Hizmet | Adres | Modül | Kurulu | Ne yapar | Yöntem |
|---|---|---|---|---|---|
| Yayıncı garantisi | `services.odoo.com/publisher-warranty/` (`publisher_warranty_url`) | `mail` (`publisher_warranty.contract`) | evet, haftalık iş açık | §4.1 | Model override (çağrı yapılmaz) + iş pasif |
| IAP hesap ve kredi | `iap.odoo.com` (`iap.endpoint`) | `iap`, `iap_mail`, `iap_crm` | evet | Kredi bakiyesi, satın alma bağlantıları | Gizle / devre dışı |
| Aday zenginleştirme | `iap-services.odoo.com` (`enrich.endpoint`) | `crm_iap_enrich` | evet, günlük iş açık | Aday e-posta alan adından şirket bilgisi | İş pasif, ayar gizli |
| Aday üretme | `iap-services.odoo.com` | `crm_iap_mine` | evet | Ücretli aday listesi | Gizle |
| İş ortağı otomatik tamamlama | `partner-autocomplete.odoo.com` | `partner_autocomplete` | evet | Şirket adı/VKN'den adres doldurma | Gizle; Türkiye için yerel kaynak ayrı iş (T3.3) |
| SMS | `sms.api.odoo.com` (`sms.endpoint`) | `sms`, `calendar_sms`, `crm_sms`, `sale_sms`, `stock_sms` | evet | SMS gönderimi IAP kredisiyle | IAP kapanınca SMS çalışmaz. Gizlenir; yerli SMS sağlayıcı ihtiyacı sonra |
| Gmail / Outlook OAuth vekili | `gmail.api.odoo.com`, `outlook.api.odoo.com` | `google_gmail`, `microsoft_outlook` | evet | Kendi OAuth anahtarı yoksa Odoo'nun vekil sunucusu | Vekil kapatılır; yalnız kendi istemci kimliğiyle |
| Düzenleyici görsel kitaplığı ve yapay zekâ metni | `media-api.odoo.com`, `olg.api.odoo.com` | `html_editor` | evet | Simge/çizim kitaplığı, metin üretimi | Gizle. (`web_unsplash` doğrudan `api.unsplash.com`'a gider; odoo.com değil, kendi anahtarıyla çalışır) |
| Aboneliğim | `upgrade.odoo.com`, `odoo.com/pricing`, `accounts.odoo.com/my/home`, `odoo.com/page/editions` | `mysubscription` (20.0'da yeni, `base`+`web` ile kendiliğinden kurulur) | evet | Menü öğesi ve yükseltme sayfası | Kullanıcı menüsü öğesi ve istemci eylemi gizlenir |
| Uygulama mağazası | `apps.odoo.com` | `base`, `base_import_module` | evet | Uygulamalar menüsünden mağaza | Uygulamalar menüsü son kullanıcıdan gizli (T7.3); mağaza bağlantıları T2.3 |
| Enterprise uygulama kartları | — | `base/data/ir_module_module.xml` (20 kayıt, `to_buy`) | evet | Uygulamalar listesinde satın alınacak Enterprise uygulamaları | Uygulamalar eyleminde `to_buy = False` filtresi (öneri). OCA `remove_odoo_enterprise` yalnız ayar ekranlarını kapsıyor |
| Ayarlardaki Enterprise özellikleri ve yükseltme penceresi | `odoo.com/odoo-enterprise/upgrade`, `odoo.com/editions` | `web` (`upgrade_boolean_field`, `upgrade_dialog`), uygulamaların ayar görünümleri | evet | Enterprise özelliğine tıklayınca reklam | OCA `remove_odoo_enterprise` (20.0) |
| Ayarlardaki dokümantasyon bağlantıları | `odoo.com/documentation/…` | `base_setup` ve uygulamaların ayar görünümleri (`documentation=`) | evet | "?" bağlantıları | Kendi belge sitemize (T8.7) yönlendirme ya da gizleme |
| Veritabanı yöneticisi gizlilik notu | `odoo.com/privacy` | `web` | evet | "Some data may be sent to Odoo online services" | §3 |
| VIES, Peppol | `vies.api.odoo.com`, `peppol.api.odoo.com` | `l10n_eu_account_vies`, `account_peppol` | hayır | AB vergi no / Peppol ağı | MVP dışı |
| Snailmail | `iap-snailmail` | `snailmail` | hayır | Posta gönderimi | MVP dışı; kurulursa gizle |
| OAuth girişi | `accounts.odoo.com` | `auth_oauth` | hayır | "odoo.com ile giriş" sağlayıcısı | Kurulursa sağlayıcı pasif |
| Ödeme vekilleri | Stripe, Razorpay, PayU, MercadoPago bağlantı akışları | `payment_*` | hayır | Hesap bağlama | MVP dışı (iyzico T10.4) |
| IoT | `download.odoo.com`, IoT vekili | `iot_drivers` | hayır | Kutu güncellemesi | MVP dışı |

- Sonuç (T2.3, 2026-10-19): IAP hesap ve kredi, aday zenginleştirme, aday üretme, iş ortağı otomatik tamamlama, SMS, Snailmail ve Aboneliğim satırları için tablodaki "gizle" önerileri yerine modüller kaldırıldı (`ov_brand`, USER_TASKS K15 varsayımı). Kurulumun sonunda kaldırılırlar, arayüzden kurulamazlar, Ayarlar'daki kutuları gizli. Diğer satırlar T2.3'te sürüyor.
- Sonuç (T2.3, 2026-10-19): Enterprise uygulama kartları ve ayarlardaki Enterprise özellikleri satırları OCA `remove_odoo_enterprise` ile kapandı (`ov_brand`'in bağımlılığı). OCA'nın 20.0 sürümü `to_buy` uygulamalarını aramadan da çıkarıyor; ayrı filtre gerekmedi.
- Sonuç (T2.3, 2026-10-19), kalan satırlar:
  - Dokümantasyon bağlantıları: gizlendi (`ov_brand`, `DocumentationLink` JS `patch()`). Kendi belge sitemiz hazır olunca ona yönlendirilir (T8.7).
  - Düzenleyici: yeni `ov_brand_html_editor`. Google Translate çevirisi, çizim kitaplığı (`media-api.odoo.com`) ve yapay zekâ metni (`olg.api.odoo.com`) kapalı; sunucu uçları ağa çıkmadan hata döner. Envanterde eksik olan Google Translate eklentisi de (`html_editor`, IAP üzerinden) bu modülde.
  - Uygulama mağazası: `ov_brand` `base_import_module`'ün mağaza çağrılarını (sektör listesi, kategoriler, indirme) boşa çıkarır; "Sektörler" süzgeci, "Tema Mağazası" ve "Üçüncü Taraf Uygulamaları" menüleri gizli.
  - Gmail/Outlook vekili: Community'de zaten kapalı, uç durumu §4.4'te.

### 4.1. Yayıncı garantisi (KVKK)

- `mail/models/update.py`, model `publisher_warranty.contract`. Zamanlanmış iş `mail.ir_cron_module_update_notification`, haftada bir. Ayrıca `l10n_fr_account` ve `l10n_fr_pos_cert` kurulumda çağırıyor.
- Gönderilen alanlar: `dbuuid`, kullanıcı sayıları (toplam, etkin, paylaşımlı, hafif), veritabanı adı ve oluşturulma tarihi, sürüm, dil, `web.base.url`, kurulu uygulamalar, Enterprise kodu; ayrıca şirketin **adı, e-postası, telefonu**.
- Adres yapılandırma dosyasından değişiyor (`publisher_warranty_url`, yalnız dosyada). Varsayılan `http://services.odoo.com/publisher-warranty/`, yani şifresiz HTTP.
- Yanıttaki mesajlar "tüm çalışanlar" kanalına yazılıyor. Yani dış sunucu müşterinin ekranına mesaj gönderebiliyor.
- Öneri (T2.3): `_get_sys_logs` / `update_notification` override ile çağrı hiç yapılmaz; iş pasif. Üretim yapılandırmasında adres ayrıca boş bir yerel adrese yöneltilebilir (iki kat güvence). OCA `disable_odoo_online` aynı işi yapıyor (§9).
- Sonuç (T2.3, 2026-10-19): `ov_brand_mail` `_get_sys_logs`'u ağa çıkmayan boş bir yanıtla değiştirir; iş pasif. `mail` kurulu her veritabanına kendiliğinden kurulur. Yapılandırma dosyasındaki adres değiştirilmedi; üretim yapılandırmasında ikinci güvence olarak T8.4'te ele alınabilir.

### 4.2. Testlerde dış istek

- Odoo test çatısı `standard` etiketli testlerde `requests.Session.send`'i yamalıyor (`odoo/tests/common.py`, `_request_handler`). localhost dışındaki istekler `BlockedRequest` ile düşüyor ve günlüğe "Blocking un-mocked external HTTP request" yazılıyor.
- Kapsamadıkları: test dışı kod yolu (kurulum, zamanlanmış işler), `urllib`/`http.client` ile yapılan istekler, tarayıcı testlerinde (tour) sayfanın kendisinin yaptığı istekler (ör. e-postadaki uzak görsel).
- T2.7 için öneri: günlükteki bu satırları odoo.com alan adlarına göre ayıran bir denetim + tarayıcı testlerinde ağ isteklerinin kaydı.

### 4.3. Aboneliğim (`mysubscription`)

- 20.0'da yeni. `auto_install` ve bağımlılığı yalnız `base` + `web`, yani her veritabanına kuruluyor. Modül bağımlılığıyla engellenemiyor.
- Kullanıcı menüsüne "My Subscription" ekliyor; açılan sayfa odoo.com fiyat, sürüm ve hesap sayfalarına bağlanıyor. Parametre: `mysubscription.database`.
- Öneri (T2.3): `ov_brand` JS'te kullanıcı menüsü kaydından öğeyi kaldırır, istemci eylemi gizlenir.
- Sonuç (T2.3, 2026-10-19): öneri uygulanmadı; modül kaldırıldı (§4 sonucu, K15).

### 4.4. Gmail/Outlook vekili ve `mail`'deki dış istekler

- `google_gmail` ve `microsoft_outlook` kendi istemci kimliği girilmemişse yayıncının vekil sunucusunu kullanır. Vekille ilk bağlantı yalnız Enterprise sürümünde açılır (`release.version_info` denetimi); Community'de bağlanma düğmesi hata verir. Vekil bu yüzden fiilen kapalı.
- Uç durum: kendi istemci kimliğiyle bağlanılıp sonra kimlik ve gizli anahtar Ayarlar'dan silinirse belirteç yenileme vekile (`gmail.api.odoo.com`, `outlook.api.odoo.com`) gider ve yenileme belirtecini gönderir. Yönetici hatası gerektiriyor; kod yazılmadı, T2.7'nin dış istek testinde denetlenir.
- `mail`'deki diğer dış istekler yayıncıya gitmiyor: görüntülü görüşme sunucusu (SFU) ve Twilio ICE sunucuları yalnız kullanıcı ayarlarsa çağrılır; bağlantı önizlemesi mesajdaki adresin kendisine gider.
- Görüntülü görüşmeler varsayılan olarak Google'ın STUN sunucularını kullanır (tarayıcıdan). Veri değil bağlantı bilgisi (IP adresi) gider; KVKK notu COMPLIANCE.md'de.
- Kontrol: 2026-10-19, upstream `afbcf79d`.

## 5. `/odoo` URL yolu (T2.4)

- Web istemcisinin yolları `/odoo`, `/odoo/action-…`, `/odoo/<model>/<id>`.
- PWA manifesti: `scope` ve `start_url` = `/odoo`, paylaşım hedefi `/odoo?share_target=trigger`.
- Çevrimdışı sayfa `/odoo/offline`.
- Yöntem T2.4'te: controller override + JS yönlendirici `patch()`; eski yoldan yönlendirme.

## 6. E-posta, rapor, portal (T2.5)

| Yüzey | Görünen | Kaynak | Yöntem |
|---|---|---|---|
| Bildirim e-postaları | "Powered by Odoo" (www.odoo.com bağlantısı) | `mail.mail_notification_layout`, `mail.mail_notification_light` | Şablon kalıtımı |
| Özet (digest) e-postası | "Sent by Odoo", "Powered by Odoo", "Odoo Mobile" bölümü | `digest.digest_mail_main`, `digest.digest_section_mobile` | Şablon kalıtımı. Mobil bölümdeki görsel `www.odoo.com`'dan yükleniyor (açılışta dış istek) |
| Özet adı ve ipuçları | "Your Odoo Periodic Digest", 12 ipucu kaydı | `digest/data/digest_tips_data.xml` | Veri kaydı override / ipuçları pasif |
| e-Fatura bildirim e-postası | Odoo logosu (`logo_inverse_white_206px.png`) | `account/data/mail_template_data.xml` (`mail_template_einvoice_notification` vb.) | Şablon (veri) override |
| Portal kayıt kenar çubuğu | "Powered by" + Odoo logosu | `portal.portal_record_sidebar` | Şablon kalıtımı |
| Satın alma portalı | "Want to import this document in Odoo?", "Not using Odoo?", "Start on Odoo" (tedarikçiye reklam) | `purchase.portal_my_purchase_order` | Şablon kalıtımı (bölüm kaldırılır) |
| Fatura PDF'i: QR kod | QR kodun ortasında Odoo "O" logosu | `account.report_invoice_document` (`Odoo_logo_O.svg`, iki yer) | Şablon kalıtımı (logo kaldırılır ya da şirket logosu) |
| PDF başlığı | `Odoo Report` | `web.report_layout`, `web.report_preview_layout` | Şablon kalıtımı |
| PDF üst verisi | `/Creator`, `/Producer` = Odoo | `odoo/tools/pdf` (`BrandedFileWriter`, PDF/A yazıcısı) | Çekirdek araç; rapor çıktısını son işlemde yeniden yazmak modülle mümkün, ama PDF/A geçerliliği korunmalı. Düşük öncelik; yöntem T2.5'te |
| Factur-X üst verisi | "Invoice generated by Odoo", Producer Odoo | `account_edi_ubl_cii/data/cii_22_templates.xml` | Şablon kalıtımı; Türkiye faturasında Factur-X kullanılıp kullanılmadığı T4.x'te bakılır |
| Şartlar ve koşullar örneği | "… doesn't engage Odoo S.A. responsibility" | `account.account_default_terms_and_conditions` | Şablon kalıtımı (Türkçe örnek metin) |
| Herkese açık sohbet kanalı | başlık `Odoo` | `mail.discuss_public_channel_template` | Şablon kalıtımı |
| Web sitesi | "Powered by Odoo", tanıtım bağlantıları | `website` | MVP dışı; `ov_brand_website` sonra |

## 7. Çeviri metinleri ve veritabanı kayıtları (T2.6)

**Çevrilebilir metinler (`.pot`):**
- Tüm upstream: 603 modülde 100.284 metin; 168 modülde 542 metin "odoo" içeriyor.
- MVP denemesinde kurulu 97 modül: 30.549 metin; 40 modülde 253 metin.
  - En çok: `base` 30, `web` 23, `account` 21, `spreadsheet` 20, `mail` 18, `crm` 16, `stock` 16, `mail_plugin` 13, `mrp` 9, `purchase` 9, `mail_bot` 8, `digest` 7.
- Bunların bir kısmı URL'dir (`odoo.com/documentation` vb.), bir kısmı ürün adıdır ("Odoo allows you to…"). Türkçe çeviriler (`tr.po`) adı çoğunlukla aynen taşıyor ("Odoo Hatası").
- Yöntem: kendi modülümüzün çeviri dosyasıyla metin değiştirme (T3.6'da araştırılan yöntem) ya da ilgili JS/şablon override. T2.6 testi, kalanları bulur.

**Veritabanı kayıtları (MVP denemesi):**
- Etkin görünümlerde "Odoo" geçen 32 kayıt. Örnekler: `web.layout`, `web.login`, `web.login_layout`, `web.brand_promotion_message`, `web.report_layout`, `web.webclient_offline`, `mail.mail_notification_layout`, `digest.digest_mail_main`, `portal.portal_record_sidebar`, `account.report_invoice_document`, `purchase.portal_my_purchase_order`, `mail_plugin.app_auth`, `api_doc.docclient`.
- E-posta şablonu 9, özet ipucu 12, iş ortağı 1 (`base.partner_root` = OdooBot).
- Uygulama adı veya özetinde "Odoo" geçen modül 4 (ör. `mail_bot` "OdooBot").

## 8. Görseller

| Dosya | Nerede görünüyor | Görev |
|---|---|---|
| `web/static/img/favicon.ico` | sekme simgesi; veritabanı yöneticisi, herkese açık sohbet | T2.2 |
| `web/static/img/odoo-icon-192x192.png`, `-512x512.png`, `odoo-icon-ios.png` | PWA ve iOS ana ekran | T2.2 |
| `web/static/img/logo.png` | `/web/binary/company_logo` yedeği: yalnız veritabanı yokken ve hata durumunda (şirket logosu yoksa `nologo.png`; varsayılan şirket logosu markasız "Your logo"), portal "Powered by" | T2.5 (portal) |
| `web/static/img/logo2.png` | veritabanı yöneticisi | üretimde kapalı (`list_db = False`) |
| `web/static/img/logo_inverse_white_206px.png` | e-Fatura bildirim e-postası | T2.5 |
| `account/static/src/img/Odoo_logo_O.svg` | fatura QR kodu | T2.5 |
| `mail/static/src/img/odoobot.webp` | OdooBot avatarı | T2.5 |
| `web/static/img/odoo_logo.svg` | POS, web sitesi yükleyicisi | MVP dışı |

Yöntem: dosyanın kendisi değiştirilmez (upstream'e dokunulmaz). Görseli kullanan şablon/rota markanın görseline yöneltilir.

## 9. OCA `server-brand` adayları

| Modül | Dal | Lisans | Bağımlılık | Ne yapar | Değerlendirme |
|---|---|---|---|---|---|
| `remove_odoo_enterprise` | 20.0 (var) | AGPL-3 | `base_setup` | Ayar ekranlarından yalnız Enterprise'da olan özellikleri kaldırır; 20.0'da satın alınacak uygulamaları ve ödeme sağlayıcılarını aramadan da çıkarır | Kullanılıyor (T2.3): `vendor/oca/server-brand`, `ov_brand`'in bağımlılığı |
| `disable_odoo_online` | 19.0; 20.0 port PR'ı açık (#124) | AGPL-3 | `mail` | Yayıncı garantisi ve odoo.com bağlantılarını kapatır | Kullanılmıyor: 2026-10-19'da PR hâlâ birleşmemiş; aynı işi `ov_brand_mail` ve `ov_brand` yapıyor (T2.3) |
| `mail_debranding` | 19.0 | AGPL-3 | `mail` | E-posta "Powered by" | T2.5'te değerlendirilir; 20.0 portu gerekir |
| `portal_debranding` | 19.0 | LGPL-3 | `portal` | Portal "Powered by" | T2.5 |
| `sale_portal_debranding` | 19.0 | AGPL-3 | `sale` | Satış portalı | T2.5 |
| `website_debranding` | 19.0 | LGPL-3 | `website` | Web sitesi | MVP dışı |

Not: OCA modüllerinin kendisi kullanıcıya "OCA" yazar adıyla görünür (Uygulamalar ekranı). Telif bilgisi olduğu için değiştirilmez; Uygulamalar menüsü son kullanıcıdan T7.3'te gizlenir. `remove_odoo_enterprise`'ın adında "Odoo" da geçiyor ("Remove Odoo Enterprise"); T2.6'nın izin listesinde ele alınır.

## 10. Değiştirilmeyenler (T2.6 izin listesi önerisi)

- Lisans ve telif notları (CLAUDE.md kural 2): kaynak başlıkları, ayarlardaki "Copyright © Odoo S.A. … LGPL" satırı, manifestlerdeki yazar `Odoo S.A.` (Uygulamalar ekranında görünür).
- Teknik adlar: `odoo` Python paketi, `@odoo/owl`, `odoo.define`, `o_` CSS sınıfları, `odoo-bin`, `release.product_name` (yalnız sunucu günlükleri ve veri klasörü adı, kullanıcıya görünmez).
- `/web/webclient/version_info` JSON yanıtı: yalnız sürüm numarası, ad içermiyor.
- E-tablo formül adları `ODOO.BALANCE`, `ODOO.PIVOT`, `ODOO.LIST` vb. (`spreadsheet`, `spreadsheet_account`). Formül yazan kullanıcı görür. Ancak kayıtlı panolar bu adları içeriyor; yeniden adlandırmak kayıtlı formülleri bozar. Varsayım: teknik ad sayılır, izin listesinde kalır (USER_TASKS K13).

## 11. Görevlere etkisi

- **T2.2 `ov_brand` (tamam):** §3, "Diğer istemci mesajları" satırı hariç. Marka adı tek ayardan okunur (F2 kabul ölçütü): `ov_brand.name` sistem parametresi, varsayılan Nexus. `web.web_app_name` eşitlenmedi: Genel Ayarlar'daki uygulama adı yalnız tarayıcıdan kurulan uygulamanın adıdır, boşsa marka adı kullanılır.
- **T2.3 (tamam):** §4. Yayıncı garantisi, IAP, `mysubscription`, Enterprise reklamları, dokümantasyon bağlantıları, metin düzenleyici ve uygulama mağazası. Gmail/Outlook uç durumu T2.7'de (§4.4).
- **T2.4:** §5.
- **T2.5:** §6 ve PDF motoru seçimi (PLAN'daki not).
- **T2.6:** §7'deki üç kaynak (sayfalar, veritabanı kayıtları, çeviriler) ve §10'daki izin listesi. §3'ten kalan üç JS metni.
- **T2.7:** §4.2'deki test çatısı engelinin üstüne günlük denetimi ve tarayıcı ağ kaydı; §4.4'teki uç durum.
