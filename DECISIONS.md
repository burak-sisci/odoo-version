# Kararlar

Son güncelleme: 2026-10-18

> **Kural:** Bu dosya yalnızca güncel kayıtları tutar. Üç durum vardır:
> - **Geçerli:** alınmış ve uygulanan karar.
> - **Açık:** kullanıcı kararı bekleyen konu (`state.json` → `blocked_on_user`).
> - **Ertelendi:** şimdi karar gerekmiyor; hangi görevden önce karar verileceği `**Karar noktası:**` satırında yazılı.
>
> Kurallar:
> - Bir karar değiştiğinde kaydı **yerinde yeniden yazılır**; ID değişmez.
> - Eski metin ve değişikliğin nedeni `CHANGELOG.md`'ye işlenir.
> - Geçerliliğini yitirmiş bir karar bu dosyada **tutulmaz**.
> - Bir konu karara bağlandığında etkilenen tüm belgeler aynı adımda güncellenir.
> - `**Karar noktası:**` ve `**Yeniden değerlendirme:**` satırları PLAN.md'deki bir göreve bağlanır. O görev tamamlandığında kayıt güncellenmezse `tools/check_docs.py` hata verir.
> - `state.json` içindeki `decisions` listesi bu dosyayla birebir aynı olmalıdır (`python tools/check_docs.py` denetler).

## Özet

| ID | Konu | Durum |
|---|---|---|
| D-001 | Ürün hedefi | Geçerli |
| D-002 | Kapsam | Geçerli |
| D-003 | Ekip ve çalışma modeli | Geçerli |
| D-004 | Dokümantasyon protokolü | Geçerli |
| D-005 | Bütçe | Geçerli |
| D-006 | Clean-room kuralı | Geçerli |
| D-007 | Marka kuralı | Geçerli |
| D-008 | Lisans uyumu kuralı | Geçerli |
| D-009 | Dil | Geçerli |
| D-010 | Temel yaklaşım | Geçerli |
| D-011 | Odoo sürümü | Geçerli |
| D-012 | e-Belge stratejisi | Geçerli |
| D-013 | Üretim barındırma yeri | Ertelendi |
| D-014 | Çalışma adı ve teknik modül öneki | Geçerli |
| D-015 | Git deposu, GitHub ve push yetkisi | Geçerli |
| D-016 | Kendi modüllerimizin lisansı | Geçerli |
| D-017 | Hedef müşteriler ve aşama stratejisi | Geçerli |
| D-018 | MVP tanımı, ürün paketleri ve teslim biçimi | Geçerli |
| D-019 | OCA modülleri ve 20.0 portları | Geçerli |
| D-020 | Ücretsiz altyapı ve araçlar | Geçerli |
| D-021 | Mesai türleri ve görev kategorileri | Geçerli |

---

## Geçerli kararlar

### D-001 · Ürün hedefi
- **Durum:** Geçerli
- **Karar:** Odoo Community tabanlı, **kendi markamızla müşterilere satılacak** bir ERP. Satış biçimi ürün ve/veya SaaS.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-002 · Kapsam
- **Durum:** Geçerli
- **Karar:** Hedef, Odoo'da normalde bulunan **tüm uygulamaların** (Community + Enterprise) işlevsel karşılığı.
  Sıralama, Türkiye pazarına, yasal zorunluluklara ve kaynaklarımıza göre `docs/MODULE_MATRIX.md` içinde yapılır. İlk satışa çıkan kapsam D-018'dedir.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-003 · Ekip ve çalışma modeli
- **Durum:** Geçerli
- **Karar:** Ekip = kullanıcı + Claude.
  - Kullanıcı ürün sahibi ve son karar mercii.
  - Claude araştırma ve geliştirmeyi **çoğunlukla otonom** yürütür.
  - Claude şu durumlarda kullanıcıya sorar: açık kararlar, para gerektiren her şey, hukuki belirsizlik, dışa dönük işlemler (yayınlama, paylaşma, depo ayarları).
  - İstisna: proje deposuna her adım sonunda push önceden onaylıdır (D-015).
  - Çalışma iki mesai türüyle yürür: standart ve otonom (D-021). Otonom mesaide Claude soru soramaz; sorular ve onaylar `USER_TASKS.md`'ye yazılır.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-004 · Dokümantasyon protokolü
