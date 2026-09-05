import sqlite3

# Aponta para o database.db da raiz
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# (O restante do código continua exatamente o mesmo)

# Apaga a tabela antiga para recriar do zero com a coluna de imagem
cursor.execute('DROP TABLE IF EXISTS presentes')

cursor.execute('''
    CREATE TABLE presentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        link TEXT,
        imagem TEXT,
        reservado INTEGER DEFAULT 0,
        reservado_por TEXT,
        whatsapp TEXT
    )
''')

# Lista completa com TODOS os seus itens e imagens da pasta static/img
presentes = [
    # COZINHA
    ('Cuscuizeiro', 'cozinha', 'https://shopee.com.br', '/static/img/cuscuizero.webp'),
    ('Descanso Tampas de Panela', 'cozinha', 'https://shopee.com.br', '/static/img/descanso tampas de panela.jpg'),
    ('Escorredor de Louça', 'cozinha', 'https://shopee.com.br', '/static/img/escorredor.webp'),
    ('Garrafa Térmica', 'cozinha', 'https://shopee.com.br', '/static/img/garrafa termica.webp'),
    ('Garrafas de Vidro', 'cozinha', 'https://shopee.com.br', '/static/img/garrafas de vidro.webp'),
    ('Geladeira', 'cozinha', 'https://shopee.com.br', '/static/img/geladeira.webp'),
    ('Ilha Bancada', 'cozinha', 'https://shopee.com.br', '/static/img/ilha bancada.webp'),
    ('Jogo de Copos', 'cozinha', 'https://shopee.com.br', '/static/img/jogo de copos.webp'),
    ('Jogo de Pratos', 'cozinha', 'https://shopee.com.br', '/static/img/jogo de pratos.webp'),
    ('Jogo Faqueiro', 'cozinha', 'https://shopee.com.br', '/static/img/Jogo Faqueiro.webp'),
    ('Kit de Panelas', 'cozinha', 'https://shopee.com.br', '/static/img/kit de panelas.webp'),
    ('Liquidificador', 'cozinha', 'https://shopee.com.br', '/static/img/Liquidificador.webp'),
    ('Panela de Pressão', 'cozinha', 'https://shopee.com.br', '/static/img/panela de pressao.webp'),
    ('Porta Temperos', 'cozinha', 'https://shopee.com.br', '/static/img/porta temperos.webp'),
    ('Pote Dispenser', 'cozinha', 'https://shopee.com.br', '/static/img/pote dispenser.webp'),
    ('Potes de Vidro', 'cozinha', 'https://shopee.com.br', '/static/img/potes de vidro.webp'),
    ('Potes Organizadores', 'cozinha', 'https://shopee.com.br', '/static/img/potes.webp'),
    ('Sanduicheira', 'cozinha', 'https://shopee.com.br', '/static/img/sanduicheira.webp'),
    ('Tábua de Churrasco', 'cozinha', 'https://shopee.com.br', '/static/img/tabua de chorrasco.webp'),
    ('Taça de Sobremesa', 'cozinha', 'https://shopee.com.br', '/static/img/taca sobremesa.webp'),
    ('Triturador de Alho', 'cozinha', 'https://shopee.com.br', '/static/img/triturador de alho.webp'),

    # SALA
    ('Cortina', 'sala', 'https://shopee.com.br', '/static/img/cortina.webp'),
    ('Painel Sala', 'sala', 'https://shopee.com.br', '/static/img/painel sala.webp'),
    ('Suporte Controle', 'sala', 'https://shopee.com.br', '/static/img/suporte controle.webp'),
    ('Tapete Sala', 'sala', 'https://shopee.com.br', '/static/img/tapete sala.webp'),

    # QUARTO
    ('Edredom', 'quarto', 'https://shopee.com.br', '/static/img/edredom.webp'),
    ('Guarda Roupas', 'quarto', 'https://shopee.com.br', '/static/img/guarda roupas.webp'),
    ('Jogos de Lençóis', 'quarto', 'https://shopee.com.br', '/static/img/jogos de lencois.webp'),
    ('Sapateira', 'quarto', 'https://shopee.com.br', '/static/img/sapateira.webp'),

    # BANHEIRO
    ('Gabinete Armário Banheiro', 'banheiro', 'https://shopee.com.br', '/static/img/gabinete armario banheiro.webp'),
    ('Jogo de Toalhas', 'banheiro', 'https://shopee.com.br', '/static/img/jogo de toalhas.webp'),
    ('Kit Banheiro', 'banheiro', 'https://shopee.com.br', '/static/img/kit banheiro.webp'),
    ('Tapete para Banheiro', 'banheiro', 'https://shopee.com.br', '/static/img/tapete para banheiro.webp'),

    # LAVANDERIA / ORGANIZAÇÃO
    ('Kit Organizador', 'lavanderia', 'https://shopee.com.br', '/static/img/kit organizador.webp'),
    ('Varal de Chão', 'lavanderia', 'https://shopee.com.br', '/static/img/varal de chao.webp'),
    ('Vassoura Mágica', 'lavanderia', 'https://shopee.com.br', '/static/img/vassoura magica.webp'),
]

for nome, categoria, link, imagem in presentes:
    cursor.execute('''
        INSERT INTO presentes (nome, categoria, link, imagem)
        VALUES (?, ?, ?, ?)
    ''', (nome, categoria, link, imagem))

conn.commit()
conn.close()
print("✅ Banco de dados atualizado com TODAS as imagens!")