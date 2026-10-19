# PDF Motoru

Son güncelleme: 2026-10-19
Araştırma tarihi: 2026-10-19
İlgili kararlar: D-005, D-007, D-010 (DECISIONS.md); USER_TASKS K18
İlgili görev: T2.5 (PLAN.md); sonuçları kullanan görevler T3.7, T8.4

> **Sonuç (2026-10-19, öneri):** Karar açık (USER_TASKS **K18**). Öneri:
> - Üretimde upstream'in varsayılan motoru **wkhtmltopdf** (0.12.6.1, "patched Qt" paketi).
> - **Paper Muncher** CI'da ikinci motor olarak denenir: T3.7'nin Türkçe belgeleri iki motorla da basılır. 1.0'a ulaşınca ya da upstream varsayılan motor yapınca geçiş yeniden değerlendirilir.
> - Motor seçimi tek bir sistem parametresi. Geri dönüşü kolay; şimdilik kurulu bir şey yok.
> - Yerel geliştirme ortamında (Windows) motor yok. PDF denemeleri Linux CI'da (T3.7).

## 1. Soru

Odoo 20.0'da PDF raporları (fatura, teklif, irsaliye) harici bir program üretir. Hangi motorla çalışacağız?

Ölçütler:
- bakım: güvenlik ve hata düzeltmesi alıyor mu;
- upstream uyumu: Odoo 20.0'ın varsayılanı ve testleri;
- olgunluk: üretimde müşteri belgesi basmaya hazır mı;
- platform: sunucu Linux; işlemci mimarisi henüz belli değil (D-013, barındırma kararı ertelendi);
- lisans (D-008) ve maliyet (D-005).

## 2. Upstream 20.0'daki durum

Kaynak: `upstream/odoo` (commit `state.json` → `upstream`).
- Motor eklentili. Çekirdekte `ir.actions.report._get_pdf_engine`:
  - raporun türü `qweb-pdf-<motor>` ise o motor;
  - değilse `report.pdf_engine_default` sistem parametresi.
- `base_report_wkhtmltox` (LGPL-3): **kendiliğinden kurulur**. Kurulunca parametreyi `wkhtmltopdf` yapar. wkhtmltopdf ≥ 0.12.0 ister; 0.12.2 ve sonrasında ek özellikler açılır.
- `base_report_paper_muncher` (LGPL-3): kendiliğinden kurulmaz.
  - Rapor türü `qweb-pdf-paper-muncher` ekler.
  - paper-muncher ≥ 0.6 ister. İkili dosyayı `PATH`'te, yoksa `/opt/paper-muncher/bin/paper-muncher` altında arar.
  - Görsel çıktısını da (`_run_image_engine`) kendisi üretebiliyor.
- Testlerde rapor, PDF yerine HTML üretir (`force_report_rendering` bağlamı yoksa). Testler motor olmadan da çalışır.
- PDF üst verisi motordan bağımsız. Sunucu birden çok kaydı bölüp birleştirdiğinde dosyayı yeniden yazar ve üretici adını koyar. `ov_brand` bu adı marka adıyla değiştirir (T2.5). Tek kayıtlık PDF'te motorun kendi üst verisi kalır; motorlar CI'a T3.7'de girdiği için orada iki motorla da denetlenir.

## 3. Motorlar

| | wkhtmltopdf | Paper Muncher |
|---|---|---|
| Geliştiren | Topluluk (wkhtmltopdf projesi) | Odoo S.A. |
| Lisans | LGPL-3 | LGPL-3 |
| Bakım | Depo **arşivde** (son push 2022-11-22). Paket deposu da arşivde; son sürüm 0.12.6.1-3 (2023-05-22) | Etkin. 0.5.0 (2026-06-23) → 0.9.0 (2026-10-06), yaklaşık ayda bir sürüm |
| Olgunluk | On yılı aşkın üretim kullanımı; bilinen tuhaflıkları belgelenmiş | Kendi tanımı "early alpha"; derleme bölümünde "henüz kullanıma hazır değil" uyarısı |
| Motor | Eski Qt WebKit | Kendi HTML/CSS motoru (C++) |
| Paketler | Linux: amd64, arm64, i386, ppc64el (bookworm, jammy …). Windows ve macOS da var | Yalnız Linux **amd64**: Debian bookworm, trixie; Ubuntu jammy, noble, plucky, resolute; genel tar.gz |
| Upstream 20.0'daki yeri | Varsayılan, kendiliğinden kurulur | Seçimlik |
| Bilinen eksi | Güvenlik düzeltmesi almıyor; modern CSS desteği zayıf | Kararlılık ve CSS uyumu hâlâ gelişiyor; arm64 paketi yok |

