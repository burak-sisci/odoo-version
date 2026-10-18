# e-Fatura / e-Arşiv / e-İrsaliye Araştırması

Son güncelleme: 2026-10-18
Araştırma tarihi: 2026-10-18
İlgili karar: D-012 (DECISIONS.md)

> **Sonuç (2026-10-18):** D-012 Geçerli.
> - MVP kapsamı e-Fatura + e-Arşiv; gönderim mevcut bir özel entegratörün API'si üzerinden.
> - Mimari: entegratörden bağımsız çekirdek + adaptör; ilk adaptör Nilvera (19.0 LGPL port).
> - Gönderim yöntemi MVP sonunda yeniden ele alınacak (ROADMAP T6.1).

> Bu belge hukuki görüş değildir. Satışa çıkmadan önce bir mali müşavir/avukat ile doğrulanmalıdır (ROADMAP T6.2).
> Birincil kaynak: GİB'in yayımladığı **509 Sıra No.lu VUK Genel Tebliği'nin güncel (konsolide) metni** (2026),
> 589 Sıra No.lu Tebliğ değişiklikleri dahil (RG 31/12/2025, sayı 33124, 5. mükerrer). Bölüm numaraları bu metne aittir.

## 1. Kimler zorunlu?

### e-Fatura (509 Tebliğ IV.1.4)

- Brüt satış hasılatı **2022 ve sonrası dönemler için 3 Milyon TL** ve üzeri olan mükellefler (a-1).
- İnternet üzerinden satış yapanlar, e-ticaret aracı hizmet sağlayıcıları, internet ilan ve reklam aracıları: **500 Bin TL** ve üzeri (a-4).
- Gayrimenkul ve/veya motorlu taşıt inşa, imal, alım, satım, kiralama ve aracılık: **500 Bin TL** ve üzeri (a-7).
- Hasılat şartı olmadan: EPDK lisanslılar, ÖTV (I) ve (III) sayılı listedeki mal imalatçıları/ithalatçıları, sebze-meyve komisyoncu/tüccarları,
  SGK ile sözleşmeli sağlık hizmeti sunucuları ve medikal tedarikçiler, belgeli konaklama tesisleri (a-2, a-3, a-5, a-6, a-8).
- Geçiş: şartın sağlandığı dönemi izleyen yılın 7. ayının başına kadar (ör. 2025 hasılatı → 1 Temmuz 2026). Bu tarih örneği ikincil kaynaktan (Finrota) alınmıştır.

### e-Arşiv ve kâğıt faturanın sonu (509 Tebliğ IV.2.4.3, 589 ile değişik)

e-Arşiv'e dahil olmayan mükelleflerin düzenlediği faturalar GİB portalinden e-Arşiv olarak düzenlenmek zorundadır:

| Mükellef | Dönem | Kural |
|---|---|---|
| Bilanço esası vb. | 1/1/2025 – 31/12/2025 | Vergiler dahil 3.000 TL'yi aşan faturalar |
| Bilanço esası vb. | **1/1/2026'dan itibaren** | **Tutarına bakılmaksızın tüm faturalar** |
| Basit usul ve işletme hesabı esası | 1/1/2025 – 31/12/2026 | Vergiler dahil 3.000 TL'yi aşan faturalar |
| Basit usul ve işletme hesabı esası | **1/1/2027'den itibaren** | Tutarına bakılmaksızın tüm faturalar |

**Sonuç:** 2026'dan itibaren bilanço esasına göre defter tutan bir şirket kâğıt fatura kesemez. 2027'den itibaren neredeyse hiçbir işletme kesemez.

### e-İrsaliye (509 Tebliğ IV.3.5)

- e-Fatura'ya kayıtlı olup brüt satış hasılatı **2021 ve sonrası için 10 Milyon TL** ve üzeri olanlar, ayrıca sektörel gruplar.
- Geçiş: izleyen hesap döneminin 7. ayının başı.

### e-Defter

- İkincil kaynağa göre (Finrota): e-Fatura'ya geçen bilanço esaslı mükellefler, geçiş yılını izleyen yılın başından itibaren e-Defter tutar.
- e-Defter ayrı tebliğle düzenlenir. **Doğrulanmadı.**

## 2. Nasıl gönderilir? (509 Tebliğ V.1)

| Yöntem | Açıklama | Bizim için |
|---|---|---|
| GİB Portal | GİB'in ücretsiz web arayüzü (V.1.1) | ERP'den otomatik gönderim için resmi API yok; kullanıcı faturayı ikinci kez elle girer. Satılabilir ürün için yeterli değil (en fazla geçici çözüm) |
| Özel Entegratör | GİB izinli firmaların sistemleri üzerinden (V.1.2). Gönderim/alım altyapısı **Türkiye sınırları içinde olmak zorunda** | **Uygun yol.** ERP entegratörün API'sini çağırır. Entegratör ücretini müşteri öder |
| Doğrudan Entegrasyon | Mükellefin kendi sistemini GİB'e bağlaması; GİB'in belirlediği şartlar, 1 yıl içinde entegrasyon (V.1.3) | Büyük mükellefler için. Bizim için değil |

### Özel entegratör olmak?

Başvuru dilekçesi, Özel Entegrasyon Bilgi İşlem Sistem Raporu (BİS), teknik kılavuzlara uygun altyapı (V.1.2).
İkincil kaynaklara göre ayrıca TÜBİTAK BİLGEM uygunluk raporu ve (29 Haziran 2026 tarihli güncel kılavuzla) TÜRKAK onaylı
ISO 27001 / 22301 / 20000 belgeleri gerekiyor. **Sıfır bütçeyle mümkün değil → mevcut entegratörlerle entegre olacağız.**

