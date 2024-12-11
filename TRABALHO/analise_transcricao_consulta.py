# analise_relato.py

from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
from guardrails import Guard
import json

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env.")

# Inicializar o cliente da OpenAI
client = OpenAI(api_key=api_key)

# Classe Pydantic para validação do output
class AnaliseTEA(BaseModel):
    palavras_chave_relacionadas: List[str] = Field(
        description="Lista de palavras-chave extraídas do relato que podem indicar sinais relacionados ao TEA"
    )
    criterios_relacionados: List[str] = Field(
        description="Lista de critérios do DSM-5 que podem estar relacionados aos pontos encontrados no relato"
    )
    resumo: str = Field(
        description="Breve resumo do comportamento observado no relato"
    )
    sugestoes_para_profissional: str = Field(
        description="Sugestões para o profissional investigar, incluindo pontos de atenção e critérios do DSM-5 a serem avaliados mais a fundo"
    )

# Criação do objeto Guard
guard = Guard.for_pydantic(output_class=AnaliseTEA)

prompt = """
Você é um especialista em TEA, com profundo conhecimento nos critérios diagnósticos do DSM-5 e experiência em analisar relatos de familiares sobre crianças no espectro do autismo.

Agora você receberá a transcrição de uma consulta neuropediátrica.  
**Atenção**: O texto inclui falas do(a) médico(a) e falas da mãe (Maria). 

A tarefa é analisar apenas as observações da mãe sobre o filho, extraindo informações que indiquem sinais relacionados ao TEA. Entretanto, se a mãe der respostas muito curtas (como "sim", "não", "talvez") que não façam sentido sem o contexto da pergunta do médico, você deve levar em consideração o mínimo necessário da fala do médico apenas para esclarecer o sentido da resposta da mãe. Em outras palavras, utilize o contexto da fala do médico apenas quando indispensável para interpretar as respostas curtas da mãe, sem nunca considerar as falas do médico como parte do relato principal e sem atribuir ao relato da mãe palavras que o médico disse.

Seu objetivo é:
1. Identificar palavras-chave ou trechos (provenientes do que a mãe relata, diretamente ou a partir do contexto mínimo necessário da pergunta do médico para entender a resposta) que possam indicar sinais relacionados ao TEA.
2. Relacionar essas palavras-chave aos critérios do DSM-5 potencialmente relevantes.
3. Fornecer um breve resumo do comportamento observado (baseado nas informações da mãe, mesmo que contextualizadas minimamente pela pergunta do médico quando a resposta for curta).
4. Sugerir ao profissional que avaliará a criança pontos de atenção, suspeitas a considerar e critérios do DSM-5 a serem investigados mais a fundo, com base nas informações fornecidas pela mãe.

Importante:
- Não inclua as falas do médico como parte do relato principal da mãe.
- Use a fala do médico somente quando necessário para entender respostas curtas da mãe, e apenas no nível mínimo necessário.
- Todos os sinais, palavras-chave, critérios e o resumo devem refletir o relato da mãe sobre o filho, não o que o médico disse.

Use o formato JSON ao final, conforme especificado anteriormente.

Exemplo (não utilizar no output final, apenas para referência):
{
  "palavras_chave_relacionadas": [...],
  "criterios_relacionados": [...],
  "resumo": "...",
  "sugestoes_para_profissional": "..."
}

Agora analise a seguinte transcrição completa da consulta:


-----------

<transcricao>



Consulta Neuropediátrica – Transcrição da Anamnese

Maria:
Boa tarde, Doutor(a). Sou a Maria, mãe de um menino de 1 ano e 6 meses. Gostaria de compartilhar algumas observações sobre a rotina e os comportamentos do meu filho, pois estou preocupada com certos atrasos.

[MÉDICO]: "Como foi o desenvolvimento inicial do seu filho, incluindo a gravidez e o parto?"

Maria:
A gravidez foi tranquila e o parto ocorreu dentro do esperado, sem complicações significativas. Desde recém-nascido, ele era um bebê muito quieto, não chorava muito, mas também não parecia prestar muita atenção ao ambiente. Comecei a notar alguns atrasos por volta dos 6 meses, principalmente na falta de interesse visual e no pouco engajamento social.

[MÉDICO]: "Seu filho já balbucia palavras como 'mamãe' ou 'papai'? Ele tenta imitar sons ou gestos?"

Maria:
Não, ele ainda não fala nenhuma palavra com significado. Às vezes emite sons como "ba" ou "da", mas de forma aleatória, sem contexto ou intenção de comunicação. Ele também não tenta imitar gestos, como acenar ou bater palmas.

[MÉDICO]: "Ele reage quando é chamado pelo nome? Demonstra interesse ao ouvir sons familiares?"

Maria:
Quase nunca. Ele reage muito raramente ao ser chamado pelo nome, mesmo quando falamos de forma clara e repetida. No entanto, parece prestar atenção a sons específicos, como barulho de embalagens ou música com ritmos repetitivos.

[MÉDICO]: "Como são as interações sociais dele? Ele faz contato visual ou demonstra afeto?"

Maria:
Ele evita contato visual na maior parte do tempo. Há momentos em que me observa de relance, especialmente quando está angustiado ou quer algo específico, mas o olhar é fugaz. Quanto ao afeto, não costuma abraçar ou buscar colo de forma espontânea, o que me preocupa bastante.

[MÉDICO]: "Como ele lida com mudanças na rotina ou ambientes novos?"

Maria:
Ele se desorganiza facilmente quando há mudanças na rotina ou quando estamos em lugares novos. Fica inquieto, chora com frequência e às vezes se joga no chão, principalmente se estiver cansado ou com fome.

[MÉDICO]: "Quais são as preferências alimentares dele? Aceita bem novos alimentos?"

Maria:
Ele é extremamente seletivo. Prefere alimentos secos e crocantes como biscoitos e pães. Qualquer coisa nova, mesmo que seja apresentada de forma gradual, é rejeitada com muito choro e resistência.

[MÉDICO]: "Como é a rotina de sono? Ele dorme durante a noite toda?"

Maria:
Dormir é um grande desafio. Mesmo com uma rotina noturna bem estabelecida, ele resiste para adormecer e, quando finalmente dorme, acorda várias vezes durante a noite. Muitas vezes fica acordado por horas, inquieto e, às vezes, chorando sem motivo aparente.

[MÉDICO]: "Ele demonstra interesse por brinquedos ou atividades específicas?"

Maria:
Sim, mas de uma forma muito particular. Ele não se interessa por brinquedos tradicionais. Prefere objetos que giram ou fazem movimentos repetitivos. Gosta de organizar seus carrinhos em fileiras e passa muito tempo girando as rodas.

[MÉDICO]: "Você já notou comportamentos repetitivos ou movimentos incomuns?"

Maria:
Sim, ele tem comportamentos repetitivos como balançar o corpo para frente e para trás quando está sentado e também mexe constantemente as mãos quando está animado ou frustrado.

[MÉDICO]: "Como ele responde a estímulos sensoriais, como barulhos altos ou toques inesperados?"

Maria:
Ele é muito sensível a barulhos altos e inesperados, o que o deixa bastante irritado. Toques inesperados também o incomodam, e ele tende a se afastar ou a chorar quando isso acontece.

[MÉDICO]: "Quais são suas maiores preocupações no momento?"

Maria:
Minha principal preocupação é o atraso no desenvolvimento da fala, a falta de interação social e a dificuldade em lidar com mudanças na rotina. Além disso, fico muito angustiada com as crises de choro frequentes e com a seletividade alimentar extrema. Quero muito entender como ajudá-lo a se desenvolver melhor e a se sentir mais confortável no dia a dia.

Fim da consulta.



</transcricao>



Lembre-se: A análise deve focar apenas no que a mãe relatou sobre o filho, ignorando completamente o que o médico disse.
${gr.complete_json_suffix_v2}
"""

