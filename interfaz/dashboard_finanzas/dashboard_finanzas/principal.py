import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
from PySide6.QtWidgets import QPushButton, QWidget, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

# ============================
# Datos ficticios
# ============================
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Generar datos mensuales
lista_registros = []
for anio in [2022, 2023]:
    ingresos = np.random.randint(20000, 50000, size=12)
    egresos = np.random.randint(10000, 30000, size=12)
    saldo = ingresos - egresos
    for i, mes in enumerate(meses):
        lista_registros.append({
            "Anio": anio,
            "Mes": mes,
            "Ingresos": ingresos[i],
            "Egresos": egresos[i],
            "Saldo": saldo[i]
        })

df_mensual = pd.DataFrame(lista_registros)

# ============================
# Dash App
# ============================
dash_app = Dash(__name__)

# Gráfica de ingresos vs egresos

#graficas (df mensual)
df_melt = df_mensual.melt(
    id_vars=["Anio", "Mes", "Saldo"],
    value_vars=["Ingresos", "Egresos"],
    var_name="Tipo",
    value_name="Monto"
)

# colores Plotly
custom_color_discrete_map = {
    "Ingresos": "#00E5FF",  # verde agua brillante
    "Egresos": "#FF9800",   # naranja brillante
    "Saldo":    "#FFEB3B",  # amarillo
}

# A) Línea Ingresos vs Egresos
fig_line_ing_eg = px.line(
    df_melt,
    x="Mes",
    y="Monto",
    color="Tipo",
    color_discrete_map=custom_color_discrete_map,
    markers=True,
    facet_col="Anio",
    title="RF4: Ingresos vs Egresos (Gráfico de Línea)"
)
fig_line_ing_eg.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white",
    legend_title_text=""
)

# B) Línea de Saldo
fig_line_saldo = px.line(
    df_mensual,
    x="Mes",
    y="Saldo",
    color="Anio",
    color_discrete_sequence=["#00E5FF", "#FF9800"],
    markers=True,
    title="RF5: Saldo (Balance) (Gráfico de Línea)"
)
fig_line_saldo.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white"
)

# C) Pastel Ingresos x Rubro
fig_pie_ingresos = px.pie(
    df_rubros_ingresos,
    names="Rubro",
    values="Valor",
    title="RF6: Proporción de Ingresos por Rubro",
    color_discrete_sequence=px.colors.sequential.Blues_r  # color secuencial
)
fig_pie_ingresos.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    font_color="white"
)

# D) Pastel Egresos x Rubro
fig_pie_egresos = px.pie(
    df_rubros_egresos,
    names="Rubro",
    values="Valor",
    title="RF7: Proporción de Egresos por Rubro",
    color_discrete_sequence=px.colors.sequential.Oranges
)
fig_pie_egresos.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    font_color="white"
)

# E) Barras Agrupadas (Ingr/Egr distintos años)
fig_barras_agrup = px.bar(
    df_melt,
    x="Anio",
    y="Monto",
    color="Tipo",
    color_discrete_map=custom_color_discrete_map,
    barmode="group",
    facet_col="Mes",
    title="RF8: Comparación Ingresos/Egresos en distintos años (Barras Agrupadas)"
)
fig_barras_agrup.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white"
)

# ============================
# 2. Funciones para estadísticas
# ============================
def calcular_estadisticas(grupo):
    ing_prom = grupo["Ingresos"].mean()
    ing_mediana = grupo["Ingresos"].median()
    ing_moda = grupo["Ingresos"].mode()
    ing_moda = ing_moda.iloc[0] if not ing_moda.empty else None

    egr_prom = grupo["Egresos"].mean()
    egr_mediana = grupo["Egresos"].median()
    egr_moda = grupo["Egresos"].mode()
    egr_moda = egr_moda.iloc[0] if not egr_moda.empty else None

    sal_prom = grupo["Saldo"].mean()
    sal_mediana = grupo["Saldo"].median()
    sal_moda = grupo["Saldo"].mode()
    sal_moda = sal_moda.iloc[0] if not sal_moda.empty else None

    return {
        "Ingresos (Promedio)": round(ing_prom, 2),
        "Ingresos (Mediana)": round(ing_mediana, 2),
        "Ingresos (Moda)": round(ing_moda, 2) if ing_moda else None,
        "Egresos (Promedio)": round(egr_prom, 2),
        "Egresos (Mediana)": round(egr_mediana, 2),
        "Egresos (Moda)": round(egr_moda, 2) if egr_moda else None,
        "Saldo (Promedio)": round(sal_prom, 2),
        "Saldo (Mediana)": round(sal_mediana, 2),
        "Saldo (Moda)": round(sal_moda, 2) if sal_moda else None,
    }

