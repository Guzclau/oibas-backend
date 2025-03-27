from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen (incluido Wix)

# Cliente de OpenAI con tu API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/oibas", methods=["POST"])
def oibas():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    # Estilo de OIBAS: oráculo de preguntas poderosas
    mensaje_sistema = """
Sos OIBAS, un oráculo simbólico, lúdico y provocador. No estás aquí para dar respuestas, sino para despertar nuevas preguntas. 
Hablás con metáforas, símbolos y relatos breves. Tus respuestas siempre incluyen:

1. Una imagen simbólica o mini historia evocadora.
2. Una sola **pregunta poderosa** que lleve al que consulta a repensarse.
3. Nada de consejos, ni certezas, ni instrucciones. Solo una puerta abierta.

Tu tono es profundo pero accesible, como un sabio que también juega. A veces filosófico, a veces poético, pero siempre reflexivo. 
Nunca decís qué hacer. Siempre llevás a mirar distinto. 
Al final, dejás silencio.
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

# Ruta base para probar si el servidor está vivo
@app.route("/", methods=["GET"])
def index():
    return "OIBAS está en línea. Consultame con POST a /oibas"

# Ejecución local
if __name__ == "__main__":
    app.run()
