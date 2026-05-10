"""
ChatBot de Atendimento para Seguros
InsurMinds Challenge 2 - i2a2.academy

Desenvolvido por:
- Arthur Pontes Motta
- Daniel Norberto  
- Maria Clara Peres

Maio 2026
"""

__version__ = "1.0.0"
__author__ = "Arthur Pontes Motta, Daniel Norberto, Maria Clara Peres"
__email__ = "insurminds@i2a2.academy"
__status__ = "Production"

# Importações principais
from .rag_engine import RAGEngine, ConversationLogger
from .chatbot import InsuranceChatbot

__all__ = [
    'RAGEngine',
    'ConversationLogger', 
    'InsuranceChatbot'
]
