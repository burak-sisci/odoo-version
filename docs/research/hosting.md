# Barındırma (Hosting) Seçenekleri

Son güncelleme: 2026-10-18
İlgili karar: D-013 (DECISIONS.md)

> **Sonuç (2026-10-18):** D-013 **Ertelendi**. Karar noktası: ROADMAP T6.3 (ilk pilot müşteriden önce).
> O zamana kadar geliştirme lokal, demolar ücretsiz yöntemlerle. Mimari sağlayıcıdan bağımsız kurulur.

> Hukuki noktalar bilgi amaçlıdır; satıştan önce avukatla doğrulanmalıdır (ROADMAP T6.2).

## Karar ne zaman gerekli?

**Şimdi gerekli değil.** Bunun üç nedeni var:
1. Geliştirme bu bilgisayarda yapılıyor ve gerçek müşteri verisi yok.
2. Mimari sağlayıcıdan bağımsız: değiştirilmemiş Odoo + modüller, standart Linux + PostgreSQL üzerinde her yerde aynı çalışır.
3. Taşınmanın maliyeti düşük: veritabanı yedeği ve filestore yeni sunucuya geri yüklenir.

**Kararın gerektiği an:** ilk gerçek müşteri verisinin işleneceği an, yani pilot (T6.3). KVKK ve e-Belge saklama kuralları gerçek veriyle devreye girer; sunucu ücreti de o zaman doğar.

**Şimdiden dikkat edilenler:**
- Bulut sağlayıcısına özel yönetilen servis kullanılmaz.
- Geliştirme Windows'ta yapılıyor, üretim Linux olacak. Kritik testler ileride Linux'ta da çalıştırılır (WSL2 veya CI).

## Belirleyici kısıtlar

1. **Sıfır bütçe (D-005):** ilk gelire kadar ücretli altyapı yok.
2. **e-Belge saklama:** e-Belgelerin asıl saklaması Türkiye sınırları içinde zorunlu. Yurt dışında yalnız ikincil arşiv serbest (509 Tebliğ VI, bkz. `e-fatura.md` §3).
3. **KVKK yurt dışı aktarım:** 7499 sayılı Kanun ile değişen KVKK m.9 (yürürlük 1 Haziran 2024) şunları istiyor:
   - yeterlilik kararı, ya da uygun güvenceler, ya da arızi aktarım şartları;
   - standart sözleşme kullanılırsa, imzadan sonra 5 iş günü içinde Kurum'a bildirim.

   Sunucu yurt dışındaysa her müşteri (veri sorumlusu) için bu süreç işler. Bu bir satış engelidir.
4. **Odoo gereksinimleri:** Linux sunucu önerilir. PostgreSQL ≥16, Python 3.12+. Kalıcı disk (filestore) ve düzenli yedek gerekir.

## Benzer platformlar nerede çalışıyor? (araştırma: 2026-10-18)

| Platform | Nerede çalışıyor | Not |
|---|---|---|
| **Odoo Online / Odoo.sh** (Odoo S.A.) | Kendi veri merkezi yok. OVHcloud ve Google Cloud kullanıyor; AB dışı bölgelerde AWS de var. Bölgeler: Amerika (ABD, Kanada), Avrupa (Fransa, Belçika), Asya-Pasifik (Singapur, Tayvan), Orta Doğu ve Güney Asya (Hindistan, Suudi Arabistan), Okyanusya (Avustralya). Yedekler Avrupa'da, çoğu bölge için ayrıca Kanada'da | Türkiye bölgesi yok. Müşteri veritabanı en yakın bölgede tutuluyor. Ayrıca müşterinin kendi sunucusuna kurulum (on-prem) seçeneği var |
| **ERPNext / Frappe Cloud** | AWS ve Oracle Cloud üzerinde ~13 bölge: Mumbai, Singapur, Cidde, Bahreyn, BAE, Cakarta, Kuzey Virginia, Londra, Zürih, Frankfurt, Cape Town, Johannesburg, Sidney | Türkiye bölgesi yok. Müşterinin kendi sunucusu (self-hosted / hybrid) da destekleniyor |
| **Paraşüt** (Türkiye, bulut ön muhasebe) | Aydınlatma metninde sunucu yeri ve sağlayıcı adı yok. Metin, saklama ve teknik altyapı desteği için verinin yurt dışındaki hâkim hissedara ve yurt içi/yurt dışı tedarikçilere aktarılabileceğini söylüyor; yurt dışı aktarım için açık rızaya dayanıyor | Yerli bir oyuncu bile verinin bir kısmını yurt dışında tutabiliyor ve bunu KVKK süreciyle çözüyor |
| **Logo** (Logo Cloud / Logo Edge) | Tamamen bulut ürünler (Logo Cloud) ile müşterinin kendi sunucusunda çalışan ve buluta bağlanan ürünler (Logo Edge) birlikte. Veri merkezi konumu bulduğumuz kamuya açık kaynaklarda yok | Karma model: bulut + on-prem |

