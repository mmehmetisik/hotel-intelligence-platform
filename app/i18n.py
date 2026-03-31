"""
Internationalization (i18n) — EN / TR / DE / NO

Simple dictionary-based translation system for the Streamlit UI.
"""

TRANSLATIONS = {
    # ─────────────── Navigation & Global ───────────────
    "app_title": {
        "en": "Hotel Intelligence Platform",
        "tr": "Otel Zeka Platformu",
        "de": "Hotel Intelligence Plattform",
        "no": "Hotel Intelligence Plattform",
    },
    "app_subtitle": {
        "en": "End-to-end AI/ML platform for hospitality analytics",
        "tr": "Konaklama analitiği için uçtan uca AI/ML platformu",
        "de": "End-to-End AI/ML-Plattform fuer Hospitality-Analytik",
        "no": "Ende-til-ende AI/ML-plattform for gjestfrihet-analyse",
    },
    "language": {
        "en": "Language",
        "tr": "Dil",
        "de": "Sprache",
        "no": "Spraak",
    },
    "nav_home": {
        "en": "Home",
        "tr": "Ana Sayfa",
        "de": "Startseite",
        "no": "Hjem",
    },

    # ─────────────── Home Page ───────────────
    "hero_description": {
        "en": "Predictive analytics, LLM-powered unstructured data processing, conversational AI, and production MLOps — all in one platform.",
        "tr": "Tahminsel analitik, LLM destekli yapilandirilmamis veri isleme, konusmaya dayali yapay zeka ve uretim MLOps — hepsi tek platformda.",
        "de": "Praediktive Analytik, LLM-gestuetzte unstrukturierte Datenverarbeitung, Konversations-KI und Produktions-MLOps — alles auf einer Plattform.",
        "no": "Prediktiv analyse, LLM-drevet ustrukturert databehandling, samtale-AI og produksjons-MLOps — alt i en plattform.",
    },
    "explore_modules": {
        "en": "Explore Modules",
        "tr": "Modulleri Kesfet",
        "de": "Module Erkunden",
        "no": "Utforsk Moduler",
    },
    "tech_stack": {
        "en": "Tech Stack",
        "tr": "Teknoloji Yigini",
        "de": "Tech-Stack",
        "no": "Teknologistabel",
    },
    "architecture": {
        "en": "Architecture",
        "tr": "Mimari",
        "de": "Architektur",
        "no": "Arkitektur",
    },

    # ─────────────── Module Names ───────────────
    "mod1_title": {
        "en": "Predictive Analytics",
        "tr": "Tahminsel Analitik",
        "de": "Praediktive Analytik",
        "no": "Prediktiv Analyse",
    },
    "mod1_desc": {
        "en": "Booking cancellation prediction, CLTV modeling, and customer segmentation with XGBoost, BG-NBD, and K-Means.",
        "tr": "XGBoost, BG-NBD ve K-Means ile rezervasyon iptal tahmini, CLTV modelleme ve musteri segmentasyonu.",
        "de": "Buchungsstornierungsvorhersage, CLTV-Modellierung und Kundensegmentierung mit XGBoost, BG-NBD und K-Means.",
        "no": "Bestillingskanselleringsforutsigelse, CLTV-modellering og kundesegmentering med XGBoost, BG-NBD og K-Means.",
    },
    "mod2_title": {
        "en": "LLM & Unstructured Data",
        "tr": "LLM ve Yapilandirilmamis Veri",
        "de": "LLM & Unstrukturierte Daten",
        "no": "LLM & Ustrukturerte Data",
    },
    "mod2_desc": {
        "en": "Invoice classification, master item cleanup with fuzzy matching, and multi-layer sentiment analysis.",
        "tr": "Fatura siniflandirma, bulanik esleme ile ana oge temizligi ve cok katmanli duygu analizi.",
        "de": "Rechnungsklassifizierung, Stammdatenbereinigung mit Fuzzy-Matching und mehrschichtige Sentimentanalyse.",
        "no": "Fakturaklassifisering, stamdata-opprydding med fuzzy-matching og flerlagssentimentanalyse.",
    },
    "mod3_title": {
        "en": "Conversational AI",
        "tr": "Konusmaya Dayali Yapay Zeka",
        "de": "Konversations-KI",
        "no": "Samtale-AI",
    },
    "mod3_desc": {
        "en": "Natural language to SQL chatbot with intent detection, auto-visualization, and business insights.",
        "tr": "Niyet algilama, otomatik gorsellestirme ve is icgoerueleri ile dogal dilden SQL'e chatbot.",
        "de": "Natural-Language-zu-SQL-Chatbot mit Intent-Erkennung, Auto-Visualisierung und Business-Insights.",
        "no": "Naturlig spraak til SQL-chatbot med intensjonsdeteksjon, autovisualisering og forretningsinnsikt.",
    },
    "mod4_title": {
        "en": "MLOps & Monitoring",
        "tr": "MLOps ve Izleme",
        "de": "MLOps & Monitoring",
        "no": "MLOps & Overvaaking",
    },
    "mod4_desc": {
        "en": "MLflow experiment tracking, model registry, data/model drift detection, and alerting system.",
        "tr": "MLflow deney takibi, model kayit defteri, veri/model sapma tespiti ve uyari sistemi.",
        "de": "MLflow-Experimentverfolgung, Modellregistrierung, Daten-/Modelldrifterkennung und Alarmsystem.",
        "no": "MLflow-eksperimentsporing, modellregister, data-/modelldriftdeteksjon og varslingssystem.",
    },

    # ─────────────── KPI Labels ───────────────
    "total_bookings": {
        "en": "Total Bookings",
        "tr": "Toplam Rezervasyon",
        "de": "Gesamtbuchungen",
        "no": "Totale Bestillinger",
    },
    "cancel_rate": {
        "en": "Cancellation Rate",
        "tr": "Iptal Orani",
        "de": "Stornierungsrate",
        "no": "Kanselleringsrate",
    },
    "total_customers": {
        "en": "Total Customers",
        "tr": "Toplam Musteri",
        "de": "Gesamtkunden",
        "no": "Totale Kunder",
    },
    "ml_models": {
        "en": "ML Models",
        "tr": "ML Modelleri",
        "de": "ML-Modelle",
        "no": "ML-Modeller",
    },
    "best_auc": {
        "en": "Best AUC-ROC",
        "tr": "En Iyi AUC-ROC",
        "de": "Bester AUC-ROC",
        "no": "Beste AUC-ROC",
    },
    "avg_revenue": {
        "en": "Avg. Revenue",
        "tr": "Ort. Gelir",
        "de": "Durchschn. Umsatz",
        "no": "Gj.snitt Inntekt",
    },

    # ─────────────── Cancellation Page ───────────────
    "cancel_title": {
        "en": "Booking Cancellation Predictor",
        "tr": "Rezervasyon Iptal Tahmincisi",
        "de": "Buchungsstornierung Vorhersage",
        "no": "Bestillingskanselleringsforutsiger",
    },
    "cancel_desc": {
        "en": "Predict whether a booking will be canceled using machine learning models.",
        "tr": "Makine ogrenimi modelleri kullanarak bir rezervasyonun iptal edilip edilmeyecegini tahmin edin.",
        "de": "Vorhersage, ob eine Buchung storniert wird, mithilfe von ML-Modellen.",
        "no": "Forutsi om en bestilling vil bli kansellert ved hjelp av maskinlaeringsmodeller.",
    },
    "model_comparison": {
        "en": "Model Comparison",
        "tr": "Model Karsilastirmasi",
        "de": "Modellvergleich",
        "no": "Modellsammenligning",
    },
    "feature_importance": {
        "en": "Feature Importance",
        "tr": "Ozellik Onemi",
        "de": "Feature-Wichtigkeit",
        "no": "Funksjonsviktighet",
    },
    "live_prediction": {
        "en": "Live Prediction",
        "tr": "Canli Tahmin",
        "de": "Live-Vorhersage",
        "no": "Live Forutsigelse",
    },
    "business_impact": {
        "en": "Business Impact",
        "tr": "Is Etkisi",
        "de": "Geschaeftsauswirkung",
        "no": "Forretningspavirkning",
    },

    # ─────────────── Customer Intelligence ───────────────
    "cust_title": {
        "en": "Customer Intelligence",
        "tr": "Musteri Zekasi",
        "de": "Kundenintelligenz",
        "no": "Kundeintelligens",
    },
    "rfm_analysis": {
        "en": "RFM Analysis",
        "tr": "RFM Analizi",
        "de": "RFM-Analyse",
        "no": "RFM-Analyse",
    },
    "cltv_prediction": {
        "en": "CLTV Prediction",
        "tr": "CLTV Tahmini",
        "de": "CLTV-Vorhersage",
        "no": "CLTV-Forutsigelse",
    },
    "clustering": {
        "en": "Customer Clustering",
        "tr": "Musteri Kumeleme",
        "de": "Kundensegmentierung",
        "no": "Kundesegmentering",
    },

    # ─────────────── Invoice Classifier ───────────────
    "invoice_title": {
        "en": "Invoice Classifier",
        "tr": "Fatura Siniflandirici",
        "de": "Rechnungsklassifizierer",
        "no": "Fakturaklassifiserer",
    },
    "rule_based": {
        "en": "Rule-Based",
        "tr": "Kural Tabanli",
        "de": "Regelbasiert",
        "no": "Regelbasert",
    },
    "llm_powered": {
        "en": "LLM-Powered",
        "tr": "LLM Destekli",
        "de": "LLM-gestuetzt",
        "no": "LLM-Drevet",
    },

    # ─────────────── Review Analyzer ───────────────
    "review_title": {
        "en": "Review Analyzer",
        "tr": "Yorum Analizcisi",
        "de": "Bewertungsanalyse",
        "no": "Anmeldelseanalysator",
    },
    "sentiment_dist": {
        "en": "Sentiment Distribution",
        "tr": "Duygu Dagilimi",
        "de": "Sentimentverteilung",
        "no": "Sentimentfordeling",
    },
    "aspect_analysis": {
        "en": "Aspect Analysis",
        "tr": "Boyut Analizi",
        "de": "Aspektanalyse",
        "no": "Aspektanalyse",
    },

    # ─────────────── Chatbot ───────────────
    "chat_title": {
        "en": "Analytics Chatbot",
        "tr": "Analitik Chatbot",
        "de": "Analytik-Chatbot",
        "no": "Analyse-Chatbot",
    },
    "chat_placeholder": {
        "en": "Ask a question about your hotel data...",
        "tr": "Otel verileriniz hakkinda bir soru sorun...",
        "de": "Stellen Sie eine Frage zu Ihren Hoteldaten...",
        "no": "Still et spoersmaal om hotelldataene dine...",
    },
    "chat_examples": {
        "en": "Example Questions",
        "tr": "Ornek Sorular",
        "de": "Beispielfragen",
        "no": "Eksempelspoerrsmaal",
    },

    # ─────────────── MLOps ───────────────
    "mlops_title": {
        "en": "MLOps Monitor",
        "tr": "MLOps Izleyici",
        "de": "MLOps-Monitor",
        "no": "MLOps-Monitor",
    },
    "health_score": {
        "en": "Health Score",
        "tr": "Saglik Puani",
        "de": "Gesundheitswert",
        "no": "Helsescore",
    },
    "data_drift": {
        "en": "Data Drift",
        "tr": "Veri Sapmasi",
        "de": "Datendrift",
        "no": "Datadrift",
    },
    "model_performance": {
        "en": "Model Performance",
        "tr": "Model Performansi",
        "de": "Modellleistung",
        "no": "Modellytelse",
    },
    "alerts": {
        "en": "Alerts",
        "tr": "Uyarilar",
        "de": "Warnungen",
        "no": "Varsler",
    },

    # ─────────────── Cancellation Page Details ───────────────
    "best_model": {
        "en": "Best Model",
        "tr": "En Iyi Model",
        "de": "Bestes Modell",
        "no": "Beste Modell",
    },
    "features": {
        "en": "Features",
        "tr": "Ozellikler",
        "de": "Merkmale",
        "no": "Funksjoner",
    },
    "model_perf_comparison": {
        "en": "Model Performance Comparison",
        "tr": "Model Performans Karsilastirmasi",
        "de": "Modellleistungsvergleich",
        "no": "Modellytelsessammenligning",
    },
    "cv_results": {
        "en": "Cross-Validation Results",
        "tr": "Capraz Dogrulama Sonuclari",
        "de": "Kreuzvalidierungsergebnisse",
        "no": "Kryssvalideringsresultater",
    },
    "cv_subtitle": {
        "en": "5-Fold Stratified CV",
        "tr": "5 Katli Tabakalastirilmis CV",
        "de": "5-fache stratifizierte CV",
        "no": "5-fold stratifisert CV",
    },
    "top_feature_importance": {
        "en": "Top 20 Feature Importance",
        "tr": "En Onemli 20 Ozellik",
        "de": "Top 20 Feature-Wichtigkeit",
        "no": "Topp 20 Funksjonsviktighet",
    },
    "make_prediction": {
        "en": "Make a Prediction",
        "tr": "Tahmin Yap",
        "de": "Vorhersage Erstellen",
        "no": "Lag en Forutsigelse",
    },
    "prediction_subtitle": {
        "en": "Enter booking details to predict cancellation risk",
        "tr": "Iptal riskini tahmin etmek icin rezervasyon bilgilerini girin",
        "de": "Geben Sie Buchungsdetails ein, um das Stornierungsrisiko vorherzusagen",
        "no": "Skriv inn bestillingsdetaljer for aa forutsi kanselleringsrisiko",
    },
    "lead_time": {
        "en": "Lead Time (days)",
        "tr": "Teslim Suresi (gun)",
        "de": "Vorlaufzeit (Tage)",
        "no": "Leveringstid (dager)",
    },
    "adr_label": {
        "en": "Average Daily Rate (EUR)",
        "tr": "Ortalama Gunluk Ucret (EUR)",
        "de": "Durchschnittlicher Tagespreis (EUR)",
        "no": "Gjennomsnittlig Dagspris (EUR)",
    },
    "adults": {
        "en": "Adults",
        "tr": "Yetiskinler",
        "de": "Erwachsene",
        "no": "Voksne",
    },
    "hotel_type": {
        "en": "Hotel Type",
        "tr": "Otel Tipi",
        "de": "Hoteltyp",
        "no": "Hotelltype",
    },
    "deposit_type": {
        "en": "Deposit Type",
        "tr": "Depozito Tipi",
        "de": "Einzahlungsart",
        "no": "Depositumstype",
    },
    "market_segment": {
        "en": "Market Segment",
        "tr": "Pazar Segmenti",
        "de": "Marktsegment",
        "no": "Markedssegment",
    },
    "repeated_guest": {
        "en": "Repeated Guest",
        "tr": "Tekrar Eden Misafir",
        "de": "Wiederkehrender Gast",
        "no": "Gjentakende Gjest",
    },
    "prev_cancellations": {
        "en": "Previous Cancellations",
        "tr": "Onceki Iptaller",
        "de": "Vorherige Stornierungen",
        "no": "Tidligere Kanselleringer",
    },
    "special_requests": {
        "en": "Special Requests",
        "tr": "Ozel Istekler",
        "de": "Sonderwuensche",
        "no": "Spesielle Oensker",
    },
    "predict_btn": {
        "en": "Predict Cancellation Risk",
        "tr": "Iptal Riskini Tahmin Et",
        "de": "Stornierungsrisiko Vorhersagen",
        "no": "Forutsi Kanselleringsrisiko",
    },
    "cancel_risk": {
        "en": "Cancellation Risk",
        "tr": "Iptal Riski",
        "de": "Stornierungsrisiko",
        "no": "Kanselleringsrisiko",
    },
    "risk_score": {
        "en": "Risk Score",
        "tr": "Risk Puani",
        "de": "Risikobewertung",
        "no": "Risikoscore",
    },
    "high_risk": {
        "en": "HIGH",
        "tr": "YUKSEK",
        "de": "HOCH",
        "no": "HOEY",
    },
    "medium_risk": {
        "en": "MEDIUM",
        "tr": "ORTA",
        "de": "MITTEL",
        "no": "MIDDELS",
    },
    "low_risk": {
        "en": "LOW",
        "tr": "DUSUK",
        "de": "NIEDRIG",
        "no": "LAV",
    },
    "risk_label": {
        "en": "RISK",
        "tr": "RISK",
        "de": "RISIKO",
        "no": "RISIKO",
    },
    "revenue_impact": {
        "en": "Revenue Impact Analysis",
        "tr": "Gelir Etki Analizi",
        "de": "Umsatzauswirkungsanalyse",
        "no": "Inntektspaavirkningsanalyse",
    },
    "revenue_subtitle": {
        "en": "Estimated savings from cancellation prediction",
        "tr": "Iptal tahmininden tahmini tasarruflar",
        "de": "Geschaetzte Einsparungen durch Stornierungsvorhersage",
        "no": "Estimerte besparelser fra kanselleringsforutsigelse",
    },
    "threshold": {
        "en": "Threshold",
        "tr": "Esik Degeri",
        "de": "Schwellenwert",
        "no": "Terskelverdi",
    },
    "cancels_caught": {
        "en": "Cancellations Caught",
        "tr": "Yakalanan Iptaller",
        "de": "Erfasste Stornierungen",
        "no": "Fangede Kanselleringer",
    },
    "recovery_rate": {
        "en": "Recovery Rate",
        "tr": "Kurtarma Orani",
        "de": "Wiederherstellungsrate",
        "no": "Gjenopprettingsrate",
    },
    "revenue_saved": {
        "en": "Revenue Saved (EUR)",
        "tr": "Kurtarilan Gelir (EUR)",
        "de": "Eingesparter Umsatz (EUR)",
        "no": "Spart Inntekt (EUR)",
    },
    "impact_message": {
        "en": "With the best model (AUC: {auc}), the hotel can proactively address high-risk bookings and potentially save <b>EUR 2M+</b> annually in recovered revenue.",
        "tr": "En iyi model (AUC: {auc}) ile otel, yuksek riskli rezervasyonlari proaktif olarak yonetebilir ve yillik <b>2M+ EUR</b> gelir kurtarabilir.",
        "de": "Mit dem besten Modell (AUC: {auc}) kann das Hotel Hochrisiko-Buchungen proaktiv behandeln und jaehrlich <b>2M+ EUR</b> an Umsatz einsparen.",
        "no": "Med den beste modellen (AUC: {auc}) kan hotellet proaktivt haandtere hoeyrisikobestillinger og potensielt spare <b>2M+ EUR</b> aarlig.",
    },

    # ─────────────── Common ───────────────
    "loading": {
        "en": "Loading...",
        "tr": "Yukleniyor...",
        "de": "Laden...",
        "no": "Laster...",
    },
    "error": {
        "en": "An error occurred",
        "tr": "Bir hata olustu",
        "de": "Ein Fehler ist aufgetreten",
        "no": "En feil oppstod",
    },
    "no_data": {
        "en": "No data available. Run the pipeline first.",
        "tr": "Veri mevcut degil. Oncelikle veri hattini calistirin.",
        "de": "Keine Daten verfuegbar. Fuehren Sie zuerst die Pipeline aus.",
        "no": "Ingen data tilgjengelig. Kjoer pipelinen foerst.",
    },
    "download": {
        "en": "Download",
        "tr": "Indir",
        "de": "Herunterladen",
        "no": "Last ned",
    },
    "filters": {
        "en": "Filters",
        "tr": "Filtreler",
        "de": "Filter",
        "no": "Filtre",
    },
    "results": {
        "en": "Results",
        "tr": "Sonuclar",
        "de": "Ergebnisse",
        "no": "Resultater",
    },
    "summary": {
        "en": "Summary",
        "tr": "Ozet",
        "de": "Zusammenfassung",
        "no": "Sammendrag",
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


LANG_OPTIONS = {
    "🇬🇧 English": "en",
    "🇹🇷 Turkce": "tr",
    "🇩🇪 Deutsch": "de",
    "🇳🇴 Norsk": "no",
}
