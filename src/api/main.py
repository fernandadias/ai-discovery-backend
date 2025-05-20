from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "AI Discovery Backend API"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/chat', methods=['POST'])
def chat():
    # Simulação de resposta para teste
    return jsonify({
        "response": "Esta é uma resposta simulada para teste do frontend.",
        "references": [
            {
                "title": "Pesquisa de Usuários",
                "snippet": "Os usuários indicaram preferência por interfaces personalizadas...",
                "filename": "pesquisa_usuarios.pdf",
                "distance": 0.23
            },
            {
                "title": "Análise de Mercado",
                "snippet": "Concorrentes têm adotado abordagens de personalização...",
                "filename": "analise_mercado.pdf",
                "distance": 0.35
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
