# Değişiklik Günlüğü

Son güncelleme: 2026-10-19

Her adımın kaydı en üste, tarih başlığıyla eklenir. Bir karar değiştiğinde **eski metni ve değişiklik nedeni** buraya yazılır (DECISIONS.md yalnız güncel hali tutar).
Kategoriler: **Kararlar**, **Belgeler**, **Kod**, **Ortam**, **Araştırma**.

## 2026-10-19

### Adım: e-posta, rapor ve portal altbilgileri, bot, PDF motoru önerisi (T2.5) — otonom mesai 2

**Kod**
- Yöntem: OCA `mail_debranding`, `portal_debranding`, `sale_portal_debranding` (19.0) yerine kendi şablon kalıtımlarımız. 20.0 portu gerekirdi; kapsadıkları yüzeyler bizim envanterimizin (§6) bir parçası.
- "Powered by" satırları kaldırıldı, yerine ürün adı yazılmadı (USER_TASKS K17 varsayımı).
- `ov_brand`:
  - PDF başlığı (`web.report_layout`, `web.report_preview_layout`) marka adı.
  - Sunucunun yazdığı PDF dosyalarında (bölünen, birleştirilen, PDF/A) `Creator` ve `Producer` marka adı. Upstream bunları çekirdek yazıcı sınıfında sabit yazıyor; sınıfın yazma yöntemi modül yüklenirken değiştirildi, ad rapor başına bağlam değişkeninden geliyor.
