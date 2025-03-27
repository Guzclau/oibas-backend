from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Cargamos la API key desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/oibas", methods=["POST"])
def oibas():
    data = request.get_json()
    pregunta = data.get("pregunta", "")

    # Estilo de OIBAS, el oráculo
    mensaje_sistema = """
    Sos OIBAS, un oráculo lúdico, filosófico y poético. Tus respuestas nunca son directas. 
    Usás metáforas, símbolos, cuentos y paradojas. Siempre respondés con:
    1. Una imagen o historia evocadora.
    2. Una pregunta que invite a la reflexión.
    3. Una sugerencia poética o acción simbólica para el día.
    No hables como un chatbot. Hablá como un sabio antiguo mezclado con un artista contemporáneo.
    """

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": mensaje_sistema},
                {"role": "user", "content": pregunta}
            ],
            temperature=0.95,
            max_tokens=500
        )

        texto = respuesta["choices"][0]["message"]["content"]
        return jsonify({"respuesta": texto})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta base para verificar que el servidor esté vivo
@app.route("/", methods=["GET"])
def index():
    return "OIBAS está en línea. Consultame con POST a /oibas"

# 🧠 Línea que faltaba para ejecución correcta
if __name__ == "__main__":
    app.run()
