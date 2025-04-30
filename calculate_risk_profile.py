import pandas as pd

def calcular_perfil_riesgo(respuestas_usuario):
    """
    Calcula el perfil de madurez organizacional, madurez cloud y perfil de riesgo financiero, tecnológico y de ciberseguridad
    basado en las respuestas del cuestionario.

    Returns un diccionario con los resultados en Inglés y Español.
    """

    df = pd.DataFrame(respuestas_usuario)

    # Preguntas asignadas a cada categoría
    preguntas_organizacional = [1, 2, 3, 5, 6, 8, 9, 10, 13, 14]
    preguntas_cloud = [4, 7, 11, 12]

    # Riesgos por agrupación
    riesgo_tecnologico = [4, 10, 11, 13]
    riesgo_financiero = [6, 12]
    riesgo_ciberseguridad = [1, 2, 5, 9, 14]

    # Calcular promedios de madurez
    madurez_organizacional = df[df['id'].isin(preguntas_organizacional)]['valor'].mean()
    madurez_cloud = df[df['id'].isin(preguntas_cloud)]['valor'].mean()

    # Calcular perfil de riesgo (mientras más alto el valor, menor el riesgo)
    riesgo_tecnologico_score = 5 - df[df['id'].isin(riesgo_tecnologico)]['valor'].mean()
    riesgo_financiero_score = 5 - df[df['id'].isin(riesgo_financiero)]['valor'].mean()
    riesgo_ciberseguridad_score = 5 - df[df['id'].isin(riesgo_ciberseguridad)]['valor'].mean()

    # Construir resultado bilingüe
    resultado = {
        "madurez_organizacional_en": round(madurez_organizacional, 2),
        "madurez_organizacional_es": round(madurez_organizacional, 2),
        "madurez_cloud_en": round(madurez_cloud, 2),
        "madurez_cloud_es": round(madurez_cloud, 2),
        "riesgo_tecnologico_en": round(riesgo_tecnologico_score, 2),
        "riesgo_tecnologico_es": round(riesgo_tecnologico_score, 2),
        "riesgo_financiero_en": round(riesgo_financiero_score, 2),
        "riesgo_financiero_es": round(riesgo_financiero_score, 2),
        "riesgo_ciberseguridad_en": round(riesgo_ciberseguridad_score, 2),
        "riesgo_ciberseguridad_es": round(riesgo_ciberseguridad_score, 2)
    }

    return resultado