def agrupar_por_intervalo(df, intervalo):
    if intervalo == "diario":
        grupos = df.groupby(df["Fecha"].dt.date)
    elif intervalo == "semanal":
        df_temp = df.copy()
        df_temp["Year"] = df_temp["Fecha"].dt.year
        df_temp["Semana"] = df_temp["Fecha"].dt.isocalendar().week
        grupos = df_temp.groupby(["Year", "Semana"])
    elif intervalo == "mensual":
        df_temp = df.copy()
        df_temp["Year"] = df_temp["Fecha"].dt.year
        df_temp["Mes"] = df_temp["Fecha"].dt.month
        grupos = df_temp.groupby(["Year", "Mes"])
    elif intervalo == "anual":
        grupos = df.groupby(df["Fecha"].dt.year)
    else:
        return pd.DataFrame()

    resultados = []
    for grupo_key, subdf in grupos:
        stats = calcular_estadisticas(subdf)
        if intervalo == "diario":
            label = str(grupo_key)
        elif intervalo == "semanal":
            label = f"{grupo_key[0]}-Semana {grupo_key[1]}"
        elif intervalo == "mensual":
            label = f"{grupo_key[0]}-Mes {grupo_key[1]}"
        elif intervalo == "anual":
            label = f"Año {grupo_key}"

        row_dict = {"Intervalo": label}
        row_dict.update(stats)
        resultados.append(row_dict)

    return pd.DataFrame(resultados)


# 3. Gráficas mensuales

df_melt = df_mensual.melt(
    id_vars=["Anio", "Mes", "Saldo"],
    value_vars=["Ingresos", "Egresos"],
    var_name="Tipo",
    value_name="Monto"
)

fig_line_ing_eg = px.line(
    df_melt,
    x="Mes",
    y="Monto",
    color="Tipo",
    facet_col="Anio",
    markers=True,
    title="Ingresos vs Egresos (Mensual)"
)
fig_line_ing_eg.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white"
)

fig_line_saldo = px.line(
    df_mensual,
    x="Mes",
    y="Saldo",
    color="Anio",
    markers=True,
    title="Saldo Mensual (Por Año)"
)
fig_line_saldo.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white"
)


# 4) FUNCIONES PARA LA TABLA (con df_diario)

def calcular_estadisticas(grupo):
    ing_prom = grupo["Ingresos"].mean()
    ing_mediana = grupo["Ingresos"].median()
    ing_moda = grupo["Ingresos"].mode()
    if not ing_moda.empty:
        ing_moda = ing_moda.iloc[0]

    egr_prom = grupo["Egresos"].mean()
    egr_mediana = grupo["Egresos"].median()
    egr_moda = grupo["Egresos"].mode()
    if not egr_moda.empty:
        egr_moda = egr_moda.iloc[0]

    sal_prom = grupo["Saldo"].mean()
    sal_mediana = grupo["Saldo"].median()
    sal_moda = grupo["Saldo"].mode()
    if not sal_moda.empty:
        sal_moda = sal_moda.iloc[0]

    return {
        "Ingresos (Promedio)": round(ing_prom, 2),
        "Ingresos (Mediana)": round(ing_mediana, 2),
        "Ingresos (Moda)": round(ing_moda, 2),
        "Egresos (Promedio)": round(egr_prom, 2),
        "Egresos (Mediana)": round(egr_mediana, 2),
        "Egresos (Moda)": round(egr_moda, 2),
        "Saldo (Promedio)": round(sal_prom, 2),
        "Saldo (Mediana)": round(sal_mediana, 2),
        "Saldo (Moda)": round(sal_moda, 2),
    }

def agrupar_por_intervalo(df, intervalo):
    if intervalo == "diario":
        grupos = df.groupby(df["Fecha"].dt.date)
    elif intervalo == "semanal":
        df_temp = df.copy()
        df_temp["Year"] = df_temp["Fecha"].dt.year
        df_temp["Semana"] = df_temp["Fecha"].dt.isocalendar().week
        grupos = df_temp.groupby(["Year", "Semana"])
    elif intervalo == "mensual":
        df_temp = df.copy()
        df_temp["Year"] = df_temp["Fecha"].dt.year
        df_temp["Mes"] = df_temp["Fecha"].dt.month
        grupos = df_temp.groupby(["Year", "Mes"])
    elif intervalo == "anual":
        grupos = df.groupby(df["Fecha"].dt.year)
    else:
        return pd.DataFrame()  # nada

    resultados = []
    for grupo_key, subdf in grupos:
        stats = calcular_estadisticas(subdf)
        if intervalo == "diario":
            label = str(grupo_key)
        elif intervalo == "semanal":
            label = f"{grupo_key[0]}-Semana {grupo_key[1]}"
        elif intervalo == "mensual":
            label = f"{grupo_key[0]}-Mes {grupo_key[1]}"
        elif intervalo == "anual":
            label = f"Año {grupo_key}"

        row_dict = {"Intervalo": label}
        row_dict.update(stats)
        resultados.append(row_dict)

    return pd.DataFrame(resultados)


