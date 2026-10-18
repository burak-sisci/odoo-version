# Lisans, Marka ve Hukuki Uyum

Son güncelleme: 2026-10-18
İlgili kararlar: D-006, D-007, D-008, D-014, D-015, D-016, D-019, D-020

> Hukuki görüş değildir. Ticari satıştan önce avukat incelemesi yapılacaktır (PLAN T9.4).

## 1. Lisanslar ve anlamları

| Bileşen | Lisans | Yapabiliriz | Yükümlülük |
|---|---|---|---|
| Odoo Community (upstream) | LGPL-3 | Kullanmak, değiştirmek, ticari satmak, SaaS olarak sunmak | Lisans/telif notlarını korumak. **Değiştirilmiş** çekirdeği müşteriye dağıtırsak değişikliklerin kaynağını LGPL ile vermek. SaaS'ta ağ maddesi yok |
| Odoo Enterprise | Odoo Enterprise Edition License v1.0 | **Hiçbir şey.** Kodunu kullanamayız, kopyalayamayız, dağıtamayız | — |
| Geçmiş sürümlerdeki LGPL modüller (ör. 19.0 Nilvera) | LGPL-3 | Yeni sürüme taşımak, değiştirmek | Türetilen kod LGPL-3 kalır, telif notları korunur |
| OCA modülleri (resmî veya bizim 20.0 portumuz, D-019) | Çoğunlukla AGPL-3, bazıları LGPL-3 | Kullanmak, değiştirmek, 20.0'a taşımak | Orijinal lisans, yazar ve telif notları korunur. AGPL: değiştirip ağ üzerinden sunarsak kaynağı kullanıcılara vermek. AGPL modüle bağımlı bir modül kapalı olamaz (D-008/4) |
| Odoo dokümantasyonu | CC BY-SA 4.0 | Okuyup işlev tanımı çıkarmak. Metin kopyalarsak atıf + aynı lisans | Kendi belgelerimize metin kopyalanırsa atıf ve CC BY-SA |
| Kendi özgün modüllerimiz | **AGPL-3** (D-016); depo kökünde `LICENSE` | Serbest (telif sahibi biziz) | Dağıtılan ve ağ üzerinden sunulan sürümlerde AGPL-3 koşulları. Gelecek sürümlerin lisansı yalnız bize ait kod için değiştirilebilir; bu yüzden dış katkı şimdilik kabul edilmez |

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
  - Dış demo, pilot ve satıştan önce kalıcı adla değiştirilir (PLAN T8.2).
  - Public GitHub depo adı da o adımda yeniden adlandırılır; GitHub eski adresi yeni adrese yönlendirir.

## 4. Veri ve mevzuat

- **e-Belge saklama:** asıl saklama Türkiye'de zorunlu; başkasının e-Belgesini saklamak GİB izni gerektirir (`research/e-fatura.md` §3).
- **KVKK:** müşteri = veri sorumlusu, biz (SaaS) = veri işleyen. Yurt dışı sunucu → m.9 süreçleri (`research/hosting.md`).
- **odoo.com'a veri gönderimi:** Community'de odoo.com'a veri gönderen bileşenler (yayıncı garantisi, IAP) ürünümüzde kapatılır veya kendi sağlayıcılarımızla değiştirilir (PLAN T2.3). Bu, otomatik testle denetlenir (PLAN T2.7). Müşteri verisi bizim bilgimiz dışında 3. tarafa gitmemelidir.
- **Public depo (D-015):** depodaki her şey herkese açık.
  - Depoya girmeyecekler: gizli bilgi (API anahtarı, şifre, sertifika), müşteri veya test kişisinin gerçek verisi, gerçek VKN/TCKN, yerel yapılandırma (`.env`, `odoo.conf`).
  - Nilvera test portalının test bilgileri kamuya açık bir belgede yayımlanmış olsa da depoya yazılmaz; yalnız `.env`'de tutulur.
  - Yeniden dağıtım izni belirsiz dış dosyalar (ör. GİB UBL-TR XSD/schematron paketleri) depoya konmaz; CI'da kaynağından indirilir (PLAN T4.2).
  - Her push'tan önce `git diff --cached` ile denetlenir; CI'da gizli bilgi taraması yapılır (PLAN T1.10).
- **Depo lisansı (D-016):**
  - Depo kökündeki `LICENSE` GNU AGPL v3 metnidir; aksi belirtilmeyen tüm özgün içerik bu lisansla yayımlanır.
  - Depo ileride private yapılırsa, o güne kadar yayımlanmış sürümler AGPL-3 altında kalır.
  - Dış katkı (pull request) şimdilik kabul edilmez (README "Katkı").

## 5. Lisans envanteri

Projeye giren her dış kod buraya yazılır. Depoya girmeyen ama geliştirme ortamında kullanılan araçlar ayrı tabloda.

| Bileşen | Sürüm/commit | Lisans | Değiştirildi mi? | Nerede |
|---|---|---|---|---|
| (henüz dış kod yok — upstream PLAN T1.4'te eklenecek) | | | | |

**Geliştirme ortamı araçları (depoya girmez, ürünle dağıtılmaz):**

| Araç | Sürüm | Lisans | Not |
|---|---|---|---|
| PostgreSQL sunucusu ve komut satırı araçları (EDB Windows ikili zip) | 18.6 | PostgreSQL License (izin verici) | T1.3. Zip içindeki pgAdmin 4 ve StackBuilder kullanılmıyor. |
