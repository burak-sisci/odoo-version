# B ve C Yaklaşımlarının Karşılaştırması

Son güncelleme: 2026-10-18
İlgili karar: D-010 (DECISIONS.md)

> **Sonuç (2026-10-18):** Kullanıcı **B**'yi seçti (D-010 Geçerli). Aşağıdaki B+ önerisi kabul edilmedi.
> Çekirdekte hiçbir dosya değiştirilmez. "Zor noktalar" (ör. `/odoo` URL yolu) modül düzeyinde çözülecek: controller override ve asset paketinde dosya değiştirme (`replace`) (ROADMAP T2.4).
> Modülle çözülemeyen bir nokta çıkarsa kullanıcıya yeni karar olarak getirilecek.

## Tanımlar

- **B — Dağıtım (distribution) modeli:** Odoo Community çekirdeği **hiç değiştirilmeden**, belirli bir commit'e sabitlenmiş olarak kullanılır.
  Ürünü oluşturan her şey (marka, Türkiye uyumu, Enterprise eşdeğerleri, SaaS yönetimi) **ayrı modüller** olarak yazılır.
- **C — Çatal (fork) modeli:** Odoo Community deposu kopyalanır, **çekirdek kodun içi** doğrudan değiştirilir
  (marka, URL'ler, davranışlar). Upstream'deki değişiklikler düzenli olarak çatala birleştirilir (merge).
- **B+ (önerilen ara yol):** B'nin aynısı. Tek fark: modül düzeyinde çözülemeyen nadir durumlar için,
  her biri belgelenmiş ve otomatik uygulanan küçük bir **yama kuyruğu** (`patches/`) tutulur. Her yama için DECISIONS.md'de ayrı bir karar kaydı açılır.

## Karşılaştırma

| Konu | B (dağıtım) | C (çatal) |
|---|---|---|
| Güvenlik/hata düzeltmelerini almak | Sabit commit ilerletilir + testler. Çakışma yok | Her birleştirmede değiştirilmiş dosyalarda çakışma. Upstream 20.0 dalı her gün commit alıyor |
| Yıllık ana sürüm geçişi | Yalnız kendi modüllerimiz taşınır (`odoo-bin upgrade_code` yardımcı) | Modüllerin yanında **tüm çekirdek değişiklikleri** de yeni sürüme yeniden uygulanır |
| Yeniden markalama derinliği | Kullanıcının gördüğü yerlerin büyük çoğunluğu modülle değişir (QWeb kalıtımı, JS `patch()`, çeviri geçersiz kılma, controller override). Zor noktalar: `/odoo` URL yolu, HTML/asset adlarındaki teknik izler, `odoo` Python paketi | %100. Her şey değiştirilebilir |
| Çekirdek davranış değişikliği | ORM kalıtımı ve override'larla çok geniş; nadiren monkey-patch gerekir | Sınırsız |
| OCA ve 3. parti modül uyumu | Tam uyumlu | Paket adı `odoo` değiştirilirse ekosistem kırılır (yalnız Community'de 5.984 Python dosyası `odoo`'yu içe aktarıyor); değiştirilmezse çatalın kazancı azalır |
| Lisans yükümlülükleri | Çekirdek değişmediği için yalnız lisans/telif notlarını korumak gerekir. Kendi modüllerimiz kapalı kaynak olabilir | Değiştirilmiş çekirdek LGPL-3 kalır. Müşteriye kurulum olarak **dağıtılırsa**, değişikliklerin kaynak kodu verilmelidir (SaaS'ta LGPL'in ağ maddesi yok). Ayrı modüllerimiz yine kapalı olabilir |
| Bakım yükü (1 kişi + Claude) | Düşük, zamanla sabit | Yüksek, her yıl birikerek artar |
| Gerçek dünya örneği | Odoo partnerlerinin ve dikey çözüm sağlayıcılarının çoğu bu modelle çalışır | Flectra (Ekim 2017'de Odoo 11'den çatallandı). Odoo S.A. Enterprise kodunun kopyalandığı iddiasıyla DMCA bildirimi ve dava açtı; ihtiyati tedbir sonrası 2018'de uzlaşmayla kapandı (Odoo'nun anlatımı). Bu dava çatal modelinden değil Enterprise kopyalamadan doğdu, ama upstream'den kopan çatalın riskini gösteriyor |
| Farklılaşma | Fark bizim modüllerimizden gelir (Türkiye uyumu, Enterprise eşdeğerleri, SaaS hizmeti) | Aynı. Çekirdek değişikliği tek başına müşteriye değer katmaz |
| Müşteri algısı | Teknik bir göz ürünün Odoo tabanlı olduğunu anlayabilir (yasal olarak sorun değil) | Daha iyi gizlenir, ama kod incelemesi yine gösterir |

## Değerlendirme

- Ürünün değeri çekirdekte değil, üzerine eklediğimiz katmanlarda.
- Tek kişi + AI ekip için yıllık birleştirme yükü C'nin en büyük maliyeti ve her yıl büyüyor.
- C'nin tek gerçek avantajı (%100 markalama), B+'nın yama kuyruğuyla ihtiyaç duyulan noktalarda karşılanabilir.

**Claude'un o tarihteki önerisi: B+.** Çekirdek varsayılan olarak hiç değiştirilmez; yalnız modülle çözülemeyen ve belgelenmiş noktalarda küçük yamalar (hedef: 10'dan az). Karar B oldu (yukarıdaki "Sonuç" notu).

## Kaynaklar

- Kod incelemesi: `docs/research/odoo-analysis.md` §7
- https://www.odoo.com/ar/page/flectra-vs-odoo-flectrahq-enterprise (Odoo'nun kendi anlatımı — taraf kaynak)
- https://community.nethserver.org/t/flectra-hq-open-source-fork-of-odoo-11/8609
- https://www.gnu.org/licenses/lgpl-3.0.html
