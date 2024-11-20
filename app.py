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

def calculate_annual_savings(rate, years, initial_capital, net_goal):
    return abs(npf.pmt(rate / 100, years, -initial_capital, net_goal, 0))

def calculate_annual_savings_with_increase(rate, increase_rate, years, initial_capital, net_goal):
    rate = rate / 100
    increase_rate = increase_rate / 100

    if rate == increase_rate:
        return (net_goal - (initial_capital * (1 + rate) ** years)) / (years * (1 + rate) ** years)

    numerator = net_goal - (initial_capital * (1 + rate) ** years)
    denominator = (
        ((1 - ((1 + increase_rate) / (1 + rate)) ** years) / (rate - increase_rate))
        * (1 + rate) ** years
    )
    return numerator / denominator if denominator != 0 else 0

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

    # Texto explicativo con formato mejorado
    texto_resultado = (
        f"En base a estos datos, el importe que debes alcanzar es {final_value:,.2f}. "
        f"Sin embargo, como Hacienda te quitará una parte de los beneficios, deberás alcanzar un capital algo mayor. "
        f"Ese GRAN CAPITAL es de {net_value:,.2f}."
    )

    # Mostrar texto formateado
    st.markdown(texto_resultado)
    st.markdown(" ")

    # Nuevo párrafo
    nuevo_parrafo = (
        "Ahora introduce la rentabilidad promedio anual que esperas alcanzar con tu estrategia de inversión. "
        "En la sección de carteras modelo, tienes varias propuestas que te indican la rentabilidad estimada "
        "en base a cómo se han comportado en el pasado. Introduce también un porcentaje de incremento anual "
        "del ahorro que destinarás a la inversión. Sería importante que lo introdujeras porque eso querrá "
        "decir que todos los años tratarás de incrementar tus aportaciones en ese porcentaje para alimentar "
        "más a tu \"máquina de hacer dinero\"."
    )
    st.markdown(nuevo_parrafo)
else:
    st.markdown("Por favor, completa todos los campos para obtener los resultados. 🙏")

# Entradas adicionales para los cálculos de ahorro
st.header("Datos de la Inversión")

expected_rate = st.number_input("Rentabilidad esperada de la inversión (%):", min_value=0.0, step=0.1)
annual_increase = st.number_input("Incremento ahorro anual (%):", min_value=0.0, step=0.1)

# Cálculos finales
if expected_rate > 0 and years > 0 and net_value > 0:
    st.header("Cálculos Finales")

    # Cálculo del ahorro sin incremento anual
    annual_savings = calculate_annual_savings(expected_rate, years, initial_capital, net_value)
    monthly_savings = annual_savings / 12

    # Mostrar resultados
    st.markdown(f"**Ahorro periódico anual (sin incremento anual):** ${annual_savings:,.2f}")
    st.markdown(f"**Ahorro periódico mensual (sin incremento anual):** ${monthly_savings:,.2f}")

    # Cálculo del ahorro con incremento anual
    annual_savings_increase = calculate_annual_savings_with_increase(
        expected_rate, annual_increase, years, initial_capital, net_value
    )
    monthly_savings_increase = annual_savings_increase / 12

    st.markdown(f"**Ahorro periódico anual (con incremento anual):** ${annual_savings_increase:,.2f}")
    st.markdown(f"**Ahorro periódico mensual (con incremento anual):** ${monthly_savings_increase:,.2f}")

    # Resumen
    st.header("Resumen")
    resumen = (
        f"¿Qué quiere decir todo lo que hemos calculado? Muy fácil, para alcanzar tu objetivo, tienes que alcanzar un GRAN CAPITAL de {net_value:,.2f} "
        f"dentro de {years} años. Para lograr ese objetivo, y suponiendo que ejecutes una estrategia de inversión que te proporcione un {expected_rate:.2f}% "
        f"de rentabilidad anual promedio, tendrás que ahorrar e invertir cada mes un monto de {monthly_savings:,.2f} o, en términos anuales, {annual_savings:,.2f}. "
        f"Ahora bien, si haces el esfuerzo de incrementar todos los años tus aportaciones en un {annual_increase:.2f}%, la cantidad mensual y anual varía en el "
        f"primer año. Ahora tendrás que ahorrar e invertir ese primer año un total de {annual_savings_increase:,.2f}, es decir, {monthly_savings_increase:,.2f} al mes."
    )
    st.markdown(resumen)

st.markdown("---")
st.markdown("Desarrollado por **Tu Nombre**")