- `ov_brand_mail`:
  - Bildirim e-postalarının iki düzeninde "Powered by" satırı yok; takibi bırakma bağlantısı kalır.
  - E-postalara gömülü yayıncı logosu (ör. e-Fatura bildirim şablonu) işlenen metinden süzülür.
  - Herkese açık sohbet sayfasının başlığı ve simgesi.
  - Bot (`base.partner_root`, upstream'de "OdooBot") marka adını ve simgesini taşır; `ov_brand.name` değişince eşitlenir. Bot sohbetlerde ve kayıt geçmişinde görünür; bu yüzden `mail`'e bağlı modülde.
- Yeni modüller (AGPL-3, ilgili uygulamayla kendiliğinden kurulur):
  - `ov_brand_portal`: belge kenar çubuğundaki "Powered by" ve logo; güvenlik sayfasındaki iki belge bağlantısı (iki adımlı doğrulama, API anahtarları).
  - `ov_brand_digest`: özet e-postasında "Sent by" ve "Powered by" satırları, mobil uygulama tanıtımı (görselleri yayıncının sunucusunda), ipuçları (yayıncının içeriği, görselleri yayıncının sunucusunda). Varsayılan özetin adı "Your Periodic Digest"; kurulumda bu kaydın eski çevirileri silinir, yoksa upstream'in "Odoo Periyodik Özetiniz" çevirisi bizimkinin önüne geçiyor (çeviri yükleyicisi var olan çeviriyi değiştirmiyor).
  - `ov_brand_account`: fatura PDF'indeki QR kodların ortasındaki yayıncı logosu; şartlar ve koşullar örneğindeki yayıncı adı geçen cümle.
  - `ov_brand_purchase`: tedarikçi portalındaki "Want to import this document in Odoo?" / "Start on Odoo" tanıtımı; yerinde belgeyi UBL olarak indirme adresi kalır.
- Testler: `ov_brand` 30, `ov_brand_mail` 6, `ov_brand_portal` 2, `ov_brand_digest` 3, `ov_brand_account` 3, `ov_brand_purchase` 1 test yöntemi. Sekiz marka modülü birlikte 51 test, hepsi geçti.
- Çeviriler: yeni metinlerin Türkçesi (`i18n/tr.po`).
- `ov_demo`: `ov_brand_portal`, `ov_brand_digest`, `ov_brand_account` kuruldu; `ov_brand`, `ov_brand_mail` güncellendi. Özetin Türkçe adı "Periyodik Özetiniz", botun adı Nexus.

**Araştırma**
- PDF motoru (`docs/research/pdf-engine.md`): wkhtmltopdf upstream'in varsayılanı ama arşivde; Paper Muncher etkin ama kendi tanımıyla erken alfa, yalnız amd64 Linux. Öneri üretimde wkhtmltopdf, Paper Muncher CI'da ikinci motor (USER_TASKS K18). Yeni risk R18.

**Kararlar (USER_TASKS)**
- K17 (yeni, varsayım A): "Powered by" satırı yok.
- K18 (yeni, varsayım A): PDF motoru önerisi.

**Belgeler**
- PLAN.md (T2.5 `[x]`, sonuç; T2.6, T3.7, T8.4 notları; R18; F2 5/7; şu anki görev T2.6), USER_TASKS.md (K17, K18), ARCHITECTURE.md (Marka satırı, PDF motoru), CLAUDE.md (PDF motoru notları), `docs/MODULE_MATRIX.md`, `docs/research/brand-inventory.md` (Sonuç, §6, §9, §11), yeni `docs/research/pdf-engine.md`, README.md, state.json.

### Adım: web istemcisi `/app` yolunda (T2.4) — otonom mesai 2

**Kod (`ov_brand`)**
- Yol `/app` (`tools.WEB_PATH`; USER_TASKS K16 varsayımı). Çekirdeğe dokunmadan, yalnız modülle (D-010).
- Sunucu:
  - `Home.web_client` override: `/app` ve `/app/...` web istemcisini sunar; `/odoo` ve `/odoo/...` sorgusuyla birlikte `/app`'e yönlendirilir (303). Sunucunun `/odoo` ile ürettiği bağlantılar (e-posta, bildirim, giriş sonrası) böylece çalışır.
  - Giriş: sonrası `/app`'e gider; `redirect=/app/...` adresli giriş sayfasının bağlantı önizlemesi eylemin adını gösterir (upstream bunu yalnız `/odoo` için yapıyordu).
  - Tarayıcıdan kurulan uygulama: kapsam, başlangıç adresi, kısayollar ve paylaşım hedefi `/app`. Service worker `/app` kapsamında; betikteki yollar (`web` ve `mail` parçaları) `/app`. Çevrimdışı sayfa iki yolda da.
- JS (`static/src/webclient/web_path.js`):
  - `router.stateToUrl` ve `router.urlToState` yamalı; yönlendiricinin iç durumu `/odoo` ile çalışmaya devam ediyor. Yönlendirici modül yüklenirken adresi okuduğu için yamadan sonra yeniden başlatılıyor.
  - Upstream'in iç bağlantı dinleyicisi yalnız `/odoo` sayfalarında çalışıyor; `/app` için aynısı eklendi, `/odoo` bağlantıları da sayfa yenilenmeden açılıyor.
  - Service worker kaydı `/app` kapsamıyla; menü ve ilişki alanı bağlantıları `/app` gösteriyor.
- `ov_brand_html_editor`: düzenleyiciye yapıştırılan `/app/...` kayıt bağlantılarının önizlemesi (upstream yalnız `/odoo`'yu tanıyordu).
- Testler: yeni `test_web_path.py` (yönlendirme, giriş, önizleme, manifest, service worker; tarayıcıda yönlendirici, menü bağlantıları ve sayfa yenilemeden iç bağlantı). Eski testler `/app` ile. `ov_brand` 27, `ov_brand_html_editor` 3 test; dört modül birlikte 35 test, hepsi geçti.
- Windows'ta bir tam çalıştırmada `test_settings_documentation_links` "Session Expired" ile düştü, tekrarında geçti.
  - Neden upstream'in oturum deposu: service worker kurulurken ana sayfayı ister, o istek oturum dosyasını yeniden yazar. Windows'ta değiştirilmekte olan dosyayı aynı anda okuyan istek `PermissionError` alır ve boş oturumla devam eder.
  - Ölçüm: 3 saniyede 17 044 okumanın 1 617'si hata verdi. Linux'ta dosya değişimi atomik; CI etkilenmez. CLAUDE.md'ye not eklendi.
- Bilinen sınırlar (envanter §5): upstream'in diğer JS bağlantıları `/odoo` ile; fareyle üzerine gelince görünebilir, tıklanınca yönlendirme ya da yeni dinleyiciyle `/app`'e varır. Veritabanı yükleme hatasındaki `?db=` temizliği yalnız `/odoo` için. Web sitesi düzenleyicisi `/odoo` varsayıyor (MVP dışı). Upstream'in `/odoo` bekleyen testleri `ov_brand` kuruluyken düşer; kendi testlerimiz etkilenmiyor.

**Belgeler**
- PLAN.md (T2.4 `[x]`, sonuç; F2 4/7; şu anki görev T2.5), USER_TASKS.md (K16), `docs/research/brand-inventory.md` §5 ve §11, README.md, CLAUDE.md (Windows test notu), state.json.

### Adım: dokümantasyon bağlantıları, metin düzenleyici ve uygulama mağazası (T2.3 bitti) — otonom mesai 2

**Kod**
- `ov_brand`:
  - Ayarlardaki odoo.com dokümantasyon bağlantıları ("?") gizli: `DocumentationLink` bileşenine JS `patch()`, bağlantı yayıncının sitesine gidiyorsa çizilmez. Hakkında bölümündeki telif satırının bağlantısı kalıyor (D-007).
  - Uygulama mağazası: `base_import_module` bağımlılık oldu (zaten `web` ile kendiliğinden kuruluyordu). Sektör modüllerinin listesi ve kategorileri boş döner, indirme hata verir; mağazaya hiç istek gitmez. Uygulamalar ekranındaki "Sektörler" süzgeci kaldırıldı, "Tema Mağazası" ve "Üçüncü Taraf Uygulamaları" menüleri pasif.
  - Yeni testler: ayarlarda yayıncıya giden dokümantasyon bağlantısı yok (tarayıcıda), mağaza çağrılmıyor, süzgeç ve menüler gizli. `test_webclient_js` sabit bir eylemi açıyor: `mail` kuruluyken varsayılan uygulama (Discuss) başlığa sohbet adını yazabiliyor, bir kez "OdooBot" görüldü (T2.5). `ov_brand` 20 test.
- Yeni modül `ov_brand_html_editor` (AGPL-3; `ov_brand`, `html_editor`; kendiliğinden kurulur):
  - Düzenleyicide "Google Translate ile çevir" eklentisi yok (sohbet penceresindeki düzenleyici dahil).
  - Görsel ekleme penceresi yayıncının çizim kitaplığını aramıyor, "Çizimler" süzgeci gizli.
  - Sunucu uçları (`generate_text`, `google_translate`, `save_library_media`) ağa çıkmadan hata döner; `media_library_search` boş sonuç verir. Bu hizmetler düzenlenen metni veya arama sözcüklerini veritabanı kimliğiyle gönderiyordu.
  - 2 test (biri tarayıcıda), Türkçe çeviri, `README.rst`.
- Bulgular, kod gerekmedi:
  - Gmail/Outlook OAuth vekili: Community'de ilk bağlantı sürüm denetimiyle engelli, vekil fiilen kapalı. Uç durum: kendi istemci kimliğiyle bağlandıktan sonra kimlik ve gizli anahtar silinirse belirteç yenileme vekile gidiyor. T2.7'nin dış istek testine eklendi (envanter §4.4).
  - `mail`'deki dış istekler yayıncıya gitmiyor: görüntülü görüşme sunucusu (SFU) ve Twilio yalnız kullanıcı ayarlarsa, bağlantı önizlemesi mesajdaki adrese. Görüşmeler varsayılan olarak Google'ın STUN sunucularını kullanıyor (tarayıcıdan, IP adresi görünür); KVKK notu olarak COMPLIANCE.md'ye yazıldı.
  - OCA `disable_odoo_online` 20.0 portu (PR #124) hâlâ birleşmemiş; kendi modüllerimiz aynı işi yapıyor, kullanılmıyor.
- Testler: `ov_brand`, `ov_brand_mail`, `ov_brand_html_editor`, `remove_odoo_enterprise` birlikte 27 test, hepsi geçti.

**Belgeler**
- PLAN.md: T2.3 `[x]`, sonuç; F2 3/7; şu anki görev T2.4. T2.7 ve T8.7'ye not.
- `docs/research/brand-inventory.md` (§4 sonuç, yeni §4.4, §9, §11), COMPLIANCE.md (KVKK), ARCHITECTURE.md (marka katmanı), README.md, state.json.

### Adım: Enterprise reklamları kaldırıldı — OCA `remove_odoo_enterprise` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- OCA `server-brand` deposu 20.0 dalıyla `vendor/oca/server-brand` altına sığ git submodule olarak eklendi (commit `9637fe38`, 2026-10-07). 20.0 dalında yalnız `remove_odoo_enterprise` var.
- `remove_odoo_enterprise` (AGPL-3; `base_setup`) `ov_brand`'in bağımlılığı oldu, marka modülüyle her zaman kurulu.
  - Ayarlar ekranında yalnız Enterprise'da olan özellikler (`upgrade_boolean`) ve boşalan bloklar gizleniyor.
  - Uygulamalar listesindeki satın alınacak uygulamalar (`to_buy`) ve ödeme sağlayıcıları aramada dönmüyor. Envanter §4'teki "ayrı `to_buy` filtresi" önerisine gerek kalmadı: OCA'nın 20.0 sürümü bunu da yapıyor.
- Yeni test: satın alınacak uygulamalar veritabanında duruyor ama listelenmiyor (`ov_brand` 17 test). `README.rst`.
- `tools/run_tests.py`: `ov_brand` önce kurulunca onunla gelen hedef modüller (ör. `remove_odoo_enterprise`) ikinci çalıştırmada güncellenir (`-i` ve `-u` birlikte), testleri de çalışır. Önceki sürümde bunların testleri atlanıyordu. Birlikte çalıştırma: 22/22 (`ov_brand` 17, `ov_brand_mail` 2, `remove_odoo_enterprise` 3).
- `ov_brand`'in tarayıcı testi sabit bir eylemi açıyor (Kullanıcılar). `mail` kuruluyken açılış uygulaması Discuss sekme başlığına "OdooBot" yazabiliyor; yerelde bir kez testi düşürdü. Gerçek bir marka izi: envanter §3'teki OdooBot satırına eklendi, T2.5'te.
- Not: modülün Uygulamalar ekranındaki adı "Remove Odoo Enterprise". Telif ve yazar bilgisi olduğu için değiştirilmedi; Uygulamalar menüsü son kullanıcıdan T7.3'te gizlenir, T2.6'nın izin listesinde ele alınır.

**Belgeler**
- docs/COMPLIANCE.md §5 (lisans envanteri), state.json (`modules.vendored`, ortam), ARCHITECTURE.md (durum notu, depo yerleşimi), CLAUDE.md (ortam), PLAN.md (T2.3 ara durum), `docs/research/brand-inventory.md` (§3 OdooBot, §4 sonuç, §9).

### Adım: eski commit'lerden oturum bağlantısı satırları silindi (K10) — otonom mesai 2

**Kullanıcının isteği:** "önceki commitlerden claude oturum linklerini sil."

**Yapılan**
- 21 commit'in 17'sindeki `Claude-Session:` satırı silindi. Satırın önünde kalan boş satır da gitti; mesajların geri kalanı aynı.
- Yöntem: depo geçici klasöre klonlandı, `git filter-branch --msg-filter` ile yalnız mesajlar yeniden yazıldı. `main` `--force-with-lease` ile bir kez force-push edildi (`ca350bb` → `e4a98f7`).
- Denetim: son commit'in dosya ağacı yeniden yazmadan önceyle aynı (`e6f9387`), commit sayısı aynı, yazar, işleyen ve tarihler aynı.
- Yerel depo yeni geçmişe `git reset --soft` ile taşındı. Ağaçlar aynı olduğu için çalışma alanı değişmedi; yarım kalan T2.3 işi korundu.
- Kalan: ilk iki commit'teki `Co-Authored-By: Claude` satırı. İstek yalnız oturum bağlantılarıydı; bu satırlar K10'da ayrı soru olarak duruyor.
- Bilinen sınır: GitHub eski commit'leri kimlikleriyle bir süre daha açabilir, eski CI çalıştırmaları eski kimlikleri gösterir. Tamamen silinmeleri için GitHub desteğine başvurmak gerekir.

**Commit kimlikleri (eski → yeni)**

| Eski | Yeni |
|---|---|
| `ca350bb` | `e4a98f7` |
| `2a6b523` | `67a61ba` |
| `c48b98f` | `1dd6aaf` |
| `1495616` | `ec14669` |
| `b4380e5` | `1bac273` |
| `a49a92c` | `9e90991` |
| `c2dbc6c` | `9fee384` |
| `1e2960f` | `6a2fc36` |
| `c6b11ba` | `6309fd5` |
| `185e4b4` | `1b94f2a` |
| `2a3a8ef` | `6df7425` |
| `b0019a5` | `95f94a8` |
| `c6d154f` | `6347bda` |
| `a253ed4` | `3f1d555` |
| `b4f2ea6` | `05c4fa2` |
| `d5d0cd6` | `3f2edda` |
| `a170482` | `a8f6bd2` |
| `811f913` | `45bda8d` |
| `409a403` | `f33fe70` |
| `24f56b3` | `363a288` |
| `cf37443` | `b267933` |

**Belgeler**
- Belgelerde geçen eski kimlikler güncellendi: USER_TASKS.md K10 (`cf37443`, `24f56b3`), bu dosyadaki ilk CI çalıştırması notu (`c6b11ba`).
- DECISIONS.md D-015 (force-push istisnası, eski commit'ler), USER_TASKS.md (K10 yalnız ortak yazar satırına indi; K11 notu).

### Adım: çevrim içi hizmet modülleri kaldırıldı — IAP ve `mysubscription` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- `ov_brand` yayıncının çevrim içi hizmet modüllerini (`iap`, `mysubscription`) onlara bağlı modüllerle birlikte kaldırıyor.
  - Neden kaldırma: ikisi de `auto_install` (`web` + `base_setup`, `base` + `web`); her yeni veritabanına kuruluyorlar, modül bağımlılığıyla engellenemiyorlar. MVP modüllerinden hiçbiri bunlara zorunlu bağımlı değil.
  - Yöntem: her kurulum ve güncellemenin sonunda (`ir.model.data._process_end`; Odoo'nun kaldırılacak modülleri kaldırmadan hemen önceki adımı) kurulu olanlar kaldırılmak üzere işaretlenir. Komut satırından kurulanlar da böylece geri alınır. `post_init_hook` kullanılmadı: aynı çalıştırmada kurulan modüller yükleme sonunda yeniden "kurulu" işaretleniyor.
  - IAP hesap kayıtları kaldırmadan önce silinir. Yoksa upstream'in kaldırma adımı, hizmet kayıtlarını silemediğini (kısıtlı yabancı anahtar) ERROR olarak günlüğe yazıyor; tablolar yine de siliniyor.
  - Arayüzden kurulum (`button_install`) bu modülleri getirecekse hata verir.
  - Ayarlar ekranında bu modülleri kuracak kutular (`module_sms`, `module_partner_autocomplete`, CRM'deki aday zenginleştirme ve üretme vb.) görünümden çıkarılır; boşalan blok da kalkar.
  - MVP deneme veritabanında (`ov_brand_scan`) kaldırılan 12 modül: `iap`, `iap_mail`, `iap_crm`, `sms`, `calendar_sms`, `crm_sms`, `sale_sms`, `stock_sms`, `partner_autocomplete`, `crm_iap_enrich`, `crm_iap_mine`, `mysubscription`. Kurulu modül sayısı 87.
  - 4 yeni test (`ov_brand` 16/16, `ov_brand_mail` 2/2). `i18n/tr.po`, `README.rst`.
- `tools/run_tests.py`: hedef modüller `ov_brand`'e bağlıysa `ov_brand` önce testsiz kurulur, testler ikinci çalıştırmada. Neden: modül kaldıran bir çalıştırmada Odoo kayıt defterini yeniden yükler ve `post_install` testlerini hiç başlatmaz.
- Yerel `ov_demo` veritabanına `ov_brand` kuruldu (`ov_brand_mail` kendiliğinden geldi); CLAUDE.md'deki demo komutu güncellendi.

**Karar**
- USER_TASKS K15 (otonom varsayım, geri dönüşü kolay): gizlemek yerine kaldırmak. PLAN T2.3'teki "kapatılır veya gizlenir" ve `mysubscription` için "menü öğesi gizlenir" önerileri bu varsayımla değişti. Envanter §4.3'teki öneri (JS ile menü öğesini kaldırmak) da uygulanmadı.

**Belgeler**
- PLAN.md (T2.3 maddeleri ve ara durum), USER_TASKS.md (K15), docs/COMPLIANCE.md (KVKK), `docs/research/brand-inventory.md` (Sonuç, §4, §4.3), ARCHITECTURE.md (demo veritabanı, test aracı), CLAUDE.md (demo komutu, test aracı), README.md, state.json.

### Adım: yayıncı garantisi kapatıldı — `ov_brand_mail` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- Yeni modül `addons/ov_brand_mail` (AGPL-3; `ov_brand`, `mail`). `auto_install`: `mail` kurulu her veritabanına kendiliğinden kurulur.
  - `publisher_warranty.contract._get_sys_logs` ağa çıkmadan boş yanıt döndürür. Rapor (veritabanı kimliği, kullanıcı sayıları, kurulu uygulamalar, şirketin adı, e-postası ve telefonu) hiç gönderilmez. Kurulumda raporu çağıran `l10n_fr_account` ve `l10n_fr_pos_cert` de bu yoldan geçer.
  - `mail.ir_cron_module_update_notification` pasif. `mail`'in kaydı `noupdate`; `mail` güncellenince yeniden açılmaz.
  - 2 test: rapor isteği hiç yapılmıyor (`requests.post` çağrılmıyor), iş pasif. `i18n/tr.po`, `README.rst`.
- OCA `disable_odoo_online` yerine kendi override'ımız: 20.0 portu (PR #124) hâlâ açık; işimiz tek yöntem (envanter §9 önerisi).

**Belgeler**
- PLAN.md (T2.3 `[~]`, ara durum), state.json (`modules.ours`), docs/COMPLIANCE.md (KVKK: yayıncı garantisi kapalı), `docs/research/brand-inventory.md` §4.1 (sonuç), ARCHITECTURE.md (modül listesi state.json'a bağlandı), README.md.

### Adım: Marka modülü `ov_brand` (T2.2) — otonom mesai 2

**Kod**
- `addons/ov_brand` tamamlandı ve depoya girdi (otonom mesai 1'deki ara durumun devamı).
  - Varsayılan ürün adı `OV ERP` yerine **Nexus** (K3). Simge mavi kare üstünde beyaz "N" (K14 varsayımı, renk `#1f5f8b`).
  - Tarayıcıdan tek uygulama olarak kurulumun manifesti (`/web/manifest.scoped_app_manifest`): Odoo'nun sabit rengi `#714B67` yerine marka rengi. Uygulamanın kendi simgesi yoksa marka simgesi.
  - `test_login_page_js` düzeltildi: yalnız yüklenemeyen modüllere ve `@ov_brand/` modüllerine bakıyor. Upstream'in test turları tembel yüklenen pakette bekleyebilir; bu hata değil.
  - `i18n/tr.po` (19 metin) ve `README.rst` (Türkçe: neleri değiştirir, ayarlar, bilinen sınırlar).
  - Testler: 12/12, ikisi tarayıcıda. Günlükteki tek CRITICAL satırı upstream gürültüsü: test kipinde websocket kapalı, Chrome kapanırken bu isteğin bağlantısı kopuyor.
- Lint çelişkisi: ruff (upstream kural seti, TID252) aynı modülden içe aktarmaların mutlak, pylint-odoo (`odoo-addons-relative-import`) göreli olmasını istiyor.
  - Upstream'in kuralı uygulandı: içe aktarmalar mutlak (`from odoo.addons.ov_brand.tools import …`).
  - pylint denetimi `.pre-commit-config.yaml`'daki kanca argümanıyla kapatıldı. `.pylintrc`'de `disable=all` + `enable=odoolint` sonrasında tek bir mesaj kapatılamıyor; `.pylintrc`'ye açıklama notu eklendi.
- Kalanlar T2.6'ya taşındı: barkod tarayıcının kamera izni mesajı ("Odoo needs your authorization first."), rapor işçileri uyarısı, güvensiz bağlam konsol uyarısı. Üçü de upstream yöntemlerinin gövdesinde çevrilebilir metin.

**Araştırma**
- Envanterdeki öneri değişti (`docs/research/brand-inventory.md` §11).
  - Eski metin: "`web.web_app_name` de bu değerle eşitlenir."
  - Yeni: eşitlenmiyor. Genel Ayarlar'daki uygulama adı yalnız tarayıcıdan kurulan uygulamanın adıdır; boşsa marka adı kullanılır.
  - Neden: iki ayarı eşitlemek, müşterinin kendi uygulama adını ürün adının üstüne yazmasına yol açar. Marka adının tek kaynağı `ov_brand.name` kalır (M2 kabul ölçütü).

**Ortam**
- Geçici veritabanı `ov_brand_scan` T2.3 denemeleri için tutuluyor. Otonom mesai 1 özetinde "T2.2 bitince silinir" yazıyordu; mesai sonunda silinecek.

**Belgeler**
- PLAN.md (T2.2 tamam; T2.6'ya kalan metinler), state.json (`modules.ours`, lint notu), CLAUDE.md (lint komutu, içe aktarma notu), ARCHITECTURE.md (durum notu, depo yerleşimi, lint), README.md, `docs/research/brand-inventory.md` (§3, §11).

### Adım: kararlar — kalıcı ürün adı Nexus (K3) ve commit oturum satırı (K11)

**Kararlar**
- K3 / D-014: kullanıcı kalıcı ürün adını seçti: **Nexus**. D-014 yerinde yeniden yazıldı (başlık "Ürün adı, çalışma adı ve teknik modül öneki").
  - Eski metin: "**Çalışma adı:** `odoo-version`. Geçicidir, MVP sonunda kalıcı adla değişecek. GitHub deposunun adı da budur." · "Yeniden değerlendirme: T8.1 (kalıcı ad ve yeniden adlandırma)."
  - Yeni: ürün adı Nexus; çalışma adı yalnız depo adında ve geliştirme ortamında kalır; yeniden değerlendirme T8.2 (tescil araştırması, depo yeniden adlandırması). Modül öneki `ov_` değişmedi.
  - Neden: kullanıcı kararı. Kalıcı ad T8.1'deki MVP sonu değerlendirmesinden öne alındı.
  - Not: "Nexus" yaygın bir sözcük; tescil çakışması riski PLAN'a R17 olarak eklendi. TÜRKPATENT sorgusu ve alan adı kontrolü dış demodan önce (T8.2).
- K11 / D-015: commit mesajlarındaki `Claude-Session:` satırı kaldırıldı. Kural CLAUDE.md kural 8'e ve D-015'e eklendi.
  - Eski hali: "Varsayılan: satır kalır" (USER_TASKS K11).
  - Eski commit'lerdeki satırlar geçmiş yeniden yazılmadan silinemez; K10'un B seçeneği bunları da kapsayacak biçimde genişletildi.
- K14: geçici ad varsayımı (`OV ERP`) kalktı; madde yalnız renk ve simgeyi kapsıyor. Simge "N" harfine çevrilecek (T2.2).
- K12: C seçeneği artık marka adı `Nexus`; Claude önerisi C. Karar kullanıcıda.

**Belgeler**
- DECISIONS.md (D-014, D-015), CLAUDE.md (proje özeti, kural 2 ve 8, protokol, komutlar), PLAN.md (§2.1, M2 kabulü, kapı ölçütü 6, T8.1, T8.2, R17), USER_TASKS.md (§1, K3, K10, K11, K12, K14, T8.1, T8.2), README.md (başlık ve ad notu), docs/COMPLIANCE.md §3, state.json.

## 2026-10-18

### Otonom mesai 1 — özet

Kullanıcının isteğiyle T2.2'nin ortasında bitirildi.

**Biten görevler (11):** T1.3 PostgreSQL, T1.2 sürüm doğrulaması (Odoo 20.0 kesinleşti), T1.4 upstream submodule, T1.5 Python ortamı, T1.6 yerel Odoo ve Türkçe demo veritabanı, T1.7 Odoo AI rehberleri, T1.8 test çalıştırıcısı, T1.9 modül şablonu ve lint, T1.10 GitHub Actions CI, T1.11 `vendor/` ve `ports/` düzeni (ilk OCA portu `report_xlsx`), T2.1 marka izleri envanteri. F1 tamamlandı.

**Süren görev:** T2.2 `ov_brand`. Kod yerelde, commit edilmedi (aşağıdaki adım). Sonraki mesaide kaldığı yerden sürer.

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** K12 modül yazar adı, K13 e-tablo `ODOO.` öneki, K14 geçici ürün adı ve görünümü. Hepsi geri dönüşü kolay varsayımlarla ilerledi. Mesai öncesinden bekleyenler: K10 (eski iki commit'teki ortak yazar satırı), K11 (oturum bağlantısı satırı).

**Onay bekleyen dışa dönük iş:** yeni yok. K9 (GitHub güvenlik özellikleri) bekliyor.

**Yerelde kalanlar:**
- `addons/ov_brand/` (commit edilmedi).
- Geçici veritabanları `ov_brand_scan` (T2.1 taraması, T2.2 denemeleri) ve `ov_test_ov_brand` (test çalıştırıcısı her seferinde yeniden kurar). Yalnız yerelde; T2.2 bitince `ov_brand_scan` silinir.
- PostgreSQL sunucusu durduruldu. Yeniden başlatmak için: `python tools/pg.py start`.

**CI:** T2.1 commit'inin çalıştırması (39152359525) başarılı.

### Adım: Marka modülü `ov_brand` (T2.2, sürüyor) — otonom mesai 1

**Kod** (yerelde, commit edilmedi)
- `addons/ov_brand` (`web`, `base_setup`): marka adı `ov_brand.name` sistem parametresinden (varsayılan `OV ERP`, K14). Oturum bilgisine (`ov_brand_name`) ve QWeb şablonlarına veriliyor.
  - Sunucu şablonları: sekme başlığı, favicon, giriş ekranı altbilgisi, bağlantı önizlemesi etiketleri (Odoo sloganı ve @Odoo kaldırıldı, görsel bizim simge), iOS simgesi ve tema rengi, çevrimdışı sayfa (metin, düğme rengi).
  - PWA manifesti: ad (Genel Ayarlar'daki uygulama adı hâlâ önce gelir), renk, simgeler.
  - JS `patch()`: pencere varsayılan başlığı, hata pencereleri ("Odoo Hatası" → "Hata" vb.), oturum süresi bildirimi, kullanıcı menüsünde "Yardım" (destek adresi yoksa gizli), Ayarlar "hakkında" alanı (marka adı ve sürüm; Odoo S.A. telif satırı kaldı, yanına AGPL notu).
  - SCSS: `$o-community-color` = `#1f5f8b`. Geçici simgeler (SVG, PNG, ICO) Pillow ile üretildi.
- Testler (`tests/test_ov_brand.py`): 11 test. 10'u geçiyor, iki tarayıcı testi dahil (web istemcisi ve giriş sayfası).
  - Kalan hata kendi testimizde: `test_login_page_js`, modül yükleyicide bekleyen işleri hata sayıyor. Bekleyen tek iş upstream'in test turu (`html_editor`); bu tembel yüklenen pakette normal. Denetim yalnız yüklenemeyen modüllere ve kendi modüllerimize bakacak biçimde düzeltilecek.
  - Kalanlar: `i18n/tr.po`, `README.rst`, lint, belge protokolü, commit.
- `tools/run_tests.py`: Odoo ek dosyaları salt okunur (0o444) yazıyor; Windows'ta bu, test veritabanı yeniden kurulurken silmeyi engelliyordu. Çalıştırıcı artık kurulumdan önce o veritabanının filestore dosyalarını yazılabilir yapıyor. T1.2'deki filestore gc hatalarının nedeni de büyük olasılıkla bu.

**Belgeler**
- PLAN.md: T2.2 `[~]`, ara durum notu. OdooBot T2.5'e taşındı. Veritabanı yöneticisi T2.2 kapsamından çıktı (veritabanı olmadan çalışır; üretimde `list_db = False`).
- `docs/research/brand-inventory.md` §3 ve §8: veritabanı yöneticisi ve OdooBot satırları düzeltildi, bağlantı önizlemesi etiketleri eklendi, `logo.png` yedeğinin ne zaman göründüğü netleşti.
  - Düzeltilen eski metin: "Kendi kurulumlarımız için şablon override `ov_brand`'da". Neden: veritabanı olmadan çalışan rotalar yalnız sunucu genelinde yüklü modülleri görür.
- USER_TASKS.md: K14 (yeni Karar), §1 güncel.

### Adım: Marka izleri envanteri (T2.1) — otonom mesai 1

**Araştırma**
- `docs/research/brand-inventory.md`: kullanıcıya görünen Odoo izleri, odoo.com'a giden çağrılar ve her birinin değiştirme yöntemi, görevleriyle (T2.2–T2.7).
  - Yöntem: upstream kod taraması; `.pot` sayımı; MVP modülleriyle kurulan geçici veritabanında kayıt sayımı ve oturumsuz sayfaların HTTP denetimi.
  - Bütün yüzeyler modülle değiştirilebiliyor (şablon kalıtımı, JS `patch()`, model/controller override, veri kaydı). Çekirdek değişikliği gereken yüzey bulunmadı; `/odoo` yolu T2.4'te.
  - MVP modülleriyle 97 kurulu modül; 40'ında 253 çevrilebilir metin "odoo" içeriyor. Tüm upstream: 168 modülde 542 metin.
  - Yayıncı garantisi (`mail`, haftalık iş varsayılan olarak açık): veritabanı kimliği, kullanıcı sayıları, kurulu uygulamalar, şirket adı, e-postası ve telefonu şifresiz HTTP ile `services.odoo.com`'a gidiyor. Yanıttaki mesajlar çalışan kanalına yazılıyor. T2.3'ün ilk işi; COMPLIANCE KVKK maddesine eklendi.
  - 20.0'da yeni `mysubscription` her veritabanına kendiliğinden kuruluyor ve odoo.com fiyat/hesap sayfalarına bağlanıyor.
  - Müşteriye giden belgelerde: fatura QR kodunun ortasında Odoo logosu, PDF üst verisinde `Creator/Producer: Odoo`, e-posta altbilgilerinde "Powered by Odoo", satın alma portalında tedarikçiye Odoo tanıtımı.
  - OCA `server-brand`: `remove_odoo_enterprise` resmî 20.0 (yalnız ayar ekranları); `disable_odoo_online` 19.0, 20.0 taşıma PR'ı (#124) açık.
  - Odoo test çatısı `requests` ile dış istekleri zaten engelliyor ve günlüğe yazıyor; T2.7 bunun üstüne kurulacak.

**Kararlar**
- K13 (yeni, varsayım, geri dönüşü kolay): e-tablo formüllerindeki `ODOO.` öneki teknik ad sayılır; marka sızıntısı testinin izin listesinde. USER_TASKS.md'de kullanıcı kararına açık.

**Ortam**
- Geçici veritabanı `ov_brand_scan` (tr_TR, TR; MVP modülleri). Yalnız yerelde, T2.2 denemeleri için tutuluyor.

**Doğrulama**
- T1.11 commit'inin CI çalıştırması (39151290971) başarılı: `ov_ci_sample` ve `report_xlsx` testleri Linux'ta geçti; alt modül önbelleği kaydedildi.

**Belgeler**
- PLAN.md (T2.1 tamam, F2 başladı; T2.2, T2.3, T2.5, T2.6, T2.7'ye envanter bulguları), USER_TASKS.md (K13), docs/COMPLIANCE.md (KVKK: yayıncı garantisinin gönderdikleri), ARCHITECTURE.md (marka katmanı satırı), docs/MODULE_MATRIX.md (`server-brand` adayları), README.md, state.json.

### Adım: `vendor/` ve `ports/` düzeni (T1.11) — otonom mesai 1

**Kod**
- `vendor/oca/server-ux`: OCA'nın resmî 20.0 deposu, sığ git submodule, commit `d952d4df` (2026-10-13).
  - İçinde `date_range` (LGPL-3). Mali raporlar ve `mis_builder` buna bağımlı.
  - `git submodule add --depth 1 -b 20.0` dalı bulamadı (sığ klon yalnız varsayılan dalı çekiyor). Yol: önce `git clone --depth 1 --branch 20.0`, sonra `submodule add` ve `absorbgitdirs`.
- `tools/port_oca.py`:
  - `fetch <depo> <modül>`: OCA deposunu geçici klasöre sığ ve seyrek klonlar, modülü `ports/oca/<depo>/<modül>`'e kopyalar. Sürüm `20.0.1.0.0` (OCA taşıma kuralı). `PORT.md`: kaynak depo, dal, commit, lisans, yazarlar. AGPL-3/LGPL-3 dışı lisansta durur. İndirilen dosyalardan hiçbiri çalıştırılmaz.
  - `upgrade <port>`: Odoo'nun `upgrade_code` betikleri (kaynak dalından sonraki sürümler ve Owl 3) yalnız porta. T1.2'deki Windows sorunları araçta çözüldü: yollar `/` ile, UTF-8, yazma yalnız port klasörüne. `ir-access` betiği bağımlılık modüllerini okur, onlara yazılmaz. Sonuç ve uyarı sayısı `PORT.md`'ye.
  - `diff <port> [--stat]`: kaynak commit'le farkın tamamı.
- `ports/oca/reporting-engine/report_xlsx`: ilk port, OCA 19.0 commit `b9e8c6cd` (AGPL-3).
  - `upgrade_code` değişiklik bulmadı (T1.2'deki gibi).
  - Elle uyarlamalar (T1.2'dekiyle aynı): `odoo.http` paket oldu (`content_disposition` → `odoo.http.stream`, `serialize_exception` → `odoo.http.dispatcher`); kaldırılan `ir.actions.report.report_file` alanı demo verisinden, testten ve kullanım örneğinden (README, `readme/USAGE.md`, `index.html`) silindi.
  - JS değişmedi: `download`, `user` ve `ir.actions.report handlers` 20.0'da aynı.
- CI: `.github/actions/upstream` → `.github/actions/submodules`. Bütün alt modüller (upstream + vendor) sığ çekilir. Önbellek anahtarı sabit commit'lerden; biri değişince son önbellek geri yüklenir.
- Lint: `vendor/` ve `ports/` OCA'nın kod biçiminde kalır. Bizim denetimlerimiz yalnız `addons/` (T1.9 ayarı korunuyor).

**Doğrulama**
- `python tools/run_tests.py report_xlsx,date_range`: addons yolunda upstream, `vendor/oca/server-ux` ve `ports/oca/reporting-engine` var. Odoo özeti 23 test, 0 hata; `RESULT: OK`, Windows gc hatası da yok.
- Aracın denemesi `account_financial_report` ile (geçici, depoya girmedi): `t-call` 3, `ir-access` 4, `owl3-migration` 1 dosya; 1 uyarı (`trial_balance.xml`'de `--` içeren yorum). Sonuç T1.2 ölçümüyle aynı. `diff` doğru farkı verdi.
- OCA'da açık taşıma PR'ı var: reporting-engine #1203 (`report_xlsx`, son güncelleme 2026-10-16). Dosyalar karşılaştırıldı: aynı import değişikliği, aynı `report_file` silme, aynı sürüm `20.0.1.0.0`. PR testleri ayrıca `BaseCommon`'a taşımış; zorunlu değil, alınmadı.
- gitleaks (yerel, `dir`): `ports/`, `tools/port_oca.py`, `.github/` temiz.
- Linux referans testi (T1.10 sonrası, elle CI çalıştırması): `l10n_tr` + `account_edi_ubl_cii` 233 test, 4 hata (Enterprise alanına yazan bir test, nedeni incelenmemiş bir içe aktarma testi, PDF motoru olmadığı için 2 test). Windows'taki 27 gc hatası ve `LocalBinaryFile` hatası Linux'ta yok. Ayrıntı `docs/research/nilvera-port.md` §8.

**Belgeler**
- ARCHITECTURE.md (Durum; §2 ağacı ve "OCA port düzeni": port prosedürü, lint ve test düzeni; §5 CI önbelleği), PLAN.md (T1.11, F1 tamam; T2.1'e OCA yazar adı notu), CLAUDE.md (Ortam: OCA; Komutlar: port aracı, yeni klonda alt modüller), README.md, COMPLIANCE.md §5 (server-ux, `report_xlsx`), MODULE_MATRIX.md (ortak bağımlılıklar), `docs/research/nilvera-port.md` (§5.1 sarmalayıcı araç oldu, §8 Linux referansı; PDF motoru görevi T2.5), state.json.

### Adım: CI düzeltmesi — elle çalıştırma ayrı grupta (T1.10 sonrası) — otonom mesai 1

**Kod**
- `.github/workflows/ci.yml`: eşzamanlılık grubu olay türünü de içeriyor (`ci-<dal>-<olay>`). Önceden `main`'de elle başlatılan referans çalıştırması, sonraki bir push ile iptal edilebiliyordu.

**Doğrulama**
- `main`'deki ilk CI çalıştırması (`6309fd5`; geçmiş 2026-10-19'da yeniden yazılmadan önce `c6b11ba`) yeşil: `checks` 1 dk 17 sn, `tests` 1 dk 48 sn. Upstream, pre-commit ve pip önbellekleri `main`'de kaydedildi.

### Adım: GitHub Actions CI (T1.10) — otonom mesai 1

**Kod**
- `.github/workflows/ci.yml`: her push'ta, pull request'te ve elle (`workflow_dispatch`) çalışır. İki iş paralel:
  - `checks`: `check_docs.py` → `pre-commit run --all-files` → gitleaks 8.30.1 ile tüm geçmiş (arşivin SHA-256'sı doğrulanır) → `sync_skills.py --check`.
  - `tests`: Ubuntu 24.04, Python 3.12, PostgreSQL 18 servisi. `.venv` ve `requirements-dev.txt`; `.env` ve `odoo.conf` yerel araçlarla üretilir.
    - Şablondan `ov_ci_sample` üretilir; modül kuralları, ruff ve pylint-odoo'dan geçirilir.
    - `addons/` ve `ports/` altındaki bütün modüller örnekle birlikte tek veritabanında test edilir (`run_tests.py -v`). Hata olursa günlüğün sonu yazdırılır.
    - Elle çalıştırmada `modules` girdisindeki modüller ayrıca test edilir (Linux referans sonucu).
  - Güvenlik: yalnız okuma yetkisi, eylemler commit SHA'sıyla sabit, `persist-credentials: false`, elle girilen modül listesi kabuğa ortam değişkeniyle geçer.
  - Aynı dalda yeni push eski çalıştırmayı iptal eder.
- `.github/actions/upstream/action.yml`: `upstream/odoo` alt modülünü sığ çeker; git nesneleri upstream commit'ine göre önbellekte.
- `tools/check_secrets.py`: staged değişikliklerde `.env` değerlerini arar (en az 8 karakter; host, port, kullanıcı adı hariç). Pre-commit kancası. Mesai başından beri oturum klasöründe kullanılan betiğin depoya alınmış hali; `.env` yoksa (CI) atlar.
- `tools/run_tests.py`: `-v` gerçek hataların traceback'ini yazar.

**Doğrulama**
- İlk çalıştırma (geçici `ci-setup` dalı): iki iş de yeşil. `checks` 1 dk 14 sn, `tests` 2 dk 11 sn.
  - Örnek modül kuruldu, 1 test, `RESULT: OK`. gitleaks: 13 commit, sızıntı yok. Rehber kopyası upstream'le aynı.
- Negatif deneme (geçici `ci-negative` dalı): bilerek başarısız testli `ov_ci_negative` modülü.
  - `tests` kırmızı: `FAIL: TestOvCiNegative.test_module_installed`, `RESULT: FAILED (1)`, traceback günlükte. `checks` yeşil (lint temiz).
  - Commit kancaları atlanmadı; lint hatalı commit yerel kanca tarafından zaten engellenir (T1.9 negatif denemesi).
- `check_secrets.py` negatif denemesi (yerel): `.env` değeri içeren geçici dosya staged iken hata verdi; dosya silindi.
- gitleaks yerelde de çalıştırıldı (Windows sürümü, sağlama doğrulandı): sızıntı yok.
- Önbellek: GitHub önbellekleri dala bağlı; iki geçici dal birbirinin önbelleğini göremedi. `main`'de oluşan önbellek bütün dallarda kullanılır. Önbelleksiz sığ upstream çekimi 20–50 sn.
- Geçici dallar `main`'e tek commit olarak alındı (squash) ve GitHub'dan silindi.

**Belgeler**
- CLAUDE.md (Ortam: CI; Komutlar: gizli bilgi denetimi, CI), ARCHITECTURE.md (§2 ağacı, §5 CI), PLAN.md (T1.10, pano), README.md (CI rozeti, durum), COMPLIANCE.md (gizli bilgi denetimi; §5 gitleaks, GitHub eylemleri, PostgreSQL imajı), state.json.

### Adım: Modül şablonu ve kod kalite araçları (T1.9) — otonom mesai 1

**Kod**
- `tools/new_module.py`: `addons/ov_<ad>/` iskeleti üretir.
  - Manifest: sürüm `20.0.1.0.0`, lisans `AGPL-3` (ya da `--license LGPL-3`), yazar, `security/ir.access.csv`.
  - `README.rst`, boş `models/`, yalnız başlık satırlı `security/ir.access.csv`, `i18n/tr.po` başlığı, kurulumu doğrulayan ilk test (`post_install`).
- `tools/check_modules.py`: proje kuralları, yalnız standart kütüphane.
  - `ov_` öneki; lisans AGPL-3 veya LGPL-3 (D-016); sürüm `20.0.x.y.z`; yazar; `description` anahtarı yok.
  - Manifest adı, özeti ve README'de "Odoo" geçmez (D-007, D-014).
  - `README.rst`, `tests/test_*.py`, `i18n/tr.po` var. OCA portları kapsam dışı (D-019).
- `ruff.toml`: upstream `ruff.toml`'u genişletir. `upstream/`, `vendor/`, `ports/` hariç (portların lint düzeni T1.11'de); `tools/` için `print` serbest.
- `.pylintrc`: pylint-odoo'nun Odoo denetimleri (`disable=all`, `enable=odoolint`). Geçerli sürüm 20.0, izinli lisanslar AGPL-3 ve LGPL-3, zorunlu yazar.
- `.pre-commit-config.yaml`: ruff (v0.16.10), pylint-odoo (v10.0.12, yalnız `addons/`), modül kuralları, belge denetimi. Yerel depoda kanca kuruldu.
- `requirements-dev.txt`: `pylint-odoo==10.0.12`, `pre-commit==4.7.0`.
- `tools/pg.py`: iki `subprocess.run` çağrısına `check=False` (ruff PLW1510).

**Araştırma**
- Modül açıklaması: Odoo 20.0, manifestte `description` yoksa README'yi kullanır ve uzantısına bakmadan reStructuredText olarak işler (`ir_module.py`). Bu yüzden modül README'si `README.rst`; Markdown başlıkları ekranda düz metin görünürdü. pylint-odoo da `description` anahtarını eskimiş sayıyor.
- Manifestte `author` yoksa Odoo uyarı verip boş bırakıyor, `license` yoksa LGPL-3 varsayıyor. Şablonda ikisi de açıkça yazılı.
- T1.6'da not edilen 14 ruff bulgusu depo yapılandırması olmadan, ruff'ın kendi kurallarıyla bulunmuştu. Upstream kural setiyle yalnız ikisi geçerli (`pg.py`, PLW1510); düzeltildi.

**Doğrulama**
- Kabul: `python tools/new_module.py ov_sample` → `python tools/run_tests.py ov_sample`: modül kuruldu, 1 test, `RESULT: OK` (14 sn). Boş `ir.access.csv` sorunsuz yüklendi. `pre-commit run --all-files` temiz.
- `README.rst`, Odoo'nun docutils ayarlarıyla doğru başlık ve paragraf üretiyor; yönerge satırları HTML yorumu olarak kalıyor.
- Negatif denemeler:
  - lisansı `OPL-1`, sürümü `1.0`, yazarı yanlış, adı ve README'si "Odoo" içeren, SQL birleştiren modül: `check_modules.py` 8 sorun; pylint-odoo C8101, C8103, C8105, C8106, C8108, E8103;
  - pre-commit üzerinden: ruff (tek satırda çoklu import), pylint-odoo (lisans, sürüm) ve modül kuralları kancaları başarısız, commit engellenirdi.
- Örnek modül depoya girmedi; şablon CI'da üretilen örnek modülle denetlenecek (T1.10).

**Kullanıcıya soru**
- K12 (USER_TASKS): modüllerde yazar olarak görünecek ad. Varsayım `burak-sisci`.

**Belgeler**
- CLAUDE.md (Odoo geliştirme kuralları "Her modülde", Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 lint), PLAN.md (T1.9, pano, T1.10'a lint ve şablon adımları, §8), USER_TASKS.md (K12), COMPLIANCE.md §5 (pylint-odoo, pylint, pre-commit), README.md, state.json.

### Adım: Test çalıştırma komutları (T1.8) — otonom mesai 1

**Kod**
- `tools/run_tests.py`: modül testlerini temiz bir veritabanında çalıştırır ve günlüğü özetler.
  - `db init --force` ile test veritabanı (demo yok, `en_US`), ardından `-i <modüller> --test-enable --test-tags /<modül>`. `--reuse` veritabanını korur ve `-u` kullanır.
  - Testler ayrı HTTP portunda (8079): Odoo test modunda HTTP sunucusunu her zaman açıyor; geliştirme sunucusuyla çakışmaz.
  - Günlükteki `ERROR:`/`FAIL:` bloklarını ve `X failed, Y error(s) of Z tests` satırını okur.
  - Windows'ta test sınıflarının filestore temizliği hataları (traceback'te `_gc_file_store_unsafe` + `PermissionError` ya da `.__gc` dosyası `AssertionError`) ayrı sayılır, çıkış kodunu etkilemez. `setUpClass`'ta da çıkıyor; ilk sürüm yalnız `tearDownClass`'ı tanıyordu, düzeltildi.
  - Özet satırı yoksa (kurulum çöktü) hata sayılır.

**Ortam**
- Doğrulama:
  - `l10n_tr`: 3 test, hata yok, `RESULT: OK` (38 sn).
  - `account_edi_ubl_cii` (negatif deneme): 230 test, 3 failed + 29 error. 27'si Windows gc hatası (24 `tearDownClass`, 3 `setUpClass`). Kalan 5 gerçek hata: T1.2'deki çekirdek test hatası (`deferred_start_date`), satır açıklaması içe aktarma testi, PDF motoru olmadığı için 2 PDF üretim testi, gömülü PDF testinde `LocalBinaryFile` TypeError. Sonuç `RESULT: FAILED (5)`, çıkış kodu 1.

**Belgeler**
- CLAUDE.md Komutlar (test komutları), ARCHITECTURE.md (§2 ağacı, §5 yerel testler), PLAN.md (T1.8, pano, T1.9 kabulüne komut), README.md, state.json.

### Adım: Odoo AI rehberleri (T1.7) — otonom mesai 1

**Kod**
- `.claude/skills/`: upstream `skills/` klasörünün değiştirilmemiş kopyası (24 dosya): `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`, `odoo-review`, `odoo-git`. Yanında `LICENSE` (upstream kopyası) ve `SOURCE.md` (kaynak commit).
- `tools/sync_skills.py`: kopyalar; `--check` upstream'le farkı denetler (CI için). Windows'ta upstream çalışma kopyası CRLF olduğundan karşılaştırma satır sonundan bağımsız; kopyalar LF.

**Araştırma**
- Rehberlerin tamamı okundu; zararlı veya gizli talimat yok.
- Lisans: klasörde ayrı lisans dosyası yok; deponun LGPL-3 lisansı ve `COPYRIGHT` notu geçerli. Envantere yazıldı.
- Proje kurallarıyla çelişenler (CLAUDE.md'ye öncelik kuralı olarak yazıldı):
  - `odoo-git`: `[TAG] kapsam: özet` commit biçimi, rebase ve `--force-with-lease`. Yalnız upstream/OCA katkısında geçerli sayıldı.
  - `odoo-review`: değişikliğin Enterprise'daki "diğer yarısına" bakma adımı. Clean-room (D-006) gereği uygulanmaz.
  - `odoo-web-guidelines`: `patch()` Odoo içinde önerilmiyor, Odoo dışı kod için uygun; kendi modüllerimizde serbest.
  - `comments`: kod yorumları, kullanıcı metinleri ve commit mesajlarında yalnız ASCII noktalama. Markdown belgelerimiz kapsam dışı.

**Belgeler**
- CLAUDE.md:
  - Odoo geliştirme kuralları: rehberler ve öncelik kuralları; görünüm kalıtımı kuralı rehberle uyumlu yazıldı.
  - Eski metin: "görünüm kalıtımı XPath ile". Yeni metin: ada bağlı kalıtım (kısa `field` biçimi, gerekirse XPath), konuma göre asla. Neden: `odoo-guidelines` kısa biçimi tercih ediyor.
  - Komutlar bölümüne `tools/sync_skills.py` eklendi.
- ARCHITECTURE.md §2 ağacı, COMPLIANCE.md §5, PLAN.md (T1.7, pano, T1.10'a rehber denetimi), README.md, state.json.

### Adım: Odoo'nun yerelde çalıştırılması (T1.6) — otonom mesai 1

**Kod**
- `deploy/odoo.conf.example`: yerel geliştirme yapılandırma şablonu.
  - Addons yolu ARCHITECTURE §2 sırasıyla, glob kalıplarıyla (`vendor/oca/*`, `ports/oca/*`, `addon[s]`): henüz olmayan klasörler uyarısız atlanır.
  - Veri klasörü `OV_HOME/odoo-data`, `workers = 0`, yalnız `127.0.0.1`.
- `tools/odoo_conf.py`: şablondan depo kökündeki `odoo.conf`'u üretir (git'e girmez). Veritabanı bilgileri `.env`'den; veritabanı yöneticisi ana şifresi ilk çalıştırmada `.env`'ye üretilir (`ODOO_ADMIN_PASSWD`).
- `ruff check tools/` (henüz depo yapılandırması yok, 0.16 varsayılanları): `odoo_conf.py` temiz; `check_docs.py` ve `pg.py`'de 14 bulgu (çoğu `re.M` → `re.MULTILINE`). Lint yapılandırmasıyla birlikte T1.9'da ele alınır.

**Ortam**
- Demo veritabanı `ov_demo`: `odoo-bin db init --with-demo --language tr_TR --country TR` (20 sn), ardından `-i account,l10n_tr` (37 sn).
- Günlükte tek uyarı: `markdown2` kurulu değil. Upstream'in hiçbir bağımlılık dosyasında yok; posta eklerinde markdown gösterimi için isteğe bağlı.
- Kabul:
  - giriş sayfası Türkçe (`Giriş`, `Şifre`, `E-posta`); admin oturumu `tr_TR`, `Europe/Istanbul`;
  - başsız Chrome ile (geçici profil) fatura listesi ve hesap planı ekranları açıldı, JS hatası yok, başlıklar `Faturalar` ve `Hesap Planı`;
  - `TR Company`: ülke TR, para birimi TRY, hesap planı `tr` (ekranda 343 satır), 44 vergi, Türkçe yevmiyeler (`Satışlar`, `Satınalma`, `Banka`, `Kasa` …), 1.046 vergi dairesi.
- Upstream demo düzeni: ana şirket (`YourCompany`, ülke TR) genel hesap planıyla ve USD ile gelir; Türk hesap planı ayrı demo şirketi `TR Company`'de. Kendi demo verimiz (T8.3) Türk şirketiyle başlayacak.

**Araştırma**
- PDF motoru: 20.0'da eklentili.
  - `base_report_wkhtmltox` kendiliğinden kurulur, ama wkhtmltopdf GitHub deposu arşivde (son push 2022-11-22).
  - `base_report_paper_muncher` Odoo'nun yeni motoru (LGPL-3, son sürüm v0.9.0, 2026-10-06); yalnız Linux paketleri var.
  - Yerelde kurulmadı; seçim T2.5'e not edildi.
- `l10n_tr` veri kalitesi gözlemleri T3.1'e not edildi: Türkçe büyük harf hatası, İngilizce kalan hesap ve vergi adları, çevrilmemiş sütun başlığı.
- Marka: giriş sayfasının başlığı `Odoo` (T2.2 kapsamında).

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 yerel Odoo), PLAN.md (T1.6, pano, T2.5 ve T3.1 notları), README.md, state.json.
- ARCHITECTURE §2 ağacında T1.3'te eklenen `tools/pg.py` eksikti; eklendi.

### Adım: Python sanal ortamı (T1.5) — otonom mesai 1

**Kod**
- `requirements-dev.txt` eklendi: upstream `requirements.txt`'yi içerir (`-r upstream/odoo/requirements.txt`), üstüne `ruff==0.16.10` (upstream `ruff.toml` 0.16 için yazılmış) ve `websocket-client==1.9.2` (HttpCase tarayıcı testleri `odoo/tests/common.py` içinde `websocket` içe aktarıyor).

**Ortam**
- Depoda `.venv` (Python 3.12.10, git'e girmez). Kurulum: `pip install --prefer-binary -r requirements-dev.txt`; `pip check` temiz.
- Kabul: `odoo-bin --version` → `Odoo Server 20.0`.
- Windows'ta upstream işaretleri yüzünden `gevent`, `greenlet`, `python-magic`, `python-ldap` kurulmaz. Yerel geliştirme iş parçacıklı sunucuyla yapılır; gevent/çok süreçli mod ve LDAP Linux'ta (CI, üretim) sınanır.

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md §5, COMPLIANCE.md §5 (ruff MIT, websocket-client Apache-2.0, upstream Python bağımlılıkları notu), PLAN.md (T1.5, pano, T8.4'e lisans dökümü notu), README.md, state.json.

### Adım: Upstream Odoo submodule (T1.4) — otonom mesai 1

**Kod**
- Odoo 20.0 Community `upstream/odoo` altına sığ git submodule olarak eklendi. Sabit commit `afbcf79d` (2026-10-18), T1.2 denemesinin yapıldığı commit.
  - `.gitmodules`: `branch = 20.0`, `shallow = true`, adres GitHub.
  - İndirme süresini kısaltmak için ilk klon yerel inceleme kopyasından alındı, sonra adres GitHub'a çevrildi (`git submodule set-url`, `sync`).
  - Kabul: depo temiz bir klasöre klonlandı; `git -c core.longpaths=true submodule update --init --depth 1` GitHub'dan sabit commit'i sığ olarak getirdi, çalışma ağacı temiz.
  - İlk deneme `-c core.longpaths=true` olmadan "Filename too long" ile düştü: süper depodaki `core.longpaths` ayarı alt modülün klonuna geçmiyor. CLAUDE.md komutu buna göre yazıldı.
- Yerel depoda `core.longpaths` açıldı (Windows yol uzunluğu, R11).

**Belgeler**
- docs/COMPLIANCE.md §5: lisans envanterine ilk satır (Odoo Community 20.0, LGPL-3, değiştirilmedi).
- CLAUDE.md: "Ortam" (upstream durumu) ve "Komutlar" (yeni klonda submodule komutu).
- ARCHITECTURE.md §2: `upstream/odoo` satırı. README.md: durum.
- PLAN.md: T1.4 `[x]`; F1 4/11; toplam 12/114; şu anki görev T1.5.
- state.json: `upstream` (yol, commit, tarih, `in_project: true`); T1.4 bitenlere eklendi.

### Adım: Sürüm doğrulaması (T1.2) — otonom mesai 1

19.0'daki Nilvera ve OCA modülleri 20.0'da gerçekten kurulup test edildi. Üç ağaç ölçüldü: değişmemiş kod, Odoo'nun otomatik dönüştürücüsü (`upgrade_code`) ve elle uyarlama.

**Araştırma**
- Yeni: `docs/research/nilvera-port.md`. Sonuçlar:
  - 19 modülden 18'i 21 tür küçük uyarlamayla kuruluyor; 268 testin 243'ü geçiyor. Elle değişiklik 36 dosya, +96/−145 satır.
  - Otomatik dönüştürücü tek başına 2/19 modülü kurulabilir yapıyor; Windows'ta düzgün çalışmıyor (yol ayırıcı, kodlama).
  - En büyük kalan kalem `account_financial_report`: 20.0'da `account.group` modeli yok (T5.4).
  - Gerçek davranış farkı: `is_company` artık vergi numarasından hesaplanıyor; Türkiye'de 11 haneli TCKN gerçek kişi sayılmalı (T4.3).
  - Kalan ek emek yaklaşık 9–15 oturum; mevcut port görevlerinin içinde.
  - 20.0 taze: Community çekirdeğinde UBL içe aktarma hatası (`deferred_start_date`) görüldü.
  - Windows'ta 20.0 test temizliği salt okunur filestore dosyalarını silemiyor; referans test ortamı Linux CI.
  - OCA geçiş gecikmesi (17.0–19.0): altyapı modülleri 0–3 ay, banka mutabakatı, cari ekstre ve kalite 4–14 ay.

**Kararlar**
- **D-011** Geçerli kaldı (**20.0**). Gerekçesine ölçüm sonucu eklendi; kabul edilen bedele `account_financial_report` ve 20.0'ın tazeliği eklendi.
  - Eski "Yeniden değerlendirme" satırı: "T1.2. İlk tahmin, MVP'nin OCA modülüne ihtiyacı olmadığı varsayımına dayanıyordu. D-018 ile bu varsayım değişti. Port maliyeti, upstream eklenmeden önce ölçülür. 20.0'ın maliyeti çok yüksek çıkarsa 19.0 seçeneği yeniden açılır."
  - Yeni hali: planlı nokta yok; yalnız 20.0 çekirdeğinde MVP'yi engelleyen, modülle aşılamayan ve upstream'de üç ay içinde düzelmeyen bir hata olursa yeniden açılır.
  - Neden: port maliyeti ölçüldü ve küçük çıktı. 19.0'da kalmak işi yalnız Eylül 2028'deki zorunlu göçe erteliyor.

**Belgeler (düzeltme)**
- Planlama adımındaki "`mis_builder`, `mis_builder_budget` ve `queue_job` 20.0'da var" bilgisi yanlıştı. Bu modüller OCA'nın 20.0 dalında yalnız yer tutucu (`installable: False`, sürüm 19.0).
  - Eski metin (planning-inputs.md §1): "`mis_builder`, `mis_builder_budget` | mis-builder | **var** | var | Doğrudan `vendor/` (T5.5)" ve "`queue_job` | queue | **var** | var | Gerekirse doğrudan `vendor/`".
  - Eski metin (PLAN.md T5.5): "OCA `mis_builder` (20.0'da mevcut) ile Tekdüzen şablonları".
  - Eski metin (MODULE_MATRIX.md): bilanço satırı "OCA (20.0 resmî)", bütçe satırı "`mis_builder_budget`, 20.0'da var".
  - Neden: o sayım OCA dallarındaki klasörlere bakıyordu; kurulabilirlik denetlenmemişti. Düzeltilen yerler: planning-inputs.md §1 (düzeltme notu ve tablo), MODULE_MATRIX.md (not ve iki satır), PLAN.md T5.5.
  - Ayrıca `account_statement_base`'in deposu düzeltildi: bank-statement-import değil, account-reconcile.
- PLAN.md: T1.2 `[x]`; F1 3/11; toplam 11/114; şu anki görev T1.4. R1 riski ölçüme göre güncellendi (olasılık D, etki O). T1.8, T4.3, T5.4 ve T5.5'e T1.2 bulguları eklendi.
- ARCHITECTURE.md: D-011 "T1.2'de doğrulandı". README.md: durum ve sıradaki görev.
- state.json: T1.2 bitenlere eklendi; şu anki görev T1.4; D-011'den `revisit` kaldırıldı; belge listesine `nilvera-port.md`.

### Adım: PostgreSQL kurulumu (T1.3) — otonom mesai 1

Otonom mesai 1 başladı (D-021). T1.3, T1.2'den önce yapıldı: T1.2'deki port denemesi (19.0 modüllerini 20.0'da kurup test etmek) çalışan bir PostgreSQL gerektiriyor.

**Ortam**
- PostgreSQL 18.6 kuruldu. Yönetici izni gerektirmeyen yol: EDB'nin Windows taşınabilir ikili zip'i, depo dışında `%LOCALAPPDATA%\odoo-version` (`OV_HOME`) altında.
  - Küme: UTF-8, `C.UTF-8` yerleşik yerel ayar, scram-sha-256 kimlik doğrulama, yalnız `localhost:5432`.
  - Sunucu kullanıcı hesabında çalışır. Windows hizmeti değildir; bilgisayar yeniden başlayınca `python tools/pg.py start` gerekir.
  - Rol `odoo` (LOGIN CREATEDB). Bağlantı bilgileri depodaki `.env` dosyasında (git'e girmez, D-015).
  - Kabul doğrulandı: `psql --version` 18.6; `odoo` rolüyle bağlantı kuruldu.
- Sürüm seçimi 18: Odoo 20.0'ın alt sınırı 16 (`odoo/release.py`); 18, CI ve olası Ubuntu sunucusunun paket sürümleriyle uyumlu.
- T1.2 için depo dışında inceleme kopyaları indirildi (`OV_HOME/src`): Odoo 20.0 (sığ klon, `afbcf79`), Odoo 19.0'ın yalnız `l10n_tr*` modülleri, ilgili OCA depolarının 19.0 ve 20.0 dalları.

**Kod**
- Yeni: `tools/pg.py` — yerel kümenin kurulumu ve yönetimi (`init`, `start`, `stop`, `status`).
  - Sunucu, çağıranın çıktı kanallarını devralmayacak biçimde başlatılır. Aksi halde çıktıyı bekleyen kabuk sunucu kapanana kadar takılıyordu (ilk denemede görüldü).

**Belgeler**
- PLAN.md: T1.3 `[x]`; F1 2/11; toplam 10/114.
- CLAUDE.md: "Ortam" (PostgreSQL) ve "Komutlar" (`tools/pg.py`).
- ARCHITECTURE.md §5: yerel PostgreSQL düzeni.
- docs/COMPLIANCE.md §5: depoya girmeyen geliştirme araçları tablosu; PostgreSQL satırı.
- state.json: `environment.postgresql`, T1.3 bitenlere eklendi.

### Adım: commit yazarlığı, kullanıcı belgesi, mesai türleri ve görev kategorileri

Kullanıcı istekleri:
- GitHub'da tek katkıcı kullanıcı olacak; Claude ortak yazar olarak yazılmayacak. Kural CLAUDE.md'ye girecek.
- Kullanıcıdan beklenenler için ayrı bir belge.
- İki mesai türü: standart (birlikte) ve otonom (Claude tek başına, kullanıcı ekran başında değil).
- Görevlerin tümü üç kategoride: kullanıcının yapacakları, birlikte yapılacaklar, Claude'un yapacakları.

**Kararlar**
- **D-015** güncellendi. Eski hali: commit yazarlığı hakkında kural yoktu; ilk iki commit'e `Co-Authored-By: Claude` satırı eklenmişti. Yeni hali: commit yazarı kullanıcının git kimliği; Claude'u yazar veya ortak yazar gösteren satır yazılmaz. Neden: kullanıcı bunu hata olarak bildirdi. Geçmiş iki commit'in temizlenmesi force-push gerektirdiği için kullanıcı kararına bırakıldı (USER_TASKS K10).
- **D-003** güncellendi. Eski hali: mesai türleri yoktu. Yeni hali: çalışma standart ve otonom mesailerle yürür; otonom mesaide sorular `USER_TASKS.md`'ye yazılır.
- **D-021** yeni, Geçerli: mesai türleri ve görev kategorileri (K / B / C); otonom mesai kuralları. Mesai türleri ve kategoriler kullanıcıdan, otonom kuralların ayrıntısı Claude'dan.

**Belgeler**
- Yeni: **`USER_TASKS.md`** — kullanıcı eylemleri, kararları ve onayları; K ve B görevlerinde kullanıcının payı; mesai türleri özeti.
  - PLAN.md §10'daki K1–K5, K8, K9 buraya taşındı.
  - K6 (müşteri listesi) ve K7 (yasal yapı) kaldırıldı; aynı işi anlatan T9.1 ve T9.3 görevleri kullanıldı.
  - Yeni: K10 (geçmiş commit'lerdeki ortak yazar satırı), K11 (`Claude-Session:` satırı).
- PLAN.md:
  - "Sorumlu" alanı "Kategori" oldu: C+K → **B**; K ve C aynı.
  - T10.4 C → B (ödeme sağlayıcısı hesabı kullanıcıda).
  - Yeni görev **T7.9 Kullanıcı kabul turu** (B). F7 kabulündeki elle tur bu göreve bağlandı. Toplam 113 → 114 görev.
  - Panoya "K · B · C" sütunu ve toplam satırına kategori sayıları eklendi: Kullanıcı 3 · Birlikte 13 · Claude 98.
  - T1.3: "gerekirse kullanıcıdan yönetici izni" yerine yönetici izni gerektirmeyen kurulum yolu.
  - §10 artık `USER_TASKS.md`'ye yönlendiriyor.
- CLAUDE.md: kural 8 (commit yazarlığı); "Mesai türleri" bölümü; belge haritasında `USER_TASKS.md`; protokol adım 3 ve 8.
- state.json: `session` alanı (otonom mesai 1), `project.user_tasks`, `project.commit_author`, D-021, belge listesinde `USER_TASKS.md`.
- README.md, ARCHITECTURE.md: `USER_TASKS.md` eklendi.
- `tools/check_docs.py`: görev kategorisi denetimi (K/B/C); panodaki ve toplam satırındaki kategori sayıları; `USER_TASKS.md`'deki K/B görev listesinin ve işaretlerinin PLAN ile aynılığı; tanımsız `K<n>` atıfları.

### Adım: detaylı planlama (T0.8)

Kullanıcı D-016'yı onayladı ve planlama kararlarını Claude'a bıraktı. Verdiği perspektif şöyle:
- öğrenci projesi, sıfır bütçe;
- bütçesiz, desteksiz ve müşterisiz alınabilecek tüm ilerleme alınınca müşteri arayışı;
- ilk müşteriler küçük işletmeler ve orta ölçekli fabrikalar; her satıştan sonra bir üst ölçek.

**Kararlar**
- **D-016** Açık → **Geçerli: AGPL-3.**
  - Eski hali: seçenekler A (AGPL-3) / B (LGPL-3) / C (kapalı) / D (karma), Claude önerisi "A, gerekirse D"; karar noktası T2.2.
  - Neden: kullanıcı öneriyi onayladı; depo ileride private yapılabilir, şimdilik AGPL-3.
  - Eklenenler: depo kökünde `LICENSE`; LGPL türevleri LGPL-3; OCA portları orijinal lisansla; private'a geçişin sınırları; dış katkı şimdilik kabul edilmiyor.
- **D-011** (20.0 kaldı, gerekçe ve tetikleyici değişti).
  - Eski metin: "MVP'nin (P0) hiçbir OCA modülüne ihtiyacı yok." Yeniden değerlendirme T3.1 (Nilvera port analizi). Submodule T1.3'te.
  - Yeni hali: bu varsayım D-018 ile geçersiz kaldı (mali raporlar, mutabakat, ekstre, kalite modülleri OCA'da yalnız 19.0'da). Yeniden değerlendirme **T1.2**: port maliyeti upstream eklenmeden önce ölçülür. Submodule T1.4'te. Gerekçeye "ilk müşteriler büyük olasılıkla 2027'de" eklendi.
- **D-012** (kullanıcının onayladığı kapsam genişletildi).
  - Eski metin: "MVP kapsamı: e-Fatura + e-Arşiv. e-İrsaliye MVP sonrası (P1), e-Defter ileride." Yeniden değerlendirme T6.1.
  - Yeni hali: MVP = e-Fatura + e-Arşiv + **e-İrsaliye** (P0). e-Defter P1 (T11.4); MVP'de mali müşavire aktarım (T5.9). Diğer e-Belgeler P3. Mimariye sahte (mock) adaptör eklendi. Yeniden değerlendirme **T8.1**.
  - Neden: hedef segmentteki orta ölçekli fabrikalar için e-İrsaliye zorunlu (e-Fatura mükellefi ve hasılat ≥ 10 Milyon TL); sevkiyat ve fason üretim e-İrsaliye gerektiriyor.
- **D-013** (Ertelendi kaldı, kapsamı daraldı).
  - Eski başlık: "Barındırma ve dağıtım modeli". Karar noktası T6.3.
  - Yeni başlık: "**Üretim barındırma yeri**". Teslim biçimi D-018'e taşındı. Karar noktası **T9.5**. "İlk müşteri on-prem seçerse daha da ertelenebilir" eklendi.
- **D-014**: yeniden değerlendirme T6.1 → **T8.1**; kalıcı adın uygulanması T8.2. OCA portları için teknik ad istisnası eklendi (D-019).
- **D-017** yeni, Geçerli: hedef müşteriler ve aşama stratejisi; müşteri arayışı kapısı M8. Yeniden değerlendirme T9.8.
- **D-018** yeni, Geçerli: MVP tanımı (Ticaret ve Üretim paketleri), öncelik tanımları (P0–P5), MVP dışı liste, teslim biçimi (yönetilen kurulum; self-servis SaaS F10). Yeniden değerlendirme T8.1.
- **D-019** yeni, Geçerli: OCA modülleri — resmî 20.0 `vendor/oca/`, yoksa 19.0'dan port `ports/oca/` (orijinal ad, lisans ve yazarlar).
- **D-020** yeni, Geçerli: ücretsiz altyapı — GitHub Actions, GitHub Pages (yalnız açık kaynak belgeler), Cloudflare Quick Tunnel (demo), Nilvera test portalı, Student Pack (isteğe bağlı).
- Küçük metin güncellemeleri:
  - **D-002:** "İlk satışa çıkan kapsam D-018'dedir" eklendi.
  - **D-005:** "Ücretsiz kaynaklar D-020'de" eklendi.
  - **D-008/3** eski metin: "AGPL-3 OCA modülleri ayrı tutulur. Değiştirilirse, SaaS kullanıcılarına değiştirilmiş kaynak sunulur." Yeni hali: 20.0 portları da (D-019) bu kapsamda.
  - **D-008/4** eski metin: "Kapalı kaynak (kendi lisansımızla) modüllerimiz AGPL modüllere bağımlı olamaz. Kapalı modül olup olmayacağı D-016'ya bağlı." Yeni hali: şu an kapalı modül yok; kendi modüllerimiz AGPL-3.
  - **D-008/5** eski metin: "her 3. parti modül". Yeni hali: "her 3. parti kod ve veri".
  - **D-010:** OCA portlarının yeri (`ports/`) eklendi.
  - DECISIONS.md giriş notu: tetikleyiciler artık "ROADMAP görevine" değil, "PLAN.md'deki bir göreve" bağlanır.

**Belgeler**
- `ROADMAP.md` → **`PLAN.md`** (yeniden adlandırıldı ve baştan yazıldı). İçerik:
  - ilerleme panosu;
  - strateji, paketler ve Türkiye gereksinimleri;
  - 12 faz (F0–F11), 113 görev; her görevde büyüklük, sorumlu ve kabul ölçütleri;
  - sürekli işler, ücretsiz kaynaklar, test stratejisi, risk kaydı, kullanıcı eylemleri (K1–K9).
- Eski → yeni görev numaraları:
  - eski T0.8 → T0.8 (tamamlandı);
  - eski T1.2–T1.7 → T1.3, T1.4, T1.5, T1.6, T1.7, T1.8; yeni T1.2 (sürüm doğrulaması), T1.9 (modül şablonu ve lint), T1.10 (CI), T1.11 (`vendor/` ve `ports/`);
  - eski T2.1–T2.4 → aynı numaralar; yeni T2.5–T2.7;
  - eski Faz 3 (e-Belge) → F4: eski T3.1 → T4.1, T3.2 → T4.3, T3.3 → T4.5, T3.4 → T4.6, T3.5 (e-İrsaliye, P1) → T4.8 (P0); eski T3.6 (SMS) → T11.5. Yeni F3: Türkiye temel yerelleştirmesi;
  - eski Faz 4 (Enterprise eşdeğerleri) → F5 (muhasebe P0 kısmı), F11 (T11.1 sabit kıymet, T11.10–T11.12 P2–P4 paketleri);
  - eski Faz 5 (SaaS) → F10 (T10.1–T10.7); eski T5.3 yedekleme → T8.5 (yönetilen kurulum için) + T10.5;
  - eski T6.1 → T8.1, T6.2 → T9.4, T6.3 → T9.5, T6.4 → T9.6.
- `LICENSE` eklendi (GNU AGPL v3, gnu.org resmî metni).
- DECISIONS.md: yukarıdaki kararlar; özet tablo; "Açık kararlar" bölümü boşaldığı için kaldırıldı.
- state.json: faz F1, şu anki görev T1.2; T0.8 tamamlandı; lisans, plan, hedef segmentler ve kilometre taşları; karar değerleri ve tetikleyicileri; `modules.ported`; yeni belge `docs/research/planning-inputs.md`.
- CLAUDE.md: proje özeti (paketler, lisans), belge haritasında PLAN.md, protokol 8 adım (PLAN işaretleri ve pano), kurallar 3–5 ve 7, ortam ve komutlarda yeni görev numaraları.
- README.md: durum, paketler, PLAN bağlantısı, lisans ve katkı bölümleri.
- ARCHITECTURE.md: durum notu, `vendor/` + `ports/` düzeni (D-019), modül tablosunda lisans sütunu ve yeni satırlar, teslim biçimi (D-018), geliştirme ortamı ve CI bölümü.
- docs/COMPLIANCE.md: lisans satırları AGPL-3; görev atıfları (T9.4, T8.2, T2.3, T2.7, T1.4); public depo kuralları (Nilvera bilgileri, GİB paketleri, CI gizli bilgi taraması, depo lisansı).
- docs/MODULE_MATRIX.md: yeni öncelik tanımları ve Paket sütunu; öncelikler paketlere göre yeniden belirlendi (ör. mrp, fason, bakım P0; e-İrsaliye P0; POS P2).
- docs/research/e-fatura.md: sonuç notu (e-İrsaliye MVP'de, e-Defter P1); §5 değerlendirme tablosu; yeni §6 "Planlama için ek bulgular"; kaynaklar; görev atıfları T6.1/T6.2 → T8.1/T9.4.
- docs/research/hosting.md: D-013'ün yeni başlığı ve kapsamı; Quick Tunnel sınırları; on-prem satırı (D-018); görev atıfları T6.2/T6.3 → T9.4/T9.5.
- docs/research/approach-b-vs-c.md: "ROADMAP T2.4" → "PLAN T2.4".
- Yeni: docs/research/planning-inputs.md (OCA 20.0 durumu, çeviri kapsamı, yerel 20.0 kontrolleri, ücretsiz kaynaklar, veri kaynakları, pazar referansları).
- `tools/check_docs.py`: ROADMAP yerine PLAN.md; yinelenen görev numarası, faz başlığı işaretleri, pano satırları, toplam satırı, "Şu anki görev" satırı ve `phase.id` denetimleri.

**Araştırma**
- OCA 20.0: `l10n-turkey` 18.0/19.0/20.0'da boş. Muhasebe, mutabakat, ekstre, kalite, MRP planlama ve sabit kıymet modülleri yalnız 19.0'da; `mis_builder`, `queue_job`, `remove_odoo_enterprise` 20.0'da var.
- 20.0 Türkçe çeviri kapsamı ölçüldü: çekirdek modüller %79–93; `l10n_tr` %33.
- Ücretsiz kaynakların koşulları: GitHub Actions, GitHub Pages (ticari kullanım yasağı), Cloudflare Quick Tunnel sınırları, Student Pack, TÜBİTAK 2209-A (son başvuru 11 Kasım 2026).
- e-Belge: Nilvera kamuya açık test ortamı; GİB doğrudan testi mali mühür gerektiriyor; 2026 UBL-TR paket güncellemeleri; Ba-Bs formlarının Eylül 2024'ten itibaren kaldırılması; e-Defter geçiş kuralı (ikincil kaynaklar).
- Veri kaynakları: TCMB günlük kur XML; il/ilçe listesi (MIT lisanslı aday).

### Adım: kullanıcı kararları (T0.7) ve git/GitHub deposu (T1.1)

**Kararlar**
- **D-010** Açık → Geçerli: **B** (kullanıcı). Eski hali: seçenekler B / C / B+, Claude önerisi B+. Neden: kullanıcı yama kuyruğu olmayan B'yi seçti; `patches/` kaldırıldı. Modülle çözülemeyen durum yeni karar olarak gelecek.
- **D-011** Açık → Geçerli: **20.0**. Eski hali: seçenekler 20.0 / 19.0 / 18.0, öneri 20.0. Neden: kullanıcı kararı Claude'a bıraktı. Yeniden değerlendirme T3.1'e bağlandı.
- **D-012** Açık → Geçerli. Eski hali (öneri): e-Fatura + e-Arşiv MVP, özel entegratör API, Nilvera 19.0 port. Neden: kullanıcı kapsamı ve yöntemi onayladı ve "MVP sonunda tekrar ele alırız" dedi. Yeniden değerlendirme T6.1'e bağlandı.
- **D-013** Açık → **Ertelendi**. Eski hali (öneri): aşamalı SaaS (lokal → ücretsiz demo → Türkiye VPS; on-prem ileride). Neden: kullanıcı "hemen karar vermeli miyiz?" diye sordu. Cevap: hayır, gerçek müşteri verisine kadar gerekmiyor. Karar noktası T6.3. Geçici düzen: lokal geliştirme ve sağlayıcıdan bağımsız mimari.
- **D-014** Açık → Geçerli. Eski hali: marka adı ve önek belirlenmemiş. Neden: kullanıcı çalışma adını `odoo-version` olarak verdi (MVP sonunda değişecek). Claude öneki markadan bağımsız ve kalıcı `ov_` olarak seçti. Yeniden değerlendirme T6.1.
- **D-015** Açık → Geçerli. Eski hali (öneri): yerel git, push yalnız onayla. Neden: kullanıcı public GitHub deposu ve her görev sonunda commit + push istedi; push önceden onaylı hale geldi.
- **D-016** yeni, Açık: kendi modüllerimizin lisansı. Neden: public depo, kod yayımlanmadan önce lisans seçimini gerektiriyor. Öneri AGPL-3 (+ gerekirse private depo). Karar noktası T2.2.
- **D-003** güncellendi. Eski metin: "dışa dönük işlemler (yayınlama, paylaşma, uzak depoya push)" kullanıcıya sorulur. Yeni hali: proje deposuna push D-015 ile önceden onaylı; yayınlama, paylaşma ve depo ayarları yine sorulur.
- **D-008/1** güncellendi. Eski metin: "Upstream Odoo Community (LGPL-3) değiştirilirse değişiklikler LGPL-3 kalır." Yeni hali: upstream değiştirilmez (D-010). Madde 4'e D-016 bağlantısı eklendi.
- Karar durumlarına **Ertelendi** eklendi. `**Karar noktası:**` ve `**Yeniden değerlendirme:**` satırları ROADMAP görevlerine bağlandı.

**Belgeler**
- DECISIONS.md yeniden yazıldı (yukarıdaki kararlar).
- ROADMAP.md:
  - T0.7 ve T1.1 tamamlandı.
  - Yeni T0.8: detaylı planlama.
  - Faz 6 yeniden numaralandı. Yeni T6.1 MVP sonu değerlendirmesi; eski T6.1 → T6.2 (hukuki inceleme), eski T6.2 → T6.3 (artık "Üretim barındırma kararı (D-013) ve üretim sunucusu"), eski T6.3 → T6.4.
  - T2.4 B'ye göre yeniden yazıldı.
  - Faz başlıklarındaki karar ön koşulları güncellendi.
- ARCHITECTURE.md:
  - Durum notu: B / 20.0 / `ov_` Geçerli.
  - `patches/` kaldırıldı.
  - Önek `ov_`; lisans sütunu D-016'ya bağlandı.
  - Konum ertelendi ve sağlayıcıdan bağımsızlık kısıtı eklendi.
  - `.gitignore` / `.gitattributes` eklendi.
- CLAUDE.md:
  - proje özeti;
  - protokol adım 3 (karar noktası görevleri) ve adım 7 (commit + push);
  - kurallar 2–7;
  - ortam (gh, git deposu) ve komutlar.
- COMPLIANCE.md: kendi modüllerimizin lisansı → D-016; çalışma adı ve marka notu; public depo kuralları; T6.1 → T6.2.
- MODULE_MATRIX.md: "Karar verilecek" lisanslar → D-016; AGPL notu.
- research/approach-b-vs-c.md, research/e-fatura.md: başa "Sonuç" notu eklendi; T6.1 → T6.2.
- research/hosting.md:
  - "Sonuç", "Karar ne zaman gerekli?" ve "Benzer platformlar nerede çalışıyor?" bölümleri eklendi;
  - "Öneri" başlığı "Ön öneri" oldu;
  - T6.1 → T6.2.
- README.md: durum, çalışma adı, lisans notu.
- `tools/check_docs.py`:
  - "Ertelendi" durumu;
  - ertelenmiş kararda karar noktası zorunluluğu;
  - karar noktası veya yeniden değerlendirme görevi tamamlanmışsa hata;
  - belgelerde (CHANGELOG hariç) ROADMAP'te olmayan görev numarasına atıf denetimi.

**Araştırma**
- Benzer platformların barındırma yerleri incelendi:
  - Odoo Online / Odoo.sh: OVHcloud, Google Cloud, AWS; Türkiye bölgesi yok.
  - Frappe Cloud: AWS ve Oracle Cloud; Türkiye bölgesi yok.
  - Paraşüt aydınlatma metni: yurt dışı aktarım açık rızayla.
  - Logo: Cloud + Edge karma modeli.

**Ortam**
- Git deposu başlatıldı (`main`), `.gitignore` ve `.gitattributes` eklendi.
- Public GitHub deposu oluşturuldu: https://github.com/burak-sisci/odoo-version

### Adım: ilk belgeler (T0.1–T0.6)

**Kararlar**
- Geçerli olarak eklendi: D-001 ürün hedefi, D-002 kapsam, D-003 ekip/çalışma modeli, D-004 dokümantasyon protokolü (kullanıcı); D-005 sıfır bütçe (kullanıcı, 2026-10-16); D-006 clean-room, D-007 marka, D-008 lisans uyumu (hukuki zorunluluk); D-009 dil (Claude varsayılanı).
- Açık olarak eklendi (Claude önerileriyle): D-010 yaklaşım (öneri B+), D-011 sürüm (öneri 20.0), D-012 e-Belge stratejisi, D-013 barındırma, D-014 marka adı/önek, D-015 git/commit yetkisi.

**Araştırma**
- B / C yaklaşım karşılaştırması (marka izleri envanteri, Flectra örneği).
- e-Fatura / e-Arşiv / e-İrsaliye: GİB 509 Tebliğ güncel metni (589 değişiklikleri dahil) incelendi. Önemli bulgu: 1/1/2026'dan itibaren bilanço esaslı mükellefler tutardan bağımsız e-Arşiv/e-Fatura düzenlemek zorunda.
- Odoo 20.0'da Nilvera e-Belge modüllerinin Enterprise'a taşındığı, 19.0'da LGPL olduğu doğrulandı.
- OCA modül sayıları 18.0 / 19.0 / 20.0 dalları için çıkarıldı; OCA lisans örnekleri (çoğu AGPL-3).
- Barındırma seçenekleri; KVKK m.9 (7499 sayılı Kanun) ve e-Belge yurt içi saklama kuralı.

**Belgeler**
- Oluşturuldu: CLAUDE.md, README.md, ARCHITECTURE.md, DECISIONS.md, ROADMAP.md, CHANGELOG.md, state.json, docs/COMPLIANCE.md, docs/MODULE_MATRIX.md, docs/research/{odoo-analysis, approach-b-vs-c, e-fatura, hosting}.md.
- Belge tutarlılık denetimi eklendi: `tools/check_docs.py`.

## 2026-10-16

**Araştırma**
- Odoo 20.0 Community kaynak kodu indirildi ve incelendi (commit `1740e969`): 657 modül, 34 uygulama, tamamı LGPL-3; mimari, ORM, web istemcisi, `skills/` klasörü.
- Lisanslar (Community LGPL-3, Enterprise özel lisans) ve edinme yolları (sıfırdan klon / Community + modüller / çatal / kendi küçük ERP'miz) değerlendirildi.
