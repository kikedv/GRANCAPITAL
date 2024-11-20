# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:48:06 2024

@author: valde
"""

import streamlit as st
import numpy_financial as npf

# Estilo para tooltips
tooltip_style = """
<style>
.tooltip {
    display: inline-block;
    position: relative;
    cursor: pointer;
    margin-left: 5px;
    color: #4a4a4a;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 220px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -110px;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 12px;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
"""

# Agregar estilos personalizados
st.markdown(tooltip_style, unsafe_allow_html=True)

# Función para generar tooltips
def tooltip_icon(tooltip_text):
    return f"""
    <div class="tooltip">
        ℹ️
        <span class="tooltiptext">{tooltip_text}</span>
    </div>
    """

# Fórmulas adicionales
def calculate_final_value(current_value, inflation, years):
    return current_value * (1 + inflation / 100) ** years

def calculate_net_value(final_value, tax_rate):
    return final_value / (1 - tax_rate / 100)

def calculate_annual_savings(rate, years, initial_capital, net_goal):
    return abs(npf.pmt(rate / 100, years, -initial_capital, net_goal, 0))

def calculate_annual_savings_with_increase(rate, increase_rate, years, initial_capital, net_goal):
    rate = rate / 100
    increase_rate = increase_rate / 100
    
    if rate == increase_rate:
        return (net_goal - (initial_capital * (1 + rate) ** years)) / \
               (years * (1 + rate) ** years)
    
    numerator = net_goal - (initial_capital * (1 + rate) ** years)
    denominator = (((1 - ((1 + increase_rate) / (1 + rate)) ** years) / (rate - increase_rate)) *
                   (1 + rate) ** years)
    return numerator / denominator if denominator != 0 else 0

# Título
st.title("Calculadora de Ahorro para Gran Capital")

# Entradas del usuario
st.header("Datos del Objetivo")

col1, col2 = st.columns([3, 1])
with col1:
    objective = st.text_input("Objetivo:", placeholder="Ejemplo: Master para mi hijo")
with col2:
    st.markdown(tooltip_icon("Escribe aquí el objetivo que quieres alcanzar, como pagar el Master de tu hijo, comprarte un coche o reunir un monto de dinero para la entrada de un piso."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    current_value = st.number_input("Importe actual del objetivo:", min_value=0.0, step=1000.0)
with col2:
    st.markdown(tooltip_icon("Introduce el costo actual de tu objetivo como si lo pagaras hoy mismo."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    initial_capital = st.number_input("Capital inicial:", min_value=0.0, step=1000.0)
with col2:
    st.markdown(tooltip_icon("Escribe cuánto dinero tienes ahorrado actualmente para alcanzar tu objetivo."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    years = st.number_input("Número de años:", min_value=1, step=1)
with col2:
    st.markdown(tooltip_icon("Indica en cuántos años deseas alcanzar tu objetivo."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    inflation = st.number_input("Inflación promedio estimada (%):", min_value=0.0, step=0.1)
with col2:
    st.markdown(tooltip_icon("Introduce la inflación promedio anual esperada para los próximos años."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    tax_rate = st.number_input("Impuestos estimados sobre las ganancias (%):", min_value=0.0, step=0.1)
with col2:
    st.markdown(tooltip_icon("Escribe el porcentaje estimado de impuestos sobre las ganancias de tu inversión."), unsafe_allow_html=True)

st.header("Cálculos Intermedios")
final_value = calculate_final_value(current_value, inflation, years)
net_value = calculate_net_value(final_value, tax_rate)

# Texto explicativo personalizado
st.markdown(f"""
En base a estos datos, el importe que debes alcanzar es **${final_value:,.2f}**.
Ahora bien, como Hacienda te quitará una parte de los beneficios, deberás alcanzar un capital algo mayor. Ese **GRAN CAPITAL** es de **${net_value:,.2f}**.
""")

# Entradas adicionales para los cálculos de ahorro
st.header("Datos de la Inversión")

col1, col2 = st.columns([3, 1])
with col1:
    expected_rate = st.number_input("Rentabilidad esperada de la inversión (%):", min_value=0.0, step=0.1)
with col2:
    st.markdown(tooltip_icon("Introduce la rentabilidad promedio anual que esperas obtener con tu inversión."), unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    annual_increase = st.number_input("Incremento ahorro anual (%):", min_value=0.0, step=0.1)
with col2:
    st.markdown(tooltip_icon("Introduce el porcentaje anual en el que esperas aumentar tu capacidad de ahorro."), unsafe_allow_html=True)

st.header("Cálculos Finales")
annual_savings = calculate_annual_savings(expected_rate, years, initial_capital, net_value)
monthly_savings = annual_savings / 12

st.write(f"**Ahorro periódico anual (sin incremento anual):** ${annual_savings:,.2f}")
st.write(f"**Ahorro periódico mensual (sin incremento anual):** ${monthly_savings:,.2f}")

annual_savings_increase = calculate_annual_savings_with_increase(expected_rate, annual_increase, years, initial_capital, net_value)
monthly_savings_increase = annual_savings_increase / 12

st.write(f"**Ahorro periódico anual (con incremento anual):** ${annual_savings_increase:,.2f}")
st.write(f"**Ahorro periódico mensual (con incremento anual):** ${monthly_savings_increase:,.2f}")

st.markdown("---")
st.markdown("Desarrollado por **Tu Nombre**")
