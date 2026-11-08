#!/usr/bin/env bash
# Descarga datos históricos reales (football-data.co.uk) para backtest.py
set -euo pipefail
mkdir -p data/historico
for lg in E0 D1 D2 SP1 N1 I1; do
  for s in 2122 2223 2324 2425 2526; do
    curl -sSL -m 60 "https://www.football-data.co.uk/mmz4281/$s/$lg.csv" -o "data/historico/${lg}_$s.csv"
  done
done
curl -sSL -m 60 "https://www.football-data.co.uk/new/ARG.csv" -o data/historico/ARG.csv
echo "Listo: $(ls data/historico | wc -l) archivos"
