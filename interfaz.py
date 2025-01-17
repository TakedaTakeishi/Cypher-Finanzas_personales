import sys
from threading import Thread

import numpy as np
import pandas as pd
import plotly.express as px

from PySide6.QtCore import QUrl, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QPushButton, QLabel, QLineEdit, QMessageBox, QStackedWidget
)
from PySide6.QtWebEngineWidgets import QWebEngineView

# DASH y dependencias
import dash
import dash_bootstrap_components as dbc  # type: ignore
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from bd_enlace import DatabaseBridge

from visualizacion_datos import DataProcessor, DashboardVisualizer, update_dash_figures, setup_dash_callbacks



# ==============================================================================
# 3. Primera App Dash (puerto 8050) - Dashboard con todas las gráficas
# ==============================================================================
app_dash = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Se asigna fondo azul marino a todo el contenedor de la app de gráficas.
app_dash.layout = html.Div(
    style={
        "border-radius": "20px",
        "overflow": "hidden",
        "background-color": "#1C2C40",
        "padding": "20px",
        "width": "100%",
        "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
    },
    children=[
        html.H1(
            "Gráficas",
            style={
                "color": "white",
                "padding": "10px",
                "text-align": "center",
                "margin-bottom": "10px",
                "border-radius": "10px",
            },
        ),
        dbc.Container([
            dbc.Row([
                dbc.Col(dcc.Graph(id='fig_line_ing_eg'), md=6),
                dbc.Col(dcc.Graph(id='fig_line_saldo'), md=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='fig_pie_ingresos'), md=6),
                dbc.Col(dcc.Graph(id='fig_pie_egresos'), md=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='fig_barras_agrup'), md=12),
            ]),
        ], fluid=True),
        html.Hr(),
        html.H2("Estadísticas Diarias", style={"color": "white"}),
        html.P("Selecciona intervalo (diario, semanal, mensual, anual):", style={"color": "white"}),
        dcc.Dropdown(
            id="intervalo-dropdown",
            options=[
                {"label": "Diario", "value": "diario"},
                {"label": "Semanal", "value": "semanal"},
                {"label": "Mensual", "value": "mensual"},
                {"label": "Anual", "value": "anual"}
            ],
            value="mensual",
            style={"width": "300px"}
        ),
        dcc.Graph(id='fig_diario_ingresos'),
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
        ),
    ]
)



