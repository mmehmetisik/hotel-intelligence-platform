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

    # ─────────────── MLOps Page Details ───────────────
    "mlops_desc": {
        "en": "Real-time model monitoring, data drift detection, and alerting",
        "tr": "Gercek zamanli model izleme, veri sapmasi tespiti ve uyari",
        "de": "Echtzeit-Modellueberwachung, Datendrifterkennung und Alarmierung",
        "no": "Sanntids modellovervaakning, datadriftdeteksjon og varsling",
    },
    "data_drift_analysis": {
        "en": "Data Drift Analysis",
        "tr": "Veri Sapmasi Analizi",
        "de": "Datendriftanalyse",
        "no": "Datadriftanalyse",
    },
    "drift_subtitle": {
        "en": "PSI and KS test results for feature distributions",
        "tr": "Ozellik dagilimlarinin PSI ve KS test sonuclari",
        "de": "PSI- und KS-Testergebnisse fuer Merkmalverteilungen",
        "no": "PSI- og KS-testresultater for funksjonsfordelinger",
    },
    "simulate_drift": {
        "en": "Simulate Drift Level",
        "tr": "Sapma Seviyesi Simule Et",
        "de": "Driftniveau Simulieren",
        "no": "Simuler Driftnivaa",
    },
    "features_analyzed": {
        "en": "Features Analyzed",
        "tr": "Analiz Edilen Ozellikler",
        "de": "Analysierte Merkmale",
        "no": "Analyserte Funksjoner",
    },
    "drifted_features": {
        "en": "Drifted Features",
        "tr": "Sapma Gosteren Ozellikler",
        "de": "Gedriftete Merkmale",
        "no": "Driftede Funksjoner",
    },
    "overall_severity": {
        "en": "Overall Severity",
        "tr": "Genel Siddet",
        "de": "Gesamtschweregrad",
        "no": "Samlet Alvorlighetsgrad",
    },
    "perf_tracking": {
        "en": "Model Performance Tracking",
        "tr": "Model Performans Takibi",
        "de": "Modellleistungsverfolgung",
        "no": "Modellytelsesoppfoelging",
    },
    "perf_subtitle": {
        "en": "AUC-ROC, F1, Precision, Recall over time",
        "tr": "Zaman icinde AUC-ROC, F1, Precision, Recall",
        "de": "AUC-ROC, F1, Precision, Recall im Zeitverlauf",
        "no": "AUC-ROC, F1, Presisjon, Recall over tid",
    },
    "simulate_degradation": {
        "en": "Simulate Performance Degradation",
        "tr": "Performans Dususu Simule Et",
        "de": "Leistungsabfall Simulieren",
        "no": "Simuler Ytelsesforringelse",
    },
    "alert_dashboard": {
        "en": "Alert Dashboard",
        "tr": "Uyari Paneli",
        "de": "Alarm-Dashboard",
        "no": "Varselpanel",
    },
    "alert_subtitle": {
        "en": "Threshold-based monitoring alerts",
        "tr": "Esik deger tabanli izleme uyarilari",
        "de": "Schwellenwertbasierte Ueberwachungsalarme",
        "no": "Terskelbaserte overvaakningsvarsler",
    },
    "experiment_tracking": {
        "en": "Experiment Tracking",
        "tr": "Deney Takibi",
        "de": "Experimentverfolgung",
        "no": "Eksperimentsporing",
    },
    "exp_subtitle": {
        "en": "Model training history and comparisons",
        "tr": "Model egitim gecmisi ve karsilastirmalar",
        "de": "Modelltrainingshistorie und Vergleiche",
        "no": "Modelltreningshistorikk og sammenligninger",
    },
    "model_registry": {
        "en": "Model Registry",
        "tr": "Model Kayit Defteri",
        "de": "Modellregistrierung",
        "no": "Modellregister",
    },
    "acknowledge_all": {
        "en": "Acknowledge All Alerts",
        "tr": "Tum Uyarilari Onayla",
        "de": "Alle Alarme Bestaetigen",
        "no": "Bekreft Alle Varsler",
    },
    "no_alerts": {
        "en": "No alerts — all systems operating normally.",
        "tr": "Uyari yok — tum sistemler normal calisiyor.",
        "de": "Keine Alarme — alle Systeme arbeiten normal.",
        "no": "Ingen varsler — alle systemer fungerer normalt.",
    },
    "perf_metrics_time": {
        "en": "Performance Metrics Over Time",
        "tr": "Zaman Icinde Performans Metrikleri",
        "de": "Leistungsmetriken im Zeitverlauf",
        "no": "Ytelsesmetrikker Over Tid",
    },
    "data_quality": {
        "en": "Data Quality",
        "tr": "Veri Kalitesi",
        "de": "Datenqualitaet",
        "no": "Datakvalitet",
    },
    "system_health": {
        "en": "System Health",
        "tr": "Sistem Sagligi",
        "de": "Systemgesundheit",
        "no": "Systemhelse",
    },

    # ─────────────── Customer Intelligence Page ───────────────
    "cust_desc": {
        "en": "RFM segmentation, CLTV prediction, and behavioral clustering",
        "tr": "RFM segmentasyonu, CLTV tahmini ve davranissal kumeleme",
        "de": "RFM-Segmentierung, CLTV-Vorhersage und Verhaltensclustering",
        "no": "RFM-segmentering, CLTV-forutsigelse og atferdsklynging",
    },
    "avg_frequency": {
        "en": "Avg. Frequency",
        "tr": "Ort. Frekans",
        "de": "Durchschn. Haeufigkeit",
        "no": "Gj.snitt Frekvens",
    },
    "total_revenue": {
        "en": "Total Revenue",
        "tr": "Toplam Gelir",
        "de": "Gesamtumsatz",
        "no": "Total Inntekt",
    },
    "customer_segments": {
        "en": "Customer Segments",
        "tr": "Musteri Segmentleri",
        "de": "Kundensegmente",
        "no": "Kundesegmenter",
    },
    "rfm_scatter_title": {
        "en": "RFM Scatter: Recency vs Monetary (size = Frequency)",
        "tr": "RFM Dagitimi: Yakinlik vs Parasal (boyut = Frekans)",
        "de": "RFM-Streuung: Recency vs Monetaer (Groesse = Haeufigkeit)",
        "no": "RFM-spredning: Recency vs Monetaer (stoerrelse = Frekvens)",
    },
    "cltv_section_title": {
        "en": "Customer Lifetime Value Prediction",
        "tr": "Musteri Yasam Boyu Degeri Tahmini",
        "de": "Customer-Lifetime-Value-Vorhersage",
        "no": "Kundelivstidsverdi-forutsigelse",
    },
    "cltv_section_subtitle": {
        "en": "BG-NBD + Gamma-Gamma Model",
        "tr": "BG-NBD + Gamma-Gamma Modeli",
        "de": "BG-NBD + Gamma-Gamma-Modell",
        "no": "BG-NBD + Gamma-Gamma-modell",
    },
    "cltv_distribution": {
        "en": "CLTV Distribution",
        "tr": "CLTV Dagilimi",
        "de": "CLTV-Verteilung",
        "no": "CLTV-fordeling",
    },
    "avg_cltv_by_segment": {
        "en": "Average CLTV by Segment",
        "tr": "Segmente Gore Ortalama CLTV",
        "de": "Durchschnittlicher CLTV nach Segment",
        "no": "Gjennomsnittlig CLTV etter Segment",
    },
    "top10_customers": {
        "en": "Top 10 Highest Value Customers",
        "tr": "En Degerli 10 Musteri",
        "de": "Top 10 Kunden mit hoechstem Wert",
        "no": "Topp 10 Kunder med Hoeyest Verdi",
    },
    "clustering_subtitle": {
        "en": "K-Means on spending patterns",
        "tr": "Harcama kaliplari uzerinde K-Means",
        "de": "K-Means auf Ausgabenmuster",
        "no": "K-Means paa forbruksmoenstre",
    },
    "num_clusters": {
        "en": "Number of Clusters",
        "tr": "Kume Sayisi",
        "de": "Anzahl der Cluster",
        "no": "Antall Klynger",
    },
    "cluster_scatter_title": {
        "en": "Customer Clusters: Spend vs Frequency",
        "tr": "Musteri Kumeleri: Harcama vs Frekans",
        "de": "Kundencluster: Ausgaben vs Haeufigkeit",
        "no": "Kundeklynger: Forbruk vs Frekvens",
    },
    "cluster_profiles": {
        "en": "Cluster Profiles (Normalized)",
        "tr": "Kume Profilleri (Normallesmis)",
        "de": "Clusterprofile (Normalisiert)",
        "no": "Klyngeprofiler (Normalisert)",
    },

    # ─────────────── Invoice Classifier Page ───────────────
    "invoice_desc": {
        "en": "Rule-based vs LLM-powered invoice line classification",
        "tr": "Kural tabanli vs LLM destekli fatura satiri siniflandirmasi",
        "de": "Regelbasierte vs LLM-gestuetzte Rechnungszeilenklassifizierung",
        "no": "Regelbasert vs LLM-drevet fakturalinjenklassifisering",
    },
    "total_invoice_lines": {
        "en": "Total Invoice Lines",
        "tr": "Toplam Fatura Satiri",
        "de": "Gesamte Rechnungszeilen",
        "no": "Totale Fakturalinjer",
    },
    "categories": {
        "en": "Categories",
        "tr": "Kategoriler",
        "de": "Kategorien",
        "no": "Kategorier",
    },
    "rule_based_accuracy": {
        "en": "Rule-Based Accuracy",
        "tr": "Kural Tabanli Dogruluk",
        "de": "Regelbasierte Genauigkeit",
        "no": "Regelbasert Noeyyaktighet",
    },
    "llm_accuracy": {
        "en": "LLM Accuracy",
        "tr": "LLM Dogrulugu",
        "de": "LLM-Genauigkeit",
        "no": "LLM-Noeyyaktighet",
    },
    "category_analysis": {
        "en": "Category Analysis",
        "tr": "Kategori Analizi",
        "de": "Kategorieanalyse",
        "no": "Kategorianalyse",
    },
    "live_demo": {
        "en": "Live Demo",
        "tr": "Canli Demo",
        "de": "Live-Demo",
        "no": "Live Demo",
    },
    "accuracy_by_method": {
        "en": "Classification Accuracy by Method",
        "tr": "Yonteme Gore Siniflandirma Dogrulugu",
        "de": "Klassifikationsgenauigkeit nach Methode",
        "no": "Klassifiseringsnoeyyaktighet etter Metode",
    },
    "latency_by_method": {
        "en": "Latency per Classification (ms)",
        "tr": "Siniflandirma Basina Gecikme (ms)",
        "de": "Latenz pro Klassifizierung (ms)",
        "no": "Ventetid per Klassifisering (ms)",
    },
    "invoice_key_insight": {
        "en": "<b>Key Insight:</b> Rule-based achieves 92.65% accuracy at near-zero latency. LLM few-shot reaches 96.8% but at 600x the latency. The hybrid approach (rule-based first, LLM fallback) gives the best of both worlds.",
        "tr": "<b>Onemli Bilgi:</b> Kural tabanli, neredeyse sifir gecikmeyle %92.65 dogruluk saglar. LLM few-shot %96.8'e ulasir ancak 600 kat daha fazla gecikmeyle. Hibrit yaklasim (once kural tabanli, sonra LLM) her iki dunyanin en iyisini sunar.",
        "de": "<b>Wichtige Erkenntnis:</b> Regelbasiert erreicht 92,65% Genauigkeit bei nahezu null Latenz. LLM Few-Shot erreicht 96,8%, aber mit 600-facher Latenz. Der hybride Ansatz (erst regelbasiert, dann LLM-Fallback) bietet das Beste aus beiden Welten.",
        "no": "<b>Viktig Innsikt:</b> Regelbasert oppnaar 92,65% noeyyaktighet med nesten null ventetid. LLM few-shot naar 96,8% men med 600x ventetiden. Hybridtilnaermingen (regelbasert foerst, LLM-reserve) gir det beste fra begge verdener.",
    },
    "invoice_cat_distribution": {
        "en": "Invoice Category Distribution",
        "tr": "Fatura Kategori Dagilimi",
        "de": "Rechnungskategorieverteilung",
        "no": "Fakturakategorifordeling",
    },
    "items_per_category": {
        "en": "Items per Category",
        "tr": "Kategori Basina Oge",
        "de": "Artikel pro Kategorie",
        "no": "Elementer per Kategori",
    },
    "sample_items_by_cat": {
        "en": "Sample Items by Category",
        "tr": "Kategoriye Gore Ornek Ogeler",
        "de": "Beispielartikel nach Kategorie",
        "no": "Eksempler etter Kategori",
    },
    "select_category": {
        "en": "Select Category",
        "tr": "Kategori Sec",
        "de": "Kategorie Auswaehlen",
        "no": "Velg Kategori",
    },
    "classify_invoice_line": {
        "en": "Classify an Invoice Line",
        "tr": "Bir Fatura Satirini Siniflandir",
        "de": "Eine Rechnungszeile Klassifizieren",
        "no": "Klassifiser en Fakturalinje",
    },
    "classify_subtitle": {
        "en": "Enter a description to classify",
        "tr": "Siniflandirmak icin bir aciklama girin",
        "de": "Geben Sie eine Beschreibung zur Klassifizierung ein",
        "no": "Skriv inn en beskrivelse for aa klassifisere",
    },
    "invoice_description": {
        "en": "Invoice Description",
        "tr": "Fatura Aciklamasi",
        "de": "Rechnungsbeschreibung",
        "no": "Fakturabeskrivelse",
    },
    "invoice_placeholder": {
        "en": "e.g., Sparkling water 500ml, Fresh salmon fillet, Bathroom towels",
        "tr": "oern., Maden suyu 500ml, Taze somon fileto, Banyo havlulari",
        "de": "z.B., Sprudelwasser 500ml, Frisches Lachsfilet, Badezimmerhandtuecher",
        "no": "f.eks., Mineralvann 500ml, Fersk laksefilet, Baaderomshaandklaer",
    },
    "classify_btn": {
        "en": "Classify",
        "tr": "Siniflandir",
        "de": "Klassifizieren",
        "no": "Klassifiser",
    },
    "classification_result": {
        "en": "Classification Result",
        "tr": "Siniflandirma Sonucu",
        "de": "Klassifizierungsergebnis",
        "no": "Klassifiseringsresultat",
    },
    "method_confidence": {
        "en": "Method: Rule-Based | Confidence: High",
        "tr": "Yontem: Kural Tabanli | Guven: Yuksek",
        "de": "Methode: Regelbasiert | Konfidenz: Hoch",
        "no": "Metode: Regelbasert | Konfidens: Hoey",
    },
    "classification_error": {
        "en": "Classification error",
        "tr": "Siniflandirma hatasi",
        "de": "Klassifizierungsfehler",
        "no": "Klassifiseringsfeil",
    },

    # ─────────────── Item Cleanup Page ───────────────
    "item_cleanup_title": {
        "en": "Master Item Cleanup",
        "tr": "Ana Oge Temizligi",
        "de": "Stammdatenbereinigung",
        "no": "Stamdata-opprydding",
    },
    "item_cleanup_desc": {
        "en": "4-layer hybrid matching pipeline: Exact -> Fuzzy -> TF-IDF Embedding -> Fuzzy Relaxed",
        "tr": "4 katmanli hibrit eslestirme hatti: Birebir -> Bulanik -> TF-IDF Gomme -> Bulanik Gevsetilmis",
        "de": "4-Schicht-Hybrid-Matching-Pipeline: Exakt -> Fuzzy -> TF-IDF-Einbettung -> Fuzzy Relaxed",
        "no": "4-lags hybrid-matchingpipeline: Eksakt -> Fuzzy -> TF-IDF-innbygging -> Fuzzy Avslappet",
    },
    "dirty_items": {
        "en": "Dirty Items",
        "tr": "Kirli Ogeler",
        "de": "Unsaubere Artikel",
        "no": "Urene Elementer",
    },
    "standard_items": {
        "en": "Standard Items",
        "tr": "Standart Ogeler",
        "de": "Standardartikel",
        "no": "Standardelementer",
    },
    "pipeline_layers": {
        "en": "Pipeline Layers",
        "tr": "Hat Katmanlari",
        "de": "Pipeline-Schichten",
        "no": "Pipelinelag",
    },
    "pipeline_overview": {
        "en": "Pipeline Overview",
        "tr": "Hat Genel Bakisi",
        "de": "Pipeline-Uebersicht",
        "no": "Pipelineoversikt",
    },
    "match_analysis": {
        "en": "Match Analysis",
        "tr": "Eslestirme Analizi",
        "de": "Match-Analyse",
        "no": "Treffanalyse",
    },
    "live_matching": {
        "en": "Live Matching",
        "tr": "Canli Eslestirme",
        "de": "Live-Matching",
        "no": "Live Matching",
    },
    "pipeline_title": {
        "en": "4-Layer Hybrid Matching Pipeline",
        "tr": "4 Katmanli Hibrit Eslestirme Hatti",
        "de": "4-Schicht-Hybrid-Matching-Pipeline",
        "no": "4-lags Hybrid-Matchingpipeline",
    },
    "layer1_desc": {
        "en": "Exact Match",
        "tr": "Birebir Eslestirme",
        "de": "Exakte Uebereinstimmung",
        "no": "Eksakt Treff",
    },
    "layer1_detail": {
        "en": "Direct string comparison after normalization",
        "tr": "Normalizasyondan sonra dogrudan dize karsilastirmasi",
        "de": "Direkter Zeichenkettenvergleich nach Normalisierung",
        "no": "Direkte strengsammenligning etter normalisering",
    },
    "layer2_desc": {
        "en": "Fuzzy Match (threshold=82)",
        "tr": "Bulanik Eslestirme (esik=82)",
        "de": "Fuzzy-Match (Schwelle=82)",
        "no": "Fuzzy-treff (terskel=82)",
    },
    "layer2_detail": {
        "en": "RapidFuzz WRatio for close matches",
        "tr": "Yakin eslesmeler icin RapidFuzz WRatio",
        "de": "RapidFuzz WRatio fuer nahe Uebereinstimmungen",
        "no": "RapidFuzz WRatio for naere treff",
    },
    "layer3_desc": {
        "en": "TF-IDF Embedding",
        "tr": "TF-IDF Gomme",
        "de": "TF-IDF-Einbettung",
        "no": "TF-IDF-innbygging",
    },
    "layer3_detail": {
        "en": "Character n-gram cosine similarity",
        "tr": "Karakter n-gram kosinus benzerligi",
        "de": "Zeichen-n-Gramm-Kosinusaehnlichkeit",
        "no": "Tegn n-gram kosinuslikhet",
    },
    "layer4_desc": {
        "en": "Fuzzy Relaxed (threshold=60)",
        "tr": "Bulanik Gevsetilmis (esik=60)",
        "de": "Fuzzy Relaxed (Schwelle=60)",
        "no": "Fuzzy Avslappet (terskel=60)",
    },
    "layer4_detail": {
        "en": "Catch remaining abbreviations",
        "tr": "Kalan kisaltmalari yakala",
        "de": "Verbleibende Abkuerzungen auffangen",
        "no": "Fang gjenvaerende forkortelser",
    },
    "pipeline_funnel_title": {
        "en": "Pipeline Funnel: Items Matched per Layer",
        "tr": "Hat Hunisi: Katman Basina Eslesen Ogeler",
        "de": "Pipeline-Trichter: Zugeordnete Artikel pro Schicht",
        "no": "Pipeline-trakt: Matchede Elementer per Lag",
    },
    "match_accuracy_by_layer": {
        "en": "Match Accuracy by Layer",
        "tr": "Katmana Gore Eslestirme Dogrulugu",
        "de": "Match-Genauigkeit nach Schicht",
        "no": "Treffnoeyyaktighet etter Lag",
    },
    "category_distribution": {
        "en": "Category Distribution",
        "tr": "Kategori Dagilimi",
        "de": "Kategorieverteilung",
        "no": "Kategorifordeling",
    },
    "items_by_category": {
        "en": "Items by Category",
        "tr": "Kategoriye Gore Ogeler",
        "de": "Artikel nach Kategorie",
        "no": "Elementer etter Kategori",
    },
    "dirty_standard_examples": {
        "en": "Dirty -> Standard Mapping Examples",
        "tr": "Kirli -> Standart Eslestirme Ornekleri",
        "de": "Unsauber -> Standard-Zuordnungsbeispiele",
        "no": "Uren -> Standard Tilordningseksempler",
    },
    "test_matching_pipeline": {
        "en": "Test the Matching Pipeline",
        "tr": "Eslestirme Hattini Test Et",
        "de": "Die Matching-Pipeline Testen",
        "no": "Test Matchingpipelinen",
    },
    "enter_dirty_name": {
        "en": "Enter a dirty product name",
        "tr": "Kirli bir urun adi girin",
        "de": "Einen unsauberen Produktnamen eingeben",
        "no": "Skriv inn et urent produktnavn",
    },
    "dirty_item_name": {
        "en": "Dirty Item Name",
        "tr": "Kirli Oge Adi",
        "de": "Unsauberer Artikelname",
        "no": "Urent Elementnavn",
    },
    "dirty_item_placeholder": {
        "en": "e.g., spag bol, chkn brst, org juce",
        "tr": "oern., spag bol, tavk gogsue, org meysu",
        "de": "z.B., Spag Bol, Hnchn Brst, Org Saft",
        "no": "f.eks., spag bol, kyll brst, org juice",
    },
    "fuzzy_threshold": {
        "en": "Fuzzy Match Threshold",
        "tr": "Bulanik Eslestirme Esigi",
        "de": "Fuzzy-Match-Schwellenwert",
        "no": "Fuzzy-treff-terskel",
    },
    "find_match_btn": {
        "en": "Find Match",
        "tr": "Eslestirme Bul",
        "de": "Match Finden",
        "no": "Finn Treff",
    },
    "best_match": {
        "en": "Best Match",
        "tr": "En Iyi Eslestirme",
        "de": "Beste Uebereinstimmung",
        "no": "Beste Treff",
    },
    "confidence_label": {
        "en": "Confidence",
        "tr": "Guven",
        "de": "Konfidenz",
        "no": "Konfidens",
    },
    "input_label": {
        "en": "Input",
        "tr": "Girdi",
        "de": "Eingabe",
        "no": "Inndata",
    },
    "no_match_found": {
        "en": "No match found above threshold ({threshold}%). Best: {best} ({score}%)",
        "tr": "Esik uzerinde eslestirme bulunamadi ({threshold}%). En iyi: {best} ({score}%)",
        "de": "Kein Treffer ueber Schwellenwert ({threshold}%). Bester: {best} ({score}%)",
        "no": "Ingen treff over terskel ({threshold}%). Beste: {best} ({score}%)",
    },
    "rapidfuzz_missing": {
        "en": "rapidfuzz not installed. Run: pip install rapidfuzz",
        "tr": "rapidfuzz yuklu degil. Calistirin: pip install rapidfuzz",
        "de": "rapidfuzz nicht installiert. Ausfuehren: pip install rapidfuzz",
        "no": "rapidfuzz ikke installert. Kjoer: pip install rapidfuzz",
    },

    # ─────────────── Review Analyzer Page ───────────────
    "review_desc": {
        "en": "Multi-layer sentiment analysis with aspect-level breakdown",
        "tr": "Boyut duezeyinde doekuemle cok katmanli duygu analizi",
        "de": "Mehrschichtige Sentimentanalyse mit aspektbasierter Aufschluesselung",
        "no": "Flerlagssentimentanalyse med aspektnivaafordeling",
    },
    "total_reviews": {
        "en": "Total Reviews",
        "tr": "Toplam Yorum",
        "de": "Gesamtbewertungen",
        "no": "Totale Anmeldelser",
    },
    "avg_rating": {
        "en": "Avg Rating",
        "tr": "Ort. Puan",
        "de": "Durchschn. Bewertung",
        "no": "Gj.snitt Vurdering",
    },
    "positive_rate": {
        "en": "Positive Rate",
        "tr": "Pozitif Oran",
        "de": "Positivrate",
        "no": "Positiv Rate",
    },
    "hotels_covered": {
        "en": "Hotels Covered",
        "tr": "Kapsanan Oteller",
        "de": "Erfasste Hotels",
        "no": "Dekkede Hoteller",
    },
    "hotel_filter": {
        "en": "Hotel",
        "tr": "Otel",
        "de": "Hotel",
        "no": "Hotell",
    },
    "sentiment_filter": {
        "en": "Sentiment",
        "tr": "Duygu",
        "de": "Sentiment",
        "no": "Sentiment",
    },
    "reviews_tab": {
        "en": "Reviews",
        "tr": "Yorumlar",
        "de": "Bewertungen",
        "no": "Anmeldelser",
    },
    "rating_distribution": {
        "en": "Rating Distribution",
        "tr": "Puan Dagilimi",
        "de": "Bewertungsverteilung",
        "no": "Vurderingsfordeling",
    },
    "sentiment_by_hotel": {
        "en": "Sentiment by Hotel",
        "tr": "Otele Gore Duygu",
        "de": "Sentiment nach Hotel",
        "no": "Sentiment etter Hotell",
    },
    "avg_aspect_scores": {
        "en": "Average Aspect Scores (1-5)",
        "tr": "Ortalama Boyut Puanlari (1-5)",
        "de": "Durchschnittliche Aspektbewertungen (1-5)",
        "no": "Gjennomsnittlige Aspektscorer (1-5)",
    },
    "aspect_radar": {
        "en": "Aspect Radar Chart",
        "tr": "Boyut Radar Grafigi",
        "de": "Aspekt-Radardiagramm",
        "no": "Aspektradardiagram",
    },
    "aspect_by_sentiment": {
        "en": "Aspect Scores by Sentiment",
        "tr": "Duyguya Gore Boyut Puanlari",
        "de": "Aspektbewertungen nach Sentiment",
        "no": "Aspektscorer etter Sentiment",
    },
    "aspect_not_found": {
        "en": "Aspect columns not found in data.",
        "tr": "Veri icinde boyut sutunlari bulunamadi.",
        "de": "Aspektspalten in den Daten nicht gefunden.",
        "no": "Aspektkolonner ikke funnet i dataene.",
    },
    "browse_reviews": {
        "en": "Browse Reviews",
        "tr": "Yorumlara Goz At",
        "de": "Bewertungen Durchsuchen",
        "no": "Bla Gjennom Anmeldelser",
    },
    "sort_by": {
        "en": "Sort by",
        "tr": "Sirala",
        "de": "Sortieren nach",
        "no": "Sorter etter",
    },
    "ascending": {
        "en": "Ascending",
        "tr": "Artan",
        "de": "Aufsteigend",
        "no": "Stigende",
    },

    # ─────────────── Analytics Chatbot Page ───────────────
    "chat_desc": {
        "en": "Ask questions about your hotel data in natural language",
        "tr": "Otel verileriniz hakkinda dogal dilde sorular sorun",
        "de": "Stellen Sie Fragen zu Ihren Hoteldaten in natuerlicher Sprache",
        "no": "Still spoersmaal om hotelldataene dine paa naturlig spraak",
    },
    "chatbot_ready": {
        "en": "Chatbot Ready — Groq LLM Connected",
        "tr": "Chatbot Hazir — Groq LLM Bagli",
        "de": "Chatbot Bereit — Groq LLM Verbunden",
        "no": "Chatbot Klar — Groq LLM Tilkoblet",
    },
    "chatbot_offline": {
        "en": "Chatbot Offline",
        "tr": "Chatbot Cevrimdisi",
        "de": "Chatbot Offline",
        "no": "Chatbot Frakoblet",
    },
    "visualization": {
        "en": "Visualization",
        "tr": "Gorsellestirme",
        "de": "Visualisierung",
        "no": "Visualisering",
    },
    "chart_placeholder_msg": {
        "en": "Chart will appear here when you ask a data question.",
        "tr": "Bir veri sorusu sordugunuzda grafik burada gorunecek.",
        "de": "Das Diagramm erscheint hier, wenn Sie eine Datenfrage stellen.",
        "no": "Diagram vil vises her naar du stiller et dataspoersmaal.",
    },
    "viz_placeholder_msg": {
        "en": "Charts and data tables will appear here<br>when you ask a question",
        "tr": "Bir soru sordugunuzda grafikler ve veri tablolari<br>burada gorunecek",
        "de": "Diagramme und Datentabellen erscheinen hier,<br>wenn Sie eine Frage stellen",
        "no": "Diagrammer og datatabeller vises her<br>naar du stiller et spoersmaal",
    },
    "view_raw_data": {
        "en": "View Raw Data",
        "tr": "Ham Veriyi Goruntule",
        "de": "Rohdaten Anzeigen",
        "no": "Vis Raadata",
    },
    "how_it_works": {
        "en": "How it works",
        "tr": "Nasil Calisir",
        "de": "So funktioniert es",
        "no": "Slik Fungerer Det",
    },
    "pipeline_architecture": {
        "en": "Pipeline Architecture",
        "tr": "Hat Mimarisi",
        "de": "Pipeline-Architektur",
        "no": "Pipelinearkitektur",
    },
    "intent_detection": {
        "en": "Intent Detection",
        "tr": "Niyet Algilama",
        "de": "Intent-Erkennung",
        "no": "Intensjonsdeteksjon",
    },
    "intent_detail": {
        "en": "LLM classifies question into: sql_query, prediction, recommendation, summary, explanation",
        "tr": "LLM soruyu siniflandirir: sql_query, prediction, recommendation, summary, explanation",
        "de": "LLM klassifiziert die Frage in: sql_query, prediction, recommendation, summary, explanation",
        "no": "LLM klassifiserer spoersmaal i: sql_query, prediction, recommendation, summary, explanation",
    },
    "sql_generation": {
        "en": "SQL Generation",
        "tr": "SQL Olusturma",
        "de": "SQL-Generierung",
        "no": "SQL-generering",
    },
    "sql_gen_detail": {
        "en": "Schema-aware NL-to-SQL with safety validation (no DROP/DELETE)",
        "tr": "Sema bilincli NL-SQL donusumu, guvenlik dogrulamasi ile (DROP/DELETE yok)",
        "de": "Schemabasierte NL-zu-SQL mit Sicherheitsvalidierung (kein DROP/DELETE)",
        "no": "Skjemabevisst NL-til-SQL med sikkerhetsvalidering (ingen DROP/DELETE)",
    },
    "execution": {
        "en": "Execution",
        "tr": "Calistirma",
        "de": "Ausfuehrung",
        "no": "Utfoerelse",
    },
    "execution_detail": {
        "en": "Query runs against SQLite analytics database (119K+ records)",
        "tr": "Sorgu SQLite analitik veritabaninda calisir (119K+ kayit)",
        "de": "Abfrage wird gegen SQLite-Analysedatenbank ausgefuehrt (119K+ Datensaetze)",
        "no": "Spoerring kjoeres mot SQLite-analysedatabase (119K+ poster)",
    },
    "insight_generation": {
        "en": "Insight Generation",
        "tr": "Icgoeruesue Olusturma",
        "de": "Insight-Generierung",
        "no": "Innsiktsgenerering",
    },
    "insight_detail": {
        "en": "LLM generates natural language business insights from results",
        "tr": "LLM sonuclardan dogal dilde is icgoerueleri olusturur",
        "de": "LLM generiert natuerlichsprachliche Business-Insights aus Ergebnissen",
        "no": "LLM genererer forretningsinnsikt paa naturlig spraak fra resultater",
    },
    "auto_viz": {
        "en": "Auto-Visualization",
        "tr": "Otomatik Gorsellestirme",
        "de": "Auto-Visualisierung",
        "no": "Autovisualisering",
    },
    "auto_viz_detail": {
        "en": "Detects optimal chart type (bar, line, pie, scatter, metric)",
        "tr": "Optimal grafik turunu tespit eder (bar, cizgi, pasta, dagitim, metrik)",
        "de": "Erkennt optimalen Diagrammtyp (Balken, Linie, Kreis, Streuung, Metrik)",
        "no": "Oppdager optimal diagramtype (soyle, linje, kake, spredning, metrikk)",
    },
    "llm_routing": {
        "en": "LLM Routing:",
        "tr": "LLM Yoenlendirme:",
        "de": "LLM-Routing:",
        "no": "LLM-ruting:",
    },
    "llm_routing_detail": {
        "en": "Cache (diskcache) -> Groq API (LLaMA 3.3 70B) -> Fallback",
        "tr": "Onbellek (diskcache) -> Groq API (LLaMA 3.3 70B) -> Yedek",
        "de": "Cache (diskcache) -> Groq API (LLaMA 3.3 70B) -> Fallback",
        "no": "Cache (diskcache) -> Groq API (LLaMA 3.3 70B) -> Reserve",
    },
    "clear_chat": {
        "en": "Clear Chat",
        "tr": "Sohbeti Temizle",
        "de": "Chat Loeschen",
        "no": "Toem Chat",
    },
    "analyzing": {
        "en": "Analyzing...",
        "tr": "Analiz ediliyor...",
        "de": "Analyse laeuft...",
        "no": "Analyserer...",
    },
    "demo_mode_msg": {
        "en": "I'm currently running in demo mode (Groq API not connected). In production, I would:\n1. Detect your intent (SQL query, prediction, recommendation)\n2. Generate a SQL query from your question\n3. Execute it against the hotel database\n4. Generate business insights from the results\n5. Create an auto-visualization",
        "tr": "Su anda demo modunda calisiyorum (Groq API bagli degil). Ueretimde su adimlari izlerdim:\n1. Niyetinizi tespit et (SQL sorgusu, tahmin, oneri)\n2. Sorunuzdan bir SQL sorgusu olustur\n3. Otel veritabaninda calistir\n4. Sonuclardan is icgoerueleri olustur\n5. Otomatik gorsellestirme olustur",
        "de": "Ich laufe derzeit im Demo-Modus (Groq API nicht verbunden). In der Produktion wuerde ich:\n1. Ihre Absicht erkennen (SQL-Abfrage, Vorhersage, Empfehlung)\n2. Eine SQL-Abfrage aus Ihrer Frage generieren\n3. Sie gegen die Hoteldatenbank ausfuehren\n4. Business-Insights aus den Ergebnissen generieren\n5. Eine Auto-Visualisierung erstellen",
        "no": "Jeg kjoerer for tiden i demomodus (Groq API ikke tilkoblet). I produksjon ville jeg:\n1. Oppdage intensjonen din (SQL-spoerring, forutsigelse, anbefaling)\n2. Generere en SQL-spoerring fra spoersmaalet ditt\n3. Kjoere den mot hotelldatabasen\n4. Generere forretningsinnsikt fra resultatene\n5. Lage en autovisualisering",
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
