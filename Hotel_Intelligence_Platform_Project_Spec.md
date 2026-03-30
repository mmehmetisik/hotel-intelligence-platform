# 🏨 Hotel Intelligence Platform — Detaylı Proje Spesifikasyonu

---

## 1. PROJENİN HİKAYESİ VE MOTİVASYONU

### 1.1 Nereden Geldi Bu Fikir?

Mehmet Işık, 10+ yıl endüstriyel tesis yönetimi deneyiminin ardından Data Scientist olarak kariyerine devam ediyor. Bu süreçte HUAYSI adlı production-grade bir AI platformu geliştirdi (Adana Su İdaresi için). HUAYSI'te yapılanlar — simülasyon motorları, AI briefing, predictive analytics, production deployment — hospitality sektörüne de birebir uygulanabilir.

Bu proje, **otelcilik sektöründe Data Science'ın nasıl değer yaratabileceğini** somut olarak göstermek için tasarlandı. Proje, bir otel zincirinin ihtiyaç duyacağı temel AI/ML yeteneklerini end-to-end olarak kapsıyor:
- Müşteri davranışı tahmini
- Gelir optimizasyonu
- Yapılandırılmamış veri analizi
- Konuşma tabanlı analitik
- Production-ready MLOps altyapısı

### 1.2 Proje Hedefi

Açık kaynak, end-to-end bir **Hotel Intelligence Platform** geliştirmek. Bu platform:
- Otel zincirlerinin veri bilimi ihtiyaçlarını karşılayan 4 ana modülden oluşur
- Sentetik ama gerçekçi veri setleri üzerinde çalışır
- Production-ready kod kalitesinde olur
- GitHub'da açık kaynak olarak yayınlanır
- Kaggle'da notebook serisi olarak paylaşılır
- Streamlit ile canlı demo sunulur

### 1.3 Hedef Kitle

Bu proje şu kişilere hitap eder:
- Hospitality sektöründe Data Science ekibi kurmak isteyen şirketler
- Data Scientist olarak iş arayan profesyoneller (referans proje)
- Otelcilik sektöründe AI/ML uygulamalarını merak edenler

---

## 2. STRAWBERRY İLANI İLE BİREBİR EŞLEŞTİRME TABLOSU

Bu tablo, projenin her modülünün Strawberry ilanındaki hangi gereksinimleri karşıladığını gösterir:

| Strawberry İlanı Gereksinimi | Proje Modülü | Detay |
|---|---|---|
| Booking cancellation prediction | Modül 1: Predictive Analytics | Classification model (XGBoost, LightGBM) |
| Customer lifetime value forecasting | Modül 1: Predictive Analytics | BG-NBD + Gamma-Gamma CLTV modeli |
| Customer classification | Modül 1: Predictive Analytics | RFM segmentasyonu + clustering |
| LLMs for unstructured data extraction | Modül 2: LLM & Unstructured Data | Fatura/POS veri sınıflandırma |
| Invoice data classification | Modül 2: LLM & Unstructured Data | LLM ile otomatik kategorizasyon |
| Classification and clean-up routines | Modül 2: LLM & Unstructured Data | Master item temizleme pipeline |
| Conversational analytics products | Modül 3: Conversational AI | Hotel Analytics Assistant chatbot |
| MLOps best practices | Modül 4: MLOps | CI/CD, MLflow, model monitoring |
| Model tested, versioned, monitored | Modül 4: MLOps | MLflow tracking + versioning |
| Data pipelines for accurate processing | Modül 4: MLOps | Automated data pipeline |
| Communicate complex results to stakeholders | Tüm modüller | Dashboard, visualizations, AI briefing |
| Design, build, and deploy ML models | Tüm modüller | End-to-end, production-ready |

---

## 3. TEKNİK MİMARİ

### 3.1 Genel Mimari Diyagramı

```
hotel-intelligence-platform/
│
├── 📊 Module 1: Predictive Analytics
│   ├── Booking Cancellation Prediction (Classification)
│   ├── Customer Lifetime Value (CLTV) Forecasting
│   └── Customer Segmentation (RFM + Clustering)
│
├── 🤖 Module 2: LLM & Unstructured Data
│   ├── Invoice/POS Data Classification (LLM-powered)
│   ├── Master Item Cleanup Pipeline
│   └── Unstructured Text Extraction
│
├── 💬 Module 3: Conversational AI
│   ├── Hotel Analytics Assistant (Streamlit Chatbot)
│   ├── Natural Language to SQL
│   └── Automated Insight Generation
│
├── ⚙️ Module 4: MLOps & Production
│   ├── MLflow Experiment Tracking
│   ├── Model Versioning & Registry
│   ├── Monitoring Dashboard
│   └── Automated Data Pipeline
│
├── 📁 data/
│   ├── raw/           (sentetik ham veri)
│   ├── processed/     (işlenmiş veri)
│   └── synthetic/     (veri üretim scriptleri)
│
├── 📁 notebooks/      (Kaggle notebook'ları)
├── 📁 app/            (Streamlit uygulaması)
├── 📁 tests/          (unit testler)
├── 📁 docs/           (dokümantasyon)
├── 📁 mlflow/         (MLflow artifact'leri)
│
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/  (CI/CD)
└── LICENSE (MIT)
```

### 3.2 Teknoloji Stack'i

