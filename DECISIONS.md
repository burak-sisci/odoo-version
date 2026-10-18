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
> - `**Karar noktası:**` ve `**Yeniden değerlendirme:**` satırları ROADMAP görevine bağlanır. O görev tamamlandığında kayıt güncellenmezse `tools/check_docs.py` hata verir.
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
| D-013 | Barındırma ve dağıtım modeli | Ertelendi |
| D-014 | Çalışma adı ve teknik modül öneki | Geçerli |
| D-015 | Git deposu, GitHub ve push yetkisi | Geçerli |
| D-016 | Kendi modüllerimizin lisansı | Açık |

---

## Geçerli kararlar

### D-001 · Ürün hedefi
- **Durum:** Geçerli
- **Karar:** Odoo Community tabanlı, **kendi markamızla müşterilere satılacak** bir ERP. Satış biçimi ürün ve/veya SaaS.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-002 · Kapsam
- **Durum:** Geçerli
- **Karar:** Hedef, Odoo'da normalde bulunan **tüm uygulamaların** (Community + Enterprise) işlevsel karşılığı.
  Sıralama, Türkiye pazarına, yasal zorunluluklara ve kaynaklarımıza göre `docs/MODULE_MATRIX.md` içinde yapılır.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-003 · Ekip ve çalışma modeli
- **Durum:** Geçerli
- **Karar:** Ekip = kullanıcı + Claude.
  - Kullanıcı ürün sahibi ve son karar mercii.
  - Claude araştırma ve geliştirmeyi **çoğunlukla otonom** yürütür.
  - Claude şu durumlarda kullanıcıya sorar: açık kararlar, para gerektiren her şey, hukuki belirsizlik, dışa dönük işlemler (yayınlama, paylaşma, depo ayarları).
  - İstisna: proje deposuna her adım sonunda push önceden onaylıdır (D-015).
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-004 · Dokümantasyon protokolü
- **Durum:** Geçerli
- **Karar:** Proje belgeleri her adımda güncel tutulur. Eski kararın belgede kalması ya da yeni kararın eklenmemesi kabul edilemez.
  Uygulama biçimi `CLAUDE.md` → "Belge güncelleme protokolü"; denetim `tools/check_docs.py`.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-005 · Bütçe
- **Durum:** Geçerli
- **Karar:** Sıfır bütçe. Ücretli lisans, servis veya altyapı kullanılmaz.
  Para gerektiren adımlar ya ilk gelire kadar ertelenir ya da maliyeti müşteriye aittir (ör. e-Fatura entegratör kontörü).
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
  3. AGPL-3 OCA modülleri ayrı tutulur. Değiştirilirse, SaaS kullanıcılarına değiştirilmiş kaynak sunulur (AGPL ağ maddesi).
  4. Kapalı kaynak (kendi lisansımızla) modüllerimiz **AGPL modüllere bağımlı olamaz** (`depends`). Kapalı modül olup olmayacağı D-016'ya bağlı.
  5. Projeye giren her 3. parti modül `docs/COMPLIANCE.md` → lisans envanterine yazılır.
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
  - Her değişiklik `addons/` altındaki kendi modüllerimizle yapılır. Kullanılan yöntemler: model kalıtımı (`_inherit`), görünüm kalıtımı (XPath), JS `patch()`, asset paketinde dosya değiştirme (`replace`), controller override. Gerekirse modül içinden monkey-patch, gerekçesi kodda yazılı olarak.
  - Modülle çözülemeyen bir durum çıkarsa çekirdeğe dokunulmaz. Konu kullanıcıya yeni karar olarak getirilir.
  - Kabul edilen sonuç: son kullanıcıya görünmeyen teknik izler kalır (`odoo` Python paketi, `odoo-bin` komutu).
- **Gerekçe:** `docs/research/approach-b-vs-c.md`. Claude'un önerisi B+ idi, kullanıcı B'yi seçti.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

