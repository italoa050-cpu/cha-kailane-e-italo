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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presencas (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                acompanhantes INTEGER DEFAULT 1
            )
        ''')
        
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

# Lista Completa dos Presentes por Categoria
LISTA_PRESENTES = []
    # COZINHA
    # Lista Completa dos Presentes ajustada para a sua pasta static/img/
LISTA_PRESENTES = [
    # COZINHA
    {"id": 1, "nome": "Cuscuizeiro", "categoria": "cozinha", "imagem": "/static/img/cuscuizero.webp", "link": "https://shopee.com.br/Cuscuzeiro-Crema-16cm-i.210928301.18293019283"},
    {"id": 2, "nome": "Descanso Tampas de Panela", "categoria": "cozinha", "imagem": "/static/img/descanso%20tampas%20de%20panela.jpg", "link": "https://shopee.com.br/Descanso-De-Panela-Suporte-Tampas-De-Panelas-Talheres-E-Acess%C3%B3rios-Organizador-Porta-Tempero-Cozinha-i.1131571856.23198681301"},
    {"id": 3, "nome": "Escorredor de Louça", "categoria": "cozinha", "imagem": "/static/img/escorredor.webp", "link": "https://shopee.com.br/Escorredor-de-Lou%C3%A7a-Duplo-Multifuncional-Suporte-para-Pratos-Talheres-e-T%C3%A1bua-de-Corte-i.1601750095.23794415375"},
    {"id": 4, "nome": "Garrafa Térmica", "categoria": "cozinha", "imagem": "/static/img/garrafa%20termica.webp", "link": "https://shopee.com.br/Garrafa-T%C3%A1rmica-N%C3%B3rdica-1-Litro-Caf%C3%A9-Ch%C3%A1-Bule-Cabo-Madeira-Mesa-Posta-Bot%C3%A3o-Fixa-Temperatura-Wood-1L-i.625510592.22493251687"},
    {"id": 5, "nome": "Garrafas de Vidro", "categoria": "cozinha", "imagem": "/static/img/garrafas%20de%20vidro.webp", "link": "https://shopee.com.br/search?keyword=2%20garrafas%20de%20vidro%201L"},
    {"id": 6, "nome": "Geladeira", "categoria": "cozinha", "imagem": "/static/img/geladeira.webp", "link": "https://shopee.com.br/search?keyword=geladeira"},
    {"id": 7, "nome": "Ilha Bancada", "categoria": "cozinha", "imagem": "/static/img/ilha%20bancada.webp", "link": "https://shopee.com.br/search?keyword=ilha%20bancada%20cozinha"},
    {"id": 8, "nome": "Jogo de Copos", "categoria": "cozinha", "imagem": "/static/img/jogo%20de%20copos.webp", "link": "https://shopee.com.br/Jogo-6-Copos-Luxo-Suco-Agua-Refrigerante-Aruba-Fum%C3%AA-465ml-i.618718566.22698032343"},
    {"id": 9, "nome": "Jogo de Pratos", "categoria": "cozinha", "imagem": "/static/img/jogo%20de%20pratos.webp", "link": "https://shopee.com.br/Kit-6-Pratos-Rasos-de-Porcelana-Branca-26-5cm-Germer-Mesa-Posta-Diamante-i.1284860786.18299590094"},
    {"id": 10, "nome": "Jogo Faqueiro", "categoria": "cozinha", "imagem": "/static/img/Jogo%20Faqueiro.webp", "link": "https://shopee.com.br/search?keyword=jogo%20faqueiro%2025%20pecas%20nude"},
    {"id": 11, "nome": "Kit de Panelas", "categoria": "cozinha", "imagem": "/static/img/kit%20de%20panelas.webp", "link": "https://shopee.com.br/Jogo-de-Panelas-Antiaderente-13-Pe%C3%A7as-Preto-com-Teflon-Tampa-de-Vidro-com-Op%C3%A7%C3%B5es-cor-Vermelho-Preto-i.1669534330.58200516233"},
    {"id": 12, "nome": "Liquidificador", "categoria": "cozinha", "imagem": "/static/img/Liquidificador.webp", "link": "https://shopee.com.br/Liquidificador-Mondial-Turbo-Power-L-99-3-Velocidades-550W-220V-i.1078343995.22297014624"},
    {"id": 13, "nome": "Panela de Pressão", "categoria": "cozinha", "imagem": "/static/img/panela%20de%20pressao.webp", "link": "https://shopee.com.br/Panela-de-Press%C3%A3o-4-5L-Cer%C3%A2mica-Moderna-Fog%C3%A3o-Indu%C3%A7%C3%A3o-Antiaderente-Fechamento-Externo-i.958447403.44760160595"},
    {"id": 14, "nome": "Porta Temperos", "categoria": "cozinha", "imagem": "/static/img/porta%20temperos.webp", "link": "https://shopee.com.br/search?keyword=porta%20temperos%205%20pecas"},
    {"id": 15, "nome": "Pote Dispenser", "categoria": "cozinha", "imagem": "/static/img/pote%20dispenser.webp", "link": "https://shopee.com.br/Pote-Dispenser-Multiuso-1200ml-sabao-em-po-liquido-plastico-i.369179570.22998781654"},
    {"id": 16, "nome": "Potes de Vidro", "categoria": "cozinha", "imagem": "/static/img/potes%20de%20vidro.webp", "link": "https://shopee.com.br/Kit-3-Potes-de-Vidro-Herm%C3%A9tico-com-Trava-Metal-750ml-1-33L-1-78L-i.384207446.53055642480"},
    {"id": 17, "nome": "Potes Organizadores", "categoria": "cozinha", "imagem": "/static/img/potes%20organizadores.webp", "link": "https://shopee.com.br/Kit-Organizadores-Potes-Herm%C3%A9ticos-Acr%C3%ADlico-Livre-BPA-Para-Mantimentos-Cozinha-Geladeira-Arm%C3%A1rio-i.577692913.23096097453"},
    {"id": 18, "nome": "Sanduicheira", "categoria": "cozinha", "imagem": "/static/img/sanduicheira.webp", "link": "https://shopee.com.br/search?keyword=sanduicheira%20britania%20antiaderente"},
    {"id": 19, "nome": "Tábua de Churrasco", "categoria": "cozinha", "imagem": "/static/img/tabua%20de%20churrasco.webp", "link": "https://shopee.com.br/Tabua-de-Carne-Churrasco-Grande-i.225023451.23591170856"},
    {"id": 20, "nome": "Taça de Sobremesa", "categoria": "cozinha", "imagem": "/static/img/taca%20de%20sobremesa.webp", "link": "https://shopee.com.br/Ta%C3%A7a-de-Sobremesa-Vidro-Canelado-Coupe-Kit-6-Ta%C3%A7as-para-Sorvete-Mousse-Pav%C3%AA-Cheesecake-i.1360529796.58256634767"},
    {"id": 21, "nome": "Triturador de Alho", "categoria": "cozinha", "imagem": "/static/img/triturador%20de%20alho.webp", "link": "https://shopee.com.br/search?keyword=triturador%20de%20alho"},

    # SALA
    {"id": 22, "nome": "Cortina", "categoria": "sala", "imagem": "/static/img/cortina.webp", "link": "https://shopee.com.br/Cortina-Luxo-Para-Sala-4-00m-X-2-60m-em-Voil-com-Forro-de-Microfibra-Para-Var%C3%A3o-Simples-Decorativa-i.380127357.8069947197"},
    {"id": 23, "nome": "Painel Sala", "categoria": "sala", "imagem": "/static/img/painel%20sala.webp", "link": "https://shopee.com.br/search?keyword=painel%20sala%20tv%2050"},
    {"id": 24, "nome": "Suporte Controle", "categoria": "sala", "imagem": "/static/img/suporte%20controle.webp", "link": "https://shopee.com.br/Suporte-Para-Controle-Remoto-Transparente-acrilico-i.456992476.23893571893"},
    {"id": 25, "nome": "Tapete Sala", "categoria": "sala", "imagem": "/static/img/tapete%20sala.webp", "link": "https://shopee.com.br/Tapete-Sala-2-00-x-1-50-F%C3%A1cil-de-limpar-i.296363855.7097861670"},

    # QUARTO
    {"id": 26, "nome": "Edredom", "categoria": "quarto", "imagem": "/static/img/edredom.webp", "link": "https://shopee.com.br/Edredom-Casal-Queen-400-Fios-Dupla-Face-2-40x2-20-Tecido-Liso-Varias-Cores-i.410424657.28564207442"},
    {"id": 27, "nome": "Guarda Roupas", "categoria": "quarto", "imagem": "/static/img/guarda%20roupas.webp", "link": "https://shopee.com.br/search?keyword=guarda%20roupas"},
    {"id": 28, "nome": "Jogos de Lençóis", "categoria": "quarto", "imagem": "/static/img/jogos%20de%20lencois.webp", "link": "https://shopee.com.br/Jogo-de-lencol-Casal-Padr%C3%A3o-Box-400-fios-Macio-i.313660590.20498131325"},
    {"id": 29, "nome": "Sapateira", "categoria": "quarto", "imagem": "/static/img/sapateira.webp", "link": "https://shopee.com.br/search?keyword=sapateira%20buenos%20aires%203%20portas"},

    # BANHEIRO
    {"id": 30, "nome": "Gabinete Armário Banheiro", "categoria": "banheiro", "imagem": "/static/img/gabinete%20armario%20banheiro.webp", "link": "https://shopee.com.br/search?keyword=gabinete%20armario%20banheiro"},
    {"id": 31, "nome": "Jogo de Toalhas", "categoria": "banheiro", "imagem": "/static/img/jogo%20de%20toalhas.webp", "link": "https://shopee.com.br/Jogo-de-Toalha-4-Pe%C3%A7as-Karsten-100-Algod%C3%A3o-2-Banho-2-Rosto-Excelente-Absor%C3%A7%C3%A3o-Felpuda-Macia-i.322387387.58200167629"},
    {"id": 32, "nome": "Kit Banheiro", "categoria": "banheiro", "imagem": "/static/img/kit%20banheiro.webp", "link": "https://shopee.com.br/Kit-Banheiro-4-Pecas-Luxo-Aco-Inox-Quadrado-Preto-Fosco-i.733802613.22692673303"},
    {"id": 33, "nome": "Tapete para Banheiro", "categoria": "banheiro", "imagem": "/static/img/tapete%20para%20banheiro.webp", "link": "https://shopee.com.br/Jogo-de-Tapete-Para-Banheiro-Kit-com-3-Pe%C3%A7as-Antiderrapante-Emborrachado-Resistente-i.1408279146.23593597115"},

    # LAVANDERIA
    {"id": 34, "nome": "Kit Organizador", "categoria": "lavanderia", "imagem": "/static/img/kit%20organizador.webp", "link": "https://shopee.com.br/Kit-Organizadores-Potes-Herm%C3%A9ticos-Acr%C3%ADlico-Livre-BPA-Para-Mantimentos-Cozinha-Geladeira-Arm%C3%A1rio-i.577692913.23096097453"},
    {"id": 35, "nome": "Varal de Chão", "categoria": "lavanderia", "imagem": "/static/img/varal%20de%20chao.webp", "link": "https://shopee.com.br/Varal-de-Ch%C3%A3o-3-Andares-Dobr%C3%A1vel-com-Rodinhas-i.1489462783.23799133359"},
    {"id": 36, "nome": "Vassoura Mágica", "categoria": "lavanderia", "imagem": "/static/img/vassoura%20magica.webp", "link": "https://shopee.com.br/Vassoura-Magica-Rodo-MOP-2-em-1-Vassoura-Rodo-M%C3%A1gico-Multifuncional-i.329256756.18036405157"}
]
@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, item, nome_convidado FROM presentes_escolhidos")
        reservados_db = cursor.fetchall()
        conn.close()
        
        reservas = {row[0]: row[2] for row in reservados_db}
    except Exception as e:
        print(f"Erro ao buscar reservas: {e}")
        reservas = {}

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