import pandas as pd
from datetime import datetime
import plotly.express as px
import dash
from dash import Input, Output, dcc  # Añadido
from dash.exceptions import PreventUpdate  # Añadido

class DataProcessor:
    @staticmethod
    def process_monthly_data(data):
        """Procesa datos mensuales de la base de datos."""
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data, columns=['YearMonth', 'Ingresos', 'Egresos', 'Saldo'])
        df['Anio'] = df['YearMonth'].str[:4]
        df['Mes'] = df['YearMonth'].str[5:].apply(lambda x: {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo',
            '04': 'Abril', '05': 'Mayo', '06': 'Junio',
            '07': 'Julio', '08': 'Agosto', '09': 'Septiembre',
            '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        }[x])
        return df

    @staticmethod
    def process_category_data(data):
        """Procesa datos de categorías de la base de datos."""
        if not data:
            return pd.DataFrame(), pd.DataFrame()
            
        df_ingresos = pd.DataFrame([
            {'Rubro': row[0] or 'Sin Categoría', 'Valor': row[1]}
            for row in data if row[1] > 0
        ])
        
        df_egresos = pd.DataFrame([
            {'Rubro': row[0] or 'Sin Categoría', 'Valor': row[2]}
            for row in data if row[2] > 0
        ])
        
        return df_ingresos, df_egresos

    @staticmethod
    def process_daily_data(data):
        """Procesa datos diarios de la base de datos."""
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data, columns=['Fecha', 'Ingresos', 'Egresos', 'Saldo'])
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df
        
    @staticmethod
    def calcular_estadisticas(grupo):
        """Calcula estadísticas para un grupo de datos."""
        if grupo.empty:
            return {}

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
            "Ingresos (Moda)": round(ing_moda, 2) if ing_moda is not None else None,
            "Egresos (Promedio)": round(egr_prom, 2),
            "Egresos (Mediana)": round(egr_mediana, 2),
            "Egresos (Moda)": round(egr_moda, 2) if egr_moda is not None else None,
            "Saldo (Promedio)": round(sal_prom, 2),
            "Saldo (Mediana)": round(sal_mediana, 2),
            "Saldo (Moda)": round(sal_moda, 2) if sal_moda is not None else None,
        }

    @staticmethod
    def agrupar_por_intervalo(df, intervalo):
        """Agrupa los datos por el intervalo especificado."""
        if df.empty:
            return pd.DataFrame()

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
            stats = DataProcessor.calcular_estadisticas(subdf)
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


class DashboardVisualizer:
    """Clase para manejar la visualización de datos en el dashboard."""
    

    @staticmethod
    def get_color_scheme():
        """Retorna el esquema de colores para las gráficas."""
        return {
            "Ingresos": "#00E5FF",
            "Egresos": "#FF9800",
            "Saldo": "#FFEB3B",
        }

    @staticmethod
    def apply_layout_style(fig):
        """Aplica el estilo común a todas las gráficas."""
        fig.update_layout(
            template="plotly",
            paper_bgcolor="#1C2C40",
            plot_bgcolor="#1C2C40",
            font_color="white",
            legend_title_text="",  # Añadido para consistencia
            showlegend=True  # Asegura que la leyenda sea visible
        )
        # Actualizar el estilo de los ejes
        fig.update_xaxes(gridcolor="#283a4d", linecolor="#283a4d")
        fig.update_yaxes(gridcolor="#283a4d", linecolor="#283a4d")
        return fig

    @staticmethod
    def create_all_figures(df_mensual, df_rubros_ingresos, df_rubros_egresos, df_diario):
        if df_mensual.empty and df_diario.empty and df_rubros_ingresos.empty and df_rubros_egresos.empty:
            print("No hay datos disponibles para mostrar en las gráficas")
            return None

        df_melt = df_mensual.melt(
            id_vars=["Anio", "Mes", "Saldo"],
            value_vars=["Ingresos", "Egresos"],
            var_name="Tipo",
            value_name="Monto"
        )
        
        color_map = DashboardVisualizer.get_color_scheme()
        figures = {}
        
        # Gráfico A: Línea (Ingresos vs Egresos)
        fig_line_ing_eg = px.line(
            df_melt,
            x="Mes", y="Monto", color="Tipo",
            color_discrete_map=color_map,
            markers=True,
            facet_col="Anio",
            title="Ingresos vs Egresos (Gráfico de Línea)"
        )
        figures['fig_line_ing_eg'] = DashboardVisualizer.apply_layout_style(fig_line_ing_eg)

        # Gráfico B: Línea de Saldo
        fig_line_saldo = px.line(
            df_mensual,
            x="Mes",
            y="Saldo",
            color="Anio",
            color_discrete_sequence=[color_map["Ingresos"], color_map["Egresos"]],
            markers=True,
            title="Saldo (Balance) (Gráfico de Línea)"
        )
        figures['fig_line_saldo'] = DashboardVisualizer.apply_layout_style(fig_line_saldo)

        # Gráfico C: Pastel de Ingresos x Rubro
        if not df_rubros_ingresos.empty:
            color_sequence_ingresos = px.colors.sequential.Blues_r[:len(df_rubros_ingresos)]
            fig_pie_ingresos = px.pie(
                df_rubros_ingresos,
                names="Rubro",
                values="Valor",
                title="Proporción de Ingresos por Rubro",
                color_discrete_sequence=color_sequence_ingresos
            )
            figures['fig_pie_ingresos'] = DashboardVisualizer.apply_layout_style(fig_pie_ingresos)

        # Gráfico D: Pastel de Egresos x Rubro
        if not df_rubros_egresos.empty:
            color_sequence_egresos = px.colors.sequential.Oranges[:len(df_rubros_egresos)]
            fig_pie_egresos = px.pie(
                df_rubros_egresos,
                names="Rubro",
                values="Valor",
                title="Proporción de Egresos por Rubro",
                color_discrete_sequence=color_sequence_egresos
            )
            figures['fig_pie_egresos'] = DashboardVisualizer.apply_layout_style(fig_pie_egresos)

        # Gráfico E: Barras agrupadas
        fig_barras_agrup = px.bar(
            df_melt,
            x="Anio",
            y="Monto",
            color="Tipo",
            color_discrete_map=color_map,
            barmode="group",
            facet_col="Mes",
            title="Comparación Ingresos/Egresos en distintos años"
        )
        figures['fig_barras_agrup'] = DashboardVisualizer.apply_layout_style(fig_barras_agrup)

        # Gráfico F: Línea diaria
        if not df_diario.empty:
            fig_diario_ingresos = px.line(
                df_diario,
                x="Fecha",
                y="Ingresos",
                title="Ingresos diarios",
                color_discrete_sequence=[color_map["Ingresos"]]
            )
            figures['fig_diario_ingresos'] = DashboardVisualizer.apply_layout_style(fig_diario_ingresos)

        return figures


