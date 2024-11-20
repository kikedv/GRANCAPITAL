# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:48:06 2024

@author: valde
"""

import streamlit as st
import numpy_financial as npf

# Fórmulas adicionales
def calculate_final_value(current_value, inflation, years):
    return current_value * (1 + inflation / 100) ** years

def calculate_net_value(final_value, tax_rate):
    return final_value / (1 - tax_rate / 100)

# Título
st.title("Calculadora de Ahorro para Gran Capital")

# Entradas del usuario
st.header("Datos del Objetivo")

objective = st.text_input("Objetivo:", placeholder="Ejemplo: Master para mi hijo")
current_value = st.number_input("Importe actual del objetivo:", min_value=0.0, step=1000.0)
initial_capital = st.number_input("Capital inicial:", min_value=0.0, step=1000.0)
years = st.number_input("Número de años:", min_value=1, step=1)
inflation = st.number_input("Inflación promedio estimada (%):", min_value=0.0, step=0.1)
tax_rate = st.number_input("Impuestos estimados sobre las ganancias (%):", min_value=0.0, step=0.1)

st.header("Cálculos Intermedios")

# Cálculo del gran capital y gran capital neto
if current_value > 0 and inflation >= 0 and years > 0 and tax_rate >= 0:
    final_value = calculate_final_value(current_value, inflation, years)
    net_value = calculate_net_value(final_value, tax_rate)

    # Texto explicativo en un párrafo con formato mejorado
    st.markdown(
        f"En base a estos datos, el importe que debes alcanzar es **${final_value:,.2f}**. "
        f"Sin embargo, como Hacienda te quitará una parte de los beneficios, deberás alcanzar un capital algo mayor. "
        f"Ese **GRAN CAPITAL** es de **${net_value:,.2f}**. 💰"
    )
else:
    st.markdown("Por favor, completa todos los campos para obtener los resultados. 🙏")

# Entradas adicionales para los cálculos de ahorro
st.header("Datos de la Inversión")

expected_rate = st.number_input("Rentabilidad esperada de la inversión (%):", min_value=0.0, step=0.1)
annual_increase = st.number_input("Incremento ahorro anual (%):", min_value=0.0, step=0.1)

st.markdown("---")
st.markdown("Desarrollado por **Tu Nombre**")
