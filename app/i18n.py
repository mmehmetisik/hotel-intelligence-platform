"""
Internationalization (i18n) — EN / TR / DE

Simple dictionary-based translation system for the Streamlit UI.
"""

TRANSLATIONS = {
    # ─────────────── Navigation & Global ───────────────
    "app_title": {
        "en": "Hotel Intelligence Platform",
        "tr": "Otel Zeka Platformu",
        "de": "Hotel Intelligence Plattform",
    },
    "app_subtitle": {
        "en": "End-to-end AI/ML platform for hospitality analytics",
        "tr": "Konaklama analitiği için uçtan uca AI/ML platformu",
        "de": "End-to-End AI/ML-Plattform fuer Hospitality-Analytik",
    },
    "language": {
        "en": "Language",
        "tr": "Dil",
        "de": "Sprache",
    },
    "nav_home": {
        "en": "Home",
        "tr": "Ana Sayfa",
        "de": "Startseite",
    },

    # ─────────────── Home Page ───────────────
    "hero_description": {
        "en": "Predictive analytics, LLM-powered unstructured data processing, conversational AI, and production MLOps — all in one platform.",
        "tr": "Tahminsel analitik, LLM destekli yapilandirilmamis veri isleme, konusmaya dayali yapay zeka ve uretim MLOps — hepsi tek platformda.",
        "de": "Praediktive Analytik, LLM-gestuetzte unstrukturierte Datenverarbeitung, Konversations-KI und Produktions-MLOps — alles auf einer Plattform.",
    },
    "explore_modules": {
        "en": "Explore Modules",
        "tr": "Modulleri Kesfet",
        "de": "Module Erkunden",
    },
    "tech_stack": {
        "en": "Tech Stack",
        "tr": "Teknoloji Yigini",
        "de": "Tech-Stack",
    },
    "architecture": {
        "en": "Architecture",
        "tr": "Mimari",
        "de": "Architektur",
    },

    # ─────────────── Module Names ───────────────
    "mod1_title": {
        "en": "Predictive Analytics",
        "tr": "Tahminsel Analitik",
        "de": "Praediktive Analytik",
    },
    "mod1_desc": {
        "en": "Booking cancellation prediction, CLTV modeling, and customer segmentation with XGBoost, BG-NBD, and K-Means.",
        "tr": "XGBoost, BG-NBD ve K-Means ile rezervasyon iptal tahmini, CLTV modelleme ve musteri segmentasyonu.",
        "de": "Buchungsstornierungsvorhersage, CLTV-Modellierung und Kundensegmentierung mit XGBoost, BG-NBD und K-Means.",
    },
    "mod2_title": {
        "en": "LLM & Unstructured Data",
        "tr": "LLM ve Yapilandirilmamis Veri",
        "de": "LLM & Unstrukturierte Daten",
    },
    "mod2_desc": {
        "en": "Invoice classification, master item cleanup with fuzzy matching, and multi-layer sentiment analysis.",
        "tr": "Fatura siniflandirma, bulanik esleme ile ana oge temizligi ve cok katmanli duygu analizi.",
        "de": "Rechnungsklassifizierung, Stammdatenbereinigung mit Fuzzy-Matching und mehrschichtige Sentimentanalyse.",
    },
    "mod3_title": {
        "en": "Conversational AI",
        "tr": "Konusmaya Dayali Yapay Zeka",
        "de": "Konversations-KI",
    },
    "mod3_desc": {
        "en": "Natural language to SQL chatbot with intent detection, auto-visualization, and business insights.",
        "tr": "Niyet algilama, otomatik gorsellestirme ve is icgoerueleri ile dogal dilden SQL'e chatbot.",
        "de": "Natural-Language-zu-SQL-Chatbot mit Intent-Erkennung, Auto-Visualisierung und Business-Insights.",
    },
    "mod4_title": {
        "en": "MLOps & Monitoring",
        "tr": "MLOps ve Izleme",
        "de": "MLOps & Monitoring",
    },
    "mod4_desc": {
        "en": "MLflow experiment tracking, model registry, data/model drift detection, and alerting system.",
        "tr": "MLflow deney takibi, model kayit defteri, veri/model sapma tespiti ve uyari sistemi.",
        "de": "MLflow-Experimentverfolgung, Modellregistrierung, Daten-/Modelldrifterkennung und Alarmsystem.",
    },

    # ─────────────── KPI Labels ───────────────
    "total_bookings": {
        "en": "Total Bookings",
        "tr": "Toplam Rezervasyon",
        "de": "Gesamtbuchungen",
    },
    "cancel_rate": {
        "en": "Cancellation Rate",
        "tr": "Iptal Orani",
        "de": "Stornierungsrate",
    },
    "total_customers": {
        "en": "Total Customers",
        "tr": "Toplam Musteri",
        "de": "Gesamtkunden",
    },
    "ml_models": {
        "en": "ML Models",
        "tr": "ML Modelleri",
        "de": "ML-Modelle",
    },
    "best_auc": {
        "en": "Best AUC-ROC",
        "tr": "En Iyi AUC-ROC",
        "de": "Bester AUC-ROC",
    },
    "avg_revenue": {
        "en": "Avg. Revenue",
        "tr": "Ort. Gelir",
        "de": "Durchschn. Umsatz",
    },

    # ─────────────── Cancellation Page ───────────────
    "cancel_title": {
        "en": "Booking Cancellation Predictor",
        "tr": "Rezervasyon Iptal Tahmincisi",
        "de": "Buchungsstornierung Vorhersage",
    },
    "cancel_desc": {
        "en": "Predict whether a booking will be canceled using machine learning models.",
        "tr": "Makine ogrenimi modelleri kullanarak bir rezervasyonun iptal edilip edilmeyecegini tahmin edin.",
        "de": "Vorhersage, ob eine Buchung storniert wird, mithilfe von ML-Modellen.",
    },
    "model_comparison": {
        "en": "Model Comparison",
        "tr": "Model Karsilastirmasi",
        "de": "Modellvergleich",
    },
    "feature_importance": {
        "en": "Feature Importance",
        "tr": "Ozellik Onemi",
        "de": "Feature-Wichtigkeit",
    },
    "live_prediction": {
        "en": "Live Prediction",
        "tr": "Canli Tahmin",
        "de": "Live-Vorhersage",
    },
    "business_impact": {
        "en": "Business Impact",
        "tr": "Is Etkisi",
        "de": "Geschaeftsauswirkung",
    },

    # ─────────────── Customer Intelligence ───────────────
    "cust_title": {
        "en": "Customer Intelligence",
        "tr": "Musteri Zekasi",
        "de": "Kundenintelligenz",
    },
    "rfm_analysis": {
        "en": "RFM Analysis",
        "tr": "RFM Analizi",
        "de": "RFM-Analyse",
    },
    "cltv_prediction": {
        "en": "CLTV Prediction",
        "tr": "CLTV Tahmini",
        "de": "CLTV-Vorhersage",
    },
    "clustering": {
        "en": "Customer Clustering",
        "tr": "Musteri Kumeleme",
        "de": "Kundensegmentierung",
    },

    # ─────────────── Invoice Classifier ───────────────
    "invoice_title": {
        "en": "Invoice Classifier",
        "tr": "Fatura Siniflandirici",
        "de": "Rechnungsklassifizierer",
    },
    "rule_based": {
        "en": "Rule-Based",
        "tr": "Kural Tabanli",
        "de": "Regelbasiert",
    },
    "llm_powered": {
        "en": "LLM-Powered",
        "tr": "LLM Destekli",
        "de": "LLM-gestuetzt",
    },

    # ─────────────── Review Analyzer ───────────────
    "review_title": {
        "en": "Review Analyzer",
        "tr": "Yorum Analizcisi",
        "de": "Bewertungsanalyse",
    },
    "sentiment_dist": {
        "en": "Sentiment Distribution",
        "tr": "Duygu Dagilimi",
        "de": "Sentimentverteilung",
    },
    "aspect_analysis": {
        "en": "Aspect Analysis",
        "tr": "Boyut Analizi",
        "de": "Aspektanalyse",
    },

    # ─────────────── Chatbot ───────────────
    "chat_title": {
        "en": "Analytics Chatbot",
        "tr": "Analitik Chatbot",
        "de": "Analytik-Chatbot",
    },
    "chat_placeholder": {
        "en": "Ask a question about your hotel data...",
        "tr": "Otel verileriniz hakkinda bir soru sorun...",
        "de": "Stellen Sie eine Frage zu Ihren Hoteldaten...",
    },
    "chat_examples": {
        "en": "Example Questions",
        "tr": "Ornek Sorular",
        "de": "Beispielfragen",
    },

    # ─────────────── MLOps ───────────────
    "mlops_title": {
        "en": "MLOps Monitor",
        "tr": "MLOps Izleyici",
        "de": "MLOps-Monitor",
    },
    "health_score": {
        "en": "Health Score",
        "tr": "Saglik Puani",
        "de": "Gesundheitswert",
    },
    "data_drift": {
        "en": "Data Drift",
        "tr": "Veri Sapmasi",
        "de": "Datendrift",
    },
    "model_performance": {
        "en": "Model Performance",
        "tr": "Model Performansi",
        "de": "Modellleistung",
    },
    "alerts": {
        "en": "Alerts",
        "tr": "Uyarilar",
        "de": "Warnungen",
    },

    # ─────────────── Common ───────────────
    "loading": {
        "en": "Loading...",
        "tr": "Yukleniyor...",
        "de": "Laden...",
    },
    "error": {
        "en": "An error occurred",
        "tr": "Bir hata olustu",
        "de": "Ein Fehler ist aufgetreten",
    },
    "no_data": {
        "en": "No data available. Run the pipeline first.",
        "tr": "Veri mevcut degil. Oncelikle veri hattini calistirin.",
        "de": "Keine Daten verfuegbar. Fuehren Sie zuerst die Pipeline aus.",
    },
    "download": {
        "en": "Download",
        "tr": "Indir",
        "de": "Herunterladen",
    },
    "filters": {
        "en": "Filters",
        "tr": "Filtreler",
        "de": "Filter",
    },
    "results": {
        "en": "Results",
        "tr": "Sonuclar",
        "de": "Ergebnisse",
    },
    "summary": {
        "en": "Summary",
        "tr": "Ozet",
        "de": "Zusammenfassung",
    },
}


def t(key: str, lang: str = "en") -> str:
    """Get translation for a key in the specified language."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang, entry.get("en", key))


def get_lang(st_module=None) -> str:
    """Get the current language from Streamlit session state."""
    if st_module and hasattr(st_module, "session_state"):
        return st_module.session_state.get("lang", "en")
    return "en"


LANG_OPTIONS = {"🇬🇧 English": "en", "🇹🇷 Turkce": "tr", "🇩🇪 Deutsch": "de"}
