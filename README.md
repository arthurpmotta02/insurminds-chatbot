# 🛡️ ChatBot de Atendimento para Seguros

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Projeto desenvolvido para o Desafio InsurMinds Challenge 2 - i2a2.academy**

Um assistente virtual inteligente para atendimento automatizado em seguros, utilizando RAG (Retrieval-Augmented Generation) com **dados REAIS de fontes verificáveis**.

---

## 👥 Equipe DataShield

- **Arthur Pontes Motta** (Representante) - [LinkedIn](https://www.linkedin.com/in/arthurpmotta/)
- **Daniel Norberto** - [LinkedIn](https://www.linkedin.com/in/daniel-norberto-72ba71264/)
- **Maria Clara Peres** - [LinkedIn](https://www.linkedin.com/in/maria-clara-peres/)

**Contato:** arthurpmotta02@gmail.com

**Repositório:** [https://github.com/arthurpmotta02/insurminds-chatbot](https://github.com/arthurpmotta02/insurminds-chatbot)

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Dados Reais Utilizados](#-dados-reais-utilizados)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias-utilizadas)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Evidências](#-evidências-de-execução)

---

## 🎯 Visão Geral

Este chatbot foi desenvolvido para otimizar a interação com segurados, proporcionando:

- ✅ Respostas rápidas e precisas baseadas em **fontes oficiais**
- ✅ Orientações sobre processos de sinistro
- ✅ Explicações de termos técnicos em linguagem acessível
- ✅ Sistema RAG para contexto relevante
- ✅ Disponibilidade 24/7

### Problema Resolvido

No setor de seguros, 50-70% das dúvidas dos segurados são recorrentes. O chatbot automatiza o atendimento dessas questões, liberando a equipe humana para casos complexos e aumentando a satisfação do cliente com respostas imediatas.

---

## 📊 Dados REAIS Utilizados

### ✅ Conformidade com o Desafio InsurMinds

**"Bases de dados para treinamento: Datasets de FAQs de seguros (Kaggle)"** ✅ ATENDIDO

O projeto utiliza **DADOS REAIS** de **FONTES PÚBLICAS VERIFICÁVEIS**:

### 🎯 Metodologia de Coleta de Dados

#### 1. **Insurance QA Dataset (Kaggle)** ⭐ DATASET PRINCIPAL
- **URL**: https://www.kaggle.com/datasets/ojassrivastava18/insurance-qa
- **Tipo**: Perguntas e Respostas sobre Seguros
- **Paper Científico**: "Applying Deep Learning to Answer Selection" (ASRU 2015)
- **Conteúdo**: Dataset acadêmico com Q&A em inglês, traduzido e adaptado para PT-BR
- **Repositório GitHub**: https://github.com/codekansas/insurance_qa_python
- **Uso no Projeto**: Tradução das perguntas/respostas para contexto brasileiro

#### 2. **SUSEP - Dados Abertos (Governo Federal)**
- **URL**: https://www.gov.br/susep/pt-br/central-de-conteudos/dados-estatisticos/bases-anonimizadas
- **Categorias**: Automóvel, Rural, Compreensivo
- **Formato**: CSV anonimizados (conforme LGPD)
- **Status**: Plano de Dados Abertos 2024-2026
- **Uso**: Referência para termos técnicos e glossário oficial

#### 3. **Portal Dados.gov.br**
- **URL**: https://dados.gov.br/organization/superintendencia-de-seguros-privados-susep
- **Conteúdo**: APIs e datasets de provisões técnicas, sinistros, produtos
- **Uso**: Complementação de informações regulatórias

#### 4. **Legislação e Órgãos Reguladores**
- Código Civil Brasileiro (Arts. 757-802)
- Resoluções CNSP (332/2015, 382/2020, 535/2016)
- Circular SUSEP 269/2004
- CNseg, FenSeg, FenaPrevi, ANS

#### 5. **Fontes Públicas de Seguradoras**
- Condições gerais: Porto Seguro, SulAmérica, Itaú, Mapfre, Allianz, Liberty
- FAQs institucionais públicas
- Guias de consumidor

#### 6. **Defesa do Consumidor**
- Proteste, Consumidor.gov.br, Procon

### 📈 Estatísticas da Base de Conhecimento

- **Total de FAQs**: 30+ perguntas e respostas
- **Categorias**: 6 (Conceitos, Auto, Residencial, Vida, Processos, Dúvidas)
- **Fontes únicas**: 15+ com URLs verificáveis
- **100%** das FAQs possuem: fonte documentada + link + origem dos dados

### 📄 Documentação Completa

Ver arquivo: `data/FONTES_DADOS.txt` (gerado automaticamente com todas as referências)

---

## 🚀 Funcionalidades

### 1. **Sistema RAG (Retrieval-Augmented Generation)**
- Busca semântica com TF-IDF
- Recuperação de FAQs e documentação relevantes
- Respostas baseadas em informação verificada

### 2. **Interface Conversacional**
- Chat em tempo real via Streamlit
- Design responsivo e amigável
- Histórico de conversas
- Botões de ação rápida com exemplos

### 3. **Base de Conhecimento Verificável**
- 30+ FAQs com fontes oficiais
- Documentação técnica abrangente
- Links para todas as fontes
- Cobertura de:
  - Seguros Auto
  - Seguros Residenciais
  - Seguros de Vida
  - Processos e Regulamentação

### 4. **Sistema de Logging**
- Registro de todas interações
- Analytics de uso
- Exportação em JSON

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal
- **NumPy**: Cálculos numéricos para embeddings
- **Pandas**: Manipulação de dados

### Frontend
- **Streamlit**: Interface web interativa
- **HTML/CSS**: Customização visual

### NLP & RAG
- **TF-IDF**: Embeddings para busca semântica
- **Cosine Similarity**: Cálculo de relevância

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/arthurpmotta02/insurminds-chatbot.git
cd insurminds-chatbot

# 2. Crie ambiente virtual
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Gere a base de dados REAL
python scripts/download_real_insurance_data.py

# 5. Execute o chatbot
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8052`

---

## 🎮 Como Usar

### Exemplos de Perguntas:

- "O que é seguro?"
- "Como funciona a franquia?"
- "O que fazer em caso de acidente?"
- "Como funciona o sistema de bônus?"
- "Quais coberturas do seguro auto?"
- "Como fazer uma reclamação na SUSEP?"

### Interface:

1. **Digite sua dúvida** no campo inferior
2. **Aguarde a resposta** (< 2 segundos)
3. **Use os botões de ação rápida** para exemplos
4. **Clique em "Nova Conversa"** para recomeçar

---

## 📊 Evidências de Execução

### Screenshots Disponíveis

Todas as evidências estão em: `docs/evidencias/`

1. **01_tela_inicial.png** - Interface do chatbot
2. **02_conversa_funcionando.png** - Exemplo de conversa
3. **03_botoes_acoes.png** - Botões de ação rápida
4. **04_knowledge_base.png** - Base de dados com fontes
5. **05_fontes_dados.png** - Documentação da metodologia

### Resultados dos Testes:

- ✅ **Taxa de sucesso:** 100% (todas interações geraram respostas apropriadas)
- ✅ **Tempo de resposta:** < 2 segundos
- ✅ **Cobertura:** 30+ FAQs com fontes verificáveis
- ✅ **Logs:** Disponíveis em `logs/`

---

## 🔮 Melhorias Futuras

### Curto Prazo:
- [ ] Integração completa com Claude API
- [ ] Embeddings neurais (sentence-transformers)
- [ ] Dashboard de analytics avançado

### Médio Prazo:
- [ ] Multicanal (WhatsApp, Telegram)
- [ ] Integração com CRM
- [ ] Voice assistant

---

## 📝 Estrutura do Projeto

```
insurminds-chatbot/
│
├── data/                          # Base de dados REAL
│   ├── knowledge_base.json        # 30+ FAQs com fontes
│   ├── FONTES_DADOS.txt           # Lista de fontes oficiais
│   └── documentacao_seguros.txt   # Documentação técnica
│
├── src/                           # Código fonte
│   ├── rag_engine.py              # Motor RAG
│   ├── chatbot.py                 # Lógica do chatbot
│   └── __init__.py
│
├── scripts/                       # Scripts auxiliares
│   └── download_real_insurance_data.py  # Gera base de dados
│
├── docs/                          # Documentação
│   └── evidencias/                # Screenshots de execução
│
├── logs/                          # Logs de conversas
│
├── .streamlit/                    # Configuração Streamlit
│   └── config.toml
│
├── app.py                         # Interface Streamlit
├── requirements.txt               # Dependências
├── test_demo.py                   # Testes
├── .gitignore
└── README.md                      # Este arquivo
```

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 📞 Contato

**Equipe DataShield**

- **Arthur Pontes Motta** (Representante)
  - Email: arthurpmotta02@gmail.com
  - LinkedIn: https://www.linkedin.com/in/arthurpmotta/

- **Daniel Norberto**
  - LinkedIn: https://www.linkedin.com/in/daniel-norberto-72ba71264/

- **Maria Clara Peres**
  - LinkedIn: https://www.linkedin.com/in/maria-clara-peres/

**Repositório**: https://github.com/arthurpmotta02/insurminds-chatbot

---

## 🙏 Agradecimentos

- **i2a2.academy** pelo desafio InsurMinds Challenge 2
- **SUSEP** pelos dados públicos
- **Kaggle** pelo Insurance QA Dataset
- **CNseg** pelas informações do setor
- **Comunidade Streamlit** pela documentação

---

## 🏆 Diferenciais do Projeto

✅ **Dados Verificáveis**: Todas as FAQs têm fonte + link + origem documentada  
✅ **Dataset Acadêmico**: Uso do Insurance QA (Kaggle) com paper científico  
✅ **Dados Brasileiros**: SUSEP como fonte oficial de regulamentação  
✅ **Metodologia Transparente**: Processo de coleta completamente documentado  
✅ **Conformidade Legal**: LGPD, Lei de Acesso à Informação  
✅ **Interface Profissional**: Streamlit com design customizado  
✅ **Sistema RAG Funcional**: Busca semântica com TF-IDF  

---

<div align="center">

**Desenvolvido com ❤️ pela Equipe DataShield**

*Desafio InsurMinds Challenge 2 - i2a2.academy*

**Maio 2026**

</div>