### D-011 · Odoo sürümü
- **Durum:** Geçerli
- **Karar:** **Odoo 20.0 Community.** Upstream `upstream/odoo` altına sabit bir commit ile eklenir (T1.3).
- **Gerekçe:**
  - Odoo her an son 3 ana sürümü destekler. 20.0 en uzun destek süresine sahip (~2029'a kadar).
  - Daha eski bir sürümle başlamak, ilk müşteriler gelirken zorunlu bir ana sürüm göçü demek.
  - MVP'nin (P0) hiçbir OCA modülüne ihtiyacı yok.
- **Kabul edilen bedel:**
  - Nilvera e-Belge modülleri 20.0'da Enterprise'da. 19.0'daki LGPL kodundan taşınacak (T3.1–T3.3).
  - OCA 20.0 dalları henüz neredeyse boş. P1 ve sonrası için OCA modülleri ya OCA taşıyınca alınır ya da kendimiz taşırız.
- **Yeniden değerlendirme:** T3.1. Nilvera port analizi beklenenden çok pahalı çıkarsa 19.0 seçeneği yeniden açılır.
- **Kaynak / tarih:** Kullanıcı kararı Claude'a bıraktı; Claude, 2026-10-18.

### D-012 · e-Belge stratejisi
- **Durum:** Geçerli
- **Karar:**
  - **MVP kapsamı:** e-Fatura + e-Arşiv. e-İrsaliye MVP sonrası (P1), e-Defter ileride.
  - **GİB'e gönderim yöntemi:** mevcut bir özel entegratörün API'si. Bu bir çalışma varsayımıdır; MVP sonunda yeniden ele alınacak.
  - **Mimari:** entegratörden bağımsız bir e-Belge çekirdeği + her entegratör için ayrı adaptör modülü.
  - **İlk adaptör:** Nilvera. 19.0'daki LGPL modüllerinden 20.0'a taşınır ve LGPL-3 kalır. Ücretsiz test ortamı var.
- **Yeniden değerlendirme:** T6.1 (MVP sonu: gönderim yöntemi kullanıcıyla yeniden ele alınır).
- **Gerekçe:** `docs/research/e-fatura.md`.
- **Kaynak / tarih:** Kullanıcı (kapsam ve yöntem), 2026-10-18. İlk entegratör seçimi Claude'a ait.

### D-014 · Çalışma adı ve teknik modül öneki
- **Durum:** Geçerli
- **Karar:**
  - **Çalışma adı:** `odoo-version`. Geçicidir, MVP sonunda kalıcı adla değişecek. GitHub deposunun adı da budur.
  - **Teknik modül öneki:** `ov_`. Markadan bağımsızdır ve kalıcıdır.
    - Marka değiştiğinde modül adları değişmez; yalnız marka modülündeki görünen ad değişir. Kurulu bir modülün teknik adını değiştirmek veritabanı göçü gerektirir, bu yüzden önek sabit tutulur.
    - Odoo 20.0'da `ov_` ile başlayan modül yok (2026-10-18). `x_` öneki Odoo'da özel alanlara ayrılmış olduğu için kullanılamaz.
  - **D-007 ile ilişki:** çalışma adı "Odoo" sözcüğünü içeriyor. Bu yüzden yalnız depoda, belgelerde ve geliştirme ortamında kullanılır. Ürün müşteriye, pilot kullanıcıya veya dış demoya çıkmadan önce kalıcı ad zorunludur.
- **Yeniden değerlendirme:** T6.1 (kalıcı ad ve yeniden adlandırma).
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
  - Diğer dışa dönük işlemler yine kullanıcı onayı ister: depo ayarları (görünürlük, yeniden adlandırma), sürüm yayınlama (release), başka yerde paylaşma.
- **Kaynak / tarih:** Kullanıcı, 2026-10-18.

---

## Ertelenmiş kararlar

### D-013 · Barındırma ve dağıtım modeli
- **Durum:** Ertelendi
- **Neden şimdi gerekmiyor:**
  - Geliştirme bu bilgisayarda yapılıyor ve gerçek müşteri verisi yok.
  - Barındırma yeri, gerçek müşteri verisi işlenmeye başladığında önem kazanır (KVKK, e-Belge saklama kuralı). Sunucu ücreti de o zaman doğar.
- **O zamana kadar geçerli düzen:**
  - Geliştirme lokal (0 TL).
  - Müşteri verisi içermeyen demolar ücretsiz yöntemlerle (Cloudflare Tunnel veya ücretsiz bulut katmanı).
- **Şimdiden geçerli mimari kısıt:** sağlayıcıdan bağımsız kalınır.
  - Yalnız standart Linux, PostgreSQL ve ters vekil kullanılır; bulut sağlayıcısına özel yönetilen servis kullanılmaz.
  - e-Belge saklama yeri ve yedek hedefi yapılandırılabilir olur.
- **Seçenekler ve ön öneri:** `docs/research/hosting.md` (ön öneri: üretim sunucusu Türkiye'de).
- **Karar noktası:** T6.3 (ilk pilot müşteriden önce; ilk gerçek müşteri verisi bu sunucuya girecek).
- **Kaynak / tarih:** Kullanıcının "hemen karar vermeli miyiz?" sorusu üzerine Claude, 2026-10-18.

---

## Açık kararlar (kullanıcı onayı bekliyor)

### D-016 · Kendi modüllerimizin lisansı
- **Durum:** Açık
- **Neden gerekli:**
  - Depo herkese açık (D-015), içindeki her şey herkes tarafından görülebilir.
  - Her modülün manifest dosyasında bir `license` değeri bulunmak zorunda.
  - Bir sürüm açık kaynak lisansla yayımlandıktan sonra o sürüm için lisans geri alınamaz.
- **Bu karardan bağımsız olarak sabit olanlar:**
  - 19.0 LGPL koddan türetilen modüller (Nilvera portu) LGPL-3 kalır (D-008/2).
  - Depoda LICENSE dosyası olmadığı sürece içerik "tüm hakları saklı" sayılır.
- **Seçenekler:**
  - **A — AGPL-3:** herkes kullanabilir. Değiştirip SaaS olarak sunan, değişikliklerini açmak zorunda. OCA'nın AGPL modüllerine serbestçe bağımlı olabiliriz.
  - **B — LGPL-3:** Odoo ekosisteminin varsayılanı. Başkaları kodu kapalı ürünlerinde kullanabilir; koruma en az.
  - **C — Kapalı lisans** (`OPL-1` veya `Other proprietary`):
    - Kod public depoda görünür ama izinsiz kullanılamaz; public depoda uygulatması zayıf.
    - AGPL OCA modüllerine bağımlı olamaz (D-008/4).
  - **D — Karma:** açık modüller bu public depoda; kapalı tutmak istediklerimiz ayrı bir **private** depoda (GitHub'da ücretsiz).
- **Claude önerisi:** **A, gerekirse D ile.**
  - Gelir kodu satmaktan değil, hizmetten gelecek: SaaS, e-Belge uyumu, destek, Türkiye yerelleştirmesi.
  - Kodu alıp kapalı bir SaaS'ta kullanan rakibe karşı en güçlü açık kaynak lisansı AGPL.
  - Gerçekten gizli kalması gereken bir modül çıkarsa o modül private depoya konur.
- **Karar noktası:** T2.2 (ilk modülümüz yazılmadan önce).
