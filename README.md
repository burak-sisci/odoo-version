# odoo-version — Odoo Community tabanlı markalı ERP

Son güncelleme: 2026-10-18

> `odoo-version` geçici bir çalışma adıdır. Ürünün kalıcı adı MVP sonunda belirlenecek (D-014).

Odoo Community 20.0 (LGPL-3) üzerine kurulan, **kendi markamızla** ürün ve/veya SaaS olarak satılacak bir ERP.
- Odoo çekirdeği değiştirilmez; her şey ayrı modüllerle eklenir (D-010).
- İlk hedef müşteriler küçük işletmeler ve orta ölçekli fabrikalar (D-017). Bunlar için iki paket hazırlanıyor (D-018):
  - **Ticaret:** cari, satış, satın alma, stok, fatura, e-Fatura / e-Arşiv / e-İrsaliye, çek/senet, banka, raporlar.
  - **Üretim:** Ticaret + üretim, fason, maliyet, kalite, bakım, izlenebilirlik.
- Uzun vadeli hedef, Odoo'daki tüm uygulamaların işlevsel karşılığı. Enterprise'a özel özellikler clean-room yöntemiyle yeniden yazılacak (D-006).

**Durum:** Faz 1 — Geliştirme altyapısı.
- Planlama tamamlandı: [PLAN.md](PLAN.md) (ilerleme panosu, fazlar, görevler, müşteri arayışı kapısı).
- Sıradaki görev: sürüm doğrulaması (T1.2), ardından geliştirme ortamı ve CI.
- Açık karar yok. Henüz kod yok.

## Belgeler

- [PLAN.md](PLAN.md) — plan ve ilerleme (buradan takip edilir)
- [state.json](state.json) — anlık durum (makine okunur)
- [DECISIONS.md](DECISIONS.md) — geçerli ve ertelenmiş kararlar
- [ARCHITECTURE.md](ARCHITECTURE.md) — mimari
- [CHANGELOG.md](CHANGELOG.md) — değişiklik günlüğü
- [docs/MODULE_MATRIX.md](docs/MODULE_MATRIX.md) — tüm uygulamaların planı
- [docs/COMPLIANCE.md](docs/COMPLIANCE.md) — lisans, marka, hukuki uyum
- [docs/research/](docs/research/) — araştırma kayıtları
- [CLAUDE.md](CLAUDE.md) — AI ajanı çalışma talimatı

## Lisans

- Bu depodaki özgün kod **GNU Affero General Public License v3.0** ile lisanslıdır: [LICENSE](LICENSE) (D-016).
- İstisnalar:
  - LGPL-3 koddan türetilen modüller LGPL-3 kalır (ör. 19.0 Odoo LGPL Türkiye e-Belge modüllerinin portları). Bu modüllerin manifestinde `LGPL-3` yazar.
  - OCA'dan taşınan modüller kendi orijinal lisanslarını korur.
  - Odoo Community (`upstream/`) LGPL-3'tür; telif sahibi Odoo S.A.'dır.
- "Odoo" Odoo S.A.'nın markasıdır. Bu proje Odoo S.A. ile bağlantılı değildir.

## Katkı

Şu an dış katkı (pull request) kabul edilmiyor (D-016). Hata ve öneriler için issue açılabilir.
