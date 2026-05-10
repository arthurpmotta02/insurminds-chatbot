import json
import os
import re
from datetime import datetime
from typing import List, Dict, Tuple
import numpy as np

class RAGEngine:
    """
    Motor de Retrieval-Augmented Generation para o chatbot de seguros.
    Usa embeddings simples baseados em TF-IDF para busca semântica.
    """
    
    def __init__(self, knowledge_base_path: str, documents_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.documents_path = documents_path
        self.knowledge_base = {}
        self.documents = []
        self.document_embeddings = []
        self.vocabulary = set()
        self.idf_scores = {}
        
        self._load_data()
        self._build_embeddings()
    
    def _load_data(self):
        """Carrega a base de conhecimento e documentos"""
        # Carrega FAQs
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            self.knowledge_base = json.load(f)
        
        # Carrega documentação técnica
        with open(self.documents_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Divide em seções
            sections = re.split(r'\n##\s+', content)
            for section in sections:
                if section.strip():
                    self.documents.append(section.strip())
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Pré-processa texto para tokenização"""
        # Converte para minúsculas
        text = text.lower()
        # Remove pontuação excessiva, mantém hífen e apóstrofo
        text = re.sub(r'[^\w\s\-áéíóúâêôãõçü]', ' ', text)
        # Tokeniza
        tokens = text.split()
        # Remove stopwords básicas
        stopwords = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'dos', 'das',
            'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem', 'sob',
            'e', 'ou', 'mas', 'que', 'se', 'é', 'são', 'foi', 'ser', 'ter'
        }
        tokens = [t for t in tokens if t not in stopwords and len(t) > 2]
        return tokens
    
    def _calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        """Calcula Term Frequency"""
        tf = {}
        total = len(tokens)
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
        # Normaliza
        for token in tf:
            tf[token] = tf[token] / total if total > 0 else 0
        return tf
    
    def _build_embeddings(self):
        """Constrói embeddings TF-IDF dos documentos"""
        # Coleta vocabulário
        all_docs = []
        
        # Adiciona FAQs
        for category in self.knowledge_base.values():
            for faq in category.values():
                text = f"{faq['pergunta']} {faq['resposta']}"
                tokens = self._preprocess_text(text)
                all_docs.append(tokens)
                self.vocabulary.update(tokens)
        
        # Adiciona documentos técnicos
        for doc in self.documents:
            tokens = self._preprocess_text(doc)
            all_docs.append(tokens)
            self.vocabulary.update(tokens)
        
        # Calcula IDF
        num_docs = len(all_docs)
        doc_count = {}
        for tokens in all_docs:
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_count[token] = doc_count.get(token, 0) + 1
        
        for token in self.vocabulary:
            self.idf_scores[token] = np.log(num_docs / (1 + doc_count.get(token, 0)))
        
        # Cria embeddings TF-IDF
        self.document_embeddings = []
        for tokens in all_docs:
            tf = self._calculate_tf(tokens)
            embedding = {}
            for token in self.vocabulary:
                embedding[token] = tf.get(token, 0) * self.idf_scores[token]
            self.document_embeddings.append(embedding)
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calcula similaridade do cosseno entre dois vetores"""
        # Produto escalar
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in self.vocabulary)
        
        # Normas
        norm1 = np.sqrt(sum(v**2 for v in vec1.values()))
        norm2 = np.sqrt(sum(v**2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def search_faqs(self, query: str, top_k: int = 3) -> List[Dict]:
        """Busca FAQs relevantes"""
        query_tokens = self._preprocess_text(query)
        query_tf = self._calculate_tf(query_tokens)
        query_embedding = {
            token: query_tf.get(token, 0) * self.idf_scores.get(token, 0)
            for token in self.vocabulary
        }
        
        results = []
        idx = 0
        for category in self.knowledge_base.values():
            for faq in category.values():
                if idx < len(self.document_embeddings):
                    similarity = self._cosine_similarity(
                        query_embedding,
                        self.document_embeddings[idx]
                    )
                    results.append({
                        'pergunta': faq['pergunta'],
                        'resposta': faq['resposta'],
                        'categoria': faq['categoria'],
                        'score': similarity
                    })
                    idx += 1
        
        # Ordena por score e retorna top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def search_documents(self, query: str, top_k: int = 2) -> List[Tuple[str, float]]:
        """Busca documentos técnicos relevantes"""
        query_tokens = self._preprocess_text(query)
        query_tf = self._calculate_tf(query_tokens)
        query_embedding = {
            token: query_tf.get(token, 0) * self.idf_scores.get(token, 0)
            for token in self.vocabulary
        }
        
        # Número de FAQs
        num_faqs = sum(len(cat) for cat in self.knowledge_base.values())
        
        results = []
        for i, doc in enumerate(self.documents):
            doc_idx = num_faqs + i
            if doc_idx < len(self.document_embeddings):
                similarity = self._cosine_similarity(
                    query_embedding,
                    self.document_embeddings[doc_idx]
                )
                # Limita tamanho do documento para o contexto
                doc_preview = doc[:1500] + "..." if len(doc) > 1500 else doc
                results.append((doc_preview, similarity))
        
        # Ordena por score e retorna top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def retrieve_context(self, query: str) -> str:
        """Recupera contexto relevante para a query"""
        # Busca FAQs
        faqs = self.search_faqs(query, top_k=3)
        
        # Busca documentos
        docs = self.search_documents(query, top_k=2)
        
        # Monta contexto
        context = "INFORMAÇÕES RELEVANTES DA BASE DE CONHECIMENTO:\n\n"
        
        if faqs and faqs[0]['score'] > 0.1:
            context += "=== PERGUNTAS FREQUENTES RELACIONADAS ===\n\n"
            for faq in faqs:
                if faq['score'] > 0.1:
                    context += f"P: {faq['pergunta']}\n"
                    context += f"R: {faq['resposta']}\n\n"
        
        if docs and docs[0][1] > 0.1:
            context += "\n=== DOCUMENTAÇÃO TÉCNICA RELEVANTE ===\n\n"
            for doc, score in docs:
                if score > 0.1:
                    context += f"{doc}\n\n"
        
        return context if len(context) > 100 else ""


class ConversationLogger:
    """Registra conversas para análise posterior"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.current_session = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def log_interaction(self, user_message: str, bot_response: str, context_used: bool):
        """Registra uma interação"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'context_used': context_used
        }
        self.current_session.append(interaction)
    
    def save_session(self):
        """Salva a sessão atual em arquivo"""
        if not self.current_session:
            return
        
        filename = f"{self.log_dir}/session_{self.session_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'session_id': self.session_id,
                'start_time': self.current_session[0]['timestamp'],
                'end_time': self.current_session[-1]['timestamp'],
                'num_interactions': len(self.current_session),
                'interactions': self.current_session
            }, f, indent=2, ensure_ascii=False)
    
    def get_session_summary(self) -> Dict:
        """Retorna resumo da sessão atual"""
        if not self.current_session:
            return {}
        
        return {
            'session_id': self.session_id,
            'num_interactions': len(self.current_session),
            'start_time': self.current_session[0]['timestamp'],
            'last_interaction': self.current_session[-1]['timestamp']
        }


if __name__ == "__main__":
    # Teste do RAG Engine
    rag = RAGEngine(
        "data/knowledge_base.json",
        "data/documentacao_seguros.txt"
    )
    
    # Testes
    test_queries = [
        "O que é franquia?",
        "Como funciona o seguro auto?",
        "O que fazer em caso de acidente?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        context = rag.retrieve_context(query)
        print(context[:500] + "..." if len(context) > 500 else context)
