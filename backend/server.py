from flask import Flask, request, jsonify
from flask_cors import CORS
import cohere

app = Flask(__name__)
CORS(app)  # Esto permite que tu React app se comunique con el servidor

# Inicializa el cliente de Cohere con tu API key
co = cohere.ClientV2("O7Cjn2pyi02rLIJE9azktO8hRehHboQjeA1HM9fQ")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    # Llama a la API de Cohere
    response = co.chat(
        model="command-r-plus",
        messages=[{"role": "user", "content": user_message}]
    )
    
    return jsonify({
        "message": response.message.content[0].text
    })

if __name__ == '__main__':
    app.run(port=5000)