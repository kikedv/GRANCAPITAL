# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:48:06 2024

@author: valde
"""

import streamlit as st
import numpy_financial as npf

# Fórmulas adicionales
def calculate_final_value(current_value, inflation, years):
    """Calcula el valor final ajustado por inflación."""
    return current_value * (1 + inflation / 100) ** years

def calculate_net_value(final_value, tax_rate):
    """Calcula el valor neto después de impuestos."""
    return final_value / (1 - tax_rate / 100)

def calculate_annual_savings(rate, years, initial_capital, net_goal):
    """Calcula el ahorro anual requerido sin incremento anual."""
    return npf.pmt(rate / 100, years, -initial_capital, net_goal, 0)

def calculate_annual_savings_with_increase(rate, increase_rate, years, initial_capital, net_goal):
    """Calcula el ahorro anual requerido con incremento anual."""
    rate = rate / 100
    increase_rate = increase_rate / 100
    numerator = net_goal - (initial_capital * (1 + rate) ** years)
    denominator = (((1 - ((1 + increase_rate) / (1 + rate)) ** years) / (rate - increase_rate)) *
                   (1 + rate) ** years)
    return numerator / denominator if denominator != 0 else 0

# Título
st.title("Calculadora de Ahorro para Gran Capital")

# Entradas del usuario
st.header("Datos del Objetivo")
objective = st.text_input("Indica el objetivo que quieres lograr:", placeholder="Ejemplo: Master para mi hijo")
current_value = st.number_input("Importe actual del objetivo:", min_value=0.0, step=1000.0)
initial_capital = st.number_input("Capital inicial:", min_value=0.0, step=1000.0)
years = st.number_input("Número de años:", min_value=1, step=1)
inflation = st.number_input("Inflación promedio estimada (%):", min_value=0.0, step=0.1)
tax_rate = st.number_input("Impuestos estimados sobre las ganancias (%):", min_value=0.0, step=0.1)

st.header("Cálculos Intermedios")
# Cálculo del gran capital y gran capital neto
final_value = calculate_final_value(current_value, inflation, years)
net_value = calculate_net_value(final_value, tax_rate)

st.write(f"**Valor final (Gran Capital) antes de impuestos:** ${final_value:,.2f}")
st.write(f"**Valor final NETO del Gran Capital:** ${net_value:,.2f}")

# Entradas adicionales para los cálculos de ahorro
st.header("Datos de la Inversión")
expected_rate = st.number_input("Rentabilidad esperada de la inversión (%):", min_value=0.0, step=0.1)
annual_increase = st.number_input("Incremento ahorro anual (%):", min_value=0.0, step=0.1)

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
