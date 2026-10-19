# Plan ve İlerleme

Son güncelleme: 2026-10-19
İlgili kararlar: D-005, D-011, D-012, D-013, D-014, D-016, D-017, D-018, D-019, D-020, D-021

Bu dosya projenin **tek plan ve ilerleme belgesidir**. İlerleme buradan takip edilir.

- **Görev işaretleri:** `[x]` tamam · `[~]` devam ediyor · `[ ]` yapılacak · `[!]` kullanıcı kararı/eylemi bekliyor.
- **Görev satırı:** `T<faz>.<sıra> Ad · Boyut · Kategori`. Altındaki maddeler çıktıyı ve kabul ölçütünü verir.
- **Boyut (kaba tahmin):**
  - S ≈ 1 çalışma oturumu;
  - M ≈ 2–3 oturum;
  - L ≈ 4–8 oturum;
  - XL > 8 oturum (başlarken alt görevlere bölünür).
- **Kategori (D-021):** her görev üç kategoriden birindedir.
  1. **K — kullanıcının yapacakları.** Yalnız kullanıcının yapabileceği işler: müşteri ilişkisi, yasal işlemler, kişisel başvurular, ödeme.
  2. **B — birlikte yapılacaklar.** Kullanıcının kararı, bilgisi veya onayı gereken işler. Standart mesaide yapılır.
  3. **C — Claude'un yapacakları.** Claude'un tek başına yapabileceği işler. Otonom mesaide yapılabilir. Görevin içinde bir onay adımı varsa (ör. yayın), o adım `USER_TASKS.md`'ye yazılır; görevin geri kalanı C kalır.
- Kullanıcıdan beklenen her şey (K ve B görevleri, eylemler, sorular, onaylar): **`USER_TASKS.md`**.
- Pano sayıları, kategori sayıları ve faz işaretleri `tools/check_docs.py` ile görev satırlarına karşı denetlenir.

## 1. İlerleme panosu

**Şu anki görev:** T2.3 — odoo.com bağlantılarının kesilmesi

| Faz | Ad | Aşama | Kilometre taşı | Durum | Görev | K · B · C |
|---|---|---|---|---|---|---|
| F0 | Araştırma ve planlama | Bütçesiz | M0 Plan hazır | `[x]` | 8/8 | 0 · 2 · 6 |
| F1 | Geliştirme altyapısı ve CI | Bütçesiz | M1 Geliştirme altyapısı | `[x]` | 11/11 | 0 · 0 · 11 |
| F2 | Marka katmanı | Bütçesiz | M2 Markasız çekirdek | `[~]` | 2/7 | 0 · 0 · 7 |
| F3 | Türkiye temel yerelleştirmesi | Bütçesiz | M3 Türkiye temeli | `[ ]` | 0/9 | 0 · 0 · 9 |
| F4 | e-Belge (e-Fatura, e-Arşiv, e-İrsaliye) | Bütçesiz | M4 e-Belge test ortamında | `[ ]` | 0/11 | 0 · 0 · 11 |
| F5 | Ticaret paketi: muhasebe, cari, raporlar | Bütçesiz | M5 Ticaret paketi | `[ ]` | 0/10 | 0 · 0 · 10 |
| F6 | Üretim paketi | Bütçesiz | M6 Üretim paketi | `[ ]` | 0/8 | 0 · 0 · 8 |
| F7 | Kullanıma hazır ürün | Bütçesiz | M7 Kullanıma hazır | `[ ]` | 0/9 | 0 · 1 · 8 |
| F8 | Satışa hazırlık | Bütçesiz | **M8 Satışa hazır (müşteri arayışı kapısı)** | `[ ]` | 0/12 | 0 · 4 · 8 |
| F9 | Müşteri arayışı ve ilk müşteri | Müşteri | M9 İlk müşteri | `[ ]` | 0/8 | 3 · 4 · 1 |
| F10 | Self-servis SaaS | Büyüme | M10 Self-servis SaaS | `[ ]` | 0/7 | 0 · 1 · 6 |
| F11 | Genişleme (sürekli, P1 ve sonrası) | Sürekli | — | `[ ]` | 0/14 | 0 · 1 · 13 |

**Toplam:** 21/114 görev · Kullanıcı 3 · Birlikte 13 · Claude 98

**Okuma notu:**
- F0–F8 sıfır bütçeyle, müşterisiz ve dış destek olmadan yapılır (D-005, D-017).
- F0–F8'deki işin büyük kısmı Claude'un (C). Kullanıcının bu aşamadaki işi: kararlar ve onaylar (B), isteğe bağlı eylemler (`USER_TASKS.md`).
- F9'dan itibaren para gerektiren işler başlar; maliyetler müşteri gelirinden karşılanır. Bu fazda kullanıcı ön planda.
- F11'deki P1 görevleri M8'den önce de yapılabilir, ama F1–F8'deki işi bekletmez.
- Mesai türleri (D-021): standart mesaide birlikte, otonom mesaide Claude tek başına çalışır. Otonom mesaide C görevleri PLAN sırasıyla yapılır; bağımlılığı karşılanmamış görev atlanır.

## 2. Bağlam ve strateji

### 2.1 Başlangıç koşulları

- Öğrenci projesi. Ekip: kullanıcı (ürün sahibi) + Claude (otonom geliştirici) (D-003). Çalışma standart ve otonom mesailerle yürür (D-021).
- Bütçe sıfır (D-005). Ücretsiz kaynaklar §7'de.
- Depo public ve AGPL-3 lisanslı (D-015, D-016).
- Ürünün kalıcı adı **Nexus** (D-014). Depo ve geliştirme ortamı şimdilik çalışma adı `odoo-version`'ı kullanıyor; bu ad hiçbir kullanıcı yüzeyine çıkmaz, depo T8.2'de yeniden adlandırılır.

### 2.2 Hedef müşteriler (D-017)

"Bugün ne kullanıyor" ve "satın alma kararı" satırları varsayımdır. Müşteri görüşmelerinde doğrulanacak (T9.2).

