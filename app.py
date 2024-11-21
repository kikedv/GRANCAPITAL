# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:48:06 2024

@author: valde
"""

import streamlit as st
import numpy_financial as npf
import matplotlib.pyplot as plt
import pandas as pd

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

    texto_resultado = (
        f"En base a estos datos, el importe que debes alcanzar es {final_value:,.2f}. "
        f"Sin embargo, como Hacienda te quitará una parte de los beneficios, deberás alcanzar un capital algo mayor. "
        f"Ese GRAN CAPITAL es de {net_value:,.2f}."
    )
    st.markdown(texto_resultado)
    st.markdown(" ")

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

    st.markdown(f"**Ahorro periódico anual (sin incremento anual):** ${annual_savings:,.2f}")
    st.markdown(f"**Ahorro periódico mensual (sin incremento anual):** ${monthly_savings:,.2f}")

    # Cálculo del ahorro con incremento anual
    annual_savings_increase = calculate_annual_savings_with_increase(
        expected_rate, annual_increase, years, initial_capital, net_value
    )
    monthly_savings_increase = annual_savings_increase / 12

    st.markdown(f"**Ahorro periódico anual (con incremento anual):** ${annual_savings_increase:,.2f}")
    st.markdown(f"**Ahorro periódico mensual (con incremento anual):** ${monthly_savings_increase:,.2f}")

    # Gráfico de evolución del capital
    st.header("Evolución del Capital Acumulado")

    # Cálculo de la evolución del capital
    capital_evolucion = []
    ahorro_anual = annual_savings_increase
    capital_actual = initial_capital

    for i in range(1, years + 1):
        capital_actual *= (1 + expected_rate / 100)  # Aplicar rentabilidad
        capital_actual += ahorro_anual              # Agregar el ahorro anual
        capital_evolucion.append(capital_actual)
        ahorro_anual *= (1 + inflation / 100)       # Incrementar el ahorro anual según la inflación

    # Crear DataFrame para el gráfico
    df_evolucion = pd.DataFrame({
        "Año": list(range(1, years + 1)),
        "Capital Acumulado": capital_evolucion
    })

    # Generar el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df_evolucion["Año"], df_evolucion["Capital Acumulado"], marker='o')
    plt.title("Evolución del Capital Acumulado", fontsize=16)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Capital Acumulado ($)", fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

st.markdown("---")
st.markdown("Desarrollado por **Tu Nombre**")