Kaynaklar (erişim 2026-10-19):
- https://github.com/wkhtmltopdf/wkhtmltopdf — GitHub API: `archived: true`, son push 2022-11-22.
- https://github.com/wkhtmltopdf/packaging/releases — 0.12.6.1-3, mimari listesi.
- https://github.com/odoo/paper-muncher — GitHub API: LGPL-3.0, arşivde değil; README "Status" ve "Building" bölümleri; 0.9.0 sürüm dosyaları.
- https://odoo.github.io/paper-muncher/ — proje sitesi.
- İkincil: https://www.nalios.com/en/blog/what-s-new-in-odoo-6/odoo-19-papermuncher-odoo-s-next-generation-pdf-engine-117 (Paper Muncher'ın 19.0'da gelişi).

## 4. Değerlendirme

- **Bugün müşteri belgesi için:** wkhtmltopdf. Upstream'in varsayılanı; 20.0'ın rapor şablonları ve testleri onunla yazılıyor. Paper Muncher'ın kendi belgesi "erken alfa" diyor; fatura gibi resmî bir belgede yazım hatası müşteri kaybı demek (R15).
- **Uzun vadede:** Paper Muncher. Odoo S.A. geliştiriyor; wkhtmltopdf'in yerine yazıldığını açıkça söylüyor. wkhtmltopdf'in güvenlik düzeltmesi almaması zamanla risk.
  - Azaltma: motor yalnız sunucunun ürettiği HTML'i işler, dışarıdan erişilemez. Kullanıcı içeriği (ör. notlardaki görsel adresleri) bu HTML'e girebildiği için sunucunun dış ağa çıkışını sınırlamak T8.4'te değerlendirilir.
- **Mimari:** Paper Muncher yalnız amd64. Barındırma kararı (D-013) arm64 bir sunucuya (ör. ücretsiz bulut katmanlarının ARM makineleri) giderse Paper Muncher'ı kaynaktan derlemek gerekir. wkhtmltopdf'in arm64 paketi var.
- **Ubuntu 24.04 (noble):** wkhtmltopdf paket deposunda noble paketi yok. jammy paketinin noble'da kurulup kurulmadığı T8.4'te denenir; olmazsa bookworm tabanlı kapsayıcı.
- **Windows:** iki motorun da yerelde kurulumu gerekmiyor. Yerel testler HTML'le çalışır; PDF'e bakan testler Linux CI'da (T3.7).

## 5. Öneri (K18)

- **A (öneri):** üretimde wkhtmltopdf. Paper Muncher CI'da ikinci motor; T3.7'nin belgeleri iki motorla da basılıp karşılaştırılır. Geçiş ölçütü: Paper Muncher 1.0 ya da upstream'in varsayılanı yapması, ve T3.7 belgelerinin onunla doğru çıkması.
- **B:** hemen Paper Muncher. Bakımı süren tek seçenek, ama "erken alfa" ve yalnız amd64.
- **C:** ikisi birden: belge türüne göre (rapor türü `qweb-pdf-paper-muncher`). Bakım yükü artar; bugün gerekçesi yok.

Uygulama yeri:
- T3.7: CI'a iki motorun kurulumu, belgelerin PDF testleri.
- T8.4: kurulum aracı seçilen motoru kurar; Paper Muncher seçilirse sunucunun amd64 olduğunu denetler.
- T2.6: sızıntı taraması sunucunun yazdığı PDF üst verisini kapsar; motorun kendi üst verisi T3.7'de.
