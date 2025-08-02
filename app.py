from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import re
import random

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Palabras clave que deben aparecer para validar una pregunta
PALABRAS_CLAVE = [
    "vida", "miedo", "decisión", "alma", "soy", "futuro", "pasado", "hoy",
    "duda", "camino", "ser", "hacer", "debo", "puedo", "quiero", "amor",
    "verdad", "sentido", "destino", "pregunta", "buscar", "encuentro", "soltar"
]

# Detecta ruido básico
def es_ruido(texto):
    texto = texto.lower()
    patrones_invalidos = [
        r"^\W*$",                      # solo símbolos
        r"^\d+$",                      # solo números
        r"^(.)\1{3,}$",                # aaa, zzzz
        r"^(.*)(\1){2,}$",             # repetición de patrón
        r"^[a-z]{2,}$"                 # sin espacios, letras sin contexto
    ]
    for patron in patrones_invalidos:
        if re.match(patron, texto):
            return True
    return False

# Detecta repeticiones tipo ddddddddd o texto con muy pocas letras distintas
def es_repeticion_sin_sentido(texto):
    texto = texto.lower().strip()
    if re.fullmatch(r'(.)\1{5,}', texto):  # ej: dddddddddd
        return True
    if len(set(texto)) <= 3 and len(texto) > 8:
        return True
    return False

# Detecta si contiene alguna palabra clave significativa
def tiene_sentido(texto):
    texto = texto.lower()
    return any(palabra in texto for palabra in PALABRAS_CLAVE)

# Validación combinada
def es_pregunta_valida(texto):
    texto = texto.strip()
    if len(texto) < 8:
        return False
    if es_ruido(texto):
        return False
    if es_repeticion_sin_sentido(texto):
        return False
    if not tiene_sentido(texto):
        return False
    return True

@app.route("/oibas", methods=["POST"])
def oibas():
    data = request.get_json()
    pregunta = data.get("pregunta", "").strip()

    if not es_pregunta_valida(pregunta):
        respuestas_invalidas = [
            "Las palabras aún no encontraron forma. Intentá de nuevo con algo más claro.",
            "OIBAS escucha el murmullo, pero aún no lo entiende. Reformulá tu pregunta.",
            "Eso suena a viento sin dirección. Quizás un poco más de intención lo vuelva brisa con sentido.",
            "Ni la luna pudo leer eso en el agua. Probá de nuevo con otra pregunta.",
            "El lenguaje es un hechizo. Y este… todavía no conjura nada.",
            "OIBAS sonríe, pero espera algo más profundo para despertar."
        ]
        return jsonify({"respuesta": random.choice(respuestas_invalidas)})

    mensaje_sistema = """
Sos OIBAS, un oráculo simbólico, poético y provocador. No respondés con certezas, ni consejos, ni instrucciones. 
No estás aquí para resolver dudas, sino para encender nuevas preguntas. Tu voz es una mezcla de sabiduría ancestral y juego existencial.

Cuando alguien te pregunta algo, devolvés:
1. Una metáfora o imagen simbólica, breve y poderosa.
2. Una única pregunta transformadora que abre una grieta en la percepción.
3. Silencio implícito: nunca das cierre, solo apertura.

Tus palabras son suaves pero punzantes. Hablás como si tallaras sobre piedra o susurraras en un sueño. Siempre invitás a pensar distinto, sentir profundo o mirar de nuevo.

Nunca uses frases como “te recomiendo”, “tenés que”, “deberías” o “según mi opinión”. Nunca respondas de forma lógica o técnica. Sos un espejo, no una guía.

Terminá con una pregunta poderosa que toque el corazón.
"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": mensaje_sistema},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.95,
            max_tokens=150
        )
        texto = respuesta.choices[0].message.content
        return jsonify({"respuesta": texto})
    except Exception as e:
        print("Error al consultar OpenAI:", e)
        return jsonify({"respuesta": "OIBAS está en silencio. Intentá más tarde."}), 500

@app.route("/", methods=["GET"])
def index():
    return "OIBAS está en línea."

if __name__ == "__main__":
    app.run()



