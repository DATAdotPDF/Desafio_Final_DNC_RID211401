#!/bin/bash

# Trap para capturar qualquer erro
trap 'echo "Erro na linha $LINENO. Verifique o log: $log_file"' ERR

# Cria pasta de logs se não existir
mkdir -p logs

# Define nome do log com timestamp
timestamp=$(date +"%Y%m%d_%H%M")
log_file="logs/pipeline_${timestamp}.log"

# Verifica se o ambiente virtual existe
if [ ! -f "venv/bin/activate" ]; then
  echo "Ambiente virtual não encontrado em venv/bin/activate"
  echo "Execute: python3 -m venv venv && source venv/bin/activate"
  exit 1
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..." >> "$log_file"
source venv/bin/activate

# Confirma ambiente e diretório
echo "Ambiente virtual: $(which python)" >> "$log_file"
echo "Diretório atual: $(pwd)" >> "$log_file"
echo "Log em: $log_file" >> "$log_file"

# Executa DAG no Airflow manualmente (se estiver rodando)
echo "Disparando DAG do Airflow manualmente..." >> "$log_file"
docker-compose run airflow-webserver airflow dags trigger dnc_pipeline >> "$log_file" 2>&1

# Executa pipeline manualmente
echo "Executando pipeline local manualmente..." >> "$log_file"
python3 03_codigo/etl_pipeline.py >> "$log_file" 2>&1

# Verifica status da execução
if [ $? -eq 0 ]; then
    echo "Pipeline local executado com sucesso."
else
    echo "Erro durante execução do pipeline local. Veja o log em $log_file"
fi

# Comandos úteis
echo ""
echo "Comandos úteis:"
echo "  docker-compose up airflow-init              → inicializa Airflow"
echo "  docker-compose up                           → sobe o Airflow no navegador"
echo "  docker-compose run airflow-webserver bash   → terminal do container"
echo "  deactivate                                  → sair do ambiente virtual"
echo ""
