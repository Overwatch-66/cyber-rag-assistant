# CyberRAG — Assistant d'aide à la conformité cybersécurité

Assistant intelligent permettant d'interroger en langage naturel les principaux référentiels
de cybersécurité (ANSSI, ISO 27001, EBIOS RM, NIS 2, RGPD).

Basé sur une architecture **RAG (Retrieval-Augmented Generation)**, l'outil indexe des documents
réglementaires au format PDF et génère des réponses contextualisées en citant systématiquement
les sources.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Contexte

Les consultants en cybersécurité manipulent quotidiennement des référentiels volumineux
pour vérifier la conformité d'un système d'information, formuler des recommandations ou
préparer des audits. La recherche manuelle dans ces documents est chronophage et sujette
à des oublis.

CyberRAG a été conçu pour répondre à ce besoin : offrir un accès instantané et fiable
aux exigences réglementaires, avec traçabilité des sources.

---

## Architecture

```
Documents PDF
      │
      ▼
  Extraction (PyPDF)
      │
      ▼
  Découpage en chunks (LangChain TextSplitter)
      │
      ▼
  Vectorisation (OpenAI Embeddings)
      │
      ▼
  Stockage (FAISS)
      │
      ▼
  Requête utilisateur ──► Recherche sémantique ──► LLM (GPT-4o-mini) ──► Réponse + Sources
```

---

## Référentiels pris en charge

| Document | Organisme |
|---|---|
| Guide d'hygiène informatique | ANSSI |
| EBIOS Risk Manager | ANSSI |
| ISO/IEC 27001 — Annexe A | ISO |
| Directive NIS 2 (synthèse) | Union Européenne |
| Guide pratique RGPD | CNIL |

D'autres documents peuvent être ajoutés en les déposant dans le répertoire `documents/`.

---

## Prérequis

- Python 3.10 ou supérieur
- Une clé API OpenAI ([platform.openai.com](https://platform.openai.com))

---

## Installation

```bash
git clone https://github.com/overwatch-66/cyber-rag-assistant.git
cd cyber-rag-assistant
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=sk-votre-cle-ici
```

---

## Utilisation

### 1. Indexation des documents

Placer les fichiers PDF dans le répertoire `documents/`, puis lancer l'ingestion :

```bash
python ingest.py
```

### 2. Lancement de l'application

```bash
streamlit run app.py
```

L'interface est accessible à l'adresse `http://localhost:8501`.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Langage | Python |
| Orchestration LLM | LangChain |
| Base vectorielle | FAISS |
| Embeddings & LLM | OpenAI API |
| Interface web | Streamlit |
| Extraction PDF | PyPDF |

---

## Structure du projet

```
cyber-rag-assistant/
├── documents/          # Référentiels PDF à indexer
├── vectorstore/        # Index FAISS (généré automatiquement)
├── ingest.py           # Script d'ingestion des documents
├── app.py              # Application Streamlit
├── requirements.txt
├── .env                # Variables d'environnement (non versionné)
├── .gitignore
└── README.md
```

---

## Améliorations envisagées

- [ ] Upload de documents directement depuis l'interface
- [ ] Support de modèles open source (Mistral)
- [ ] Export des réponses au format PDF
- [ ] Ajout d'un mode comparatif entre référentiels

---

## Auteure

**Placida ALLOKPENOUDJI** — Consultante junior en architecture et sécurité des SI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Placida_ALLOKPENOUDJI-0A66C2?logo=linkedin)](https://www.linkedin.com/in/placida-allokpenoudji)

---

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.