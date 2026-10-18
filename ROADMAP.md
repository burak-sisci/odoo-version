# Yol Haritası

Son güncelleme: 2026-10-18

İşaretler: `[x]` tamam · `[ ]` yapılacak · `[~]` devam ediyor · `[!]` kullanıcı kararı bekliyor
Görev ID'leri (`T<faz>.<sıra>`) `state.json` ve `DECISIONS.md` içinde kullanılır.

## Faz 0 — Araştırma ve planlama `[~]`

- [x] T0.1 Odoo kaynak kodu (20.0) ve dokümantasyonunun incelenmesi — `docs/research/odoo-analysis.md`
- [x] T0.2 Lisans, marka, Community/Enterprise farkları — `docs/COMPLIANCE.md`
- [x] T0.3 B / C yaklaşım karşılaştırması — `docs/research/approach-b-vs-c.md`
- [x] T0.4 e-Fatura / e-Arşiv mevzuat araştırması — `docs/research/e-fatura.md`
- [x] T0.5 Barındırma seçenekleri — `docs/research/hosting.md`
- [x] T0.6 Proje belgelerinin ve belge denetim aracının oluşturulması
- [x] T0.7 Açık kararların (D-010 … D-015) kullanıcıyla netleştirilmesi
- [ ] T0.8 Detaylı planlama (kullanıcıyla): MVP tanımı ve kapsamı, fazların ve görevlerin ayrıntılandırılması

## Faz 1 — Geliştirme ortamı `[~]`

- [x] T1.1 Git deposu ve GitHub public depo (D-015)
- [ ] T1.2 PostgreSQL 16+ kurulumu (Windows, ücretsiz)
- [ ] T1.3 Upstream Odoo 20.0'ın (D-011) sabit commit ile `upstream/odoo` altına eklenmesi (git submodule) + lisans envanteri
- [ ] T1.4 Python sanal ortamı ve bağımlılıklar
- [ ] T1.5 Odoo'nun yerelde çalıştırılması; Türkçe dil + `l10n_tr` ile demo veritabanı
- [ ] T1.6 Odoo `skills/` klasörünün `.claude/skills/` altına kurulması
- [ ] T1.7 Test çalıştırma komutlarının CLAUDE.md'ye yazılması

## Faz 2 — Marka katmanı `[ ]` (D-016 kararı T2.2'den önce gerekli)

- [ ] T2.1 Kullanıcıya görünen Odoo marka izlerinin tam envanteri
- [ ] T2.2 Marka modülü (`ov_brand`): ad, logo, favicon, başlıklar, giriş ekranı, e-posta/rapor/web sitesi altbilgileri, PWA manifest, kullanıcı menüsü
- [ ] T2.3 odoo.com bağlantılarının kapatılması: yayıncı garantisi, IAP servisleri, dokümantasyon/destek bağlantıları
- [ ] T2.4 `/odoo` URL yolu için modül düzeyinde çözüm (controller override + asset `replace`). Modülle çözülemezse kullanıcıya yeni karar (D-010)

## Faz 3 — Türkiye e-Belge katmanı `[ ]`

- [ ] T3.1 19.0 Nilvera LGPL modüllerinin analizi ve 20.0 port planı
- [ ] T3.2 Entegratörden bağımsız e-Belge çekirdeği (UBL-TR, senaryolar, fatura tipleri, mükellef sorgulama, durum takibi)
- [ ] T3.3 Nilvera adaptörü (test ortamı `apitest.nilvera.com`; test hesabı koşulları doğrulanacak)
- [ ] T3.4 e-Arşiv akışları (iptal dahil)
- [ ] T3.5 e-İrsaliye (MVP sonrası, P1)
- [ ] T3.6 Türk SMS sağlayıcısı adaptörü (IAP SMS yerine, P1)

## Faz 4 — Enterprise eşdeğerleri `[ ]`

Öncelik sırası ve durum `docs/MODULE_MATRIX.md` §C'de tutulur. Her modül için önce `docs/specs/<modül>.md` (clean-room işlev tanımı) yazılır.

- [ ] T4.1 P1 muhasebe paketi: banka mutabakatı, mali raporlar, sabit kıymet
- [ ] T4.2 P2 paketi: bütçe, onaylar, helpdesk, dokümanlar, barkod, abonelik, PWA
- [ ] T4.3 P3 paketi
- [ ] T4.4 P4 paketi

## Faz 5 — SaaS altyapısı `[ ]`

Sağlayıcıdan bağımsız kurulur (D-013 kısıtı). Barındırma yeri bu fazı beklemez.

- [ ] T5.1 Çok kiracılı yapı (veritabanı başına kiracı, `dbfilter`, alt alan adları, wildcard TLS)
- [ ] T5.2 Kiracı yaşam döngüsü: oluşturma, askıya alma, silme
- [ ] T5.3 Yedekleme ve geri yükleme (veritabanı + filestore)
- [ ] T5.4 İzleme ve günlükler
- [ ] T5.5 Abonelik ve tahsilat (`payment_iyzico`)
- [ ] T5.6 Ana sürüm yükseltme hattı (OpenUpgrade + hazırlık ortamı)

## Faz 6 — MVP sonu, pilot ve yayına alma `[ ]`

- [ ] T6.1 MVP sonu değerlendirmesi (kullanıcıyla): e-Belge gönderim yöntemi (D-012), kalıcı marka adı ve yeniden adlandırma (D-014)
- [ ] T6.2 Hukuki inceleme (avukat + mali müşavir): lisanslar, marka, KVKK, e-Belge, müşteri sözleşmeleri
- [ ] T6.3 Üretim barındırma kararı (D-013) ve üretim sunucusu (maliyet ilk gelirden)
- [ ] T6.4 İlk pilot müşteri
