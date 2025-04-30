# app_local.py

import streamlit as st
import pandas as pd
import json
from calculate_risk_profile import calcular_perfil_riesgo
from predict_risk import predecir_madurez_y_riesgo
from visualizations import generar_radar_chart, generar_heatmap, mostrar_badges, mostrar_leyenda_madurez, mostrar_recomendaciones
from dofa_analysis import generar_dofa, mostrar_dofa_en_app, exportar_dofa_html, exportar_dofa_pdf

# Cargar cuestionario bilingüe
with open("onboarding_questionnaire_bilingue.json", "r", encoding="utf-8") as f:
    preguntas = json.load(f)

# Selección de idioma
idioma = st.radio("Select Language / Seleccione Idioma", ("English", "Español"))
st.title("🌐 Cloud Maturity Risk Solutions")

# Captura de respuestas
respuestas = []
for pregunta in preguntas:
    texto_pregunta = pregunta["pregunta_en"] if idioma == "English" else pregunta["pregunta_es"]
    opciones = [op["texto_en"] if idioma == "English" else op["texto_es"] for op in pregunta["opciones"]]
    seleccion = st.selectbox(texto_pregunta, opciones, key=pregunta["id"])

    for op in pregunta["opciones"]:
        if (op["texto_en"] if idioma == "English" else op["texto_es"]) == seleccion:
            respuestas.append({
                "id": pregunta["id"],
                "pregunta": texto_pregunta,
                "respuesta": seleccion,
                "valor": op["valor"],
                "nivel_madurez": op["nivel_madurez"],
                "tipo_de_riesgo": pregunta["tipo_de_riesgo"]
            })
            break

# Evaluar perfil
if st.button("Evaluate Profile / Evaluar Perfil"):
    df_resultados = pd.DataFrame(respuestas)
    st.success("✅ Evaluation complete / Evaluación completada")
    st.subheader("📄 Answers Summary / Resumen de Respuestas")
    st.dataframe(df_resultados)

    perfil = calcular_perfil_riesgo(respuestas)
    predicciones = predecir_madurez_y_riesgo([r["valor"] for r in respuestas])

    st.subheader("📊 Maturity & Risk Profile" if idioma == "English" else "📊 Perfil de Madurez y Riesgo")
    mostrar_badges(perfil, idioma=idioma)

    st.subheader("🧠 AI-Based Predictions" if idioma == "English" else "🧠 Predicciones con IA")
    mostrar_badges(predicciones, idioma=idioma)

    st.subheader("📌 Radar Chart")
    generar_radar_chart(perfil, predicciones, idioma=idioma)

    st.subheader("🔥 Heatmap: Exposure vs Maturity" if idioma == "English" else "🔥 Mapa de Exposición vs Madurez")
    generar_heatmap(perfil["madurez_organizacional_en" if idioma=="English" else "madurez_organizacional_es"],
                    perfil["riesgo_ciberseguridad_en" if idioma=="English" else "riesgo_ciberseguridad_es"],
                    idioma=idioma)

    st.subheader("📘 Maturity Levels (NIST / CoE)")
    mostrar_leyenda_madurez(idioma=idioma)

    st.subheader("🧩 Recommendations")
    mostrar_recomendaciones(perfil, idioma=idioma)

    st.subheader("📋 SWOT / DOFA Analysis")
    dofa = generar_dofa(perfil, predicciones, idioma=idioma)
    mostrar_dofa_en_app(dofa, idioma=idioma)

    if st.button("📥 Export DOFA to HTML"):
        exportar_dofa_html(dofa)
        st.success("✅ Exported as dofa_matrix.html")

    if st.button("📥 Export DOFA to PDF"):
        exportar_dofa_pdf(dofa)
        st.success("✅ Exported as dofa_matrix.pdf")