## 3. Saklama (509 Tebliğ VI)

- "e-Belgelerin muhafazasının Türkiye Cumhuriyeti sınırları içerisinde ve Türkiye Cumhuriyeti kanunlarının geçerli olduğu yerlerde yapılması zorunludur. Bu zorunluluk yurt dışında ikincil bir arşivleme yapılmasına engel teşkil etmez."
- Başka mükelleflerin e-Belgelerini saklama hizmeti vermek GİB'den **saklama izni** gerektirir.
- **Ürün için anlamı:** Yasal arşivi entegratör tutar (entegratörlerin bu hizmeti var). Bizim SaaS veritabanımızdaki kopya operasyonel kopyadır; kendimizi "yasal saklama hizmeti" olarak konumlandırmayız. Yine de üretim sunucusunun Türkiye'de olması en güvenli yoldur (bkz. `hosting.md`).

## 4. Odoo'daki mevcut durum

| Sürüm | Türkiye e-Belge modülleri | Lisans |
|---|---|---|
| 18.0 Community | l10n_tr_nilvera, _einvoice, _einvoice_extended, _edispatch | LGPL-3 |
| 19.0 Community | yukarıdakiler + l10n_tr_nilvera_base_vat | LGPL-3 |
| 20.0 Community | yalnız `l10n_tr` (hesap planı, vergiler, vergi daireleri) | LGPL-3 |
| 20.0 Enterprise | Nilvera e-Fatura "yalnız Enterprise" (Odoo 20 sürüm notları) | Özel mülk |

19.0 LGPL modüllerinin içeriği:
- Nilvera API istemcisi (canlı: `api.nilvera.com`, test: `apitest.nilvera.com`).
- GİB etiketi (alias) yönetimi.
- UBL-TR fatura XML üretimi (`tools/ubl_tr_invoice.py`).
- e-Fatura ve e-Arşiv senaryoları; tevkifat, istisna, ihracat ve çoklu döviz test XML'leri.
- e-İrsaliye (`stock.picking`), dorse plakası, gelen fatura içe aktarma.

**Önemli:** 19.0'daki LGPL izni geri alınamaz. Bu modülleri 20.0'a taşımak (port) yasaldır. Taşınan kod LGPL-3 kalır ve Odoo S.A. telif notları korunur. Enterprise 20.0 sürümünün koduna **bakılmaz** (D-006).

OCA `l10n-turkey` deposu: 18.0 ve 19.0 dallarında modül yok.

## 5. Bizim amacımız açısından değerlendirme

| Belge | Gereklilik | Gerekçe |
|---|---|---|
| e-Fatura + e-Arşiv | **Zorunlu (MVP)** | Türkiye'de B2B müşterilerin büyük kısmı e-Fatura mükellefi. 2026'dan itibaren bilanço esaslı şirketler kâğıt fatura kesemiyor. Bu özelliği olmayan bir ERP'nin fatura modülü kullanılamaz; ürün satılamaz |
| e-İrsaliye | Yüksek (2. aşama) | Stok/dağıtım yapan ve 10 Milyon TL üstü hasılatlı müşteriler için zorunlu |
| e-Defter | Orta (ileride) | Çoğu KOBİ e-Defter'i mali müşavirinin yazılımında tutuyor. Tam muhasebe hedefi için ileride |
| e-SMM, e-Müstahsil vb. | Düşük | Niş müşteri grupları |

**Maliyet:** Entegratör kontör/paket ücretini son müşteri öder (müşteri entegratörle kendisi sözleşme yapar). Biz yalnız API bağlantısını sağlarız → bize bütçe yükü yok.
Geliştirme için Nilvera test ortamı var. Test hesabı koşulları **doğrulanmadı**.

**Mimari öneri:** entegratörden bağımsız bir e-Belge çekirdeği (UBL-TR üretimi, senaryolar, fatura tipleri, mükellef sorgulama, durum takibi) + entegratör başına adaptör modülü. İlk adaptör: Nilvera (19.0 LGPL kodundan port). Diğer entegratörler pazara göre eklenir.

## Kaynaklar

- GİB — 509 Sıra No.lu VUK Genel Tebliği, güncel metin (2026): https://cdn.gib.gov.tr/api/gibportal-file/file/getFile?objectKey=MEVZUAT_TEBLIGLER%2FUNIVERSAL%2F2026%2FMEVZUAT_TEBLIGLER_2026_VukTeb509_Guncel.pdf
- 589 Sıra No.lu Tebliğ özeti: https://www.muhasebetr.com/guncelmevzuat/mevzuat_oku.php?mevzuat_id=7116
- TÜRMOB sirküleri 02.01.2026/16-1: https://www.turmob.org.tr/ekutuphane/Read/9208c1d3-f311-468d-9dd7-0d50a202bd6c
- Finrota (ikincil): https://finrota.com/blog/2026-e-fatura-zorunluluk-limitleri-ve-gecis-rehberi
- Paraşüt (ikincil): https://www.parasut.com/blog/e-fatura-ve-e-arsiv-zorunlulugu
- Özel entegrasyon kılavuzu güncellemesi (ikincil): https://musavirlerkulubu.com.tr/makale/e-fatura-ozel-entegrasyon-kilavuzu-guncellendi-iso-belgesi-sarti-geldi
- Odoo 20 sürüm notları: https://www.odoo.com/odoo-20-release-notes
- Odoo 19.0 Nilvera modülleri: https://github.com/odoo/odoo/tree/19.0/addons/l10n_tr_nilvera_einvoice
- Ücretli 3. parti örnek: https://apps.odoo.com/apps/modules/18.0/parasut
