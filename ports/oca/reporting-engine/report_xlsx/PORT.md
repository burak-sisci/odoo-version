# Port notu: report_xlsx

Son güncelleme: 2026-10-18

OCA modülü `report_xlsx`'in Odoo 20.0'a taşınmış kopyası (D-019, ARCHITECTURE.md §2 "OCA port düzeni").
Teknik ad, lisans, yazarlar ve telif notları değiştirilmez. OCA resmî 20.0 sürümünü yayımlayınca
port silinir ve modül `vendor/oca/reporting-engine` altından kullanılır.

| Alan | Değer |
|---|---|
| Kaynak depo | https://github.com/OCA/reporting-engine |
| Kaynak dal | 19.0 |
| Kaynak commit | b9e8c6cdd2d106614eddaf81bd78f487ae35db45 (2026-09-23) |
| Lisans | AGPL-3 |
| Yazarlar | ACSONE SA/NV,Creu Blanca,Odoo Community Association (OCA) |

## Değişiklikler

Kaynakla farkın tamamı: `python tools/port_oca.py diff ports/oca/reporting-engine/report_xlsx`

- Manifest sürümü `19.0.1.0.2` → `20.0.1.0.0`, OCA taşıma kuralı (`port_oca.py fetch`).
- Odoo `upgrade_code` betikleri, 19.0 sonrası ve Owl 3 (`port_oca.py upgrade`): değişiklik yok.
