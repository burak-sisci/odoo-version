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
  - Envanter (T2.1, `research/brand-inventory.md` §4): yayıncı garantisi haftada bir veritabanı kimliğini, kullanıcı sayılarını, kurulu uygulamaları ve şirketin adı, e-postası ve telefonunu şifresiz HTTP ile `services.odoo.com`'a gönderiyor; varsayılan olarak açık.
- **Public depo (D-015):** depodaki her şey herkese açık.
  - Depoya girmeyecekler: gizli bilgi (API anahtarı, şifre, sertifika), müşteri veya test kişisinin gerçek verisi, gerçek VKN/TCKN, yerel yapılandırma (`.env`, `odoo.conf`).
  - Nilvera test portalının test bilgileri kamuya açık bir belgede yayımlanmış olsa da depoya yazılmaz; yalnız `.env`'de tutulur.
  - Yeniden dağıtım izni belirsiz dış dosyalar (ör. GİB UBL-TR XSD/schematron paketleri) depoya konmaz; CI'da kaynağından indirilir (PLAN T4.2).
  - Her commit'te `tools/check_secrets.py` (pre-commit kancası) staged değişikliklerde `.env` değerlerini arar; push'tan önce `git diff --cached` elle de denetlenir.
  - CI'da gitleaks her push'ta tüm geçmişi tarar (T1.10).
- **Depo lisansı (D-016):**
  - Depo kökündeki `LICENSE` GNU AGPL v3 metnidir; aksi belirtilmeyen tüm özgün içerik bu lisansla yayımlanır.
  - Depo ileride private yapılırsa, o güne kadar yayımlanmış sürümler AGPL-3 altında kalır.
  - Dış katkı (pull request) şimdilik kabul edilmez (README "Katkı").

## 5. Lisans envanteri

Projeye giren her dış kod buraya yazılır. Depoya girmeyen ama geliştirme ortamında kullanılan araçlar ayrı tabloda.

| Bileşen | Sürüm/commit | Lisans | Değiştirildi mi? | Nerede |
|---|---|---|---|---|
| Odoo Community | 20.0, commit `afbcf79d` (2026-10-18) | LGPL-3 (`LICENSE`, `COPYRIGHT`) | Hayır (D-010) | `upstream/odoo`, sığ git submodule (T1.4) |
| Odoo AI rehberleri (upstream `skills/`) | 20.0, commit `afbcf79d` | LGPL-3 (klasörde kendi lisans dosyası yok, depo lisansı geçerli; `LICENSE` kopyası yanında) | Hayır; yalnız satır sonu LF'ye çevrildi | `.claude/skills/`, kaynak notu `SOURCE.md` (T1.7, `tools/sync_skills.py`) |
| OCA server-ux (`date_range`) | 20.0, commit `d952d4df` (2026-10-13) | `date_range` LGPL-3 (manifest ve dosya başlıkları); depo `LICENSE` AGPL-3 | Hayır (D-010, D-019) | `vendor/oca/server-ux`, sığ git submodule (T1.11) |
| OCA `report_xlsx` (reporting-engine) | 19.0, commit `b9e8c6cd` (2026-09-23); port sürümü `20.0.1.0.0` | AGPL-3; yazarlar ACSONE SA/NV, Creu Blanca, OCA; telif başlıkları korunuyor | Evet: 20.0 uyarlaması, ayrıntı modüldeki `PORT.md` | `ports/oca/reporting-engine/report_xlsx` (T1.11) |

**Geliştirme ortamı araçları (depoya girmez, ürünle dağıtılmaz):**

| Araç | Sürüm | Lisans | Not |
|---|---|---|---|
| PostgreSQL sunucusu ve komut satırı araçları (EDB Windows ikili zip) | 18.6 | PostgreSQL License (izin verici) | T1.3. Zip içindeki pgAdmin 4 ve StackBuilder kullanılmıyor. |
| ruff | 0.16.10 | MIT | T1.5, `requirements-dev.txt`. Lint; kural seti upstream `ruff.toml`, depodaki `ruff.toml` onu genişletir (T1.9). |
| pylint-odoo | 10.0.12 | AGPL-3.0-or-later | T1.9, `requirements-dev.txt` ve pre-commit. Odoo'ya özgü lint denetimleri. |
| pylint, astroid, pylint-plugin-utils | 4.0.10, 4.0.4, 0.9.0 | GPL-2.0-or-later; astroid LGPL-2.1-or-later | T1.9, pylint-odoo'nun bağımlılıkları. Yalnız geliştirmede çalışır, kodumuza lisans etkisi yok. |
| pre-commit | 4.7.0 | MIT | T1.9, `requirements-dev.txt`. Commit öncesi denetimler; kanca ortamlarını GitHub ve PyPI'dan kurar. |
| gitleaks | 8.30.1 | MIT | T1.10. CI'da gizli bilgi taraması; resmî sürüm arşivi indirilir, SHA-256 doğrulanır. |
| GitHub eylemleri: actions/checkout, actions/setup-python, actions/cache | v7.0.1, v7.0.0, v6.1.0 (commit SHA'sıyla sabit) | MIT | T1.10, `.github/`. |
| PostgreSQL resmî Docker imajı (`postgres:18`) | 18 | PostgreSQL License; imaj betikleri MIT | T1.10. CI'da test veritabanı servisi. |
| websocket-client | 1.9.2 | Apache-2.0 | T1.5, `requirements-dev.txt`. Odoo HttpCase tarayıcı testleri için. |
| Odoo'nun Python bağımlılıkları | upstream `requirements.txt` sürümleri | Çeşitli (çoğu izin verici) | T1.5, `.venv`. Ürünle dağıtılacak paketlerin tam lisans dökümü paketleme görevinde çıkarılır (T8.4). |
