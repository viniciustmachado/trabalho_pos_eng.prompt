# Análise de Transcrição de Consulta Neuropediátrica

O script `analise_transcricao_consulta.py` é uma ferramenta criada para auxiliar pediatras na identificação de possíveis sinais relacionados ao Transtorno do Espectro Autista (TEA) a partir do relato de um(a) responsável durante uma consulta. Ele utiliza critérios do DSM-5 e análise de linguagem natural, e tem como objetivo extrair informações relevantes da fala da mãe, a partir da transcrição do diálogo na consulta, filtrando o conteúdo da fala do(a) médico(a) para garantir que o foco seja apenas no que a mãe relatou sobre a criança.

## Funcionalidades

- **Extração de Palavras-Chave**: Identifica termos e trechos do relato materno que possam indicar comportamentos relacionados ao TEA.
- **Mapeamento para o DSM-5**: Relaciona as palavras-chave encontradas aos critérios diagnósticos do DSM-5 mais pertinentes.
- **Resumo do Comportamento**: Cria um breve resumo do comportamento observado na criança, conforme descrito pela mãe.
- **Sugestões para o Profissional**: Fornece recomendações sobre pontos de atenção, suspeitas e critérios do DSM-5 que devem ser investigados mais profundamente por um especialista.

## Tecnologias e Bibliotecas Utilizadas

- **Python 3.8+**
- **[openai](https://pypi.org/project/openai/)**: Para interagir com o modelo de linguagem da OpenAI.
- **[pydantic](https://pydantic-docs.helpmanual.io/)**: Para validação dos dados de saída.
- **[guardrails](https://github.com/ShreyaR/guardrails)**: Para garantir que o output do modelo esteja em conformidade com o esquema definido.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Para carregar as variáveis de ambiente, incluindo a chave da API da OpenAI.

## Preparando o Ambiente

1. Instale as dependências listadas em `requirements.txt`:
   `pip install -r requirements.txt`
2. Crie um arquivo `.env` na raiz do projeto contendo sua chave de API da OpenAI:
   `OPENAI_API_KEY=SUA_CHAVE_DE_API_AQUI`

## Como Executar

1. Garanta que todas as dependências estejam instaladas e que o arquivo `.env` esteja configurado corretamente.
2. Execute o script:
   `python analise_transcricao_consulta.py`
3. O script irá:
   - Enviar o prompt para a API da OpenAI.
   - Validar a saída retornada com o schema definido pelo Pydantic e Guardrails.
   - Exibir a saída final validada em JSON no console.
   - Apresentar uma versão formatada em Markdown, facilitando a leitura e análise do resultado.

## Estrutura de Saída

A saída final validada em JSON segue o formato:
    {
    "palavras_chave_relacionadas": [...],
    "criterios_relacionados": [...],
    "resumo": "...",
    "sugestoes_para_profissional": "..."
    }

Sendo:
- palavras_chave_relacionadas: Lista de palavras ou trechos do relato que possam indicar sinais de TEA.
- criterios_relacionados: Lista de critérios do DSM-5 que podem estar associados aos pontos identificados.
- resumo: Um breve sumário do comportamento da criança conforme descrito pela mãe.
- sugestoes_para_profissional: Recomendações para o profissional, incluindo pontos de atenção e critérios a serem avaliados.

