# Nexus — Odoo Community tabanlı ERP

Son güncelleme: 2026-11-05

[![CI](https://github.com/burak-sisci/odoo-version/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/burak-sisci/odoo-version/actions/workflows/ci.yml)

> Ürünün adı **Nexus** (D-014). Depo adı `odoo-version` geçici bir çalışma adıdır; depo kullanıcı onayıyla yeniden adlandırılacak (T8.2).

Odoo Community 20.0 (LGPL-3) üzerine kurulan, **kendi markamızla** ürün ve/veya SaaS olarak satılacak bir ERP.
- Odoo çekirdeği değiştirilmez; her şey ayrı modüllerle eklenir (D-010).
- İlk hedef müşteriler küçük işletmeler ve orta ölçekli fabrikalar (D-017). Bunlar için iki paket hazırlanıyor (D-018):
  - **Ticaret:** cari, satış, satın alma, stok, fatura, e-Fatura / e-Arşiv / e-İrsaliye, çek/senet, banka, raporlar.
  - **Üretim:** Ticaret + üretim, fason, maliyet, kalite, bakım, izlenebilirlik.
- Uzun vadeli hedef, Odoo'daki tüm uygulamaların işlevsel karşılığı. Enterprise'a özel özellikler clean-room yöntemiyle yeniden yazılacak (D-006).

**Durum:** Faz 3 — Türkiye temel yerelleştirmesi. Faz 1 (geliştirme altyapısı) ve Faz 2 (marka katmanı) tamamlandı.
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
- Marka modülleri: `ov_brand` ürün adını (Nexus), simgeleri, giriş ekranını ve hata pencerelerini değiştiriyor (T2.2). `ov_brand_mail` yayıncıya giden haftalık veritabanı raporunu kapatıyor; `ov_brand` yayıncının çevrim içi hizmet modüllerini (IAP, Aboneliğim), Enterprise reklamlarını, dokümantasyon bağlantılarını ve uygulama mağazasını kaldırıyor; `ov_brand_html_editor` metin düzenleyicinin yayıncı hizmetlerini kapatıyor (T2.3). Web istemcisi `/nexus` adresinde (T2.4, K16). E-posta, portal, özet e-postası, fatura ve satın alma portalındaki yayıncı izleri, PDF başlığı ve üst verisi kaldırıldı; bot ürünün adını taşıyor (T2.5).
- Altyapı metinlerindeki eski ürün adı gösterilirken Nexus'la değiştiriliyor; otomatik sızıntı testi kurulu bütün modülleri İngilizce ve Türkçe tarıyor, CI'da MVP uygulamalarıyla çalışıyor (T2.6).
- Kurulumda, zamanlanmış işlerde, testlerde ve ana sayfalarda yayıncının alan adlarına istek gitmediği otomatik testle denetleniyor; CI'da MVP uygulamalarıyla çalışıyor. Marka katmanı (F2) tamamlandı (T2.7).
- Upstream `l10n_tr` (20.0) incelendi: 26 eksik bulundu ve her biri bir göreve bağlandı (`docs/research/l10n-tr.md`, T3.1).
- `ov_l10n_tr` Türk hesap planını düzeltiyor: Türkçe hesap ve vergi adları, eksik Tekdüzen hesapları, kira ve serbest meslek stopajı, Tekdüzen'e bağlı özel hesaplar. Kalıcı test Türkçe adlardaki İngilizce kalıntıları ve büyük harf hatalarını yakalıyor (T3.2).
- `ov_l10n_tr` kimlik numaralarını Türkiye kurallarıyla ele alıyor: TCKN'li iş ortağı gerçek kişi, VKN'li iş ortağı şirket; VKN/TCKN etiketi, yer tutucusu ve hata mesajı Türkçe; MERSİS numarasında 16 hane denetleniyor (T3.3).
- `ov_l10n_tr` adreslere 81 ilin 973 ilçesini ekledi (İçişleri Bakanlığı envanteri): ilçe seçilince il dolar, il seçiliyse liste o ille sınırlı; portal ve e-ticaret formunda da. İl zorunlu, posta kodu isteğe bağlı; adres "34710 Kadıköy/İstanbul" biçiminde (T3.4).
- `ov_l10n_tr_tcmb` Merkez Bankası (TCMB) döviz kurlarını her iş günü kendiliğinden alıyor: kur türü seçilebiliyor (döviz/efektif, alış/satış), kaçırılan günler tamamlanıyor, geçmiş kurlar ayarlardan aktarılıyor (T3.5).
- `ov_i18n_tr` upstream'in Türkçe çevirisindeki eksikleri tamamlıyor, hatalı çevirileri düzeltiyor; kapsam her commit'te ölçülüyor ve CI'da eşikle korunuyor. Paket modüllerinde %81'den %100'e (83 modül, 29.518 terim; kapı ölçütü %95); muhasebe, satış, satın alma, stok, üretim, mesajlaşma, web istemcisinin arayüz metinleri, temel modül (kullanıcılar, erişim yetkileri, şirket, banka), hesap tablosu, ürünler, takvim (müşteriye giden davet e-postaları dahil), metin düzenleyici, e-fatura (UBL/CII), CRM, çevrim içi ödeme, teklif şablonları, müşteri portalı, çalışma takvimleri, satış/satın alma–stok bağlantıları ve stok değerleme tam; faturadaki varsayılan satış koşullarının ve ödeme tahsilatının ("yakalama") bozuk çevirileri düzeltildi, Incoterm her yerde "Teslim Şekli". Formlardaki "Discard" düğmesi artık "Sil" değil "Vazgeç"; hesap tablosundaki "Şal" (Wrap), "Donmak" (Freeze) gibi makine çevirisi hataları düzeltildi; simge seçicide Türkçe arama çalışıyor (T3.6).
- Türk şirketinin belgeleri Türk düzeninde basılıyor (`ov_l10n_tr`, `ov_l10n_tr_sale`, `ov_l10n_tr_stock`): şirket bilgilerinde VKN, MERSİS ve ticaret sicil numarası, web sitesi; faturada müşterinin "VKN: …" / "TCKN: …" satırı; tutar "Yalnız: Binikiyüzotuzdört Türk Lirası Ellialtı Kuruş" biçiminde (upstream'in "Iki" hatası düzeldi); tahsilat ve tediye makbuzu; çıkış transferinde düzenleme ve fiili sevk tarihi ayrı "Sevk İrsaliyesi". PDF motorlarıyla denetim sürüyor (T3.7).
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
