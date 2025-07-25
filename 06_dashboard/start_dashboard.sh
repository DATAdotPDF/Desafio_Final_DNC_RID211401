#!/bin/bash

# Ativa o ambiente virtual
if [ ! -f "venv/bin/activate" ]; then
  echo "Ambiente virtual não encontrado em venv/bin/activate"
  echo "Execute: python3 -m venv venv && source venv/bin/activate"
  exit 1
fi

source venv/bin/activate

# Roda o Dash localmente
echo "Iniciando dashboard em http://localhost:8050"
python3 06_dashboard/app.py