| Katman | Teknoloji | Neden Bu Seçildi |
|---|---|---|
| **Programlama Dili** | Python 3.11+ | Strawberry ilanında Python istenmiş |
| **ML Kütüphaneleri** | Scikit-learn, XGBoost, LightGBM, CatBoost | Classification, regression, clustering |
| **CLTV Modelleri** | btyd kütüphanesi (BG-NBD, Gamma-Gamma) | Müşteri ömür değeri hesaplama — `lifetimes` kütüphanesi archived/bakımsız olduğu için aktif olarak maintain edilen `btyd` (Buy Till You Die) tercih edildi |
| **Deep Learning** | ~~TensorFlow/Keras~~ — Bu projede kullanılmayacak. XGBoost/LightGBM/CatBoost yeterli. Gerekirse ileride eklenebilir | Gereksiz ağırlık (500MB+) eklememek için çıkarıldı |
| **LLM** | Groq API (ücretsiz tier) + Response Caching + Local Fallback | Hızlı, ücretsiz LLM erişimi. Rate limit sorunlarına karşı: (1) Response caching — aynı soru tekrar sorulunca API'ye gitmez, (2) Local fallback — küçük Hugging Face model (DistilBERT veya benzeri) Groq erişilemezse devreye girer |
| **NLP** | Hugging Face Transformers | Text classification, NER |
| **Veri İşleme** | Pandas, NumPy, SciPy | Veri manipülasyonu |
| **Visualization** | Matplotlib, Seaborn, Plotly | Grafikler ve dashboardlar |
| **Web App** | Streamlit | Canlı demo, chatbot arayüzü |
| **MLOps** | MLflow | Experiment tracking, model registry |
| **Database** | SQLite (demo) / PostgreSQL (production) | Veri depolama |
| **CI/CD** | GitHub Actions | Otomatik test ve deployment |
| **Container** | Docker, docker-compose | Reproducibility |
| **Version Control** | Git/GitHub | Kod yönetimi |

---

## 4. VERİ STRATEJİSİ

### 4.1 Veri Kaynakları

Gerçek otel verisi kullanamayız (gizlilik), bu yüzden şu stratejiyi izleyeceğiz:

#### a) Kaggle'dan Hazır Veri Setleri
- **Hotel Booking Demand Dataset** (Antonio, Almeida & Nunes, 2019)
  - ~119.390 kayıt, 32 özellik
  - İptal durumu, müşteri tipi, lead time, oda tipi, fiyat, vs.
  - Kaynak: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
  - Kullanım: Modül 1 (Booking cancellation, customer classification)

#### b) Sentetik Veri Üretimi (Biz Oluşturacağız)
- **CLTV verisi**: Müşteri işlem geçmişi (recency, frequency, monetary)
  - Python Faker + custom logic ile üretilecek
  - 10.000+ müşteri, 2 yıllık işlem geçmişi
  - Kullanım: Modül 1 (CLTV forecasting)

- **Fatura/POS verisi**: Yapılandırılmamış metin verileri
  - Restoran, spa, minibar, oda servisi faturaları
  - Çoklu dil, farklı formatlar, typo'lar dahil
  - 5.000+ fatura satırı
  - Kullanım: Modül 2 (LLM classification)

- **Master Item verisi**: Kirli, tutarsız ürün isimleri
  - "Coke", "Coca Cola", "coca-cola", "CC 330ml" gibi varyasyonlar
  - 1.000+ ürün kaydı
  - Kullanım: Modül 2 (Cleanup pipeline)

- **Konuşma verisi**: Örnek analytics soruları
  - "What was the cancellation rate last month?"
  - "Show me top 10 customers by revenue"
  - "Compare Q1 vs Q2 occupancy"
  - 100+ örnek soru-cevap çifti
  - Kullanım: Modül 3 (Conversational AI)

### 4.2 Veri Üretim Pipeline'ı

```python
# data/synthetic/generate_all_data.py
# Bu script tüm sentetik verileri üretir

# 1. CLTV Transaction Data
# 2. Invoice/POS Data (unstructured)
# 3. Master Item Data (dirty)
# 4. Sample Analytics Questions
# 5. Hotel operational metrics (daily)
```