- **Durum:** Geçerli
- **Karar:** Proje belgeleri her adımda güncel tutulur. Eski kararın belgede kalması ya da yeni kararın eklenmemesi kabul edilemez.
  Uygulama biçimi `CLAUDE.md` → "Belge güncelleme protokolü"; denetim `tools/check_docs.py`.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-005 · Bütçe
- **Durum:** Geçerli
- **Karar:** Sıfır bütçe. Ücretli lisans, servis veya altyapı kullanılmaz.
  Para gerektiren adımlar ya ilk gelire kadar ertelenir ya da maliyeti müşteriye aittir (ör. e-Fatura entegratör kontörü). Ücretsiz kaynaklar D-020'de.
- **Kaynak / tarih:** Kullanıcı ("bütçesiz"), 2026-10-16.

### D-006 · Clean-room kuralı (zorunlu)
- **Durum:** Geçerli
- **Karar:** Odoo Enterprise kaynak kodu hiçbir biçimde kullanılmaz ve incelenmez. Buna şunlar dahildir:
  - sızdırılmış kopyalar ve GitHub'daki izinsiz yüklemeler;
  - Enterprise deneme/SaaS örneklerinden alınan JS/CSS/görseller;
  - 20.0+ Enterprise'a taşınmış modüllerin yeni sürümleri.

  Enterprise eşdeğeri özellikler yalnız şu kaynaklardan geliştirilir:
  1. Odoo'nun kamuya açık dokümantasyonu (CC BY-SA 4.0);
  2. Community kodu (LGPL);
  3. geçmiş sürümlerde LGPL ile yayımlanmış kod;
  4. OCA kodu (lisans kurallarına uyarak);
  5. kendi tasarımımız.

  Ayrıntılı izinli/yasak kaynak listesi: `docs/COMPLIANCE.md`.
- **Gerekçe:** Enterprise lisansı kopyalamayı yasaklıyor. Flectra davası (2017–2018) Odoo S.A.'nın bu konuda dava açtığını gösteriyor.
- **Kaynak / tarih:** Hukuki zorunluluk (Claude), 2026-10-18.

### D-007 · Marka kuralı (zorunlu)
- **Durum:** Geçerli
- **Karar:** "Odoo" adı ve logosu, ürünün kullanıcıya görünen hiçbir yerinde ürün adı ya da logo olarak kullanılmaz.
  Lisans ve telif notları (kaynak dosya başlıkları, LICENSE/COPYRIGHT) **korunur**; bunlar marka kullanımı değil, lisans yükümlülüğüdür.
- **Gerekçe:** Açık kaynak lisansı marka kullanım hakkı vermez. "Odoo" Odoo S.A.'nın markasıdır.
- **Kaynak / tarih:** Hukuki zorunluluk (Claude), 2026-10-18.

### D-008 · Lisans uyumu kuralı (zorunlu)
- **Durum:** Geçerli
- **Karar:**
  1. Upstream Odoo Community (LGPL-3) değiştirilmez (D-010). Değiştirilseydi değişiklikler LGPL-3 kalırdı.
  2. LGPL koddan türetilen (kopyalanıp uyarlanan) modüller LGPL-3 kalır ve telif notlarını korur.
  3. AGPL-3 OCA modülleri değiştirilirse (ör. 20.0 portu, D-019), SaaS kullanıcılarına değiştirilmiş kaynak sunulur (AGPL ağ maddesi).
  4. Kapalı kaynak bir modül hiçbir zaman AGPL modüllere bağımlı olamaz (`depends`). Şu an kapalı modül yoktur; kendi modüllerimiz AGPL-3'tür (D-016).
  5. Projeye giren her 3. parti kod ve veri `docs/COMPLIANCE.md` → lisans envanterine yazılır.
- **Kaynak / tarih:** Hukuki zorunluluk (Claude), 2026-10-18.

