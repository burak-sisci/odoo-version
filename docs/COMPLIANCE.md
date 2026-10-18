# Lisans, Marka ve Hukuki Uyum

Son güncelleme: 2026-10-18
İlgili kararlar: D-006, D-007, D-008, D-014, D-015, D-016

> Hukuki görüş değildir. Ticari satıştan önce avukat incelemesi yapılacaktır (ROADMAP T6.2).

## 1. Lisanslar ve anlamları

| Bileşen | Lisans | Yapabiliriz | Yükümlülük |
|---|---|---|---|
| Odoo Community (upstream) | LGPL-3 | Kullanmak, değiştirmek, ticari satmak, SaaS olarak sunmak | Lisans/telif notlarını korumak. **Değiştirilmiş** çekirdeği müşteriye dağıtırsak değişikliklerin kaynağını LGPL ile vermek. SaaS'ta ağ maddesi yok |
| Odoo Enterprise | Odoo Enterprise Edition License v1.0 | **Hiçbir şey.** Kodunu kullanamayız, kopyalayamayız, dağıtamayız | — |
| Geçmiş sürümlerdeki LGPL modüller (ör. 19.0 Nilvera) | LGPL-3 | Yeni sürüme taşımak, değiştirmek | Türetilen kod LGPL-3 kalır, telif notları korunur |
| OCA modülleri | Çoğunlukla AGPL-3, bazıları LGPL-3 | Kullanmak, değiştirmek | AGPL: değiştirip ağ üzerinden sunarsak kaynağı kullanıcılara vermek. AGPL modüle bağımlı modülümüz kapalı olamaz (D-008/4) |
| Odoo dokümantasyonu | CC BY-SA 4.0 | Okuyup işlev tanımı çıkarmak. Metin kopyalarsak atıf + aynı lisans | Kendi belgelerimize metin kopyalanırsa atıf ve CC BY-SA |
| Kendi özgün modüllerimiz | **D-016 ile belirlenecek** (açık; öneri AGPL-3, gizli kalması gerekenler ayrı private depoda) | Serbest | Kapalı lisans seçilirse LGPL/AGPL koddan türetilmemiş olmalı ve AGPL modüle bağımlı olmamalı |

## 2. Clean-room kuralı (D-006)

Bu bir tersine mühendislik projesidir. Hedef **işlevi** yeniden üretmek, **kodu** değil.

### İzinli kaynaklar
1. Odoo Community kaynak kodu (bütün sürümler, LGPL kısmı).
2. Odoo'nun herkese açık dokümantasyonu (`odoo.com/documentation`, `github.com/odoo/documentation`).
3. Odoo'nun herkese açık sürüm notları, pazarlama sayfaları, herkese açık tanıtım videoları (yalnız **işlev** öğrenmek için; görsel/metin kopyalanmaz).
4. OCA kodu (lisansına uyularak).
5. Yasal mevzuat ve standart belgeleri (GİB kılavuzları, UBL-TR şemaları vb.).

### Yasak kaynaklar
1. Odoo Enterprise kaynak kodu (her biçimde: sızıntı, GitHub'daki izinsiz kopyalar, arşivler).
2. Enterprise deneme hesaplarından veya odoo.com SaaS'tan indirilen JS/CSS/XML/görseller (tarayıcıya gelen küçültülmüş kod dahil).
3. Enterprise modüllerinin ikonları, görselleri, tema dosyaları.
4. 3. parti ücretli Odoo uygulamalarının (apps.odoo.com, OPL lisanslı) kodu.

### Çalışma kuralı
- Her Enterprise eşdeğeri modül için `docs/specs/<modül>.md` dosyasına işlev tanımı yazılır. Tanım yalnız izinli kaynaklara dayanır ve kaynak bağlantıları içerir.
- Kod bu tanımdan yazılır.

## 3. Marka (D-007)

- Ürün adı, logo, favicon, sayfa başlıkları, e-posta altbilgileri, PDF rapor başlıkları, giriş ekranı, web sitesi altbilgisi ve PWA manifestinde **kendi markamız** kullanılır.
- Kaynak dosyalardaki `# Part of Odoo. See LICENSE file…` başlıkları ve `LICENSE`/`COPYRIGHT` dosyaları **silinmez**.
- "Odoo Community tabanlıdır" gibi tanımlayıcı bir ifade belgelerde kullanılabilir; ürün adı veya logo olarak kullanılamaz. Pazarlama metinlerinde kullanım avukata danışılarak netleştirilecek.
- **Çalışma adı `odoo-version` (D-014)** "Odoo" sözcüğünü içerir.
  - Yalnız depo adı, belgeler ve geliştirme ortamında kullanılır.
  - Dış demo, pilot ve satıştan önce kalıcı adla değiştirilir (ROADMAP T6.1).
  - Public GitHub depo adı da o adımda yeniden adlandırılır; GitHub eski adresi yeni adrese yönlendirir.

## 4. Veri ve mevzuat

- **e-Belge saklama:** asıl saklama Türkiye'de zorunlu; başkasının e-Belgesini saklamak GİB izni gerektirir (`research/e-fatura.md` §3).
- **KVKK:** müşteri = veri sorumlusu, biz (SaaS) = veri işleyen. Yurt dışı sunucu → m.9 süreçleri (`research/hosting.md`).
- **odoo.com'a veri gönderimi:** Community'de odoo.com'a veri gönderen bileşenler (yayıncı garantisi, IAP) ürünümüzde kapatılır veya kendi sağlayıcılarımızla değiştirilir (ROADMAP T2.3). Müşteri verisi bizim bilgimiz dışında 3. tarafa gitmemelidir.
- **Public depo (D-015):** depodaki her şey herkese açık.
  - Depoya girmeyecekler: gizli bilgi (API anahtarı, şifre, sertifika), müşteri veya test kişisinin gerçek verisi, yerel yapılandırma (`.env`, `odoo.conf`).
  - Her push'tan önce `git diff --cached` ile denetlenir.
  - Depoda LICENSE dosyası olmadığı sürece içerik "tüm hakları saklı" sayılır. Kendi modüllerimizin lisansı D-016 ile belirlenecek.

## 5. Lisans envanteri

Projeye giren her dış kod buraya yazılır.

| Bileşen | Sürüm/commit | Lisans | Değiştirildi mi? | Nerede |
|---|---|---|---|---|
| (henüz yok — upstream projeye eklenmedi, ROADMAP T1.3) | | | | |