Her veri seti için:
- Üretim scripti (`data/synthetic/generate_*.py`)
- Veri sözlüğü (`docs/data_dictionary.md`)
- Kalite kontrol scripti (`tests/test_data_quality.py`)
- Örnek veri (ilk 100 satır README'de gösterilir)

---

## 5. MODÜL 1: PREDICTIVE ANALYTICS (En Büyük Modül)

### 5.1 Alt-Modül 1A: Booking Cancellation Prediction

**Amaç:** Bir otel rezervasyonunun iptal edilip edilmeyeceğini tahmin etmek.

**İş Değeri:** Otel, yüksek iptal olasılığı olan rezervasyonlar için:
- Overbooking stratejisi uygulayabilir
- Depozit politikasını ayarlayabilir
- Hedefli iletişim kampanyası başlatabilir

**Veri:** Hotel Booking Demand Dataset (Kaggle)

**Feature Engineering Adımları:**
1. Temporal features: lead time buckets, arrival month/season, weekend flag
2. Customer features: previous cancellations, repeated guest, customer type
3. Booking features: deposit type, booking changes, special requests count
4. Price features: ADR (Average Daily Rate), total stay cost, price deviation from mean
5. Interaction features: lead_time × deposit_type, is_repeated × previous_cancellations
6. Aggregation features: historical cancellation rate by hotel type, by customer segment

**Modeller (karşılaştırmalı):**
1. Logistic Regression (baseline)
2. Random Forest
3. XGBoost
4. LightGBM
5. CatBoost

**Evaluation Metrikleri:**
- AUC-ROC
- Precision, Recall, F1
- Confusion Matrix
- Feature Importance (SHAP values)
- Business Impact Analysis (estimated revenue saved)

**Dosya Yapısı:**
```
module_1_predictive/
├── 1a_cancellation/
│   ├── 01_eda.py                    # Exploratory Data Analysis
│   ├── 02_feature_engineering.py     # Feature creation
│   ├── 03_model_training.py          # Train all models
│   ├── 04_model_evaluation.py        # Compare models
│   ├── 05_shap_analysis.py           # Explainability
│   ├── 06_business_impact.py         # Revenue impact calculation
│   └── config.yaml                   # Hyperparameters, paths
```

**Kaggle Notebook:** "Hotel Booking Cancellation Prediction — End-to-End ML Pipeline with Business Impact Analysis"

---

### 5.2 Alt-Modül 1B: Customer Lifetime Value (CLTV) Forecasting

**Amaç:** Her müşterinin gelecek 6-12 ay içindeki tahmini gelir değerini hesaplamak.

**İş Değeri:**
- Yüksek değerli müşterilere özel kampanyalar
- Sadakat programı optimizasyonu
- Pazarlama bütçesi tahsisi

**Veri:** Sentetik müşteri işlem verisi (biz üretiyoruz)

**Metodoloiji:**
1. **RFM Analizi**: Recency, Frequency, Monetary skorlama
2. **BG-NBD Modeli**: Müşterinin gelecekte kaç işlem yapacağını tahmin
3. **Gamma-Gamma Modeli**: Her işlemin ortalama parasal değerini tahmin
4. **CLTV Hesaplama**: BG-NBD × Gamma-Gamma = 6 aylık CLTV
5. **Segmentasyon**: CLTV'ye göre müşteri grupları (Champions, Loyal, At Risk, Lost)

**Dosya Yapısı:**
```
module_1_predictive/
├── 1b_cltv/
│   ├── 01_data_preparation.py        # Transaction data hazırlama
│   ├── 02_rfm_analysis.py            # RFM skorlama
│   ├── 03_bgnbd_model.py             # BG-NBD frequency prediction
│   ├── 04_gamma_gamma_model.py       # Monetary value prediction
│   ├── 05_cltv_calculation.py        # Final CLTV hesaplama
│   ├── 06_segmentation.py            # Müşteri segmentasyonu
│   ├── 07_visualization.py           # Segment dashboards
│   └── config.yaml
```

**Kaggle Notebook:** "Hotel Customer Lifetime Value — BG-NBD & Gamma-Gamma with Actionable Segmentation"

---

### 5.3 Alt-Modül 1C: Customer Segmentation & Classification

**Amaç:** Müşterileri davranışsal özelliklerine göre anlamlı gruplara ayırmak.

**İş Değeri:**
- Hedefli pazarlama kampanyaları
- Kişiselleştirilmiş otel deneyimi
- Churn (kayıp) riski olan müşterileri tespit

**Veri:** Hotel Booking Demand + Sentetik CLTV verisi (birleştirilmiş)

**Metodoloji:**
1. **Feature Engineering**: Booking patterns, spending habits, loyalty indicators
2. **K-Means Clustering**: Optimal k seçimi (Elbow + Silhouette)
3. **Hierarchical Clustering**: Dendrogram analizi
4. **Segment Profiling**: Her segmentin karakteristikleri
5. **Classification Model**: Yeni müşteriyi otomatik segmente atama (supervised)

**Dosya Yapısı:**
```
module_1_predictive/
├── 1c_segmentation/
│   ├── 01_feature_engineering.py
│   ├── 02_clustering.py              # K-Means, Hierarchical
│   ├── 03_segment_profiling.py       # Segment analizi
│   ├── 04_classification_model.py    # Yeni müşteri sınıflandırma
│   ├── 05_visualization.py           # Segment dashboard
│   └── config.yaml
```

---

## 6. MODÜL 2: LLM & UNSTRUCTURED DATA

### 6.1 Alt-Modül 2A: Invoice/POS Data Classification

**Amaç:** Yapılandırılmamış fatura verilerini LLM kullanarak otomatik sınıflandırmak.

**İş Değeri:**
- Manuel fatura sınıflandırma işgücünü %90 azaltma
- Tutarlı ve doğru gelir raporlaması
- Gerçek zamanlı harcama analizi

**Veri:** Sentetik fatura verileri (biz üretiyoruz)

**Örnek Ham Veri:**
```
"2x espresso + 1 croissant - Room 412"
"Spa treatment - Swedish massage 60min"  
"Minibar: 2 beer, 1 wine, chips"
"Room service: Club sandwich + fries + coke"
"Parking 3 days - underground"
"Laundry service - 5 items express"
```

**Kategoriler:**
- Food & Beverage (Restaurant, Room Service, Minibar)
- Spa & Wellness
- Room Charges
- Transportation (Parking, Transfer)
- Laundry & Housekeeping
- Events & Meetings
- Other

**Metodoloji:**
1. **Rule-based baseline**: Regex + keyword matching
2. **LLM Classification**: Groq API ile zero-shot classification
3. **LLM + Few-shot**: Örnek verilerle few-shot prompting
4. **Fine-tuned approach**: Hugging Face model ile text classification
5. **Karşılaştırma**: Accuracy, speed, cost analizi

**Dosya Yapısı:**
```
module_2_llm/
├── 2a_invoice_classification/
│   ├── 01_data_generation.py          # Sentetik fatura üretimi
│   ├── 02_rule_based_baseline.py      # Regex baseline
│   ├── 03_llm_zero_shot.py            # LLM zero-shot
│   ├── 04_llm_few_shot.py             # LLM few-shot
│   ├── 05_transformer_classification.py # Fine-tuned model
│   ├── 06_comparison.py               # Method comparison
│   ├── prompts/                       # Prompt templates
│   │   ├── zero_shot_prompt.txt
│   │   ├── few_shot_prompt.txt
│   │   └── system_prompt.txt
│   └── config.yaml
```

---

### 6.2 Alt-Modül 2B: Master Item Cleanup Pipeline

**Amaç:** Tutarsız, kirli ürün isimlerini LLM ile standardize etmek.

**İş Değeri:**
- Doğru envanter takibi
- Tutarlı raporlama
- Tedarik zinciri optimizasyonu

**Örnek:**
```
Input:                    → Standardized Output:
"Coke 330ml"             → "Coca-Cola 330ml"
"coca cola"              → "Coca-Cola 330ml"
"CC can"                 → "Coca-Cola 330ml"
"Pepsi Cola 500"         → "Pepsi 500ml"
"peps 500ml"             → "Pepsi 500ml"
"Spagetti Bolognese"     → "Spaghetti Bolognese"
"spag bol"               → "Spaghetti Bolognese"
```

**Metodoloji:**
1. **Fuzzy Matching**: fuzzywuzzy / rapidfuzz ile string similarity
2. **LLM Standardization**: Groq API ile isim standardizasyonu
3. **Embedding-based**: Sentence embeddings + cosine similarity ile gruplandırma
4. **Hybrid Pipeline**: Fuzzy + LLM + embedding kombine

**Dosya Yapısı:**
```
module_2_llm/
├── 2b_master_item_cleanup/
│   ├── 01_data_generation.py          # Kirli veri üretimi
│   ├── 02_fuzzy_matching.py           # String similarity
│   ├── 03_llm_standardization.py      # LLM ile temizleme
│   ├── 04_embedding_clustering.py     # Embedding-based gruplandırma
│   ├── 05_hybrid_pipeline.py          # Kombine pipeline
│   ├── 06_evaluation.py               # Accuracy karşılaştırma
│   └── config.yaml
```

---

### 6.3 Alt-Modül 2C: Unstructured Review Analysis

**Amaç:** Müşteri yorumlarından otomatik insight çıkarmak.

**İş Değeri:**
- Müşteri memnuniyeti trendlerini takip
- Operasyonel sorunları erken tespit
- Departman bazlı performans analizi

**Metodoloji:**
1. **Sentiment Analysis**: Pozitif/Negatif/Nötr sınıflandırma
2. **Topic Extraction**: LLM ile ana konuları çıkarma (temizlik, yemek, personel, konum...)
3. **Aspect-based Sentiment**: Her konu için ayrı sentiment skoru
4. **Trend Analysis**: Zaman bazlı sentiment değişimi

**Dosya Yapısı:**
```
module_2_llm/
├── 2c_review_analysis/
│   ├── 01_data_preparation.py
│   ├── 02_sentiment_analysis.py
│   ├── 03_topic_extraction.py
│   ├── 04_aspect_sentiment.py
│   ├── 05_trend_dashboard.py
│   └── config.yaml
```

---

## 7. MODÜL 3: CONVERSATIONAL AI

### 7.1 Hotel Analytics Assistant

**Amaç:** Doğal dilde soru sorarak otel verilerinden insight alan bir chatbot.

**İş Değeri:**
- Non-technical stakeholder'ların veriye erişimi
- Anlık karar desteği
- Rapor otomasyonu

**Örnek Konuşmalar:**
```
User: "What was the cancellation rate last month?"
Bot: "Last month's cancellation rate was 23.4%, which is 2.1% higher 
     than the previous month. The increase was mainly driven by 
     bookings with lead times over 90 days."

User: "Show me top 10 customers by total revenue"
Bot: [Generates table + bar chart]
     "Here are the top 10 customers. Customer #4521 leads with 
     €12,340 in total spend across 8 stays."

User: "Compare weekend vs weekday occupancy for Q1"
Bot: [Generates comparison chart]
     "Weekend occupancy averaged 87% vs 72% for weekdays in Q1. 
     January weekends showed the lowest occupancy at 69%."

User: "Which customer segment has the highest churn risk?"
Bot: "The 'At Risk' segment (342 customers) shows a 45% probability 
     of not returning within 6 months. Recommended action: targeted 
     re-engagement campaign with personalized offers."
```

**Teknik Mimari:**
```
User Question (Natural Language)
         ↓
    ┌────────────────────┐
    │  Cache Check        │ ← diskcache: aynı/benzer soru daha önce soruldu mu?
    └────────────────────┘
         ↓ (cache miss)
    Intent Detection (LLM — Groq API)
         ↓
    ┌────────────────────┐
    │  SQL Generation    │ ← Schema-aware prompt
    │  (Text-to-SQL)     │
    └────────────────────┘
         ↓
    Query Execution (SQLite/PostgreSQL)
         ↓
    ┌────────────────────┐
    │  Result Processing │
    │  + Visualization   │
    └────────────────────┘
         ↓
    ┌────────────────────┐
    │  Natural Language   │ ← LLM generates insight
    │  Response + Charts  │
    └────────────────────┘
         ↓
    Cache Store + Streamlit UI
```

**⚠️ Groq API Rate Limit Stratejisi:**
1. **Response Caching (diskcache):** Her LLM çağrısının sonucu cache'lenir. Aynı veya çok benzer soru tekrar sorulduğunda API'ye gitmeden cache'den döner. TTL (time-to-live) ayarlanabilir.
2. **Local Fallback Model:** Groq API erişilemezse veya rate limit aşılırsa, küçük bir Hugging Face model (DistilBERT veya küçük bir text-generation model) devreye girer. Bu model daha basit cevaplar verir ama sistem çökmez.
3. **Retry with Backoff:** Rate limit hatası alındığında exponential backoff ile yeniden deneme.
4. **Usage Dashboard:** Kalan API kotasını gösteren bir Streamlit widget'ı.

**Dosya Yapısı:**
```
module_3_conversational/
├── app.py                         # Streamlit main app
├── agents/
│   ├── intent_detector.py         # Soru tipi belirleme
│   ├── sql_generator.py           # NL → SQL dönüşümü
│   ├── insight_generator.py       # Sonuçtan insight üretme
│   └── chart_generator.py         # Otomatik grafik oluşturma
├── llm/
│   ├── groq_client.py             # Groq API wrapper + retry logic
│   ├── cache_manager.py           # diskcache response caching
│   ├── fallback_model.py          # Local HuggingFace fallback
│   └── llm_router.py             # Groq → fallback otomatik yönlendirme
├── database/
│   ├── schema.sql                 # Database şeması
│   ├── init_db.py                 # DB initialization
│   └── sample_queries.py          # Örnek sorgular
├── prompts/
│   ├── intent_prompt.txt
│   ├── sql_prompt.txt
│   ├── insight_prompt.txt
│   └── schema_context.txt
├── utils/
│   ├── db_connector.py
│   ├── chart_utils.py
│   └── response_formatter.py
├── tests/
│   ├── test_sql_generation.py
│   ├── test_intent_detection.py
│   ├── test_cache.py              # Cache testleri
│   ├── test_fallback.py           # Fallback testleri
│   └── test_queries.py
└── config.yaml
```

---

## 8. MODÜL 4: MLOps & PRODUCTION

### 8.1 MLflow Experiment Tracking

**Amaç:** Tüm modellerin experiment tracking, versioning ve registry'si.

**Kapsam:**
- Her model eğitimi MLflow'da loglanır
- Hyperparameter'lar, metrikler, artifact'ler kaydedilir
- Model comparison dashboard
- Best model otomatik seçimi

**Dosya Yapısı:**
```
module_4_mlops/
├── tracking/
│   ├── mlflow_setup.py            # MLflow server config
│   ├── experiment_logger.py       # Generic experiment logger
│   └── model_registry.py          # Model registration
```

### 8.2 Model Monitoring

**Amaç:** Production'daki modellerin performansını izlemek.

**Kapsam:**
- Data drift detection (input dağılımı değişimi)
- Model performance drift (accuracy düşüşü)
- Alerting (threshold aşımında uyarı)
- Monitoring dashboard (Streamlit)

**Dosya Yapısı:**
```
module_4_mlops/
├── monitoring/
│   ├── data_drift.py              # Input distribution monitoring
│   ├── model_drift.py             # Performance monitoring
│   ├── alerts.py                  # Threshold-based alerts
│   └── monitoring_dashboard.py    # Streamlit dashboard
```

### 8.3 CI/CD Pipeline

**Amaç:** Otomatik test, lint ve deployment.

**GitHub Actions Workflow:**
```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m flake8 src/
```

### 8.4 Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    command: mlflow server --host 0.0.0.0
```

---

## 9. DETAYLI DOSYA YAPISI (TAM)

```
hotel-intelligence-platform/
│
├── README.md                          # Ana README (aşağıda detayı var)
├── LICENSE                            # MIT License
├── requirements.txt                   # Python bağımlılıkları
├── setup.py                           # Package setup
├── Dockerfile                         # Docker image
├── docker-compose.yml                 # Docker compose (app + mlflow)
├── .gitignore                         # Git ignore
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI/CD
│
├── data/
│   ├── raw/
│   │   └── hotel_bookings.csv         # Kaggle dataset (gitignore, README'de link)
│   ├── processed/
│   │   ├── bookings_featured.csv      # Feature engineered
│   │   ├── customers_rfm.csv          # RFM scores
│   │   ├── customers_cltv.csv         # CLTV values
│   │   └── customers_segments.csv     # Segment labels
│   └── synthetic/
│       ├── generate_transactions.py   # CLTV transaction data
│       ├── generate_invoices.py       # Unstructured invoice data
│       ├── generate_master_items.py   # Dirty product names
│       ├── generate_reviews.py        # Hotel reviews
│       ├── generate_analytics_qa.py   # Q&A pairs for chatbot
│       └── generate_all.py            # Run all generators
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Global config
│   │
│   ├── module_1_predictive/
│   │   ├── __init__.py
│   │   ├── cancellation/
│   │   │   ├── __init__.py
│   │   │   ├── eda.py
│   │   │   ├── features.py
│   │   │   ├── train.py
│   │   │   ├── evaluate.py
│   │   │   ├── shap_analysis.py
│   │   │   └── business_impact.py
│   │   ├── cltv/
│   │   │   ├── __init__.py
│   │   │   ├── data_prep.py
│   │   │   ├── rfm.py
│   │   │   ├── bgnbd.py
│   │   │   ├── gamma_gamma.py
│   │   │   ├── cltv_calc.py
│   │   │   └── segmentation.py
│   │   └── clustering/
│   │       ├── __init__.py
│   │       ├── features.py
│   │       ├── kmeans.py
│   │       ├── profiling.py
│   │       └── classifier.py
│   │
│   ├── module_2_llm/
│   │   ├── __init__.py
│   │   ├── invoice_classification/
│   │   │   ├── __init__.py
│   │   │   ├── rule_based.py
│   │   │   ├── llm_zero_shot.py
│   │   │   ├── llm_few_shot.py
│   │   │   ├── transformer_model.py
│   │   │   └── comparison.py
│   │   ├── master_item_cleanup/
│   │   │   ├── __init__.py
│   │   │   ├── fuzzy_match.py
│   │   │   ├── llm_standardize.py
│   │   │   ├── embedding_cluster.py
│   │   │   └── hybrid_pipeline.py
│   │   └── review_analysis/
│   │       ├── __init__.py
│   │       ├── sentiment.py
│   │       ├── topics.py
│   │       ├── aspect_sentiment.py
│   │       └── trends.py
│   │
│   ├── module_3_conversational/
│   │   ├── __init__.py
│   │   ├── agents/
│   │   │   ├── intent_detector.py
│   │   │   ├── sql_generator.py
│   │   │   ├── insight_generator.py
│   │   │   └── chart_generator.py
│   │   ├── llm/
│   │   │   ├── groq_client.py         # Groq API wrapper + retry
│   │   │   ├── cache_manager.py       # diskcache response caching
│   │   │   ├── fallback_model.py      # Local HuggingFace fallback
│   │   │   └── llm_router.py         # Groq → fallback yönlendirme
│   │   ├── database/
│   │   │   ├── schema.sql
│   │   │   ├── init_db.py
│   │   │   └── sample_queries.py
│   │   ├── prompts/
│   │   │   ├── intent_prompt.txt
│   │   │   ├── sql_prompt.txt
│   │   │   ├── insight_prompt.txt
│   │   │   └── schema_context.txt
│   │   └── utils/
│   │       ├── db_connector.py
│   │       ├── chart_utils.py
│   │       └── response_formatter.py
│   │
│   └── module_4_mlops/
│       ├── __init__.py
│       ├── tracking/
│       │   ├── mlflow_setup.py
│       │   ├── experiment_logger.py
│       │   └── model_registry.py
│       ├── monitoring/
│       │   ├── data_drift.py
│       │   ├── model_drift.py
│       │   ├── alerts.py
│       │   └── dashboard.py
│       └── pipeline/
│           ├── data_pipeline.py
│           └── retrain_pipeline.py
│
├── app/
│   ├── main.py                        # Streamlit ana sayfa
│   ├── pages/
│   │   ├── 1_cancellation_predictor.py
│   │   ├── 2_cltv_dashboard.py
│   │   ├── 3_customer_segments.py
│   │   ├── 4_invoice_classifier.py
│   │   ├── 5_item_cleanup.py
│   │   ├── 6_review_analyzer.py
│   │   ├── 7_analytics_assistant.py
│   │   └── 8_mlops_monitor.py
│   ├── components/
│   │   ├── sidebar.py
│   │   ├── metrics_card.py
│   │   └── chart_components.py
│   └── assets/
│       ├── logo.png
│       └── style.css
│
├── notebooks/
│   ├── 01_booking_cancellation_prediction.ipynb
│   ├── 02_customer_lifetime_value.ipynb
│   ├── 03_customer_segmentation.ipynb
│   ├── 04_invoice_classification_llm.ipynb
│   ├── 05_master_item_cleanup.ipynb
│   ├── 06_review_sentiment_analysis.ipynb
│   └── 07_conversational_ai_demo.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── test_data_quality.py
│   ├── test_cancellation_model.py
│   ├── test_cltv_pipeline.py
│   ├── test_invoice_classifier.py
│   ├── test_sql_generator.py
│   └── test_monitoring.py
│
└── docs/
    ├── data_dictionary.md             # Tüm veri setlerinin açıklaması
    ├── model_card_cancellation.md     # Model documentation
    ├── model_card_cltv.md
    ├── architecture.md                # Sistem mimarisi detayı
    ├── deployment_guide.md            # Deployment talimatları
    └── api_reference.md               # API dokümantasyonu (opsiyonel)
```

---

## 10. README.md YAPISI

GitHub README'si şu bölümlerden oluşacak:

```markdown
# 🏨 Hotel Intelligence Platform
> End-to-end AI/ML platform for hospitality analytics — 
> from predictive models to conversational AI

[Demo Link] | [Kaggle Notebooks] | [Documentation]

## 🎯 What is this?
One-paragraph açıklama + GIF/screenshot

## ⚡ Quick Start
```bash
git clone ...
pip install -r requirements.txt
streamlit run app/main.py
```

## 🏗️ Architecture
Mimari diyagram (Mermaid veya PNG)

## 📊 Modules

### Module 1: Predictive Analytics
- Booking Cancellation Prediction (AUC: X.XX)
- Customer Lifetime Value (CLTV)
- Customer Segmentation

### Module 2: LLM & Unstructured Data
- Invoice Classification (Accuracy: X.XX%)
- Master Item Cleanup
- Review Sentiment Analysis

### Module 3: Conversational AI
- Hotel Analytics Assistant (demo GIF)

### Module 4: MLOps
- MLflow Tracking
- Model Monitoring
- CI/CD Pipeline

## 📁 Project Structure
(Dosya ağacı)

## 🔧 Tech Stack
(Tablo)

## 📈 Results & Benchmarks
(Model karşılaştırma tabloları)

## 🚀 Deployment
Docker instructions

## 📚 Kaggle Notebooks
Links to each notebook

## 🤝 Contributing
Guidelines

## 📄 License
MIT
```

---

## 11. UYGULAMA ADIMLARI (SIRALAMA)

### Faz 1: Temel Altyapı (1-2 gün)
1. GitHub repo oluştur
2. Dosya yapısını kur
3. requirements.txt hazırla
4. .gitignore, LICENSE, boş README ekle
5. Docker ve docker-compose dosyalarını hazırla
6. GitHub Actions CI pipeline kur

### Faz 2: Veri Üretimi (1-2 gün)
7. Hotel Booking Demand dataset'i indir ve incele
8. CLTV transaction verisi üret
9. Invoice/POS sentetik verisi üret
10. Master item kirli verisi üret
11. Review verisi üret
12. Analytics Q&A çiftleri üret
13. Data dictionary yaz
14. Data quality testleri yaz

### Faz 3: Modül 1 — Predictive Analytics (3-4 gün)
15. Booking Cancellation: EDA
16. Booking Cancellation: Feature Engineering
17. Booking Cancellation: Model Training + Evaluation
18. Booking Cancellation: SHAP Analysis + Business Impact
19. CLTV: Data Prep + RFM
20. CLTV: BG-NBD + Gamma-Gamma + Segmentation
21. Customer Segmentation: Clustering + Classification
22. MLflow integration for all models

### Faz 4: Modül 2 — LLM & Unstructured Data (2-3 gün)
23. Invoice Classification: Rule-based baseline
24. Invoice Classification: LLM zero-shot + few-shot
25. Invoice Classification: Comparison analysis
26. Master Item Cleanup: Fuzzy + LLM + Embedding hybrid
27. Review Analysis: Sentiment + Topics + Trends

### Faz 5: Modül 3 — Conversational AI (3-5 gün) ⚠️ EN UZUN FAZ
28. Database schema + initialization
29. Intent detection agent
30. SQL generation agent
31. Insight generation agent
32. Chart generation
33. Response caching layer (Groq rate limit koruması)
34. Local fallback model entegrasyonu (Groq erişilemezse)
35. Streamlit chatbot UI
36. Test suite for SQL generation

### Faz 6: Modül 4 — MLOps (1-2 gün)
37. MLflow experiment tracking setup
38. Model registry
39. Data drift monitoring
40. Model performance monitoring
41. Monitoring dashboard

### Faz 7: Streamlit App (2-3 gün)
42. Main page + navigation
43. Cancellation predictor page
44. CLTV dashboard page
45. Customer segments page
46. Invoice classifier page
47. Review analyzer page
48. Analytics assistant page
49. MLOps monitor page
50. Styling + polish

### Faz 8: Kaggle Notebooks (2-3 gün)
51. Notebook 1: Booking Cancellation
52. Notebook 2: CLTV
53. Notebook 3: Customer Segmentation
54. Notebook 4: Invoice Classification with LLM
55. Notebook 5: Review Sentiment Analysis
56. Notebook 6: Conversational AI Demo

### Faz 9: Dokümantasyon & Yayın (1-2 gün)
57. README.md (full)
58. Architecture documentation
59. Model cards
60. Deployment guide
61. Screenshots / GIFs
62. GitHub repo finalize
63. Kaggle notebooks publish
64. LinkedIn post

**Toplam Tahmini Süre:**
- **Claude ile birlikte çalışarak: 18-25 gün** (günde 3-4 saat)
- **Tek başına çalışarak: 28-35 gün** (günde 3-4 saat)
- **⚠️ Darboğazlar:** Modül 1 (Predictive Analytics) ve Modül 3 (Conversational AI) en çok zaman alan bileşenler — toplam sürenin ~%60'ı buralarda harcanır.
- **💡 Strateji:** Önce Modül 1'i bitir (Strawberry'nin en çok istediği), sonra Modül 2 ve 3'e geç. Modül 4 (MLOps) her modüle paralel eklenebilir.

---

## 12. KRİTİK BAŞARI FAKTÖRLERİ

### Yapılması Gerekenler:
- [x] Her modül bağımsız çalışabilmeli (modüler mimari)
- [x] Kod kalitesi yüksek olmalı (docstrings, type hints, clean code)
- [x] Her model için SHAP veya başka explainability olmalı
- [x] Business impact her yerde vurgulanmalı (sadece accuracy değil, €/$ cinsinden)
- [x] README etkileyici olmalı (GIF'ler, badges, clear structure)
- [x] Testler olmalı (minimum %80 coverage hedefi)
- [x] Docker ile tek komutla çalışmalı

### Yapılmaması Gerekenler:
- [ ] Gerçek müşteri verisi kullanma (GDPR!)
- [ ] Overengineering yapma (basit tut, çalışsın)
- [ ] Sadece notebook olarak bırakma (production-ready olmalı)
- [ ] Hata yönetimini atlama (try-except, logging)
- [ ] Dokümantasyonu atlama

---

## 13. STRAWBERRY'YE NASIL SUNULACAK?

Proje tamamlandığında, Marion'a şu şekilde sunulabilir:

1. **Email'de bahset:** "I've also built a demo project specifically aligned with Strawberry's Data Science needs — covering booking cancellation prediction, CLTV forecasting, LLM-based invoice classification, and a conversational analytics assistant."

2. **GitHub link paylaş:** "You can explore it here: github.com/mmehmetisik/hotel-intelligence-platform"

3. **Canlı demo göster:** "A live demo is available at: [Streamlit link]"

4. **Interview'da kullan:** Her teknik soru için bu projeden somut örnekler ver.

---

## 14. BAĞIMLILIKLAR (requirements.txt)

```
# Core
python>=3.11
pandas>=2.0
numpy>=1.24
scipy>=1.11

# ML
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
catboost>=1.2
btyd>=0.1  # BG-NBD, Gamma-Gamma (lifetimes kütüphanesinin aktif fork'u)

# NOT: TensorFlow bu projede kullanılmıyor — XGBoost/LightGBM/CatBoost yeterli.
# Gerekirse ileride eklenebilir ama 500MB+ gereksiz ağırlık eklememek için çıkarıldı.

# LLM
groq>=0.4
openai>=1.0  # backup
huggingface-hub>=0.20
transformers>=4.36
sentence-transformers>=2.2

# NLP
nltk>=3.8
rapidfuzz>=3.5

# Visualization
matplotlib>=3.8
seaborn>=0.13
plotly>=5.18

# Web App
streamlit>=1.30

# MLOps
mlflow>=2.10

# Database
sqlalchemy>=2.0

# Caching (Groq API rate limit koruması)
diskcache>=5.6  # LLM response caching — aynı soru tekrar sorulunca API'ye gitmez

# Testing
pytest>=7.4
pytest-cov>=4.1

# Code Quality
flake8>=6.1
black>=23.12

# Utilities
pyyaml>=6.0
python-dotenv>=1.0
faker>=22.0  # Synthetic data generation
```

---

## 15. SON NOTLAR

- Bu doküman, projenin **tam spesifikasyonu**dur. Başka bir Claude oturumunda bu dosyayı paylaştığında, buradan devam edilebilir.
- Her faz sonunda GitHub'a commit yapılmalı (küçük, sık commitler).
- Proje MIT lisansı ile açık kaynak olacak.
- Projenin amacı sadece Strawberry değil — genel olarak hospitality sektöründe Data Science yeteneklerini göstermek. Diğer otel/turizm şirketlerine başvururken de kullanılabilir.
- Kaggle notebook'ları ayrı ayrı da paylaşılabilir (her biri bağımsız bir çalışma olarak).

---

**Doküman Versiyonu:** 1.1
**Oluşturulma Tarihi:** Mart 2026
**Son Güncelleme:** Mart 2026
**Yazar:** Mehmet Işık & Claude (Anthropic)
**Durum:** Spesifikasyon tamamlandı, uygulama başlamadı

---

## 16. DEĞİŞİKLİK KAYDI (CHANGELOG)

### v1.1 (Mart 2026) — Review Sonrası Güncelleme
1. **`lifetimes` → `btyd`**: CLTV kütüphanesi değiştirildi. `lifetimes` archived/bakımsız olduğu için aktif olarak maintain edilen `btyd` (Buy Till You Die) tercih edildi.
2. **TensorFlow çıkarıldı**: Projede deep learning şart değil — XGBoost/LightGBM/CatBoost yeterli. 500MB+ gereksiz ağırlık eklememek için requirements'tan çıkarıldı.
3. **Süre tahmini güncellendi**: 15-22 gün → 18-25 gün (Claude ile birlikte), 28-35 gün (tek başına). Modül 1 ve Modül 3 darboğaz olarak işaretlendi.
4. **Groq API rate limit stratejisi eklendi**: Response caching (diskcache), local fallback model (DistilBERT), retry with backoff, usage dashboard.
5. **Modül 3 dosya yapısı güncellendi**: `llm/` klasörü eklendi (groq_client, cache_manager, fallback_model, llm_router).
6. **Faz 5 (Conversational AI) süresi güncellendi**: 2-3 gün → 3-5 gün (en uzun faz olarak işaretlendi).

### v1.0 (Mart 2026) — İlk Versiyon
- Proje spesifikasyonu oluşturuldu
- 4 modül detaylandırıldı
- Dosya yapısı, tech stack, uygulama planı yazıldı
