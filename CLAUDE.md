# CLAUDE.md

Son güncelleme: 2026-10-18

Bu dosya, bu projede çalışan Claude (ve diğer AI ajanları) için çalışma talimatıdır. Belgeler Türkçe, kod İngilizce (D-009).

## Proje

Odoo Community tabanlı, **kendi markamızla müşterilere satılacak** bir ERP (ürün ve/veya SaaS).
- Hedef: Odoo'daki tüm uygulamaların (Community + Enterprise) işlevsel karşılığı (D-001, D-002).
- Temel: Odoo 20.0 Community, çekirdeğe dokunmadan yalnız modüllerle (D-010 B, D-011).
- Çalışma adı `odoo-version` (geçici), modül öneki `ov_` (kalıcı) (D-014).
- Ekip: kullanıcı (ürün sahibi, karar mercii) + Claude (çoğunlukla otonom geliştirici) (D-003).
- Bütçe: sıfır (D-005).
- Depo: https://github.com/burak-sisci/odoo-version — **public** (D-015).

**Şu anki durum, aktif görev ve bekleyen kararlar için önce `state.json` dosyasını oku.**

## Belge haritası (her bilginin tek bir yeri vardır)

| Belge | İçerik | Ne zaman güncellenir |
|---|---|---|
| `state.json` | Makine okunur anlık durum: faz, aktif görev, biten görevler, bekleyen kararlar, ortam, modüller | **Her adımda** |
| `CHANGELOG.md` | Tarihli adım kaydı; değişen kararların eski hali ve nedeni | **Her adımda** |
| `DECISIONS.md` | Yalnız **Geçerli**, **Açık** ve **Ertelendi** durumundaki kararlar | Karar alındığında/değiştiğinde |
| `ROADMAP.md` | Fazlar ve görevler (`T<faz>.<sıra>`), durum işaretleri | Görev başladığında/bittiğinde |
| `ARCHITECTURE.md` | Hedef/gerçek mimari, depo yerleşimi, katmanlar, çalışma zamanı | Yapı veya mimari değiştiğinde |
| `docs/MODULE_MATRIX.md` | Tüm uygulamaların edinme yolu, önceliği, durumu | Modül planı/durumu değiştiğinde |
| `docs/COMPLIANCE.md` | Lisans, clean-room, marka, KVKK; **lisans envanteri** | Dış kod eklendiğinde, hukuki bulguda |
| `docs/specs/<modül>.md` | Enterprise eşdeğerleri için clean-room işlev tanımı | Modül geliştirmeden önce |
| `docs/research/*.md` | Tarihli araştırma kayıtları (kaynaklı) | Bulgu yeniden doğrulandığında/değiştiğinde |
| `README.md` | İnsanlar için kısa genel bakış | Durum özeti değiştiğinde |
| `CLAUDE.md` | Bu dosya: kurallar, protokol, komutlar | Kural, komut veya ortam değiştiğinde |

## Belge güncelleme protokolü (ZORUNLU — D-004)

Kullanıcı için kritik: **eski bir kararın herhangi bir belgede kalması veya yeni bir kararın eklenmemesi kabul edilemez.**

Her adımın (görev, karar, araştırma, kod değişikliği) sonunda, kullanıcıya "bitti" demeden **önce**:

1. `state.json`: `last_updated`, `current_task`, `tasks_done`, `blocked_on_user`, `next_actions`, `decisions`, `environment`, `modules`.
2. `CHANGELOG.md`: bugünün tarih başlığı altında ne yapıldığı. Karar değiştiyse **eski metin + neden**.
3. Karar alındı/değişti ise:
   - `DECISIONS.md` kaydı **yerinde** yeniden yazılır (ID değişmez, Durum güncellenir, özet tablo güncellenir).
   - Kararın geçtiği **tüm** belgeler aranıp güncellenir: `grep -rn "D-0xx"` ve konuyla ilgili anahtar kelimeler (ör. sürüm numarası, yaklaşım adı). Özellikle ARCHITECTURE.md başındaki "Durum" notu, MODULE_MATRIX.md, ROADMAP.md, README.md, ilgili `docs/research/*.md` başındaki "Sonuç" notu.
   - Bir görev tamamlandığında, o göreve `**Karar noktası:**` veya `**Yeniden değerlendirme:**` ile bağlı kararlar da ele alınır ve güncellenir.