# ==============================================================================
# 4. Segunda App Dash (puerto 8051) - Ingreso de Datos / Lista de Operaciones
# ==============================================================================
def create_empty_app(database: DatabaseBridge):
    """
    Crea una aplicación Dash para operaciones.
    
    Args:
        database: Instancia de DatabaseBridge para manejar operaciones de base de datos
    """
    empty_app = Dash(
        __name__,
        external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"],
    )

    empty_app.layout = html.Div(
        style={"border-radius": "40px", "background-color": "#1C2C40", "padding": "20px"},
        children=[
            dcc.Store(id="operaciones-data", data=[]),
            html.H1(
                "Operaciones",
                style={
                    "color": "white",
                    "padding": "10px",
                    "text-align": "center",
                    "margin-bottom": "0px",
                    "border-radius": "10px",
                },
            ),
            html.Div(
                "Seleccione fecha",
                style={
                    "color": "white",
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "5px",
                    "border-radius": "5px",
                },
            ),
            html.Div(
                [
                    dcc.DatePickerSingle(
                        id="date-picker-single",
                        date=pd.Timestamp.now().strftime("%Y-%m-%d"),
                        display_format="DD-MM-YYYY",
                        style={
                            "background-color": "#1C2C40",
                            "color": "white",
                            "border": "1px",
                            "border-radius": "5px",
                            "padding": "5px",
                            "margin": "0px auto",
                            "display": "block",
                            "text-align": "center",
                        },
                    )
                ],
                style={"text-align": "center", "margin": "0px"},
            ),
            html.Div(
                [
                    # Panel Izquierdo: Formulario para ingresar operación
                    html.Div(
                        [
                            html.Div(
                                "NUEVA OPERACIÓN",
                                style={
                                    "margin-bottom": "10px",
                                    "font-size": "20px",
                                    "color": "white",
                                    "text-align": "center",
                                    "fontWeight": "bold",
                                },
                            ),
                            dcc.Dropdown(
                                id="action-type",
                                options=[
                                    {"label": "Manual", "value": "manual"},
                                    {"label": "Plantilla", "value": "plantilla"},
                                ],
                                placeholder="Selecciona la forma de ingresar la operación",
                                style={"margin-top": "10px", "padding": "5px", "border-radius": "5px"},
                                clearable=False,
                                searchable=False,
                            ),
                            dcc.Dropdown(
                                id="transaction-type",
                                options=[
                                    {"label": "Ingreso", "value": "ingreso"},
                                    {"label": "Egreso", "value": "egreso"},
                                ],
                                placeholder="Selecciona el tipo de transacción",
                                style={"margin-top": "10px", "padding": "5px", "border-radius": "5px"},
                                clearable=False,
                                searchable=False,
                            ),
                            dcc.Dropdown(
                                id="operation-type",
                                options=[
                                    {"label": "Simple", "value": "simple"},
                                    {"label": "Recurrente", "value": "recurrente"},
                                ],
                                placeholder="Selecciona el tipo de operación",
                                style={"margin-top": "10px", "padding": "5px", "border-radius": "5px"},
                                clearable=False,
                                searchable=False,
                            ),
                            html.Div(
                                [
                                    html.Div("Concepto", style={"margin-top": "10px", "color": "white"}),
                                    dcc.Input(
                                        id="input-concepto",
                                        type="text",
                                        placeholder="Ingrese el concepto",
                                        style={"margin-top": "5px", "padding": "5px", "border-radius": "5px", "width": "100%"},
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Div("Monto", style={"margin-top": "10px", "color": "white"}),
                                    dcc.Input(
                                        id="input-monto",
                                        type="text",
                                        placeholder="Ingrese el monto",
                                        style={"margin-top": "5px", "padding": "5px", "border-radius": "5px", "width": "100%"},
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Div("Rubro (opcional)", style={"margin-top": "10px", "color": "white"}),
                                    dcc.Input(
                                        id="input-rubro",
                                        type="text",
                                        placeholder="Ingrese el rubro",
                                        style={"margin-top": "5px", "padding": "5px", "border-radius": "5px", "width": "100%"},
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Button(
                                        "Agregar operación",
                                        id="agregar_operacion",
                                        style={
                                            "background-color": "#ff2a00",
                                            "color": "white",
                                            "padding": "10px 20px",
                                            "margin": "10px",
                                            "border": "none",
                                            "border-radius": "5px",
                                            "cursor": "pointer",
                                            "text-align": "center",
                                        },
                                    ),
                                    html.Button(
                                        "Limpiar",
                                        id="limpiar_campos",
                                        style={
                                            "background-color": "#757575",
                                            "color": "white",
                                            "padding": "10px 20px",
                                            "margin": "10px",
                                            "border": "none",
                                            "border-radius": "5px",
                                            "cursor": "pointer",
                                            "text-align": "center",
                                        },
                                    ),
                                ],
                                style={"text-align": "center"},
                            ),
                        ],
                        style={"padding": "10px", "text-align": "center", "margin-right": "5px", "margin-left": "40px", "flex": "1"},
                    ),
                    # Panel Derecho: Lista de Operaciones
                    html.Div(
                        [
                            html.Div(
                                "OPERACIONES REALIZADAS",
                                style={"margin-bottom": "10px", "font-size": "20px", "color": "white", "text-align": "center", "fontWeight": "bold"},
                            ),
                            html.Table(
                                id="operations-list",
                                children=[],
                                style={
                                    "text-align": "left",
                                    "margin": "10px",
                                    "padding": "20px",
                                    "list-style-type": "none",
                                    "color": "white",
                                },
                            ),
                            html.Div(
                                [
                                    html.Button(
                                        "Editar",
                                        id="btn_editar",
                                        style={
                                            "background-color": "#007bff",
                                            "color": "white",
                                            "padding": "10px 20px",
                                            "margin": "5px",
                                            "border": "none",
                                            "border-radius": "5px",
                                            "cursor": "pointer",
                                            "text-align": "center",
                                        },
                                    ),
                                    html.Button(
                                        "Eliminar",
                                        id="btn_eliminar",
                                        style={
                                            "background-color": "#dc3545",
                                            "color": "white",
                                            "padding": "10px 20px",
                                            "margin": "5px",
                                            "border": "none",
                                            "border-radius": "5px",
                                            "cursor": "pointer",
                                            "text-align": "center",
                                        },
                                    ),
                                ],
                                style={"text-align": "center", "margin-bottom": "10px"},
                            ),
                            html.Button(
                                "Subir a base de datos",
                                id="subir_base",
                                style={
                                    "background-color": "#ff2a00",
                                    "color": "white",
                                    "padding": "10px 20px",
                                    "margin": "10px",
                                    "border": "none",
                                    "border-radius": "5px",
                                    "cursor": "pointer",
                                    "text-align": "center",
                                },
                            ),
                        ],
                        style={"padding": "10px", "text-align": "center", "margin-left": "40px", "margin-right": "40px", "flex": "1"},
                    ),
                ],
                style={"display": "flex", "flex-direction": "row", "margin-top": "10px"},
            ),
        ],
    )

    @empty_app.callback(
        Output("operaciones-data", "data"),
        Input("agregar_operacion", "n_clicks"),
        State("input-concepto", "value"),
        State("input-monto", "value"),
        State("input-rubro", "value"),
        State("transaction-type", "value"),
        State("action-type", "value"),
        State("operation-type", "value"),
        State("operaciones-data", "data"),
    )
    def agregar_operacion(n_clicks, concepto, monto, rubro, transaccion, action_t, operation_t, operaciones):
        if not n_clicks:
            raise PreventUpdate
        if operaciones is None:
            operaciones = []
        nueva_op = {
            "concepto": concepto or "",
            "monto": monto or "",
            "rubro": rubro or "",
            "transaccion": transaccion or "",
            "action_type": action_t or "",
            "operation_type": operation_t or ""
        }
        operaciones.append(nueva_op)
        return operaciones

    @empty_app.callback(
        [
            Output("input-concepto", "value"),
            Output("input-monto", "value"),
            Output("input-rubro", "value"),
            Output("transaction-type", "value"),
            Output("action-type", "value"),
            Output("operation-type", "value"),
        ],
        Input("limpiar_campos", "n_clicks"),
        prevent_initial_call=True,
    )
    def limpiar_campos(n_clicks):
        if not n_clicks:
            raise PreventUpdate
        return ["", "", "", None, None, None]


    @empty_app.callback(
        Output("date-picker-single", "date"),
        Input("date-picker-single", "date")
    )
    def update_date(date):
        if date:
            print(f"Fecha seleccionada: {date}")
            database.handle_date_selection(date)
        return date

    @empty_app.callback(
        Output("operaciones-data", "data", allow_duplicate=True),
        Input("subir_base", "n_clicks"),
        [State("operaciones-data", "data"),
        State("date-picker-single", "date")],
        prevent_initial_call=True
    )
    def subir_a_base(n_clicks, operaciones, selected_date):
        if not n_clicks or not operaciones:
            raise PreventUpdate
        
        print("\n=== Subiendo operaciones a la base de datos ===")
        success = database.upload_operations(operaciones, selected_date)
        
        if success:
            print("Operaciones subidas exitosamente")
            # Actualizar las gráficas después de subir operaciones
            update_dash_figures(app_dash, database)
            return []
        else:
            print("Error al subir operaciones")
            return operaciones

    @empty_app.callback(
        dash.dependencies.Output("operations-list", "children"),
        dash.dependencies.Input("operaciones-data", "data"),
    )
    def actualizar_tabla(operaciones):
        table_header = html.Thead(html.Tr([
            html.Th("ID"),
            html.Th("Concepto"),
            html.Th("Tipo"),
            html.Th("Monto"),
            html.Th("Rubro"),
        ], style={"borderBottom": "2px solid black"}))
        if not operaciones:
            return [table_header, html.Tbody([])]
        filas = []
        for i, op in enumerate(operaciones, start=1):
            row = html.Tr(
                [
                    html.Td(str(i)),
                    html.Td(op["concepto"]),
                    html.Td(op["transaccion"]),
                    html.Td(op["monto"]),
                    html.Td(op["rubro"]),
                ],
                id={"type": "op-row", "index": i},
                n_clicks=0,
                style={"cursor": "pointer", "borderBottom": "1px solid #555"}
            )
            filas.append(row)
        table_body = html.Tbody(filas)
        return [table_header, table_body]

    return empty_app

# ==============================================================================
# 5. Pantalla de Login
# ==============================================================================
class LoginWidget(QWidget):
    def __init__(self, on_login_success, database: DatabaseBridge):
        """
        Args:
            on_login_success: Función a llamar si la validación del login es correcta
            database: Instancia de DatabaseBridge para manejar la conexión
        """
        super().__init__()
        self.on_login_success = on_login_success
        self.database = database  # Guardamos la referencia a la base de datos
        self.setup_ui()

    def setup_ui(self):
        # Layout centrado, sin márgenes para ocupar toda la ventana.
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo (reemplaza "logo.png" con tu ruta de imagen)
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo_label.setFixedSize(120, 120)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Título
        welcome_label = QLabel("Bienvenido a Cypher")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black; margin-bottom: 20px;")
        layout.addWidget(welcome_label)
        
        # Campo Usuario
        usuario_container = QVBoxLayout()
        usuario_container.setSpacing(5)
        usuario_label = QLabel("Usuario")
        usuario_label.setStyleSheet("font-size: 14px; color: black;")
        usuario_label.setAlignment(Qt.AlignLeft)
        usuario_container.addWidget(usuario_label)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Ingresa tu usuario")
        self.user_input.setFixedWidth(300)
        self.user_input.setStyleSheet("""
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: white;
            color: black;
        """)
        usuario_container.addWidget(self.user_input)
        layout.addLayout(usuario_container)
        
        layout.addSpacing(15)
        
        # Campo Contraseña
        contrasena_container = QVBoxLayout()
        contrasena_container.setSpacing(5)
        contrasena_label = QLabel("Contraseña")
        contrasena_label.setStyleSheet("font-size: 14px; color: black;")
        contrasena_label.setAlignment(Qt.AlignLeft)
        contrasena_container.addWidget(contrasena_label)
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Ingresa tu contraseña")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedWidth(300)
        self.pass_input.setStyleSheet("""
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: white;
            color: black;
        """)
        contrasena_container.addWidget(self.pass_input)
        layout.addLayout(contrasena_container)
        
        layout.addSpacing(20)
        
        # Botón de Login
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignCenter)
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setFixedWidth(200)
        self.login_button.setStyleSheet("""
            background-color: #ff2a00;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.login_button.clicked.connect(self.handle_login)
        button_container.addWidget(self.login_button)
        layout.addLayout(button_container)
        
        self.setLayout(layout)

    def handle_login(self):
        usuario = self.user_input.text().strip()
        password = self.pass_input.text().strip()
        
        # Usamos la instancia de database para intentar conectar
        if self.database.connect_user(usuario, password):
            self.on_login_success()
        else:
            QMessageBox.warning(self, "Error de autenticación", "Usuario o contraseña incorrectos.")
# ==============================================================================
# 6. Ventana Principal (PySide6) Integrada: Login y Dashboard
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cypher")
        self.resize(1200, 800)
        # Creamos una instancia del puente de base de datos
        self.database = DatabaseBridge()

        self.init_ui()

    def init_ui(self):
        # Usamos un QStackedWidget para alternar entre Login y la aplicación principal.
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Vista Login
        self.login_widget = LoginWidget(
            on_login_success=self.login_success,
            database=self.database  # Cambiamos el nombre para más claridad
        )
        self.stack.addWidget(self.login_widget)
        
        # Vista Principal (se construirá tras login exitoso)
        self.main_app_widget = QWidget()
        self.stack.addWidget(self.main_app_widget)

    def login_success(self):
        self.build_main_app()
        self.stack.setCurrentWidget(self.main_app_widget)

    def build_main_app(self):
        layout = QHBoxLayout()
        self.main_app_widget.setLayout(layout)
        
        # Menú Lateral
        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("background-color: #1C2C40; color: white; border-radius:20px")
        self.menu_frame.setFixedWidth(80)
        menu_layout = QVBoxLayout(self.menu_frame)
        
        # Botón Dashboard (App Dash, puerto 8050)
        self.dashboard_button = QPushButton()
        self.dashboard_button.setIcon(QIcon("inicio.png"))
        self.dashboard_button.setStyleSheet("background-color: transparent; border: none; padding: 10px;")
        self.dashboard_button.setIconSize(QSize(40, 40))
        self.dashboard_button.clicked.connect(self.show_dashboard)
        menu_layout.addWidget(self.dashboard_button)
        
        # Botón Estadísticas/Ingreso de Datos (App Vacía, puerto 8051)
        self.stats_button = QPushButton()
        self.stats_button.setIcon(QIcon("calculadora.png"))
        self.stats_button.setStyleSheet("background-color: transparent; border: none; padding: 10px;")
        self.stats_button.setIconSize(QSize(40, 40))
        self.stats_button.clicked.connect(self.show_empty_dashboard)
        menu_layout.addWidget(self.stats_button)
        
        # Botón Configuración (opcional)
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("base.png"))
        self.settings_button.setIconSize(QSize(45, 50))
        self.settings_button.setStyleSheet("background-color: transparent; border: none; padding: 10px;")
        menu_layout.addWidget(self.settings_button)
        
        menu_layout.addStretch()
        
        # Contenedor principal para Dash (QWebEngineView)
        self.content_frame = QFrame()
        content_layout = QVBoxLayout(self.content_frame)
        self.web_view = QWebEngineView()
        content_layout.addWidget(self.web_view)
        
        layout.addWidget(self.menu_frame)
        layout.addWidget(self.content_frame)
        
        # Inicia la App Dash del Dashboard en puerto 8050
        self.start_dash_server()

    def start_dash_server(self):
        def run_dash():
            # Configurar callbacks
            setup_dash_callbacks(app_dash, self.database)
            
            # Actualizar gráficas iniciales
            update_dash_figures(app_dash, self.database)
            
            # Iniciar servidor
            app_dash.run_server(debug=False, use_reloader=False, port=8050)
        
        self.dash_thread = Thread(target=run_dash, daemon=True)
        self.dash_thread.start()
        self.web_view.setUrl(QUrl("http://127.0.0.1:8050"))

    def show_dashboard(self):
        # Actualizar gráficas antes de mostrar el dashboard
        update_dash_figures(app_dash, self.database)
        self.web_view.setUrl(QUrl("http://127.0.0.1:8050"))

    def show_empty_dashboard(self):
        empty_app = create_empty_app(database=self.database)

        def run_empty():
            empty_app.run_server(debug=False, use_reloader=False, port=8051)

        if not hasattr(self, 'empty_thread'):
            self.empty_thread = Thread(target=run_empty, daemon=True)
            self.empty_thread.start()

        self.web_view.setUrl(QUrl("http://127.0.0.1:8051"))

# ==============================================================================
# 7. Ejecución de la Aplicación PySide6
# ==============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())






