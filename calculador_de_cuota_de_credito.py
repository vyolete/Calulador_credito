import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular la cuota de un crédito
def calcular_cuota_credito(monto, tasa_interes_anual, num_cuotas):
    tasa_mensual = tasa_interes_anual / 12 / 100
    cuota = monto * (tasa_mensual * (1 + tasa_mensual)**num_cuotas) / ((1 + tasa_mensual)**num_cuotas - 1)
    return cuota

# Función para generar la tabla de amortización
def generar_tabla_amortizacion(monto, tasa_interes_anual, num_cuotas):
    cuota = calcular_cuota_credito(monto, tasa_interes_anual, num_cuotas)
    saldo_inicial = monto
    tabla = []

    for i in range(1, num_cuotas + 1):
        interes = saldo_inicial * (tasa_interes_anual / 12 / 100)
        capital = cuota - interes
        saldo_final = saldo_inicial - capital
        tabla.append([i, saldo_inicial, cuota, capital, interes, saldo_final])
        saldo_inicial = saldo_final

    return pd.DataFrame(tabla, columns=["Mes", "Saldo Inicial", "Cuota", "Capital", "Interés", "Saldo Final"])

# Interfaz de usuario con Streamlit
st.title("Calculadora de Crédito")

st.sidebar.header("Parámetros del Crédito")
monto = st.sidebar.number_input("Monto del crédito:", min_value=0.0, value=10000.0, step=100.0)
tasa_interes_anual = st.sidebar.number_input("Tasa de interés anual (%):", min_value=0.0, value=5.0, step=0.1)
num_cuotas = st.sidebar.number_input("Número de cuotas:", min_value=1, value=12, step=1)

if st.sidebar.button("Calcular"):
    tabla_amortizacion = generar_tabla_amortizacion(monto, tasa_interes_anual, num_cuotas)

    st.subheader("Tabla de Amortización")
    st.dataframe(tabla_amortizacion)

    st.subheader("Gráfica de Amortización")
    fig, ax = plt.subplots()
    ax.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Capital"], label="Capital", color='blue')
    ax.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Interés"], label="Interés", color='orange')
    ax.plot(tabla_amortizacion["Mes"], tabla_amortizacion["Saldo Final"], label="Saldo Final", color='green')
    ax.set_title("Amortización del Crédito")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Monto en $")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
