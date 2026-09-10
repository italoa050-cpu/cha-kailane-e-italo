from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    # Configura para acessar as colunas pelo nome (ex: p['imagem'], p['nome'])
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    # Garante acesso via chave no Jinja2 (p.imagem / p['imagem'])
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM presentes')
    presentes = cursor.fetchall()
    conn.close()
    return render_template('index.html', presentes=presentes)

@app.route('/reservar/<int:item_id>', methods=['POST'])
def reservar(item_id):
    dados = request.get_json()
    nome = dados.get('nome')
    whatsapp = dados.get('whatsapp')

    if not nome or not whatsapp:
        return jsonify({'sucesso': False, 'mensagem': 'Por favor, preencha nome e WhatsApp.'})

    conn = get_db()
    cursor = conn.cursor()
    
    # Verifica se o item já não foi reservado por outra pessoa
    cursor.execute('SELECT reservado FROM presentes WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if item and item['reservado'] == 1:
        conn.close()
        return jsonify({'sucesso': False, 'mensagem': 'Este item já foi reservado por outra pessoa!'})

    # Atualiza o status para reservado
    cursor.execute('''
        UPDATE presentes 
        SET reservado = 1, reservado_por = ?, whatsapp = ? 
        WHERE id = ?
    ''', (nome, whatsapp, item_id))
    
    conn.commit()
    conn.close()
    return jsonify({'sucesso': True})

@app.route('/confirmar-presenca', methods=['POST'])
def confirmar_presenca():
    dados = request.get_json()
    nome = dados.get('nome')
    acompanhantes = dados.get('acompanhantes')
    whatsapp = dados.get('whatsapp')

    if not nome or not whatsapp:
        return jsonify({'sucesso': False, 'mensagem': 'Preencha os campos obrigatórios.'})

    # Aqui você pode salvar numa tabela de RSVP se tiver, ou apenas confirmar o sucesso
    return jsonify({'sucesso': True})

@app.route('/admin')
def admin():
    conn = sqlite3.connect('database.db') # ou o nome correto do seu arquivo .db
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, whatsapp, acompanhantes FROM presencas ORDER BY id DESC")
    presencas = cursor.fetchall()
    conn.close()
    
    # Calcula o total de pessoas (convidado + acompanhantes)
    total_pessoas = sum(1 + (p[3] if p[3] else 0) for p in presencas)
    
    return render_template('admin.html', presencas=presencas, total_pessoas=total_pessoas)

if __name__ == '__main__':
    app.run(debug=True)