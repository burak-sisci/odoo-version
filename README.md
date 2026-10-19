# Nexus — Odoo Community tabanlı ERP

Son güncelleme: 2026-10-19

[![CI](https://github.com/burak-sisci/odoo-version/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/burak-sisci/odoo-version/actions/workflows/ci.yml)

> Ürünün adı **Nexus** (D-014). Depo adı `odoo-version` geçici bir çalışma adıdır; depo kullanıcı onayıyla yeniden adlandırılacak (T8.2).

Odoo Community 20.0 (LGPL-3) üzerine kurulan, **kendi markamızla** ürün ve/veya SaaS olarak satılacak bir ERP.
- Odoo çekirdeği değiştirilmez; her şey ayrı modüllerle eklenir (D-010).
- İlk hedef müşteriler küçük işletmeler ve orta ölçekli fabrikalar (D-017). Bunlar için iki paket hazırlanıyor (D-018):
  - **Ticaret:** cari, satış, satın alma, stok, fatura, e-Fatura / e-Arşiv / e-İrsaliye, çek/senet, banka, raporlar.
  - **Üretim:** Ticaret + üretim, fason, maliyet, kalite, bakım, izlenebilirlik.
- Uzun vadeli hedef, Odoo'daki tüm uygulamaların işlevsel karşılığı. Enterprise'a özel özellikler clean-room yöntemiyle yeniden yazılacak (D-006).

**Durum:** Faz 2 — Marka katmanı. Faz 1 (geliştirme altyapısı) tamamlandı.
- Planlama tamamlandı: [PLAN.md](PLAN.md) (ilerleme panosu, fazlar, görevler, müşteri arayışı kapısı).
- Görevler üç kategoride: kullanıcının yapacakları, birlikte yapılacaklar, Claude'un yapacakları (D-021).
- Sürüm doğrulandı: 20.0'da kalınıyor (T1.2, `docs/research/nilvera-port.md`).
- Upstream Odoo 20.0 projeye eklendi (`upstream/odoo`, T1.4).
- Python geliştirme ortamı hazır (`.venv`, `requirements-dev.txt`, T1.5).
- Odoo yerelde çalışıyor: Türkçe arayüz, `l10n_tr` ve Türk hesap planlı demo şirketi (T1.6).
- Odoo'nun AI rehberleri kuruldu (`.claude/skills/`, T1.7).
- Test komutu hazır (`tools/run_tests.py`, T1.8).
- Modül şablonu ve kod kalite araçları hazır (`tools/new_module.py`, ruff, pylint-odoo, pre-commit; T1.9).
- CI çalışıyor: her push'ta belge denetimi, lint, gizli bilgi taraması ve modül testleri (GitHub Actions, T1.10).
- OCA düzeni hazır: resmî 20.0 depoları `vendor/oca/`, bizim 20.0 portlarımız `ports/oca/` (`tools/port_oca.py`, T1.11). İlk port: `report_xlsx`.
- Kullanıcıya görünen Odoo izlerinin envanteri çıkarıldı (`docs/research/brand-inventory.md`, T2.1).
- İlk ürün modülü: marka modülü `ov_brand`. Ürün adı Nexus, simgeler, giriş ekranı, hata pencereleri (T2.2).
- Sıradaki görev: odoo.com bağlantılarının kesilmesi (T2.3).
- Açık karar yok.

## Belgeler

- [PLAN.md](PLAN.md) — plan ve ilerleme (buradan takip edilir)
- [USER_TASKS.md](USER_TASKS.md) — kullanıcıdan beklenenler (eylemler, kararlar, onaylar)
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
