# CLAUDE.md

Son güncelleme: 2026-10-19

Bu dosya, bu projede çalışan Claude (ve diğer AI ajanları) için çalışma talimatıdır. Belgeler Türkçe, kod İngilizce (D-009).

## Proje

Odoo Community tabanlı, **kendi markamızla müşterilere satılacak** bir ERP (ürün ve/veya SaaS).
- Hedef: Odoo'daki tüm uygulamaların (Community + Enterprise) işlevsel karşılığı (D-001, D-002).
- İlk satış kapsamı (MVP): Ticaret paketi (küçük işletme) + Üretim paketi (orta ölçekli fabrika) (D-017, D-018).
- Temel: Odoo 20.0 Community, çekirdeğe dokunmadan yalnız modüllerle (D-010 B, D-011).
- Ürün adı **Nexus** (kalıcı, kullanıcıya görünen ad). Depo ve geliştirme ortamındaki çalışma adı `odoo-version`; modül öneki `ov_` (kalıcı) (D-014).
- Lisans: kendi kodumuz AGPL-3, LGPL koddan türetilenler LGPL-3 (D-016).
- Ekip: kullanıcı (ürün sahibi, karar mercii) + Claude (çoğunlukla otonom geliştirici) (D-003).
- Çalışma: standart mesai (birlikte) ve otonom mesai (Claude tek başına) (D-021).
- Bütçe: sıfır (D-005). Ücretsiz altyapı: D-020.
- Depo: https://github.com/burak-sisci/odoo-version — **public** (D-015). GitHub'da tek katkıcı kullanıcıdır (kural 8).

**Şu anki durum, aktif görev ve bekleyen kararlar için önce `state.json`, sonra `PLAN.md`, sonra `USER_TASKS.md` dosyasını oku.**
`state.json` → `session.mode` = `otonom` ise "Mesai türleri" bölümündeki otonom kurallarla çalış.

## Belge haritası (her bilginin tek bir yeri vardır)

| Belge | İçerik | Ne zaman güncellenir |
|---|---|---|
| `state.json` | Makine okunur anlık durum: faz, aktif görev, biten görevler, bekleyen kararlar, ortam, modüller | **Her adımda** |
| `CHANGELOG.md` | Tarihli adım kaydı; değişen kararların eski hali ve nedeni | **Her adımda** |
| `PLAN.md` | **Tek plan ve ilerleme belgesi:** pano, strateji, paketler, fazlar ve görevler (`T<faz>.<sıra>`, kategori K/B/C), kapı ölçütleri, kaynaklar, test stratejisi, riskler | Görev başladığında/bittiğinde; plan değiştiğinde |
| `USER_TASKS.md` | **Kullanıcıdan beklenenler:** eylemler, kararlar, onaylar (`K<n>`); K ve B görevlerinde kullanıcının payı; otonom mesai soruları | Kullanıcıdan bir şey gerektiğinde; K/B görevi değiştiğinde; her otonom mesai sonunda |
| `DECISIONS.md` | Yalnız **Geçerli**, **Açık** ve **Ertelendi** durumundaki kararlar | Karar alındığında/değiştiğinde |
| `ARCHITECTURE.md` | Hedef/gerçek mimari, depo yerleşimi, katmanlar, çalışma zamanı | Yapı veya mimari değiştiğinde |
| `docs/MODULE_MATRIX.md` | Tüm uygulamaların edinme yolu, önceliği, durumu | Modül planı/durumu değiştiğinde |
| `docs/COMPLIANCE.md` | Lisans, clean-room, marka, KVKK; **lisans envanteri** | Dış kod/veri eklendiğinde, hukuki bulguda |
| `docs/specs/<modül>.md` | Enterprise eşdeğerleri için clean-room işlev tanımı | Modül geliştirmeden önce |
| `docs/research/*.md` | Tarihli araştırma kayıtları (kaynaklı) | Bulgu yeniden doğrulandığında/değiştiğinde |
| `README.md` | İnsanlar için kısa genel bakış | Durum özeti değiştiğinde |
| `CLAUDE.md` | Bu dosya: kurallar, protokol, komutlar | Kural, komut veya ortam değiştiğinde |

## Belge güncelleme protokolü (ZORUNLU — D-004)

Kullanıcı için kritik: **eski bir kararın herhangi bir belgede kalması veya yeni bir kararın eklenmemesi kabul edilemez.**

