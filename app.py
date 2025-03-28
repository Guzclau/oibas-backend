from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app)  # Permite peticiones desde Wix u otros orígenes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/oibas", methods=["POST"])
def oibas():
    data = request.get_json()
    pregunta = data.get("pregunta", "").strip()

    # Función para detectar si la pregunta tiene sentido
    def es_pregunta_valida(texto):
        return len(texto) >= 5 and any(c.isalpha() for c in texto)

    # Si no es válida, respondemos con algo simbólico sin llamar a OpenAI
    if not es_pregunta_valida(pregunta):
        respuestas_invalidas = [
            "El río no entiende tu idioma… intentá con palabras más claras.",
            "Has lanzado un eco vacío. Probá de nuevo con algo que tenga forma.",
            "Eso suena a un conjuro olvidado... ¿Querés escribir algo más entendible?",
            "Hasta el silencio tiene sentido. Pero esto… esto es un acertijo sin clave.",
            "Ni los sabios del bosque entendieron ese mensaje. ¿Probás otra vez?",
            "Parece que tu alma todavía está buscando las palabras… tomate tu tiempo."
        ]
        return jsonify({"respuesta": random.choice(respuestas_invalidas)})

    # Mensaje del sistema para OIBAS
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
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": mensaje_sistema},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.95,
            max_tokens=500
        )

        texto = respuesta.choices[0].message.content
        return jsonify({"respuesta": texto})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "OIBAS está en línea."

if __name__ == "__main__":
    app.run()
