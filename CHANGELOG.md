# Değişiklik Günlüğü

Son güncelleme: 2026-11-04

Her adımın kaydı en üste, tarih başlığıyla eklenir. Bir karar değiştiğinde **eski metni ve değişiklik nedeni** buraya yazılır (DECISIONS.md yalnız güncel hali tutar).
Kategoriler: **Kararlar**, **Belgeler**, **Kod**, **Ortam**, **Araştırma**.

## 2026-11-04

### Adım: `spreadsheet` çevirisi ve makine çevirisi hataları (T3.6, 7. adım) — otonom mesai 6

**Kod**
- Çeviriler: `spreadsheet` 467 eksik terim; 2.468/2.468 tam. Paket kapsamı %90,31 → %91,89; eksik 2.860 → 2.393.
  - Kapsam: grafik önerileri ve açıklamaları, adlandırılmış aralıklar, sayfa kilitleme, yazdırma, istatistik işlevlerinin (T.TEST, SKEW, KURT, GEOMEAN …) açıklamaları ve hata iletileri, pivot gösterim biçimleri.
  - Bağlantıyla bölünmüş cümle ("Automatic evaluation is disabled. Press [here] or F9 to recalculate.") Türkçe söz dizimine göre üç parçaya dağıtıldı: "… Yeniden hesaplamak için [buraya] tıklayın veya F9'a basın."
- Upstream düzeltmeleri (makine çevirisi hataları), 19 terim:
  - `spreadsheet`: "Wrap" → "Şal" (giysi) ve "Clip" → "Klips" yerine "Kaydırma", "Kırpma"; "Freeze"/"Unfreeze" → "Donmak"/"Çözme" yerine "Dondur"/"Dondurmayı kaldır"; "All matches", "First match" → "Tüm maçlar", "İlk maç" yerine "eşleşme"; "Match to end" → "Maç bitmek üzere" yerine "Metin sonunu eşleşme say"; ölçü → "önlem" (2 terim); "… copied to clipboard" → "Panoya kopyalanan …" (ad öbeği) yerine "… panoya kopyalandı" (4 terim).
  - `web` emoji adları: iskambil renkleri "kulüp kıyafeti", "elmas takım elbise", "kalp takım elbise", "maça takım elbise" yerine "sinek", "karo", "kupa", "maça".
  - Tarama yöntemi: bütün upstream `tr.po` dosyalarında şüpheli sözcükler (maç, şal, donmak, önlem, "panoya kopyalanan") arandı; "önlemek" (to prevent) gibi doğru kullanımlar elendi. `html_editor`'deki "Panoya kopyalanan çapa" sıradaki `html_editor` partisinde ele alınacak.
- Düzeltme tablosu (`CORRECTIONS`) 4 terim büyüdü: "Wrap", "Freeze", "Match to end", "club suit". Mutasyon denemesi: `spreadsheet.po`'da "Wrap" yeniden "Şal" yapılınca `test_corrections` (`module='spreadsheet', src='Wrap'`) düştü; dosya geri yüklendi, `ov_i18n_tr` 12/12.
- `check` 11 dosya, 0 sorun. CI kapsam eşiği `--min 90.1` → `91.7`.

**Kararlar**
- K24'e hesap tablosu terimleri eklendi.

**Belgeler**
- PLAN.md (T3.6 ilerleme, düzeltmeler, sıradaki modüller, testler), USER_TASKS.md (K24), README.md, state.json.

### Adım: `base` çevirisi (T3.6, 6. adım) — otonom mesai 6

**Kod**
- Çeviriler: `base` 494 terim (490 eksik + 4 düzeltme); 3.555/3.555 tam. Paket kapsamı %88,65 → %90,31; eksik 3.350 → 2.860.
  - Kapsam: kullanıcı formu, erişim yetkileri ve grup ekranları, sunucu işlemi formu, para birimi, banka hesabı, ülkelere göre şirket kimlik numaralarının adları ve örnekleri, ORM hata iletileri, demo şirketin fatura koşulları.
  - Upstream düzeltmesi: erişim hatasındaki işlem adları "oluşturun", "oku", "yazmak" diye karışık çevrilmişti; hepsi ad biçiminde ("oluşturma", "okuma", "yazma", "silme"). Hata cümlesi de ardından gelen kayıt listesine bağlandı ("… kullanıcısının şu kayıtlar için 'okuma' erişimi yok:").
  - Örnek kimlik numaralarında "or" → "veya"; "NIN" örneği TCKN olarak yazıldı.
- Doğrulama: `check` 11 dosya, 0 sorun; `ov_i18n_tr` 12/12 (gerçek çeviri dosyalarının Odoo okuyucusuyla okunması `base`'in kod metinlerini de karşılaştırıyor).
- CI kapsam eşiği `--min 88.5` → `90.1`.
- `471ad34`'ün CI'ı GitHub kesintisi bitince çalıştı ve geçti.

**Kararlar**
- K24'e `base` terimleri eklendi (Erişim Yetkisi, Kısıtlama/İzin, Kapsam, Sınırlı Kullanıcı, Kapsanan/Kapsayan Grup, Genel Kullanıcı, Takas Numarası; işlem adları).

**Belgeler**
- PLAN.md (T3.6 ilerleme, düzeltme, sıradaki modüller), USER_TASKS.md (K24), README.md, state.json.

### Adım: `web` arayüz metinleri ve "Discard" düzeltmesi (T3.6, 5. adım) — otonom mesai 6

**Kod**
- Çeviriler: `web` 270 terim; arayüz metinleri tam (4.519/5.178). Paket kapsamı %87,74 → %88,65; eksik 3.619 → 3.350.
  - Upstream düzeltmesi: "Discard" düğmesi "Sil" (silme) diye çevrilmişti, kaydı sileceği izlenimini veriyordu. 7 modülde "Vazgeç" oldu (`web`, `html_editor`, `spreadsheet`, `sale`, `mrp`, `stock`, `mail`); `mail`'deki "Discard editing" de "Düzenlemeden vazgeç".
  - Fatura düzeni önizlemesindeki örnek ürün metinleri Türkçe; tutarlar, şirket adı ve adres örneği aynı kaldı.
  - Emoji arama anahtar sözcüklerindeki tek harfler (kan grubu düğmeleri) ve Japonca karakterler olduğu gibi kopyalandı.
  - `web` modül açıklamasında reStructuredText başlık çizgisi başlıktan bir karakter kısa yazılmıştı; denetim aracı yakaladı, düzeltildi.
- Yeni test `TestOverlayFiles.test_corrections`: upstream düzeltmelerinin tablosu (`CORRECTIONS`) Odoo'nun okuduğu çevirilerle karşılaştırılıyor. Yerine "Sil" geri yazıldığında `web` alt testi düşüyor, düzeltmeyle geçiyor; `ov_i18n_tr` 12/12.
- Ertelenen: `web`'in 659 simge arama etiketi (`web/icons.py`). Upstream'in simge araması İngilizce etiketlere de bakıyor (`html_editor/tools.py`, `search_icons`); çeviri yalnız Türkçe aramayı ekler.
- CI kapsam eşiği `--min 87.6` → `88.5`.
- Önceki commit'in (`471ad34`) CI'ı GitHub Actions kesintisi yüzünden kuyrukta bekliyor ("Incident with Actions and Pages", githubstatus.com).

**Kararlar**
- K24'e varsayım eklendi: simge arama etiketleri en sona; çevrildiklerinde her simgeye küçük harfli kısa bir Türkçe anahtar sözcük listesi yazılacak.

**Belgeler**
- PLAN.md (T3.6 ilerleme, düzeltme, sıradaki modüller, testler), USER_TASKS.md (K24), README.md, state.json (otonom mesai 6).

### Otonom mesai 5 — özet

Mesai, kullanıcının isteğiyle T3.6 sürerken kapandı (2026-11-04). Elde olan `mail` partisi bitirilip kaydedildi.

**Biten görev:** yok. T3.6 Türkçe çeviri `[~]` sürüyor; kapı ölçütü %95, ulaşılan %87,74.

**İlerleme:** toplam 31/114 görev; F3 5/9. T3.6'da dört adım:
1. Çeviri katmanı `ov_i18n_tr` ve ölçüm aracı `tools/po_coverage.py`. Hatalı upstream çevirileri kurulumda düzeltiliyor.
2. `account`, `sale`, `purchase` tam. `{{ … }}` ifade denetimi Python AST'siyle yapılıyor; araç testleri (`tools/tests`) eklendi.
3. `stock`, `mrp` tam.
4. `mail` tam.

Paket kapsamı %81,11 → %87,74. Eksik 5.576 → 3.619 (1.957 terim çevrildi). CI eşiği her partide yükseldi: 81.1 → 87.6.

**Yarım kalan:** T3.6'da sırada `web` (928 eksik), `base`, `spreadsheet`, `product`, `calendar`, `html_editor`. `web`'deki "Discard" → "Sil" upstream hatası henüz düzeltilmedi ("Vazgeç" olacak). Sıra ve sayılar PLAN.md'deki T3.6 ilerleme notunda.

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** K24 — çevirinin tamamlanma yöntemi ve terim tercihleri (muhasebe, stok/üretim, mesajlaşma). Geri dönüşü kolay varsayımlarla ilerledi.

**Onay bekleyen dışa dönük iş:** yeni onay yok. K9 (GitHub güvenlik özellikleri) duruyor.

**Zaman kısıtlı:** K2 TÜBİTAK 2209-A son başvuru 11 Kasım 2026.

**CI:**
- `73e30e4` düştü: `test_module_name` CI'da `account` kurulu geldiği için başarısız oldu. `2d55aa6`'da düzeltildi.
- `2d55aa6` ve `56a760b` Linux'ta geçti.
- Yerelde `ov_i18n_tr` 11/11 geçti.

### Adım: `mail` çevirisi (T3.6, 4. adım) — otonom mesai 5

**Kod**
- Çeviriler: `mail` 735 terim (2.519/2.519). Hepsi eksik tamamlama. Paket kapsamı %85,25 → %87,74; eksik 4.354 → 3.619.
  - Davet e-postası parçaları, cümle sırası şablondaki sabit ifade yerlerine göre kuruldu. Bunlar takipçi daveti ("… sizi takipçi olarak ekledi") ile aktivite ataması ("… size aşağıdaki aktiviteyi atadı. Belge: …").
  - Modül açıklaması reStructuredText olarak docutils'le uyarısız işlendi.
- CI kapsam eşiği `--min 85.1` → `87.6`.

**Kararlar**
- K24'e mesajlaşma terim tercihleri eklendi (varsayım): Thread → Konu, Call → Arama, Bookmark → Yer İşareti, Chatter → Mesaj akışı, Artifact → Çıktı.

**Belgeler**
- PLAN.md (T3.6 ilerleme ve sıradaki modüller), USER_TASKS.md (K24, §1), README.md, state.json (oturum `standart`).

### Adım: `stock` ve `mrp` çevirileri (T3.6, 3. adım) — otonom mesai 5

**Kod**
- Çeviriler: `stock` 288 terim (1.919/1.919), `mrp` 209 (1.167/1.167). Hepsi eksik tamamlama; upstream çevirisi değiştirilen terim yok. Paket kapsamı %83,57 → %85,25; eksik 4.851 → 4.354.
  - Etiket yazıcısı (ZPL) şablonlarında yalnız kod içeren parçalar olduğu gibi kopyalandı; metinler Türkçe harfsiz ("Paket Tarihi:", "Barkod yok").
  - `mrp` modül açıklaması reStructuredText olarak docutils'le uyarısız işlendi.
- CI kapsam eşiği `--min 83.5` → `85.1`.
- Önceki commit'in CI'ı (2d55aa6) başarılı: `test_module_name` düzeltmesi Linux'ta da geçti.

**Kararlar**
- K24'e stok ve üretim terim tercihleri eklendi (varsayım): Batch → Parti, Backorder → Kalan Teslimat, Replenishment → İkmal, Shop Floor → Üretim Alanı, Unbuild → Parçalama; ZPL metinleri Türkçe harfsiz.

**Belgeler**
- PLAN.md (T3.6 ilerleme), USER_TASKS.md (K24), README.md, state.json.

### Adım: `account`, `sale`, `purchase` çevirileri; ifade denetimi ve araç testleri (T3.6, 2. adım) — otonom mesai 5

**Kod**
- Çeviriler: `account` 423 terim (3.392/3.392), `sale` 185 (903/903), `purchase` 105 (656/656). Paket kapsamı %81,16 → %83,57; eksik 5.562 → 4.851.
  - E-posta şablonları (fatura, alıcı tarafından düzenlenen fatura, ödeme makbuzu, teklif/sipariş, sipariş onayı, ödeme durumu, proforma, teklif talebi) etiketlerin arasındaki metin parçaları çevrilerek yazıldı; etiketler ve QWeb ifadeleri aynı.
  - `purchase` modül açıklaması reStructuredText olarak docutils'le uyarısız işlendi.
  - Upstream düzeltmesi: doğrulama sihirbazındaki "dates for" ("gün") ve "amounts for" ("için tutar") parçaları cümleye uyacak biçimde yeniden çevrildi.
- `tools/po_coverage.py`: `{{ … }}` ifadelerinde çıktı metinleri (`and`/`or` işlenenleri, koşullu ifadenin dalları) artık çevrilebilir. Karşılaştırılan değerler, alanlar ve ifadenin yapısı Python AST'siyle karşılaştırılır. Önceki kural e-posta konularındaki `'Quotation'`/`'Order'` sözcüklerinin çevirisini reddediyordu.
- Yeni `tools/tests/test_po_coverage.py`: denetim kurallarının 8 testi. Eski kurala karşı çalıştırıldığında ifade testi düşüyor, yenisiyle geçiyor. pre-commit kancası `tool-tests` (`tools/` değişince) ve CI adımı.
- `ov_i18n_tr` testi `test_module_name`: CI'da bütün modüllerimiz birlikte kurulduğu için `account` kurulu geliyordu ve test düştü (önceki commit'in CI hatası). Test artık örnek modülü kurulu değil sayıyor; `account` kurulu veritabanında 11 test geçti.
- CI kapsam eşiği `--min 81.1` → `83.5`.

**Kararlar**
- K24'e terim tercihleri eklendi (varsayım): Credit Note → İade Faturası, Tax Return → Vergi Beyannamesi, Suspense Account → Geçici Hesap, Reconcile → Denkleştirme, hash → özetlenmiş (hash).

**Belgeler**
- PLAN.md (T3.6 ilerleme ve denetim), USER_TASKS.md (K24), ARCHITECTURE.md (araçlar, CI), CLAUDE.md (komutlar), state.json.

### Adım: Türkçe çeviri katmanı ve ölçüm aracı (T3.6, 1. adım) — otonom mesai 5

