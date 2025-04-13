from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
    return conn

# Rota para testar o servidor
@app.route('/')
def index():
    return "Servidor Flask está funcionando!"

# Rota para consultar o saldo de um usuário
@app.route('/saldo/<usuario>', methods=['GET'])
def consultar_saldo(usuario):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT saldo FROM usuarios WHERE nome = ?', (usuario,))
    saldo = cursor.fetchone()
    
    if saldo:
        return jsonify({"usuario": usuario, "saldo": saldo["saldo"]}), 200
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

# Rota para adicionar um pagamento
@app.route('/pagar', methods=['POST'])
def processar_pagamento():
    dados = request.get_json()
    nome_usuario = dados.get('usuario')
    valor = dados.get('valor')
    
    if not nome_usuario or not valor:
        return jsonify({"error": "Dados incompletos!"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT saldo FROM usuarios WHERE nome = ?', (nome_usuario,))
    saldo_atual = cursor.fetchone()
    
    if saldo_atual:
        novo_saldo = saldo_atual['saldo'] - valor
        if novo_saldo < 0:
            return jsonify({"error": "Saldo insuficiente"}), 400
        cursor.execute('UPDATE usuarios SET saldo = ? WHERE nome = ?', (novo_saldo, nome_usuario))
        conn.commit()
        return jsonify({"usuario": nome_usuario, "novo_saldo": novo_saldo}), 200
    else:
        return jsonify({"error": "Usuário não encontrado"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
