import os
import sqlite3
from flask import Flask, render_template, request, jsonify

try:
    import psycopg2
except ImportError:
    psycopg2 = None

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url and psycopg2:
        return psycopg2.connect(database_url)
    
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'database.db')
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tabela de Presenças Confirmadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presencas (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                acompanhantes INTEGER DEFAULT 1
            )
        ''')
        
        # Tabela de Presentes Reservados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presentes_escolhidos (
                id INTEGER PRIMARY KEY,
                item TEXT NOT NULL,
                nome_convidado TEXT NOT NULL,
                whatsapp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

init_db()

# Lista Completa dos Presentes
LISTA_PRESENTES = [
    {"id": 1, "nome": "Jogo de Panelas", "categoria": "cozinha", "imagem": "/static/img/panelas.jpg", "link": "https://shopee.com.br"},
    {"id": 2, "nome": "Aparelho de Jantar", "categoria": "cozinha", "imagem": "/static/img/jantar.jpg", "link": "https://shopee.com.br"},
    {"id": 3, "nome": "Jogo de Faqueiro", "categoria": "cozinha", "imagem": "/static/img/faqueiro.jpg", "link": "https://shopee.com.br"},
    {"id": 4, "nome": "Almofadas Decorativas", "categoria": "sala", "imagem": "/static/img/almofadas.jpg", "link": "https://shopee.com.br"},
    {"id": 5, "nome": "Jogo de Cama Casal", "categoria": "quarto", "imagem": "/static/img/cama.jpg", "link": "https://shopee.com.br"},
    {"id": 6, "nome": "Jogo de Toalhas", "categoria": "banheiro", "imagem": "/static/img/toalhas.jpg", "link": "https://shopee.com.br"},
    {"id": 7, "nome": "Cesto de Roupas", "categoria": "lavanderia", "imagem": "/static/img/cesto.jpg", "link": "https://shopee.com.br"}
]

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, item, nome_convidado FROM presentes_escolhidos")
        reservados_db = cursor.fetchall()
        conn.close()
        
        # Cria um dicionário de quais itens estão reservados
        reservas = {row[0]: row[2] for row in reservados_db}
    except Exception as e:
        print(f"Erro ao buscar reservas: {e}")
        reservas = {}

    # Monta a lista completa com o status de reservado
    presentes_processados = []
    for item in LISTA_PRESENTES:
        item_copy = item.copy()
        if item['id'] in reservas:
            item_copy['reservado'] = True
            item_copy['reservado_por'] = reservas[item['id']]
        else:
            item_copy['reservado'] = False
            item_copy['reservado_por'] = ''
        presentes_processados.append(item_copy)

    return render_template('index.html', presentes=presentes_processados)

@app.route('/reservar/<int:item_id>', methods=['POST'])
def reservar_item(item_id):
    data = request.get_json()
    nome = data.get('nome')
    whatsapp = data.get('whatsapp')

    if not nome or not whatsapp:
        return jsonify({'sucesso': False, 'mensagem': 'Preencha nome e WhatsApp!'})

    item_obj = next((item for item in LISTA_PRESENTES if item['id'] == item_id), None)
    item_nome = item_obj['nome'] if item_obj else f"Item #{item_id}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        is_postgres = bool(os.environ.get('DATABASE_URL'))
        
        query = (
            "INSERT INTO presentes_escolhidos (id, item, nome_convidado, whatsapp) VALUES (%s, %s, %s, %s)"
            if is_postgres else
            "INSERT INTO presentes_escolhidos (id, item, nome_convidado, whatsapp) VALUES (?, ?, ?, ?)"
        )
        cursor.execute(query, (item_id, item_nome, nome, whatsapp))
        conn.commit()
        conn.close()
        return jsonify({'sucesso': True})
    except Exception as e:
        print(f"Erro ao reservar: {e}")
        return jsonify({'sucesso': False, 'mensagem': 'Este item já foi reservado ou ocorreu um erro!'})

@app.route('/confirmar-presenca', methods=['POST'])
def confirmar_presenca():
    data = request.get_json()
    nome = data.get('nome')
    whatsapp = data.get('whatsapp')
    acompanhantes = data.get('acompanhantes', 1)

    if not nome or not whatsapp:
        return jsonify({'sucesso': False, 'mensagem': 'Preencha nome e WhatsApp!'})

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        is_postgres = bool(os.environ.get('DATABASE_URL'))
        
        query = (
            "INSERT INTO presencas (nome, whatsapp, acompanhantes) VALUES (%s, %s, %s)"
            if is_postgres else
            "INSERT INTO presencas (nome, whatsapp, acompanhantes) VALUES (?, ?, ?)"
        )
        cursor.execute(query, (nome, whatsapp, acompanhantes))
        conn.commit()
        conn.close()
        return jsonify({'sucesso': True})
    except Exception as e:
        print(f"Erro ao confirmar presença: {e}")
        return jsonify({'sucesso': False, 'mensagem': 'Erro ao confirmar presença.'})

@app.route('/admin')
def admin():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome, whatsapp, acompanhantes FROM presencas ORDER BY id DESC")
        presencas = cursor.fetchall()
        
        try:
            cursor.execute("SELECT id, item, nome_convidado, whatsapp FROM presentes_escolhidos ORDER BY id DESC")
            presentes = cursor.fetchall()
        except Exception:
            presentes = []
            
        conn.close()
        
        total_pessoas = 0
        for p in presencas:
            try:
                acomp = int(p[3]) if p[3] is not None else 1
            except (ValueError, TypeError):
                acomp = 1
            total_pessoas += acomp
        
        return render_template('admin.html', presencas=presencas, presentes=presentes, total_pessoas=total_pessoas)
    except Exception as e:
        return f"Erro ao acessar admin: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)