Her adımın (görev, karar, araştırma, kod değişikliği) sonunda, kullanıcıya "bitti" demeden **önce**:

1. `state.json`: `last_updated`, `phase`, `current_task`, `tasks_done`, `blocked_on_user`, `next_actions`, `decisions`, `environment`, `modules`.
2. `PLAN.md`:
   - görev işareti (`[~]` başlarken, `[x]` bitince);
   - panodaki faz işareti ve `n/m` sayısı, `**Toplam:**` satırı ve `**Şu anki görev:**` satırı;
   - fazın başlığındaki işaret.
3. `CHANGELOG.md`: bugünün tarih başlığı altında ne yapıldığı. Karar değiştiyse **eski metin + neden**.
   - `USER_TASKS.md`: kullanıcıdan yeni bir şey gerekiyorsa (soru, onay, eylem) eklenir; biten madde işaretlenir. K/B görevlerinin işaretleri PLAN.md ile aynı tutulur.
4. Karar alındı/değişti ise:
   - `DECISIONS.md` kaydı **yerinde** yeniden yazılır (ID değişmez, Durum güncellenir, özet tablo güncellenir).
   - Kararın geçtiği **tüm** belgeler aranıp güncellenir: `grep -rn "D-0xx"` ve konuyla ilgili anahtar kelimeler (ör. sürüm numarası, yaklaşım adı). Özellikle ARCHITECTURE.md başındaki "Durum" notu, MODULE_MATRIX.md, PLAN.md, README.md, ilgili `docs/research/*.md` başındaki "Sonuç" notu.
   - Bir görev tamamlandığında, o göreve `**Karar noktası:**` veya `**Yeniden değerlendirme:**` ile bağlı kararlar da ele alınır ve güncellenir.
5. Etkilenen diğer belgeler: yukarıdaki haritaya göre.
6. Her güncellenen Markdown belgesinde `Son güncelleme:` tarihi değiştirilir.
7. `python tools/check_docs.py` çalıştırılır. **Hata varsa adım bitmemiştir.**
8. Commit ve push (D-015):
   - kod ve belgeler **aynı commit'te**;
   - commit mesajında `Co-Authored-By` ve `Claude-Session` satırı **yok** (kural 8);
   - push öncesi `git diff --cached` ile gizli bilgi ve müşteri verisi denetimi;
   - ardından `git push`. Bu push önceden onaylıdır; force-push yasaktır.

