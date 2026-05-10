import os
import json
from typing import List, Dict
from datetime import datetime
from rag_engine import RAGEngine, ConversationLogger


class InsuranceChatbot:
    """
    Chatbot de atendimento para seguros usando Claude API com RAG
    """
    
    def __init__(self, rag_engine: RAGEngine):
        self.rag_engine = rag_engine
        self.conversation_history = []
        self.logger = ConversationLogger()
        
        # System prompt otimizado para seguros
        self.system_prompt = """Você é um assistente virtual especializado em seguros no Brasil, criado para atender segurados de forma eficiente e profissional.

SUAS RESPONSABILIDADES:
1. Responder perguntas sobre seguros de forma clara e precisa
2. Explicar termos técnicos em linguagem simples
3. Orientar sobre procedimentos (sinistros, cotações, renovações)
4. Ajudar na escolha de coberturas adequadas
5. Informar sobre direitos do consumidor
6. Encaminhar casos complexos para atendimento humano

DIRETRIZES DE ATENDIMENTO:
- Seja empático, especialmente em situações de sinistro
- Use linguagem clara e acessível, evite jargão excessivo
- Seja objetivo nas respostas
- Quando não souber algo, admita e ofereça alternativas
- Sempre baseie suas respostas nas informações fornecidas no contexto
- Nunca invente informações sobre coberturas ou valores
- Se a pergunta for muito específica (valores, coberturas particulares), oriente a consultar a apólice ou falar com corretor

CASOS QUE DEVEM SER ENCAMINHADOS:
- Discussão de valores específicos de indenização
- Divergências ou reclamações formais
- Situações médicas ou jurídicas complexas
- Solicitações que exigem acesso a sistemas internos

FORMATO DAS RESPOSTAS:
- Respostas curtas (2-4 parágrafos) para perguntas simples
- Respostas estruturadas (com tópicos) para perguntas complexas
- Sempre que relevante, mencione que o segurado deve consultar sua apólice para detalhes específicos"""

    def _build_context_message(self, query: str) -> str:
        """Constrói mensagem com contexto RAG"""
        context = self.rag_engine.retrieve_context(query)
        
        if context:
            return f"""{context}

PERGUNTA DO SEGURADO:
{query}

Baseie sua resposta principalmente nas informações acima. Se as informações não forem suficientes para responder completamente, seja honesto sobre isso e sugira próximos passos."""
        else:
            return query
    
    def chat(self, user_message: str) -> Dict[str, str]:
        """
        Processa mensagem do usuário e retorna resposta
        
        Args:
            user_message: Mensagem do usuário
            
        Returns:
            Dict com 'response' e metadados
        """
        # Recupera contexto via RAG
        context_message = self._build_context_message(user_message)
        context_used = len(context_message) > len(user_message)
        
        # Adiciona à conversa
        self.conversation_history.append({
            "role": "user",
            "content": context_message
        })
        
        # Simula resposta do Claude (para demonstração)
        # Em produção, aqui seria a chamada real à API
        response = self._generate_response(user_message, context_message)
        
        # Adiciona resposta ao histórico
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Loga interação
        self.logger.log_interaction(user_message, response, context_used)
        
        return {
            'response': response,
            'context_used': context_used,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_response(self, original_query: str, context_message: str) -> str:
        """
        Gera resposta usando lógica baseada em regras (fallback)
        Em produção, substituir por chamada à API do Claude
        """
        query_lower = original_query.lower()
        
        # Detecção de intenções básicas
        if any(word in query_lower for word in ['olá', 'oi', 'bom dia', 'boa tarde', 'boa noite']):
            return """Olá! Bem-vindo ao atendimento virtual de seguros. 

Como posso ajudá-lo hoje? Posso esclarecer dúvidas sobre:
- Coberturas e tipos de seguro
- Como acionar em caso de sinistro
- Processo de cotação e contratação
- Renovação de apólices
- Direitos do consumidor

Digite sua dúvida e terei prazer em ajudar!"""
        
        if any(word in query_lower for word in ['sinistro', 'acidente', 'batida', 'roubo', 'furto']):
            return """Em caso de sinistro, siga estes passos:

1️⃣ **Acione imediatamente a seguradora**
   - Ligue para o telefone 24h (consta na apólice)
   - Ou use o aplicativo da seguradora

2️⃣ **Providencie documentação**
   - Boletim de Ocorrência (quando necessário)
   - Fotos dos danos
   - Documentos do veículo/imóvel

3️⃣ **Siga as orientações**
   - Aguarde o guincho/perito
   - Não faça acordos sem autorização
   - Guarde todos os comprovantes

4️⃣ **Acompanhe o processo**
   - Pelo app ou site da seguradora
   - A análise leva até 30 dias

**Importante:** Quanto mais rápido acionar, mais rápido será o atendimento!

Posso esclarecer algum ponto específico sobre o processo?"""
        
        if 'franquia' in query_lower:
            return """**Franquia** é o valor que fica por sua conta em caso de sinistro.

🔹 **Como funciona:**
Se o conserto custa R$ 5.000 e sua franquia é R$ 2.000:
- Você paga: R$ 2.000
- Seguradora paga: R$ 3.000

🔹 **Quando NÃO paga franquia:**
- Perda total por roubo/furto
- Danos a terceiros (RCF-V)
- Assistência 24h

🔹 **Tipos de franquia:**
- **Obrigatória:** valor padrão da seguradora
- **Reduzida:** menor valor, prêmio maior
- **Majorada:** maior valor, prêmio menor

O valor da franquia consta na sua apólice. Tem alguma dúvida específica sobre ela?"""
        
        if 'bônus' in query_lower or 'bonus' in query_lower or 'desconto' in query_lower:
            return """O **Sistema de Bônus** premia segurados sem sinistros com desconto no prêmio!

📊 **Como funciona:**
- Cada ano sem sinistro: você sobe uma classe
- Cada classe = mais desconto
- Desconto pode chegar a 50% ou mais

📈 **Exemplo:**
- Classe 0 (inicial): 0% desconto
- Classe 1 (1 ano sem sinistro): ~5% desconto
- Classe 5 (5 anos sem sinistro): ~30% desconto
- Classe 10: até 50% desconto

⚠️ **Perda de bônus:**
- Sinistro com culpa: pode perder várias classes
- Sinistro sem culpa (terceiro bateu): geralmente mantém
- Assistência 24h: NÃO afeta o bônus

💡 **Dica:** Na renovação, sua classe de bônus atual consta na proposta. Vale comparar seguradoras - algumas aceitam transferir seu bônus!

Quer saber mais sobre algum aspecto?"""
        
        if 'cotação' in query_lower or 'contratar' in query_lower or 'quanto custa' in query_lower:
            return """Para fazer uma **cotação de seguro**:

🔍 **Processo:**
1. Acesse o site/app da seguradora ou fale com corretor
2. Preencha os dados solicitados
3. Escolha as coberturas desejadas
4. Receba a proposta com valor do prêmio
5. Compare com outras seguradoras
6. Contrate a melhor opção

💡 **Dica importante:** Compare pelo menos 3 seguradoras! O preço pode variar muito.

📋 **O que influencia o valor:**
- Perfil do segurado (idade, profissão, CEP)
- Histórico de sinistros
- Coberturas escolhidas
- Franquia (maior franquia = menor prêmio)
- Classe de bônus

🤝 **Corretor de seguros:**
Profissional habilitado que busca as melhores condições para você. Não cobra diretamente - recebe comissão da seguradora.

Quer dicas sobre quais coberturas escolher?"""
        
        # Resposta genérica com base no contexto
        if "INFORMAÇÕES RELEVANTES" in context_message:
            return f"""Baseado nas informações da nossa base de conhecimento:

{context_message.split('PERGUNTA DO SEGURADO:')[0]}

Esta informação ajuda com sua dúvida? Se precisar de mais detalhes ou tiver outras perguntas, estou à disposição!

**Importante:** Para informações específicas da sua apólice (valores, coberturas exatas), consulte seu contrato ou fale com seu corretor."""
        
        # Fallback
        return """Entendo sua dúvida, mas preciso de mais informações para ajudá-lo adequadamente.

Posso esclarecer dúvidas sobre:
- 🚗 **Seguro Auto** (coberturas, franquia, bônus, sinistro)
- 🏠 **Seguro Residencial** (coberturas, responsabilidade civil)
- ❤️ **Seguro de Vida** (coberturas, beneficiários)
- 📋 **Processos** (cotação, contratação, renovação, cancelamento)
- ⚖️ **Direitos** (reclamações, SUSEP, prazos)

Poderia reformular sua pergunta ou escolher um desses tópicos?

**Para casos complexos ou específicos da sua apólice, recomendo contatar diretamente sua seguradora ou corretor.**"""
    
    def reset_conversation(self):
        """Reseta a conversa"""
        self.logger.save_session()
        self.conversation_history = []
        self.logger = ConversationLogger()
    
    def get_conversation_summary(self) -> Dict:
        """Retorna resumo da conversa"""
        return self.logger.get_session_summary()


# Para uso em produção com API real do Claude
class ClaudeAPIIntegration:
    """
    Integração com a API do Claude (Anthropic)
    NOTA: Requer API key configurada
    """
    
    @staticmethod
    def call_claude_api(messages: List[Dict], system_prompt: str) -> str:
        """
        Chama a API do Claude
        
        Esta é uma implementação de exemplo. Em produção:
        1. Instalar: pip install anthropic
        2. Configurar API key
        3. Descomentar o código abaixo
        """
        
        # import anthropic
        # 
        # client = anthropic.Anthropic(
        #     api_key=os.environ.get("ANTHROPIC_API_KEY")
        # )
        # 
        # response = client.messages.create(
        #     model="claude-sonnet-4-20250514",
        #     max_tokens=1000,
        #     system=system_prompt,
        #     messages=messages
        # )
        # 
        # return response.content[0].text
        
        return "API do Claude não configurada. Use o modo fallback."


if __name__ == "__main__":
    # Teste do chatbot
    print("Inicializando RAG Engine...")
    rag = RAGEngine(
        "data/knowledge_base.json",
        "data/documentacao_seguros.txt"
    )
    
    print("Inicializando Chatbot...")
    chatbot = InsuranceChatbot(rag)
    
    # Teste de interações
    test_messages = [
        "Olá!",
        "O que é franquia?",
        "Como faço para acionar o seguro em caso de acidente?",
        "Como funciona o bônus?"
    ]
    
    print("\n" + "="*60)
    print("TESTE DO CHATBOT")
    print("="*60)
    
    for msg in test_messages:
        print(f"\n👤 Usuário: {msg}")
        response = chatbot.chat(msg)
        print(f"\n🤖 Bot: {response['response']}")
        print(f"\n📊 Contexto usado: {response['context_used']}")
        print("\n" + "-"*60)
    
    # Salva sessão
    chatbot.logger.save_session()
    print("\n✅ Sessão salva em logs/")
