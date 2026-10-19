# Kullanıcıdan Beklenenler

Son güncelleme: 2026-10-19
İlgili kararlar: D-003, D-015, D-021

Bu belge, **kullanıcının yapması, karar vermesi veya onaylaması gereken her şeyin** tek listesidir.
- Otonom mesaiden dönünce ilk bakılacak yer burası (§1). Mesainin özeti CHANGELOG.md'de.
- Claude otonom mesaide soru soramaz. Soruları ve onay bekleyen işleri buraya yazar, kendi yapabileceği işlere devam eder (D-021).
- İşaretler: `[ ]` bekliyor · `[x]` tamam · `[-]` vazgeçildi.
- Görev kategorileri (D-021): **K** kullanıcının yapacakları · **B** birlikte yapılacaklar · **C** Claude'un yapacakları. Tam liste ve sayılar PLAN.md'de.

## 1. Şimdi bakılacaklar

Öncelik sırasıyla. Hiçbiri Claude'un işini durdurmuyor.

1. **K2: TÜBİTAK 2209-A için son başvuru 11 Kasım 2026.** Başvurmak istiyorsan danışman bulmak zaman alır.
2. **K10:** eski commit'lerdeki oturum bağlantısı satırları silindi (isteğin üzerine, 2026-10-19). İlk iki commit'teki Claude ortak yazar satırı duruyor; o da silinsin mi? Bir force-push daha gerekir.
3. **K1:** GitHub Student Developer Pack başvurusu. Onay süreci uzayabildiği için erken başvurmak iyi olur.
4. **K9:** GitHub güvenlik özellikleri (ücretsiz). Onay verirsen Claude açar.
5. **K12:** modüllerde yazar olarak görünecek ad. Şimdilik `burak-sisci`; marka belirlendiği için `Nexus` seçeneği öne çıktı.
6. **K13:** e-tablo formüllerindeki `ODOO.` öneki. Şimdilik teknik ad sayıldı, değişmiyor.
7. **K14:** ürünün rengi ve simgesi. Ad artık Nexus; renk ve simge yer tutucu olarak varsayıldı.
8. **K15:** yayıncının çevrim içi hizmet modülleri (IAP, Aboneliğim) kaldırıldı. SMS ve iş ortağı otomatik tamamlama da bu yüzden yok.

Otonom mesai 1 bitti (2026-10-18). Özeti CHANGELOG.md'de, "Otonom mesai 1 — özet".

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
- [ ] K4 **Eylem (isteğe bağlı)** — örnek banka ekstresi dosyaları.
  - Kullandığın bankalardan Excel/CSV ekstre. Kişisel veriler silinmiş olmalı; depoya girmez.
  - Ne zaman: T5.2'den önce. Yoksa bankaların kamuya açık biçim belgeleriyle ve kurgusal dosyalarla çalışılır.
- [ ] K5 **Onay** — yayınlar.
  - Kullanıcı belgeleri sitesi (T8.7), tanıtım sayfası (T8.11), depo yeniden adlandırma (T8.2).
  - Claude içeriği hazırlar; yayın senin onayınla.
- [ ] K8 **Onay (isteğe bağlı)** — upstream ve OCA'ya katkı: çeviriler (T3.6), OCA portları (T11.14).
- [ ] K9 **Onay (isteğe bağlı)** — GitHub güvenlik özelliklerinin açılması.
  - Dependabot uyarıları ve gizli bilgi taraması (push koruması dahil). Public depoda ücretsiz.
  - Bu bir depo ayarı olduğu için onay gerekiyor (D-015). Onay verirsen Claude `gh` ile açar.
- [ ] K10 **Karar** — geçmiş commit'lerdeki Claude ortak yazar satırı.
  - Oturum bağlantısı satırları (`Claude-Session:`) eski commit'lerden silindi: kullanıcının isteği, 2026-10-19. Geçmiş bir kez yeniden yazıldı ve `main` force-push edildi; bütün commit kimlikleri değişti (eşleme CHANGELOG.md'de).
  - Kalan: ilk iki commit'te (`b267933`, `363a288`) `Co-Authored-By: Claude` satırı var. GitHub bu yüzden Claude'u katkıcı olarak gösteriyor. Sonraki commit'lerde bu satır yok (D-015, CLAUDE.md).
  - Seçenekler:
    - **A — bırak:** geçmiş değişmez, Claude katkıcı listesinde kalır.
    - **B — temizle:** iki satır silinir, `main` bir kez daha force-push edilir. Commit kimlikleri yine değişir; belgelerde geçen kimlikler güncellenir. D-015 force-push'u yasaklıyor, bu yüzden senin açık onayın gerekir.
  - Claude önerisi: **B**. Depo yeni ve başka kopyası yok, risk düşük. GitHub'ın katkıcı listesinin güncellenmesi biraz sürebilir.
  - Onay verirsen bir sonraki mesaide yapılır.
- [x] K11 **Karar** — commit mesajlarındaki `Claude-Session:` satırı: **kaldırıldı** (kullanıcı, 2026-10-19). Kural CLAUDE.md kural 8'de ve D-015'te. Eski commit'lerdeki satırlar da silindi (kullanıcı, 2026-10-19; geçmiş yeniden yazıldı, tek force-push).
- [ ] K12 **Karar** — modül manifestlerindeki yazar (`author`) adı.
  - Neden: Odoo, Uygulamalar ekranında her modülün yazarını gösterir; müşteri de görür.
  - Varsayım (otonom mesai 1, geri dönüşü kolay): `burak-sisci`, GitHub kullanıcı adın. `tools/check_modules.py` ve `.pylintrc`'de tanımlı; değişirse mevcut manifestler de güncellenir.
  - Seçenekler: **A** — `burak-sisci` kalsın · **B** — adın soyadın · **C** — marka adı `Nexus` (K3).
  - Claude önerisi: **C**, marka belirlendi. Onay verirsen manifestler ve denetim aracı birlikte güncellenir.
  - Ne zaman: ilk dış demodan önce (F7).
- [ ] K13 **Karar** — e-tablo formül adlarındaki `ODOO.` öneki (`ODOO.BALANCE`, `ODOO.PIVOT`, `ODOO.LIST` vb.).
  - Neden: panolarda ve e-tablolarda formül yazan kullanıcı bu adları görür. Ama kayıtlı panolar bu adları içeriyor; değiştirmek kayıtlı formülleri bozar (`docs/research/brand-inventory.md` §10).
  - Varsayım (otonom mesai 1, geri dönüşü kolay): teknik ad sayılır, marka sızıntısı testinin (T2.6) izin listesinde kalır.
  - Seçenekler: **A** — olduğu gibi kalsın · **B** — kendi önekimizle eş adlar eklensin, `ODOO.` eski kayıtlar için çalışmaya devam etsin · **C** — tamamen yeniden adlandırılsın, kayıtlı formüller dönüştürülsün.
  - Claude önerisi: şimdilik **A**; kalıcı marka adı belirlenince (T8.2) **B** yeniden değerlendirilir.
  - Ne zaman: T2.6'dan önce ya da T8.2'de.
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
  - Ne zaman: SMS ya da şirket bilgisi otomatik doldurma ihtiyacı doğduğunda (yerli kaynak T3.3).

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