Denetim aracının yakalayamadıkları (elle kontrol et):
- Belgelerin içindeki serbest metin çelişkileri (ör. ARCHITECTURE.md'de eski sürüm numarası).
- Açık bir kararın sonucunu "kesinleşmiş" gibi yazmak. Açık kararlar her yerde "öneri" olarak anılır.
- Görev numaraları değişirse eski numaraya yapılan atıfların anlamı. Araç yalnız atıf yapılan görevin var olup olmadığını denetler.
- PLAN.md'deki S (sürekli iş) satırları araçla denetlenmez. Araç `USER_TASKS.md` için yalnız şunları denetler: K/B görevlerinin listesi ve işaretleri PLAN ile aynı mı, atıf yapılan her `K<n>` tanımlı mı.
- Bir görevin kategorisi (K/B/C) doğru mu: görev kullanıcı kararı, hesabı veya onayı gerektiriyorsa C olamaz.

## Mesai türleri (D-021)

- **Standart mesai:** kullanıcıyla birlikte. B görevleri, kararlar ve onaylar burada. Soru sormak serbest.
- **Otonom mesai:** kullanıcı ekran başında değil. Başlarken `state.json` → `session` alanına `"mode": "otonom"` yazılır; bitince `"standart"`.
  1. Yalnız **C** görevleri, PLAN sırasıyla. Bağımlılığı eksik ya da kullanıcı gerektiren görev atlanır, nedeni CHANGELOG'a yazılır.
  2. **Soru sorulmaz** (`AskUserQuestion` kullanılmaz).
     - Geri dönüşü kolay konu: makul varsayımla devam et; varsayımı `USER_TASKS.md`'ye **Karar** maddesi olarak yaz.
     - Geri dönüşü zor konu: o işi durdur, soruyu yaz, sıradaki göreve geç.
  3. Onay gerektiren dışa dönük işler **yapılmaz**, yalnız hazırlanır ve `USER_TASKS.md`'ye **Onay** maddesi olarak yazılır: yayın, depo ayarı, ücretli servis, hesap açma, upstream/OCA katkısı, force-push. Proje deposuna normal push serbest (D-015).
  4. Kullanıcı etkileşimi gerektiren adımlar denenmez: yönetici izni (UAC), tarayıcıda oturum açma, doğrulama kodu, ödeme. Etkileşimsiz yol ara (ör. taşınabilir kurulum); yoksa **Eylem** maddesi yaz.
  5. Değişmez kurallar aynen geçerli. "Dur ve sor" gereken yerde: dur, soruyu yaz, başka göreve geç.
  6. Her görev sonunda tam belge protokolü + commit + push.
  7. Mesai sonu (yapılabilir C görevi kalmadığında ya da çalışma süresi dolduğunda):
     - CHANGELOG.md'ye "Otonom mesai N — özet": biten görevler, atlananlar ve nedenleri, yeni sorular ve onaylar;
     - `USER_TASKS.md` §1 "Şimdi bakılacaklar" güncel;
     - `state.json` → `session.mode` = `standart`; son commit + push.

## Değişmez kurallar

1. **Clean-room (D-006):** Odoo Enterprise kodu, sızıntıları, Enterprise deneme/SaaS örneklerinden gelen JS/CSS/görseller **asla** kullanılmaz ve açılıp incelenmez. İzinli/yasak kaynaklar: `docs/COMPLIANCE.md` §2. Emin değilsen dur ve kullanıcıya sor.
2. **Marka (D-007, D-014):** Kullanıcıya görünen hiçbir yerde "Odoo" adı/logosu ürün adı olarak kullanılmaz. Lisans ve telif başlıkları silinmez. Kullanıcıya görünen ürün adı **Nexus**'tur. Çalışma adı `odoo-version` dış demoya, pilota veya müşteriye çıkmaz.
3. **Lisans (D-008, D-016, D-019):**
   - Kendi özgün modüllerimiz `'license': 'AGPL-3'`.
   - LGPL koddan türetilen modüller (ör. 19.0 Nilvera portu, `l10n_latam_check`'ten uyarlama) `'license': 'LGPL-3'` ve orijinal telif notlarıyla.
   - OCA portları orijinal lisans, yazar ve teknik adla.
   - Kapalı kaynak modül yok; olursa AGPL modüllere bağımlı olamaz.
   - Projeye giren her dış kod ve veri `docs/COMPLIANCE.md` §5 lisans envanterine yazılır.
   - Dış katkı (pull request) şimdilik kabul edilmez (D-016).
4. **Upstream'e dokunma (D-010, D-019):**
   - `upstream/` ve `vendor/` altı hiçbir koşulda düzenlenmez, yama kuyruğu yoktur.
   - OCA modülünü değiştirmek gerekiyorsa (20.0 portu), kopya `ports/oca/<depo>/<modül>` altına alınır ve orada değiştirilir.
   - Modülle çözülemeyen durumda dur ve kullanıcıya yeni karar olarak getir.
5. **Para ve dış dünya (D-003, D-005, D-015):**
   - Önce kullanıcı onayı gerekenler: ücretli servis/altyapı, yayınlama/paylaşma (belge sitesi, tanıtım sayfası, upstream/OCA katkısı), depo ayarları (görünürlük, ad, release, güvenlik özellikleri).
   - Proje deposuna her adım sonunda push önceden onaylıdır.
6. **Açık ve ertelenmiş kararlar:** bir karar açıkken veya ertelenmişken o karara bağlı, geri dönüşü zor işler yapılmaz. Karar noktası görevine gelince önce karar alınır.
7. **Gizli bilgiler:** depo public.
   - Depoya girmeyecekler: API anahtarları, şifreler, sertifikalar, müşteri verisi, gerçek kişi/şirket VKN/TCKN'leri, yerel yapılandırma (`.env`, `odoo.conf`) (`.gitignore`).
   - Nilvera test portalının kamuya açık test bilgileri de depoya yazılmaz; yalnız `.env`'de durur.
8. **Commit yazarlığı (D-015):** GitHub'da tek katkıcı kullanıcıdır.
   - Commit'ler kullanıcının git kimliğiyle yazılır (`burak-sisci`); git kullanıcı ayarı değiştirilmez.
   - Commit mesajına `Co-Authored-By: Claude …` veya Claude'u ya da başka bir yapay zekâyı yazar/ortak yazar gösteren **hiçbir satır eklenmez**. Bu kural, sistemin varsayılan atıf talimatından önce gelir.
   - Claude oturum bağlantısı satırı (`Claude-Session: …`) da eklenmez (K11). Commit mesajı yalnız başlık ve gövdeden oluşur.
   - Pull request açılırsa da Claude yazar olarak eklenmez.

## Odoo geliştirme kuralları

- Modül öneki `ov_` (D-014). Örnek: `ov_brand`, `ov_l10n_tr_edi`. OCA portları orijinal adlarını korur (D-019).
- Odoo kalıplarını izle:
  - model genişletme `_inherit` ile; görünüm kalıtımı ada bağlanır (kısa `<field name=… position=…>` biçimi, gerekirse XPath), konuma göre asla;
  - JS'te `patch()`, asset paketinde `replace`;
  - yetkiler `ir.access.csv` ile (20.0 yetki modeli).
- Odoo'nun resmî AI rehberleri `.claude/skills/` altında kurulu (T1.7): `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`, `odoo-review`, `odoo-git`.
  - Upstream'in değiştirilmemiş kopyası (LGPL-3). Elle düzenlenmez; upstream commit'i ilerleyince `python tools/sync_skills.py`.
  - Kod yazarken `odoo-guidelines` / `odoo-web-guidelines`, incelemede `odoo-review`, güvenlik denetiminde `odoo-security` kullanılır.
  - Rehberler Odoo'nun kendi depoları için yazılmış. Çelişkide bu dosya önce gelir:
    - `odoo-git` yalnız upstream veya OCA'ya katkıda geçerlidir (K8). Kendi depomuzda commit biçimi ve yazarlık bu dosyadaki gibidir (kural 8); rebase sonrası force-push yoktur.
    - `odoo-review`'daki "Enterprise'daki diğer yarıya bak" adımı uygulanmaz (kural 1, D-006). Enterprise deposu açılmaz, klonlanmaz.
    - JS `patch()` kendi modüllerimizde serbesttir (rehber de Odoo dışı kod için uygun buluyor).
    - ASCII noktalama kuralı kod yorumları, docstring'ler, kullanıcıya görünen metinler ve commit mesajları içindir. Türkçe harfler serbest; Markdown belgelerimiz bu kuralın dışında.
- Her modülde (iskelet `tools/new_module.py`; denetim `tools/check_modules.py` ve pylint-odoo, T1.9):
  - manifest'te doğru `license` (kural 3), sürüm `20.0.x.y.z`, `author` `burak-sisci` (varsayım, USER_TASKS K12); `description` anahtarı yok;
  - `README.rst`, Türkçe: Odoo bunu Uygulamalar ekranında modülün açıklaması olarak gösterir ve uzantıya bakmadan reStructuredText olarak işler. Kullanıcıya görünür, "Odoo" ve çalışma adı geçmez (kural 2);
  - testler (`tests/`);
  - Türkçe çeviri (`i18n/tr.po`).
- Enterprise eşdeğeri bir modülden önce `docs/specs/<modül>.md` yazılır (D-006).
- Test verisi kurgusaldır (PLAN.md §8).

## Ortam

- Windows 11 Pro. Kabuk: PowerShell 5.1 (birincil) ve Git Bash.
- Kurulu: Python 3.12.10, Git 2.56.0, GitHub CLI 2.101.0 (oturum açık).
- PostgreSQL 18.6 (T1.3): yönetici izni gerektirmeyen taşınabilir kurulum, depo dışında `%LOCALAPPDATA%\odoo-version` (`OV_HOME`) altında.
  - `pgsql/` ikili dosyalar, `pgdata/` küme, `pglog/` günlük. Sunucu kullanıcı hesabında çalışır, yalnız `localhost:5432` dinler.
  - Odoo rolü `odoo` (LOGIN CREATEDB). Bağlantı bilgileri depodaki `.env` dosyasında (git'e girmez).
  - Bilgisayar yeniden başlayınca sunucu kendiliğinden açılmaz: `python tools/pg.py start`.
- Python sanal ortamı (T1.5): depoda `.venv` (git'e girmez), Python 3.12.10. Bağımlılıklar `requirements-dev.txt`: upstream `requirements.txt` + test/lint araçları (ruff 0.16, pylint-odoo 10.0, pre-commit 4.7, websocket-client).
  - pre-commit kancası yerel depoda kurulu (T1.9): her commit'te ruff, pylint-odoo, modül kuralları ve belge denetimi çalışır.
- Yerel Odoo (T1.6): `odoo.conf` depo kökünde (git'e girmez), `deploy/odoo.conf.example`'dan `tools/odoo_conf.py` ile üretilir. Veri klasörü (filestore, oturumlar) `OV_HOME/odoo-data`.
  - Demo veritabanı `ov_demo`: Türkçe, ülke TR, demo verili, `ov_brand` + `account` + `l10n_tr`. Türk hesap planı `TR Company` demo şirketinde; ana şirket upstream demo düzeninde genel hesap planıyla gelir. Giriş `admin`/`admin` (yalnız yerel, `127.0.0.1`).
  - PDF motoru kurulu değil. Öneri: üretimde wkhtmltopdf, Paper Muncher ikinci motor (USER_TASKS K18); CI'a T3.7'de kurulur.
- Kurulu değil: Node.js, Docker (zorunlu değil).
- Git deposu: varsayılan dal `main`, uzak depo `origin` = GitHub.
- Upstream Odoo 20.0: `upstream/odoo` altında sığ git submodule, sabit commit (`state.json` → `upstream`). Windows'ta `core.longpaths` açık olmalı.
- OCA (T1.11, D-019): resmî 20.0 depoları `vendor/oca/<depo>` altında sığ git submodule (`server-ux`, `server-brand`). 20.0'da olmayan modüllerin portları `ports/oca/<depo>/<modül>` altında, her birinde `PORT.md` (şimdilik `report_xlsx`). Prosedür ARCHITECTURE.md §2.
- CI (T1.10): GitHub Actions (`.github/workflows/ci.yml`), her push'ta. İki iş: belgeler + lint + gizli bilgi + rehber kopyası; PostgreSQL 18 servisiyle modül testleri. Ayrıntı ARCHITECTURE.md §5.

## Komutlar

- Belge denetimi: `python tools/check_docs.py`
- Yeni klonda alt modüller (upstream, vendor): `git -c core.longpaths=true submodule update --init --depth 1`, ardından `git submodule foreach --quiet git config core.longpaths true` (düz `git config` alt modüle geçmez)
- PostgreSQL: `python tools/pg.py start|stop|status` (ilk kurulum: `init`; ikili dosyalar `OV_HOME/pgsql` altında olmalı)
- Adım sonu kayıt: `git add -A` → `git diff --cached` (denetim) → `git commit` (`Co-Authored-By` ve `Claude-Session` yok; pre-commit kancaları çalışır, hata varsa commit olmaz) → `git push`
- Python ortamı: `python -m venv .venv` → `.venv/Scripts/python -m pip install --prefer-binary -r requirements-dev.txt` (upstream güncellenince yeniden çalıştırılır)
- Odoo sürüm kontrolü: `.venv/Scripts/python upstream/odoo/odoo-bin --version`
- Odoo AI rehberleri: `python tools/sync_skills.py` (kopyalar), `python tools/sync_skills.py --check` (upstream'le farkı denetler)
- Yerel yapılandırma: `python tools/odoo_conf.py` (`--force` ile yeniden yazar; `.env`'de `ODOO_ADMIN_PASSWD` yoksa üretir)
- Demo veritabanı: `.venv/Scripts/python upstream/odoo/odoo-bin db -c odoo.conf init ov_demo --with-demo --language tr_TR --country TR` → `.venv/Scripts/python upstream/odoo/odoo-bin -c odoo.conf -d ov_demo -i ov_brand,account,l10n_tr --stop-after-init`
- Sunucu: `.venv/Scripts/python upstream/odoo/odoo-bin -c odoo.conf -d ov_demo` → http://127.0.0.1:8069
- Odoo kabuğu: `.venv/Scripts/python upstream/odoo/odoo-bin shell -c odoo.conf -d ov_demo --no-http` (Türkçe çıktı için `PYTHONIOENCODING=utf-8`)
- Testler (T1.8): `python tools/run_tests.py <modül>[,<modül>…]`
  - Her çalıştırmada temiz test veritabanı (`ov_test_<ilk modül>`, demo yok, `en_US`), modül(ler) testlerle kurulur, varsayılan etiket `/<modül>`.
  - Hedef modüller `ov_brand`'e bağlıysa `ov_brand` önce testsiz kurulur: kurulumu çevrim içi hizmet modüllerini kaldırıyor, Odoo da modül kaldıran çalıştırmada `post_install` testlerini başlatmıyor (T2.3). Onunla gelen hedef modüller (ör. `remove_odoo_enterprise`) ikinci çalıştırmada güncellenir, testleri de çalışır.
  - Etiketli veya tek test: `--tags` Odoo'nun `--test-tags` sözdizimiyle (`[-][etiket][/modül][:Sınıf][.yöntem]`; ör. `--tags /l10n_tr:TestClassName.test_method`, `--tags post_install/l10n_tr`).
  - Hızlı tekrar: `--reuse` (veritabanını korur, `-u` ile günceller). Demo gerekiyorsa `--with-demo` (testler demoya dayanmamalı).
  - Testler kendi HTTP portunu kullanır (8079); geliştirme sunucusu 8069'da açık kalabilir.
  - Çıktı: test sayısı, gerçek hatalar, `RESULT: OK` / `RESULT: FAILED (n)`; çıkış kodu 0/1. Tam günlük `OV_HOME/logs/tests/<db>.log`.
  - Windows'ta Odoo 20.0'ın test sınıflarındaki filestore temizliği hataları (`setUpClass`/`tearDownClass` → `_gc_file_store_unsafe`) ayrı sayılır ve sonucu bozmaz. Referans sonuç Linux CI'dır (T1.10).
  - Windows'ta tarayıcı testleri ara sıra "Session Expired" ile düşebilir. Upstream'in oturum deposu, bir istek oturum dosyasını yeniden yazarken aynı anda okuyan isteğe boş oturum veriyor (Windows'ta dosya değişimi atomik değil). Test tek başına yeniden çalıştırılır (`--reuse --tags`); Linux CI etkilenmez (T2.4).
  - Testlerde raporlar PDF yerine HTML üretir (upstream davranışı). PDF'i zorlayan (`force_report_rendering`) ve motoru taklit etmeyen testler yerelde düşer; PDF denemeleri Linux CI'da (T3.7).
  - Doğrudan Odoo ile: `.venv/Scripts/python upstream/odoo/odoo-bin -c odoo.conf -d <db> -i <modül> --test-enable --test-tags /<modül> --stop-after-init`
- Yeni modül (T1.9): `python tools/new_module.py ov_<ad> [--title …] [--summary …] [--depends base,…] [--license LGPL-3]` → `addons/ov_<ad>/`, ardından `python tools/run_tests.py ov_<ad>`
- Lint (T1.9): `.venv/Scripts/pre-commit run --all-files`
  - Tek tek: `.venv/Scripts/ruff check .` · `.venv/Scripts/pre-commit run pylint_odoo --all-files` · `python tools/check_modules.py`
  - Kurallar: `ruff.toml` (upstream'in kural seti), `.pylintrc` (Odoo'ya özgü denetimler), `tools/check_modules.py` (proje kuralları).
  - Modül içi import mutlak yazılır (`from odoo.addons.<modül>.tools import …`), upstream gibi; ruff TID252 bunu ister. pylint-odoo'nun tersini isteyen `odoo-addons-relative-import` denetimi kanca argümanıyla kapalı.
  - Kanca: yeni klonda bir kez `.venv/Scripts/pre-commit install`. İlk çalıştırma ruff ve pylint-odoo ortamlarını kurar (GitHub ve PyPI).
  - Araç sürümleri `requirements-dev.txt` ve `.pre-commit-config.yaml`'da birlikte güncellenir.
- Gizli bilgi denetimi (T1.10): `python tools/check_secrets.py`. Staged değişikliklerde `.env` değerlerini arar; pre-commit kancası olarak her commit'te çalışır. CI'da gitleaks tüm geçmişi tarar.
- CI (T1.10): `gh run list --limit 5` · başarısız adımların günlüğü `gh run view <id> --log-failed`
  - Linux'ta referans test (ör. upstream modülleri): `gh workflow run ci.yml -f modules=l10n_tr` → `gh run watch <id>`
- OCA portu (T1.11): `python tools/port_oca.py fetch <depo> <modül> [--branch 19.0] [--commit SHA]` → `python tools/port_oca.py upgrade ports/oca/<depo>/<modül>` → elle uyarlama + `python tools/run_tests.py <modül>`
  - Kaynakla fark: `python tools/port_oca.py diff ports/oca/<depo>/<modül> [--stat]`. Adımların tamamı ve kayıtlar: ARCHITECTURE.md §2 "Port prosedürü".
