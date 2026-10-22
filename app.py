import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

try:
    import psycopg2
except ImportError:
    psycopg2 = None

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

def get_db_connection():
    """Conecta ao PostgreSQL se estiver no Render, ou ao SQLite local."""
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
    """Cria as tabelas de presenças e presentes se não existirem."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Tabela de Presenças Confimadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presencas (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                acompanhantes INTEGER DEFAULT 0
            )
        ''')
        
        # Tabela de Presentes Escolhidos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presentes_escolhidos (
                id SERIAL PRIMARY KEY,
                item TEXT NOT NULL,
                nome_convidado TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirmar_presenca', methods=['POST'])
def confirmar_presenca():
    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    acompanhantes = request.form.get('acompanhantes', 0)

    if not nome or not whatsapp:
        flash('Por favor, preencha nome e WhatsApp!', 'danger')
        return redirect(url_for('index'))

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
        flash('Presença confirmada com sucesso!', 'success')
    except Exception as e:
        print(f"Erro ao salvar presença: {e}")
        flash('Erro ao confirmar presença.', 'danger')

    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Visualização das Pessoas Confirmadas e Presentes Comprados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Busca presenças
        cursor.execute("SELECT id, nome, whatsapp, acompanhantes FROM presencas ORDER BY id DESC")
        presencas = cursor.fetchall()
        
        # Busca presentes marcados/comprados
        try:
            cursor.execute("SELECT id, item, nome_convidado FROM presentes_escolhidos ORDER BY id DESC")
            presentes = cursor.fetchall()
        except Exception:
            presentes = []
            
        conn.close()
        
        # Soma total de convidados
        total_pessoas = 0
        for p in presencas:
            try:
                acomp = int(p[3]) if p[3] is not None else 0
            except (ValueError, TypeError):
                acomp = 0
            total_pessoas += 1 + acomp
        
        return render_template('admin.html', presencas=presencas, presentes=presentes, total_pessoas=total_pessoas)
    except Exception as e:
        return f"Erro ao acessar admin: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)