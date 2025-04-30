# visualizations.py

import streamlit as st
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Radar chart con madurez organizacional, cloud y predicha
def generar_radar_chart(perfil_real, perfil_predicho, idioma='English'):
    labels = ["Organizational Maturity", "Cloud Maturity", "Predicted Maturity"] if idioma == 'English' else ["Madurez Organizacional", "Madurez Cloud", "Madurez Predicha"]
    values = [
        perfil_real.get("madurez_organizacional_en" if idioma == "English" else "madurez_organizacional_es", 0),
        perfil_real.get("madurez_cloud_en" if idioma == "English" else "madurez_cloud_es", 0),
        perfil_predicho.get("madurez_general_en" if idioma == "English" else "madurez_general_es", 0)
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        name='Maturity Profile'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,5])),
        showlegend=False,
        title="Radar Chart – Maturity Profile" if idioma == 'English' else "Gráfico Radar – Perfil de Madurez"
    )
    st.plotly_chart(fig)

# Heatmap exposición vs madurez
def generar_heatmap(madurez_score, riesgo_score, idioma='English'):
    fig, ax = plt.subplots()
    data = np.zeros((5,5))
    x_idx = int(round(5 - riesgo_score)) - 1
    y_idx = int(round(madurez_score)) - 1
    data[y_idx, x_idx] = 1

    sns.heatmap(data, cmap="YlOrRd", cbar=False, annot=False, ax=ax, linewidths=0.5, square=True)
    ax.invert_yaxis()

    ax.set_xticks(np.arange(5)+0.5)
    ax.set_yticks(np.arange(5)+0.5)
    ax.set_xticklabels(['1','2','3','4','5'])
    ax.set_yticklabels(['1','2','3','4','5'])

    ax.set_xlabel("Risk Level (Low→High)" if idioma == "English" else "Nivel de Riesgo (Bajo→Alto)")
    ax.set_ylabel("Maturity Level (Low→High)" if idioma == "English" else "Nivel de Madurez (Bajo→Alto)")
    ax.set_title("Heatmap: Maturity vs Risk" if idioma == "English" else "Mapa de Calor: Madurez vs Riesgo")
    st.pyplot(fig)

# Badges visuales
def mostrar_badges(perfil, idioma='English'):
    for key, value in perfil.items():
        if '_en' in key and idioma == 'English':
            label = key.replace("_en", "").replace("_", " ").title()
        elif '_es' in key and idioma == 'Español':
            label = key.replace("_es", "").replace("_", " ").title()
        else:
            continue

        color = "🟢" if value >= 4 else "🟡" if value >= 2.5 else "🔴"
        st.markdown(f"**{label}:** {value} {color}")

# Leyenda profesional
def mostrar_leyenda_madurez(idioma='English'):
    st.markdown("### Maturity Level Mapping" if idioma == 'English' else "### Mapeo de Niveles de Madurez")
    niveles = [
        ("1.0 – 1.9", "Ad Hoc", "Partial", "No formal governance / Sin gobierno formal"),
        ("2.0 – 2.9", "Opportunistic", "Risk-Informed", "Initial awareness / Consciencia inicial"),
        ("3.0 – 3.9", "Repeatable", "Repeatable", "Documented and consistent / Documentado y repetible"),
        ("4.0 – 4.5", "Managed", "Adaptive", "Actively monitored / Gestionado"),
        ("4.6 – 5.0", "Optimized", "Adaptive", "Continuously improving / Mejora continua")
    ]
    for rango, coe, nist, desc in niveles:
        st.markdown(f"**{rango}** → CoE: *{coe}*, NIST: *{nist}* – {desc}")

# Recomendaciones automáticas
def mostrar_recomendaciones(perfil, idioma='English'):
    st.markdown("### Recommendations" if idioma == "English" else "### Recomendaciones")

    def nivel(valor):
        if valor >= 4.6: return "Optimized"
        elif valor >= 4.0: return "Managed"
        elif valor >= 3.0: return "Repeatable"
        elif valor >= 2.0: return "Opportunistic"
        else: return "Ad Hoc"

    madurez = perfil.get("madurez_organizacional_en" if idioma == "English" else "madurez_organizacional_es", 0)
    riesgo = perfil.get("riesgo_ciberseguridad_en" if idioma == "English" else "riesgo_ciberseguridad_es", 0)

    if idioma == "English":
        st.write(f"Organizational maturity is at **{nivel(madurez)}** level.")
        st.write(f"Cybersecurity risk is rated at **{nivel(riesgo)}** level.")
        if riesgo >= 3:
            st.write("🔴 High risk detected. Consider implementing a continuous monitoring program, strengthening access controls, and reviewing your incident response strategy.")
        elif madurez < 3:
            st.write("🟡 Consider maturing your governance and training practices to reduce exposure.")
        else:
            st.write("🟢 Your posture is consistent with a mature and secure organization.")
    else:
        st.write(f"La madurez organizacional está en el nivel **{nivel(madurez)}**.")
        st.write(f"El riesgo de ciberseguridad se encuentra en nivel **{nivel(riesgo)}**.")
        if riesgo >= 3:
            st.write("🔴 Riesgo alto detectado. Considere implementar monitoreo continuo, reforzar controles de acceso y revisar su estrategia de respuesta a incidentes.")
        elif madurez < 3:
            st.write("🟡 Se recomienda fortalecer la gobernanza y capacitación del personal.")
        else:
            st.write("🟢 Su postura es consistente con una organización madura y segura.")