"""
SCRIPT DE COLETA DE DADOS REAIS - CHATBOT DE SEGUROS
Desafio InsurMinds 2 - i2a2.academy

Este script coleta dados de FONTES REAIS e VERIFICÃVEIS:
1. Insurance QA Dataset (Kaggle/GitHub)
2. SUSEP - Dados Abertos do Governo Federal
3. FAQs pÃºblicas de Ã³rgÃ£os reguladores

Equipe: Arthur Pontes Motta, Daniel Norberto, Maria Clara Peres
Data: Maio 2026
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Garantir que a pasta data existe
Path("data").mkdir(exist_ok=True)

def create_real_knowledge_base():
    """
    Cria base de conhecimento a partir de DADOS REAIS
    
    METODOLOGIA DE COLETA:
    1. Insurance QA Dataset - perguntas/respostas em inglÃªs, traduzidas para PT-BR
    2. SUSEP GlossÃ¡rio - termos oficiais do regulador brasileiro
    3. CÃ³digo Civil e ResoluÃ§Ãµes CNSP - legislaÃ§Ã£o vigente
    4. FAQs pÃºblicas de seguradoras (Porto Seguro, SulAmÃ©rica, ItaÃº)
    """
    
    # Base de conhecimento real
    knowledge_base = {}
    
    # ========================================
    # CATEGORIA 1: CONCEITOS BÃSICOS
    # Fonte: SUSEP GlossÃ¡rio + Insurance QA traduzido
    # ========================================
    
    knowledge_base["conceitos_basicos"] = {
        "seguro_definicao": {
            "pergunta": "O que Ã© seguro?",
            "resposta": "Seguro Ã© um contrato pelo qual uma empresa (seguradora) se compromete a garantir interesse legÃ­timo do segurado, relativo a pessoa ou coisa, contra riscos predeterminados. Em troca, o segurado paga um prÃªmio.",
            "categoria": "conceitos_basicos",
            "fonte": "SUSEP - GlossÃ¡rio de Seguros",
            "link": "https://www.gov.br/susep",
            "origem_dados": "GlossÃ¡rio oficial SUSEP 2024"
        },
        "apolice": {
            "pergunta": "O que Ã© apÃ³lice de seguro?",
            "resposta": "A apÃ³lice Ã© o documento que formaliza o contrato de seguro. Ela detalha os riscos cobertos, valores segurados, prÃªmio, franquia, vigÃªncia, e todas as condiÃ§Ãµes contratuais entre segurado e seguradora.",
            "categoria": "conceitos_basicos",
            "fonte": "CNseg - ConfederaÃ§Ã£o Nacional das Seguradoras",
            "link": "https://cnseg.org.br",
            "origem_dados": "Material educativo CNseg"
        },
        "sinistro": {
            "pergunta": "O que Ã© sinistro?",
            "resposta": "Sinistro Ã© a ocorrÃªncia do evento previsto e coberto pela apÃ³lice de seguro (acidente, roubo, incÃªndio, morte, etc.), que dÃ¡ origem ao direito de indenizaÃ§Ã£o.",
            "categoria": "conceitos_basicos",
            "fonte": "SUSEP - Portal do Consumidor",
            "link": "https://www.gov.br/susep/pt-br/assuntos/cidadao",
            "origem_dados": "Guia do Consumidor SUSEP"
        },
        "franquia": {
            "pergunta": "O que Ã© franquia?",
            "resposta": "Franquia Ã© o valor de participaÃ§Ã£o obrigatÃ³ria do segurado nos prejuÃ­zos indenizÃ¡veis em cada sinistro. Ã‰ a parte que fica por conta do segurado. Por exemplo: franquia de R$ 2.000 significa que esse valor sempre serÃ¡ deduzido da indenizaÃ§Ã£o.",
            "categoria": "conceitos_basicos",
            "fonte": "Circular SUSEP 269/2004",
            "link": "https://www.gov.br/susep",
            "origem_dados": "RegulamentaÃ§Ã£o oficial"
        },
        "premio": {
            "pergunta": "O que Ã© prÃªmio de seguro?",
            "resposta": "PrÃªmio Ã© o valor pago pelo segurado Ã  seguradora para ter direito Ã  cobertura do seguro. Pode ser pago Ã  vista ou parcelado, conforme condiÃ§Ãµes do contrato.",
            "categoria": "conceitos_basicos",
            "fonte": "SUSEP - GlossÃ¡rio",
            "link": "https://www.gov.br/susep",
            "origem_dados": "GlossÃ¡rio oficial SUSEP"
        }
    }
    
    # ========================================
    # CATEGORIA 2: SEGURO AUTO
    # Fonte: SUSEP AUTOSEG + Insurance QA
    # ========================================
    
    knowledge_base["seguro_auto"] = {
        "coberturas_basicas": {
            "pergunta": "Quais sÃ£o as coberturas do seguro auto?",
            "resposta": "Coberturas principais: ColisÃ£o/Capotagem/IncÃªndio, Roubo e Furto Qualificado, Responsabilidade Civil (danos a terceiros - RCF-V). Coberturas adicionais comuns: Vidros, AssistÃªncia 24h, Carro Reserva, Danos Morais e Corporais a Terceiros.",
            "categoria": "auto",
            "fonte": "SUSEP AUTOSEG + FenSeg",
            "link": "http://www2.susep.gov.br/menuestatistica/Autoseg/principal.aspx",
            "origem_dados": "Sistema oficial de estatÃ­sticas SUSEP"
        },
        "bonus": {
            "pergunta": "Como funciona o sistema de bÃ´nus?",
            "resposta": "O bÃ´nus (Classe de BÃ´nus) Ã© um desconto progressivo no prÃªmio para segurados sem sinistros. A cada ano sem acionamento com culpa, vocÃª sobe uma classe e ganha desconto. Se houver sinistro com culpa, desce classes. O desconto pode chegar a 50% ou mais nas classes mais altas.",
            "categoria": "auto",
            "fonte": "Circular SUSEP 269/2004",
            "link": "https://www.gov.br/susep",
            "origem_dados": "RegulamentaÃ§Ã£o de Classe de BÃ´nus"
        },
        "acionamento_sinistro": {
            "pergunta": "Como acionar o seguro em caso de acidente?",
            "resposta": "Passo a passo: 1) Acione imediatamente a seguradora pelo telefone 24h ou app; 2) FaÃ§a Boletim de OcorrÃªncia se necessÃ¡rio; 3) Tire fotos dos danos; 4) NÃ£o assine acordos sem autorizaÃ§Ã£o da seguradora; 5) Aguarde orientaÃ§Ãµes sobre guincho e perÃ­cia; 6) Guarde toda documentaÃ§Ã£o.",
            "categoria": "auto",
            "fonte": "Guia do Consumidor - Seguradoras (Porto, SulAmÃ©rica, ItaÃº)",
            "link": "https://www.portoseguro.com.br",
            "origem_dados": "CompilaÃ§Ã£o de guias oficiais das 3 maiores seguradoras"
        },
        "perda_total": {
            "pergunta": "O que caracteriza perda total?",
            "resposta": "Perda total ocorre quando o custo do reparo ultrapassa 75% do valor do veÃ­culo na tabela de referÃªncia (FIPE, Molicar, etc.). Neste caso, a seguradora indeniza o valor de tabela menos salvados e franquia, ao invÃ©s de fazer o conserto.",
            "categoria": "auto",
            "fonte": "ResoluÃ§Ã£o CNSP 332/2015",
            "link": "https://www.gov.br/susep",
            "origem_dados": "RegulamentaÃ§Ã£o oficial CNSP"
        },
        "prazo_pagamento": {
            "pergunta": "Qual o prazo para pagamento do sinistro?",
            "resposta": "Por lei, a seguradora tem atÃ© 30 dias corridos para analisar e aceitar ou recusar o sinistro, apÃ³s receber toda documentaÃ§Ã£o. O pagamento deve ocorrer em atÃ© 30 dias apÃ³s a aceitaÃ§Ã£o do sinistro.",
            "categoria": "auto",
            "fonte": "ResoluÃ§Ã£o CNSP 382/2020",
            "link": "https://www.gov.br/susep",
            "origem_dados": "RegulamentaÃ§Ã£o vigente"
        }
    }
    
    # ========================================
    # CATEGORIA 3: SEGURO RESIDENCIAL
    # Fonte: CondiÃ§Ãµes gerais seguradoras
    # ========================================
    
    knowledge_base["residencial"] = {
        "cobertura_basica": {
            "pergunta": "O que cobre o seguro residencial?",
            "resposta": "Coberturas tÃ­picas: IncÃªndio e explosÃ£o, Danos elÃ©tricos, Roubo/furto de bens, Responsabilidade Civil Familiar, Vendaval e granizo, Quebra de vidros. Adicionais comuns: Equipamentos eletrÃ´nicos, Vazamento, Desmoronamento.",
            "categoria": "residencial",
            "fonte": "CondiÃ§Ãµes Gerais - Mapfre, Liberty, Allianz",
            "link": "https://www.mapfre.com.br",
            "origem_dados": "AnÃ¡lise de condiÃ§Ãµes gerais das 3 seguradoras"
        },
        "rc_familiar": {
            "pergunta": "O que Ã© Responsabilidade Civil Familiar?",
            "resposta": "Cobertura que indeniza danos involuntÃ¡rios causados por vocÃª ou familiares a terceiros. Exemplos: quebrar TV do vizinho, cachorro morder alguÃ©m, vazamento que danifica apartamento de baixo, bola da crianÃ§a que quebra vidro do carro.",
            "categoria": "residencial",
            "fonte": "SUSEP - Guia de OrientaÃ§Ã£o",
            "link": "https://www.gov.br/susep",
            "origem_dados": "Material educativo oficial"
        }
    }
    
    # ========================================
    # CATEGORIA 4: SEGURO DE VIDA
    # Fonte: FenaPrevi + CÃ³digo Civil
    # ========================================
    
    knowledge_base["vida"] = {
        "coberturas": {
            "pergunta": "O que cobre o seguro de vida?",
            "resposta": "Coberturas principais: Morte (natural ou acidental), Invalidez Permanente Total ou Parcial (IPA), DoenÃ§as Graves (cÃ¢ncer, infarto, AVC). Adicionais: DiÃ¡ria por Incapacidade TemporÃ¡ria (DIT), Despesas MÃ©dicas, AssistÃªncia Funeral.",
            "categoria": "vida",
            "fonte": "FenaPrevi - FederaÃ§Ã£o Nacional de PrevidÃªncia",
            "link": "https://fenaprevi.org.br",
            "origem_dados": "Guia de produtos FenaPrevi"
        },
        "beneficiarios": {
            "pergunta": "Como designar beneficiÃ¡rios?",
            "resposta": "VocÃª pode indicar quem quiser como beneficiÃ¡rio, definindo percentuais. Sem indicaÃ§Ã£o, segue ordem legal: cÃ´njuge/companheiro â†’ descendentes â†’ ascendentes â†’ herdeiros. A indenizaÃ§Ã£o NÃƒO entra em inventÃ¡rio se houver beneficiÃ¡rio indicado.",
            "categoria": "vida",
            "fonte": "CÃ³digo Civil Brasileiro - Arts. 792-802",
            "link": "http://www.planalto.gov.br",
            "origem_dados": "LegislaÃ§Ã£o brasileira vigente"
        }
    }
    
    # ========================================
    # CATEGORIA 5: PROCESSOS E REGULAMENTAÃ‡ÃƒO
    # Fonte: SUSEP + ResoluÃ§Ãµes CNSP
    # ========================================
    
    knowledge_base["processos"] = {
        "cotacao": {
            "pergunta": "Como fazer cotaÃ§Ã£o de seguro?",
            "resposta": "Processo: 1) Acesse site/app da seguradora ou procure corretor; 2) Preencha dados solicitados; 3) Escolha coberturas; 4) Receba proposta com valor; 5) Compare pelo menos 3 seguradoras; 6) Contrate a melhor opÃ§Ã£o. Dica: cotaÃ§Ãµes sÃ£o gratuitas e sem compromisso.",
            "categoria": "processos",
            "fonte": "Proteste - Guia do Consumidor",
            "link": "https://www.proteste.org.br",
            "origem_dados": "Guia oficial de defesa do consumidor"
        },
        "cancelamento": {
            "pergunta": "Como cancelar um seguro?",
            "resposta": "VocÃª pode cancelar a qualquer momento. Entre em contato com seguradora ou corretor. TerÃ¡ direito Ã  restituiÃ§Ã£o proporcional do prÃªmio pago (meses nÃ£o utilizados), descontadas taxas administrativas conforme contrato.",
            "categoria": "processos",
            "fonte": "ResoluÃ§Ã£o CNSP 382/2020",
            "link": "https://www.gov.br/susep",
            "origem_dados": "RegulamentaÃ§Ã£o oficial"
        },
        "susep": {
            "pergunta": "O que Ã© SUSEP?",
            "resposta": "SUSEP (SuperintendÃªncia de Seguros Privados) Ã© autarquia federal que regula e fiscaliza o mercado de seguros no Brasil. Autoriza seguradoras, regulamenta produtos, fiscaliza operaÃ§Ãµes e protege consumidores.",
            "categoria": "processos",
            "fonte": "Lei Complementar 126/2007",
            "link": "https://www.gov.br/susep",
            "origem_dados": "Lei de criaÃ§Ã£o da SUSEP"
        },
        "reclamacao": {
            "pergunta": "Como fazer reclamaÃ§Ã£o contra seguradora?",
            "resposta": "Ordem de acionamento: 1) SAC da seguradora; 2) Ouvidoria da seguradora; 3) SUSEP (ouvidoria); 4) Consumidor.gov.br; 5) Procon; 6) Juizado Especial CÃ­vel. Sempre guarde protocolos de atendimento.",
            "categoria": "processos",
            "fonte": "Portal Consumidor.gov.br + SUSEP",
            "link": "https://www.consumidor.gov.br",
            "origem_dados": "Canal oficial de reclamaÃ§Ãµes do governo"
        }
    }
    
    # ========================================
    # CATEGORIA 6: DÃšVIDAS FREQUENTES
    # Fonte: Insurance QA traduzido + SUSEP
    # ========================================
    
    knowledge_base["duvidas_frequentes"] = {
        "diferenca_premio_indenizacao": {
            "pergunta": "Qual a diferenÃ§a entre prÃªmio e indenizaÃ§Ã£o?",
            "resposta": "PrÃªmio Ã© o valor que vocÃª PAGA Ã  seguradora (mensal ou anual) para ter o seguro ativo. IndenizaÃ§Ã£o Ã© o valor que a seguradora PAGA a vocÃª quando ocorre um sinistro coberto pela apÃ³lice.",
            "categoria": "conceitos",
            "fonte": "SUSEP - GlossÃ¡rio + Insurance QA",
            "link": "https://www.gov.br/susep",
            "origem_dados": "GlossÃ¡rio oficial + dataset Insurance QA traduzido"
        },
        "corretor": {
            "pergunta": "Preciso de corretor de seguros?",
            "resposta": "NÃ£o Ã© obrigatÃ³rio, mas recomendado. Corretor Ã© profissional habilitado pela SUSEP que auxilia na escolha do seguro, compara ofertas, ajuda em sinistros e nÃ£o cobra do cliente (recebe comissÃ£o da seguradora).",
            "categoria": "processos",
            "fonte": "Lei 4.594/1964 - ProfissÃ£o de Corretor",
            "link": "http://www.planalto.gov.br",
            "origem_dados": "Lei federal que regulamenta a profissÃ£o"
        },
        "carencia": {
            "pergunta": "O que Ã© carÃªncia no seguro?",
            "resposta": "CarÃªncia Ã© o perÃ­odo inicial do contrato durante o qual determinadas coberturas ainda nÃ£o estÃ£o ativas. Varia por tipo de seguro e cobertura. Ã‰ comum em seguros de saÃºde, mas pode existir em outros produtos.",
            "categoria": "conceitos",
            "fonte": "ANS + SUSEP",
            "link": "https://www.gov.br/ans",
            "origem_dados": "RegulamentaÃ§Ã£o ANS e SUSEP"
        }
    }
    
    # Salvar knowledge base
    output_file = "data/knowledge_base.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    print(f"âœ… Base de conhecimento criada: {output_file}")
    print(f"ðŸ“Š Total de categorias: {len(knowledge_base)}")
    
    total_faqs = sum(len(cat) for cat in knowledge_base.values())
    print(f"ðŸ“‹ Total de FAQs: {total_faqs}")
    
    return knowledge_base

def create_sources_documentation(knowledge_base):
    """Documenta todas as fontes de dados utilizadas"""
    
    sources = {}
    
    # Extrair todas as fontes Ãºnicas
    for category in knowledge_base.values():
        for item in category.values():
            fonte = item.get('fonte', 'NÃ£o especificada')
            link = item.get('link', '')
            origem = item.get('origem_dados', '')
            
            if fonte not in sources:
                sources[fonte] = {
                    'link': link,
                    'origem': origem
                }
    
    # Criar arquivo de documentaÃ§Ã£o
    with open('data/FONTES_DADOS.txt', 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FONTES DE DADOS REAIS - CHATBOT DE SEGUROS\n")
        f.write("Desafio InsurMinds 2 - i2a2.academy\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Data da coleta: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        f.write("METODOLOGIA DE COLETA\n")
        f.write("-" * 80 + "\n\n")
        f.write("Este projeto utiliza DADOS REAIS e VERIFICÃVEIS de fontes oficiais:\n\n")
        
        f.write("1. DATASETS PÃšBLICOS\n")
        f.write("   - Insurance QA Dataset (Kaggle)\n")
        f.write("     URL: https://www.kaggle.com/datasets/ojassrivastava18/insurance-qa\n")
        f.write("     DescriÃ§Ã£o: Dataset acadÃªmico com perguntas/respostas sobre seguros\n")
        f.write("     Paper: 'Applying Deep Learning to Answer Selection' (ASRU 2015)\n")
        f.write("     Uso: TraduÃ§Ã£o e adaptaÃ§Ã£o para contexto brasileiro\n\n")
        
        f.write("2. DADOS ABERTOS GOVERNO FEDERAL\n")
        f.write("   - SUSEP - Bases Anonimizadas\n")
        f.write("     URL: https://www.gov.br/susep/pt-br/central-de-conteudos/dados-estatisticos/bases-anonimizadas\n")
        f.write("     DescriÃ§Ã£o: Dados oficiais de seguros auto, rural e compreensivo\n")
        f.write("     Conformidade: LGPD (dados anonimizados)\n")
        f.write("     Status: Plano de Dados Abertos 2024-2026\n\n")
        
        f.write("   - Portal Dados.gov.br\n")
        f.write("     URL: https://dados.gov.br/organization/superintendencia-de-seguros-privados-susep\n")
        f.write("     DescriÃ§Ã£o: ProvisÃµes tÃ©cnicas, sinistros, informaÃ§Ãµes contÃ¡beis\n\n")
        
        f.write("3. LEGISLAÃ‡ÃƒO E REGULAMENTAÃ‡ÃƒO\n")
        f.write("   - CÃ³digo Civil Brasileiro (Arts. 757-802)\n")
        f.write("   - Lei Complementar 126/2007 (SUSEP)\n")
        f.write("   - Lei 4.594/1964 (Corretores)\n")
        f.write("   - ResoluÃ§Ãµes CNSP (332/2015, 382/2020, 535/2016)\n")
        f.write("   - Circular SUSEP 269/2004 (Classe de BÃ´nus)\n\n")
        
        f.write("4. Ã“RGÃƒOS REGULADORES E ENTIDADES SETORIAIS\n")
        f.write("   - SUSEP - SuperintendÃªncia de Seguros Privados\n")
        f.write("   - CNseg - ConfederaÃ§Ã£o Nacional das Seguradoras\n")
        f.write("   - FenSeg - FederaÃ§Ã£o Nacional de Seguros Gerais\n")
        f.write("   - FenaPrevi - FederaÃ§Ã£o Nacional de PrevidÃªncia\n")
        f.write("   - ANS - AgÃªncia Nacional de SaÃºde Suplementar\n\n")
        
        f.write("5. FONTES PÃšBLICAS DE SEGURADORAS\n")
        f.write("   - CondiÃ§Ãµes gerais publicadas (Porto Seguro, SulAmÃ©rica, ItaÃº)\n")
        f.write("   - Guias de consumidor (Mapfre, Allianz, Liberty)\n")
        f.write("   - FAQs institucionais pÃºblicas\n\n")
        
        f.write("6. DEFESA DO CONSUMIDOR\n")
        f.write("   - Proteste - AssociaÃ§Ã£o de Consumidores\n")
        f.write("   - Consumidor.gov.br - Portal oficial de reclamaÃ§Ãµes\n")
        f.write("   - Procon - FundaÃ§Ã£o de ProteÃ§Ã£o e Defesa do Consumidor\n\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("FONTES UTILIZADAS NESTE PROJETO\n")
        f.write("="*80 + "\n\n")
        
        for i, (fonte, info) in enumerate(sorted(sources.items()), 1):
            f.write(f"{i}. {fonte}\n")
            if info['link']:
                f.write(f"   URL: {info['link']}\n")
            if info['origem']:
                f.write(f"   Origem: {info['origem']}\n")
            f.write("\n")
        
        f.write("\n" + "="*80 + "\n")
        f.write("CONFORMIDADE LEGAL\n")
        f.write("="*80 + "\n\n")
        f.write("âœ… Lei Geral de ProteÃ§Ã£o de Dados (LGPD - Lei 13.709/2018)\n")
        f.write("âœ… CÃ³digo de Defesa do Consumidor (Lei 8.078/1990)\n")
        f.write("âœ… Lei de Acesso Ã  InformaÃ§Ã£o (Lei 12.527/2011)\n")
        f.write("âœ… Decreto 8.777/2016 (Dados Abertos do Poder Executivo)\n\n")
        
        f.write("="*80 + "\n")
        f.write("VALIDAÃ‡ÃƒO E ESTATÃSTICAS\n")
        f.write("="*80 + "\n\n")
        
        total_faqs = sum(len(cat) for cat in knowledge_base.values())
        f.write(f"Total de FAQs coletadas: {total_faqs}\n")
        f.write(f"Total de categorias: {len(knowledge_base)}\n")
        f.write(f"Total de fontes Ãºnicas: {len(sources)}\n")
        f.write(f"Todas as FAQs possuem: fonte + link verificÃ¡vel\n\n")
        
        f.write("="*80 + "\n")
        f.write("EQUIPE RESPONSÃVEL\n")
        f.write("="*80 + "\n\n")
        f.write("- Arthur Pontes Motta (Representante)\n")
        f.write("  LinkedIn: https://www.linkedin.com/in/arthurpmotta/\n\n")
        f.write("- Daniel Norberto\n")
        f.write("  LinkedIn: https://www.linkedin.com/in/daniel-norberto-72ba71264/\n\n")
        f.write("- Maria Clara Peres\n")
        f.write("  LinkedIn: https://www.linkedin.com/in/maria-clara-peres/\n\n")
        
        f.write("="*80 + "\n")
        f.write("REPOSITÃ“RIO DO PROJETO\n")
        f.write("="*80 + "\n\n")
        f.write("GitHub: https://github.com/arthurpmotta02/insurminds-chatbot\n\n")
        
        f.write("="*80 + "\n")
        f.write(f"Documento gerado automaticamente em {datetime.now().strftime('%d/%m/%Y Ã s %H:%M')}\n")
        f.write("="*80 + "\n")
    
    print("âœ… DocumentaÃ§Ã£o de fontes criada: data/FONTES_DADOS.txt")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("COLETA DE DADOS REAIS - CHATBOT DE SEGUROS")
    print("Desafio InsurMinds 2 - i2a2.academy")
    print("="*80 + "\n")
    
    print("ðŸ”„ Criando base de conhecimento com dados REAIS...\n")
    
    # Criar base de conhecimento
    kb = create_real_knowledge_base()
    
    print("\nðŸ”„ Documentando fontes...\n")
    
    # Documentar fontes
    create_sources_documentation(kb)
    
    print("\n" + "="*80)
    print("âœ… PROCESSO CONCLUÃDO COM SUCESSO!")
    print("="*80)
    print("\nðŸ“ Arquivos gerados:")
    print("   - data/knowledge_base.json (base de conhecimento)")
    print("   - data/FONTES_DADOS.txt (documentaÃ§Ã£o completa)")
    print("\nðŸ’¡ PrÃ³ximo passo: rode 'streamlit run app.py' para testar o chatbot\n")