### D-009 · Dil
- **Durum:** Geçerli
- **Karar:** Belgeler Türkçe. Kod, tanımlayıcılar, kod yorumları ve commit mesajları İngilizce (Odoo geleneği).
  Kullanıcıya görünen metinler İngilizce kaynak + Türkçe çeviri (`i18n/tr.po`).
- **Kaynak / tarih:** Claude varsayılanı, 2026-10-18. Kullanıcı değiştirebilir.

### D-010 · Temel yaklaşım
- **Durum:** Geçerli
- **Karar:** **B — dağıtım modeli.**
  - `upstream/odoo` altındaki Odoo Community dosyaları **hiç değiştirilmez**. Yama kuyruğu (`patches/`) yoktur.
  - Her değişiklik kendi modüllerimizle yapılır (`addons/`; OCA portları `ports/`, D-019). Kullanılan yöntemler: model kalıtımı (`_inherit`), görünüm kalıtımı (XPath), JS `patch()`, asset paketinde dosya değiştirme (`replace`), controller override. Gerekirse modül içinden monkey-patch, gerekçesi kodda yazılı olarak.
  - Modülle çözülemeyen bir durum çıkarsa çekirdeğe dokunulmaz. Konu kullanıcıya yeni karar olarak getirilir.
  - Kabul edilen sonuç: son kullanıcıya görünmeyen teknik izler kalır (`odoo` Python paketi, `odoo-bin` komutu).
