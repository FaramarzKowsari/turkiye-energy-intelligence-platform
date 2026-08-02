<p align="center">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=256" width="128" height="128" alt="Faramarz Kowsari, author, Software Engineer and AI researcher">
</p>

<h1 align="center">Türkiye Energy Intelligence Platform</h1>
<p align="center"><strong>EnerjiNabız AI</strong> · Near-real-time electricity analytics, forecasting, anomaly detection and BI-ready exports for Türkiye.</p>
<p align="center">
  <a href="https://github.com/FaramarzKowsari/turkiye-energy-intelligence-platform/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/FaramarzKowsari/turkiye-energy-intelligence-platform/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://enerjinabiz-ai.streamlit.app" target="_blank">
  <img alt="Launch Interactive App" src="https://img.shields.io/badge/Launch-Interactive_App-FF4B4B?logo=streamlit&logoColor=white">
</a>
<a href="https://doi.org/10.5281/zenodo.21749628"><img alt="Zenodo DOI" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21749628-1682D4?logo=zenodo&logoColor=white"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-168d73.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3670A0.svg">
  <img alt="Data: Demo ready" src="https://img.shields.io/badge/Data-Demo%20ready-f3b43f.svg">
</p>


<p align="center">
  <a href="#english">English</a> ·
  <a href="#türkçe">Türkçe</a> ·
  <a href="https://enerjinabiz-ai.streamlit.app" target="_blank">Interactive App</a> ·
  <a href="https://faramarzkowsari.github.io/turkiye-energy-intelligence-platform/">Project Website</a> ·
  <a href="docs/RELEASE_AND_ZENODO.md">Release & DOI</a>
</p>

> **Independence by design:** the repository runs immediately with reproducible demo data, accepts local CSV/XLSX/Parquet files, supports public TEİAŞ report discovery, and offers EPİAŞ as an optional Bring-Your-Own-Credentials connector. Credentials are never committed.

---

<a id="english"></a>
## English

### What this project is

EnerjiNabız AI is an open-source research and engineering platform for Turkish electricity-market intelligence. It turns hourly consumption, generation mix and market-price data into clean analytical tables, quality reports, forecasts, anomaly alerts, interactive charts, a REST API, and export packages for Power BI and Tableau.

### Why it is portfolio-grade

- Provider-agnostic data architecture: demo, local files, TEİAŞ public reports and optional EPİAŞ APIs.
- Reproducible ETL with schema normalization, duplicate control, missing-value checks and provenance fields.
- Time-series forecasting with a transparent baseline and machine-learning model comparison.
- Anomaly detection for load, price and renewable-generation deviations.
- Streamlit dashboard, FastAPI endpoints and static bilingual GitHub Pages.
- BI-ready star-schema exports in CSV, XLSX and Parquet when PyArrow is installed.
- Scientific metadata for citation, GitHub release archiving and Zenodo DOI integration.

### Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev,app]"
python scripts/generate_demo.py
python scripts/build_exports.py
streamlit run app/streamlit_app.py
```

The default mode uses demo data and does not require registration.

### Optional EPİAŞ mode

Create a free EPİAŞ Transparency Platform account, copy `.env.example` to `.env`, and set:

```env
ENERGY_DATA_PROVIDER=epias
EPIAS_USERNAME=your-email
EPIAS_PASSWORD=your-password
```

Then verify the connection locally:

```bash
python scripts/verify_epias_connection.py
```

Never send credentials to another person and never commit `.env`.

### Main outputs

| Output | Location |
|---|---|
| Clean hourly analytical table | `data/processed/energy_hourly.csv` |
| Power BI / Tableau fact table | `data/exports/fact_energy_hourly.csv` |
| Generation-mix long table | `data/exports/fact_generation_mix.csv` |
| Date dimension | `data/exports/dim_datetime.csv` |
| KPI summary | `data/exports/dashboard_kpis.csv` |
| Excel workbook | `data/exports/enerjinabiz_bi_pack.xlsx` |
| Data-quality report | `reports/data_quality_report.json` |
| Forecast metrics | `reports/forecast_metrics.json` |
| Static project website | `docs/index.html` |

### Architecture

```text
Demo / local files / TEİAŞ catalog / EPİAŞ API
                      ↓
          ingestion + provenance
                      ↓
      validation + schema normalization
                      ↓
      analytical table + quality scores
                      ↓
 forecasting / anomalies / KPI computation
                      ↓