try:
    # Primeiro, chamar o modelo usando o client (como no exemplo fornecido)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Ajuste conforme o modelo disponível
        messages=[
            {"role": "system", "content": "Você é um especialista em TEA e DSM-5. Sempre explique suas conclusões de forma clara e empática."},
            {"role": "assistant", "content": "Entendido. Estou pronto para analisar o próximo relato levando em conta apenas as falas da mãe."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extrair o conteúdo da resposta
    response_text = completion.choices[0].message.content

    # Validar a resposta usando guard
    res = guard.parse(response_text)

    validated_output = res.validated_output
    print("Saída validada pelo Guardrails:")
    # print(validated_output)

    # Agora, formatação em Markdown
    # Transformar o dicionário em um prompt para o modelo formatar
    format_prompt = f"""
Abaixo está o resultado da análise em formato JSON:

{json.dumps(validated_output, indent=2)}

Por favor, apresente esses dados em um formato Markdown, organizado e fácil de ler.
Liste as palavras-chave, os critérios do DSM-5, o resumo e as sugestões de forma clara.
"""

    formatting_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente que formata informações em Markdown."},
            {"role": "user", "content": format_prompt}
        ]
    )

    formatted_markdown = formatting_completion.choices[0].message.content
    print("\nResposta em Markdown:")
    print(formatted_markdown)

except Exception as e:
    print(f"Ocorreu um erro ao interagir com o modelo: {e}")