**Çıkarımlar:**
1. Hiçbiri işe kendi veri merkeziyle başlamamış, sunucu kiralıyorlar. Odoo S.A. bile OVH, Google ve AWS kullanıyor.
2. Uluslararası platformların Türkiye bölgesi yok. Türk müşterisi KVKK yurt dışı aktarım sürecini kendisi yürütmek zorunda. Türkiye'de barındırma bu yüzden bizim için bir satış argümanı olabilir.
3. Hepsi bulut ve on-prem seçeneklerini birlikte sunuyor. Bizim mimarimiz (değiştirilmemiş Odoo + modüller) ikisine de uygun.
4. **Açık soru (T6.2'de netleşecek):**
   - Özel entegratörler e-Belgeleri kendi Türkiye altyapılarında saklıyor.
   - Bizim sistemimizde duran kopya hukuken "asıl saklama" sayılırsa yer Türkiye olmak zorunda. "İkincil arşiv" sayılırsa yer serbest.
   - Cevap, barındırma kısıtının ne kadar katı olduğunu belirleyecek.

## Seçenekler

| # | Seçenek | Maliyet | Avantajlar | Dezavantajlar | Uygun kullanım |
|---|---|---|---|---|---|
| 1 | **Bu bilgisayar (lokal)** | 0 | Hızlı geliştirme döngüsü, tam kontrol | Müşteri erişemez; bilgisayar kapanınca durur; Windows üretim için önerilmez | Geliştirme ve test (**şimdi**) |
| 2 | **Lokal + Cloudflare Tunnel** | 0 (sabit adres için alan adı gerekir) | Ücretsiz HTTPS, port açmadan dışarıya demo | PC açık olmalı; ev interneti; üretim verisi için uygun değil | Potansiyel müşteriye demo |
| 3 | **Ücretsiz bulut katmanları** (ör. Oracle Cloud Always Free) | 0 | 7/24 açık, gerçek Linux sunucu | Koşullar değişebilir; hesap/kaynak geri alınabilir; bölge büyük olasılıkla yurt dışı (KVKK + e-Belge kuralı) | Pilot/demo. Ödeme yapan müşteri verisi için değil |
| 4 | **Yurt dışı VPS** (Hetzner, DigitalOcean vb.) | Düşük aylık ücret | Ucuz, güvenilir, iyi araçlar (snapshot, API) | KVKK yurt dışı aktarım süreci; e-Belge asıl saklama kuralı | Türkiye dışı müşteriler veya yedek |
| 5 | **Türkiye'de VPS/bulut** (yerli veri merkezleri) | Aylık ücret (ilk gelirden karşılanır) | KVKK ve e-Belge kuralları açısından en temiz yol; "verileriniz Türkiye'de" satış argümanı; düşük gecikme | Ücretli; sağlayıcıya göre araç ve güvenilirlik farkı (snapshot ve yedek desteği olan seçilmeli) | **Üretim SaaS** |
| 6 | **Müşterinin kendi sunucusu (on-prem)** | Bize 0 | Veri müşteride; bazı kurumsal müşteriler bunu şart koşar; barındırma maliyeti yok | Müşteri başına kurulum, yükseltme ve destek yükü; Python kaynak kodu müşteride görünür; LGPL dağıtım yükümlülükleri devreye girer; düzenli gelir zorlaşır | İleride, büyük müşteriler için opsiyon |

## SaaS'ta çok kiracılı yapı (Odoo'nun kendi yöntemi)

- Tek Odoo sunucusu, **müşteri başına ayrı PostgreSQL veritabanı**.
- Alt alan adına göre veritabanı seçimi (`dbfilter = ^%d$`; `musteri1.marka.com` → `musteri1` veritabanı); `list_db = False`.
- Önde ters vekil (Caddy/nginx), wildcard TLS (Let's Encrypt — ücretsiz).
- Avantaj: düşük maliyet, tek kod tabanı, kolay yedekleme. Dezavantaj: tüm müşteriler aynı modül sürümünde olmalı; ağır bir müşteri diğerlerini etkileyebilir (işçi/worker ayarı ve izleme gerekir).

## Ön öneri (aşamalı — karar T6.3'te verilecek)

1. **Şimdi:** geliştirme bu bilgisayarda (Seçenek 1). 0 TL.
2. **Demo dönemi:** Seçenek 2 veya 3, yalnız müşteri verisi içermeyen demo verisiyle. 0 TL.
3. **İlk pilot / ödeme yapan müşteri (T6.3):** Seçenek 5, Türkiye'de sunucu. Maliyet ilk gelirden karşılanır, böylece sıfır bütçe kuralı bozulmaz.
4. **İleride:** büyük müşteriler için Seçenek 6 opsiyonu.

## Kaynaklar

- KVKK standart sözleşme duyurusu: https://www.kvkk.gov.tr/Icerik/7938/Standart-Sozlesmeler-ve-Baglayici-Sirket-Kurallarina-Iliskin-Dokumanlar-Hakkinda-Kamuoyu-Duyurusu
- KVKK standart sözleşme bildirim modülü: https://www.kvkk.gov.tr/Icerik/8043/Standart-Sozlesme-Bildirim-Modulu-Hakkinda-Kamuoyu-Duyurusu
- 509 Sıra No.lu VUK Genel Tebliği güncel metin (GİB): https://cdn.gib.gov.tr/api/gibportal-file/file/getFile?objectKey=MEVZUAT_TEBLIGLER%2FUNIVERSAL%2F2026%2FMEVZUAT_TEBLIGLER_2026_VukTeb509_Guncel.pdf
- Odoo dağıtım dokümanı: https://www.odoo.com/documentation/20.0/administration/on_premise/deploy.html
- Odoo gizlilik politikası (barındırma bölgeleri ve alt işleyenler): https://www.odoo.com/privacy
- Odoo güvenlik sayfası: https://www.odoo.com/security
- Odoo Cloud SLA: https://www.odoo.com/cloud-sla
- Frappe Cloud (bölgeler): https://frappe.io/cloud
- Paraşüt aydınlatma metni: https://www.parasut.com/kisisel-verilerin-korunmasi-ve-islenmesine-iliskin-aydinlatma-metni
- Logo ürün mimarisi (Logo Cloud / Logo Edge): https://www.capital.com.tr/haberler/tum-haberler/logo-yazilim-urun-mimarisini-yeniden-yapilandirdi
