# Kullanıcıdan Beklenenler

Son güncelleme: 2026-10-18
İlgili kararlar: D-003, D-015, D-021

Bu belge, **kullanıcının yapması, karar vermesi veya onaylaması gereken her şeyin** tek listesidir.
- Otonom mesaiden dönünce ilk bakılacak yer burası (§1). Mesainin özeti CHANGELOG.md'de.
- Claude otonom mesaide soru soramaz. Soruları ve onay bekleyen işleri buraya yazar, kendi yapabileceği işlere devam eder (D-021).
- İşaretler: `[ ]` bekliyor · `[x]` tamam · `[-]` vazgeçildi.
- Görev kategorileri (D-021): **K** kullanıcının yapacakları · **B** birlikte yapılacaklar · **C** Claude'un yapacakları. Tam liste ve sayılar PLAN.md'de.

## 1. Şimdi bakılacaklar

Öncelik sırasıyla. Hiçbiri Claude'un işini durdurmuyor.

1. **K2: TÜBİTAK 2209-A için son başvuru 11 Kasım 2026.** Başvurmak istiyorsan danışman bulmak zaman alır.
2. **K10:** geçmiş iki commit'te Claude ortak yazar görünüyor; temizlensin mi?
3. **K11:** commit mesajlarındaki oturum bağlantısı satırı kalsın mı?
4. **K1:** GitHub Student Developer Pack başvurusu. Onay süreci uzayabildiği için erken başvurmak iyi olur.
5. **K9:** GitHub güvenlik özellikleri (ücretsiz). Onay verirsen Claude açar.

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
- [ ] K3 **Karar** — kalıcı marka adı için adaylar. Ne zaman: T8.1'e kadar. Claude T8.1'de marka ve alan adı uygunluk araştırmasıyla seçenek sunar.
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
  - Durum: ilk iki commit'te (`cf37443`, `24f56b3`) `Co-Authored-By: Claude` satırı var. GitHub bu yüzden Claude'u katkıcı olarak gösteriyor. Bundan sonraki commit'lerde bu satır yok (D-015, CLAUDE.md).
  - Seçenekler:
    - **A — bırak:** geçmiş değişmez, Claude katkıcı listesinde kalır.
    - **B — temizle:** iki commit'in mesajı yeniden yazılır ve `main` bir kez force-push edilir. D-015 force-push'u yasaklıyor, bu yüzden senin açık onayın gerekir.
  - Claude önerisi: **B**. Depo yeni ve başka kopyası yok, risk düşük. GitHub'ın katkıcı listesinin güncellenmesi biraz sürebilir.
  - Onay verirsen bir sonraki mesaide yapılır.
- [ ] K11 **Karar** — commit mesajlarındaki `Claude-Session:` satırı.
  - Bu satır commit'in hangi Claude oturumunda hazırlandığını gösteren bir bağlantı. GitHub'da katkıcı oluşturmaz.
  - Varsayılan: satır kalır. Kaldırılmasını istersen CLAUDE.md'ye kural olarak eklenir.

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
  - Sen: e-Belge gönderim yöntemi (D-012), kalıcı marka adı (D-014, K3) ve paket kapsamı (D-018) kararları.
- [ ] T8.2 Kalıcı adın uygulanması
  - Sen: ad seçimi, depo yeniden adlandırma onayı (K5), alan adı (K1).
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
