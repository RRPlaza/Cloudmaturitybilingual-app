# dofa_analysis.py

import streamlit as st
import pandas as pd
from fpdf import FPDF

def generar_dofa(perfil, pred, idioma='English'):
    def nivel(valor):
        if valor >= 4.6: return "Optimized"
        elif valor >= 4.0: return "Managed"
        elif valor >= 3.0: return "Repeatable"
        elif valor >= 2.0: return "Opportunistic"
        else: return "Ad Hoc"

    madurez = perfil.get("madurez_organizacional_en" if idioma == "English" else "madurez_organizacional_es", 0)
    riesgo = perfil.get("riesgo_ciberseguridad_en" if idioma == "English" else "riesgo_ciberseguridad_es", 0)
    pred_madurez = pred.get("madurez_general_en" if idioma == "English" else "madurez_general_es", 0)
    pred_riesgo = pred.get("riesgo_general_en" if idioma == "English" else "riesgo_general_es", 0)

    dofa = {
        "Strengths" if idioma == "English" else "Fortalezas": [],
        "Weaknesses" if idioma == "English" else "Debilidades": [],
        "Opportunities" if idioma == "English" else "Oportunidades": [],
        "Threats" if idioma == "English" else "Amenazas": []
    }

    if madurez >= 4:
        dofa["Strengths" if idioma == "English" else "Fortalezas"].append("Organizational governance is mature" if idioma == "English" else "La gobernanza organizacional es madura")
    else:
        dofa["Weaknesses" if idioma == "English" else "Debilidades"].append("Governance processes need strengthening" if idioma == "English" else "Los procesos de gobernanza deben fortalecerse")

    if riesgo >= 3:
        dofa["Threats" if idioma == "English" else "Amenazas"].append("High cybersecurity exposure" if idioma == "English" else "Alta exposición en ciberseguridad")
    else:
        dofa["Opportunities" if idioma == "English" else "Oportunidades"].append("Leverage low risk to optimize resilience" if idioma == "English" else "Aprovechar el bajo riesgo para optimizar la resiliencia")

    if pred_madurez >= 4:
        dofa["Opportunities" if idioma == "English" else "Oportunidades"].append("Scalable improvement potential detected" if idioma == "English" else "Potencial de mejora escalable detectado")
    else:
        dofa["Weaknesses" if idioma == "English" else "Debilidades"].append("Maturity gaps predicted by AI" if idioma == "English" else "Brechas de madurez detectadas por IA")

    return dofa

def mostrar_dofa_en_app(dofa_dict, idioma='English'):
    st.markdown("### SWOT Matrix" if idioma == "English" else "### Matriz DOFA")
    df = pd.DataFrame.from_dict(dofa_dict, orient='index').transpose().fillna("")
    st.table(df)

def exportar_dofa_html(dofa_dict, filename="dofa_matrix.html"):
    df = pd.DataFrame.from_dict(dofa_dict, orient='index').transpose().fillna("")
    df.to_html(filename, index=False)

def exportar_dofa_pdf(dofa_dict, filename="dofa_matrix.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Matriz DOFA", ln=True, align='C')

    for categoria, items in dofa_dict.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=categoria, ln=True)
        pdf.set_font("Arial", size=11)
        for item in items:
            pdf.multi_cell(0, 10, f"- {item}")
        pdf.ln(5)

    pdf.output(filename)