import os
import boto3
import pandas as pd
import pyarrow.parquet as pq
import s3fs
from dotenv import load_dotenv

import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Carrega variáveis de ambiente
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
GOLD_KEY = "gold/usuarios_agrupados.parquet"

# Lê dados do .parquet no S3
def read_gold_from_s3_parquet():
    s3_path = f"s3://{S3_BUCKET_NAME}/{GOLD_KEY}"
    fs = s3fs.S3FileSystem(
        key=AWS_ACCESS_KEY_ID,
        secret=AWS_SECRET_ACCESS_KEY,
        client_kwargs={"region_name": AWS_REGION}
    )
    return pd.read_parquet(s3_path, filesystem=fs)

df = read_gold_from_s3_parquet()
faixas = df['faixa_etaria'].dropna().unique()
status = df['subscription_status'].dropna().unique()

# Inicia o app Dash
app = dash.Dash(__name__)
app.title = "Dashboard - Camada Gold"

# Layout
app.layout = html.Div([
    html.H1("Dashboard de Usuários Agrupados", style={"textAlign": "center"}),

    html.Div([
        html.Label("Filtrar por Faixa Etária:"),
        dcc.Dropdown(
            options=[{"label": f, "value": f} for f in faixas],
            id="faixa-dropdown",
            multi=True,
            placeholder="Selecione faixas..."
        ),

        html.Label("Filtrar por Status de Assinatura:"),
        dcc.Dropdown(
            options=[{"label": s, "value": s} for s in status],
            id="status-dropdown",
            multi=True,
            placeholder="Selecione status..."
        ),

        html.Label("Aplicar filtros em quais gráficos?"),
        dcc.Checklist(
            id="grafico-checklist",
            options=[
                {"label": "Quantidade de Usuários", "value": "qtd"},
                {"label": "Porcentagem de Ativos", "value": "pct"},
                {"label": "Dias desde Cadastro", "value": "dias"}
            ],
            value=["qtd", "pct", "dias"],
            labelStyle={"display": "block"}
        )
    ], style={"width": "25%", "float": "left", "padding": "20px"}),

    html.Div([
        dcc.Graph(id="grafico-qtd"),
        dcc.Graph(id="grafico-pct"),
        dcc.Graph(id="grafico-dias")
    ], style={"width": "70%", "float": "right"})
])

# Callback
@app.callback(
    [
        Output("grafico-qtd", "figure"),
        Output("grafico-pct", "figure"),
        Output("grafico-dias", "figure")
    ],
    [
        Input("faixa-dropdown", "value"),
        Input("status-dropdown", "value"),
        Input("grafico-checklist", "value")
    ]
)
def atualizar_graficos(faixas_sel, status_sel, graficos_sel):
    df_filtrado = df.copy()
    if faixas_sel:
        df_filtrado = df_filtrado[df_filtrado['faixa_etaria'].isin(faixas_sel)]
    if status_sel:
        df_filtrado = df_filtrado[df_filtrado['subscription_status'].isin(status_sel)]

    fig_qtd = px.bar(df_filtrado, x="faixa_etaria", y="qtd_usuarios", color="subscription_status", barmode="group", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_pct = px.bar(df_filtrado, x="faixa_etaria", y="pct_ativos_na_faixa", text="pct_ativos_na_faixa", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_dias = px.bar(df_filtrado, x="faixa_etaria", y="dias_desde_cadastro_media", color_discrete_sequence=px.colors.qualitative.Pastel)

    return (
        fig_qtd if "qtd" in graficos_sel else dash.no_update,
        fig_pct if "pct" in graficos_sel else dash.no_update,
        fig_dias if "dias" in graficos_sel else dash.no_update
    )

if __name__ == "__main__":
    app.run(debug=True)