Streamlit · FastAPI · GitHub Pages · Power BI · Tableau
```

### Data-source position

EPİAŞ is an optional authenticated provider. Its official electrical-services documentation describes REST endpoints, TGT authentication, hourly real-time consumption published with a delay, resource-level real-time generation and day-ahead market clearing prices. TEİAŞ public sector-report pages are used as a discoverable public-report source. The project does not claim affiliation with EPİAŞ, TEİAŞ or the Government of Türkiye.


### Research and product documentation

- [Data Card](docs/DATA_CARD.md)
- [Model Card](docs/MODEL_CARD.md)
- [Trust and governance](docs/TRUST_AND_GOVERNANCE.md)
- [Public-sector use cases](docs/PUBLIC_SECTOR_USE_CASES.md)
- [Startup brief](docs/STARTUP_BRIEF.md)
- [Roadmap](docs/ROADMAP.md)

### Responsible use

This software is an analytical and educational tool. It is not an official grid-control system, trading recommendation, market operator service, emergency warning system or certified energy audit.

---

<a id="türkçe"></a>
## Türkçe

### Proje nedir?

EnerjiNabız AI, Türkiye elektrik piyasasına yönelik açık kaynaklı bir araştırma ve mühendislik platformudur. Saatlik tüketim, üretim karması ve piyasa fiyatı verilerini temiz analitik tablolara, veri-kalitesi raporlarına, tahminlere, anomali uyarılarına, etkileşimli grafiklere, REST API'lerine ve Power BI/Tableau çıktılarına dönüştürür.

### Neden güçlü bir portföy projesidir?

- Demo, yerel dosya, TEİAŞ açık raporları ve isteğe bağlı EPİAŞ bağlantısı.
- Şema standardizasyonu, tekrar kayıt kontrolü, eksik veri analizi ve veri kökeni takibi.
- Şeffaf temel modeller ile makine öğrenmesi tahminlerinin karşılaştırılması.
- Tüketim, fiyat ve yenilenebilir üretim sapmaları için anomali tespiti.
- Streamlit paneli, FastAPI servisi ve iki dilli GitHub Pages sitesi.
- Power BI ve Tableau için CSV, XLSX ve uygun ortamda Parquet çıktıları.
- GitHub sürümü ve Zenodo DOI arşivlemesi için bilimsel metadata.

### Hızlı başlangıç

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,app]"
python scripts/generate_demo.py
python scripts/build_exports.py
streamlit run app/streamlit_app.py
```

Varsayılan demo modu üyelik gerektirmez.

### İsteğe bağlı EPİAŞ bağlantısı

EPİAŞ Şeffaflık Platformu hesabınızı oluşturduktan sonra `.env.example` dosyasını `.env` olarak kopyalayın ve kendi bilgilerinizi yalnızca yerel makinenizde girin. Proje kimlik bilgilerini GitHub'a yüklemez.

### Temel çıktılar

- Temiz saatlik veri seti
- Üretim kaynağı bazında uzun-format tablo
- Tarih/saat boyutu
- Yönetici KPI özeti
- Power BI ve Tableau veri paketi
- Tahmin ve anomali raporları
- İki dilli statik web sitesi

### Araştırma ve ürün belgeleri

- [Veri Kartı / Data Card](docs/DATA_CARD.md)
- [Model Kartı / Model Card](docs/MODEL_CARD.md)
- [Güven ve yönetişim](docs/TRUST_AND_GOVERNANCE.md)
- [Kamu sektörü kullanım alanları](docs/PUBLIC_SECTOR_USE_CASES.md)
- [Girişim özeti](docs/STARTUP_BRIEF.md)
- [Yol haritası](docs/ROADMAP.md)

### Kullanım sınırı

Bu yazılım resmî şebeke kontrolü, yatırım tavsiyesi, piyasa işletmecisi hizmeti, acil durum uyarısı veya sertifikalı enerji etüdü değildir.

### Yazar

**Faramarz Kowsari**, İstanbul merkezli bir yazar, Yazılım Mühendisi ve yapay zekâ araştırmacısıdır. Teknoloji, eğitim ve kişisel gelişimin kesişimine odaklanarak uluslararası platformlarda 80'den fazla dijital eser yayımlamıştır. Uzmanlık alanları Yapay Zekâ, istem mühendisliği, modern işlem stratejileri (Smart Money Concepts ve algoritmik işlem), klasik edebiyat ve farkındalık çalışmalarını kapsar. Yazarlığın yanı sıra web tabanlı eğitim araçları geliştirir ve uzmanlaşmış eğitim videoları üretir.

Resmî profiller: [ORCID](https://orcid.org/0000-0003-1692-0453) · [Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) · [GitHub](https://github.com/FaramarzKowsari) · [LinkedIn](https://www.linkedin.com/in/faramarzkowsari) · [Google Books](https://play.google.com/store/search?q=Faramarz_Kowsari&c=books) · [Resmî Web Sitesi](https://FaramarzKowsari.github.io) · [Zenodo Kayıtları](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22&l=list&p=1&s=10&sort=bestmatch)

---

## Author

**Faramarz Kowsari** is an author, Software Engineer and AI researcher based in Istanbul. Focusing on the intersection of technology, education, and personal growth, he has published over 80 digital titles on international platforms. His areas of expertise span Artificial Intelligence, prompt engineering, modern trading strategies (Smart Money Concepts & algorithmic trading), as well as classical literature and mindfulness. In addition to writing, he develops web-based educational tools and creates specialized instructional video content.

Official profiles: [ORCID](https://orcid.org/0000-0003-1692-0453) · [Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) · [GitHub](https://github.com/FaramarzKowsari) · [LinkedIn](https://www.linkedin.com/in/faramarzkowsari) · [Google Books](https://play.google.com/store/search?q=Faramarz_Kowsari&c=books) · [Official Website](https://FaramarzKowsari.github.io) · [Zenodo Records](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22&l=list&p=1&s=10&sort=bestmatch)

## Citation

To cite the archived version `v1.0.0`:

> Kowsari, Faramarz. (2026). *Türkiye Energy Intelligence Platform* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21749629

Machine-readable citation metadata is available in [`CITATION.cff`](CITATION.cff).

For references to the software project across all current and future versions, use the [Concept DOI](https://doi.org/10.5281/zenodo.21749628).

## License

MIT License for source code. Data obtained from external providers remains subject to each provider's terms and attribution requirements.


<!-- ZENODO_DOI_START -->
### Zenodo DOI

- **All versions / Concept DOI:** [10.5281/zenodo.21749628](https://doi.org/10.5281/zenodo.21749628)
- **Version v1.0.0 DOI:** [10.5281/zenodo.21749629](https://doi.org/10.5281/zenodo.21749629)
<!-- ZENODO_DOI_END -->
