import streamlit as st
import sys
import os
from datetime import datetime

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rag_engine import RAGEngine
from chatbot import InsuranceChatbot

# Configuração da página
st.set_page_config(
    page_title="ChatBot de Seguros - InsurMinds",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #1E88E5;
    }
    
    .bot-message {
        background-color: #F1F8E9;
        border-left: 4px solid #43A047;
    }
    
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do chatbot
@st.cache_resource
def initialize_chatbot():
    rag = RAGEngine(
        "data/knowledge_base.json",
        "data/documentacao_seguros.txt"
    )
    return InsuranceChatbot(rag)

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = initialize_chatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Header
st.markdown('<div class="main-header">🛡️ ChatBot de Atendimento - Seguros</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Informações da Sessão")
    st.markdown(f"**Início:** {st.session_state.session_start.strftime('%H:%M:%S')}")
    st.markdown(f"**Mensagens:** {len(st.session_state.messages)}")
    
    st.markdown("---")
    
    st.markdown("### 💡 Dicas Rápidas")
    
    if st.button("📋 Como acionar?", use_container_width=True):
        example_query = "Como acionar o seguro em caso de acidente?"
        st.session_state.messages.append({"role": "user", "content": example_query})
        response = st.session_state.chatbot.chat(example_query)
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()
    
    if st.button("💰 O que é franquia?", use_container_width=True):
        example_query = "O que é franquia no seguro?"
        st.session_state.messages.append({"role": "user", "content": example_query})
        response = st.session_state.chatbot.chat(example_query)
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()
    
    if st.button("🎯 Como funciona bônus?", use_container_width=True):
        example_query = "Como funciona o sistema de bônus?"
        st.session_state.messages.append({"role": "user", "content": example_query})
        response = st.session_state.chatbot.chat(example_query)
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Nova Conversa", use_container_width=True):
        st.session_state.chatbot.reset_conversation()
        st.session_state.messages = []
        st.session_state.session_start = datetime.now()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 👥 Equipe InsurMinds")
    st.markdown("""
    - Arthur Pontes Motta
    - Daniel Norberto
    - Maria Clara Peres
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Conversa")
    
    if not st.session_state.messages:
        st.success("""
👋 **Bem-vindo ao Atendimento Virtual!**

Sou seu assistente especializado em seguros. Posso ajudá-lo com:
- Dúvidas sobre coberturas e tipos de seguro
- Orientações para sinistros
- Processo de contratação e renovação
- Direitos do consumidor

Como posso ajudá-lo hoje?
        """)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 **Você**\n\n{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 **Assistente Virtual**\n\n{message["content"]}</div>', unsafe_allow_html=True)
    
    user_input = st.chat_input("Digite sua dúvida sobre seguros...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Analisando sua dúvida..."):
            response = st.session_state.chatbot.chat(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()

with col2:
    st.markdown("### 📈 Analytics")
    
    summary = st.session_state.chatbot.get_conversation_summary()
    if summary:
        st.info(f"""
**Sessão Atual**

**ID:** {summary.get('session_id', 'N/A')[:8]}...

**Interações:** {summary.get('num_interactions', 0)}

**Início:** {st.session_state.session_start.strftime('%H:%M')}
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔗 Links Úteis")
    st.markdown("""
**Órgãos Reguladores:**
- [SUSEP](https://www.gov.br/susep)
- [ANS](https://www.gov.br/ans)

**Canais de Reclamação:**
- Ouvidoria da SUSEP
- Procon
- Consumidor.gov.br
""")
    
    st.markdown("---")
    
    st.markdown("### ⚡ Ações Rápidas")
    
    if st.button("🏥 Seguro de Vida", use_container_width=True):
        example_query = "O que cobre o seguro de vida?"
        st.session_state.messages.append({"role": "user", "content": example_query})
        response = st.session_state.chatbot.chat(example_query)
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()
    
    if st.button("🏠 Seguro Residencial", use_container_width=True):
        example_query = "O que cobre o seguro residencial?"
        st.session_state.messages.append({"role": "user", "content": example_query})
        response = st.session_state.chatbot.chat(example_query)
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>
        <strong>ChatBot de Seguros</strong> | InsurMinds Challenge 2 - i2a2.academy<br>
        Arthur Pontes Motta • Daniel Norberto • Maria Clara Peres<br>
        <em>Dados baseados em fontes oficiais: SUSEP, CNseg, Insurance QA Dataset (Kaggle)</em>
    </small>
</div>
""", unsafe_allow_html=True)