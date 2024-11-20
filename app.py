# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:48:06 2024

@author: valde
"""

import streamlit as st
import numpy_financial as npf

# Estilo para el ícono de ayuda con tooltip
tooltip_style = """
<style>
.tooltip {
    display: inline-block;
    position: relative;
    cursor: pointer;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    position: absolute;
    z-index: 1;
    bottom: 125%; /* Ajuste para que el texto aparezca arriba */
    left: 50%;
    margin-left: -100px;
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

st.markdown(tooltip_style, unsafe_allow_html=True)

# Función para generar tooltips
def tooltip_icon(text):
    return f"""
    <div class="tooltip">
        ℹ️
        <span class="tooltiptext">{text}</span>
    </div>
    """

# Fórmulas adicionales
def calculate_final_value(current_value, inflation, years):
    """Calcula el valor final ajustado por inflación."""
    return current_value * (1 + inflation / 100) ** years

def calculate_net_value(final_value, tax_rate):
    """Calcula el valor neto después de impuestos."""
    return final_value / (1 - tax_rate / 100)

def calculate_annual_savings(rate, years, initial_capital, net_goal):
    """Calcula el ahorro anual requerido sin incremento anual."""
    return abs(npf.pmt(rate / 100, years, -initial_capital, net_goal, 0))

def calculate_annual_savings_with_increase(rate, increase_rate, years, initial_capital, net_goal):
    """Calcula el ahorro anual requerido con incremento anual."""
    rate = rate / 100
    increase_rate = increase_rate / 100
    
    if rate == increase_rate:  # Manejar el caso especial donde ambas tasas son iguales
        # Fórmula simplificada cuando rate == increase_rate
        return (net_goal - (initial_capital * (1 + rate) ** years)) / \
               (years * (1 + rate) ** years)
    
    # Fórmula general
    numerator = net_goal - (initial_capital * (1 + rate) ** years)
    denominator = (((1 - ((1 + increase_rate) / (1 + rate)) ** years) / (rate - increase_rate)) *
                   (1 + rate) ** years)
    
    return numerator / denominator if denominator != 0 else 0

# Título
st.title("Calculadora de Ahorro para Gran Capital")

# Entradas del usuario
st.header("Datos del Objetivo")
objective = st.text_input(
    "Indica el objetivo que quieres lograr: " + 
    st.markdown(tooltip_icon("Escribe aquí en formato texto el objetivo que quieres alcanzar, como pagar el Master de tu hijo, comprarte un coche, o alcanzar un monto de dinero para la entrada de un piso."), unsafe_allow_html=True),
    placeholder="Ejemplo: Master para mi hijo"
)

current_value = st.number_input(
    "Importe actual del objetivo: " + 
    st.markdown(tooltip_icon("Introduce el valor en dinero que cuesta tu objetivo en la actualidad, como si lo pagaras hoy mismo."), unsafe_allow_html=True),
    min_value=0.0, step=1000.0
)

initial_capital = st.number_input(
    "Capital inicial: " +
    st.markdown(tooltip_icon("Escribe cuánto dinero tienes ahorrado en este momento para comenzar a alcanzar tu objetivo."), unsafe_allow_html=True),
    min_value=0.0, step=1000.0
)

years = st.number_input(
    "Número de años: " +
    st.markdown(tooltip_icon("Introduce el número de años en los que deseas alcanzar tu objetivo."), unsafe_allow_html=True),
    min_value=1, step=1
)

inflation = st.number_input(
    "Inflación promedio estimada (%): " +
    st.markdown(tooltip_icon("Indica la inflación promedio anual que esperas para los próximos años."), unsafe_allow_html=True),
    min_value=0.0, step=0.1
)

tax_rate = st.number_input(
    "Impuestos estimados sobre las ganancias (%): " +
    st.markdown(tooltip_icon("Introduce el porcentaje estimado de impuestos que se aplicará a las ganancias de tu inversión."), unsafe_allow_html=True),
    min_value=0.0, step=0.1
)

st.header("Cálculos Intermedios")
# Cálculo del gran capital y gran capital neto
final_value = calculate_final_value(current_value, inflation, years)
net_value = calculate_net_value(final_value, tax_rate)

st.write(f"**Valor final (Gran Capital) antes de impuestos:** ${final_value:,.2f}")
st.write(f"**Valor final NETO del Gran Capital:** ${net_value:,.2f}")

# Entradas adicionales para los cálculos de ahorro
st.header("Datos de la Inversión")
expected_rate = st.number_input(
    "Rentabilidad esperada de la inversión (%): " +
    st.markdown(tooltip_icon("Introduce la rentabilidad promedio anual que esperas obtener con tu inversión, en porcentaje."), unsafe_allow_html=True),
    min_value=0.0, step=0.1
)

annual_increase = st.number_input(
    "Incremento ahorro anual (%): " +
    st.markdown(tooltip_icon("Introduce el porcentaje anual en el que esperas aumentar tu capacidad de ahorro."), unsafe_allow_html=True),
    min_value=0.0, step=0.1
)

st.header("Cálculos Finales")
# Ahorro periódico sin incremento anual
annual_savings = calculate_annual_savings(expected_rate, years, initial_capital, net_value)
monthly_savings = annual_savings / 12

st.write(f"**Ahorro periódico anual (sin incremento anual):** ${annual_savings:,.2f}")
st.write(f"**Ahorro periódico mensual (sin incremento anual):** ${monthly_savings:,.2f}")

# Ahorro periódico con incremento anual
annual_savings_increase = calculate_annual_savings_with_increase(expected_rate, annual_increase, years, initial_capital, net_value)
monthly_savings_increase = annual_savings_increase / 12

st.write(f"**Ahorro periódico anual (con incremento anual):** ${annual_savings_increase:,.2f}")
st.write(f"**Ahorro periódico mensual (con incremento anual):** ${monthly_savings_increase:,.2f}")

st.markdown("---")
st.markdown("Desarrollado por **Tu Nombre**")
