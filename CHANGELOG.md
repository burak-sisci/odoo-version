# Değişiklik Günlüğü

Son güncelleme: 2026-10-18

Her adımın kaydı en üste, tarih başlığıyla eklenir. Bir karar değiştiğinde **eski metni ve değişiklik nedeni** buraya yazılır (DECISIONS.md yalnız güncel hali tutar).
Kategoriler: **Kararlar**, **Belgeler**, **Kod**, **Ortam**, **Araştırma**.

## 2026-10-18

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
