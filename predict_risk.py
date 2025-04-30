# predict_risk.py

import joblib
import numpy as np

# Cargar el modelo entrenado
model = joblib.load("model_sklearn_xgb.pkl")

def predecir_madurez_y_riesgo(respuestas_usuario):
    '''
    respuestas_usuario: lista de 14 valores (1–5) en el mismo orden que las preguntas
    Retorna: diccionario con predicción de madurez y riesgo, en inglés y español
    '''
    if len(respuestas_usuario) != 14:
        raise ValueError("Se esperaban exactamente 14 respuestas")

    entrada = np.array(respuestas_usuario).reshape(1, -1)
    pred = model.predict(entrada)[0]

    return {
        "madurez_general_en": round(pred[0], 2),
        "madurez_general_es": round(pred[0], 2),
        "riesgo_general_en": round(pred[1], 2),
        "riesgo_general_es": round(pred[1], 2)
    }