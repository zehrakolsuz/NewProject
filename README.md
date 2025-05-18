# 🕵️ Malware Davranış ve İz Analizi Aracı

Bu proje, Eric Zimmerman araçları ile toplanan adli verilerin analiz edilmesi ve basit bir HTML dashboard ile raporlanmasını hedefler.

## 👥 Ekip Üyeleri ve Görev Dağılımı

### 🔍 Zehra Kolsuz – MFT & Amcache Analizi
- `scripts/mft_parser.py`
- `scripts/amcache_parser.py`
- `scripts/file_activity_combiner.py`

### 🧠 [Sena Zorver](https://github.com/SenaZorver)– Event Log & Sysmon Analizi
- `scripts/event_log_parser.py`
- `scripts/behavior_score.py`
- `scripts/user_session_mapper.py`

### 📊 [Emir Keçeli](https://github.com/EmirKeceli) – Raporlama & Dashboard
- `scripts/report_generator.py`
- `web/dashboard.html`
- `web/style.css`
- `web/chart.js`

## 🎯 Proje Amacı

- Zimmerman araçlarının çıktılarından anlamlı izler çıkarmak
- Python ile analiz modülleri geliştirmek
- HTML arayüzle zaman çizelgesi ve olay skorlarını görselleştirmek

## 🗂 Klasör Yapısı