# 5) GRÁFICA ADICIONAL (diario) Y CONSTRUIR LA APP

fig_diario_ingresos = px.line(
    df_diario, x="Fecha", y="Ingresos",
    title="Ingresos diarios (2023)",
    color_discrete_sequence=["#00E5FF"]
)
fig_diario_ingresos.update_layout(
    template="plotly",
    paper_bgcolor="#1C2C40",
    plot_bgcolor="#1C2C40",
    font_color="white"
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard prueba"

app.layout = html.Div(
    className="main-background",  # ver style.css
    children=[
        html.H1("Graficas Dash", className="titulo-principal"),
        
        # SECCIÓN 1: graficas mensuales
        dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_line_ing_eg, className="card-graph"), md=6),
                dbc.Col(dcc.Graph(figure=fig_line_saldo,  className="card-graph"), md=6),
            ], className="row-section"),

            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_pie_ingresos, className="card-graph"), md=6),
                dbc.Col(dcc.Graph(figure=fig_pie_egresos,  className="card-graph"), md=6),
            ], className="row-section"),

            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_barras_agrup, className="card-graph"), md=12),
            ], className="row-section"),
        ], fluid=True),

        html.Hr(),

        # SECCIÓN 2: datos diarios + tabla dstadisticas
        html.H2("Estadísticas Diarias", className="subtitle"),
        html.P("Selecciona un intervalo para agrupar los datos (diario, semanal, mensual, anual):", className="explanatory-text"),
        
        dcc.Dropdown(
            id="intervalo-dropdown",
            options=[
                {"label": "Diario",   "value": "diario"},
                {"label": "Semanal",  "value": "semanal"},
                {"label": "Mensual",  "value": "mensual"},
                {"label": "Anual",    "value": "anual"}
            ],
            value="mensual",
            className="custom-dropdown"
        ),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_diario_ingresos, className="card-graph"), md=12),
        ], className="row-section"),
        html.Div(
            className="data-table-custom",
            children=[
                dash_table.DataTable(
                    id="tabla-estadisticas",
                    columns=[
                        {"name": "Intervalo", "id": "Intervalo"},
                        {"name": "Ingresos (Promedio)", "id": "Ingresos (Promedio)"},
                        {"name": "Ingresos (Mediana)", "id": "Ingresos (Mediana)"},
                        {"name": "Ingresos (Moda)", "id": "Ingresos (Moda)"},
                        {"name": "Egresos (Promedio)", "id": "Egresos (Promedio)"},
                        {"name": "Egresos (Mediana)", "id": "Egresos (Mediana)"},
                        {"name": "Egresos (Moda)", "id": "Egresos (Moda)"},
                        {"name": "Saldo (Promedio)", "id": "Saldo (Promedio)"},
                        {"name": "Saldo (Mediana)", "id": "Saldo (Mediana)"},
                        {"name": "Saldo (Moda)", "id": "Saldo (Moda)"},
                    ],
                    data=[],
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "#283a4d",
                        "fontWeight": "bold",
                        "color": "white",
                    },
                    style_cell={
                        "backgroundColor": "#1C2C40",
                        "color": "white",
                        "border": "1px solid #555",
                    },
                )
            ],
        ),
    ]
)


# ============================
# Ventana principal de PySide6
# ============================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cypher")
        self.resize(1200, 800)

        # Layout principal
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Menú lateral
        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("background-color: #102542;")
        self.menu_frame.setFixedWidth(200)

        menu_layout = QVBoxLayout()
        self.menu_frame.setLayout(menu_layout)

        self.inicio_button = QPushButton("Inicio")
        self.inicio_button.setStyleSheet("color: white;")
        menu_layout.addWidget(self.inicio_button)

        self.ingresar_datos_button = QPushButton("Ingresar datos")
        self.ingresar_datos_button.setStyleSheet("color: white;")
        menu_layout.addWidget(self.ingresar_datos_button)

        # Sección de contenido
        self.content_frame = QFrame()
        content_layout = QVBoxLayout()
        self.content_frame.setLayout(content_layout)

        # Visor Dash (gráficas)
        self.web_view = QWebEngineView()
        content_layout.addWidget(self.web_view)

        # Agregar menús y contenido al layout principal
        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.content_frame)

        # Iniciar Dash
        self.start_dash_server()

    def start_dash_server(self):
        from threading import Thread

        def run_dash():
            dash_app.run_server(debug=True, use_reloader=False, port=8050)

        self.dash_thread = Thread(target=run_dash, daemon=True)
        self.dash_thread.start()

        # Conectar Dash al visor web
        self.web_view.setUrl(QUrl("http://127.0.0.1:8050"))


# ============================
# Ejecutar la aplicación
# ============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())