def update_dash_figures(app_dash, database):
    """Actualiza todas las gráficas de Dash con datos de la base de datos."""
    try:
        # Obtener datos
        monthly_data = database.get_monthly_data()
        category_data = database.get_category_data()
        daily_data = database.get_daily_data()
        
        # Procesar datos
        df_mensual = DataProcessor.process_monthly_data(monthly_data)
        df_rubros_ingresos, df_rubros_egresos = DataProcessor.process_category_data(category_data)
        df_diario = DataProcessor.process_daily_data(daily_data)
        
        # Crear figuras
        figures = DashboardVisualizer.create_all_figures(
            df_mensual, df_rubros_ingresos, df_rubros_egresos, df_diario
        )
        
        if figures:
            # Actualizar cada gráfica en el dashboard
            for graph_id, fig in figures.items():
                if hasattr(app_dash, graph_id):
                    setattr(app_dash, graph_id, fig)
                print(f"Actualizada gráfica: {graph_id}")
                
    except Exception as e:
        print(f"Error al actualizar las gráficas: {e}")

def setup_dash_callbacks(app_dash, database):
    """Configura los callbacks de Dash."""
    # Callback para las gráficas
    @app_dash.callback(
        [
            Output('fig_line_ing_eg', 'figure'),
            Output('fig_line_saldo', 'figure'),
            Output('fig_pie_ingresos', 'figure'),
            Output('fig_pie_egresos', 'figure'),
            Output('fig_barras_agrup', 'figure'),
            Output('fig_diario_ingresos', 'figure')
        ],
        [Input('intervalo-dropdown', 'value')]
    )
    def update_graphs(value):
        try:
            # Obtener y procesar datos
            monthly_data = database.get_monthly_data()
            category_data = database.get_category_data()
            daily_data = database.get_daily_data()
            
            df_mensual = DataProcessor.process_monthly_data(monthly_data)
            df_rubros_ingresos, df_rubros_egresos = DataProcessor.process_category_data(category_data)
            df_diario = DataProcessor.process_daily_data(daily_data)
            
            # Crear figuras
            figures = DashboardVisualizer.create_all_figures(
                df_mensual, df_rubros_ingresos, df_rubros_egresos, df_diario
            )
            
            if not figures:
                raise PreventUpdate
                
            return [
                figures['fig_line_ing_eg'],
                figures['fig_line_saldo'],
                figures['fig_pie_ingresos'],
                figures['fig_pie_egresos'],
                figures['fig_barras_agrup'],
                figures['fig_diario_ingresos']
            ]
        except Exception as e:
            print(f"Error en update_graphs: {e}")
            raise PreventUpdate

    # Callback para la tabla de estadísticas
    @app_dash.callback(
        Output("tabla-estadisticas", "data"),
        [Input("intervalo-dropdown", "value")]
    )
    def actualizar_tabla(intervalo):
        try:
            daily_data = database.get_daily_data()
            if not daily_data:
                print("No hay datos diarios disponibles")
                return []
                
            df_diario = DataProcessor.process_daily_data(daily_data)
            if df_diario.empty:
                print("DataFrame diario está vacío")
                return []

            df_result = DataProcessor.agrupar_por_intervalo(df_diario, intervalo)
            return df_result.to_dict("records")
        except Exception as e:
            print(f"Error al actualizar tabla: {e}")
            return []