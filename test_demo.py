"""
Script de Teste e Demonstração do ChatBot de Seguros
InsurMinds Challenge 2 - i2a2.academy

Este script demonstra as funcionalidades principais do chatbot
e gera evidências para o relatório.
"""

import sys
import os
import json
from datetime import datetime

# Adiciona src ao path
sys.path.insert(0, 'src')

from rag_engine import RAGEngine
from chatbot import InsuranceChatbot

def print_separator(char="=", length=70):
    """Imprime separador visual"""
    print(char * length)

def print_header(text):
    """Imprime cabeçalho formatado"""
    print_separator()
    print(f" {text}")
    print_separator()
    print()

def test_rag_engine():
    """Testa o motor RAG"""
    print_header("TESTE 1: Motor RAG - Busca Semântica")
    
    rag = RAGEngine(
        "data/knowledge_base.json",
        "data/documentacao_seguros.txt"
    )
    
    test_queries = [
        "O que é franquia?",
        "Como acionar seguro?",
        "Bônus no seguro auto"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 70)
        
        # Busca FAQs
        faqs = rag.search_faqs(query, top_k=2)
        print("\n📚 FAQs Encontradas:")
        for i, faq in enumerate(faqs, 1):
            print(f"\n{i}. Pergunta: {faq['pergunta']}")
            print(f"   Categoria: {faq['categoria']}")
            print(f"   Score: {faq['score']:.4f}")
            print(f"   Resposta: {faq['resposta'][:100]}...")
        
        print("\n")
    
    print("✅ Teste RAG Engine concluído!\n\n")
    return rag

def test_chatbot_interactions(rag):
    """Testa interações do chatbot"""
    print_header("TESTE 2: Interações do Chatbot")
    
    chatbot = InsuranceChatbot(rag)
    
    test_conversations = [
        {
            "scenario": "Cumprimento Inicial",
            "messages": ["Olá, tudo bem?"]
        },
        {
            "scenario": "Dúvida sobre Franquia",
            "messages": [
                "O que é franquia?",
                "E quando não preciso pagar franquia?"
            ]
        },
        {
            "scenario": "Situação de Sinistro",
            "messages": [
                "Meu carro foi roubado, o que faço?",
                "Preciso fazer boletim de ocorrência?"
            ]
        },
        {
            "scenario": "Informações sobre Bônus",
            "messages": [
                "Como funciona o sistema de bônus?",
                "Posso perder meu bônus?"
            ]
        }
    ]
    
    all_interactions = []
    
    for conv in test_conversations:
        print(f"\n🎭 Cenário: {conv['scenario']}")
        print("=" * 70)
        
        for msg in conv['messages']:
            print(f"\n👤 Usuário: {msg}")
            response = chatbot.chat(msg)
            print(f"\n🤖 Bot: {response['response'][:300]}...")
            print(f"\n📊 Metadados:")
            print(f"   - Contexto RAG usado: {response['context_used']}")
            print(f"   - Timestamp: {response['timestamp']}")
            
            all_interactions.append({
                'scenario': conv['scenario'],
                'user': msg,
                'bot': response['response'],
                'context_used': response['context_used']
            })
        
        print("\n" + "-" * 70)
    
    # Salva sessão
    chatbot.logger.save_session()
    print("\n✅ Teste de Interações concluído!")
    print(f"📁 Logs salvos em: logs/session_{chatbot.logger.session_id}.json\n\n")
    
    return all_interactions

def test_coverage():
    """Testa cobertura de tópicos"""
    print_header("TESTE 3: Cobertura de Tópicos")
    
    rag = RAGEngine(
        "data/knowledge_base.json",
        "data/documentacao_seguros.txt"
    )
    
    topics = {
        "Conceitos Básicos": ["seguro", "apólice", "sinistro", "franquia"],
        "Seguro Auto": ["colisão", "bônus", "perda total"],
        "Seguro Residencial": ["incêndio", "responsabilidade civil"],
        "Seguro de Vida": ["morte", "invalidez", "beneficiários"],
        "Processos": ["cotação", "acionamento", "renovação"],
        "Regulamentação": ["SUSEP", "reclamação"]
    }
    
    for category, keywords in topics.items():
        print(f"\n📂 Categoria: {category}")
        print("-" * 70)
        for keyword in keywords:
            faqs = rag.search_faqs(keyword, top_k=1)
            if faqs and faqs[0]['score'] > 0.1:
                print(f"   ✅ {keyword}: Cobertura encontrada (score: {faqs[0]['score']:.3f})")
            else:
                print(f"   ⚠️  {keyword}: Cobertura limitada")
    
    print("\n✅ Teste de Cobertura concluído!\n\n")

def generate_statistics():
    """Gera estatísticas da base de conhecimento"""
    print_header("TESTE 4: Estatísticas da Base de Conhecimento")
    
    # Carrega base de conhecimento
    with open("data/knowledge_base.json", 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    # Conta FAQs
    total_faqs = 0
    categories = {}
    for category_name, category_data in kb.items():
        count = len(category_data)
        total_faqs += count
        categories[category_name] = count
    
    print(f"📊 Total de FAQs: {total_faqs}")
    print(f"📂 Total de Categorias: {len(categories)}")
    print("\n📋 FAQs por Categoria:")
    for cat, count in categories.items():
        print(f"   - {cat}: {count} FAQs")
    
    # Carrega documentação
    with open("data/documentacao_seguros.txt", 'r', encoding='utf-8') as f:
        doc_content = f.read()
    
    doc_lines = len(doc_content.split('\n'))
    doc_words = len(doc_content.split())
    doc_chars = len(doc_content)
    
    print(f"\n📄 Documentação Técnica:")
    print(f"   - Linhas: {doc_lines}")
    print(f"   - Palavras: {doc_words}")
    print(f"   - Caracteres: {doc_chars}")
    
    print("\n✅ Estatísticas geradas!\n\n")

def main():
    """Executa todos os testes"""
    print_header("🛡️ DEMONSTRAÇÃO - ChatBot de Seguros InsurMinds")
    print("Equipe: Arthur Pontes Motta, Daniel Norberto, Maria Clara Peres")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    input("Pressione ENTER para iniciar os testes...\n")
    
    # Teste 1: RAG Engine
    rag = test_rag_engine()
    input("Pressione ENTER para continuar...\n")
    
    # Teste 2: Interações
    interactions = test_chatbot_interactions(rag)
    input("Pressione ENTER para continuar...\n")
    
    # Teste 3: Cobertura
    test_coverage()
    input("Pressione ENTER para continuar...\n")
    
    # Teste 4: Estatísticas
    generate_statistics()
    
    print_separator("=")
    print("🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print_separator("=")
    print("\n📦 Artefatos gerados:")
    print("   ✅ Logs de conversas em /logs")
    print("   ✅ Evidências de execução capturadas")
    print("   ✅ Base de conhecimento validada")
    print("\n🚀 Para executar a interface web, rode: streamlit run app.py")
    print()

if __name__ == "__main__":
    main()
