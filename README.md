# Sistema de Cadastro e Análise de Risco Hospitalar

Este projeto fornece uma aplicação de linha de comando para registrar pacientes
na chegada ao hospital e realizar uma triagem automática baseada em sinais
vitais e sintomas.

## Funcionalidades

- Cadastro de novos pacientes com idade, sinais vitais e sintomas.
- Avaliação automática de risco (baixo, moderado e alto) com recomendações.
- Listagem dos pacientes já cadastrados.
- Busca de pacientes pelo nome.
- Persistência simples dos dados em arquivo JSON (`dados_pacientes.json`).

## Requisitos

- Python 3.11 ou superior.

## Como executar

```bash
python app.py
```

Durante a execução, utilize o menu interativo para cadastrar e consultar
pacientes.

## Estrutura de risco

A pontuação de risco é calculada com base em critérios simples de triagem,
considerando idade, temperatura, pressão arterial, frequência cardíaca e a
presença de sintomas críticos (como falta de ar ou dor no peito). A
pontuação final determina o nível de risco:

- **Alto**: pontuação maior ou igual a 6.
- **Moderado**: pontuação entre 3 e 5.
- **Baixo**: pontuação até 2.

As recomendações exibidas no sistema ajudam a orientar a equipe de triagem
sobre a prioridade de atendimento.
