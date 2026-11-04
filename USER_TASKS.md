# Kullanıcıdan Beklenenler

Son güncelleme: 2026-11-04
İlgili kararlar: D-003, D-015, D-021

Bu belge, **kullanıcının yapması, karar vermesi veya onaylaması gereken her şeyin** tek listesidir.
- Otonom mesaiden dönünce ilk bakılacak yer burası (§1). Mesainin özeti CHANGELOG.md'de.
- Claude otonom mesaide soru soramaz. Soruları ve onay bekleyen işleri buraya yazar, kendi yapabileceği işlere devam eder (D-021).
- İşaretler: `[ ]` bekliyor · `[x]` tamam · `[-]` vazgeçildi.
- Görev kategorileri (D-021): **K** kullanıcının yapacakları · **B** birlikte yapılacaklar · **C** Claude'un yapacakları. Tam liste ve sayılar PLAN.md'de.

## 1. Şimdi bakılacaklar

Öncelik sırasıyla. Hiçbiri Claude'un işini durdurmuyor.

1. **K2: TÜBİTAK 2209-A için son başvuru 11 Kasım 2026.** Başvurmak istiyorsan danışman bulmak zaman alır.
2. **K1:** GitHub Student Developer Pack başvurusu. Onay süreci uzayabildiği için erken başvurmak iyi olur.
3. **K9:** GitHub güvenlik özellikleri (ücretsiz). Onay verirsen Claude açar.
4. **K12:** modüllerde yazar olarak görünecek ad. Şimdilik `burak-sisci`; marka belirlendiği için `Nexus` seçeneği öne çıktı.
5. **K14:** ürünün rengi ve simgesi. Ad artık Nexus; renk ve simge yer tutucu olarak varsayıldı.
6. **K15:** yayıncının çevrim içi hizmet modülleri (IAP, Aboneliğim) kaldırıldı. SMS ve iş ortağı otomatik tamamlama da bu yüzden yok.
7. **K18:** PDF motoru önerisi: üretimde wkhtmltopdf, Paper Muncher CI'da denenir. Kurulum T3.7'de; o zamana kadar karar verebilirsin.
8. **K19:** metinlerdeki eski ürün adı, kayıtlı metinler değiştirilmeden gösterimde değiştiriliyor. Botun e-posta adresi örnek bir adres; yayıncının destek masasına yönlendiren cümleler çıkarıldı.
9. **K20:** Türk hesap planında bazı hesap eşlemeleri varsayımla yapıldı (stopaj 360'a, erken ödeme indirimi 611/649, kasa farkı 679/689). Üç eşleme mali müşavire sorulmalı.
10. **K21:** TCKN'li iş ortağı (şahıs şirketi dahil) gerçek kişi sayılıyor; MERSİS numarasında yalnız 16 hane denetleniyor.
11. **K22:** ilçe listesi açık lisanslı bir veri seti yerine İçişleri Bakanlığı'nın resmî envanterinden alındı. Merkez ilçelerin adı "Merkez"; il zorunlu, posta kodu isteğe bağlı.
12. **K23:** TCMB kurları kendiliğinden alınıyor. Varsayılan döviz alış; bir bülten ertesi günden başlayarak uygulanıyor (önceki iş gününün kuru). Mali müşavire K20 ile birlikte sorulabilir.
13. **K4:** örnek banka ekstreleri. Hangi bankalar, hangi işlemler, nasıl anonimleştirileceği ve araştırma soruları K4'te.
14. **K24:** Türkçe çeviri eksikleri ayrı bir modülle (`ov_i18n_tr`) tamamlanıyor; modül kurulurken hatalı upstream çevirilerinin yerine geçiyor. Terim tercihlerin varsa K24'e yazabilirsin.

Otonom mesai 4 bitti (2026-11-03). Özeti CHANGELOG.md'de, "Otonom mesai 4 — özet". Yeni maddeler: K22, K23.

## 2. Kullanıcı eylemleri, kararları ve onayları

Tür: **Eylem** (senin yapacağın iş) · **Karar** (seçim) · **Onay** (Claude hazırlar, sen izin verirsin).

- [ ] K1 **Eylem** — GitHub Student Developer Pack başvurusu (ücretsiz, öğrenci doğrulaması).
  - Ne için: alan adı, bulut kredisi, geliştirici araçları (D-020).
  - Ne zaman: F8'den önce (T8.2 alan adı, T8.8 demo).
- [ ] K2 **Eylem (isteğe bağlı)** — TÜBİTAK 2209-A başvurusu.
  - 2026 çağrısında son başvuru: **11 Kasım 2026**.
  - Koşullar (danışman vb.) ve destek tutarı çağrı duyurusundan kontrol edilmeli; tutar doğrulanmadı (`docs/research/planning-inputs.md`).
  - Başvurmaya karar verirsen Claude standart mesaide proje önerisi taslağını hazırlar.
  - Plan bu desteğe bağlı değil (D-017).
- [x] K3 **Karar** — kalıcı marka adı: **Nexus** (kullanıcı, 2026-10-19; D-014). Tescil ve alan adı uygunluğu dış demodan önce araştırılır (T8.2, PLAN R17).
- [ ] K4 **Eylem (isteğe bağlı)** — örnek banka ekstreleri (T5.2 içe aktarma, T5.3 mutabakat).
  - Ne için: Türk bankalarının ekstre dosyalarını okuyan eşleme şablonları (T5.2) ve banka mutabakatı testleri (T5.3). Gerçek dosyanın düzeni (sütunlar, tarih ve tutar biçimi, karakter kodlaması, açıklama kalıpları) kurgusal dosyayla tahmin edilemez.
  - **En az:** 2 banka, her birinden 1 TL hesap, 1 ay, aşağıdaki "olmazsa olmaz" işlemlerle. Gerisi isteğe bağlı.
  - **Bankalar:** senin ve hedef müşterilerin kullandığı bankalar; ideali 4–5 banka. Kamu (Ziraat, Halkbank, VakıfBank), özel (İş, Garanti BBVA, Yapı Kredi, Akbank) ve bir katılım bankası (Kuveyt Türk gibi) karışık olursa iyi.
  - **Hesap:** öncelik ticari hesap (kurumsal internet şubesi), TL vadesiz. Varsa bir döviz hesabı (USD ya da EUR). Bireysel hesap da işe yarar ama dosya düzeni farklı olabilir; hangisi olduğunu not et.
  - **Dönem:** en az bir ay, bir ay sonunu kapsasın. Aynı hesaptan örtüşen iki dosya (ör. ayın 1–20'si ve 15–31'i) çift kayıt denetimi için iyi olur.
  - **Biçimler:** bankanın sunduğu her biçimden bir dosya: Excel (xlsx/xls), CSV/TXT; varsa MT940 ya da camt.053 (XML). PDF yalnız karşılaştırma için. İndirme ekranının (biçim seçenekleri) ekran görüntüsü de yararlı.
  - **İşlemler:** ekstrede bulunmasını istediklerim.
    - Olmazsa olmaz:
      1. Gelen havale/EFT/FAST (müşteriden tahsilat; açıklamada fatura numarası geçen varsa daha iyi).
      2. Giden havale/EFT/FAST (tedarikçiye ödeme).
      3. Banka masrafı ve komisyon; ayrı satırda BSMV.
      4. Kendi hesapların arasında virman.
      5. Nakit yatırma ya da çekme (şube veya ATM).
      6. Vergi ya da SGK ödemesi.
      7. Talimatlı ödeme (elektrik, telefon) ya da kredi kartı borcu ödemesi.
    - Varsa iyi olur:
      8. POS (üye işyeri) tahsilatı: blokaj çözülmesi, komisyon kesintisi.
      9. Çek: tahsile verilen müşteri çekinin takastan tahsili, kendi çekinin ödenmesi, karşılıksız çek (T5.7 için de).
      10. Senet tahsili.
      11. Faiz geliri ve stopajı; kredi taksiti; ek hesap (BCH/KMH) faizi.
      12. Döviz alım-satımı: TL ve döviz hesabı arasında, iki hesabın ekstresiyle.
      13. Toplu ödeme (maaş gibi). Kişisel veri yoğun; anonimleştirmesi zorsa atla.
      14. DBS (Doğrudan Borçlandırma Sistemi) ödemesi.
      15. İade ya da iptal edilmiş bir işlem.
      16. İşlem tarihiyle valör tarihi farklı bir işlem.
      17. Aynı gün aynı tutarda iki işlem.
  - **Anonimleştirme:** dosyayı bana vermeden önce. Ham dosya yalnız senin bilgisayarında kalır. Okuduğum dosyanın içeriği yapay zekâ hizmetine gider; karşı tarafların kişisel verileri bu yüzden önceden çıkarılmalı (KVKK).
    - Değiştir: karşı tarafın adı ve unvanı ("Müşteri A", "Tedarikçi B"), IBAN ve hesap numarası (aynı uzunlukta başka rakamlar), VKN/TCKN, telefon, adres, kendi şirketinin adı ve hesap numarası, açıklamalardaki kişi adları.
    - Değiştirme: sütun başlıkları ve sırası, tarih ve tutar biçimi (ör. `1.234,56`, eksi işareti ya da B/A sütunu), bankanın işlem kodları ve açıklama kalıpları ("FAST GELEN", "BSMV" gibi), boş satırlar, başlık ve toplam satırları.
    - Tutarlar: değiştirmen gerekmez. Değiştirirsen not et; bakiye sütunu tutmayacağı için bunu dosyanın hatası saymayayım.
    - Araç: Excel dosyasını Excel'de düzenleyip aynı biçimde (xlsx ya da xls) kaydet. CSV, TXT ve MT940 dosyasını Excel'de açıp kaydetme; ayraç ve Türkçe karakter kodlaması bozulur. Bunlar için kodlamayı koruyan bir metin düzenleyici kullan (Notepad++ gibi).
  - **Her dosya için kısa not** (dosyanın yanına `NOT.txt`):
    - banka, kanal (kurumsal/bireysel internet şubesi, mobil) ve menü yolu (ör. "Hesaplar > Hesap Hareketleri > Excel'e Aktar");
    - seçilebilen biçimler, hesabın para birimi, dönem;
    - anonimleştirmede neyin değiştiği; dosya indirildikten sonra bir programda açılıp kaydedildi mi.
  - **Araştırma soruları** (bankaya ya da mali müşavire sorulabilir):
    - Hedef müşterilerin (küçük ticari işletme, orta ölçekli fabrika) en çok kullandığı bankalar hangileri?
    - Her banka ticari müşteriye hangi biçimleri veriyor: Excel, CSV, MT940, camt.053? MT940 için başvuru ya da ücret gerekiyor mu?
    - Otomatik kanal var mı: e-posta ya da SFTP ile günlük MT940, bankanın ERP entegrasyonu (web servisi), açık bankacılık (hesap bilgisi hizmeti)? Bunlar MVP sonrası için not edilir.
  - **Nereye:** depo dışında, `%LOCALAPPDATA%\odoo-version\samples\bank\<banka>\` klasörüne (yoksa oluştur). Depoya girmez. Testler bu dosyaların düzeninde üretilmiş kurgusal dosyalarla çalışır (PLAN.md §8).
  - Ne zaman: T5.2'den önce. Gelmezse bankaların kamuya açık biçim belgeleriyle ve kurgusal dosyalarla çalışılır.
- [ ] K5 **Onay** — yayınlar.
  - Kullanıcı belgeleri sitesi (T8.7), tanıtım sayfası (T8.11), depo yeniden adlandırma (T8.2).
  - Claude içeriği hazırlar; yayın senin onayınla.
- [ ] K8 **Onay (isteğe bağlı)** — upstream ve OCA'ya katkı: çeviriler (T3.6), OCA portları (T11.14).
- [ ] K9 **Onay (isteğe bağlı)** — GitHub güvenlik özelliklerinin açılması.
  - Dependabot uyarıları ve gizli bilgi taraması (push koruması dahil). Public depoda ücretsiz.
  - Bu bir depo ayarı olduğu için onay gerekiyor (D-015). Onay verirsen Claude `gh` ile açar.
- [x] K10 **Karar** — geçmiş commit'lerdeki Claude ortak yazar satırı: **silindi** (kullanıcı, 2026-11-03; seçenek B).
  - Oturum bağlantısı satırları (`Claude-Session:`) 2026-10-19'da, ilk iki commit'teki `Co-Authored-By: Claude` satırları 2026-11-03'te silindi. Her seferinde geçmiş yeniden yazıldı ve `main` bir kez force-push edildi; commit kimlikleri değişti (eşlemeler CHANGELOG.md'de).
  - Artık hiçbir commit'te Claude'u yazar ya da ortak yazar gösteren satır yok. GitHub'ın katkıcı listesinin güncellenmesi biraz sürebilir.
- [x] K11 **Karar** — commit mesajlarındaki `Claude-Session:` satırı: **kaldırıldı** (kullanıcı, 2026-10-19). Kural CLAUDE.md kural 8'de ve D-015'te. Eski commit'lerdeki satırlar da silindi (kullanıcı, 2026-10-19; geçmiş yeniden yazıldı, tek force-push).
- [ ] K12 **Karar** — modül manifestlerindeki yazar (`author`) adı.
  - Neden: Odoo, Uygulamalar ekranında her modülün yazarını gösterir; müşteri de görür.
  - Varsayım (otonom mesai 1, geri dönüşü kolay): `burak-sisci`, GitHub kullanıcı adın. `tools/check_modules.py` ve `.pylintrc`'de tanımlı; değişirse mevcut manifestler de güncellenir.
  - Seçenekler: **A** — `burak-sisci` kalsın · **B** — adın soyadın · **C** — marka adı `Nexus` (K3).
  - Claude önerisi: **C**, marka belirlendi. Onay verirsen manifestler ve denetim aracı birlikte güncellenir.
  - Ne zaman: ilk dış demodan önce (F7).
- [x] K13 **Karar** — e-tablo formül adlarındaki `ODOO.` öneki: **B — `NEXUS.` önekli eş adlar** (kullanıcı, 2026-11-03).
  - `NEXUS.BALANCE`, `NEXUS.LIST` gibi eş adlar eklenecek; kayıtlı e-tablolardaki `ODOO.` adları çalışmaya devam edecek. Formül yazan kullanıcıya yalnız `NEXUS.` adları önerilecek.
  - Zaman: e-tablo düzenlemeyle birlikte (OCA `spreadsheet_oca` portu, `docs/MODULE_MATRIX.md`). Bugün Community'de e-tablolar yalnız salt okunur panolarda açılıyor; formül adı hiçbir ekranda görünmüyor. O zamana kadar `ODOO.` adları sızıntı testinin (T2.6) izin listesinde.
  - Formül adları kayıtlı e-tablolarda saklanır: ad değişirse (R17) `NEXUS.` adları da eş ad olarak çalışmaya devam etmek zorunda.
- [ ] K14 **Karar** — ürünün rengi ve simgesi (T2.2).
  - Ad artık kalıcı: Nexus (K3, D-014). Otonom mesai 1'deki geçici ad varsayımı (`OV ERP`) kalktı.
  - Neden: ekranlarda bir renk ve simge gerekiyor, ama logo tasarımı henüz yok.
  - Varsayım (geri dönüşü kolay): renk `#1f5f8b` (koyu mavi), simge mavi kare üstünde beyaz "N" harfi. Renk ve simge `ov_brand` modülünde tek yerde; ad bir sistem parametresinden (`ov_brand.name`) de değiştirilebilir.
  - Kullanıcı menüsündeki "Yardım" öğesi destek adresi (`ov_brand.support_url`) girilene kadar gizli.
  - Seçenekler: **A** — logo tasarlanana kadar böyle kalsın · **B** — kendi renk ya da logonu ver.
  - Claude önerisi: **A**; logo tanıtım materyaliyle birlikte ele alınır (T8.11).
  - Ne zaman: dış demodan önce.
- [ ] K15 **Karar** — yayıncının çevrim içi hizmet modülleri (T2.3).
  - Neden: `iap` (uygulama içi satın alma kredileri) ve `mysubscription` ("Aboneliğim") her yeni veritabanına kendiliğinden kuruluyor ve odoo.com'a bağlanıyor. SMS, iş ortağı otomatik tamamlama, aday zenginleştirme ve üretme, posta ile gönderim bunlara bağlı.
  - Varsayım (otonom mesai 2, geri dönüşü kolay): **A** uygulandı. `ov_brand` bu modülleri bağlı modülleriyle kaldırır; arayüzden kurulamazlar, Ayarlar'daki kutuları gizli.
  - Seçenekler: **A** — kaldırılsın · **B** — kurulu kalsın, yalnız arayüzde gizlensin; veri gönderen çağrılar tek tek kapatılsın.
  - Claude önerisi: **A**. Gizlemede upstream'in her yeni sürümünde yeni bir çağrıyı kaçırma riski var; kaldırınca kod hiç yüklenmiyor (KVKK, T2.7).
  - Sonucu: upstream `sms` modülü `iap`'ye bağlı. Yerli bir SMS sağlayıcısı ya bu bağımlılık olmadan yazılır ya da bu karar yeniden açılır.
  - Ne zaman: SMS ya da şirket bilgisi otomatik doldurma ihtiyacı doğduğunda. Yerli kaynak: e-Belge mükellef sorgulaması VKN'den unvanı verir (T4.3, T4.5).
- [x] K16 **Karar** — web istemcisinin adres yolu: **B — marka adı, `/nexus`** (kullanıcı, 2026-11-03).
  - `ov_brand` web istemcisini `/nexus`'ta sunar; `/odoo` adresleri sorgusuyla birlikte oraya yönlendirilir (T2.4). Değer iki sabitte: `tools.py` ve `web_path.js`.
  - T2.4'ten beri kullanılan `/app` yalnız geliştirme ortamında kullanıldığı için yönlendirilmiyor.
  - Ad değişirse (R17) yol da değişir; müşterideki eski bağlantılar için bir yönlendirme daha gerekir.
- [x] K17 **Karar** — müşteriye giden e-posta ve sayfalarda "Powered by" satırı: **B — ürün adı, bağlantısız** (kullanıcı, 2026-11-03).
  - Bildirim e-postalarının, özet e-postasının, portal belgelerinin ve portal sayfalarının altında "Powered by Nexus" yazar; yayıncıya ya da ürün sitesine bağlantı yok. Satır tek bir şablonda (`ov_brand.powered_by`), ad `ov_brand.name`'den gelir.
  - Müşteri satırı kapatabilir: Genel Ayarlar > Şirketler > Alt Bilgide Ürün Adı (varsayılan açık).
  - Türkçesi "Altyapı: Nexus" (Claude seçimi; upstream "Powered by"ı "Hazırlayan" diye çeviriyor, ad sonra geliyordu). Başka bir ifade istersen yalnız `ov_brand/i18n/tr.po`'daki iki satır değişir.
  - Özet e-postasındaki ikinci satır ("Sent by") geri gelmedi: aynı e-postada ad iki kez yazmasın diye.
- [ ] K18 **Karar** — PDF motoru (T2.5).
  - Neden: Odoo 20.0'da iki motor var. wkhtmltopdf upstream'in varsayılanı ama 2022'den beri arşivde, güvenlik düzeltmesi almıyor. Paper Muncher yayıncının yeni motoru; kendi tanımıyla "erken alfa" ve yalnız amd64 Linux için paketli.
  - Varsayım (otonom mesai 2, geri dönüşü kolay): **A**. Henüz kurulan bir şey yok; T3.7'de CI'a buna göre kurulur.
  - Seçenekler: **A** — üretimde wkhtmltopdf, Paper Muncher CI'da ikinci motor · **B** — hemen Paper Muncher · **C** — belge türüne göre ikisi.
  - Claude önerisi: **A**. Geçiş ölçütü: Paper Muncher'ın 1.0'a ulaşması ya da upstream'in varsayılanı yapması, ve Türkçe belgelerin (T3.7) onunla doğru çıkması. Ayrıntı `docs/research/pdf-engine.md`.
  - Ne zaman: T3.7'den önce. Barındırma kararında (D-013) sunucu arm64 olursa Paper Muncher kaynaktan derlenmeli.
- [ ] K19 **Karar** — eski ürün adının metinlerde değiştirilme yöntemi (T2.6).
  - Neden: upstream'de 500'den fazla çevrilebilir metin ve onların Türkçe çevirileri eski adı taşıyor. Yenileri her upstream güncellemesiyle gelir.
  - Varsayım (otonom mesai 3, geri dönüşü kolay): **gösterimde değiştirme**. Kayıtlı metinler ve çeviri dosyaları değişmez; ad, kullanıcıya gösterilirken ürün adıyla değiştirilir, Türkçe ekler uydurulur ("Nexus'ta"). Sunucunun kod çevirisi işlevi modül yüklenirken sarmalanır; çekirdeğe dokunulmaz (D-010).
  - Bedeli: önbelleğe alınmayan yüzeylerde (sunucu mesajları, e-posta şablonları) her gösterimde kısa bir metin denetimi. Dışa aktarılan çeviri dosyaları eski adı taşır.
  - Seçenekler: **A** — gösterimde değiştirme kalsın · **B** — kendi çeviri dosyalarımızla metin metin değiştirme: upstream'in her güncellemesinde elle bakım ister, testin bulduğunu yine elle düzeltmek gerekir.
  - Claude önerisi: **A**. Upstream'in yeni metinleri de kendiliğinden kapsanır; sızıntı testi kalanları yakalar.
  - Aynı adımdaki küçük varsayımlar:
    - botun e-posta adresi `bot@example.com` (upstream `odoobot@example.com`);
    - yayıncının destek masasına yönlendiren cümleler (e-tablo hata mesajları) çıkarıldı. Destek adresimiz (`ov_brand.support_url`, K14) girilince oraya yönlendirme ayrı bir iş olarak eklenebilir.

- [ ] K20 **Karar** — Türk hesap planındaki hesap eşlemeleri (T3.2).
  - Neden: upstream bazı işlemleri Tekdüzen dışı ya da yanlış hesaplara kaydediyordu (`docs/research/l10n-tr.md` §3.6, G27–G29). Doğru hesap muhasebe uygulamasına bağlı; mali müşavir görüşü gerekir.
  - Varsayımlar (otonom mesai 3, geri dönüşü kolay; hepsi `ov_l10n_tr` verisinde):
    - erken ödeme indirimi: verilen 611 Satış İskontoları, alınan 649 Diğer Olağan Gelir ve Kârlar;
    - kasa farkı: fazla 679, eksik 689 (diğer olağandışı gelir/gider);
    - cari yıl kârı veya zararı: 590 Dönem Net Kârı (yalnız yeni şirkette; kurulu şirket kendi 999999 hesabını korur);
    - gelir vergisi stopajı: kira (GVK 94/5-a) ve serbest meslek (GVK 94/2-b) %20, 360 Ödenecek Vergi ve Fonlar'a. Upstream'in 191'e kaydeden kira stopajı pasif; geçmiş kayıtlar değişmez;
    - 193 ve 360 alacak/borç hesabı türünden çıkarıldı. Yoksa bu hesaplara vergi kaydedilemiyor. Kayıtlı hesapta tür değişmez.
  - Mali müşavire sorulacaklar (upstream'in eşlemeleri, değiştirilmedi):
    1. Alışta tevkif edilen KDV 391005'e kaydediliyor. Uygulamada genellikle 360'ta izlenir. Hangisi?
    2. Satışta damga vergisi 391006'ya (Hesaplanan KDV'nin altında) kaydediliyor. 360 daha doğru olabilir.
    3. Alışta damga vergisi 770 Genel Yönetim Giderleri'ne kaydediliyor. Uygun mu?
  - Seçenekler: **A** — varsayımlar kalsın, sorular pilot öncesi mali müşavire sorulsun · **B** — şimdi farklı bir eşleme ver.
  - Claude önerisi: **A**. Değişiklik yalnız veri dosyasında; kurulu şirketler modül güncellemesiyle yeni eşlemeyi alır.
  - Ne zaman: T5.8 (KDV hazırlık raporu) ya da ilk pilottan (T9.6) önce; sorular T9.4'teki mali müşavir görüşmesine de eklenebilir.

- [ ] K21 **Karar** — Türkiye'de kişi/şirket ayrımı ve MERSİS denetimi (T3.3).
  - Neden: 20.0'da iş ortağının şirket olup olmadığı elle seçilmiyor; vergi numarası olan herkes şirket sayılıyordu. TCKN girilen gerçek kişi de şirket görünüyordu (`docs/research/l10n-tr.md` G16).
  - Varsayımlar (otonom mesai 3, geri dönüşü kolay; hepsi `ov_l10n_tr` kodunda):
    - 11 haneli vergi numarası (TCKN) olan Türk iş ortağı gerçek kişidir, şahıs şirketi dahil. e-Belge'de kişi olarak (`cac:Person`) yazılması bu kurala dayanacak (T4.3). 10 haneli VKN'li iş ortağı şirkettir.
    - MERSİS numarasında yalnız 16 hane denetlenir; boşluk ve tire temizlenir. İç yapısı (şirkette 0 + VKN + 5 hane) yalnız ikincil kaynaklarda geçiyor; resmî bir kural bulunamadı.
  - Seçenekler: **A** — varsayımlar kalsın · **B** — şahıs şirketleri şirket sayılsın (kişi yalnız e-Belge'de ayrılır) · **C** — MERSİS iç yapısı da denetlensin.
  - Claude önerisi: **A**. Şahıs şirketi vergide gerçek kişidir; resmî kaynağı olmayan bir iç yapı denetimi geçerli bir numarayı reddedebilir.
  - Ne zaman: e-Belge çekirdeğinden (T4.3) önce; mali müşavire K20 sorularıyla birlikte sorulabilir.

- [ ] K22 **Karar** — Türkiye adreslerinde il/ilçe düzeni (T3.4).
  - Neden: upstream'de ilçe listesi yoktu, il zorunlu değildi, posta kodu zorunluydu (`docs/research/l10n-tr.md` G19). e-Belge adreste il ve ilçe bekler.
  - Varsayımlar (otonom mesai 4, geri dönüşü kolay; hepsi `ov_l10n_tr`'de):
    - Veri kaynağı: plandaki açık lisanslı GitHub veri setleri yerine İçişleri Bakanlığı Mülki İdare Bölümleri Envanteri. O depolar aynı adların ikincil kopyası. İlçe adları kanunla belirlenen olgular; envanterde lisans belirtilmemiş (`docs/COMPLIANCE.md` §4). Hukuki incelemede (T9.4) teyit edilir.
    - Büyükşehir olmayan 51 ilin merkez ilçesinin adı "Merkez" (adreslerde "Merkez/Bolu" gibi). Envanter bu ilçeleri ilçe listesinde vermiyor; il belediyesi listesinden eklendi.
    - Adlar resmî yazımla, şapkasız: "Bala", "Şehitkamil". Kurulu kişilerdeki şapkalı yazım ("Balâ") eşleştirmede tanınır.
    - İl zorunlu, posta kodu isteğe bağlı. Adres biçimi "34710 Kadıköy/İstanbul".
    - Portal ve e-ticaret adres formunda ilçe, ilin listesinden seçilir; listede olmayan ilçe yazılamaz.
    - Kurulu kişiler yalnız belirsizlik yoksa ilçeye bağlanır. Şehir alanına il adı yazılmış kişi o ilin merkez ilçesine bağlanır.
  - Seçenekler: **A** — varsayımlar kalsın · **B** — merkez ilçeler il adıyla anılsın ("Bolu Merkez") · **C** — posta kodu zorunlu olsun · **D** — veri açık lisanslı bir GitHub veri setinden alınsın.
  - Claude önerisi: **A**. Resmî envanter kendi sayılarıyla denetlenebiliyor (922 ilçe); ikincil veri setlerinin güncelliği ona bağlı.
  - Ne zaman: e-Belge çekirdeğinden (T4.3) önce.

- [ ] K23 **Karar** — TCMB döviz kurlarının kullanımı (T3.5).
  - Neden: upstream'de TCMB kuru yoktu, dövizli işlemde kur elle giriliyordu (`docs/research/l10n-tr.md` G20). Hangi kurun hangi güne yazılacağı muhasebe uygulamasına bağlı.
  - Varsayımlar (otonom mesai 4, geri dönüşü kolay; hepsi `ov_l10n_tr_tcmb`'de):
    - Varsayılan kur türü **döviz alış**. Şirket ayarından döviz satış, efektif alış ya da efektif satış seçilebilir.
    - Bülten kendi tarihiyle kaydedilir; sistem bir kuru tarihinden sonraki günden başlayarak uygular. Böylece işleme önceki iş günü ilan edilen kur uygulanır (3 Kasım bülteni 4 Kasım işlemlerinde). Hafta sonu ve tatilde son bülten geçerli kalır.
    - TCMB'nin efektif kur vermediği para birimlerinde (RUB, CNY, AED ve diğerleri) aynı yönün döviz kuru kullanılır.
    - Ülkesi Türkiye olan şirketlerde günlük güncelleme açık gelir. Kurlar her gün 16.00'da alınır (bülten 15.30 sularında).
    - Yalnız etkin para birimlerine kur yazılır.
    - Kaçırılan bültenler en çok 31 gün geriye kadar tamamlanır; alınamazsa bir saat sonra yeniden denenir. Elle aktarım bir seferde en çok 62 gün.
    - Para birimi Türk lirası olmayan şirkete Türk lirası üzerinden çapraz kur yazılır.
  - Seçenekler: **A** — varsayımlar kalsın · **B** — bülten yayımlandığı gün de uygulansın (3 Kasım bülteni 3 Kasım'da) · **C** — varsayılan kur türü başka olsun (ör. efektif satış) · **D** — başka bir düzen.
  - Claude önerisi: **A**. Yaygın uygulamada TCMB'nin bir gün ilan ettiği kur ertesi günün işlemlerinde kullanılır; 20.0'ın tarih kuralı bunu kendiliğinden veriyor (ölçüldü). Döviz alış en yaygın seçim. Vergi mevzuatındaki kesin kural bu oturumda birincil kaynaktan doğrulanmadı; mali müşavirle teyit edilmeli.
  - Ne zaman: ilk pilot müşteriden (F9) önce; mali müşavire K20 sorularıyla birlikte sorulabilir.

- [ ] K24 **Karar** — Türkçe çevirinin tamamlanma yöntemi (T3.6).
  - Neden: upstream'in Türkçe çevirisi paket modüllerinde %81; çevrilmemiş metinler İngilizce görünüyor, bazı çeviriler hatalı (ör. formdaki "Discard" düğmesi "Sil" diye çevrilmiş).
  - Varsayımlar (otonom mesai 5, geri dönüşü kolay; hepsi `ov_i18n_tr`'de):
    - Çeviriler ayrı bir modülde (`ov_i18n_tr`, LGPL-3: upstream metinlerinin çevirisi). Her yeni veritabanına kendiliğinden kurulur.
    - Modül kurulurken çevirileri, önceden kurulu uygulamalardaki var olan çevirilerin yerine yazılır. Sonraki güncellemelerde yalnız eksikler tamamlanır, müşterinin düzenlediği çeviri korunur. Müşterinin düzenlemesine ayrılmış kayıtlara (ör. ülke adları) hiç dokunulmaz.
    - Kaynak metinde "Odoo" geçen çevirilerde ad olduğu gibi kalır; gösterimde `ov_brand` "Nexus" yazar (K19). Böylece çeviriler istenirse upstream'e de verilebilir (K8).
    - Ölçüm upstream'in çeviri şablonlarına (`.pot`) göre. Paket: CI'daki MVP uygulamaları, modüllerimiz, bağımlılıkları ve onlarla kendiliğinden kurulanlar (83 modül). CI eşiği her çeviri partisiyle yükselir.
    - Terimler upstream'in yerleşik Türkçe karşılıklarıyla tutarlı tutulur (ör. Contact → Kontak, Journal Entry → Yevmiye Kaydı); upstream'in kendi içinde tutarsız olduğu yerde en yaygın karşılık seçilir.
    - Muhasebe terimleri (`account`): Credit Note → İade Faturası, Tax Return → Vergi Beyannamesi (upstream'de yer yer "Vergi İadesi", yanlış), Suspense Account → Geçici Hesap, Reconcile → Denkleştirme, hash → özetlenmiş (hash), Accrued Expenses/Income → Gider/Gelir Tahakkukları, Furniture & Fixtures → Demirbaşlar, leasehold improvements → Özel Maliyetler.
  - Seçenekler: **A** — varsayımlar kalsın · **B** — modül kurulurken var olan çevirilere dokunulmasın, yalnız eksikler tamamlansın · **C** — "Odoo" geçen metinlerin çevirisinde doğrudan "Nexus" yazılsın · **D** — başka bir düzen.
  - Claude önerisi: **A**. Kurulumda üzerine yazma, hatalı upstream çevirilerinin (ör. "Sil") önceden kurulmuş veritabanlarında da düzelmesini sağlıyor; yeni müşteride zaten ilk kurulumdur.
  - Ne zaman: acil değil; F9 pilotundan önce. Terim tercihlerin varsa (ör. "Kontak" yerine "Kişi") liste olarak verebilirsin.

Numaralarda boşluk var: eski iki madde (müşteri listesi, yasal yapı) aynı işi anlatan T9.1 ve T9.3 görevleriyle birleştirildi (§3).

## 3. Kategori K — kullanıcının görevleri

Bu görevleri yalnız sen yapabilirsin. Claude hazırlık desteği verir.

- [ ] T9.1 Hedef müşteri listesi ve ilk temaslar
  - Sen: yakın çevre, organize sanayi bölgeleri, esnaf ve sanayi odalarından aday işletmeler; ilk görüşmeler.
  - Claude: liste şablonu, görüşme soruları, demo senaryosu.
- [ ] T9.3 Yasal yapı
  - Sen: şirket veya şahıs işletmesi kuruluşu, mali müşavir seçimi.
  - Claude: seçeneklerin araştırması (ör. genç girişimci kazanç istisnası; koşullar doğrulanacak).
- [ ] T9.4 Hukuki inceleme
  - Sen: avukat ve mali müşavirle görüşme (önce ücretsiz seçenekler).
  - Claude: incelenecek soru listesi ve taslak belgeler (T8.10).

## 4. Kategori B — birlikte yapılacak görevler

Standart mesaide yapılır. Senden beklenen her görevin altında yazıyor.

- [x] T0.7 Açık kararların (D-010 … D-015) kullanıcıyla netleştirilmesi
- [x] T0.8 Detaylı planlama
- [ ] T7.9 Kullanıcı kabul turu
  - Sen: sistemi ilk kez gören biri gibi paketi seçip kurulum sihirbazını tamamlarsın; ilk faturayı ve ilk üretim emrini yardım almadan oluşturursun.
  - Claude: tur senaryosu ve geri bildirim formu; bulgular göreve dönüşür.
- [ ] T8.1 MVP sonu değerlendirmesi
  - Sen: e-Belge gönderim yöntemi (D-012) ve paket kapsamı (D-018) kararları. Kalıcı ad seçildi (Nexus, K3).
- [ ] T8.2 Kalıcı adın uygulanması
  - Sen: depo yeniden adlandırma onayı (K5), alan adı (K1). Ad seçildi: Nexus (K3).
- [ ] T8.9 Rakip ve fiyat araştırması, fiyat listesi
  - Sen: fiyatların onayı.
- [ ] T8.12 Kapı kontrolü ve go/no-go
  - Sen: müşteri arayışına başlama kararı.
- [ ] T9.2 Demo görüşmeleri ve geri bildirim döngüsü
  - Sen: görüşmeleri yaparsın. Claude: demo ortamı, notların kişisel veri içermeden özetlenmesi.
- [ ] T9.5 Üretim barındırma kararı (D-013) ve sunucu
  - Sen: sağlayıcı seçimi ve ödeme (ilk gelirden).
- [ ] T9.6 İlk pilot kurulum
  - Sen: müşteriyle sözleşme ve eğitim. Claude: kurulum, veri aktarımı, e-Belge canlı geçişi.
- [ ] T9.8 İlk müşteri sonrası değerlendirme
  - Sen: strateji kararları (D-017).
- [ ] T10.4 Abonelik ve tahsilat
  - Sen: ödeme sağlayıcısı (iyzico) üye işyeri hesabı ve sözleşmesi.
- [ ] T11.14 OCA'ya port katkıları
  - Sen: katkı onayı (K8).

## 5. Mesai türleri (D-021)

- **Standart mesai:** birlikte çalışırız. Kategori B görevleri, kararlar ve onaylar burada.
- **Otonom mesai:** Claude tek başına çalışır, sen ekran başında değilsin.
  - Başlatmak için "otonom mesaiye başla" demen yeterli.
  - Claude yalnız kategori C görevlerini yapar. Her görev sonunda commit + push eder; iş yarıda kesilse de kaybolmaz.
  - Dışa dönük ve onay gerektiren hiçbir şey yapmaz: yayın, depo ayarı, ücretli servis, hesap açma, force-push.
  - Mesai sonunda: CHANGELOG.md'de mesai özeti, bu belgede yeni sorular ve onaylar.