- **Gerekçe:** `docs/research/approach-b-vs-c.md`. Claude'un önerisi B+ idi, kullanıcı B'yi seçti.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-011 · Odoo sürümü
- **Durum:** Geçerli
- **Karar:** **Odoo 20.0 Community.** Upstream `upstream/odoo` altına sabit bir commit ile eklenir (T1.4).
- **Gerekçe:**
  - Odoo her an son 3 ana sürümü destekler. 20.0 en uzun destek süresine sahip (~2029'a kadar).
  - İlk müşteriler büyük olasılıkla 2027'de gelecek. 19.0 ile başlamak, bu müşterilerde kısa süre sonra zorunlu bir ana sürüm göçü demek.
  - T1.2 ölçümü (`docs/research/nilvera-port.md`): MVP'nin 19 modülünden 18'i, 21 tür küçük uyarlamayla 20.0'da kuruluyor; 268 testin 243'ü geçiyor. Kalan ek emek yaklaşık 9–15 oturum ve mevcut port görevlerinin içinde.
  - 19.0'da kalmak port işini yalnız erteler. Nilvera 20.0'dan itibaren Community'de yok; 19.0'ın desteği Eylül 2028'de bitiyor. O tarihteki göç, kendi modüllerimiz ve müşteri veritabanlarıyla birlikte daha pahalı.
- **Kabul edilen bedel:**
  - Nilvera e-Belge modülleri 20.0'da Enterprise'da. 19.0'daki LGPL kodundan taşınacak (F4).
  - MVP'nin ihtiyaç duyduğu OCA modüllerinin çoğu (mali raporlar, banka mutabakatı, ekstre içe aktarma, kalite) yalnız 19.0'da var. OCA o tarihe kadar taşımazsa biz taşıyacağız (D-019). En büyük kalem `account_financial_report` (20.0'da `account.group` yok, T5.4).
  - 20.0 taze bir sürüm; denenen commit'te Community çekirdeğinde hata görüldü. Upstream sabit commit'te tutulur ve düzenli güncellenir (T1.4); çekirdek yamalanmaz (D-010).
- **Yeniden değerlendirme:** Planlı bir nokta yok; sürüm ölçümle doğrulandı. Yalnız şu durumda yeniden açılır: 20.0 çekirdeğinde MVP'yi engelleyen ve modülle aşılamayan bir hata, upstream'de üç ay içinde düzelmezse.
- **Kaynak / tarih:** Kullanıcı kararı Claude'a bıraktı; Claude, 2026-10-18. T1.2 ölçümüyle doğrulandı, 2026-10-18.

### D-012 · e-Belge stratejisi
- **Durum:** Geçerli
- **Karar:**
  - **MVP kapsamı:** e-Fatura + e-Arşiv + **e-İrsaliye** (hepsi P0).
  - **e-Defter:** MVP'de yok. MVP'de muhasebe fişleri mali müşavirin programına aktarılır (PLAN T5.9). e-Defter çözümü P1 (T11.4).
  - **Diğer e-Belgeler** (e-SMM, e-Müstahsil vb.): P3.
  - **GİB'e gönderim yöntemi:** mevcut bir özel entegratörün API'si. Bu bir çalışma varsayımıdır; MVP sonunda yeniden ele alınacak.
  - **Mimari:** entegratörden bağımsız bir e-Belge çekirdeği + her entegratör için ayrı adaptör modülü + testler için sahte (mock) adaptör.
  - **İlk adaptör:** Nilvera.
    - 19.0'daki LGPL modüllerinden 20.0'a taşınır ve LGPL-3 kalır.
    - Kamuya açık bir test ortamı var (`docs/research/e-fatura.md` §6).
- **Gerekçe:**
  - `docs/research/e-fatura.md`.
  - e-İrsaliye'nin MVP'ye alınma nedeni: ilk hedef segmentlerden biri orta ölçekli fabrikalar (D-017). e-Fatura'ya kayıtlı ve hasılatı 10 Milyon TL ve üzeri olanlar için e-İrsaliye zorunlu; sevkiyat ve fason üretim de e-İrsaliye gerektiriyor.
- **Yeniden değerlendirme:** T8.1 (MVP sonu: gönderim yöntemi kullanıcıyla yeniden ele alınır).
- **Kaynak / tarih:**
  - Kullanıcı: kapsam (e-Fatura + e-Arşiv) ve yöntem, 2026-10-18.
  - Claude: ilk entegratör seçimi ve e-İrsaliye'nin MVP'ye alınması, 2026-10-18. Kullanıcı planlama kararlarını Claude'a bıraktı.

### D-014 · Çalışma adı ve teknik modül öneki
- **Durum:** Geçerli
- **Karar:**
  - **Çalışma adı:** `odoo-version`. Geçicidir, MVP sonunda kalıcı adla değişecek. GitHub deposunun adı da budur.
  - **Teknik modül öneki:** `ov_`. Markadan bağımsızdır ve kalıcıdır.
    - Marka değiştiğinde modül adları değişmez; yalnız marka modülündeki görünen ad değişir. Kurulu bir modülün teknik adını değiştirmek veritabanı göçü gerektirir, bu yüzden önek sabit tutulur.
    - Odoo 20.0'da `ov_` ile başlayan modül yok (2026-10-18). `x_` öneki Odoo'da özel alanlara ayrılmış olduğu için kullanılamaz.
    - İstisna: OCA portları orijinal teknik adlarını korur (D-019).
  - **D-007 ile ilişki:** çalışma adı "Odoo" sözcüğünü içeriyor. Bu yüzden yalnız depoda, belgelerde ve geliştirme ortamında kullanılır. Ürün müşteriye, pilot kullanıcıya veya dış demoya çıkmadan önce kalıcı ad zorunludur (T8.2).
- **Yeniden değerlendirme:** T8.1 (kalıcı ad ve yeniden adlandırma).
- **Kaynak / tarih:** Kullanıcı (çalışma adı), 2026-10-18. Önek seçimi Claude'a ait.

### D-015 · Git deposu, GitHub ve push yetkisi
- **Durum:** Geçerli
- **Karar:**
  - Proje klasörü bir git deposudur; varsayılan dal `main`.
  - Uzak depo GitHub'da ve **herkese açık (public)**: https://github.com/burak-sisci/odoo-version
  - Claude her görev/adım sonunda kodu ve belgeleri **aynı commit'te** kaydeder ve `origin/main`'e push eder. Bu push kullanıcı tarafından önceden onaylanmıştır.
  - Public depo kuralları:
    - Her push'tan önce gizli bilgi ve müşteri verisi denetimi yapılır.
    - Force-push yapılmaz, geçmiş yeniden yazılmaz.
  - **Commit yazarlığı:** GitHub'da tek katkıcı kullanıcıdır.
    - Commit'lerin yazarı kullanıcının git kimliğidir (`burak-sisci`).
    - Claude commit'lere yazar veya ortak yazar olarak eklenmez: `Co-Authored-By` satırı ve Claude'u ya da başka bir yapay zekâyı yazar gösteren hiçbir satır yazılmaz.
    - İlk iki commit'te bu satır var. Temizlenmesi geçmişi yeniden yazmayı ve force-push'u gerektirdiği için kullanıcı kararına bağlı (`USER_TASKS.md` K10).
  - Diğer dışa dönük işlemler yine kullanıcı onayı ister: depo ayarları (görünürlük, yeniden adlandırma), sürüm yayınlama (release), başka yerde paylaşma.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18 (commit yazarlığı kuralı aynı gün eklendi).

### D-016 · Kendi modüllerimizin lisansı
- **Durum:** Geçerli
- **Karar:**
  - **Kendi özgün kodumuz: AGPL-3.** Depo kökünde `LICENSE` (GNU AGPL v3 metni); modül manifestlerinde `'license': 'AGPL-3'`.
  - **LGPL koddan türetilen modüller: LGPL-3** (D-008/2). Örnek: 19.0 Nilvera portu (`ov_l10n_tr_edi*`, `ov_l10n_tr_edispatch`).
  - **OCA portları:** orijinal lisanslarını korur (D-019).
  - **İleride private depo:** kullanıcı depoyu ileride private yapabilir. Bilinen sınırlar:
    1. Yayımlanmış sürümler AGPL-3 altında kalır. O sürümü alan herkes onu AGPL koşullarıyla kullanmaya devam edebilir.
    2. Telif hakkı yalnız bize ait kodun gelecek sürümleri için lisans değiştirilebilir. LGPL veya AGPL koddan türetilen kısımlar için değiştirilemez.
    3. Kendi kodumuzun telif sahibi biz olduğumuz için AGPL bizi kendi kodumuz konusunda bağlamaz. Ama değiştirdiğimiz 3. parti AGPL kodu (OCA portları) SaaS'ta çalıştırırsak, kaynağını kullanıcılara sunmak zorundayız.
  - **Dış katkılar:** lisans esnekliğini korumak için dış katkı (pull request) şimdilik kabul edilmez (README'de yazılı). Kabul edilecekse önce bir katkı sözleşmesi kararı alınır.
- **Gerekçe:**
  - Gelir kodu satmaktan değil, hizmetten gelecek: kurulum, barındırma, destek, e-Belge uyumu, Türkiye yerelleştirmesi.
  - Kodu alıp kapalı bir SaaS'ta kullanan rakibe karşı en güçlü açık kaynak lisansı AGPL.
  - OCA'nın AGPL modüllerine serbestçe bağımlı olabiliriz.
- **Kaynak / tarih:** Kullanıcı (Claude'un A + gerekirse D önerisini onayladı), 2026-10-18.

### D-017 · Hedef müşteriler ve aşama stratejisi
- **Durum:** Geçerli
- **Karar:**
  - **Başlangıç:** proje bir öğrenci projesi olarak, sıfır bütçeyle (D-005), destek ve müşteri olmadan başlar.
  - **Aşama 1 — bütçesiz ilerleme:** müşteri, bütçe ya da dış destek gerektirmeyen tüm ilerleme alınır.
    - Aşamanın sonu PLAN.md §2.6'daki **M8 kapısıdır**: hedef segmentlere satılabilir en iyi ürün (F0–F8).
    - Plan dış desteğe bağlı değildir. TÜBİTAK 2209-A gibi destekler ve Student Pack avantajları isteğe bağlı hızlandırıcılardır.
  - **Aşama 2 — müşteri arayışı:** ilk teklifler **küçük işletmelere** ve **orta ölçekli fabrikalara** verilir.
  - **Aşama 3 — büyüme:** her satış ve anlaşmadan sonra bir üst ölçekteki müşteriye hitap edilir (PLAN.md §2.3 büyüme merdiveni).
- **Kapı tanımının gerekçesi (Claude):**
  - "Bütçesiz alınabilecek tüm ilerleme" ucu açık bir hedef: D-002'nin tamamı da bütçesiz yapılabilir.
  - Kapı bu yüzden "hedef segmentlere satılabilir en iyi ürün" olarak tanımlandı.
  - Kapıdan sonra geliştirme sürer (F11). Ama müşteri geri bildirimi olmadan eklenen özelliklerin getirisi azalır, yanlış şeyi yapma riski artar.
- **Yeniden değerlendirme:** T9.8 (ilk müşteriden sonra).
- **Kaynak / tarih:**
  - Kullanıcı: perspektif, segmentler ve aşamalar, 2026-10-18.
  - Claude: kapı tanımı ve merdivenin ayrıntısı, 2026-10-18. Kullanıcı karar almayı Claude'a bıraktı.

### D-018 · MVP tanımı, ürün paketleri ve teslim biçimi
- **Durum:** Geçerli
- **Karar:**
  - **MVP** = M8'de satışa çıkan sürüm. İki paketten oluşur (ayrıntı PLAN.md §3):
    - **Ticaret paketi** (küçük işletme): cari, satış, satın alma, stok, fatura + e-Belge, tahsilat/ödeme, çek/senet, banka, raporlar, mali müşavire aktarım, CRM.
    - **Üretim paketi** (orta ölçekli fabrika): Ticaret + üretim, fason, maliyet, kalite, bakım, izlenebilirlik.
  - **Öncelik tanımları** (`docs/MODULE_MATRIX.md`):
    - P0 = M8 kapısı için zorunlu;
    - P1 = hedef segmentler için değerli, kapıyı bekletmez;
    - P2–P4 = sonraki sürümler;
    - P5 = ertelendi (para veya dış servis gerektiriyor).
  - **MVP dışı:** e-Defter, bordro, POS, web sitesi/e-ticaret, Studio, yapay zekâ, self-servis SaaS, ikinci entegratör, yerel mobil uygulama (liste PLAN.md §3.3).
  - **Teslim biçimi:** ilk müşterilerde yönetilen kurulum.
    - Her müşterinin ayrı veritabanı olur.
    - Kurulum müşterinin kendi sunucusunda (on-prem) ya da bizim yönettiğimiz bir sunucuda yapılır. Sunucunun yeri D-013'te.
    - İki seçenek de aynı kurulum aracını kullanır.
  - **Self-servis SaaS** (kayıt, deneme, otomatik tahsilat): Basamak 2'den sonra (PLAN F10).
  - **Dil:** Türkçe öncelikli.
- **Gerekçe:**
  - İki segment ortak bir çekirdeği (Ticaret) paylaşıyor; Üretim paketi onun üstüne kuruluyor. Tek kod tabanı, iki teklif.
  - Fabrikalar e-İrsaliye, kalite ve maliyet olmadan ikna olmaz. Küçük işletmeler e-Belge, cari ve çek/senet olmadan.
  - Yönetilen kurulum ilk birkaç müşteri için self-servis SaaS'tan çok daha az iş. Odoo'nun veritabanı başına kiracı yapısı bunu hazır sunuyor.
- **Yeniden değerlendirme:** T8.1 (MVP sonu: paket kapsamı).
- **Kaynak / tarih:** Claude (kullanıcı planlama kararlarını Claude'a bıraktı), 2026-10-18.

### D-019 · OCA modülleri ve 20.0 portları
- **Durum:** Geçerli
- **Karar:**
  - **OCA'nın resmî 20.0 sürümü varsa:** `vendor/oca/<depo>` altında git submodule, sabit commit, dokunulmaz (D-010).
  - **Yoksa ve P0/P1 için gerekiyorsa:** 19.0 sürümünü kendimiz 20.0'a taşırız → `ports/oca/<depo>/<modül>`.
    - Teknik ad, lisans, yazarlar ve telif notları korunur; kaynak commit kaydedilir.
    - OCA'nın taşıma kurallarına uyulur, böylece port ileride OCA'ya gönderilebilir.
    - OCA resmî 20.0 sürümünü yayımlayınca porttan resmî sürüme geçilir. Teknik ad aynı olduğu için veritabanı göçü gerekmez; farklar testle doğrulanır.
  - **OCA'ya katkı** (port veya düzeltme göndermek) dışa dönük bir işlemdir; kullanıcı onayıyla yapılır (PLAN T11.14).
  - **18.0'da olup 19.0'da olmayan modüller:** önce alternatif aranır. Port bedeli büyükse kendi tasarımımız yazılır.
  - Her port lisans envanterine yazılır (COMPLIANCE §5).
- **Gerekçe:**
  - OCA 20.0 dalları büyük ölçüde boş (2026-10-18). MVP'nin ihtiyaç duyduğu muhasebe ve kalite modülleri 19.0'da var.
  - Teknik adı korumak resmî sürüme geçişi ucuz tutar.
  - `vendor/` dokunulmaz kalır; değiştirilmiş kod ayrı bir yerde ve açıkça işaretli olur.
- **Kaynak / tarih:** Claude, 2026-10-18.

### D-020 · Ücretsiz altyapı ve araçlar
- **Durum:** Geçerli
- **Karar:**
  - **CI:** GitHub Actions. Public depoda standart runner kullanımı ücretsiz.
  - **Kullanıcı belgeleri sitesi:** GitHub Pages.
    - Pages kuralları ticari iş veya SaaS barındırmaya izin vermiyor. Bu yüzden Pages'te yalnız açık kaynak proje belgeleri yer alır.
    - Ticari tanıtım sayfasının yeri PLAN T8.11'de, kurala uygun ücretsiz bir seçenekle belirlenir.
  - **Demo:** toplantı anında lokal kurulum + Cloudflare Quick Tunnel.
    - Hesap ve alan adı gerekmez.
    - Yalnız test/geliştirme amaçlı; 200 eşzamanlı istek sınırı var, SSE desteklenmiyor, adres her seferinde değişiyor.
    - Sürekli açık bir demo için ücretsiz katman veya öğrenci kredisi PLAN T8.8'de değerlendirilir.
    - Demolarda gerçek müşteri verisi yok.
  - **e-Belge testi:** Nilvera test portalı. Kamuya açık test bilgileri depoya girmez (`.env`).
  - **GitHub Student Developer Pack:** kullanıcı başvurursa (PLAN K1) alan adı, bulut kredisi ve geliştirici araçları için kullanılır. Avantajlar süreli olduğu için, süre bitince ücret doğuracak bir bağımlılık kurulmaz.
  - **Ücretliye geçiş:** yalnız ilk gelirden ve kullanıcı onayıyla (D-003, D-005).
- **Gerekçe:** `docs/research/planning-inputs.md` (koşullar ve kaynaklar).
- **Kaynak / tarih:** Claude, 2026-10-18.

### D-021 · Mesai türleri ve görev kategorileri
- **Durum:** Geçerli
- **Karar:**
  - **Görev kategorileri:** PLAN.md'deki her görev üç kategoriden birindedir.
    1. **K — kullanıcının yapacakları:** yalnız kullanıcının yapabileceği işler (müşteri ilişkisi, yasal işlemler, kişisel başvurular, ödeme).
    2. **B — birlikte yapılacaklar:** kullanıcının kararı, bilgisi veya onayı gereken işler.
    3. **C — Claude'un yapacakları:** Claude'un tek başına yapabileceği işler. Görevin içindeki onay adımı (ör. yayın) `USER_TASKS.md`'ye yazılır; görevin geri kalanı C kalır.
  - **Standart mesai:** kullanıcı ve Claude birlikte çalışır. B görevleri, kararlar ve onaylar burada yapılır.
  - **Otonom mesai:** Claude tek başına çalışır, kullanıcı ekran başında değildir. Kurallar:
    1. Mesaiyi kullanıcı başlatır. Claude önce `state.json`, `PLAN.md` ve `USER_TASKS.md`'yi okur.
    2. Yalnız C görevleri yapılır, PLAN sırasıyla. Bağımlılığı karşılanmamış ya da kullanıcı gerektiren görev atlanır.
    3. Kullanıcıya soru sorulmaz. Bir konu kullanıcı kararı gerektirirse:
       - geri dönüşü kolaysa Claude makul bir varsayımla devam eder ve varsayımı `USER_TASKS.md`'ye soru olarak yazar;
       - geri dönüşü zorsa o iş durdurulur, soru `USER_TASKS.md`'ye yazılır, sıradaki göreve geçilir.
    4. Dışa dönük ve onay gerektiren işler yapılmaz, yalnız hazırlanır: yayın, depo ayarı, ücretli servis, hesap açma, dış katkı, force-push. Onay `USER_TASKS.md`'de beklenir. Proje deposuna normal push önceden onaylıdır (D-015).
    5. Kullanıcı etkileşimi gerektiren adımlar denenmez: yönetici izni (UAC), tarayıcıda oturum açma, doğrulama kodları. Bunun yerine etkileşimsiz bir yol aranır (ör. taşınabilir kurulum); bulunamazsa `USER_TASKS.md`'ye eylem yazılır.
    6. Değişmez kurallar aynen geçerlidir (CLAUDE.md). Normalde "dur ve sor" denen durumda otonom mesaide: dur, soruyu yaz, başka göreve geç.
    7. Her görev sonunda belge protokolü, commit ve push. Mesai yarıda kesilse de iş kaybolmaz.
    8. Mesai sonu: Claude, yapılabilir C görevi kalmayınca ya da çalışma süresi dolunca mesaiyi kapatır. CHANGELOG.md'ye mesai özeti yazılır, `USER_TASKS.md` güncellenir, son push yapılır. Kullanıcı mesaiyi istediği an bitirebilir.
  - Mesainin türü `state.json` → `session` alanında tutulur. Böylece bağlam sıkıştırması veya yeni oturum sonrasında kural korunur.
- **Gerekçe:**
  - Kullanıcı her zaman ekran başında olamaz. Otonom mesai, kullanıcı yokken de C görevlerinin ilerlemesini sağlar.
  - Kategoriler, hangi işin hangi mesaide yapılacağını ve kullanıcının neyi beklediğini açık hale getirir.
- **Kaynak / tarih:** Kullanıcı (mesai türleri ve üç kategori), 2026-10-18. Otonom mesai kurallarının ayrıntısı Claude'a ait.

---

## Ertelenmiş kararlar

### D-013 · Üretim barındırma yeri
- **Durum:** Ertelendi
- **Kapsam:** bizim yönettiğimiz üretim sunucusunun yeri ve sağlayıcısı. Teslim biçimi (on-prem / yönetilen kurulum / SaaS) bu kararın konusu değil; D-018'de.
- **Neden şimdi gerekmiyor:**
  - Geliştirme bu bilgisayarda yapılıyor ve gerçek müşteri verisi yok.
  - Barındırma yeri, gerçek müşteri verisi işlenmeye başladığında önem kazanır (KVKK, e-Belge saklama kuralı). Sunucu ücreti de o zaman doğar.
  - İlk müşteri on-prem kurulum seçerse bu karar daha da ertelenebilir.
- **O zamana kadar geçerli düzen:**
  - Geliştirme lokal (0 TL).
  - Müşteri verisi içermeyen demolar ücretsiz yöntemlerle (D-020).
- **Şimdiden geçerli mimari kısıt:** sağlayıcıdan bağımsız kalınır.
  - Yalnız standart Linux, PostgreSQL ve ters vekil kullanılır; bulut sağlayıcısına özel yönetilen servis kullanılmaz.
  - e-Belge saklama yeri ve yedek hedefi yapılandırılabilir olur.
- **Seçenekler ve ön öneri:** `docs/research/hosting.md` (ön öneri: üretim sunucusu Türkiye'de).
- **Karar noktası:** T9.5 (bizim sunucumuzda çalışacak ilk müşteriden önce; ilk gerçek müşteri verisi bu sunucuya girecek).
- **Kaynak / tarih:** Kullanıcının "hemen karar vermeli miyiz?" sorusu üzerine Claude, 2026-10-18.