4. Etkilenen diğer belgeler: yukarıdaki haritaya göre.
5. Her güncellenen Markdown belgesinde `Son güncelleme:` tarihi değiştirilir.
6. `python tools/check_docs.py` çalıştırılır. **Hata varsa adım bitmemiştir.**
7. Commit ve push (D-015):
   - kod ve belgeler **aynı commit'te**;
   - push öncesi `git diff --cached` ile gizli bilgi ve müşteri verisi denetimi;
   - ardından `git push`. Bu push önceden onaylıdır; force-push yasaktır.

Denetim aracının yakalayamadıkları (elle kontrol et):
- Belgelerin içindeki serbest metin çelişkileri (ör. ARCHITECTURE.md'de eski sürüm numarası).
- Açık bir kararın sonucunu "kesinleşmiş" gibi yazmak. Açık kararlar her yerde "öneri" olarak anılır.
- Görev numaraları değişirse eski numaraya yapılan atıfların anlamı. Araç yalnız atıf yapılan görevin var olup olmadığını denetler.

## Değişmez kurallar

1. **Clean-room (D-006):** Odoo Enterprise kodu, sızıntıları, Enterprise deneme/SaaS örneklerinden gelen JS/CSS/görseller **asla** kullanılmaz ve açılıp incelenmez. İzinli/yasak kaynaklar: `docs/COMPLIANCE.md` §2. Emin değilsen dur ve kullanıcıya sor.
2. **Marka (D-007, D-014):** Kullanıcıya görünen hiçbir yerde "Odoo" adı/logosu ürün adı olarak kullanılmaz. Lisans ve telif başlıkları silinmez. Çalışma adı `odoo-version` dış demoya, pilota veya müşteriye çıkmaz.
3. **Lisans (D-008, D-016):** LGPL'den türetilen kod LGPL kalır. Kapalı kaynak modüllerimiz AGPL modüllere bağımlı olamaz. Projeye giren her dış kod `docs/COMPLIANCE.md` §5 lisans envanterine yazılır. Kendi modüllerimizin lisansı D-016 ile belirlenmeden ilk modül (T2.2) yazılmaz.
4. **Upstream'e dokunma (D-010):** `upstream/` ve `vendor/` altı hiçbir koşulda düzenlenmez, yama kuyruğu yoktur. Modülle çözülemeyen durumda dur ve kullanıcıya yeni karar olarak getir.
5. **Para ve dış dünya (D-003, D-005, D-015):**
   - Önce kullanıcı onayı gerekenler: ücretli servis/altyapı, yayınlama/paylaşma, depo ayarları (görünürlük, ad, release).
   - Proje deposuna her adım sonunda push önceden onaylıdır.
6. **Açık ve ertelenmiş kararlar:** bir karar açıkken veya ertelenmişken o karara bağlı, geri dönüşü zor işler yapılmaz. Karar noktası görevine gelince önce karar alınır.
7. **Gizli bilgiler:** depo public. API anahtarları, şifreler, müşteri verisi, yerel yapılandırma (`.env`, `odoo.conf`) depoya girmez (`.gitignore`).

## Odoo geliştirme kuralları

- Modül öneki `ov_` (D-014). Örnek: `ov_brand`, `ov_l10n_tr_edi`.
- Odoo kalıplarını izle:
  - model genişletme `_inherit` ile, görünüm kalıtımı XPath ile;
  - JS'te `patch()`, asset paketinde `replace`;
  - yetkiler `ir.access.csv` ile (20.0 yetki modeli).
- Odoo 20 deposu `skills/` klasöründe resmi AI rehberleri içerir (`odoo-guidelines`, `odoo-review`, `odoo-security`, `odoo-web-guidelines`, `odoo-git`). T1.6'da `.claude/skills/` altına kurulacak. Kurulunca kod yazarken ve incelerken bunlara uy.
- Her modülde: manifest'te doğru `license`, testler (`tests/`), Türkçe çeviri (`i18n/tr.po`).

## Ortam

- Windows 11 Pro. Kabuk: PowerShell 5.1 (birincil) ve Git Bash.
- Kurulu: Python 3.12.10, Git 2.56.0, GitHub CLI 2.101.0 (oturum açık).
- Kurulu değil: PostgreSQL (T1.2'de kurulacak), Node.js, Docker (zorunlu değil).
- Git deposu: varsayılan dal `main`, uzak depo `origin` = GitHub.
- Upstream Odoo henüz projede değil (T1.3).

## Komutlar

- Belge denetimi: `python tools/check_docs.py`
- Adım sonu kayıt: `git add -A` → `git diff --cached` (denetim) → `git commit` → `git push`
- Odoo çalıştırma ve test komutları: henüz yok, T1.5 / T1.7'de buraya eklenecek.
