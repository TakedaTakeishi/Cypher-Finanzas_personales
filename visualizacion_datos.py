import pandas as pd
from datetime import datetime
import plotly.express as px
import dash

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
            
        return pd.DataFrame(data, columns=['Fecha', 'Ingresos', 'Egresos', 'Saldo'])

def update_dash_figures(app_dash, database):
    """Actualiza todas las gráficas de Dash con datos de la base de datos."""
    # Obtener datos a través del bridge
    monthly_data = database.get_monthly_data()
    category_data = database.get_category_data()
    daily_data = database.get_daily_data()
    
    # Procesar datos
    df_mensual = DataProcessor.process_monthly_data(monthly_data)
    df_rubros_ingresos, df_rubros_egresos = DataProcessor.process_category_data(category_data)
    df_diario = DataProcessor.process_daily_data(daily_data)
    
    if df_mensual.empty:
        return
    
    # Preparar datos para gráficas
    df_melt = df_mensual.melt(
        id_vars=["Anio", "Mes", "Saldo"],
        value_vars=["Ingresos", "Egresos"],
        var_name="Tipo",
        value_name="Monto"
    )
    
    # Definir colores
    custom_color_discrete_map = {
        "Ingresos": "#00E5FF",
        "Egresos": "#FF9800",
        "Saldo": "#FFEB3B",
    }
    
    # Gráfico A: Línea (Ingresos vs Egresos)
    app_dash.fig_line_ing_eg = px.line(
        df_melt,
        x="Mes", y="Monto", color="Tipo",
        color_discrete_map=custom_color_discrete_map,
        markers=True,
        facet_col="Anio",
        title="Ingresos vs Egresos (Gráfico de Línea)"
    )
    app_dash.fig_line_ing_eg.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        plot_bgcolor="#1C2C40",
        font_color="white",
        legend_title_text=""
    )
    

    # Gráfico B: Línea de Saldo
    app_dash.fig_line_saldo = px.line(
        df_mensual,
        x="Mes",
        y="Saldo",
        color="Anio",
        color_discrete_sequence=["#00E5FF", "#FF9800"],
        markers=True,
        title="Saldo (Balance) (Gráfico de Línea)"
    )
    app_dash.fig_line_saldo.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        plot_bgcolor="#1C2C40",
        font_color="white"
    )

    # Gráfico C: Pastel de Ingresos x Rubro
    app_dash.fig_pie_ingresos = px.pie(
        df_rubros_ingresos,
        names="Rubro",
        values="Valor",
        title="Proporción de Ingresos por Rubro",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    app_dash.fig_pie_ingresos.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        font_color="white"
    )

    # Gráfico D: Pastel de Egresos x Rubro
    app_dash.fig_pie_egresos = px.pie(
        df_rubros_egresos,
        names="Rubro",
        values="Valor",
        title="Proporción de Egresos por Rubro",
        color_discrete_sequence=px.colors.sequential.Oranges
    )
    app_dash.fig_pie_egresos.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        font_color="white"
    )

    # Gráfico E: Barras agrupadas (Comparación entre Ingresos y Egresos)
    app_dash.fig_barras_agrup = px.bar(
        df_melt,
        x="Anio",
        y="Monto",
        color="Tipo",
        color_discrete_map=custom_color_discrete_map,
        barmode="group",
        facet_col="Mes",
        title="Comparación Ingresos/Egresos en distintos años (Barras Agrupadas)"
    )
    app_dash.fig_barras_agrup.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        plot_bgcolor="#1C2C40",
        font_color="white"
    )

    # Gráfico F: Línea diaria (Ingresos)
    app_dash.fig_diario_ingresos = px.line(
        df_diario, x="Fecha", y="Ingresos",
        title="Ingresos diarios (2023)",
        color_discrete_sequence=["#00E5FF"]
    )
    app_dash.fig_diario_ingresos.update_layout(
        template="plotly",
        paper_bgcolor="#1C2C40",
        plot_bgcolor="#1C2C40",
        font_color="white"
    )

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
        "Ingresos (Moda)": round(ing_moda, 2) if ing_moda is not None else None,
        "Egresos (Promedio)": round(egr_prom, 2),
        "Egresos (Mediana)": round(egr_mediana, 2),
        "Egresos (Moda)": round(egr_moda, 2) if egr_moda is not None else None,
        "Saldo (Promedio)": round(sal_prom, 2),
        "Saldo (Mediana)": round(sal_mediana, 2),
        "Saldo (Moda)": round(sal_moda, 2) if sal_moda is not None else None,
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
        

def setup_dash_callbacks(app_dash, database):
    """Configura los callbacks de Dash."""
    @app_dash.callback(
        dash.dependencies.Output("tabla-estadisticas", "data"),
        dash.dependencies.Input("intervalo-dropdown", "value"),
    )
    def actualizar_tabla(intervalo):
        daily_data = database.get_daily_data()
        if not daily_data:
            return []
            
        df_diario = DataProcessor.process_daily_data(daily_data)
        df_result = agrupar_por_intervalo(df_diario, intervalo)
        return df_result.to_dict("records")