**Kod**
- Yeni modül `ov_i18n_tr` (LGPL-3, `base`'e bağlı, kendiliğinden kurulur). Upstream modülünün eksik ve hatalı Türkçe çevirileri `i18n_overlay/<modül>.po`'da; upstream'in `tr.po`'sundan sonra aynı içe aktarmada okunur.
  - Kod metinleri: `odoo.tools.translate.get_po_paths` sarıldı (süreç geneli; önbellek modül yüklenince boşaltılır).
  - Kayıt metinleri ve kurulu olmayan modüllerin adları: aynı işlevin `ir.module.module` ve manifest okuyucusundaki kopyaları yalnız bu modülün yükleyicileri çalışırken çeviri dosyamızı ekler (`contextvars`). Modülün kurulu olmadığı veritabanı etkilenmez.
  - Upstream kuralları korunur: kurulumda yazılır, güncellemede eksik tamamlanır, `noupdate` kayda dokunulmaz. Bu modülün kendi kurulumunda önceden kurulu uygulamalara da yazılır (var olanın yerine; K24 varsayımı).
- `tools/po_coverage.py`: paket modüllerinin Türkçe çeviri kapsamı (`report`), eksik terimler (`missing`), çeviri ekleme (`add`, doğrulayarak), terim arama (`lookup`), denetim (`check`), şablonla eşitleme (`sync`).
  - Paket listesi statik hesaplanıyor: `MVP_APPS` + modüllerimiz + bağımlılıklar + kendiliğinden kurulanlar; TR dışı ülke modülleri ve `ov_brand`'in kaldırdığı çevrim içi hizmetler hariç. CI'daki paket veritabanının 90 modülüyle birebir aynı (fark yalnız sonradan eklenen kendi modüllerimiz).
  - Denetim kuralları 12 örnekle sınandı (yer tutucu sırası ve adları, `{ad}`, etiket ve çevrilmeyen öznitelikler, satır başı/sonu, ürün adı eklenmesi, reStructuredText başlık çizgisi).
- pre-commit kancası `check-translations`; CI belge işinde kapsam eşiği (`--min 81.1`, her partide yükselir).
- `tools/run_tests.py`: hedef modüller her zaman `-i … -u …` ile çalıştırılıyor. Kendiliğinden kurulan modül veritabanı oluşturulurken geldiği için `-i` testleri başlatmıyordu (0 test).
- Testler: `ov_i18n_tr` 11 test, hepsi geçti (kurgusal çeviri dosyalarıyla Python ve web metinleri, eksik/var olan/`noupdate` kayıt, görünüm terimi, modülün kendi kurulumu, kurulu olmayan modül adı; gerçek çeviri dosyaları Odoo'nun okuyucusuyla).
- İlk çeviriler: `l10n_tr` 14 terim (7/21 → 21/21). Modül açıklamasındaki reStructuredText docutils'le uyarısız işlendi.

**Araştırma**
- Upstream'in çeviri yükleme yolları (20.0): `get_po_paths` üç yerde adıyla içe aktarılıyor; kod çevirileri süreç genelinde önbellekte; `TranslationImporter` sonraki dosyayı öncekinin üstüne yazıyor, kaydederken `overwrite` ve `noupdate` kuralını uyguluyor; `file_path` yüklü modülün dosyasını yalnız kendi klasöründe arıyor (ayrı addons yolunda `i18n_extra` olmuyor).
- `.pot` şablonları canlı terimlerle karşılaştırıldı (`ov_demo`): `account`'ta şablon dışı 379 terim (çoğu genel hesap planı verisi), `base` 164, diğerleri 0–3. Ölçüm şablona göre.
- Başlangıç kapsamı: 83 modül, 29.518 terim, %81,11. En çok eksik: `web` 928, `mail` 735, `base` 490, `spreadsheet` 467, `account` 421.

**Kararlar**
- Varsayımlar `USER_TASKS.md` K24'e yazıldı (ayrı modül, kurulumda üzerine yazma, "Odoo" adının çeviride kalması, ölçüm yöntemi, terim tutarlılığı).

**Belgeler**
- PLAN.md (T3.6 durumu), USER_TASKS.md (K24, §1), ARCHITECTURE.md (katman tablosu, araçlar, CI, testler), docs/MODULE_MATRIX.md, docs/COMPLIANCE.md (§5 envanter), README.md, CLAUDE.md (komutlar), state.json.

## 2026-11-03

### Adım: e-posta ve portal altlarında "Powered by Nexus" (K17) — standart mesai

**Kullanıcının kararı:** "k17: B. powered by Nexus, ürün bağlantısız." (K17 seçenek B)

**Kararlar**
- K17: müşteriye giden e-posta ve sayfaların altında bağlantısız "Powered by Nexus". Eski metin: "Satırlar kaldırıldı, yerine ürün adı yazılmadı (K17 varsayımı A)". Neden: kullanıcı seçeneği.
  - K17'deki seçenek metninde yazdığı gibi müşteri satırı kapatabilir: Genel Ayarlar > Şirketler > Alt Bilgide Ürün Adı, varsayılan açık.
  - Türkçesi "Altyapı: Nexus" (Claude seçimi, USER_TASKS K17'de). Upstream "Powered by"ı tek başına "Hazırlayan" diye çeviriyor; portal altbilgisindeki "Powered by %s%s" ise "Tarafından desteklenmektedir Nexus" çıkıyordu. Ad metnin içine yer tutucuyla girdi, Türkçede sıra doğru.
  - Özet e-postasındaki "Sent by" satırı geri gelmedi; ad aynı e-postada iki kez yazmasın.

**Kod**
- `ov_brand`:
  - ortak şablon `ov_brand.powered_by` (çevrilebilir "Powered by %s", ad kaçışlı);
  - ayar `ov_powered_by` (`ov_brand.powered_by`, 20.0'ın tipli parametresiyle varsayılan açık);
  - portal sayfalarının altbilgisi aynı ayara bağlı, metni bu modülde çevriliyor.
  - Şablon değerleri (`ov_brand_name`, `ov_brand_color`, `ov_powered_by`) artık en küçük bağlamla (`minimal_qcontext`) oluşturulan şablonlara da veriliyor; e-postalar bu bağlamla oluşturuluyor.
- `ov_brand_mail`: iki bildirim düzeninde satır, takibi bırakma bağlantısının önünde ayraç. Ayraç bağlantının içinde: takipçi olmayan alıcıda upstream bağlantıyı silerken ayracı da siliyor.
- `ov_brand_portal`: belge kenar çubuğunda yayıncı logosu yerine satır. `ov_brand_digest`: şirket adının altında satır.
- Testler: yeni `test_powered_by.py` (bağlantısız, en küçük bağlamda da, ad kaçışlı, ayar, Türkçe); e-posta, portal ve özet testleri satırı ve ayarla gizlenmesini ölçüyor. E-posta testi upstream'in takipçi olmayan alıcı için yaptığı kişiselleştirmeyi de çalıştırıyor; bildirim düzeninin alt bilgisi, fatura, satış ve satın alma gönderimlerindeki gibi bağlamla açılıyor (20.0'da varsayılan kapalı).
- `test_web_path`: tarayıcı testi menü bağlantıları oluşmadan denetime başlayabiliyordu (temiz veritabanında bir kez düştü, tek başına iki kez geçti). Hazır olma koşulu artık menü bağlantılarını da bekliyor.
- Doğrulama: yedi marka modülü temiz veritabanında 86 test, 0 hata. Yeni dört metnin Türkçesi var (Odoo'nun terim çıkarıcısıyla `tr.po` karşılaştırıldı, yeni eksik 0).
- README.rst'ler (dört modül), `ov_brand` Türkçe çevirisi (4 metin).

**Belgeler**
- USER_TASKS.md (K17 `[x]`, §1'den çıktı), PLAN.md (T2.5 sonucu), docs/research/brand-inventory.md (§6), state.json.

### Adım: web istemcisi `/nexus` yolunda (K16); e-tablo formül adları kararı (K13) — standart mesai

**Kullanıcının kararları**
- "k16: B. marka adı" (K16 seçenek B).
- "k13: B. kendi ön ekimizle eş adlar eklensin." (K13 seçenek B). Ek sorulara yanıt: zaman "Düzenlemeyle", önek `NEXUS.`.

**Kararlar**
- K16: web istemcisi `/app` yerine `/nexus` yolunda. Eski metin: "Web istemcisi `/app` yolunda (K16 varsayımı)". Neden: kullanıcı ürün adını seçti.
  - `/app` yönlendirilmiyor. Yalnız geliştirme ortamında kullanıldı; müşteriye ya da demoya çıkmadı.
- K13: e-tablo formüllerine `NEXUS.` önekli eş adlar eklenecek; kayıtlı e-tablolar için `ODOO.` adları çalışmaya devam edecek, formül önerilerinde yalnız `NEXUS.` adları çıkacak. Eski metin: "teknik ad sayılır, izin listesinde kalır (K13 varsayımı)". Neden: kullanıcı seçeneği.
  - Zaman: e-tablo düzenlemeyle birlikte (OCA `spreadsheet_oca` portu, MODULE_MATRIX). Bugün Community 20.0'da e-tablolar yalnız salt okunur pano olarak açılıyor (`mode: "dashboard"`); formül adı hiçbir ekranda görünmüyor. Bu yüzden şimdi kod yok, `ODOO.*` sızıntı testinin izin listesinde kalıyor.

**Kod**
- `ov_brand`: `WEB_PATH` `/nexus` (`tools.py` ve `web_path.js`).
- Testler yolu sabitten okuyor (`test_web_path.py` tarayıcı adımları, `ov_brand_html_editor` önizleme testi); yol yeniden değişirse testlere dokunmak gerekmiyor.
- README.rst'ler (`ov_brand`, `ov_brand_html_editor`) `/nexus`. `brand_leak.py` izin listesi açıklaması K13 kararına göre.
- Doğrulama: `run_tests.py ov_brand,ov_brand_html_editor` 58 test, 0 hata.

**Belgeler**
- USER_TASKS.md (K13 ve K16 `[x]`, §1'den çıktı), PLAN.md (T2.4 sonucu, T2.6 izin listesi notu), docs/MODULE_MATRIX.md (e-tablo düzenleme satırı), docs/research/brand-inventory.md (§5, §10, baş not), README.md, state.json.

### Adım: örnek banka ekstrelerinde istenenler (K4) — standart mesai

**Kullanıcının isteği:** "örnek banka ekstreleri ile ilgili tam olarak isteklerini user_task.md dosyasına yaz. örneğin, ekstreler hangi işlemlerin çıktısı olsun? buna göre gerekli araştırmayı yapacağım."

**Belgeler**
- USER_TASKS.md K4 ayrıntılandı:
  - en az istenen (2 banka, TL hesap, 1 ay); bankalar, hesap türü, dönem ve biçimler;
  - ekstrede olması istenen işlemler: 7'si olmazsa olmaz, 10'u varsa iyi olur;
  - anonimleştirme kuralları (neyin değişeceği, neyin korunacağı, hangi araçla);
  - her dosya için not, bankaya sorulacak araştırma soruları ve dosyaların yeri (depo dışında).
- K4 §1'e eklendi. PLAN.md T5.2: bankalar MT940 ya da camt.053 veriyorsa OCA'nın bu biçimler için içe aktarıcıları da değerlendirilir.

### Adım: ilk iki commit'ten Claude ortak yazar satırı silindi (K10) — standart mesai

**Kullanıcının kararı:** "k10: claude ortak yazar satırı da silinsin." (K10 seçenek B)

**Yapılan**
- İlk iki commit'teki `Co-Authored-By: Claude` satırı ve önündeki boş satır silindi (`b267933` → `872fbf1`, `363a288` → `7c199aa`). Öteki 33 commit'in mesajı bayt bayt aynı.
- Yöntem 2026-10-19'dakiyle aynı: depo geçici bir çıplak kopyaya klonlandı, `git filter-branch --msg-filter` ile yalnız mesajlar yeniden yazıldı. Önceki geçmiş bir git paketine (bundle) yedeklendi (yerel, depo dışında).
- Denetim: 35 commit'in hepsinde dosya ağacı, yazar, işleyen ve tarihler aynı. Son commit'in ağacı değişmedi. Geçmişte `Co-Authored-By` satırı kalmadı.
- Yerel depo yeni geçmişe `git reset --soft` ile taşındı; çalışma alanı değişmedi. `main` `--force-with-lease` ile bir kez force-push edildi (`75ba52d` → `dfb751d`, üstüne bu kayıt).
- Bilinen sınır: GitHub eski commit'leri kimlikleriyle bir süre daha açabilir; eski CI çalıştırmaları eski kimlikleri gösterir. Katkıcı listesinin güncellenmesi biraz sürebilir.

**Commit kimlikleri (eski → yeni)**

2026-10-19 tablosunun "Yeni" sütunu bu tablonun "Eski" sütunudur.

| Eski | Yeni |
|---|---|
| `75ba52d` | `dfb751d` |
| `db97a74` | `82db439` |
| `23ca86d` | `54224e2` |
| `ff3ceb2` | `6056763` |
| `da141d5` | `851a8e4` |
| `183d2fe` | `251c56b` |
| `2b8cd27` | `7e6da9a` |
| `2307c4b` | `fb132a9` |
| `5e3dc81` | `7ee7b8e` |
| `19ed083` | `2e5183e` |
| `1d3d8a7` | `96ed93d` |
| `d0a89dd` | `3c72da5` |
| `ef074d3` | `7ed099d` |
| `4eee7bd` | `3850677` |
| `e4a98f7` | `fe49d3c` |
| `67a61ba` | `3d2c308` |
| `1dd6aaf` | `24133d4` |
| `ec14669` | `e8a306f` |
| `1bac273` | `7478a25` |
| `9e90991` | `e450845` |
| `9fee384` | `1e8747d` |
| `6a2fc36` | `24c5100` |
| `6309fd5` | `d35d8ab` |
| `1b94f2a` | `117fd43` |
| `6df7425` | `3d04eb8` |
| `95f94a8` | `5a4940f` |
| `6347bda` | `41d71a6` |
| `3f1d555` | `b42f278` |
| `05c4fa2` | `f121240` |
| `3f2edda` | `368c888` |
| `a8f6bd2` | `3a8849d` |
| `45bda8d` | `9288986` |
| `f33fe70` | `5fc8995` |
| `363a288` | `7c199aa` |
| `b267933` | `872fbf1` |

**Belgeler**
- USER_TASKS.md: K10 `[x]`, §1'den çıktı. DECISIONS.md D-015: force-push istisnaları ve eski commit'ler. state.json: bekleyenler.
- Bu dosyada geçen kimlikler güncellendi: mesai özetlerindeki CI notları (`23ca86d`, `db97a74`, `da141d5`) ve ilk CI çalıştırması notu (`6309fd5`). Eski kayıtlardaki K10 anlatımları tarihleriyle olduğu gibi kaldı.

### Otonom mesai 4 — özet

Mesai, kullanıcının isteğiyle T3.6'nın yöntem araştırması sırasında kapandı (2026-11-03).

**Biten görevler (2):**
- T3.4 il/ilçe adres yapısı: 973 ilçe (İçişleri Bakanlığı envanteri), il zorunlu, posta kodu isteğe bağlı, portal ve e-ticaret formunda ilçe seçimi;
- T3.5 TCMB döviz kurları: yeni modül `ov_l10n_tr_tcmb` (günlük iş, kur türü, eksik günleri tamamlama, geçmiş aktarımı).

**İlerleme:** toplam 31/114 görev; F3 5/9.

**Yarım kalan:** T3.6 Türkçe çeviri `[~]`. Yalnız upstream'in çeviri yükleme kodu okundu; kod ve belge değişikliği yok. Bulgular PLAN.md'deki T3.6 durum notunda: başka modülün kayıt metinleri bizim `.po`'muzla çevrilebiliyor; kod metinleri (Python, JS) ve sonradan kurulan uygulamalar için yükleme yönteminin genişletilmesi gerekiyor.

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** ikisi de geri dönüşü kolay varsayımlarla ilerledi.
- K22: ilçe listesinin kaynağı, "Merkez" ilçeler, il zorunlu, posta kodu isteğe bağlı (T3.4).
- K23: TCMB kur türü (döviz alış) ve tarih kuralı (önceki iş gününün kuru); mali müşavire K20 ile birlikte sorulabilir (T3.5).

**Onay bekleyen dışa dönük iş:** K10 (ilk iki commit'teki ortak yazar satırı, force-push gerekir), K9 (GitHub güvenlik özellikleri). Yeni onay yok.

**Zaman kısıtlı:** K2 TÜBİTAK 2209-A son başvuru 11 Kasım 2026.

**CI:** T3.4 (`54224e2`) ve T3.5 (`82db439`) commit'leri Linux'ta geçti. T3.5'te bütün modüllerle 147 test, MVP uygulamalarıyla marka sızıntısı ve dış istek testi 13 test; yayıncıya istek yok. Yerelde bütün modüllerle 146/146.

**Yerelde kalanlar:**
- PostgreSQL mesai sonunda düzgün kapatıldı (`python tools/pg.py stop`). Sonraki mesaide `python tools/pg.py start`.
- `ov_demo` güncel: `ov_l10n_tr` 20.0.1.2.0, `ov_l10n_tr_tcmb` 20.0.1.0.0 kurulu. 01.10–03.11.2026 TCMB kurları canlı ölçümden kaldı.
- Geçici veritabanları: `ov_brand_scan` ve `t12_base` (eski denemeler, silinmedi) ile `ov_test_*` test veritabanları (`tools/run_tests.py` her çalıştırmada yeniden kurar).
- Çalışan Odoo sunucusu ya da test tarayıcısı yok. Commit edilmemiş iş yok.

### Adım: TCMB döviz kurları (T3.5) — otonom mesai 4

**Kod**
- Yeni modül `ov_l10n_tr_tcmb` 20.0.1.0.0 (AGPL-3). `account` ve `ov_l10n_tr`'ye bağlı, kendiliğinden kurulur (G20).
- Bülten okuma (`tools.py`): `today.xml` ve tarih arşivi (`kurlar/YYYYAA/GGAAYYYY.xml`).
  - Ayrıştırıcı dış varlık ve DTD yüklemez; DOCTYPE'lı, 1 MB'tan büyük ya da `Tarih_Date` olmayan yanıt reddedilir. Geçersiz kod, birim ya da değer atlanır.
  - Bülten olmayan gün (404) boş döner. İstenen günden başka tarihli bülten hata sayılır.
  - Kur türü: döviz alış/satış, efektif alış/satış. Efektif kuru olmayan para birimlerinde aynı yönün döviz kuru kullanılır. Birim (JPY 100 gibi) bölünür.
  - Para birimi TRY olmayan şirket için kurlar Türk lirası üzerinden çapraz hesaplanır; şirketin para birimi bültende yoksa kur yazılmaz.
- Şirket (`res.company`): günlük güncelleme (ülkesi Türkiye olan şirkette açık gelir), kur türü (varsayılan döviz alış), son bülten tarihi.
  - Kurlar ana şirkete, yalnız etkin para birimlerine yazılır. Aynı güne kayıtlı kur değiştirilir.
  - Kaçırılan iş günleri arşivden tamamlanır, en çok 31 gün geriye; indirilen bülten aynı çalıştırmada tekrar istenmez.
- Zamanlanmış iş "TCMB: Döviz kurlarını güncelle": her gün 16.00 (İstanbul; bülten 15.30 sularında). Bağlantı ya da bülten hatasında uyarı yazılır ve iş bir saat sonrasına yeniden kurulur (`ir.cron._trigger`). İş, kullanıcısının şirketlerinden bağımsız bütün ana şirketleri tarar.
- Ayarlar: Faturalama ayarlarında Para Birimleri bölümünde "TCMB Döviz Kurları" (ikinci para birimi etkinken görünür). Günlük güncelleme, kur türü, son bülten, "Şimdi Güncelle", "Geçmiş Kurları Aktar". Şubede açılan ayar ana şirketin ayarıdır.
  - Bölüm upstream'in "kurları güncelle" ayarına değil bölümün kendisine bağlandı: `ov_brand` OCA `remove_odoo_enterprise` ile o ayarı (Enterprise modülü kutusu) kaldırıyor.
- Geçmiş aktarımı (`ov.tcmb.rate.import`, yalnız muhasebe yöneticisi): bir seferde en çok 62 gün, bugünden ileri gitmez. Bağlantı koparsa o güne kadar kaydedilenler korunur ve hangi günden yeniden başlanacağı söylenir. Son bülten tarihine dokunmaz.
- Çeviri: `i18n/tr.po` 37 metin. Modül açıklaması Türkçe README olduğu için çeviriye girmez.
- Testler: 28 yeni test (TCMB taklit edilir, dış istek yok). 10'u bülten okuma ve hesaplar, 18'i kur kaydı, tarih kuralı, zamanlanmış işin tamamlama, sınır, hata ve yeniden deneme davranışı, ayarlar, aktarım ve görünümler. Test bülteni kurgusal (13.01.2025).
  - Sonuç: `ov_l10n_tr_tcmb` 28/28; bütün modüllerle birlikte 146/146.
- Ölçüm (`ov_demo`, canlı TCMB; alınan kurlar demo veritabanında kaldı):
  - zamanlanmış iş 3,42 s: iki Türk ana şirkete 03.11.2026 bülteni. TR Company'de USD = 49,9094 TRY (TCMB döviz alış); para birimi USD olan şirkette TRY kuru aynı değerden;
  - 01.10–03.11.2026 aktarımı 5,2 s: 22 bülten, 22 kur. 28 ve 29 Ekim'de bülten yok (404);
  - dönüşümler: 31.10 ve 02.11'de 49,7747 (30.10 bülteni), 03.11'de 49,8827 (02.11 bülteni), 04.11'de 49,9094;
  - Türkçe arayüz: ayar ve sihirbaz metinleri, iş adı, tarih biçimi (03.11.2026).

**Araştırma**
- Kur tarihinin anlamı ölçüldü (`ov_demo`, geri alınan betik): 20.0'da bir kur, tarihinden sonraki günden başlayarak uygulanır (`_get_rates`, `name < tarih`). Önceki kur yoksa ilk sonraki kur kullanılır. Bu yüzden bülten kendi tarihiyle kaydedildi; işleme önceki iş gününün kuru uygulanır.
- TCMB arşivi: ortanca yanıt 0,35 s, en çok 3,46 s; art arda isteklerde bir kez 20 s zaman aşımı. Kütüphanenin varsayılan User-Agent'ı kabul ediliyor. Zaman aşımı 10 s bağlantı, 30 s okuma.
- OCA `currency` deposunun 20.0 dalında modül yok. `currency_rate_update` port edilmedi; kendi modülümüz yazıldı.
  - Eski metin (`docs/research/planning-inputs.md` §1): "TCMB için kendi modülümüz yeterli olabilir (T3.5'te karar)".
  - Neden: TCMB'ye özgü iş (kur türü, tarih kuralı, çapraz kur, tatil günleri) küçük ve tek kaynaklı; genel sağlayıcı çatısı 20.0'a port edilmeden gerekmiyor.

**Belgeler**
- PLAN.md: T3.5 `[x]` ve sonucu; F3 5/9; toplam 31/114; şu anki görev T3.6. §4'teki döviz satırı.
- USER_TASKS.md: K23 (TCMB varsayımları), §1'e eklendi.
- `docs/COMPLIANCE.md` §4: TCMB notu (çalışma anında alınan olgu verisi, istekte müşteri bilgisi yok; depoda TCMB verisi yok, envanter girişi gerekmez).
- `docs/research/l10n-tr.md`: T3.5 sonucu, G20 kapandı, G25 test sayıları. `docs/research/planning-inputs.md`: `currency_rate_update` satırı.
- `docs/MODULE_MATRIX.md`, README.md, ARCHITECTURE.md (Türkiye temeli), state.json.

### Adım: il/ilçe adres yapısı (T3.4) — otonom mesai 4

**Kod**
- `ov_l10n_tr` 20.0.1.1.0 → 20.0.1.2.0. Yeni bağımlılıklar `base_address_extended` ve `portal`. İkisi `l10n_tr` kurulunca zaten kuruluyor (`account` → `portal` → `base_address_extended`); kendiliğinden kurulma koşulu değişmedi.
- İlçe listesi (G19): `data/res.city.csv`, 81 ilin 973 ilçesi.
  - 922'si İçişleri Bakanlığı Mülki İdare Bölümleri Envanteri'nin ilçe listesinden. Büyükşehir olmayan 51 ilin merkez ilçesi bu listede yok; il belediyeleri listesinden "Merkez" adıyla eklendi.
  - Adlar envanterdeki büyük harften Türkçe yazıma çevrildi ("KARAİSALI" → "Karaisalı", "19 MAYIS" → "19 Mayıs").
  - `tools/tr_districts.py` (yeni): iki raporu indirir, okunan ilçeleri envanterin kendi sayılarıyla karşılaştırır (il başına ilçe sayısı, toplam 922), CSV'yi yazar. `--check` farkı bildirir; kayıtlı raporlardan aynı dosya yeniden üretildi.
- Ülke ayarları (`res.country._ov_l10n_tr_setup`):
  - ilçe listeden seçilir, il zorunlu, posta kodu isteğe bağlı;
  - adres biçimi `%(zip)s %(city)s/%(state_name)s` ("34710 Kadıköy/İstanbul"). İlçe ya da il boşsa eğik çizgi yazılmaz. İlçe seçilmiş ama şehir metni boşsa (içe aktarma, API) ilçenin adı yazılır.
  - `base.tr` noupdate olduğu için T3.3'teki XML veri dosyası (`data/res_country_data.xml`, yalnız VKN etiketi) kaldırıldı. Bütün ülke ayarlarını kurulum kancası ve güncelleme betiği aynı yöntemle yazar.
- Form: il seçiliyse ilçe listesi o ilin ilçeleriyle sınırlı (kişi ve alt kişi formu). Aynı adlı ilçeler ayrılır: Ereğli (Konya, Zonguldak).
- Portal ve e-ticaret adres formu: upstream ilçe seçimini beş ülkeyle (BR, CL, PE, CO, TW) sınırlıyor; Türkiye eklendi. İl seçilince ilçeleri gelir; ilçe ve il zorunlu.
- Kurulu kişiler (kurulum kancası, `migrations/20.0.1.2.0`): şehir metni tek bir ilçeyi gösteriyorsa kişi ilçeye bağlanır. Büyük/küçük harf, şapka ve boşluk farkı yok sayılır.
  - İl seçiliyse o ilin ilçesi; şehir alanına il adı yazılmışsa o ilin merkez ilçesi; il seçili değilse yalnız tek ilde bulunan bir ad.
  - Belirsizler (iki ilde aynı ad, bilinmeyen ad, il seçilmeden "Merkez") olduğu gibi kalır.
- Lint: ruff, yorum ve docstring'lerdeki Türkçe "ı" harfini "i"ye benzeyen karakter sayıyordu (RUF002, RUF003). `ruff.toml`'a `allowed-confusables = ["ı"]` eklendi: Türkçe harfler kod yorumlarında serbest (CLAUDE.md).
- Testler: 15 yeni test.
  - 11'i veri, ad yazımı, ülke ayarları, adres metni, form, ilçe alanının süzgeci ve kurulu kişilerin eşleştirilmesi için.
  - 4'ü portalın HTTP uçlarıyla: ülke bilgisi, ilin ilçeleri, adres kaydı, ilçe ve il zorunluluğu.
  - Sonuç: `ov_l10n_tr` 34/34; bütün modüllerle birlikte 114/114. Günlükteki 2 CRITICAL satırı bilinen upstream gürültüsü (test kipinde websocket kapalı, Chrome kapanırken bağlantı kopuyor).
- Ölçüm (`ov_demo`, 20.0.1.2.0'a güncellendi; göç 0,13 sn):
  - 973 ilçe; ülke ayarları yazıldı;
  - 7 Türk kişinin 2'si ilçeye bağlandı: Beyoğlu/İstanbul, Ürgüp/Nevşehir. Bağlanmayanlar: "Konak Belediyesi", "İç Anadolu Bölgesi" ve ili California görünen 3 demo kaydı.

**Araştırma**
- İlçe verisinin kaynağı değişti.
  - Eski metin (`docs/research/planning-inputs.md` §5): "`siberfx/turkiye-address` (MIT) ve GitHub `turkiye-il-ilce-listesi` konusu altındaki depolar". PLAN T3.4: "İlçe verisi açık lisanslı bir veri setinden gelir".
  - Neden: o depolar aynı olguların ikincil kopyası; doğrulukları ve güncellikleri resmî envantere bağlı. Resmî envanter kendi sayılarıyla denetlenebiliyor.
  - Lisans durumu `docs/COMPLIANCE.md` §4'te; varsayım `USER_TASKS.md` K22.
- Ad yazımı Wikidata'yla karşılaştırıldı (yalnız denetim, depoya girmedi). Yalnız büyük/küçük harf farkı olan ad yok. Wikidata'da o ile bağlı bulunmayan 44 adın 2'si şapkalı yazım (Balâ, Şehitkâmil); resmî yazım şapkasız. Kalanlar Wikidata'da ile bağlanmamış bilinen ilçeler (Çekmeköy, Gaziosmanpaşa gibi).
- e-Belge adres eşlemesi (T4.3 için): ilçe `cbc:CitySubdivisionName`, il `cbc:CityName`.

**Belgeler**
- PLAN.md: T3.4 `[x]` ve sonucu; F3 4/9; toplam 30/114; şu anki görev T3.5. §4'teki il/ilçe satırı; T4.3'e adres eşlemesi eklendi.
- USER_TASKS.md: K22 (il/ilçe varsayımları), §1'e eklendi.
- `docs/COMPLIANCE.md`: §4 ilçe listesi notu, §5 envanter satırı.
- `docs/research/l10n-tr.md`: T3.4 sonucu, G19 kapandı, kaynaklar. `docs/research/planning-inputs.md` §5: seçilen kaynak.
- `docs/MODULE_MATRIX.md`, README.md, ARCHITECTURE.md (Türkiye temeli, `tools/` ağacı, ruff notu), CLAUDE.md (ilçe listesi komutu), state.json.

### Otonom mesai 3 — özet

Mesai, kullanıcının isteğiyle T3.3'ten sonra kapandı (2026-11-03). Kullanıcı gerektiren işler mesai boyunca bekletildi; mesai sonunda birlikte ele alınacak.

**Biten görevler (5):**
- T2.6 marka sızıntısı testi (mesai 2'den süren);
- T2.7 dış istek testi; marka katmanı (F2) ve **M2 Markasız çekirdek** tamamlandı;
- T3.1 upstream `l10n_tr` analizi (26 eksik, her biri bir göreve bağlı);
- T3.2 `ov_l10n_tr`: Türk hesap planı ve vergi düzeltmeleri;
- T3.3 VKN / TCKN: kişi/şirket ayrımı, Türkçe etiketler, MERSİS denetimi.

**İlerleme:** toplam 29/114 görev; F3 3/9. Sıradaki C görevi T3.4 (il/ilçe adres yapısı), başlanmadı.

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** hepsi geri dönüşü kolay varsayımlarla ilerledi.
- K19: metinlerdeki eski ürün adı gösterimde değiştiriliyor (T2.6).
- K20: Türk hesap planındaki hesap eşlemeleri; mali müşavire üç soru (T3.2).
- K21: TCKN'li iş ortağı gerçek kişi; MERSİS'te yalnız 16 hane denetimi (T3.3).

**Onay bekleyen dışa dönük iş:** K10 (ilk iki commit'teki ortak yazar satırı, force-push gerekir), K9 (GitHub güvenlik özellikleri), K5 (yayınlar; şimdilik iş yok).

**Zaman kısıtlı:** K2 TÜBİTAK 2209-A son başvuru 11 Kasım 2026.

**CI:** T3.3 commit'i (`851a8e4`) Linux'ta geçti: bütün modüllerle 104 test, MVP uygulamalarıyla marka sızıntısı ve dış istek testi 13 test; yayıncıya istek yok. Yereldeki birleşik çalıştırma PostgreSQL kapandığı için yarım kaldı (T3.3 kaydı).

**Yerelde kalanlar:**
- PostgreSQL kapalı: 10:27'de bir Ctrl+C olayıyla kapandı (T3.3 kaydı). Sonraki mesaide `python tools/pg.py start`.
- `ov_demo` güncel: `ov_l10n_tr` 20.0.1.1.0.
- Geçici veritabanları: `ov_brand_scan` (T2.3 denemeleri; silinmesi bir önceki özette mesai sonuna bırakılmıştı, PostgreSQL kapalı olduğu için silinmedi) ve `ov_test_*` test veritabanları (`tools/run_tests.py` her çalıştırmada yeniden kurar).
- Commit edilmemiş iş yok.

### Adım: VKN / TCKN doğrulama, kişi/şirket ayrımı ve MERSİS (T3.3) — otonom mesai 3

**Kod**
- `ov_l10n_tr` 20.0.1.0.0 → 20.0.1.1.0. Modülün adı "Turkish Accounting Corrections" (Türkçesi "Türkiye Muhasebe Düzeltmeleri") idi, "Turkey - Localization" (Türkçesi "Türkiye Yerelleştirmesi") oldu. Neden: kapsam hesap planının dışına çıktı (kimlik numaraları; sırada il/ilçe, T3.4).
- Kişi/şirket ayrımı (G16): 20.0'da `is_company` hesaplanan bir alan; vergi numarası olan her iş ortağı şirket sayılıyordu. Türkiye'de 11 haneli vergi numarası (TCKN) olan iş ortağı artık gerçek kişi, şahıs şirketi dahil. 10 haneli VKN'li iş ortağı şirket kalır. Kural yalnız Türk iş ortaklarına uygulanır.
  - Kurulu iş ortakları kurulumda (`post_init_hook`) ve güncellemede (`migrations/20.0.1.1.0`) yeniden hesaplanır.
  - e-Belge için mükellef türü: `res.partner._ov_l10n_tr_tax_id_type()` ticari iş ortağına göre `VKN` / `TCKN` döner (T4.3'te `cac:Person` ve `schemeID`).
- Türkçe görünüm (G17):
  - ülkenin vergi numarası etiketi "VKN/TCKN";
  - iş ortağı ve şirket formunda yer tutucu "2222222222 (VKN) veya 11111111111 (TCKN)" (upstream'de İngilizce "NIN" kısaltması);
  - geçersiz numara hatası: "Ayşe Örnek için girilen VKN/TCKN [...] geçerli değil. VKN 10, TCKN 11 hanelidir."
- MERSİS (G18): 16 hane denetlenir, boşluk ve tire temizlenir; harfli ya da eksik/fazla haneli numara reddedilir. MERSİS, ticaret sicil ve şube numarası etiketleri Türkçe.
- Bulgu: `base.tr` ülke kaydı `noupdate`. Modülün XML verisi etiketi yalnız ilk kurulumda yazar; kurulu veritabanında etiketi güncelleme betiği yazar.
- Testler: 10 yeni test (kurgusal VKN/TCKN, resmî sağlama algoritmasıyla üretildi). `ov_l10n_tr` 19/19.
  - Bütün modüllerle birlikte yerel çalıştırma testlere geçmeden durdu: PostgreSQL 10:27'de bir Ctrl+C olayıyla kapandı (istemci süreci `0xC000013A` ile sonlandı, ardından hızlı kapanma). Kodla ilgisi yok; birleşik doğrulama Linux CI'da.
- Ölçüm (`ov_demo`, 20.0.1.1.0'a güncellendi, Türkçe): TCKN'li kişi `is_company = False`, VKN'li firma `True`; etiket "VKN/TCKN"; yer tutucu, etiketler ve hata metni Türkçe; "12AB" MERSİS olarak reddedildi.

**Araştırma**
- `docs/research/l10n-tr.md`: T3.3 sonucu notu; G16, G17, G18 kapandı. G18'in eski hedefi: "T3.3 (denetim), T3.6 (çeviri)". Neden: etiketler kimlik numarası kurallarıyla aynı yerde tanımlandığı için çevirileri de bu görevde yapıldı.
- MERSİS: 16 hane bütün kaynaklarda aynı. İç yapı (şirkette 0 + VKN + 5 hane, şahıs şirketinde TCKN + 5 hane) yalnız ikincil kaynaklarda geçiyor; bu yüzden denetlenmiyor (USER_TASKS K21).

**Belgeler**
- PLAN.md: T3.3 `[x]` ve sonucu; F3 3/9; toplam 29/114; şu anki görev T3.4. T4.3'teki `cac:Person` notuna T3.3'ün kuralı ve yöntemi eklendi.
- USER_TASKS.md: K21 (kişi/şirket ve MERSİS varsayımları), §1'e eklendi.
  - K15'in "Ne zaman" satırı ve `docs/research/brand-inventory.md`'deki iş ortağı otomatik tamamlama satırı Türkiye için yerli kaynağı T3.3'e bağlıyordu ("yerli kaynak T3.3", "Türkiye için yerel kaynak ayrı iş (T3.3)"). T3.3 bu işi içermiyordu. Yeni atıf: e-Belge mükellef sorgulaması VKN'den unvanı verir (T4.3, T4.5).
- `docs/MODULE_MATRIX.md`, README.md, ARCHITECTURE.md (Türkiye temeli satırı), state.json: T3.3 sonucu.

### Adım: temel yerelleştirme modülü `ov_l10n_tr` (T3.2) — otonom mesai 3

**Kod**
- `addons/ov_l10n_tr` (yeni, AGPL-3, `l10n_tr`'ye bağlı, kendiliğinden kurulur). Upstream'e dokunmadan `@template('tr', …)` uzantılarıyla; yöntem adları `_ov_l10n_tr_*`, böylece upstream'in yöntemlerinden sonra çalışıp onların verisine eklenir.
  - Hesap planı (`data/template/account.account-tr.csv`):
    - 69 hesabın adı düzeltildi: Türkçesi olmayanlar, büyük harf ve yazım hataları, yanlış çeviriler (391004/391005), kaymış ya da yanlış adlar (326, 437, 438, 54, 690/692).
    - 17 grubu ve 8 eksik hesap eklendi: 170, 178, 179, 480, 481, 502, 503, 523.
    - 193 ve 360 alacak/borç hesabı türünden vergi hesabı türüne alındı; hesapta kayıt varsa değişmez.
  - Şirket ayarları: erken ödeme indirimi 611/649, kasa farkı 679/689, cari yıl kârı veya zararı 590. Plan dışı 999 kodlu hesaplar artık açılmıyor. Kurulu bir şirket kendi 999999 hesabını korur; bu hesap Türkçe ad alır.
  - Vergiler (`account.tax-tr.csv`, `account.tax.group-tr.csv`):
    - 44 verginin ve 7 tevkifat grubunun Türkçe adı, açıklaması ve fatura etiketi: "%20 Tevkifatlı 2/10", "Satış Tevkifatı 2/10 (%-4)", "Tevkifat %-4", "DV %0,948".
    - "Kira Stopajı %-20" ve "Serbest Meslek Stopajı %-20" (yeni, 360'a kaydeder) ve "Stopaj %-20" grubu.
    - Upstream'in 191'e kaydeden kira stopajı pasif yapıldı.
  - Kurulu şirketler: `post_init_hook`, Türk hesap planlı her şirkete upstream'in modül kurulumundaki yeniden yükleme adımlarını uygular. Ardından Türkçe adları yazar; kullanıcının değiştirdiği ad korunur, yalnız upstream'deki haliyle ya da Türkçesi olmadan duran adlar değişir.
  - Kalıcı ad testi (`tests/turkish_names.py`): Türkçe bağlamda İngilizce kalan ad ve kısaltma, yasak ifadeler ("ne zaman", "satın al"), Türkçe büyük harf hatası (ince ünlüden sonra "I", kök sözlüğü), dipnot artığı. Upstream'in 400 Türkçe adından 35'ini işaretliyor; T1.6'da elle görülen örneklerin hepsi içinde.
  - 9 test: adlar, kuralların upstream hatalarını yakalaması, düzeltilen ve yeni hesaplar, özel hesaplar, stopajlı alış faturası (1.000 → 360'a 200, toplam 800), kurulu şirketin güncellenmesi, kurulu şirketin cari yıl kârı hesabı.
- Ölçüm (`ov_demo`, Türkçe bağlam): sorunlu ad 86 → 0 (366 hesap, 15 vergi grubu, 46 vergi, 8 mali pozisyon). `ov_l10n_tr` `ov_demo`'ya kuruldu.
- Testler: `ov_l10n_tr` 9/9; bütün modüllerle birlikte 93 test geçti, yayıncıya istek yok.

**Araştırma**
- `docs/research/l10n-tr.md`: T3.2 sonucu notu; §3.6 T3.2'de bulunanlar; §4'te kapanan eksikler işaretlendi; yeni eksikler G27 (999 kodlu özel hesaplar), G28 (kira stopajı 191'de), G29 (193/360 türü vergi kaydını engelliyor).
  - 17 grubu, 170–179 ve 502/503 MSUGT Sıra No 12 ile doğrulandı. G4'ün eski metni: "Eksik THP hesapları: 480, 481, 523 (doğrulandı); 170–179, 502/503 (doğrulanacak)". Neden: doğrulandı ve eklendi.
  - Damga vergisi oranları 2026'da değişmedi (G13). Kira ve serbest meslek stopajı %20 (GVK 94/5-a, 94/2-b).
  - Saat dilimi (G24): şirket dilimi ülkeden `Europe/Istanbul` hesaplanıyor (`ov_demo`'da iki şirkette ölçüldü). İş gerekmedi.
  - G9 ve G10'un eski hedefi: "T3.2 (oranlar), T4.3 (6xx kodları)" ve "T3.2 (vergiler), T4.3 (3xx kodları)". Yeni hedef T4.3. Neden: %10/%1 oranlı tevkifat ve istisna vergileri GİB kod listeleriyle (T4.2) birlikte tanımlanınca e-Belge'deki kodlarla tek seferde eşleşir. İhraç kayıtlı satış vergisinin incelenmesi de T4.3'e (IHRACKAYITLI tipi).

**Belgeler**
- PLAN.md: T3.2 `[x]` ve sonucu; F3 2/9; toplam 28/114; şu anki görev T3.3. T4.3'e T3.2'den taşınanlar, T5.8'e stopaj özeti ve K20 notu eklendi.
- USER_TASKS.md: K20 (hesap eşleme varsayımları ve mali müşavire üç soru), §1'e eklendi.
- `docs/COMPLIANCE.md` §4: mevzuat verisinin kaynağı ve lisans notu (envantere dış kod girişi gerekmez).
- `docs/MODULE_MATRIX.md`: `ov_l10n_tr` `plan` → `geliştiriliyor` (T3.3, T3.4 ve T4.3 de bu modüle eklenecek).
- ARCHITECTURE.md (Türkiye temeli satırı), README (durum ve madde), `state.json` (modül, görev, sonraki işler).
- Eski kalmış iki durum bilgisi düzeltildi:
  - README "Durum: Faz 2 — Marka katmanı. Faz 1 (geliştirme altyapısı) tamamlandı." → Faz 3; F2 T2.7'de bitmişti.
  - `state.json` `next_milestone` "M2 Markasız çekirdek" → "M3 Türkiye temeli".
- `state.json` `docs` listesine T3.1'de eklenmemiş `docs/research/l10n-tr.md` eklendi.

### Adım: `l10n_tr` (20.0) analizi (T3.1) — otonom mesai 3

**Araştırma**
- `docs/research/l10n-tr.md` (yeni): upstream `l10n_tr` (commit `afbcf79d`) ve çekirdekteki Türkiye'ye özgü kod incelendi; `ov_demo`'da Türkçe bağlamda ölçüldü.
  - Var olan: 347 hesap, 44 vergi, 8 mali pozisyon, vergi ve damga vergisi raporu.
  - 1.046 vergi dairesi: 81 ilin hepsi, ilsiz kayıt ve tekrar yok, ek veri gerekmez.
  - VKN/TCKN sağlaması çekirdekte (`check_vat_tr`); Türkçe tarih/sayı biçimi ve hafta başı doğru.
- 26 eksik (G1–G26), her biri bir göreve bağlandı. Başlıcaları:
  - 20 hesabın Türkçe adı yok; ~25 hesapta büyük harf ve yazım hatası.
  - Yanlış çeviriler: "Sales WH" → "SATIŞ NOKTASI", "Purchases WH" → "SATIN ALIMLAR NE ZAMAN", tevkifat grupları "ne zaman %-20".
  - 31 vergi Türkçe ekranda İngilizce kısaltmalı; KDV tevkifatına "stopaj" deniyor.
  - TCKN'li gerçek kişi şirket sayılıyor (ölçüldü).
  - Tevkifat yalnız %20 KDV için; istisna ve gelir vergisi stopajı tanımları eksik.
  - Eksik THP hesapları 480, 481, 523.
  - Çeviri kapsamı: `l10n_tr` %33,3, paket modülleri %70,8–86,3.
- Mevzuat karşılaştırmasında resmî tebliğ metnine ulaşılamadı. İkincil kaynakla doğrulananlar ayrıldı; oranların ve kodların tek tek doğrulanması T3.2/T4.3'te.

**Belgeler**
- PLAN.md:
  - T3.1 `[x]` ve sonucu; F3 `[~]` 1/9; şu anki görev T3.2.
  - T3.2 maddeleri T3.1'e göre yazıldı. Eski metin: "T3.1'e göre eksik vergi, tevkifat ve istisna tanımları. / Türkiye varsayılanları: TRY, Europe/Istanbul, tarih biçimi, hafta başı Pazartesi." Neden: tarih biçimi ve hafta başı upstream'de zaten doğru, TRY hesap planıyla geliyor; eksikler listelendi; kalıcı ad testi eklendi.
  - T3.3. Eski metin: "Sağlama algoritması (python-stdnum, Odoo'nun mevcut bağımlılığı). / Gerçek kişi / tüzel kişi ayrımı; e-Belge için mükellef türü." Neden: sağlama çekirdekte zaten var; görev kişi/şirket ayrımı, MERSİS ve Türkçe etikete daraldı.
  - T3.4'e il/posta kodu zorunluluğu, T5.8'e terim düzeltmesi, T7.1'e hesap ön ayarı (153/621) eklendi.
  - §4 tablosu: vergi dairesi "T3.1'de doğrulanır" → doğrulandı; VKN/TCKN satırı. §11'e araştırma belgesi.
- `docs/research/e-fatura.md` (vergi dairesi notu doğrulandı), `docs/MODULE_MATRIX.md` (`ov_l10n_tr` satırı), README, `state.json`.
- T2.7'nin CI sonucu (Linux, run 41589662350): 85 test geçti; MVP adımında 13 test geçti, dış adres yalnız `example.com`. M2 Linux'ta da doğrulandı.

### Adım: dış istek testi (T2.7), marka katmanı (F2) tamam — otonom mesai 3

**Kod**
- `tools/netguard.py` (yeni): bir Python betiğini, yerel ağ dışındaki her ad çözümlemesinin kaydıyla çalıştırır (PEP 578 denetim kancası: `socket.getaddrinfo`, `gethostbyname`). Kitaplıktan bağımsızdır (`requests`, `urllib`, `http.client`, `smtplib`). Yayıncının alan adları (`odoo.com`, `odoocdn.com`, `odoo.sh` ve alt alanları) ayrıca reddedilir; CI yayıncıya hiç bağlanmaz. Kayıtta çağıran kod satırları da var.
- `tools/run_tests.py`: Odoo'yu `netguard.py` ile çalıştırır (veritabanı açma, `ov_brand` ön kurulumu, testler). Günlükten test çatısının engellediği Python isteklerini ve tarayıcı isteklerini de okur. Çıktıda `external requests:` satırı bütün dış adresleri listeler. `ov_brand` kuruluysa yayıncıya giden istek `RESULT: FAILED` verir; değilse (upstream referans çalıştırmaları) yalnız listelenir.
- `ov_brand/tests/external_requests.py` (yeni): test sınıflarına kayıt katmanı (`_request_handler`, `fetch_proxy`) ve `assertNoPublisherRequest`.
- `ov_brand` testleri (`ov_external` etiketi): kayıt düzeneğinin kendisi (örnek bir dış adresle, Python'da ve tarayıcıda); bütün zamanlanmış işler (etkin ya da değil, test işlemi içinde birer kez); ana sayfalar tarayıcıda (giriş, ana ekran, Ayarlar, Uygulamalar; kuruluysa Sohbet ve portal).
- `ov_brand_mail`: Gmail/Outlook hesabının kimlik bilgileri Ayarlar'dan silinmişse erişim belirteci yayıncının vekilinden istenmez. Yerine bilgilerin yeniden girilmesini isteyen bir hata (Türkçe çevirili) verilir. Envanter §4.4'teki uç durum ölçüldü ve gerçekti: upstream yöntemleri yenileme belirtecini `gmail.api.odoo.com` ve `outlook.api.odoo.com`'a gönderiyordu. `google_gmail` ve `microsoft_outlook`, `mail` ile kendiliğinden kurulduğu için `ov_brand_mail`'in bağımlılığı oldu (`auth_totp_mail` emsali). İki test.

**Testler ve ölçüm**
- `ov_brand` + MVP uygulamaları (`ov_test_mvp`, `ov_brand_leak,ov_external`): 13 test, hepsi geçti. 28 zamanlanmış iş çalıştı, hiçbiri hata vermedi; 6 sayfa açıldı. Kurulumda, işlerde, testlerde ve sayfalarda dış ad çözümlemesi yok, yayıncıya 0 istek. Tek dış adres testin kendi örneği (`example.com`).
- Kanıt denetimi: koruyucu Odoo süreci içinde yayıncı adresini reddedip kaydediyor (Odoo kabuğunda denendi). Çalıştırıcının hata yolu örnek kayıtla denendi.
- Sekiz modül birlikte (`ov_test_ci`): 84 test. İlk çalıştırmada portal sayfası (`/my`) web istemcisinin hazır işaretini beklediği için düştü; hazır koşulu sayfa türüne göre ayrıldı. Düzeltmeden sonra 84 testin hepsi geçti.
- `ov_demo` güncellendi; Gmail/Outlook iletisi Türkçe ve İngilizce doğru.

**CI**
- MVP adımı artık `ov_external` etiketli testleri de çalıştırır (adı "Brand leak and external request tests with the MVP apps"). Bütün adımlarda yayıncıya giden istek sonucu bozar.

**Faz**
- F2 bitti (7/7). M2 ölçütleri: sızıntı testi CI'da geçiyor (T2.6), testlerde yayıncıya istek yok (bu adım; CI sonucu bu commit'le), ürün adı tek ayardan (T2.2). Sıradaki faz F3, ilk görev T3.1.

**Belgeler**
- PLAN.md (T2.7 `[x]` ve sonuç; F2 `[x]` 7/7; T2.3'teki uç durum notu; şu anki görev T3.1), ARCHITECTURE.md (araç ağacı, yerel testler, CI, özel testler, Marka satırı), README.md, CLAUDE.md (test komutları), `docs/COMPLIANCE.md` (§odoo.com'a veri gönderimi), `docs/research/brand-inventory.md` (§4.2 düzeltme ve sonuç, §4.4 sonuç, §4 T2.3 satırı, §11), modül README'leri (`ov_brand`, `ov_brand_mail`), state.json (faz F3, modül notları, CI).

### Adım: marka sızıntısı testi ve metinlerde ürün adı (T2.6) — otonom mesai 3

Otonom mesai 3 kullanıcının isteğiyle başladı. Kullanıcıyı gerektiren işler bekletilip mesai sonunda birlikte ele alınacak (kullanıcı, 2026-11-03). İlk iş mesai 2'den yerelde kalan T2.6'nın bitirilmesi.

**Kod**
- Yöntem (PLAN'ın bu görevde seçilmesini istediği "metin düzeyinde değiştirme"): **gösterimde değiştirme** (USER_TASKS K19 varsayımı). Kayıtlı metinler ve çeviri dosyaları değişmez; eski ad, kullanıcıya gösterilirken ürün adıyla değiştirilir. Çekirdeğe dokunulmadı (D-010).
- `ov_brand/rebrand.py` (saf işlevler):
  - Ad kuralı: "Odoo", "OdooBot" → ürün adı. Yayıncının şirket adı, ücretli sürüm, Studio, `Odoo.sh`, `Odoo Online`, posta eklentileri, sürüm numaraları, yollar ve teknik adlar değişmez.
  - Türkçe ekler ürün adına uyar: kaynaştırma harfi ve ünlü uyumu ("Odoo'da" → "Nexus'ta", "Odoo'ya" → "Nexus'a", "OdooBot'u" → "Nexus'u"). Başka adlarla da denendi (Nova, Kelebek, Atlas, ÖRÜM).
  - Örnek adresler `example.com`'a döner. Yayıncının destek masasına yönlendiren cümleler çıkarılır (e-tablo hata mesajları). HTML kaynaklarda yayıncının ana sayfasına giden bağlantı kalkar, metni kalır.
  - Sunucunun kod çevirisi işlevi (`get_translation`) modül yüklenirken sarmalanır. Ürün adı veritabanı başına tutulur, istek iş parçacığının veritabanından okunur.
- `ov_brand`, ortak gösterim noktaları:
  - web istemcisi çevirileri: çevirisi olmayan İngilizce metinler istemciye gitmediği için modülün `.pot` dosyasından eklenir;
  - alan adları, yardım metinleri, seçimler (önbellekli; modül lisans adları değişmez);
  - görünümler ve QWeb şablonları: yalnız metinler ve görünen öznitelikler. İfadeler, betikler ve stiller değişmez; çeviri düzenleme kipinde de değişmez;
  - eylem, grup, uygulama kategorisi ve modül kayıtlarının metinleri okunurken.
  - Ürün adı (`ov_brand.name`) değişince şablon ve alan önbellekleri temizlenir.
  - Erişim hakları formundaki yayıncı belge sitesi bağlantısı kaldırıldı.
- `ov_brand_mail`:
  - e-posta şablonlarının konu ve gövdesi işlenmeden önce; e-posta yazma penceresinin işlemeden kopyaladığı metinler (toplu e-posta);
  - botun e-posta adresi `bot@example.com` (upstream `odoobot@example.com`). Botun karşılama mesajları kod çevirisi yoluyla değişti;
  - güvenlik uyarısı e-postasındaki iki adımlı doğrulama bağlantısı (yayıncının belge sitesi) kaldırıldı, cümle kaldı;
  - e-posta sunucusu ayarının, yayıncının barındırma hizmetini anlatan ipucu kaldırıldı;
  - yazarı olmayan mesajların tarayıcı bildirimi ürünün simgesini taşır.
- `ov_brand_account`: belge düzeni önizlemesindeki QR kodun ortasındaki yayıncı logosu.
- T2.2'den kalan üç JS metni (barkod tarayıcı kamera izni, rapor işçileri uyarısı, güvensiz bağlam uyarısı) web istemcisi çevirileri yoluyla değişti.

**Testler**
- Sızıntı testi (`ov_brand_leak` etiketi; `ov_brand` ve `ov_brand_mail`): kurulu bütün modüllerde İngilizce ve Türkçe olarak sunucu ve istemci çevirileri, alanlar, görünümler, kayıtlar (eylemler, gruplar, kategoriler, modüller, menüler, bot), ana sayfalar (giriş, manifest, çevrimdışı, web istemcisi) ve e-posta şablonları.
- İzin listesi gerekçeleriyle `ov_brand/tests/brand_leak.py`'de (envanter §10): e-tablo formül adları (K13), lisans adları, ücretli sürümün fiyat bağlantıları (yalnız yöneticiler görür), `remove_odoo_enterprise` adı, yer tutucu metin, gösterilmeyen şablonlar, geliştirici araçları, kendi ifadelerimiz.
- Kural testleri: ad, korunan adlar, teknik adlar, örnek adresler, destek cümleleri, HTML bağlantıları, Türkçe ekler, görünüm ağacı; gösterim noktaları ve ürün adı değişikliği.
- Sonuç (yerel): sekiz marka modülü ve `report_xlsx` birlikte 78 test, hepsi geçti (`ov_brand` 51, `ov_brand_mail` 11). `ov_brand` + MVP uygulamaları (`sale_management`, `purchase`, `stock`, `crm`, `mrp`, `mrp_subcontracting`, `maintenance`, `contacts`, `calendar`, `l10n_tr`) veritabanında 7 sızıntı testi geçti.
- İlk taramanın bulduğu ve düzeltilenler: e-posta sunucusu ipucu, davet e-postasındaki yayıncı bağlantısı ve örnek adres (`yourcompany.odoo.com`), e-tablo destek cümleleri, `from_filter` yardımındaki örnek alan adı. 20.0 API farkları da düzeldi: `file_open` kodlama almıyor, önbellek temizliği `env.transaction.invalidate_ormcache` ile.
- `ov_demo` güncellendi. Türkçe ölçüm: web istemcisi mesajlarında, menülerde ve eylem yardım metinlerinde 0 sızıntı; kayıtlı 15 eylem yardım metni bilerek upstream haliyle duruyor.

**CI**
- Modül testlerinden sonra yeni adım: `ov_brand` ve MVP uygulamaları (`MVP_APPS`) ayrı bir veritabanına kurulur, yalnız sızıntı testleri çalışır (M2 ölçütü).

**Kararlar (USER_TASKS)**
- K19 (yeni, varsayım A): gösterimde değiştirme. Aynı maddede botun e-posta adresi ve destek cümleleri.
- K13: "Ne zaman" T8.2; T2.6'da varsayımla izin listesine yazıldı.

**Belgeler**
- PLAN.md (T2.6 `[x]`, sonuç; F2 6/7; şu anki görev T2.7), USER_TASKS.md (K19, §1), README.md, ARCHITECTURE.md (Marka satırı, CI), CLAUDE.md (sızıntı testi komutu), `docs/research/brand-inventory.md` (Sonuç, §3, §6, §7, §8, §9, §10, §11), `docs/research/pdf-engine.md` (T2.6 satırı), state.json (mesai 3, modül notları, ortam).

## 2026-10-19

### Otonom mesai 2 — özet

Mesai, T2.6 sürerken özeti yazılmadan kapandı (oturum bağlam sınırına ulaştı, ardından ara verildi). Özet, otonom mesai 3'ün başında yazıldı (2026-11-03).

**Biten görevler (4):** T2.2 marka modülü `ov_brand` (mesai 1'den süren), T2.3 odoo.com bağlantılarının kesilmesi, T2.4 web istemcisi `/app` yolunda, T2.5 e-posta, rapor ve portal altbilgileri.

**Kullanıcının isteğiyle:** kalıcı ad Nexus (K3) ve commit oturum satırı kararı (K11) kaydedildi; eski commit'lerdeki oturum bağlantısı satırları silindi (geçmiş yeniden yazıldı, tek force-push; K10'un kalan kısmı bekliyor).

**Süren görev:** T2.6 marka sızıntısı testi. Kod yerelde kaldı; mesai 3'te bitti (yukarıda).

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** K15 çevrim içi hizmet modülleri, K16 `/app` yolu, K17 "Powered by" satırı, K18 PDF motoru. Hepsi geri dönüşü kolay varsayımlarla ilerledi. K14 marka adına göre güncellendi.

**Onay bekleyen dışa dönük iş:** K10 (ilk iki commit'teki ortak yazar satırı, force-push gerekir), K9 (GitHub güvenlik özellikleri).

**Yerelde kalanlar:** T2.6 kodu (commit edilmedi), geçici veritabanları `ov_brand_scan` ve `ov_test_ov_brand`. PostgreSQL bilgisayar yeniden başlayınca durdu; mesai 3'te başlatıldı.

### Adım: e-posta, rapor ve portal altbilgileri, bot, PDF motoru önerisi (T2.5) — otonom mesai 2

**Kod**
- Yöntem: OCA `mail_debranding`, `portal_debranding`, `sale_portal_debranding` (19.0) yerine kendi şablon kalıtımlarımız. 20.0 portu gerekirdi; kapsadıkları yüzeyler bizim envanterimizin (§6) bir parçası.
- "Powered by" satırları kaldırıldı, yerine ürün adı yazılmadı (USER_TASKS K17 varsayımı).
- `ov_brand`:
  - PDF başlığı (`web.report_layout`, `web.report_preview_layout`) marka adı.
  - Sunucunun yazdığı PDF dosyalarında (bölünen, birleştirilen, PDF/A) `Creator` ve `Producer` marka adı. Upstream bunları çekirdek yazıcı sınıfında sabit yazıyor; sınıfın yazma yöntemi modül yüklenirken değiştirildi, ad rapor başına bağlam değişkeninden geliyor.
- `ov_brand_mail`:
  - Bildirim e-postalarının iki düzeninde "Powered by" satırı yok; takibi bırakma bağlantısı kalır.
  - E-postalara gömülü yayıncı logosu (ör. e-Fatura bildirim şablonu) işlenen metinden süzülür.
  - Herkese açık sohbet sayfasının başlığı ve simgesi.
  - Bot (`base.partner_root`, upstream'de "OdooBot") marka adını ve simgesini taşır; `ov_brand.name` değişince eşitlenir. Bot sohbetlerde ve kayıt geçmişinde görünür; bu yüzden `mail`'e bağlı modülde.
- Yeni modüller (AGPL-3, ilgili uygulamayla kendiliğinden kurulur):
  - `ov_brand_portal`: belge kenar çubuğundaki "Powered by" ve logo; güvenlik sayfasındaki iki belge bağlantısı (iki adımlı doğrulama, API anahtarları).
  - `ov_brand_digest`: özet e-postasında "Sent by" ve "Powered by" satırları, mobil uygulama tanıtımı (görselleri yayıncının sunucusunda), ipuçları (yayıncının içeriği, görselleri yayıncının sunucusunda). Varsayılan özetin adı "Your Periodic Digest"; kurulumda bu kaydın eski çevirileri silinir, yoksa upstream'in "Odoo Periyodik Özetiniz" çevirisi bizimkinin önüne geçiyor (çeviri yükleyicisi var olan çeviriyi değiştirmiyor).
  - `ov_brand_account`: fatura PDF'indeki QR kodların ortasındaki yayıncı logosu; şartlar ve koşullar örneğindeki yayıncı adı geçen cümle.
  - `ov_brand_purchase`: tedarikçi portalındaki "Want to import this document in Odoo?" / "Start on Odoo" tanıtımı; yerinde belgeyi UBL olarak indirme adresi kalır.
- Testler: `ov_brand` 30, `ov_brand_mail` 6, `ov_brand_portal` 2, `ov_brand_digest` 3, `ov_brand_account` 3, `ov_brand_purchase` 1 test yöntemi. Sekiz marka modülü birlikte 51 test, hepsi geçti.
- Çeviriler: yeni metinlerin Türkçesi (`i18n/tr.po`).
- `ov_demo`: `ov_brand_portal`, `ov_brand_digest`, `ov_brand_account` kuruldu; `ov_brand`, `ov_brand_mail` güncellendi. Özetin Türkçe adı "Periyodik Özetiniz", botun adı Nexus.

**Araştırma**
- PDF motoru (`docs/research/pdf-engine.md`): wkhtmltopdf upstream'in varsayılanı ama arşivde; Paper Muncher etkin ama kendi tanımıyla erken alfa, yalnız amd64 Linux. Öneri üretimde wkhtmltopdf, Paper Muncher CI'da ikinci motor (USER_TASKS K18). Yeni risk R18.

**Kararlar (USER_TASKS)**
- K17 (yeni, varsayım A): "Powered by" satırı yok.
- K18 (yeni, varsayım A): PDF motoru önerisi.

**Belgeler**
- PLAN.md (T2.5 `[x]`, sonuç; T2.6, T3.7, T8.4 notları; R18; F2 5/7; şu anki görev T2.6), USER_TASKS.md (K17, K18), ARCHITECTURE.md (Marka satırı, PDF motoru), CLAUDE.md (PDF motoru notları), `docs/MODULE_MATRIX.md`, `docs/research/brand-inventory.md` (Sonuç, §6, §9, §11), yeni `docs/research/pdf-engine.md`, README.md, state.json.

### Adım: web istemcisi `/app` yolunda (T2.4) — otonom mesai 2

**Kod (`ov_brand`)**
- Yol `/app` (`tools.WEB_PATH`; USER_TASKS K16 varsayımı). Çekirdeğe dokunmadan, yalnız modülle (D-010).
- Sunucu:
  - `Home.web_client` override: `/app` ve `/app/...` web istemcisini sunar; `/odoo` ve `/odoo/...` sorgusuyla birlikte `/app`'e yönlendirilir (303). Sunucunun `/odoo` ile ürettiği bağlantılar (e-posta, bildirim, giriş sonrası) böylece çalışır.
  - Giriş: sonrası `/app`'e gider; `redirect=/app/...` adresli giriş sayfasının bağlantı önizlemesi eylemin adını gösterir (upstream bunu yalnız `/odoo` için yapıyordu).
  - Tarayıcıdan kurulan uygulama: kapsam, başlangıç adresi, kısayollar ve paylaşım hedefi `/app`. Service worker `/app` kapsamında; betikteki yollar (`web` ve `mail` parçaları) `/app`. Çevrimdışı sayfa iki yolda da.
- JS (`static/src/webclient/web_path.js`):
  - `router.stateToUrl` ve `router.urlToState` yamalı; yönlendiricinin iç durumu `/odoo` ile çalışmaya devam ediyor. Yönlendirici modül yüklenirken adresi okuduğu için yamadan sonra yeniden başlatılıyor.
  - Upstream'in iç bağlantı dinleyicisi yalnız `/odoo` sayfalarında çalışıyor; `/app` için aynısı eklendi, `/odoo` bağlantıları da sayfa yenilenmeden açılıyor.
  - Service worker kaydı `/app` kapsamıyla; menü ve ilişki alanı bağlantıları `/app` gösteriyor.
- `ov_brand_html_editor`: düzenleyiciye yapıştırılan `/app/...` kayıt bağlantılarının önizlemesi (upstream yalnız `/odoo`'yu tanıyordu).
- Testler: yeni `test_web_path.py` (yönlendirme, giriş, önizleme, manifest, service worker; tarayıcıda yönlendirici, menü bağlantıları ve sayfa yenilemeden iç bağlantı). Eski testler `/app` ile. `ov_brand` 27, `ov_brand_html_editor` 3 test; dört modül birlikte 35 test, hepsi geçti.
- Windows'ta bir tam çalıştırmada `test_settings_documentation_links` "Session Expired" ile düştü, tekrarında geçti.
  - Neden upstream'in oturum deposu: service worker kurulurken ana sayfayı ister, o istek oturum dosyasını yeniden yazar. Windows'ta değiştirilmekte olan dosyayı aynı anda okuyan istek `PermissionError` alır ve boş oturumla devam eder.
  - Ölçüm: 3 saniyede 17 044 okumanın 1 617'si hata verdi. Linux'ta dosya değişimi atomik; CI etkilenmez. CLAUDE.md'ye not eklendi.
- Bilinen sınırlar (envanter §5): upstream'in diğer JS bağlantıları `/odoo` ile; fareyle üzerine gelince görünebilir, tıklanınca yönlendirme ya da yeni dinleyiciyle `/app`'e varır. Veritabanı yükleme hatasındaki `?db=` temizliği yalnız `/odoo` için. Web sitesi düzenleyicisi `/odoo` varsayıyor (MVP dışı). Upstream'in `/odoo` bekleyen testleri `ov_brand` kuruluyken düşer; kendi testlerimiz etkilenmiyor.

**Belgeler**
- PLAN.md (T2.4 `[x]`, sonuç; F2 4/7; şu anki görev T2.5), USER_TASKS.md (K16), `docs/research/brand-inventory.md` §5 ve §11, README.md, CLAUDE.md (Windows test notu), state.json.

### Adım: dokümantasyon bağlantıları, metin düzenleyici ve uygulama mağazası (T2.3 bitti) — otonom mesai 2

**Kod**
- `ov_brand`:
  - Ayarlardaki odoo.com dokümantasyon bağlantıları ("?") gizli: `DocumentationLink` bileşenine JS `patch()`, bağlantı yayıncının sitesine gidiyorsa çizilmez. Hakkında bölümündeki telif satırının bağlantısı kalıyor (D-007).
  - Uygulama mağazası: `base_import_module` bağımlılık oldu (zaten `web` ile kendiliğinden kuruluyordu). Sektör modüllerinin listesi ve kategorileri boş döner, indirme hata verir; mağazaya hiç istek gitmez. Uygulamalar ekranındaki "Sektörler" süzgeci kaldırıldı, "Tema Mağazası" ve "Üçüncü Taraf Uygulamaları" menüleri pasif.
  - Yeni testler: ayarlarda yayıncıya giden dokümantasyon bağlantısı yok (tarayıcıda), mağaza çağrılmıyor, süzgeç ve menüler gizli. `test_webclient_js` sabit bir eylemi açıyor: `mail` kuruluyken varsayılan uygulama (Discuss) başlığa sohbet adını yazabiliyor, bir kez "OdooBot" görüldü (T2.5). `ov_brand` 20 test.
- Yeni modül `ov_brand_html_editor` (AGPL-3; `ov_brand`, `html_editor`; kendiliğinden kurulur):
  - Düzenleyicide "Google Translate ile çevir" eklentisi yok (sohbet penceresindeki düzenleyici dahil).
  - Görsel ekleme penceresi yayıncının çizim kitaplığını aramıyor, "Çizimler" süzgeci gizli.
  - Sunucu uçları (`generate_text`, `google_translate`, `save_library_media`) ağa çıkmadan hata döner; `media_library_search` boş sonuç verir. Bu hizmetler düzenlenen metni veya arama sözcüklerini veritabanı kimliğiyle gönderiyordu.
  - 2 test (biri tarayıcıda), Türkçe çeviri, `README.rst`.
- Bulgular, kod gerekmedi:
  - Gmail/Outlook OAuth vekili: Community'de ilk bağlantı sürüm denetimiyle engelli, vekil fiilen kapalı. Uç durum: kendi istemci kimliğiyle bağlandıktan sonra kimlik ve gizli anahtar silinirse belirteç yenileme vekile gidiyor. T2.7'nin dış istek testine eklendi (envanter §4.4).
  - `mail`'deki dış istekler yayıncıya gitmiyor: görüntülü görüşme sunucusu (SFU) ve Twilio yalnız kullanıcı ayarlarsa, bağlantı önizlemesi mesajdaki adrese. Görüşmeler varsayılan olarak Google'ın STUN sunucularını kullanıyor (tarayıcıdan, IP adresi görünür); KVKK notu olarak COMPLIANCE.md'ye yazıldı.
  - OCA `disable_odoo_online` 20.0 portu (PR #124) hâlâ birleşmemiş; kendi modüllerimiz aynı işi yapıyor, kullanılmıyor.
- Testler: `ov_brand`, `ov_brand_mail`, `ov_brand_html_editor`, `remove_odoo_enterprise` birlikte 27 test, hepsi geçti.

**Belgeler**
- PLAN.md: T2.3 `[x]`, sonuç; F2 3/7; şu anki görev T2.4. T2.7 ve T8.7'ye not.
- `docs/research/brand-inventory.md` (§4 sonuç, yeni §4.4, §9, §11), COMPLIANCE.md (KVKK), ARCHITECTURE.md (marka katmanı), README.md, state.json.

### Adım: Enterprise reklamları kaldırıldı — OCA `remove_odoo_enterprise` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- OCA `server-brand` deposu 20.0 dalıyla `vendor/oca/server-brand` altına sığ git submodule olarak eklendi (commit `9637fe38`, 2026-10-07). 20.0 dalında yalnız `remove_odoo_enterprise` var.
- `remove_odoo_enterprise` (AGPL-3; `base_setup`) `ov_brand`'in bağımlılığı oldu, marka modülüyle her zaman kurulu.
  - Ayarlar ekranında yalnız Enterprise'da olan özellikler (`upgrade_boolean`) ve boşalan bloklar gizleniyor.
  - Uygulamalar listesindeki satın alınacak uygulamalar (`to_buy`) ve ödeme sağlayıcıları aramada dönmüyor. Envanter §4'teki "ayrı `to_buy` filtresi" önerisine gerek kalmadı: OCA'nın 20.0 sürümü bunu da yapıyor.
- Yeni test: satın alınacak uygulamalar veritabanında duruyor ama listelenmiyor (`ov_brand` 17 test). `README.rst`.
- `tools/run_tests.py`: `ov_brand` önce kurulunca onunla gelen hedef modüller (ör. `remove_odoo_enterprise`) ikinci çalıştırmada güncellenir (`-i` ve `-u` birlikte), testleri de çalışır. Önceki sürümde bunların testleri atlanıyordu. Birlikte çalıştırma: 22/22 (`ov_brand` 17, `ov_brand_mail` 2, `remove_odoo_enterprise` 3).
- `ov_brand`'in tarayıcı testi sabit bir eylemi açıyor (Kullanıcılar). `mail` kuruluyken açılış uygulaması Discuss sekme başlığına "OdooBot" yazabiliyor; yerelde bir kez testi düşürdü. Gerçek bir marka izi: envanter §3'teki OdooBot satırına eklendi, T2.5'te.
- Not: modülün Uygulamalar ekranındaki adı "Remove Odoo Enterprise". Telif ve yazar bilgisi olduğu için değiştirilmedi; Uygulamalar menüsü son kullanıcıdan T7.3'te gizlenir, T2.6'nın izin listesinde ele alınır.

**Belgeler**
- docs/COMPLIANCE.md §5 (lisans envanteri), state.json (`modules.vendored`, ortam), ARCHITECTURE.md (durum notu, depo yerleşimi), CLAUDE.md (ortam), PLAN.md (T2.3 ara durum), `docs/research/brand-inventory.md` (§3 OdooBot, §4 sonuç, §9).

### Adım: eski commit'lerden oturum bağlantısı satırları silindi (K10) — otonom mesai 2

**Kullanıcının isteği:** "önceki commitlerden claude oturum linklerini sil."

**Yapılan**
- 21 commit'in 17'sindeki `Claude-Session:` satırı silindi. Satırın önünde kalan boş satır da gitti; mesajların geri kalanı aynı.
- Yöntem: depo geçici klasöre klonlandı, `git filter-branch --msg-filter` ile yalnız mesajlar yeniden yazıldı. `main` `--force-with-lease` ile bir kez force-push edildi (`ca350bb` → `e4a98f7`).
- Denetim: son commit'in dosya ağacı yeniden yazmadan önceyle aynı (`e6f9387`), commit sayısı aynı, yazar, işleyen ve tarihler aynı.
- Yerel depo yeni geçmişe `git reset --soft` ile taşındı. Ağaçlar aynı olduğu için çalışma alanı değişmedi; yarım kalan T2.3 işi korundu.
- Kalan: ilk iki commit'teki `Co-Authored-By: Claude` satırı. İstek yalnız oturum bağlantılarıydı; bu satırlar K10'da ayrı soru olarak duruyor.
- Bilinen sınır: GitHub eski commit'leri kimlikleriyle bir süre daha açabilir, eski CI çalıştırmaları eski kimlikleri gösterir. Tamamen silinmeleri için GitHub desteğine başvurmak gerekir.

**Commit kimlikleri (eski → yeni)**

| Eski | Yeni |
|---|---|
| `ca350bb` | `e4a98f7` |
| `2a6b523` | `67a61ba` |
| `c48b98f` | `1dd6aaf` |
| `1495616` | `ec14669` |
| `b4380e5` | `1bac273` |
| `a49a92c` | `9e90991` |
| `c2dbc6c` | `9fee384` |
| `1e2960f` | `6a2fc36` |
| `c6b11ba` | `6309fd5` |
| `185e4b4` | `1b94f2a` |
| `2a3a8ef` | `6df7425` |
| `b0019a5` | `95f94a8` |
| `c6d154f` | `6347bda` |
| `a253ed4` | `3f1d555` |
| `b4f2ea6` | `05c4fa2` |
| `d5d0cd6` | `3f2edda` |
| `a170482` | `a8f6bd2` |
| `811f913` | `45bda8d` |
| `409a403` | `f33fe70` |
| `24f56b3` | `363a288` |
| `cf37443` | `b267933` |

**Belgeler**
- Belgelerde geçen eski kimlikler güncellendi: USER_TASKS.md K10 (`cf37443`, `24f56b3`), bu dosyadaki ilk CI çalıştırması notu (`c6b11ba`).
- DECISIONS.md D-015 (force-push istisnası, eski commit'ler), USER_TASKS.md (K10 yalnız ortak yazar satırına indi; K11 notu).

### Adım: çevrim içi hizmet modülleri kaldırıldı — IAP ve `mysubscription` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- `ov_brand` yayıncının çevrim içi hizmet modüllerini (`iap`, `mysubscription`) onlara bağlı modüllerle birlikte kaldırıyor.
  - Neden kaldırma: ikisi de `auto_install` (`web` + `base_setup`, `base` + `web`); her yeni veritabanına kuruluyorlar, modül bağımlılığıyla engellenemiyorlar. MVP modüllerinden hiçbiri bunlara zorunlu bağımlı değil.
  - Yöntem: her kurulum ve güncellemenin sonunda (`ir.model.data._process_end`; Odoo'nun kaldırılacak modülleri kaldırmadan hemen önceki adımı) kurulu olanlar kaldırılmak üzere işaretlenir. Komut satırından kurulanlar da böylece geri alınır. `post_init_hook` kullanılmadı: aynı çalıştırmada kurulan modüller yükleme sonunda yeniden "kurulu" işaretleniyor.
  - IAP hesap kayıtları kaldırmadan önce silinir. Yoksa upstream'in kaldırma adımı, hizmet kayıtlarını silemediğini (kısıtlı yabancı anahtar) ERROR olarak günlüğe yazıyor; tablolar yine de siliniyor.
  - Arayüzden kurulum (`button_install`) bu modülleri getirecekse hata verir.
  - Ayarlar ekranında bu modülleri kuracak kutular (`module_sms`, `module_partner_autocomplete`, CRM'deki aday zenginleştirme ve üretme vb.) görünümden çıkarılır; boşalan blok da kalkar.
  - MVP deneme veritabanında (`ov_brand_scan`) kaldırılan 12 modül: `iap`, `iap_mail`, `iap_crm`, `sms`, `calendar_sms`, `crm_sms`, `sale_sms`, `stock_sms`, `partner_autocomplete`, `crm_iap_enrich`, `crm_iap_mine`, `mysubscription`. Kurulu modül sayısı 87.
  - 4 yeni test (`ov_brand` 16/16, `ov_brand_mail` 2/2). `i18n/tr.po`, `README.rst`.
- `tools/run_tests.py`: hedef modüller `ov_brand`'e bağlıysa `ov_brand` önce testsiz kurulur, testler ikinci çalıştırmada. Neden: modül kaldıran bir çalıştırmada Odoo kayıt defterini yeniden yükler ve `post_install` testlerini hiç başlatmaz.
- Yerel `ov_demo` veritabanına `ov_brand` kuruldu (`ov_brand_mail` kendiliğinden geldi); CLAUDE.md'deki demo komutu güncellendi.

**Karar**
- USER_TASKS K15 (otonom varsayım, geri dönüşü kolay): gizlemek yerine kaldırmak. PLAN T2.3'teki "kapatılır veya gizlenir" ve `mysubscription` için "menü öğesi gizlenir" önerileri bu varsayımla değişti. Envanter §4.3'teki öneri (JS ile menü öğesini kaldırmak) da uygulanmadı.

**Belgeler**
- PLAN.md (T2.3 maddeleri ve ara durum), USER_TASKS.md (K15), docs/COMPLIANCE.md (KVKK), `docs/research/brand-inventory.md` (Sonuç, §4, §4.3), ARCHITECTURE.md (demo veritabanı, test aracı), CLAUDE.md (demo komutu, test aracı), README.md, state.json.

### Adım: yayıncı garantisi kapatıldı — `ov_brand_mail` (T2.3, sürüyor) — otonom mesai 2

**Kod**
- Yeni modül `addons/ov_brand_mail` (AGPL-3; `ov_brand`, `mail`). `auto_install`: `mail` kurulu her veritabanına kendiliğinden kurulur.
  - `publisher_warranty.contract._get_sys_logs` ağa çıkmadan boş yanıt döndürür. Rapor (veritabanı kimliği, kullanıcı sayıları, kurulu uygulamalar, şirketin adı, e-postası ve telefonu) hiç gönderilmez. Kurulumda raporu çağıran `l10n_fr_account` ve `l10n_fr_pos_cert` de bu yoldan geçer.
  - `mail.ir_cron_module_update_notification` pasif. `mail`'in kaydı `noupdate`; `mail` güncellenince yeniden açılmaz.
  - 2 test: rapor isteği hiç yapılmıyor (`requests.post` çağrılmıyor), iş pasif. `i18n/tr.po`, `README.rst`.
- OCA `disable_odoo_online` yerine kendi override'ımız: 20.0 portu (PR #124) hâlâ açık; işimiz tek yöntem (envanter §9 önerisi).

**Belgeler**
- PLAN.md (T2.3 `[~]`, ara durum), state.json (`modules.ours`), docs/COMPLIANCE.md (KVKK: yayıncı garantisi kapalı), `docs/research/brand-inventory.md` §4.1 (sonuç), ARCHITECTURE.md (modül listesi state.json'a bağlandı), README.md.

### Adım: Marka modülü `ov_brand` (T2.2) — otonom mesai 2

**Kod**
- `addons/ov_brand` tamamlandı ve depoya girdi (otonom mesai 1'deki ara durumun devamı).
  - Varsayılan ürün adı `OV ERP` yerine **Nexus** (K3). Simge mavi kare üstünde beyaz "N" (K14 varsayımı, renk `#1f5f8b`).
  - Tarayıcıdan tek uygulama olarak kurulumun manifesti (`/web/manifest.scoped_app_manifest`): Odoo'nun sabit rengi `#714B67` yerine marka rengi. Uygulamanın kendi simgesi yoksa marka simgesi.
  - `test_login_page_js` düzeltildi: yalnız yüklenemeyen modüllere ve `@ov_brand/` modüllerine bakıyor. Upstream'in test turları tembel yüklenen pakette bekleyebilir; bu hata değil.
  - `i18n/tr.po` (19 metin) ve `README.rst` (Türkçe: neleri değiştirir, ayarlar, bilinen sınırlar).
  - Testler: 12/12, ikisi tarayıcıda. Günlükteki tek CRITICAL satırı upstream gürültüsü: test kipinde websocket kapalı, Chrome kapanırken bu isteğin bağlantısı kopuyor.
- Lint çelişkisi: ruff (upstream kural seti, TID252) aynı modülden içe aktarmaların mutlak, pylint-odoo (`odoo-addons-relative-import`) göreli olmasını istiyor.
  - Upstream'in kuralı uygulandı: içe aktarmalar mutlak (`from odoo.addons.ov_brand.tools import …`).
  - pylint denetimi `.pre-commit-config.yaml`'daki kanca argümanıyla kapatıldı. `.pylintrc`'de `disable=all` + `enable=odoolint` sonrasında tek bir mesaj kapatılamıyor; `.pylintrc`'ye açıklama notu eklendi.
- Kalanlar T2.6'ya taşındı: barkod tarayıcının kamera izni mesajı ("Odoo needs your authorization first."), rapor işçileri uyarısı, güvensiz bağlam konsol uyarısı. Üçü de upstream yöntemlerinin gövdesinde çevrilebilir metin.

**Araştırma**
- Envanterdeki öneri değişti (`docs/research/brand-inventory.md` §11).
  - Eski metin: "`web.web_app_name` de bu değerle eşitlenir."
  - Yeni: eşitlenmiyor. Genel Ayarlar'daki uygulama adı yalnız tarayıcıdan kurulan uygulamanın adıdır; boşsa marka adı kullanılır.
  - Neden: iki ayarı eşitlemek, müşterinin kendi uygulama adını ürün adının üstüne yazmasına yol açar. Marka adının tek kaynağı `ov_brand.name` kalır (M2 kabul ölçütü).

**Ortam**
- Geçici veritabanı `ov_brand_scan` T2.3 denemeleri için tutuluyor. Otonom mesai 1 özetinde "T2.2 bitince silinir" yazıyordu; mesai sonunda silinecek.

**Belgeler**
- PLAN.md (T2.2 tamam; T2.6'ya kalan metinler), state.json (`modules.ours`, lint notu), CLAUDE.md (lint komutu, içe aktarma notu), ARCHITECTURE.md (durum notu, depo yerleşimi, lint), README.md, `docs/research/brand-inventory.md` (§3, §11).

### Adım: kararlar — kalıcı ürün adı Nexus (K3) ve commit oturum satırı (K11)

**Kararlar**
- K3 / D-014: kullanıcı kalıcı ürün adını seçti: **Nexus**. D-014 yerinde yeniden yazıldı (başlık "Ürün adı, çalışma adı ve teknik modül öneki").
  - Eski metin: "**Çalışma adı:** `odoo-version`. Geçicidir, MVP sonunda kalıcı adla değişecek. GitHub deposunun adı da budur." · "Yeniden değerlendirme: T8.1 (kalıcı ad ve yeniden adlandırma)."
  - Yeni: ürün adı Nexus; çalışma adı yalnız depo adında ve geliştirme ortamında kalır; yeniden değerlendirme T8.2 (tescil araştırması, depo yeniden adlandırması). Modül öneki `ov_` değişmedi.
  - Neden: kullanıcı kararı. Kalıcı ad T8.1'deki MVP sonu değerlendirmesinden öne alındı.
  - Not: "Nexus" yaygın bir sözcük; tescil çakışması riski PLAN'a R17 olarak eklendi. TÜRKPATENT sorgusu ve alan adı kontrolü dış demodan önce (T8.2).
- K11 / D-015: commit mesajlarındaki `Claude-Session:` satırı kaldırıldı. Kural CLAUDE.md kural 8'e ve D-015'e eklendi.
  - Eski hali: "Varsayılan: satır kalır" (USER_TASKS K11).
  - Eski commit'lerdeki satırlar geçmiş yeniden yazılmadan silinemez; K10'un B seçeneği bunları da kapsayacak biçimde genişletildi.
- K14: geçici ad varsayımı (`OV ERP`) kalktı; madde yalnız renk ve simgeyi kapsıyor. Simge "N" harfine çevrilecek (T2.2).
- K12: C seçeneği artık marka adı `Nexus`; Claude önerisi C. Karar kullanıcıda.

**Belgeler**
- DECISIONS.md (D-014, D-015), CLAUDE.md (proje özeti, kural 2 ve 8, protokol, komutlar), PLAN.md (§2.1, M2 kabulü, kapı ölçütü 6, T8.1, T8.2, R17), USER_TASKS.md (§1, K3, K10, K11, K12, K14, T8.1, T8.2), README.md (başlık ve ad notu), docs/COMPLIANCE.md §3, state.json.

## 2026-10-18

### Otonom mesai 1 — özet

Kullanıcının isteğiyle T2.2'nin ortasında bitirildi.

**Biten görevler (11):** T1.3 PostgreSQL, T1.2 sürüm doğrulaması (Odoo 20.0 kesinleşti), T1.4 upstream submodule, T1.5 Python ortamı, T1.6 yerel Odoo ve Türkçe demo veritabanı, T1.7 Odoo AI rehberleri, T1.8 test çalıştırıcısı, T1.9 modül şablonu ve lint, T1.10 GitHub Actions CI, T1.11 `vendor/` ve `ports/` düzeni (ilk OCA portu `report_xlsx`), T2.1 marka izleri envanteri. F1 tamamlandı.

**Süren görev:** T2.2 `ov_brand`. Kod yerelde, commit edilmedi (aşağıdaki adım). Sonraki mesaide kaldığı yerden sürer.

**Atlanan görev:** yok. K ve B görevlerine kurala göre dokunulmadı (D-021).

**Kullanıcıya yeni sorular (USER_TASKS.md):** K12 modül yazar adı, K13 e-tablo `ODOO.` öneki, K14 geçici ürün adı ve görünümü. Hepsi geri dönüşü kolay varsayımlarla ilerledi. Mesai öncesinden bekleyenler: K10 (eski iki commit'teki ortak yazar satırı), K11 (oturum bağlantısı satırı).

**Onay bekleyen dışa dönük iş:** yeni yok. K9 (GitHub güvenlik özellikleri) bekliyor.

**Yerelde kalanlar:**
- `addons/ov_brand/` (commit edilmedi).
- Geçici veritabanları `ov_brand_scan` (T2.1 taraması, T2.2 denemeleri) ve `ov_test_ov_brand` (test çalıştırıcısı her seferinde yeniden kurar). Yalnız yerelde; T2.2 bitince `ov_brand_scan` silinir.
- PostgreSQL sunucusu durduruldu. Yeniden başlatmak için: `python tools/pg.py start`.

**CI:** T2.1 commit'inin çalıştırması (39152359525) başarılı.

### Adım: Marka modülü `ov_brand` (T2.2, sürüyor) — otonom mesai 1

**Kod** (yerelde, commit edilmedi)
- `addons/ov_brand` (`web`, `base_setup`): marka adı `ov_brand.name` sistem parametresinden (varsayılan `OV ERP`, K14). Oturum bilgisine (`ov_brand_name`) ve QWeb şablonlarına veriliyor.
  - Sunucu şablonları: sekme başlığı, favicon, giriş ekranı altbilgisi, bağlantı önizlemesi etiketleri (Odoo sloganı ve @Odoo kaldırıldı, görsel bizim simge), iOS simgesi ve tema rengi, çevrimdışı sayfa (metin, düğme rengi).
  - PWA manifesti: ad (Genel Ayarlar'daki uygulama adı hâlâ önce gelir), renk, simgeler.
  - JS `patch()`: pencere varsayılan başlığı, hata pencereleri ("Odoo Hatası" → "Hata" vb.), oturum süresi bildirimi, kullanıcı menüsünde "Yardım" (destek adresi yoksa gizli), Ayarlar "hakkında" alanı (marka adı ve sürüm; Odoo S.A. telif satırı kaldı, yanına AGPL notu).
  - SCSS: `$o-community-color` = `#1f5f8b`. Geçici simgeler (SVG, PNG, ICO) Pillow ile üretildi.
- Testler (`tests/test_ov_brand.py`): 11 test. 10'u geçiyor, iki tarayıcı testi dahil (web istemcisi ve giriş sayfası).
  - Kalan hata kendi testimizde: `test_login_page_js`, modül yükleyicide bekleyen işleri hata sayıyor. Bekleyen tek iş upstream'in test turu (`html_editor`); bu tembel yüklenen pakette normal. Denetim yalnız yüklenemeyen modüllere ve kendi modüllerimize bakacak biçimde düzeltilecek.
  - Kalanlar: `i18n/tr.po`, `README.rst`, lint, belge protokolü, commit.
- `tools/run_tests.py`: Odoo ek dosyaları salt okunur (0o444) yazıyor; Windows'ta bu, test veritabanı yeniden kurulurken silmeyi engelliyordu. Çalıştırıcı artık kurulumdan önce o veritabanının filestore dosyalarını yazılabilir yapıyor. T1.2'deki filestore gc hatalarının nedeni de büyük olasılıkla bu.

**Belgeler**
- PLAN.md: T2.2 `[~]`, ara durum notu. OdooBot T2.5'e taşındı. Veritabanı yöneticisi T2.2 kapsamından çıktı (veritabanı olmadan çalışır; üretimde `list_db = False`).
- `docs/research/brand-inventory.md` §3 ve §8: veritabanı yöneticisi ve OdooBot satırları düzeltildi, bağlantı önizlemesi etiketleri eklendi, `logo.png` yedeğinin ne zaman göründüğü netleşti.
  - Düzeltilen eski metin: "Kendi kurulumlarımız için şablon override `ov_brand`'da". Neden: veritabanı olmadan çalışan rotalar yalnız sunucu genelinde yüklü modülleri görür.
- USER_TASKS.md: K14 (yeni Karar), §1 güncel.

### Adım: Marka izleri envanteri (T2.1) — otonom mesai 1

**Araştırma**
- `docs/research/brand-inventory.md`: kullanıcıya görünen Odoo izleri, odoo.com'a giden çağrılar ve her birinin değiştirme yöntemi, görevleriyle (T2.2–T2.7).
  - Yöntem: upstream kod taraması; `.pot` sayımı; MVP modülleriyle kurulan geçici veritabanında kayıt sayımı ve oturumsuz sayfaların HTTP denetimi.
  - Bütün yüzeyler modülle değiştirilebiliyor (şablon kalıtımı, JS `patch()`, model/controller override, veri kaydı). Çekirdek değişikliği gereken yüzey bulunmadı; `/odoo` yolu T2.4'te.
  - MVP modülleriyle 97 kurulu modül; 40'ında 253 çevrilebilir metin "odoo" içeriyor. Tüm upstream: 168 modülde 542 metin.
  - Yayıncı garantisi (`mail`, haftalık iş varsayılan olarak açık): veritabanı kimliği, kullanıcı sayıları, kurulu uygulamalar, şirket adı, e-postası ve telefonu şifresiz HTTP ile `services.odoo.com`'a gidiyor. Yanıttaki mesajlar çalışan kanalına yazılıyor. T2.3'ün ilk işi; COMPLIANCE KVKK maddesine eklendi.
  - 20.0'da yeni `mysubscription` her veritabanına kendiliğinden kuruluyor ve odoo.com fiyat/hesap sayfalarına bağlanıyor.
  - Müşteriye giden belgelerde: fatura QR kodunun ortasında Odoo logosu, PDF üst verisinde `Creator/Producer: Odoo`, e-posta altbilgilerinde "Powered by Odoo", satın alma portalında tedarikçiye Odoo tanıtımı.
  - OCA `server-brand`: `remove_odoo_enterprise` resmî 20.0 (yalnız ayar ekranları); `disable_odoo_online` 19.0, 20.0 taşıma PR'ı (#124) açık.
  - Odoo test çatısı `requests` ile dış istekleri zaten engelliyor ve günlüğe yazıyor; T2.7 bunun üstüne kurulacak.

**Kararlar**
- K13 (yeni, varsayım, geri dönüşü kolay): e-tablo formüllerindeki `ODOO.` öneki teknik ad sayılır; marka sızıntısı testinin izin listesinde. USER_TASKS.md'de kullanıcı kararına açık.

**Ortam**
- Geçici veritabanı `ov_brand_scan` (tr_TR, TR; MVP modülleri). Yalnız yerelde, T2.2 denemeleri için tutuluyor.

**Doğrulama**
- T1.11 commit'inin CI çalıştırması (39151290971) başarılı: `ov_ci_sample` ve `report_xlsx` testleri Linux'ta geçti; alt modül önbelleği kaydedildi.

**Belgeler**
- PLAN.md (T2.1 tamam, F2 başladı; T2.2, T2.3, T2.5, T2.6, T2.7'ye envanter bulguları), USER_TASKS.md (K13), docs/COMPLIANCE.md (KVKK: yayıncı garantisinin gönderdikleri), ARCHITECTURE.md (marka katmanı satırı), docs/MODULE_MATRIX.md (`server-brand` adayları), README.md, state.json.

### Adım: `vendor/` ve `ports/` düzeni (T1.11) — otonom mesai 1

**Kod**
- `vendor/oca/server-ux`: OCA'nın resmî 20.0 deposu, sığ git submodule, commit `d952d4df` (2026-10-13).
  - İçinde `date_range` (LGPL-3). Mali raporlar ve `mis_builder` buna bağımlı.
  - `git submodule add --depth 1 -b 20.0` dalı bulamadı (sığ klon yalnız varsayılan dalı çekiyor). Yol: önce `git clone --depth 1 --branch 20.0`, sonra `submodule add` ve `absorbgitdirs`.
- `tools/port_oca.py`:
  - `fetch <depo> <modül>`: OCA deposunu geçici klasöre sığ ve seyrek klonlar, modülü `ports/oca/<depo>/<modül>`'e kopyalar. Sürüm `20.0.1.0.0` (OCA taşıma kuralı). `PORT.md`: kaynak depo, dal, commit, lisans, yazarlar. AGPL-3/LGPL-3 dışı lisansta durur. İndirilen dosyalardan hiçbiri çalıştırılmaz.
  - `upgrade <port>`: Odoo'nun `upgrade_code` betikleri (kaynak dalından sonraki sürümler ve Owl 3) yalnız porta. T1.2'deki Windows sorunları araçta çözüldü: yollar `/` ile, UTF-8, yazma yalnız port klasörüne. `ir-access` betiği bağımlılık modüllerini okur, onlara yazılmaz. Sonuç ve uyarı sayısı `PORT.md`'ye.
  - `diff <port> [--stat]`: kaynak commit'le farkın tamamı.
- `ports/oca/reporting-engine/report_xlsx`: ilk port, OCA 19.0 commit `b9e8c6cd` (AGPL-3).
  - `upgrade_code` değişiklik bulmadı (T1.2'deki gibi).
  - Elle uyarlamalar (T1.2'dekiyle aynı): `odoo.http` paket oldu (`content_disposition` → `odoo.http.stream`, `serialize_exception` → `odoo.http.dispatcher`); kaldırılan `ir.actions.report.report_file` alanı demo verisinden, testten ve kullanım örneğinden (README, `readme/USAGE.md`, `index.html`) silindi.
  - JS değişmedi: `download`, `user` ve `ir.actions.report handlers` 20.0'da aynı.
- CI: `.github/actions/upstream` → `.github/actions/submodules`. Bütün alt modüller (upstream + vendor) sığ çekilir. Önbellek anahtarı sabit commit'lerden; biri değişince son önbellek geri yüklenir.
- Lint: `vendor/` ve `ports/` OCA'nın kod biçiminde kalır. Bizim denetimlerimiz yalnız `addons/` (T1.9 ayarı korunuyor).

**Doğrulama**
- `python tools/run_tests.py report_xlsx,date_range`: addons yolunda upstream, `vendor/oca/server-ux` ve `ports/oca/reporting-engine` var. Odoo özeti 23 test, 0 hata; `RESULT: OK`, Windows gc hatası da yok.
- Aracın denemesi `account_financial_report` ile (geçici, depoya girmedi): `t-call` 3, `ir-access` 4, `owl3-migration` 1 dosya; 1 uyarı (`trial_balance.xml`'de `--` içeren yorum). Sonuç T1.2 ölçümüyle aynı. `diff` doğru farkı verdi.
- OCA'da açık taşıma PR'ı var: reporting-engine #1203 (`report_xlsx`, son güncelleme 2026-10-16). Dosyalar karşılaştırıldı: aynı import değişikliği, aynı `report_file` silme, aynı sürüm `20.0.1.0.0`. PR testleri ayrıca `BaseCommon`'a taşımış; zorunlu değil, alınmadı.
- gitleaks (yerel, `dir`): `ports/`, `tools/port_oca.py`, `.github/` temiz.
- Linux referans testi (T1.10 sonrası, elle CI çalıştırması): `l10n_tr` + `account_edi_ubl_cii` 233 test, 4 hata (Enterprise alanına yazan bir test, nedeni incelenmemiş bir içe aktarma testi, PDF motoru olmadığı için 2 test). Windows'taki 27 gc hatası ve `LocalBinaryFile` hatası Linux'ta yok. Ayrıntı `docs/research/nilvera-port.md` §8.

**Belgeler**
- ARCHITECTURE.md (Durum; §2 ağacı ve "OCA port düzeni": port prosedürü, lint ve test düzeni; §5 CI önbelleği), PLAN.md (T1.11, F1 tamam; T2.1'e OCA yazar adı notu), CLAUDE.md (Ortam: OCA; Komutlar: port aracı, yeni klonda alt modüller), README.md, COMPLIANCE.md §5 (server-ux, `report_xlsx`), MODULE_MATRIX.md (ortak bağımlılıklar), `docs/research/nilvera-port.md` (§5.1 sarmalayıcı araç oldu, §8 Linux referansı; PDF motoru görevi T2.5), state.json.

### Adım: CI düzeltmesi — elle çalıştırma ayrı grupta (T1.10 sonrası) — otonom mesai 1

**Kod**
- `.github/workflows/ci.yml`: eşzamanlılık grubu olay türünü de içeriyor (`ci-<dal>-<olay>`). Önceden `main`'de elle başlatılan referans çalıştırması, sonraki bir push ile iptal edilebiliyordu.

**Doğrulama**
- `main`'deki ilk CI çalıştırması (`d35d8ab`; geçmiş yeniden yazılmadan önce 2026-10-19'a kadar `c6b11ba`, 2026-11-03'e kadar `6309fd5`) yeşil: `checks` 1 dk 17 sn, `tests` 1 dk 48 sn. Upstream, pre-commit ve pip önbellekleri `main`'de kaydedildi.

### Adım: GitHub Actions CI (T1.10) — otonom mesai 1

**Kod**
- `.github/workflows/ci.yml`: her push'ta, pull request'te ve elle (`workflow_dispatch`) çalışır. İki iş paralel:
  - `checks`: `check_docs.py` → `pre-commit run --all-files` → gitleaks 8.30.1 ile tüm geçmiş (arşivin SHA-256'sı doğrulanır) → `sync_skills.py --check`.
  - `tests`: Ubuntu 24.04, Python 3.12, PostgreSQL 18 servisi. `.venv` ve `requirements-dev.txt`; `.env` ve `odoo.conf` yerel araçlarla üretilir.
    - Şablondan `ov_ci_sample` üretilir; modül kuralları, ruff ve pylint-odoo'dan geçirilir.
    - `addons/` ve `ports/` altındaki bütün modüller örnekle birlikte tek veritabanında test edilir (`run_tests.py -v`). Hata olursa günlüğün sonu yazdırılır.
    - Elle çalıştırmada `modules` girdisindeki modüller ayrıca test edilir (Linux referans sonucu).
  - Güvenlik: yalnız okuma yetkisi, eylemler commit SHA'sıyla sabit, `persist-credentials: false`, elle girilen modül listesi kabuğa ortam değişkeniyle geçer.
  - Aynı dalda yeni push eski çalıştırmayı iptal eder.
- `.github/actions/upstream/action.yml`: `upstream/odoo` alt modülünü sığ çeker; git nesneleri upstream commit'ine göre önbellekte.
- `tools/check_secrets.py`: staged değişikliklerde `.env` değerlerini arar (en az 8 karakter; host, port, kullanıcı adı hariç). Pre-commit kancası. Mesai başından beri oturum klasöründe kullanılan betiğin depoya alınmış hali; `.env` yoksa (CI) atlar.
- `tools/run_tests.py`: `-v` gerçek hataların traceback'ini yazar.

**Doğrulama**
- İlk çalıştırma (geçici `ci-setup` dalı): iki iş de yeşil. `checks` 1 dk 14 sn, `tests` 2 dk 11 sn.
  - Örnek modül kuruldu, 1 test, `RESULT: OK`. gitleaks: 13 commit, sızıntı yok. Rehber kopyası upstream'le aynı.
- Negatif deneme (geçici `ci-negative` dalı): bilerek başarısız testli `ov_ci_negative` modülü.
  - `tests` kırmızı: `FAIL: TestOvCiNegative.test_module_installed`, `RESULT: FAILED (1)`, traceback günlükte. `checks` yeşil (lint temiz).
  - Commit kancaları atlanmadı; lint hatalı commit yerel kanca tarafından zaten engellenir (T1.9 negatif denemesi).
- `check_secrets.py` negatif denemesi (yerel): `.env` değeri içeren geçici dosya staged iken hata verdi; dosya silindi.
- gitleaks yerelde de çalıştırıldı (Windows sürümü, sağlama doğrulandı): sızıntı yok.
- Önbellek: GitHub önbellekleri dala bağlı; iki geçici dal birbirinin önbelleğini göremedi. `main`'de oluşan önbellek bütün dallarda kullanılır. Önbelleksiz sığ upstream çekimi 20–50 sn.
- Geçici dallar `main`'e tek commit olarak alındı (squash) ve GitHub'dan silindi.

**Belgeler**
- CLAUDE.md (Ortam: CI; Komutlar: gizli bilgi denetimi, CI), ARCHITECTURE.md (§2 ağacı, §5 CI), PLAN.md (T1.10, pano), README.md (CI rozeti, durum), COMPLIANCE.md (gizli bilgi denetimi; §5 gitleaks, GitHub eylemleri, PostgreSQL imajı), state.json.

### Adım: Modül şablonu ve kod kalite araçları (T1.9) — otonom mesai 1

**Kod**
- `tools/new_module.py`: `addons/ov_<ad>/` iskeleti üretir.
  - Manifest: sürüm `20.0.1.0.0`, lisans `AGPL-3` (ya da `--license LGPL-3`), yazar, `security/ir.access.csv`.
  - `README.rst`, boş `models/`, yalnız başlık satırlı `security/ir.access.csv`, `i18n/tr.po` başlığı, kurulumu doğrulayan ilk test (`post_install`).
- `tools/check_modules.py`: proje kuralları, yalnız standart kütüphane.
  - `ov_` öneki; lisans AGPL-3 veya LGPL-3 (D-016); sürüm `20.0.x.y.z`; yazar; `description` anahtarı yok.
  - Manifest adı, özeti ve README'de "Odoo" geçmez (D-007, D-014).
  - `README.rst`, `tests/test_*.py`, `i18n/tr.po` var. OCA portları kapsam dışı (D-019).
- `ruff.toml`: upstream `ruff.toml`'u genişletir. `upstream/`, `vendor/`, `ports/` hariç (portların lint düzeni T1.11'de); `tools/` için `print` serbest.
- `.pylintrc`: pylint-odoo'nun Odoo denetimleri (`disable=all`, `enable=odoolint`). Geçerli sürüm 20.0, izinli lisanslar AGPL-3 ve LGPL-3, zorunlu yazar.
- `.pre-commit-config.yaml`: ruff (v0.16.10), pylint-odoo (v10.0.12, yalnız `addons/`), modül kuralları, belge denetimi. Yerel depoda kanca kuruldu.
- `requirements-dev.txt`: `pylint-odoo==10.0.12`, `pre-commit==4.7.0`.
- `tools/pg.py`: iki `subprocess.run` çağrısına `check=False` (ruff PLW1510).

**Araştırma**
- Modül açıklaması: Odoo 20.0, manifestte `description` yoksa README'yi kullanır ve uzantısına bakmadan reStructuredText olarak işler (`ir_module.py`). Bu yüzden modül README'si `README.rst`; Markdown başlıkları ekranda düz metin görünürdü. pylint-odoo da `description` anahtarını eskimiş sayıyor.
- Manifestte `author` yoksa Odoo uyarı verip boş bırakıyor, `license` yoksa LGPL-3 varsayıyor. Şablonda ikisi de açıkça yazılı.
- T1.6'da not edilen 14 ruff bulgusu depo yapılandırması olmadan, ruff'ın kendi kurallarıyla bulunmuştu. Upstream kural setiyle yalnız ikisi geçerli (`pg.py`, PLW1510); düzeltildi.

**Doğrulama**
- Kabul: `python tools/new_module.py ov_sample` → `python tools/run_tests.py ov_sample`: modül kuruldu, 1 test, `RESULT: OK` (14 sn). Boş `ir.access.csv` sorunsuz yüklendi. `pre-commit run --all-files` temiz.
- `README.rst`, Odoo'nun docutils ayarlarıyla doğru başlık ve paragraf üretiyor; yönerge satırları HTML yorumu olarak kalıyor.
- Negatif denemeler:
  - lisansı `OPL-1`, sürümü `1.0`, yazarı yanlış, adı ve README'si "Odoo" içeren, SQL birleştiren modül: `check_modules.py` 8 sorun; pylint-odoo C8101, C8103, C8105, C8106, C8108, E8103;
  - pre-commit üzerinden: ruff (tek satırda çoklu import), pylint-odoo (lisans, sürüm) ve modül kuralları kancaları başarısız, commit engellenirdi.
- Örnek modül depoya girmedi; şablon CI'da üretilen örnek modülle denetlenecek (T1.10).

**Kullanıcıya soru**
- K12 (USER_TASKS): modüllerde yazar olarak görünecek ad. Varsayım `burak-sisci`.

**Belgeler**
- CLAUDE.md (Odoo geliştirme kuralları "Her modülde", Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 lint), PLAN.md (T1.9, pano, T1.10'a lint ve şablon adımları, §8), USER_TASKS.md (K12), COMPLIANCE.md §5 (pylint-odoo, pylint, pre-commit), README.md, state.json.

### Adım: Test çalıştırma komutları (T1.8) — otonom mesai 1

**Kod**
- `tools/run_tests.py`: modül testlerini temiz bir veritabanında çalıştırır ve günlüğü özetler.
  - `db init --force` ile test veritabanı (demo yok, `en_US`), ardından `-i <modüller> --test-enable --test-tags /<modül>`. `--reuse` veritabanını korur ve `-u` kullanır.
  - Testler ayrı HTTP portunda (8079): Odoo test modunda HTTP sunucusunu her zaman açıyor; geliştirme sunucusuyla çakışmaz.
  - Günlükteki `ERROR:`/`FAIL:` bloklarını ve `X failed, Y error(s) of Z tests` satırını okur.
  - Windows'ta test sınıflarının filestore temizliği hataları (traceback'te `_gc_file_store_unsafe` + `PermissionError` ya da `.__gc` dosyası `AssertionError`) ayrı sayılır, çıkış kodunu etkilemez. `setUpClass`'ta da çıkıyor; ilk sürüm yalnız `tearDownClass`'ı tanıyordu, düzeltildi.
  - Özet satırı yoksa (kurulum çöktü) hata sayılır.

**Ortam**
- Doğrulama:
  - `l10n_tr`: 3 test, hata yok, `RESULT: OK` (38 sn).
  - `account_edi_ubl_cii` (negatif deneme): 230 test, 3 failed + 29 error. 27'si Windows gc hatası (24 `tearDownClass`, 3 `setUpClass`). Kalan 5 gerçek hata: T1.2'deki çekirdek test hatası (`deferred_start_date`), satır açıklaması içe aktarma testi, PDF motoru olmadığı için 2 PDF üretim testi, gömülü PDF testinde `LocalBinaryFile` TypeError. Sonuç `RESULT: FAILED (5)`, çıkış kodu 1.

**Belgeler**
- CLAUDE.md Komutlar (test komutları), ARCHITECTURE.md (§2 ağacı, §5 yerel testler), PLAN.md (T1.8, pano, T1.9 kabulüne komut), README.md, state.json.

### Adım: Odoo AI rehberleri (T1.7) — otonom mesai 1

**Kod**
- `.claude/skills/`: upstream `skills/` klasörünün değiştirilmemiş kopyası (24 dosya): `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`, `odoo-review`, `odoo-git`. Yanında `LICENSE` (upstream kopyası) ve `SOURCE.md` (kaynak commit).
- `tools/sync_skills.py`: kopyalar; `--check` upstream'le farkı denetler (CI için). Windows'ta upstream çalışma kopyası CRLF olduğundan karşılaştırma satır sonundan bağımsız; kopyalar LF.

**Araştırma**
- Rehberlerin tamamı okundu; zararlı veya gizli talimat yok.
- Lisans: klasörde ayrı lisans dosyası yok; deponun LGPL-3 lisansı ve `COPYRIGHT` notu geçerli. Envantere yazıldı.
- Proje kurallarıyla çelişenler (CLAUDE.md'ye öncelik kuralı olarak yazıldı):
  - `odoo-git`: `[TAG] kapsam: özet` commit biçimi, rebase ve `--force-with-lease`. Yalnız upstream/OCA katkısında geçerli sayıldı.
  - `odoo-review`: değişikliğin Enterprise'daki "diğer yarısına" bakma adımı. Clean-room (D-006) gereği uygulanmaz.
  - `odoo-web-guidelines`: `patch()` Odoo içinde önerilmiyor, Odoo dışı kod için uygun; kendi modüllerimizde serbest.
  - `comments`: kod yorumları, kullanıcı metinleri ve commit mesajlarında yalnız ASCII noktalama. Markdown belgelerimiz kapsam dışı.

**Belgeler**
- CLAUDE.md:
  - Odoo geliştirme kuralları: rehberler ve öncelik kuralları; görünüm kalıtımı kuralı rehberle uyumlu yazıldı.
  - Eski metin: "görünüm kalıtımı XPath ile". Yeni metin: ada bağlı kalıtım (kısa `field` biçimi, gerekirse XPath), konuma göre asla. Neden: `odoo-guidelines` kısa biçimi tercih ediyor.
  - Komutlar bölümüne `tools/sync_skills.py` eklendi.
- ARCHITECTURE.md §2 ağacı, COMPLIANCE.md §5, PLAN.md (T1.7, pano, T1.10'a rehber denetimi), README.md, state.json.

### Adım: Odoo'nun yerelde çalıştırılması (T1.6) — otonom mesai 1

**Kod**
- `deploy/odoo.conf.example`: yerel geliştirme yapılandırma şablonu.
  - Addons yolu ARCHITECTURE §2 sırasıyla, glob kalıplarıyla (`vendor/oca/*`, `ports/oca/*`, `addon[s]`): henüz olmayan klasörler uyarısız atlanır.
  - Veri klasörü `OV_HOME/odoo-data`, `workers = 0`, yalnız `127.0.0.1`.
- `tools/odoo_conf.py`: şablondan depo kökündeki `odoo.conf`'u üretir (git'e girmez). Veritabanı bilgileri `.env`'den; veritabanı yöneticisi ana şifresi ilk çalıştırmada `.env`'ye üretilir (`ODOO_ADMIN_PASSWD`).
- `ruff check tools/` (henüz depo yapılandırması yok, 0.16 varsayılanları): `odoo_conf.py` temiz; `check_docs.py` ve `pg.py`'de 14 bulgu (çoğu `re.M` → `re.MULTILINE`). Lint yapılandırmasıyla birlikte T1.9'da ele alınır.

**Ortam**
- Demo veritabanı `ov_demo`: `odoo-bin db init --with-demo --language tr_TR --country TR` (20 sn), ardından `-i account,l10n_tr` (37 sn).
- Günlükte tek uyarı: `markdown2` kurulu değil. Upstream'in hiçbir bağımlılık dosyasında yok; posta eklerinde markdown gösterimi için isteğe bağlı.
- Kabul:
  - giriş sayfası Türkçe (`Giriş`, `Şifre`, `E-posta`); admin oturumu `tr_TR`, `Europe/Istanbul`;
  - başsız Chrome ile (geçici profil) fatura listesi ve hesap planı ekranları açıldı, JS hatası yok, başlıklar `Faturalar` ve `Hesap Planı`;
  - `TR Company`: ülke TR, para birimi TRY, hesap planı `tr` (ekranda 343 satır), 44 vergi, Türkçe yevmiyeler (`Satışlar`, `Satınalma`, `Banka`, `Kasa` …), 1.046 vergi dairesi.
- Upstream demo düzeni: ana şirket (`YourCompany`, ülke TR) genel hesap planıyla ve USD ile gelir; Türk hesap planı ayrı demo şirketi `TR Company`'de. Kendi demo verimiz (T8.3) Türk şirketiyle başlayacak.

**Araştırma**
- PDF motoru: 20.0'da eklentili.
  - `base_report_wkhtmltox` kendiliğinden kurulur, ama wkhtmltopdf GitHub deposu arşivde (son push 2022-11-22).
  - `base_report_paper_muncher` Odoo'nun yeni motoru (LGPL-3, son sürüm v0.9.0, 2026-10-06); yalnız Linux paketleri var.
  - Yerelde kurulmadı; seçim T2.5'e not edildi.
- `l10n_tr` veri kalitesi gözlemleri T3.1'e not edildi: Türkçe büyük harf hatası, İngilizce kalan hesap ve vergi adları, çevrilmemiş sütun başlığı.
- Marka: giriş sayfasının başlığı `Odoo` (T2.2 kapsamında).

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md (§2 ağacı, §5 yerel Odoo), PLAN.md (T1.6, pano, T2.5 ve T3.1 notları), README.md, state.json.
- ARCHITECTURE §2 ağacında T1.3'te eklenen `tools/pg.py` eksikti; eklendi.

### Adım: Python sanal ortamı (T1.5) — otonom mesai 1

**Kod**
- `requirements-dev.txt` eklendi: upstream `requirements.txt`'yi içerir (`-r upstream/odoo/requirements.txt`), üstüne `ruff==0.16.10` (upstream `ruff.toml` 0.16 için yazılmış) ve `websocket-client==1.9.2` (HttpCase tarayıcı testleri `odoo/tests/common.py` içinde `websocket` içe aktarıyor).

**Ortam**
- Depoda `.venv` (Python 3.12.10, git'e girmez). Kurulum: `pip install --prefer-binary -r requirements-dev.txt`; `pip check` temiz.
- Kabul: `odoo-bin --version` → `Odoo Server 20.0`.
- Windows'ta upstream işaretleri yüzünden `gevent`, `greenlet`, `python-magic`, `python-ldap` kurulmaz. Yerel geliştirme iş parçacıklı sunucuyla yapılır; gevent/çok süreçli mod ve LDAP Linux'ta (CI, üretim) sınanır.

**Belgeler**
- CLAUDE.md (Ortam, Komutlar), ARCHITECTURE.md §5, COMPLIANCE.md §5 (ruff MIT, websocket-client Apache-2.0, upstream Python bağımlılıkları notu), PLAN.md (T1.5, pano, T8.4'e lisans dökümü notu), README.md, state.json.

### Adım: Upstream Odoo submodule (T1.4) — otonom mesai 1

**Kod**
- Odoo 20.0 Community `upstream/odoo` altına sığ git submodule olarak eklendi. Sabit commit `afbcf79d` (2026-10-18), T1.2 denemesinin yapıldığı commit.
  - `.gitmodules`: `branch = 20.0`, `shallow = true`, adres GitHub.
  - İndirme süresini kısaltmak için ilk klon yerel inceleme kopyasından alındı, sonra adres GitHub'a çevrildi (`git submodule set-url`, `sync`).
  - Kabul: depo temiz bir klasöre klonlandı; `git -c core.longpaths=true submodule update --init --depth 1` GitHub'dan sabit commit'i sığ olarak getirdi, çalışma ağacı temiz.
  - İlk deneme `-c core.longpaths=true` olmadan "Filename too long" ile düştü: süper depodaki `core.longpaths` ayarı alt modülün klonuna geçmiyor. CLAUDE.md komutu buna göre yazıldı.
- Yerel depoda `core.longpaths` açıldı (Windows yol uzunluğu, R11).

**Belgeler**
- docs/COMPLIANCE.md §5: lisans envanterine ilk satır (Odoo Community 20.0, LGPL-3, değiştirilmedi).
- CLAUDE.md: "Ortam" (upstream durumu) ve "Komutlar" (yeni klonda submodule komutu).
- ARCHITECTURE.md §2: `upstream/odoo` satırı. README.md: durum.
- PLAN.md: T1.4 `[x]`; F1 4/11; toplam 12/114; şu anki görev T1.5.
- state.json: `upstream` (yol, commit, tarih, `in_project: true`); T1.4 bitenlere eklendi.

### Adım: Sürüm doğrulaması (T1.2) — otonom mesai 1

19.0'daki Nilvera ve OCA modülleri 20.0'da gerçekten kurulup test edildi. Üç ağaç ölçüldü: değişmemiş kod, Odoo'nun otomatik dönüştürücüsü (`upgrade_code`) ve elle uyarlama.

**Araştırma**
- Yeni: `docs/research/nilvera-port.md`. Sonuçlar:
  - 19 modülden 18'i 21 tür küçük uyarlamayla kuruluyor; 268 testin 243'ü geçiyor. Elle değişiklik 36 dosya, +96/−145 satır.
  - Otomatik dönüştürücü tek başına 2/19 modülü kurulabilir yapıyor; Windows'ta düzgün çalışmıyor (yol ayırıcı, kodlama).
  - En büyük kalan kalem `account_financial_report`: 20.0'da `account.group` modeli yok (T5.4).
  - Gerçek davranış farkı: `is_company` artık vergi numarasından hesaplanıyor; Türkiye'de 11 haneli TCKN gerçek kişi sayılmalı (T4.3).
  - Kalan ek emek yaklaşık 9–15 oturum; mevcut port görevlerinin içinde.
  - 20.0 taze: Community çekirdeğinde UBL içe aktarma hatası (`deferred_start_date`) görüldü.
  - Windows'ta 20.0 test temizliği salt okunur filestore dosyalarını silemiyor; referans test ortamı Linux CI.
  - OCA geçiş gecikmesi (17.0–19.0): altyapı modülleri 0–3 ay, banka mutabakatı, cari ekstre ve kalite 4–14 ay.

**Kararlar**
- **D-011** Geçerli kaldı (**20.0**). Gerekçesine ölçüm sonucu eklendi; kabul edilen bedele `account_financial_report` ve 20.0'ın tazeliği eklendi.
  - Eski "Yeniden değerlendirme" satırı: "T1.2. İlk tahmin, MVP'nin OCA modülüne ihtiyacı olmadığı varsayımına dayanıyordu. D-018 ile bu varsayım değişti. Port maliyeti, upstream eklenmeden önce ölçülür. 20.0'ın maliyeti çok yüksek çıkarsa 19.0 seçeneği yeniden açılır."
  - Yeni hali: planlı nokta yok; yalnız 20.0 çekirdeğinde MVP'yi engelleyen, modülle aşılamayan ve upstream'de üç ay içinde düzelmeyen bir hata olursa yeniden açılır.
  - Neden: port maliyeti ölçüldü ve küçük çıktı. 19.0'da kalmak işi yalnız Eylül 2028'deki zorunlu göçe erteliyor.

**Belgeler (düzeltme)**
- Planlama adımındaki "`mis_builder`, `mis_builder_budget` ve `queue_job` 20.0'da var" bilgisi yanlıştı. Bu modüller OCA'nın 20.0 dalında yalnız yer tutucu (`installable: False`, sürüm 19.0).
  - Eski metin (planning-inputs.md §1): "`mis_builder`, `mis_builder_budget` | mis-builder | **var** | var | Doğrudan `vendor/` (T5.5)" ve "`queue_job` | queue | **var** | var | Gerekirse doğrudan `vendor/`".
  - Eski metin (PLAN.md T5.5): "OCA `mis_builder` (20.0'da mevcut) ile Tekdüzen şablonları".
  - Eski metin (MODULE_MATRIX.md): bilanço satırı "OCA (20.0 resmî)", bütçe satırı "`mis_builder_budget`, 20.0'da var".
  - Neden: o sayım OCA dallarındaki klasörlere bakıyordu; kurulabilirlik denetlenmemişti. Düzeltilen yerler: planning-inputs.md §1 (düzeltme notu ve tablo), MODULE_MATRIX.md (not ve iki satır), PLAN.md T5.5.
  - Ayrıca `account_statement_base`'in deposu düzeltildi: bank-statement-import değil, account-reconcile.
- PLAN.md: T1.2 `[x]`; F1 3/11; toplam 11/114; şu anki görev T1.4. R1 riski ölçüme göre güncellendi (olasılık D, etki O). T1.8, T4.3, T5.4 ve T5.5'e T1.2 bulguları eklendi.
- ARCHITECTURE.md: D-011 "T1.2'de doğrulandı". README.md: durum ve sıradaki görev.
- state.json: T1.2 bitenlere eklendi; şu anki görev T1.4; D-011'den `revisit` kaldırıldı; belge listesine `nilvera-port.md`.

### Adım: PostgreSQL kurulumu (T1.3) — otonom mesai 1

Otonom mesai 1 başladı (D-021). T1.3, T1.2'den önce yapıldı: T1.2'deki port denemesi (19.0 modüllerini 20.0'da kurup test etmek) çalışan bir PostgreSQL gerektiriyor.

**Ortam**
- PostgreSQL 18.6 kuruldu. Yönetici izni gerektirmeyen yol: EDB'nin Windows taşınabilir ikili zip'i, depo dışında `%LOCALAPPDATA%\odoo-version` (`OV_HOME`) altında.
  - Küme: UTF-8, `C.UTF-8` yerleşik yerel ayar, scram-sha-256 kimlik doğrulama, yalnız `localhost:5432`.
  - Sunucu kullanıcı hesabında çalışır. Windows hizmeti değildir; bilgisayar yeniden başlayınca `python tools/pg.py start` gerekir.
  - Rol `odoo` (LOGIN CREATEDB). Bağlantı bilgileri depodaki `.env` dosyasında (git'e girmez, D-015).
  - Kabul doğrulandı: `psql --version` 18.6; `odoo` rolüyle bağlantı kuruldu.
- Sürüm seçimi 18: Odoo 20.0'ın alt sınırı 16 (`odoo/release.py`); 18, CI ve olası Ubuntu sunucusunun paket sürümleriyle uyumlu.
- T1.2 için depo dışında inceleme kopyaları indirildi (`OV_HOME/src`): Odoo 20.0 (sığ klon, `afbcf79`), Odoo 19.0'ın yalnız `l10n_tr*` modülleri, ilgili OCA depolarının 19.0 ve 20.0 dalları.

**Kod**
- Yeni: `tools/pg.py` — yerel kümenin kurulumu ve yönetimi (`init`, `start`, `stop`, `status`).
  - Sunucu, çağıranın çıktı kanallarını devralmayacak biçimde başlatılır. Aksi halde çıktıyı bekleyen kabuk sunucu kapanana kadar takılıyordu (ilk denemede görüldü).

**Belgeler**
- PLAN.md: T1.3 `[x]`; F1 2/11; toplam 10/114.
- CLAUDE.md: "Ortam" (PostgreSQL) ve "Komutlar" (`tools/pg.py`).
- ARCHITECTURE.md §5: yerel PostgreSQL düzeni.
- docs/COMPLIANCE.md §5: depoya girmeyen geliştirme araçları tablosu; PostgreSQL satırı.
- state.json: `environment.postgresql`, T1.3 bitenlere eklendi.

### Adım: commit yazarlığı, kullanıcı belgesi, mesai türleri ve görev kategorileri

Kullanıcı istekleri:
- GitHub'da tek katkıcı kullanıcı olacak; Claude ortak yazar olarak yazılmayacak. Kural CLAUDE.md'ye girecek.
- Kullanıcıdan beklenenler için ayrı bir belge.
- İki mesai türü: standart (birlikte) ve otonom (Claude tek başına, kullanıcı ekran başında değil).
- Görevlerin tümü üç kategoride: kullanıcının yapacakları, birlikte yapılacaklar, Claude'un yapacakları.

**Kararlar**
- **D-015** güncellendi. Eski hali: commit yazarlığı hakkında kural yoktu; ilk iki commit'e `Co-Authored-By: Claude` satırı eklenmişti. Yeni hali: commit yazarı kullanıcının git kimliği; Claude'u yazar veya ortak yazar gösteren satır yazılmaz. Neden: kullanıcı bunu hata olarak bildirdi. Geçmiş iki commit'in temizlenmesi force-push gerektirdiği için kullanıcı kararına bırakıldı (USER_TASKS K10).
- **D-003** güncellendi. Eski hali: mesai türleri yoktu. Yeni hali: çalışma standart ve otonom mesailerle yürür; otonom mesaide sorular `USER_TASKS.md`'ye yazılır.
- **D-021** yeni, Geçerli: mesai türleri ve görev kategorileri (K / B / C); otonom mesai kuralları. Mesai türleri ve kategoriler kullanıcıdan, otonom kuralların ayrıntısı Claude'dan.

**Belgeler**
- Yeni: **`USER_TASKS.md`** — kullanıcı eylemleri, kararları ve onayları; K ve B görevlerinde kullanıcının payı; mesai türleri özeti.
  - PLAN.md §10'daki K1–K5, K8, K9 buraya taşındı.
  - K6 (müşteri listesi) ve K7 (yasal yapı) kaldırıldı; aynı işi anlatan T9.1 ve T9.3 görevleri kullanıldı.
  - Yeni: K10 (geçmiş commit'lerdeki ortak yazar satırı), K11 (`Claude-Session:` satırı).
- PLAN.md:
  - "Sorumlu" alanı "Kategori" oldu: C+K → **B**; K ve C aynı.
  - T10.4 C → B (ödeme sağlayıcısı hesabı kullanıcıda).
  - Yeni görev **T7.9 Kullanıcı kabul turu** (B). F7 kabulündeki elle tur bu göreve bağlandı. Toplam 113 → 114 görev.
  - Panoya "K · B · C" sütunu ve toplam satırına kategori sayıları eklendi: Kullanıcı 3 · Birlikte 13 · Claude 98.
  - T1.3: "gerekirse kullanıcıdan yönetici izni" yerine yönetici izni gerektirmeyen kurulum yolu.
  - §10 artık `USER_TASKS.md`'ye yönlendiriyor.
- CLAUDE.md: kural 8 (commit yazarlığı); "Mesai türleri" bölümü; belge haritasında `USER_TASKS.md`; protokol adım 3 ve 8.
- state.json: `session` alanı (otonom mesai 1), `project.user_tasks`, `project.commit_author`, D-021, belge listesinde `USER_TASKS.md`.
- README.md, ARCHITECTURE.md: `USER_TASKS.md` eklendi.
- `tools/check_docs.py`: görev kategorisi denetimi (K/B/C); panodaki ve toplam satırındaki kategori sayıları; `USER_TASKS.md`'deki K/B görev listesinin ve işaretlerinin PLAN ile aynılığı; tanımsız `K<n>` atıfları.

### Adım: detaylı planlama (T0.8)

Kullanıcı D-016'yı onayladı ve planlama kararlarını Claude'a bıraktı. Verdiği perspektif şöyle:
- öğrenci projesi, sıfır bütçe;
- bütçesiz, desteksiz ve müşterisiz alınabilecek tüm ilerleme alınınca müşteri arayışı;
- ilk müşteriler küçük işletmeler ve orta ölçekli fabrikalar; her satıştan sonra bir üst ölçek.

**Kararlar**
- **D-016** Açık → **Geçerli: AGPL-3.**
  - Eski hali: seçenekler A (AGPL-3) / B (LGPL-3) / C (kapalı) / D (karma), Claude önerisi "A, gerekirse D"; karar noktası T2.2.
  - Neden: kullanıcı öneriyi onayladı; depo ileride private yapılabilir, şimdilik AGPL-3.
  - Eklenenler: depo kökünde `LICENSE`; LGPL türevleri LGPL-3; OCA portları orijinal lisansla; private'a geçişin sınırları; dış katkı şimdilik kabul edilmiyor.
- **D-011** (20.0 kaldı, gerekçe ve tetikleyici değişti).
  - Eski metin: "MVP'nin (P0) hiçbir OCA modülüne ihtiyacı yok." Yeniden değerlendirme T3.1 (Nilvera port analizi). Submodule T1.3'te.
  - Yeni hali: bu varsayım D-018 ile geçersiz kaldı (mali raporlar, mutabakat, ekstre, kalite modülleri OCA'da yalnız 19.0'da). Yeniden değerlendirme **T1.2**: port maliyeti upstream eklenmeden önce ölçülür. Submodule T1.4'te. Gerekçeye "ilk müşteriler büyük olasılıkla 2027'de" eklendi.
- **D-012** (kullanıcının onayladığı kapsam genişletildi).
  - Eski metin: "MVP kapsamı: e-Fatura + e-Arşiv. e-İrsaliye MVP sonrası (P1), e-Defter ileride." Yeniden değerlendirme T6.1.
  - Yeni hali: MVP = e-Fatura + e-Arşiv + **e-İrsaliye** (P0). e-Defter P1 (T11.4); MVP'de mali müşavire aktarım (T5.9). Diğer e-Belgeler P3. Mimariye sahte (mock) adaptör eklendi. Yeniden değerlendirme **T8.1**.
  - Neden: hedef segmentteki orta ölçekli fabrikalar için e-İrsaliye zorunlu (e-Fatura mükellefi ve hasılat ≥ 10 Milyon TL); sevkiyat ve fason üretim e-İrsaliye gerektiriyor.
- **D-013** (Ertelendi kaldı, kapsamı daraldı).
  - Eski başlık: "Barındırma ve dağıtım modeli". Karar noktası T6.3.
  - Yeni başlık: "**Üretim barındırma yeri**". Teslim biçimi D-018'e taşındı. Karar noktası **T9.5**. "İlk müşteri on-prem seçerse daha da ertelenebilir" eklendi.
- **D-014**: yeniden değerlendirme T6.1 → **T8.1**; kalıcı adın uygulanması T8.2. OCA portları için teknik ad istisnası eklendi (D-019).
- **D-017** yeni, Geçerli: hedef müşteriler ve aşama stratejisi; müşteri arayışı kapısı M8. Yeniden değerlendirme T9.8.
- **D-018** yeni, Geçerli: MVP tanımı (Ticaret ve Üretim paketleri), öncelik tanımları (P0–P5), MVP dışı liste, teslim biçimi (yönetilen kurulum; self-servis SaaS F10). Yeniden değerlendirme T8.1.
- **D-019** yeni, Geçerli: OCA modülleri — resmî 20.0 `vendor/oca/`, yoksa 19.0'dan port `ports/oca/` (orijinal ad, lisans ve yazarlar).
- **D-020** yeni, Geçerli: ücretsiz altyapı — GitHub Actions, GitHub Pages (yalnız açık kaynak belgeler), Cloudflare Quick Tunnel (demo), Nilvera test portalı, Student Pack (isteğe bağlı).
- Küçük metin güncellemeleri:
  - **D-002:** "İlk satışa çıkan kapsam D-018'dedir" eklendi.
  - **D-005:** "Ücretsiz kaynaklar D-020'de" eklendi.
  - **D-008/3** eski metin: "AGPL-3 OCA modülleri ayrı tutulur. Değiştirilirse, SaaS kullanıcılarına değiştirilmiş kaynak sunulur." Yeni hali: 20.0 portları da (D-019) bu kapsamda.
  - **D-008/4** eski metin: "Kapalı kaynak (kendi lisansımızla) modüllerimiz AGPL modüllere bağımlı olamaz. Kapalı modül olup olmayacağı D-016'ya bağlı." Yeni hali: şu an kapalı modül yok; kendi modüllerimiz AGPL-3.
  - **D-008/5** eski metin: "her 3. parti modül". Yeni hali: "her 3. parti kod ve veri".
  - **D-010:** OCA portlarının yeri (`ports/`) eklendi.
  - DECISIONS.md giriş notu: tetikleyiciler artık "ROADMAP görevine" değil, "PLAN.md'deki bir göreve" bağlanır.

**Belgeler**
- `ROADMAP.md` → **`PLAN.md`** (yeniden adlandırıldı ve baştan yazıldı). İçerik:
  - ilerleme panosu;
  - strateji, paketler ve Türkiye gereksinimleri;
  - 12 faz (F0–F11), 113 görev; her görevde büyüklük, sorumlu ve kabul ölçütleri;
  - sürekli işler, ücretsiz kaynaklar, test stratejisi, risk kaydı, kullanıcı eylemleri (K1–K9).
- Eski → yeni görev numaraları:
  - eski T0.8 → T0.8 (tamamlandı);
  - eski T1.2–T1.7 → T1.3, T1.4, T1.5, T1.6, T1.7, T1.8; yeni T1.2 (sürüm doğrulaması), T1.9 (modül şablonu ve lint), T1.10 (CI), T1.11 (`vendor/` ve `ports/`);
  - eski T2.1–T2.4 → aynı numaralar; yeni T2.5–T2.7;
  - eski Faz 3 (e-Belge) → F4: eski T3.1 → T4.1, T3.2 → T4.3, T3.3 → T4.5, T3.4 → T4.6, T3.5 (e-İrsaliye, P1) → T4.8 (P0); eski T3.6 (SMS) → T11.5. Yeni F3: Türkiye temel yerelleştirmesi;
  - eski Faz 4 (Enterprise eşdeğerleri) → F5 (muhasebe P0 kısmı), F11 (T11.1 sabit kıymet, T11.10–T11.12 P2–P4 paketleri);
  - eski Faz 5 (SaaS) → F10 (T10.1–T10.7); eski T5.3 yedekleme → T8.5 (yönetilen kurulum için) + T10.5;
  - eski T6.1 → T8.1, T6.2 → T9.4, T6.3 → T9.5, T6.4 → T9.6.
- `LICENSE` eklendi (GNU AGPL v3, gnu.org resmî metni).
- DECISIONS.md: yukarıdaki kararlar; özet tablo; "Açık kararlar" bölümü boşaldığı için kaldırıldı.
- state.json: faz F1, şu anki görev T1.2; T0.8 tamamlandı; lisans, plan, hedef segmentler ve kilometre taşları; karar değerleri ve tetikleyicileri; `modules.ported`; yeni belge `docs/research/planning-inputs.md`.
- CLAUDE.md: proje özeti (paketler, lisans), belge haritasında PLAN.md, protokol 8 adım (PLAN işaretleri ve pano), kurallar 3–5 ve 7, ortam ve komutlarda yeni görev numaraları.
- README.md: durum, paketler, PLAN bağlantısı, lisans ve katkı bölümleri.
- ARCHITECTURE.md: durum notu, `vendor/` + `ports/` düzeni (D-019), modül tablosunda lisans sütunu ve yeni satırlar, teslim biçimi (D-018), geliştirme ortamı ve CI bölümü.
- docs/COMPLIANCE.md: lisans satırları AGPL-3; görev atıfları (T9.4, T8.2, T2.3, T2.7, T1.4); public depo kuralları (Nilvera bilgileri, GİB paketleri, CI gizli bilgi taraması, depo lisansı).
- docs/MODULE_MATRIX.md: yeni öncelik tanımları ve Paket sütunu; öncelikler paketlere göre yeniden belirlendi (ör. mrp, fason, bakım P0; e-İrsaliye P0; POS P2).
- docs/research/e-fatura.md: sonuç notu (e-İrsaliye MVP'de, e-Defter P1); §5 değerlendirme tablosu; yeni §6 "Planlama için ek bulgular"; kaynaklar; görev atıfları T6.1/T6.2 → T8.1/T9.4.
- docs/research/hosting.md: D-013'ün yeni başlığı ve kapsamı; Quick Tunnel sınırları; on-prem satırı (D-018); görev atıfları T6.2/T6.3 → T9.4/T9.5.
- docs/research/approach-b-vs-c.md: "ROADMAP T2.4" → "PLAN T2.4".
- Yeni: docs/research/planning-inputs.md (OCA 20.0 durumu, çeviri kapsamı, yerel 20.0 kontrolleri, ücretsiz kaynaklar, veri kaynakları, pazar referansları).
- `tools/check_docs.py`: ROADMAP yerine PLAN.md; yinelenen görev numarası, faz başlığı işaretleri, pano satırları, toplam satırı, "Şu anki görev" satırı ve `phase.id` denetimleri.

**Araştırma**
- OCA 20.0: `l10n-turkey` 18.0/19.0/20.0'da boş. Muhasebe, mutabakat, ekstre, kalite, MRP planlama ve sabit kıymet modülleri yalnız 19.0'da; `mis_builder`, `queue_job`, `remove_odoo_enterprise` 20.0'da var.
- 20.0 Türkçe çeviri kapsamı ölçüldü: çekirdek modüller %79–93; `l10n_tr` %33.
- Ücretsiz kaynakların koşulları: GitHub Actions, GitHub Pages (ticari kullanım yasağı), Cloudflare Quick Tunnel sınırları, Student Pack, TÜBİTAK 2209-A (son başvuru 11 Kasım 2026).
- e-Belge: Nilvera kamuya açık test ortamı; GİB doğrudan testi mali mühür gerektiriyor; 2026 UBL-TR paket güncellemeleri; Ba-Bs formlarının Eylül 2024'ten itibaren kaldırılması; e-Defter geçiş kuralı (ikincil kaynaklar).
- Veri kaynakları: TCMB günlük kur XML; il/ilçe listesi (MIT lisanslı aday).

### Adım: kullanıcı kararları (T0.7) ve git/GitHub deposu (T1.1)

**Kararlar**
- **D-010** Açık → Geçerli: **B** (kullanıcı). Eski hali: seçenekler B / C / B+, Claude önerisi B+. Neden: kullanıcı yama kuyruğu olmayan B'yi seçti; `patches/` kaldırıldı. Modülle çözülemeyen durum yeni karar olarak gelecek.
- **D-011** Açık → Geçerli: **20.0**. Eski hali: seçenekler 20.0 / 19.0 / 18.0, öneri 20.0. Neden: kullanıcı kararı Claude'a bıraktı. Yeniden değerlendirme T3.1'e bağlandı.
- **D-012** Açık → Geçerli. Eski hali (öneri): e-Fatura + e-Arşiv MVP, özel entegratör API, Nilvera 19.0 port. Neden: kullanıcı kapsamı ve yöntemi onayladı ve "MVP sonunda tekrar ele alırız" dedi. Yeniden değerlendirme T6.1'e bağlandı.
- **D-013** Açık → **Ertelendi**. Eski hali (öneri): aşamalı SaaS (lokal → ücretsiz demo → Türkiye VPS; on-prem ileride). Neden: kullanıcı "hemen karar vermeli miyiz?" diye sordu. Cevap: hayır, gerçek müşteri verisine kadar gerekmiyor. Karar noktası T6.3. Geçici düzen: lokal geliştirme ve sağlayıcıdan bağımsız mimari.
- **D-014** Açık → Geçerli. Eski hali: marka adı ve önek belirlenmemiş. Neden: kullanıcı çalışma adını `odoo-version` olarak verdi (MVP sonunda değişecek). Claude öneki markadan bağımsız ve kalıcı `ov_` olarak seçti. Yeniden değerlendirme T6.1.
- **D-015** Açık → Geçerli. Eski hali (öneri): yerel git, push yalnız onayla. Neden: kullanıcı public GitHub deposu ve her görev sonunda commit + push istedi; push önceden onaylı hale geldi.
- **D-016** yeni, Açık: kendi modüllerimizin lisansı. Neden: public depo, kod yayımlanmadan önce lisans seçimini gerektiriyor. Öneri AGPL-3 (+ gerekirse private depo). Karar noktası T2.2.
- **D-003** güncellendi. Eski metin: "dışa dönük işlemler (yayınlama, paylaşma, uzak depoya push)" kullanıcıya sorulur. Yeni hali: proje deposuna push D-015 ile önceden onaylı; yayınlama, paylaşma ve depo ayarları yine sorulur.
- **D-008/1** güncellendi. Eski metin: "Upstream Odoo Community (LGPL-3) değiştirilirse değişiklikler LGPL-3 kalır." Yeni hali: upstream değiştirilmez (D-010). Madde 4'e D-016 bağlantısı eklendi.
- Karar durumlarına **Ertelendi** eklendi. `**Karar noktası:**` ve `**Yeniden değerlendirme:**` satırları ROADMAP görevlerine bağlandı.

**Belgeler**
- DECISIONS.md yeniden yazıldı (yukarıdaki kararlar).
- ROADMAP.md:
  - T0.7 ve T1.1 tamamlandı.
  - Yeni T0.8: detaylı planlama.
  - Faz 6 yeniden numaralandı. Yeni T6.1 MVP sonu değerlendirmesi; eski T6.1 → T6.2 (hukuki inceleme), eski T6.2 → T6.3 (artık "Üretim barındırma kararı (D-013) ve üretim sunucusu"), eski T6.3 → T6.4.
  - T2.4 B'ye göre yeniden yazıldı.
  - Faz başlıklarındaki karar ön koşulları güncellendi.
- ARCHITECTURE.md:
  - Durum notu: B / 20.0 / `ov_` Geçerli.
  - `patches/` kaldırıldı.
  - Önek `ov_`; lisans sütunu D-016'ya bağlandı.
  - Konum ertelendi ve sağlayıcıdan bağımsızlık kısıtı eklendi.
  - `.gitignore` / `.gitattributes` eklendi.
- CLAUDE.md:
  - proje özeti;
  - protokol adım 3 (karar noktası görevleri) ve adım 7 (commit + push);
  - kurallar 2–7;
  - ortam (gh, git deposu) ve komutlar.
- COMPLIANCE.md: kendi modüllerimizin lisansı → D-016; çalışma adı ve marka notu; public depo kuralları; T6.1 → T6.2.
- MODULE_MATRIX.md: "Karar verilecek" lisanslar → D-016; AGPL notu.
- research/approach-b-vs-c.md, research/e-fatura.md: başa "Sonuç" notu eklendi; T6.1 → T6.2.
- research/hosting.md:
  - "Sonuç", "Karar ne zaman gerekli?" ve "Benzer platformlar nerede çalışıyor?" bölümleri eklendi;
  - "Öneri" başlığı "Ön öneri" oldu;
  - T6.1 → T6.2.
- README.md: durum, çalışma adı, lisans notu.
- `tools/check_docs.py`:
  - "Ertelendi" durumu;
  - ertelenmiş kararda karar noktası zorunluluğu;
  - karar noktası veya yeniden değerlendirme görevi tamamlanmışsa hata;
  - belgelerde (CHANGELOG hariç) ROADMAP'te olmayan görev numarasına atıf denetimi.

**Araştırma**
- Benzer platformların barındırma yerleri incelendi:
  - Odoo Online / Odoo.sh: OVHcloud, Google Cloud, AWS; Türkiye bölgesi yok.
  - Frappe Cloud: AWS ve Oracle Cloud; Türkiye bölgesi yok.
  - Paraşüt aydınlatma metni: yurt dışı aktarım açık rızayla.
  - Logo: Cloud + Edge karma modeli.

**Ortam**
- Git deposu başlatıldı (`main`), `.gitignore` ve `.gitattributes` eklendi.
- Public GitHub deposu oluşturuldu: https://github.com/burak-sisci/odoo-version

### Adım: ilk belgeler (T0.1–T0.6)

**Kararlar**
- Geçerli olarak eklendi: D-001 ürün hedefi, D-002 kapsam, D-003 ekip/çalışma modeli, D-004 dokümantasyon protokolü (kullanıcı); D-005 sıfır bütçe (kullanıcı, 2026-10-16); D-006 clean-room, D-007 marka, D-008 lisans uyumu (hukuki zorunluluk); D-009 dil (Claude varsayılanı).
- Açık olarak eklendi (Claude önerileriyle): D-010 yaklaşım (öneri B+), D-011 sürüm (öneri 20.0), D-012 e-Belge stratejisi, D-013 barındırma, D-014 marka adı/önek, D-015 git/commit yetkisi.

**Araştırma**
- B / C yaklaşım karşılaştırması (marka izleri envanteri, Flectra örneği).
- e-Fatura / e-Arşiv / e-İrsaliye: GİB 509 Tebliğ güncel metni (589 değişiklikleri dahil) incelendi. Önemli bulgu: 1/1/2026'dan itibaren bilanço esaslı mükellefler tutardan bağımsız e-Arşiv/e-Fatura düzenlemek zorunda.
- Odoo 20.0'da Nilvera e-Belge modüllerinin Enterprise'a taşındığı, 19.0'da LGPL olduğu doğrulandı.
- OCA modül sayıları 18.0 / 19.0 / 20.0 dalları için çıkarıldı; OCA lisans örnekleri (çoğu AGPL-3).
- Barındırma seçenekleri; KVKK m.9 (7499 sayılı Kanun) ve e-Belge yurt içi saklama kuralı.

**Belgeler**
- Oluşturuldu: CLAUDE.md, README.md, ARCHITECTURE.md, DECISIONS.md, ROADMAP.md, CHANGELOG.md, state.json, docs/COMPLIANCE.md, docs/MODULE_MATRIX.md, docs/research/{odoo-analysis, approach-b-vs-c, e-fatura, hosting}.md.
- Belge tutarlılık denetimi eklendi: `tools/check_docs.py`.

## 2026-10-16

**Araştırma**
- Odoo 20.0 Community kaynak kodu indirildi ve incelendi (commit `1740e969`): 657 modül, 34 uygulama, tamamı LGPL-3; mimari, ORM, web istemcisi, `skills/` klasörü.
- Lisanslar (Community LGPL-3, Enterprise özel lisans) ve edinme yolları (sıfırdan klon / Community + modüller / çatal / kendi küçük ERP'miz) değerlendirildi.
