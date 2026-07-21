"""
CyberRAG — Assistant d'aide à la conformité cybersécurité
Application Streamlit basée sur une architecture RAG.
"""

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

load_dotenv()

# ── Configuration ────────────────────────────────

st.set_page_config(
    page_title="CyberRAG",
    page_icon="🛡️",
    layout="wide"
)

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Tu es un assistant spécialisé en cybersécurité et conformité réglementaire.
Tu accompagnes les consultants dans la navigation des référentiels de sécurité
(ANSSI, ISO 27001, EBIOS RM, NIS 2, RGPD).

Consignes :
- Réponds uniquement à partir du contexte fourni.
- Cite systématiquement la source (document et page si disponible).
- Si l'information ne figure pas dans le contexte, indique-le explicitement.
- Structure la réponse avec des titres et des listes pour faciliter la lecture.
- Réponds en français.

Contexte :
{context}

Question : {question}

Réponse :
"""
)

# ── Chargement des ressources ────────────────────

@st.cache_resource
def load_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

@st.cache_resource
def create_chain():
    vectorstore = load_vectorstore()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        ),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT_TEMPLATE},
        return_source_documents=True
    )

# ── Interface ────────────────────────────────────

with st.sidebar:
    st.title("🛡️ CyberRAG")
    st.caption("Assistant d'aide à la conformité cybersécurité")
    st.markdown("---")
    st.markdown("""
    **Référentiels indexés**
    - Guide d'hygiène ANSSI
    - ISO 27001 — Annexe A
    - EBIOS Risk Manager
    - Directive NIS 2
    - Guide RGPD (CNIL)
    """)
    st.markdown("---")
    st.markdown("""
    **Exemples de requêtes**
    - *Quelles mesures ANSSI couvrent le contrôle d'accès ?*
    - *Décrire les étapes d'une analyse EBIOS RM.*
    - *Quels contrôles ISO 27001 traitent la gestion des incidents ?*
    - *Quelles obligations NIS 2 pour les opérateurs essentiels ?*
    """)

st.header("Interroger les référentiels")
st.caption(
    "Posez une question en langage naturel. L'assistant recherche les passages "
    "pertinents dans les documents indexés et formule une réponse sourcée."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            try:
                chain = create_chain()
                result = chain.invoke({"question": prompt})
                answer = result["answer"]
                sources = result.get("source_documents", [])

                st.markdown(answer)

                if sources:
                    with st.expander("Sources consultées"):
                        for i, doc in enumerate(sources):
                            src = doc.metadata.get("source_document", "—")
                            page = doc.metadata.get("page", "—")
                            st.markdown(f"**[{i+1}]** `{src}` — page {page}")
                            st.caption(doc.page_content[:300] + "...")
                            st.markdown("---")

            except Exception as e:
                answer = f"Erreur : {str(e)}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})