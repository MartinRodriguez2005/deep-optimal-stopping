
import streamlit as st

TRANSLATIONS = {
    "en": {},
    "fr": {
        "Deep Optimal Stopping": "Arrêt Optimal par Deep Learning",
        "Numerical methods and deep learning for option pricing":
            "Méthodes numériques et deep learning pour le pricing d'options",
        "A quantitative finance research project exploring numerical methods, stochastic processes and machine learning techniques for the valuation of financial derivatives.":
            "Un projet de recherche en finance quantitative explorant les méthodes numériques, les processus stochastiques et le machine learning pour l'évaluation des produits dérivés.",

        "Project Overview": "Présentation du projet",
        "The objective of this project is to implement, analyze and compare different numerical approaches to financial derivative pricing.":
            "L'objectif de ce projet est d'implémenter, d'analyser et de comparer différentes approches numériques de valorisation des produits dérivés.",
        "Particular attention is given to optimal stopping problems, which arise in the valuation of American and Bermudan options.":
            "Une attention particulière est accordée aux problèmes d'arrêt optimal, rencontrés dans la valorisation des options américaines et bermudéennes.",
        "The project progressively combines:": "Le projet combine progressivement :",
        "Stochastic calculus and probability theory.": "Calcul stochastique et théorie des probabilités.",
        "Monte Carlo simulation methods.": "Méthodes de simulation Monte Carlo.",
        "Numerical optimization and regression.": "Optimisation numérique et régression.",
        "Deep learning with PyTorch.": "Deep learning avec PyTorch.",
        "Quantitative model evaluation.": "Évaluation quantitative des modèles.",

        "Available Modules": "Modules disponibles",
        "01 — GBM Simulation": "01 — Simulation GBM",
        "Stochastic Process Simulation": "Simulation de processus stochastiques",
        "Simulation of Geometric Brownian Motion paths.":
            "Simulation de trajectoires de mouvement brownien géométrique.",
        "Topics:": "Thématiques :",
        "Brownian motion.": "Mouvement brownien.",
        "Geometric Brownian Motion.": "Mouvement brownien géométrique.",
        "Monte Carlo simulation.": "Simulation Monte Carlo.",
        "Statistical moment validation.": "Validation des moments statistiques.",
        "Open GBM Simulation": "Ouvrir la simulation GBM",

        "02 — Analytical Pricing": "02 — Pricing analytique",
        "Closed-form Derivative Valuation": "Valorisation analytique des produits dérivés",
        "Analytical pricing models for financial derivatives.":
            "Modèles de pricing analytique pour les produits dérivés.",
        "Black–Scholes European options.": "Options européennes Black–Scholes.",
        "Forward contracts.": "Contrats Forward.",
        "Price sensitivity analysis.": "Analyse de sensibilité des prix.",
        "Theoretical valuation.": "Valorisation théorique.",
        "Open Analytical Pricing": "Ouvrir le pricing analytique",

        "Research Roadmap": "Feuille de route du projet",
        "Stochastic Processes": "Processus stochastiques",
        "GBM simulation and Monte Carlo methods.":
            "Simulation GBM et méthodes Monte Carlo.",
        "Analytical Pricing": "Pricing analytique",
        "Black–Scholes and Forward contracts.": "Black–Scholes et contrats Forward.",
        "Longstaff–Schwartz": "Longstaff–Schwartz",
        "Regression-based American option pricing.":
            "Pricing d'options américaines par régression.",
        "Deep Optimal Stopping": "Arrêt optimal par Deep Learning",
        "Neural networks for optimal stopping.":
            "Réseaux de neurones pour l'arrêt optimal.",
        "Model Evaluation": "Évaluation des modèles",
        "Convergence, accuracy and computational performance.":
            "Convergence, précision et performances computationnelles.",
        "Completed": "Terminé",
        "Planned": "Prévu",

        "Technical Stack": "Environnement technique",
        "Language": "Langage",
        "Numerical Computing": "Calcul numérique",
        "Machine Learning": "Apprentissage automatique",
        "Interface": "Interface",
        "Research and implementation project — Quantitative Finance.":
            "Projet de recherche et d'implémentation — Finance quantitative.",
    },
}


def init_language():
    if "language" not in st.session_state:
        st.session_state["language"] = "en"

    st.sidebar.selectbox(
        "Language / Langue",
        options=["en", "fr"],
        format_func=lambda lang: "English" if lang == "en" else "Français",
        key="language",
    )


def t(text: str) -> str:
    language = st.session_state.get("language", "en")
    return TRANSLATIONS.get(language, {}).get(text, text)