| | S1 — Küçük işletme | S2 — Orta ölçekli fabrika |
|---|---|---|
| Profil | Ticaret veya hizmet; 1–20 çalışan; muhasebe çoğunlukla dış mali müşavirde | Üretim; yaklaşık 20–250 çalışan; çoğunda iç muhasebe birimi |
| Bugün ne kullanıyor (varsayım) | Excel, bulut ön muhasebe programları, GİB portalı | Hazır muhasebe/ERP paketi + Excel; üretim planı çoğu zaman Excel'de |
| Temel ihtiyaç | Teklif → sipariş → fatura, e-Fatura/e-Arşiv, cari, stok, tahsilat, çek/senet | S1'in hepsi + ürün ağacı, üretim planlama, maliyet, kalite, bakım, lot izleme, e-İrsaliye |
| Yasal yükümlülük (§4) | e-Arşiv (2026/2027'den itibaren neredeyse herkes); çoğunda e-Fatura | e-Fatura, e-Arşiv, e-İrsaliye (10 Milyon TL eşiği), e-Defter |
| Satın alma kararı (varsayım) | İşletme sahibi; fiyat ve kolaylık | Sahip + muhasebe/üretim yöneticisi; güvenilirlik ve referans |
| Bizim paketimiz (§3) | **Ticaret** | **Üretim** |

### 2.3 Büyüme merdiveni (D-017)

| Basamak | Müşteri | Amaç | Bu basamakta ne olur |
|---|---|---|---|
| 0 (bugün) | — | M8: satışa hazır ürün | F0–F8; bütçesiz |
| 1 | 1–3 pilot (yakın çevre) | Gerçek kullanım, referans, ilk gelir | İndirimli kurulum karşılığında referans ve geri bildirim. İlk gelir sunucuya, hukuki incelemeye ve şirket giderlerine gider (F9) |
| 2 | 5–10 ücretli küçük işletme / fabrika | Düzenli gelir | Kurulum ve destek süreci olgunlaşır; self-servis SaaS (F10) |
| 3 | Daha büyük fabrikalar (çok şirket, çok depo) | Büyük sözleşmeler | P1/P2 özellikler: çok seviyeli MRP, e-Defter, onaylar, ikinci entegratör (F11) |
| 4 | Kurumsal müşteriler / iş ortakları | Ölçek | P3–P4 özellikler, iş ortağı ağı |

Her basamağa, bir önceki basamaktaki satış veya anlaşmadan sonra geçilir. Strateji ilk müşteriden sonra yeniden değerlendirilir (T9.8).

### 2.4 Konumlandırma

- **Hepsi bir arada:** ön muhasebe, e-Belge, stok ve üretim tek sistemde.
- **Kullanıcı başı lisans ücreti yok:** yazılım açık kaynak (AGPL-3); ücret hizmet içindir.
  - Üst fiyat referansı: Odoo Enterprise yaklaşık 31 $/kullanıcı/ay (`docs/research/planning-inputs.md`).
- **Türkiye'ye özgü:** Türkçe arayüz, e-Belge, çek/senet, TCMB kurları, Tekdüzen hesap planı.
- **Veri sahipliği:** müşteri isterse sistem kendi sunucusunda çalışır; kilitlenme yok.

### 2.5 Gelir modeli (öneri — fiyatlar T8.9'da)

| Kalem | Tür | Not |
|---|---|---|
| Kurulum ve veri aktarımı | Tek seferlik | Pilotlarda indirimli |
| Hizmet bedeli | Aylık/yıllık | Barındırma (bizim sunucumuzdaysa), bakım, güncelleme, destek |
| Eğitim | Tek seferlik / saatlik | |
| Özelleştirme | Proje / saatlik | Özel modüller de AGPL-3 (D-016) |
| e-Belge kontörü | — | Müşteri entegratöre doğrudan öder (D-012); biz aracılık yapmayız |

### 2.6 Müşteri arayışına geçiş kapısı (M8)

"Bütçesiz alınabilecek tüm ilerleme" bu kapıyla tanımlanır (D-017): **hedef segmentlere satılabilir en iyi ürün.**
Kapıdan sonra geliştirme durmaz (F11 sürer). Ama müşteri geri bildirimi olmadan eklenen her özelliğin getirisi azalır, yanlış şeyi yapma riski artar.

Kapı ölçütleri (T8.12'de tek tek denetlenir):
1. Ticaret (T5.10) ve Üretim (T6.8) kabul senaryoları otomatik testte ve elle turda geçiyor.
2. e-Fatura, e-Arşiv ve e-İrsaliye entegratör test ortamında uçtan uca çalışıyor. Her UBL-TR çıktısı GİB XSD + schematron doğrulamasından geçiyor (T4.10).
3. Kullanıcıya görünen hiçbir yerde "Odoo" yok, odoo.com'a istek gitmiyor (T2.6, T2.7).
4. Paket modüllerinde Türkçe çeviri ≥ %95 (T3.6 aracıyla ölçülür).
5. Kurulum aracı temiz bir Linux sunucuya tek komutla kuruyor. Yedekten geri yükleme test edildi (T8.4, T8.5).
6. Kalıcı ad (Nexus) her yüzeyde uygulandı; tescil ve alan adı uygunluğu araştırıldı (T8.2).
7. Kullanıcı belgeleri, demo ortamı, fiyat listesi, teklif ve sözleşme şablonları hazır (T8.7–T8.11).
8. CI yeşil; bilinen kritik hata yok.
9. Kullanıcıyla go/no-go kararı verildi.

## 3. Ürün paketleri ve MVP sınırı (D-018)

MVP = M8'de satışa çıkan sürüm. İki paketten oluşur.

### 3.1 Ticaret paketi (S1)

| Alan | İçerik | Kaynak |
|---|---|---|
| Kişiler ve cari | Müşteri/tedarikçi, VKN/TCKN, vergi dairesi, il/ilçe adres; cari ekstre ve mutabakat | Community + F3 + T5.6 |
| Satış | Teklif, sipariş, fiyat listeleri, proforma | Community `sale_management` + T3.7 |
| Satın alma | Talep, sipariş, mal kabul | Community `purchase` |
| Stok | Çoklu depo, lot/seri, sayım, sevkiyat | Community `stock` |
| Fatura ve e-Belge | Satış/alış faturası, e-Fatura, e-Arşiv, e-İrsaliye, gelen e-Fatura | Community `account` + F4 |
| Tahsilat ve ödeme | Kasa, banka, çek ve senet, banka ekstresi içe aktarma, banka mutabakatı | Community + T5.2, T5.3, T5.7 |
| Raporlar | Mizan, muavin, yaşlandırma, bilanço, gelir tablosu, KDV hazırlık | T5.4, T5.5, T5.8 |
| Mali müşavir | Muhasebe fişlerinin dışa aktarımı | T5.9 |
| Döviz | TCMB kurları | T3.5 |
| CRM | Fırsat ve aktivite takibi | Community `crm` |

### 3.2 Üretim paketi (S2) = Ticaret paketi +

| Alan | İçerik | Kaynak |
|---|---|---|
| Üretim | Ürün ağacı, rota, iş merkezi, iş emri, MRP önerileri | Community `mrp` + T6.2 |
| Fason üretim | Fasoncuya malzeme gönderimi ve dönüş (e-İrsaliye ile) | Community `mrp_subcontracting` + T6.7 |
| Maliyet | İş merkezi maliyetleri, standart/ortalama maliyet, 7/A hesap eşleştirmesi | T6.3 |
| Kalite | Giriş, üretim ve sevk kontrolleri | OCA `quality_control_oca` portu (T6.4) |
| Bakım | Önleyici bakım, arıza kayıtları | Community `maintenance` + T6.5 |
| İzlenebilirlik | Hammaddeden müşteriye lot/seri izleme | Community + T6.6 |

### 3.3 MVP'de olmayanlar

Bunlar bilinçli olarak dışarıda. Öncelikleri `docs/MODULE_MATRIX.md` ve F11'de.
- **e-Defter** (P1, T11.4). MVP'de onun yerine mali müşavire aktarım (T5.9) var.
- **Bordro** (P3). Küçük işletmelerde genelde mali müşavir yapıyor.
- **POS / perakende** (P2). Türkiye'de perakende satış yeni nesil ödeme kaydedici cihaz gerektiriyor; önce araştırma (T11.9).
- Web sitesi ve e-ticaret (P2).
- İK'nın temel kayıt dışındaki kısımları (P1–P3).
- Studio, yapay zekâ, OCR (P4–P5).
- Self-servis SaaS kaydı ve otomatik tahsilat (F10).
- İkinci e-Belge entegratörü (P2, müşteri talebine göre).
- Yerel mobil uygulama (PWA yeterli kabul edildi, T7.5).
- İngilizce arayüz kalitesi. Upstream İngilizcesi korunur ama ürün Türkçe öncelikli.

### 3.4 Teslim biçimi

- İlk müşterilerde **yönetilen kurulum**. Her müşterinin ayrı veritabanı olur. İki seçenek:
  - müşterinin kendi sunucusunda (on-prem);
  - bizim yönettiğimiz bir sunucuda. Sunucunun yeri D-013 ile ertelendi (T9.5).
- İki seçenek de aynı kurulum aracını kullanır (T8.4).
- Self-servis SaaS (kayıt, deneme, otomatik ödeme) Basamak 2'den sonra yapılır (F10).

## 4. Türkiye gereksinimleri

Ayrıntılar ve kaynaklar: `docs/research/e-fatura.md`, `docs/research/planning-inputs.md`. Hukuki görüş değildir (T9.4).

| Gereksinim | Kimi etkiler | Plan | Öncelik |
|---|---|---|---|
| e-Fatura (UBL-TR 1.2.1) | Hasılat eşiğini (3 Milyon TL) aşanlar ve sektörel gruplar; onlara fatura kesen herkes | F4 (T4.3, T4.5, T4.7) | P0 |
| e-Arşiv | e-Fatura mükellefi olmayan alıcıya kesilen faturalar; 2026'dan itibaren bilanço esaslılarda tutar sınırı yok | T4.6 | P0 |
| e-İrsaliye | e-Fatura'ya kayıtlı ve hasılatı 10 Milyon TL ve üzeri olanlar + sektörel gruplar | T4.8, T6.7 | P0 |
| e-Defter | e-Fatura'ya geçen bilanço esaslı mükellefler, geçişi izleyen yıl başından (ikincil kaynak) | MVP'de mali müşavire aktarım (T5.9); e-Defter T11.4 | P1 |
| Ba-Bs formları | **Kaldırıldı** (565 Sıra No.lu VUK Genel Tebliği, Eylül 2024 döneminden itibaren) | Gerekmiyor | — |
| Tekdüzen hesap planı, KDV oranları, damga vergisi raporu | Herkes | `l10n_tr` (20.0'da var) + eksikler T3.1–T3.2 | P0 |
| KDV tevkifatı ve istisnalar | Tevkifatlı işlem yapanlar, ihracatçılar | T3.2, T4.3 | P0 |
| VKN / TCKN | Herkes | T3.3 | P0 |
| Vergi dairesi | Herkes (e-Belge'de zorunlu) | `l10n_tr` 20.0'da ~1.046 vergi dairesi var; T3.1'de doğrulanır | P0 |
| İl / ilçe adres | e-Belge adres alanları | 81 il upstream'de var; ilçe T3.4 | P0 |
| Döviz değerlemesi (TCMB kuru) | Dövizli işlem yapanlar | T3.5 | P0 |
| Çek ve senet | Çoğu ticari işletme | T5.7 | P0 |
| Amortisman (VUK oranları) | Demirbaşı olanlar | T11.1 | P1 |
| Enflasyon düzeltmesi | Bilanço esaslılar (güncel kapsam doğrulanmadı) | T11.7 araştırma | P1 |
| Bordro (SGK, gelir/damga vergisi) | İşverenler | T11.13 | P3 |
| KVKK | Biz (veri işleyen) ve müşteri (veri sorumlusu) | T8.10, T9.4, D-013 | P0 (satıştan önce) |
| e-Belge saklama (Türkiye'de) | Herkes | Yasal arşiv entegratörde; sunucu yeri D-013 | P0 |

## 5. Fazlar ve görevler

### F0 — Araştırma ve planlama `[x]`

- [x] T0.1 Odoo kaynak kodu (20.0) ve dokümantasyonunun incelenmesi · L · C — `docs/research/odoo-analysis.md`
- [x] T0.2 Lisans, marka, Community/Enterprise farkları · M · C — `docs/COMPLIANCE.md`
- [x] T0.3 B / C yaklaşım karşılaştırması · M · C — `docs/research/approach-b-vs-c.md`
- [x] T0.4 e-Fatura / e-Arşiv mevzuat araştırması · M · C — `docs/research/e-fatura.md`
- [x] T0.5 Barındırma seçenekleri · S · C — `docs/research/hosting.md`
- [x] T0.6 Proje belgelerinin ve belge denetim aracının oluşturulması · M · C
- [x] T0.7 Açık kararların (D-010 … D-015) kullanıcıyla netleştirilmesi · S · B
- [x] T0.8 Detaylı planlama · M · B — bu belge; D-016 … D-020; `docs/research/planning-inputs.md`

### F1 — Geliştirme altyapısı ve CI `[x]`

**Amaç:** lokal çalışan Odoo 20.0, modül şablonu ve her push'ta testleri çalıştıran CI.
**Kabul (M1):**
- Odoo lokal olarak Türkçe bir veritabanıyla açılıyor.
- Şablondan üretilen örnek modülün testleri lokal ve CI'da geçiyor.
- CI her push'ta şunları çalıştırıyor: belge denetimi, lint, gizli bilgi taraması, modül testleri.

- [x] T1.1 Git deposu ve GitHub public depo (D-015) · S · C
- [x] T1.2 Sürüm doğrulaması (D-011): 19.0 → 20.0 port maliyeti ön analizi · M · C — sonuç: 20.0'da kal; `docs/research/nilvera-port.md`
  - Neden şimdi: sürüm, upstream eklenmeden (T1.4) ve ilk modül yazılmadan önce kesinleşmeli.
  - İçerik:
    - 19.0 LGPL Türkiye e-Belge modüllerinin (`l10n_tr_nilvera*`, `l10n_tr_gib_invoice_scenarios`) boyutu ve 20.0'da değişen API'lere bağımlılığı;
    - MVP'nin ihtiyaç duyduğu OCA modüllerinin (T5.2–T5.6, T6.4) 19.0 → 20.0 port emeği;
    - 20.0'ın destek süresi avantajıyla karşılaştırma.
  - Çıktı: analiz notu (`docs/research/nilvera-port.md`); D-011 kaydının güncellenmesi.
  - Kabul: "20.0'da kal" ya da "19.0'a dön" sonucu gerekçeli ve sayılarla yazılmış.
- [x] T1.3 PostgreSQL kurulumu (Windows, ≥ 16, ücretsiz) · S · C — PostgreSQL 18.6, EDB taşınabilir ikili dosyalar, kullanıcı hesabında; `tools/pg.py`
  - Yönetici izni gerektirmeyen yol tercih edilir (taşınabilir ikili dosyalar, kullanıcı hesabında çalışan sunucu). Olmazsa `USER_TASKS.md`'ye eylem yazılır.
  - Odoo için veritabanı rolü; şifre yalnız yerel yapılandırmada.
  - Kabul: `psql --version` ≥ 16; rol ile bağlantı kuruluyor.
- [x] T1.4 Upstream Odoo'nun (D-011) `upstream/odoo` altına git submodule olarak eklenmesi · M · C — commit `afbcf79d`
  - Sığ klon (`shallow = true`), sabit commit, Windows'ta `core.longpaths`.
  - Lisans envanterine satır (COMPLIANCE §5).
  - Kabul: temiz bir klonda `git submodule update --init --depth 1` çalışıyor; commit `state.json`'da.
- [x] T1.5 Python sanal ortamı ve bağımlılıklar · S · C — `odoo-bin --version` = Odoo Server 20.0
  - `.venv`; upstream `requirements.txt` + kendi `requirements-dev.txt` (test ve lint araçları).
  - Kabul: `odoo-bin --version` çalışıyor.
- [x] T1.6 Odoo'nun yerelde çalıştırılması · S · C — `ov_demo`, Türkçe arayüz ve `TR Company` hesap planı doğrulandı
  - `deploy/odoo.conf.example` depoya girer; yerel `odoo.conf` girmez.
  - Türkçe dil + `l10n_tr` ile demo veritabanı.
  - Kabul: tarayıcıda Türkçe arayüz, Türk demo şirketi ve hesap planı yüklü.
- [x] T1.7 Odoo `skills/` rehberlerinin `.claude/skills/` altına kurulması · S · C — 5 rehber, LGPL-3; öncelik kuralları CLAUDE.md'de
  - Rehberlerin lisansı kontrol edilir ve envantere yazılır.
- [x] T1.8 Test çalıştırma komutları · S · C — `tools/run_tests.py`
  - Tek modül testi ve etiketli test (`--test-tags`) komutları CLAUDE.md "Komutlar" bölümüne yazılır.
  - Windows'ta 20.0 test temizliği salt okunur filestore dosyalarını silemiyor (`tearDownClass` hatası, T1.2). Komutlar bu hatayı ayırt eder; referans sonuç Linux CI'dır (T1.10).
- [x] T1.9 Modül şablonu ve kod kalite araçları · M · C — `tools/new_module.py`, `tools/check_modules.py`, ruff + pylint-odoo + pre-commit
  - Şablon üretici (`tools/new_module.py`). Ürettiği iskelet:
    - manifest: `license`, `author`, sürüm `20.0.x.y.z`;
    - `tests/`, `i18n/tr.po`, `security/ir.access.csv`, `README`.
  - pre-commit: ruff, pylint-odoo; manifest lisans denetimi (D-016 kuralları).
  - Kabul: şablondan üretilen boş modül kuruluyor, testi geçiyor (`tools/run_tests.py`), lint temiz.
- [x] T1.10 GitHub Actions CI (D-020) · M · C — `.github/workflows/ci.yml`; push'ta yeşil, negatif deneme kırmızı
  - Sıra: belge denetimi → lint → gizli bilgi taraması → PostgreSQL servisiyle `addons/` ve `ports/` testleri.
  - Rehber kopyası denetimi: `python tools/sync_skills.py --check` (T1.7).
  - Lint: `pre-commit run --all-files` (ruff, pylint-odoo, modül kuralları, belge denetimi; T1.9).
  - Şablon denetimi: `tools/new_module.py` ile örnek modül üretilir, testleri ve lint'i çalıştırılır (T1.9). Örnek modül depoya girmez.
  - Upstream önbelleği ile çalışma süresi kısaltılır.
  - Kabul: push'ta yeşil. Kasıtlı bir hata CI'ı kırmızıya çeviriyor (negatif deneme).
- [x] T1.11 `vendor/` ve `ports/` düzeni (D-019) · S · C — `vendor/oca/server-ux`, `ports/oca/reporting-engine/report_xlsx`, `tools/port_oca.py`; testler geçiyor
  - `vendor/oca/<depo>`: resmî OCA 20.0, submodule, dokunulmaz.
  - `ports/oca/<depo>/<modül>`: bizim 20.0 portlarımız.
  - Port prosedürü ARCHITECTURE.md'ye yazılır.
  - Portların lint'i: OCA'nın kod biçimi korunur; bizim lint denetimlerimiz yalnız `addons/` (T1.9).
  - Kabul: addons yolu üç kaynağı da içeriyor; örnek bir port kuruluyor.

### F2 — Marka katmanı `[~]`

**Amaç:** kullanıcı hiçbir ekranda Odoo adını veya logosunu görmez; sistem odoo.com'a bağlanmaz (D-007).
**Kabul (M2):**
- Marka sızıntısı testi (en_US + tr_TR) CI'da geçiyor.
- Testler sırasında odoo.com'a giden ağ isteği yok.
- Marka adı (Nexus) tek bir ayardan geliyor. Ad değişirse yalnız bu ayar değişir.

- [x] T2.1 Kullanıcıya görünen Odoo izlerinin envanteri · M · C
  - Kaynak: 20.0 Community kodu. Ekran, dosya ve değiştirme yöntemi listelenir.
  - OCA modüllerinin yazar adı ("Odoo Community Association (OCA)") Uygulamalar ekranında görünüyor. Telif bilgisi olduğu için değiştirilmez (CLAUDE.md kural 2–3). Son kullanıcıdan Uygulamalar menüsünü gizlemek T7.3'te.
  - Çıktı: `docs/research/brand-inventory.md`.
  - Sonuç: bütün yüzeyler modülle değiştirilebiliyor; çekirdek değişikliği gerekmiyor. MVP modülleriyle 97 kurulu modülde 253 çevrilebilir metin "odoo" içeriyor. Yayıncı garantisi haftalık olarak şirket adı, e-posta ve telefonunu da gönderiyor (KVKK).
- [x] T2.2 Marka modülü `ov_brand` · L · C
  - Yapılandırılabilir tek marka adı ve logo.
  - Değişen yerler (envanter §3): pencere başlığı, favicon, giriş ekranı ve bağlantı önizlemesi (Open Graph), PWA manifesti ve simgeleri, çevrimdışı sayfa, pencere ve hata başlıkları, kullanıcı menüsündeki destek bağlantısı, ayarlardaki "hakkında" alanı (Odoo S.A. telif satırı kalır).
  - Kapsam dışı: OdooBot adı ve avatarı `mail` modülüne bağlı, T2.5'e taşındı. Veritabanı yöneticisi veritabanı olmadan çalışır, veritabanına kurulan modüller ona ulaşamaz; üretimde `list_db = False` ile kapalıdır.
  - Sonuç: `addons/ov_brand` (AGPL-3; `web`, `base_setup`). Ürün adı `ov_brand.name` sistem parametresinden, varsayılan Nexus. Renk `#1f5f8b` ve "N" simgesi yer tutucu (K14). Tarayıcıdan tek uygulama olarak kurulumun manifesti de marka renginde. 12 test (ikisi tarayıcıda), Türkçe çeviri.
  - Kalan üç JS metni T2.6'ya taşındı (aşağıda).
- [~] T2.3 odoo.com bağlantılarının kesilmesi · M · C
  - Envanter §4. İlk iş yayıncı garantisi çağrısı.
  - IAP servisleri: SMS, iş ortağı otomatik tamamlama, aday zenginleştirme ve üretme. Modülleriyle kaldırılır (K15 varsayımı).
  - Düzenleyicinin görsel kitaplığı ve yapay zekâ metni; Gmail/Outlook OAuth vekilleri. Kapatılır veya gizlenir.
  - `mysubscription` ("Aboneliğim"): 20.0'da yeni, her veritabanına kendiliğinden kuruluyor; kaldırılır (K15 varsayımı).
  - Enterprise reklamları: ayar ekranları için OCA 20.0 `remove_odoo_enterprise`; Uygulamalar listesindeki satın alınacak uygulama kartları (`to_buy`) için ayrı filtre.
  - odoo.com dokümantasyon/destek bağlantıları.
  - Ara durum:
    - yayıncı garantisi kapandı (`ov_brand_mail`: rapor hiç gönderilmez, zamanlanmış iş pasif);
    - `iap` ve `mysubscription` bağlı modülleriyle kaldırıldı (`ov_brand`): her kurulum ve güncellemenin sonunda kaldırılır, arayüzden kurulamaz, ayar kutuları gizli. `tools/run_tests.py` bu yüzden `ov_brand`'i önce testsiz kurar;
    - Enterprise reklamları kalktı: OCA `remove_odoo_enterprise` (20.0, `vendor/oca/server-brand`) `ov_brand`'in bağımlılığı. Ayarlar'daki Enterprise özellikleri gizli; Uygulamalar listesindeki satın alınacak uygulamalar (`to_buy`) ve ödeme sağlayıcıları aramada hiç dönmüyor;
    - sıradakiler: dokümantasyon ve düzenleyici bağlantıları, Gmail/Outlook vekili, uygulama mağazası.
- [ ] T2.4 `/odoo` URL yolu için modül düzeyinde çözüm · M · C
  - Controller override + JS yönlendirici `patch()` ile markadan bağımsız bir yol; eski yoldan yönlendirme.
  - Modülle çözülemezse kullanıcıya yeni karar olarak getirilir (D-010).
- [ ] T2.5 E-posta, rapor, portal ve web sitesi altbilgileri · M · C
  - "Powered by" ifadeleri, e-posta şablonları, PDF rapor düzenleri (`ov_brand_mail`, `ov_brand_website`).
  - Envanter §6: fatura QR kodunun ortasındaki Odoo logosu, PDF üst verisi (`Creator/Producer`), satın alma portalındaki tanıtım bölümü, özet e-postasının odoo.com'dan yüklenen görseli.
  - OdooBot adı ve avatarı (`base.partner_root`, `mail`; T2.2'den taşındı).
  - PDF motoru seçimi (T1.6 bulgusu): 20.0'da motor eklentili. `base_report_wkhtmltox` kendiliğinden kurulur, ama wkhtmltopdf deposu 2022'den beri arşivde. `base_report_paper_muncher` Odoo'nun yeni motoru (LGPL-3, etkin geliştiriliyor); yalnız Linux ikili dosyaları var. Yerelde ikisi de kurulu değil; PDF denemeleri Linux'ta (CI). Seçim önerisi bu görevde yazılır.
- [ ] T2.6 Otomatik marka sızıntısı testi · M · C
  - Ana sayfaları, e-posta şablonlarını, PDF raporları ve çevirileri tarar.
  - Kullanıcıya görünen metinde "Odoo" = hata. İzin listesi: lisans notları, teknik adlar (envanter §10). E-tablo `ODOO.*` formül adları şimdilik izin listesinde (K13 varsayımı).
  - T2.2'den kalanlar (envanter §3): barkod tarayıcının kamera izni mesajı, rapor işçileri uyarısı, güvensiz bağlam konsol uyarısı. Üçü de upstream yöntemlerinin gövdesinde çevrilebilir metin; `patch()` bütün yöntemi kopyalamayı gerektirir. Metin düzeyinde değiştirme yöntemi bu görevde seçilir.
- [ ] T2.7 Dış istek testi · S · C
  - Odoo test çatısı `requests` ile yapılan dış istekleri zaten engelliyor ve günlüğe yazıyor (envanter §4.2). Kapsamadıkları: kurulum ve zamanlanmış işler, tarayıcı testlerinde sayfanın kendi istekleri.
  - Testler sırasında dış HTTP istekleri kaydedilir; odoo.com alan adlarına istek = hata.

### F3 — Türkiye temel yerelleştirmesi `[ ]`

**Amaç:** e-Belge dışındaki Türkiye ihtiyaçları.
**Kabul (M3):**
- Bir Türk şirketi kurulup e-Belgesiz satış ve alış döngüsü Türkçe olarak tamamlanıyor.
- Hatalı VKN/TCKN girişi uyarı veriyor; adreste il/ilçe seçiliyor.
- TCMB kurları otomatik geliyor.
- Paket modüllerinde Türkçe çeviri ≥ %95.

- [ ] T3.1 `l10n_tr` (20.0) analizi · M · C
  - Bugün var olanlar (2026-10-18 incelemesi): Tekdüzen hesap planı, vergiler, mali pozisyonlar, vergi raporu, damga vergisi raporu, ~1.046 vergi dairesi, 81 il.
  - Çıktı: eksik listesi ve her eksiğin hangi göreve gideceği (`docs/research/l10n-tr.md`).
  - T1.6 demo gözlemleri: bazı hesap adlarında Türkçe büyük harf hatası (`TAHSIL EDILMEYEN ÖDEMELER`); İngilizce kalan hesap ve vergi adları (`Private Sector Bonds, Shares And Notes`, `WH 20% (2/10)`); hesap planı ekranında çevrilmemiş sütun (`Payment Reconciliation`).
- [ ] T3.2 Temel yerelleştirme modülü `ov_l10n_tr` · M · C
  - T3.1'e göre eksik vergi, tevkifat ve istisna tanımları.
  - Türkiye varsayılanları: TRY, Europe/Istanbul, tarih biçimi, hafta başı Pazartesi.
- [ ] T3.3 VKN / TCKN doğrulama · S · C
  - Sağlama algoritması (python-stdnum, Odoo'nun mevcut bağımlılığı).
  - Gerçek kişi / tüzel kişi ayrımı; e-Belge için mükellef türü.
- [ ] T3.4 İl/ilçe adres yapısı · M · C
  - İlçe verisi açık lisanslı bir veri setinden gelir; lisans envanterine yazılır.
  - İlçe seçimi e-Belge adres alanlarıyla eşleşir.
- [ ] T3.5 TCMB döviz kurları `ov_l10n_tr_tcmb` · M · C
  - Günlük zamanlanmış iş (`today.xml`), geçmiş tarih arşivi, alış/satış/efektif seçimi, tatil günü davranışı.
- [ ] T3.6 Türkçe çeviri · L · C
  - Başka modüllerin çevirisini kendi modülümüzle tamamlama/değiştirme yöntemi araştırılır.
  - Ölçüm aracı `tools/po_coverage.py`; CI'da eşik.
  - Paket modüllerindeki eksikler çevrilir. Öncelik: `l10n_tr` (%33), `account`, `sale`, `purchase`, `stock`, `mrp`, `mail`, `web`.
  - Upstream'e çeviri katkısı isteğe bağlı ve kullanıcı onayıyla (K8).
- [ ] T3.7 Türkçe belge çıktıları · M · C
  - Teklif, sipariş, proforma, irsaliye (kâğıt/yedek), tahsilat ve tediye makbuzu.
  - Tutarın yazıyla gösterimi (num2words, Odoo'nun mevcut bağımlılığı); VKN, vergi dairesi, MERSİS alanları.
- [ ] T3.8 Resmî tatiller ve çalışma takvimi · S · C
  - Sabit tatiller + yıllık dini bayram verisi; iş merkezleri ve izin hesapları için.
- [ ] T3.9 Türkiye temeli kabul testi · S · C
  - Otomatik senaryo: şirket kurulumu → teklif → fatura → döviz → raporlar.
  - Çeviri kapsamı raporu.

### F4 — e-Belge (e-Fatura, e-Arşiv, e-İrsaliye) `[ ]`

**Amaç:** D-012'deki e-Belge kapsamı, entegratörden bağımsız çekirdek + adaptör mimarisiyle.
**Kabul (M4):**
- e-Fatura (temel ve ticari), e-Arşiv ve e-İrsaliye Nilvera test ortamında uçtan uca çalışıyor: gönderim, durum, gelen belge, yanıt.
- Üretilen her UBL-TR belgesi GİB XSD + schematron doğrulamasından geçiyor (CI'da).
- CI, sahte entegratörle ağ olmadan tüm akışları test ediyor.

- [ ] T4.1 Nilvera modüllerinin ayrıntılı port planı · M · C
  - T1.2 analizi üzerine dosya dosya plan: çekirdeğe ne gidecek, adaptöre ne gidecek; test XML'leri.
  - Yalnız 19.0 LGPL kod kullanılır; 20.0 Enterprise sürümüne bakılmaz (D-006).
- [ ] T4.2 GİB UBL-TR doğrulama altyapısı · M · C
  - GİB paketlerini (XSD + schematron) indiren, sürümünü ve sağlama toplamını sabitleyen betik.
  - `tools/validate_ubl.py`; schematron XSLT 2 gerektiriyorsa ücretsiz SaxonC-HE.
  - Paketler depoya konmaz (yeniden dağıtım izni belirsiz); CI'da indirilir.
- [ ] T4.3 e-Belge çekirdeği `ov_l10n_tr_edi` (LGPL-3) · L · C
  - UBL-TR 1.2.1 üretimi.
  - Senaryolar (TEMELFATURA, TICARIFATURA, EARSIVFATURA, IHRACAT vb.) ve fatura tipleri (SATIS, IADE, TEVKIFAT, ISTISNA, IHRACKAYITLI vb.).
  - Tevkifat ve istisna kodları, ETTN, numaralama.
  - Mükellef sorgulama arayüzü, durum takibi, adaptör arayüzü.
  - 20.0 farkları (T1.2): `is_company` vergi numarasından hesaplanıyor; Türkiye için 11 haneli TCKN gerçek kişi sayılır (`cac:Person`). Vergi daireleri için çekirdekteki `l10n_tr.tax.office` kullanılır.
- [ ] T4.4 Sahte (mock) entegratör adaptörü · S · C
  - Ağsız çalışır; CI ve demo için. Gerçek entegratörün durum geçişlerini taklit eder.
- [ ] T4.5 Nilvera adaptörü `ov_l10n_tr_edi_nilvera` (LGPL-3) · L · C
  - Kimlik doğrulama, gönderim, durum sorgulama, mükellef (etiket) sorgulama, gelen belge çekme.
  - Test bilgileri yalnız `.env` veya yerel şirket ayarında; depoya girmez.
  - Kabul: test portalında uçtan uca gönderim ve durum.
- [ ] T4.6 e-Arşiv · M · C
  - Gönderim, iptal, internet satışı bilgileri, alıcıya e-posta/PDF.
- [ ] T4.7 Gelen e-Faturalar · M · C
  - Çekme, ticari senaryoda kabul/red, tedarikçi faturası oluşturma, ürün eşleştirme.
- [ ] T4.8 e-İrsaliye `ov_l10n_tr_edispatch` (LGPL-3) · L · C
  - Sevkiyattan irsaliye, taşıyıcı ve plaka, irsaliye yanıtı, gelen irsaliyeden mal kabul.
- [ ] T4.9 Görsel çıktı · M · C
  - XSLT ile önizleme ve PDF; markalı XSLT'nin UBL içine gömülmesi.
- [ ] T4.10 e-Belge kabul testleri · M · C
  - Senaryo matrisi: tip × senaryo × para birimi × tevkifat/istisna.
  - Otomatik testler (sahte adaptör) + test ortamında elle tur; sonuç CHANGELOG'a.
- [ ] T4.11 e-Belge kurulum rehberi · S · C
  - Entegratör hesabı, test → canlı geçiş, sık hatalar. T8.7'de belge sitesine taşınır.

### F5 — Ticaret paketi: muhasebe, cari, raporlar `[ ]`

**Amaç:** S1 için eksiksiz ön muhasebe ve raporlama.
**Kabul (M5):**
- Ticaret kabul senaryosu (T5.10) otomatik testte ve elle turda geçiyor.
- Mizan, muavin, yaşlandırma, bilanço ve gelir tablosu Türkçe ve Tekdüzen düzeninde.
- Mali müşavire aktarım dosyası üretiliyor.

- [ ] T5.1 OCA bağımlılık analizi ve port sırası (D-019) · S · C
  - Gerekli OCA modülleri ve 20.0'da olmayan bağımlılıkları (ör. tarih aralıkları, Excel rapor altyapısı).
  - O tarihte OCA'nın resmî 20.0'a taşıdıkları `vendor/`'a, taşımadıkları `ports/`'a.
- [ ] T5.2 Banka ekstresi içe aktarma · M · C
  - OCA `account_statement_import_file` ve `account_statement_import_sheet_file` portu (19.0).
  - Türk bankaları için Excel/CSV eşleme şablonları. Örnek dosyalar kullanıcıdan (K4), depoya girmez.
- [ ] T5.3 Banka mutabakatı · L · C
  - OCA `account_reconcile_oca` + `account_statement_base` portu; Türkçe.
- [ ] T5.4 Mali raporlar · L · C
  - OCA `account_financial_report` portu: mizan, muavin defter, yaşlandırma, açık kalemler; Excel çıktısı.
  - 20.0'da `account.group` modeli yok; hesap gruplaması `account.account` hiyerarşisine taşınır (T1.2 ölçümü: 12 dosyada 115 atıf).
- [ ] T5.5 Bilanço ve gelir tablosu · M · C
  - OCA `mis_builder` portu (19.0; 20.0 dalındaki yer tutucu, T1.2) ile Tekdüzen şablonları (`ov_l10n_tr_mis_reports`). T1.2 denemesinde 4 küçük uyarlamayla 98/98 test geçti.
- [ ] T5.6 Cari ekstre ve mutabakat · M · C
  - OCA `partner_statement` portu ya da kendi modülümüz; mutabakat mektubu (PDF, e-posta).
- [ ] T5.7 Çek ve senet `ov_l10n_tr_check` · L · C
  - Alınan ve verilen çek/senet, portföy, ciro, tahsile verme, tahsil, karşılıksız/protesto, vade raporu.
  - Tasarım girdisi: Community `l10n_latam_check` (LGPL) incelenir; türetilen kod LGPL-3 kalır (D-008/2).
- [ ] T5.8 KDV hazırlık raporu · M · C
  - `l10n_tr` vergi raporunun üzerine: KDV beyannamesi için matrah ve vergi özetleri, tevkifat ayrıntısı, indirilecek KDV listesi.
  - Yalnız dışa aktarım; beyanname gönderimi yok.
- [ ] T5.9 Mali müşavire aktarım · M · C
  - Muhasebe fişlerinin dışa aktarımı: genel Excel biçimi + yaygın muhasebe programlarının kamuya açık içe aktarma biçimleri (araştırılarak).
- [ ] T5.10 Ticaret kabul senaryosu · M · C
  - Teklif → sipariş → sevkiyat + e-İrsaliye → e-Fatura → tahsilat (nakit, banka, çek) → banka ekstresi → mutabakat → cari ekstre → raporlar → müşavire aktarım.

### F6 — Üretim paketi `[ ]`

**Amaç:** S2 için üretim, maliyet, kalite ve bakım.
**Kabul (M6):**
- Üretim kabul senaryosu (T6.8) geçiyor.
- Maliyet raporu muhasebe kayıtlarıyla tutarlı.
- Kalite ve bakım kayıtları üretime bağlı.

- [ ] T6.1 Fabrika gereksinim analizi · M · C
  - Community `mrp`, `mrp_subcontracting`, `maintenance`, `stock` (lot/seri, izlenebilirlik) yetenekleri ve boşlukları.
  - Enterprise'a özel işlevler için clean-room spec listesi (D-006).
  - Çıktı: `docs/research/manufacturing.md`.
- [ ] T6.2 Üretim temel ayarları · M · C
  - Ürün ağacı, rota, iş merkezi, iş emri, varyantlar; Türkçe akış; paket ön ayarlarına (T7.1) girdi.
- [ ] T6.3 Üretim maliyeti · L · C
  - İş merkezi saat maliyeti, standart/ortalama maliyet, Tekdüzen 7/A hesap eşleştirmesi, sipariş bazlı maliyet raporu.
- [ ] T6.4 Kalite kontrol · L · C
  - OCA `quality_control_oca` portu (19.0): giriş, üretim ve sevk kontrolleri; kontrol planı; uygunsuzluk kaydı.
- [ ] T6.5 Bakım · S · C
  - `maintenance` ayarları, önleyici bakım, iş merkezi duruşlarıyla bağlantı.
- [ ] T6.6 İzlenebilirlik · S · C
  - Lot/seri ile hammaddeden müşteriye izleme raporu (Community raporu); Türkçe ve testli.
- [ ] T6.7 Fason üretim · M · C
  - `mrp_subcontracting` + fasoncuya malzeme gönderimi ve dönüşü için e-İrsaliye.
- [ ] T6.8 Üretim kabul senaryosu · M · C
  - Satış siparişi → MRP önerisi → satın alma → mal kabul + kalite → üretim → kalite → sevk + e-İrsaliye → e-Fatura → maliyet.

### F7 — Kullanıma hazır ürün `[ ]`

**Amaç:** boş bir veritabanından birkaç dakikada çalışan bir şirkete.
**Kabul (M7):**
- Elle tur: paketi seçip sihirbazı tamamlayan biri, yardım almadan ilk faturasını ve ilk üretim emrini oluşturabiliyor (T7.9).
- Rol bazlı yetki testleri geçiyor.

- [ ] T7.1 Paket modülleri · M · C
  - `ov_pack_ticaret`, `ov_pack_uretim`: bağımlılıklar + ön ayarlar.
- [ ] T7.2 Türkiye kurulum sihirbazı · L · C
  - Şirket (unvan, VKN, vergi dairesi, adres, MERSİS), hesap planı, e-Belge entegratör bağlantısı (test/canlı), açılış bakiyeleri, depolar.
- [ ] T7.3 Rol şablonları ve sade menüler · M · C
  - Yönetici, Muhasebe, Satış, Satın alma, Depo, Üretim, Kalite.
- [ ] T7.4 Veri aktarım şablonları · M · C
  - Cari, ürün, ürün ağacı, açılış bakiyesi, stok sayımı (Excel) + içe aktarım rehberi.
- [ ] T7.5 Mobil kullanım (PWA) · S · C
  - Markalı PWA; temel ekranların telefonda kullanılabilirliği.
- [ ] T7.6 Uygulama içi yardım bağlantıları · S · C
  - odoo.com dokümantasyon bağlantıları yerine yapılandırılabilir kendi belge adresimiz.
- [ ] T7.7 Performans turu · M · C
  - Büyük demo veriyle ana ekranların süreleri; gerekirse indeks ve sunucu ayarı.
- [ ] T7.8 Güvenlik ve yetki incelemesi · M · C
  - Rol başına erişim testleri; `odoo-security` rehberiyle kod incelemesi; portal erişimleri.
- [ ] T7.9 Kullanıcı kabul turu · S · B
  - Kullanıcı sistemi ilk kez gören biri gibi kullanır: paketi seçer, sihirbazı tamamlar, ilk faturayı ve ilk üretim emrini yardım almadan oluşturur.
  - Claude tur senaryosunu ve geri bildirim formunu hazırlar; bulgular göreve dönüşür.
  - Neden B: geliştiren kişi kendi ürününün kullanılabilirliğini tarafsız ölçemez.

### F8 — Satışa hazırlık `[ ]`

**Amaç:** müşteri arayışına çıkmak için gereken her şey.
**Kabul (M8):** §2.6'daki kapı ölçütlerinin tamamı.

- [ ] T8.1 MVP sonu değerlendirmesi · S · B
  - Kullanıcıya gerekçeli seçeneklerle getirilir:
    - e-Belge gönderim yöntemi (D-012);
    - paket kapsamı (D-018).
  - Kalıcı marka adı bu listeden çıktı: kullanıcı 2026-10-19'da Nexus'u seçti (D-014, K3).
- [ ] T8.2 Kalıcı adın uygulanması · M · B
  - Ad seçildi: Nexus (D-014). `ov_brand`'ın varsayılan adı T2.2'den beri Nexus.
  - Kalan: depo yeniden adlandırması kullanıcı onayıyla (K5); belgelerde ve geliştirme ortamında çalışma adı.
  - Alan adı: Student Pack ücretsiz yılı (K1) ya da ilk gelir.
  - Marka araştırması: TÜRKPATENT sorgusu ücretsiz; dış demodan önce yapılır (R17). Tescil ücretli olduğu için ilk gelirle yapılır.
- [ ] T8.3 Demo verisi üretici · M · C
  - Ticaret (toptan satış) ve Üretim (ör. metal/mobilya) senaryolu kurgusal şirketler; gerçek kişisel veri yok.
- [ ] T8.4 Kurulum aracı (`deploy/`) · L · C
  - Temiz Ubuntu LTS'ye tek komutla kurulum: PostgreSQL, Odoo servisi, Caddy + HTTPS.
  - Docker Compose seçeneği.
  - Kurulan Python paketlerinin lisans dökümü COMPLIANCE §5'e yazılır (T1.5'te yalnız geliştirme araçları yazıldı).
  - CI'da kurulum testi.
- [ ] T8.5 Yedekleme, geri yükleme ve güncelleme · M · C
  - Betikler + otomatik geri yükleme testi; modül güncelleme ve geri dönüş prosedürü.
- [ ] T8.6 Sunucu güvenliği · S · C
  - Kontrol listesi ve denetim betiği: `list_db`, yönetici şifresi, `proxy_mode`, güvenlik duvarı, HTTPS, yedek şifreleme.
- [ ] T8.7 Kullanıcı belgeleri sitesi · M · C
  - MkDocs; GitHub Pages (D-020). Yayın kullanıcı onayıyla (K5).
  - İçerik: kurulum, e-Belge, ticaret ve üretim akışları, SSS.
- [ ] T8.8 Demo ortamı (D-020) · S · C
  - Toplantı anında: lokal + Cloudflare Quick Tunnel.
  - Sürekli açık demo için ücretsiz seçenek değerlendirmesi. Demolarda gerçek müşteri verisi yok.
- [ ] T8.9 Rakip ve fiyat araştırması, fiyat listesi · M · B
  - §2.5 gelir modeli kalemlerine fiyat; paket teklif şablonu.
- [ ] T8.10 Sözleşme ve KVKK şablonları · M · C
  - Hizmet sözleşmesi, veri işleme sözleşmesi, aydınlatma metni, destek/SLA.
  - Taslaktır; avukat incelemesi T9.4'te.
- [ ] T8.11 Tanıtım materyali · M · C
  - Tanıtım sayfası, sunum, demo senaryosu, tek sayfalık broşür.
  - Tanıtım sayfası GitHub Pages'te barındırılmaz (Pages ticari site için kullanılamaz, D-020). Kurala uygun ücretsiz yer bu görevde seçilir. Yayın kullanıcı onayıyla (K5).
- [ ] T8.12 Kapı kontrolü ve go/no-go · S · B
  - §2.6 ölçütleri tek tek denetlenir; sonuç kullanıcıyla karara bağlanır.

### F9 — Müşteri arayışı ve ilk müşteri `[ ]`

**Amaç:** Basamak 1. Bu fazda kullanıcı ön planda; para gerektiren işler müşteri gelirinden karşılanır.
**Kabul (M9):** ilk müşteri canlı kullanımda; e-Belge canlı ortamda.

- [ ] T9.1 Hedef müşteri listesi ve ilk temaslar · M · K
  - Yakın çevre, organize sanayi bölgeleri, esnaf ve sanayi odaları. Claude liste şablonu ve görüşme soruları hazırlar.
- [ ] T9.2 Demo görüşmeleri ve geri bildirim döngüsü · M · B
  - Görüşme notları kişisel veri içermeden özetlenir; bulgular plana işlenir.
- [ ] T9.3 Yasal yapı · M · K
  - Şirket veya şahıs işletmesi, mali müşavir, fatura kesme düzeni.
  - Claude araştırma desteği verir (ör. genç girişimci kazanç istisnası, GVK md. 20/B; koşullar doğrulanacak).
- [ ] T9.4 Hukuki inceleme · M · K
  - Avukat ve mali müşavir: lisanslar, marka, KVKK, e-Belge, sözleşmeler. Ücretsiz seçenekler önce araştırılır.
- [ ] T9.5 Üretim barındırma kararı (D-013) ve sunucu · S · B
  - Yalnız müşteri bizim sunucumuzu kullanacaksa gerekir. Maliyet ilk gelirden.
- [ ] T9.6 İlk pilot kurulum · L · B
  - Sözleşme, veri aktarımı, kurulum, eğitim, e-Belge'de canlıya geçiş (müşterinin entegratör sözleşmesiyle).
- [ ] T9.7 Destek ve bakım süreci · M · C
  - Talep kaydı (kendi ürünümüzle), yanıt süreleri, güncelleme takvimi.
- [ ] T9.8 İlk müşteri sonrası değerlendirme · S · B
  - Segment ve basamak stratejisi (D-017), fiyatlar, sıradaki özellikler.

### F10 — Self-servis SaaS `[ ]`

**Başlama koşulu:** Basamak 2 (ilk 3–5 ücretli müşteri) ya da açık talep.
**Kabul (M10):** yeni müşteri kendi kendine kayıt olup deneme veritabanı açabiliyor ve ödeme yapabiliyor.

- [ ] T10.1 Çok kiracılı yapı · M · C
  - Veritabanı başına kiracı, `dbfilter`, alt alan adları, wildcard TLS.
- [ ] T10.2 Kiracı yaşam döngüsü (`ov_saas_*`) · L · C
  - Oluşturma, askıya alma, silme, plan değişikliği.
- [ ] T10.3 Self-servis kayıt ve deneme · M · C
- [ ] T10.4 Abonelik ve tahsilat · L · B
  - `payment_iyzico` (Community); kendi faturalarımız e-Belge ile.
  - Neden B: ödeme sağlayıcısının üye işyeri hesabı ve sözleşmesi kullanıcıda.
- [ ] T10.5 Kiracı başına otomatik yedek ve yedek doğrulama · M · C
- [ ] T10.6 İzleme ve günlükler · M · C
- [ ] T10.7 Ana sürüm yükseltme hattı · L · C
  - OpenUpgrade + hazırlık ortamı.

### F11 — Genişleme (sürekli, P1 ve sonrası) `[ ]`

- P1 görevleri M8'den önce de yapılabilir, ama F1–F8'deki işi bekletmez.
- P2 ve sonrası M8'den sonra, müşteri talebine göre sıralanır.
- Enterprise eşdeğerlerinde önce `docs/specs/<modül>.md` yazılır (D-006).

- [ ] T11.1 Sabit kıymet ve amortisman · P1 · L · C
  - OCA `account_asset_management` portu + VUK amortisman oranları.
- [ ] T11.2 Çok seviyeli MRP planlama · P1 · L · C
  - OCA `mrp_multi_level` portu.
- [ ] T11.3 Barkodlu depo işlemleri · P1 · L · C
  - Seçenek analizi: OCA 18.0 `stock_barcodes` portu ya da kendi basit okutma ekranımız.
- [ ] T11.4 e-Defter · P1 · L · C
  - Önce araştırma: entegratör üzerinden mi, kendi üretimimiz mi; sonra uygulama.
- [ ] T11.5 Türk SMS sağlayıcısı adaptörü · P1 · M · C
- [ ] T11.6 Personel devam takibi ve izin için Türkiye uyarlaması · P1 · M · C
- [ ] T11.7 Enflasyon düzeltmesi: güncel mevzuat araştırması, gerekirse rapor · P1 · M · C
- [ ] T11.8 İkinci entegratör adaptörü · P2 · M · C
- [ ] T11.9 POS ve perakende · P2 · L · C
  - Önce yeni nesil ödeme kaydedici cihaz zorunluluğu araştırılır.
- [ ] T11.10 Enterprise eşdeğerleri P2 paketi · P2 · XL · C
  - MODULE_MATRIX §C: bütçe, onaylar, helpdesk, dokümanlar, abonelik.
- [ ] T11.11 Enterprise eşdeğerleri P3 paketi · P3 · XL · C
- [ ] T11.12 Enterprise eşdeğerleri P4 paketi · P4 · XL · C
- [ ] T11.13 Türkiye bordrosu · P3 · XL · C
- [ ] T11.14 OCA'ya port katkıları · P2 · M · B
  - Dışa dönük işlem; kullanıcı onayıyla (K8, D-019).

## 6. Sürekli işler

Bunlar görev değil, düzenli rutinlerdir. Yapıldıklarında CHANGELOG'a yazılır.

| ID | İş | Sıklık |
|---|---|---|
| S1 | Upstream 20.0 takibi: submodule commit'ini ilerlet, testleri çalıştır (güvenlik düzeltmeleri) | Ayda bir |
| S2 | OCA 20.0 takibi: portlarımızın resmî 20.0 sürümü çıktıysa `vendor/`'a geçiş (D-019) | Ayda bir |
| S3 | GİB UBL-TR paket güncellemeleri: doğrulama paketlerini ve kodu güncelle. 2026'da 4 güncelleme oldu | GİB duyurusunda |
| S4 | Mevzuat takibi: KDV oranları, e-Belge eşikleri, yeni zorunluluklar | Ayda bir |
| S5 | Bağımlılık güvenliği: Python paketleri ve güvenlik duyuruları | Ayda bir |
| S6 | Entegratör API değişiklikleri (Nilvera) | Duyuru geldikçe |
| S7 | Belge güncelleme protokolü (D-004) | Her adımda |

## 7. Ücretsiz kaynaklar planı (D-020)

| Kaynak | Ne için | Koşul / sınır | Ne zaman |
|---|---|---|---|
| GitHub (public depo) | Kod, belgeler | Depo herkese açık (D-015) | Şimdi |
| GitHub Actions | CI | Public depoda standart runner ücretsiz | T1.10 |
| GitHub Pages | Kullanıcı belgeleri sitesi | Ticari iş veya SaaS barındırmak için kullanılamaz; site ≤ 1 GB; ~100 GB/ay bant genişliği | T8.7 |
| Cloudflare Quick Tunnel | Toplantı anı demo | Hesap ve alan adı gerekmez. Yalnız test/geliştirme amaçlı; 200 eşzamanlı istek; SSE yok; adres her seferinde değişir | T8.8 |
| Nilvera test portalı | e-Belge geliştirme ve test | Kamuya açık ortak test hesabı; bilgiler depoya girmez | T4.5 |
| GİB UBL-TR paketleri | XSD + schematron doğrulama | Kamuya açık; depoya konmaz, CI'da indirilir | T4.2 |
| TCMB kur servisi | Döviz kurları | Kamuya açık XML | T3.5 |
| OCA modülleri | Muhasebe, kalite, MRP | AGPL-3 / LGPL-3; 20.0 dalları büyük ölçüde boş (D-019) | F5, F6, F11 |
| Odoo dokümantasyonu | İşlev tanımı | CC BY-SA 4.0; metin kopyalanırsa atıf | Sürekli |
| Python araçları | Test, lint, doğrulama | ruff, pylint-odoo, SaxonC-HE, MkDocs (ücretsiz lisanslar) | F1, F4, F8 |
| GitHub Student Developer Pack | Alan adı, bulut kredisi, geliştirici araçları | Kullanıcı başvurusu gerekir (K1). Avantajlar süreli; süre bitince ücret doğuracak bağımlılık kurulmaz | F8 |

**Para gerektirenler ve ne zaman:**

| Kalem | Ne zaman | Kim öder |
|---|---|---|
| Üretim sunucusu | T9.5 (yalnız bizim sunucumuzda çalışacak müşteri için) | İlk müşteri geliri |
| Hukuki inceleme | T9.4 | İlk gelir (önce ücretsiz seçenekler araştırılır) |
| Şirket kuruluşu, mali müşavir | T9.3 | İlk gelir |
| Marka tescili | T8.2'de araştırma, tescil ilk gelirle | İlk gelir |
| Alan adı | T8.2 | Student Pack ücretsiz yıl, sonra ilk gelir |
| e-Belge entegratör kontörü | Müşteri canlıya geçince | Müşteri |
| SMS | Müşteri kullanırsa | Müşteri |

## 8. Test ve kalite stratejisi

- **Modül testleri:** her modülde `tests/` (Odoo `TransactionCase`, `HttpCase`, tur testleri). Yeni işlev testsiz birleştirilmez.
- **CI (her push):**
  - belge denetimi;
  - lint: ruff, pylint-odoo, modül kuralları (`pre-commit`, T1.9);
  - gizli bilgi taraması;
  - modül testleri;
  - özel testler: marka sızıntısı (T2.6), dış istek (T2.7), UBL-TR doğrulama (T4.2), çeviri kapsamı (T3.6), kurulum (T8.4), yedekten geri yükleme (T8.5).
- **Kabul senaryoları:** T3.9, T4.10, T5.10, T6.8. Hem otomatik test hem elle tur; her kilometre taşında yeniden çalıştırılır.
- **Kod incelemesi:** Odoo'nun `odoo-review`, `odoo-security`, `odoo-web-guidelines` rehberleri (T1.7'den sonra).
- **Test verisi:** yalnız kurgusal veri. Gerçek kişi veya şirketin VKN/TCKN'si kullanılmaz. Entegratörün test numaraları ya da sağlamayı geçen kurgusal numaralar kullanılır.
- **Sürüm disiplini:** modül sürümü `20.0.x.y.z`. Veri yapısı değişirse göç (migration) betiği ve testi yazılır.
- **Hatalar:** ilgili göreve veya CHANGELOG'a yazılır. Gerekirse GitHub Issues kullanılır.

## 9. Risk kaydı

Olasılık/Etki: Y = yüksek, O = orta, D = düşük.

| ID | Risk | Olasılık | Etki | Önlem |
|---|---|---|---|---|
| R1 | 19.0 → 20.0 port beklenenden pahalı (Nilvera, OCA) | D | O | T1.2'de ölçüldü: 19 modülün 18'i küçük uyarlamayla kuruluyor, ek emek ~9–15 oturum; en büyük kalem T5.4 (`nilvera-port.md`) |
| R2 | OCA 20.0 geç kalır, port yükü büyür | Y | O | D-019 (kendimiz taşırız); yalnız gerekli modüller; resmî sürüm çıkınca geçiş |
| R3 | GİB UBL-TR paketleri sık değişir | Y | O | Otomatik doğrulama (T4.2); S3 rutini |
| R4 | Nilvera test ortamı kapanır veya koşulları değişir | D | O | Sahte adaptör (T4.4); adaptör mimarisi; ikinci entegratör (T11.8) |
| R5 | Marka ihlali ("Odoo" görünür kalır) | O | Y | D-007; otomatik sızıntı testi (T2.6); kalıcı ad (T8.2) |
| R6 | Enterprise koduyla temas (clean-room ihlali) | D | Y | D-006; izinli kaynak listesi; spec önce |
| R7 | Zaman: öğrenci takvimi, oturumlar arası bağlam kaybı | Y | O | Küçük görevler; `state.json` ve bu plan; her adım commit |
| R8 | Sıfır bütçe canlıya geçişi engeller (sunucu, hukuk) | O | Y | Maliyetler ilk gelirden; on-prem seçeneği sunucu maliyetini sıfırlar; fiyata kurulum ücreti |
| R9 | Müşteri öğrenci ürününe güvenmez | Y | Y | Pilot indirimi karşılığı referans; açık kaynak şeffaflığı; yerinde destek; veri müşteride seçeneği |
| R10 | AGPL müşteride yanlış algılanır | O | D | Kısa açıklama: müşteri yazılımı kullanır, yükümlülük yeniden dağıtımda doğar; satış materyalinde SSS (T8.11) |
| R11 | Upstream deposunun boyutu, Windows yol uzunluğu | O | D | Sığ submodule, `core.longpaths` (T1.4) |
| R12 | Public depoda gizli bilgi sızıntısı | O | Y | `.gitignore`; push öncesi `git diff --cached`; CI'da gizli bilgi taraması (T1.10) |
| R13 | Rekabet (yerli ön muhasebe ve ERP paketleri, Odoo iş ortakları) | Y | O | Konumlandırma §2.4; üretim + e-Belge birlikteliği; fiyat |
| R14 | Türkçe çeviri kalitesi düşük kalır | O | O | Ölçüm aracı ve eşik (T3.6); terim listesi |
| R15 | e-Belge hatası nedeniyle müşteri zararı | D | Y | GİB doğrulaması; test matrisi (T4.10); sözleşmede sorumluluk sınırı (T8.10) |
| R16 | Mevzuat yorum hatası (eşikler, tarihler) | O | O | Birincil kaynak önceliği; mali müşavir doğrulaması (T9.4); S4 rutini |
| R17 | Kalıcı ad "Nexus" tescilli bir markayla çakışır (yaygın sözcük) | O | O | TÜRKPATENT sorgusu ve alan adı kontrolü dış demodan önce (T8.2); gerekirse ayırt edici ek; ad tek ayardan geldiği için teknik maliyet düşük (D-014) |

## 10. Kullanıcıdan beklenenler

Ayrı belgede: **`USER_TASKS.md`**. İçeriği:
- kullanıcı eylemleri, kararları ve onayları (K1, K2, …);
- kategori K ve B görevlerinde kullanıcıdan beklenenler;
- otonom mesailerde biriken sorular ve onay bekleyen işler.

Plan bu eylemlerin hiçbirine bağlı değildir. Hepsi isteğe bağlı ya da ilgili göreve gelince gereklidir.

## 11. Kaynaklar

Planı besleyen araştırmalar ve kaynak bağlantıları:
- `docs/research/planning-inputs.md`: OCA 20.0 durumu, çeviri kapsamı, ücretsiz kaynaklar, veri kaynakları, pazar referansları.
- `docs/research/e-fatura.md`: e-Belge mevzuatı, Nilvera test ortamı, GİB paketleri, Ba-Bs, e-Defter.
- `docs/research/hosting.md`: barındırma seçenekleri.
