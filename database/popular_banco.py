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
    ('Cuscuizeiro', 'cozinha', 'https://shopee.com.br/Cuscuzeiro-Crema-16cm-i.210928301.18293019283', '/static/img/cuscuizero.webp'),
    ('Descanso Tampas de Panela', 'cozinha', 'https://shopee.com.br/Descanso-de-Panela-Suporte-Porta-Tempero-i.1107305320.23294138680', '/static/img/descanso tampas de panela.jpg'),
    ('Escorredor de Louça', 'cozinha', 'https://shopee.com.br/Escorredor-de-Louca-Duplo-i.291029381.17203918273', '/static/img/escorredor.webp'),
    ('Garrafa Térmica', 'cozinha', 'https://shopee.com.br/Garrafa-Termica-Nordica-1L-i.410293812.21203918273', '/static/img/garrafa termica.webp'),
    ('Garrafas de Vidro', 'cozinha', 'https://shopee.com.br/2-Garrafas-de-Vidro-1L-i.381920391.18203918273', '/static/img/garrafas de vidro.webp'),
    ('Geladeira', 'cozinha', 'https://shopee.com.br', '/static/img/geladeira.webp'),
    ('Ilha Bancada', 'cozinha', 'https://shopee.com.br', '/static/img/ilha bancada.webp'),
    ('Jogo de Copos', 'cozinha', 'https://shopee.com.br/Jogo-6-Copos-Aruba-Fume-i.281920391.21102938129', '/static/img/jogo de copos.webp'),
    ('Jogo de Pratos', 'cozinha', 'https://shopee.com.br/Kit-6-Pratos-Rasos-Porcelana-i.391029381.16102938129', '/static/img/jogo de pratos.webp'),
    ('Jogo Faqueiro', 'cozinha', 'https://shopee.com.br/Kit-6-Pecas-Facas-Profissional-i.410293812.20102938129', '/static/img/Jogo Faqueiro.webp'),
    ('Kit de Panelas', 'cozinha', 'https://shopee.com.br/Jogo-de-Panelas-Antiaderente-i.401928301.23102938129', '/static/img/kit de panelas.webp'),
    ('Liquidificador', 'cozinha', 'https://shopee.com.br/Liquidificador-Mondial-Turbo-Power-i.391029381.18102938129', '/static/img/Liquidificador.webp'),
    ('Panela de Pressão', 'cozinha', 'https://shopee.com.br/Panela-de-Pressao-4,5L-Ceramica-i.310293812.23102938129', '/static/img/panela de pressao.webp'),
    ('Porta Temperos', 'cozinha', 'https://shopee.com.br/Porta-Temperos-Industrial-5-Pecas-i.482019283.21102938129', '/static/img/porta temperos.webp'),
    ('Pote Dispenser', 'cozinha', 'https://shopee.com.br/Pote-Dispenser-Multiuso-1200ml-i.501928301.22019283019', '/static/img/pote dispenser.webp'),
    ('Potes de Vidro', 'cozinha', 'https://shopee.com.br/Kit-3-Potes-de-Vidro-Hermetico-i.410293812.17102938129', '/static/img/potes de vidro.webp'),
    ('Potes Organizadores', 'cozinha', 'https://shopee.com.br/Kit-15-Potes-Variados-i.381920391.22102938129', '/static/img/potes.webp'),
    ('Sanduicheira', 'cozinha', 'https://shopee.com.br/Sanduicheira-Britania-Antiaderente-i.310293812.20192830192', '/static/img/sanduicheira.webp'),
    ('Tábua de Churrasco', 'cozinha', 'https://shopee.com.br/Tabua-de-Churrasco-Grande-i.381920391.17102938129', '/static/img/tabua de chorrasco.webp'),
    ('Taça de Sobremesa', 'cozinha', 'https://shopee.com.br/Taca-de-Sobremesa-Kit-6-Tacas-i.482019283.23019283019', '/static/img/taca sobremesa.webp'),
    ('Triturador de Alho', 'cozinha', 'https://shopee.com.br', '/static/img/triturador de alho.webp'),

    # SALA
    ('Cortina', 'sala', 'https://shopee.com.br/Cortina-Luxo-Para-Sala-4,00m-x-2,60m-i.382029141.22923984102', '/static/img/cortina.webp'),
    ('Painel Sala', 'sala', 'https://shopee.com.br/Painel-Sala-de-Estar-Para-TV-ate-50-i.403819201.21938201923', '/static/img/painel sala.webp'),
    ('Suporte Controle', 'sala', 'https://shopee.com.br/Suporte-Organizador-Porta-Controle-Remoto-i.281920391.14920391823', '/static/img/suporte controle.webp'),
    ('Tapete Sala', 'sala', 'https://shopee.com.br/Tapete-Sala-2,00-x-1,50-i.310293812.16729301928', '/static/img/tapete sala.webp'),

    # QUARTO
    ('Edredom', 'quarto', 'https://shopee.com.br/Edredom-Casal-Queen-Dupla-Face-i.482019283.16102938129', '/static/img/edredom.webp'),
    ('Guarda Roupas', 'quarto', 'https://shopee.com.br', '/static/img/guarda roupas.webp'),
    ('Jogos de Lençóis', 'quarto', 'https://shopee.com.br/Jogo-de-Lencol-Aconchegante-i.291029381.19102938129', '/static/img/jogos de lencois.webp'),
    ('Sapateira', 'quarto', 'https://shopee.com.br/Sapateira-Buenos-Aires-3-Portas-i.293810293.15920391827', '/static/img/sapateira.webp'),

    # BANHEIRO
    ('Gabinete Armário Banheiro', 'banheiro', 'https://shopee.com.br', '/static/img/gabinete armario banheiro.webp'),
    ('Jogo de Toalhas', 'banheiro', 'https://shopee.com.br/Jogo-de-Toalha-2-Banho-e-2-Rosto-i.281920391.18102938129', '/static/img/jogo de toalhas.webp'),
    ('Kit Banheiro', 'banheiro', 'https://shopee.com.br/Kit-Banheiro-4-Pecas-Luxo-i.401928301.15102938129', '/static/img/kit banheiro.webp'),
    ('Tapete para Banheiro', 'banheiro', 'https://shopee.com.br/Tapete-para-Banheiro-Kit-3-Pecas-i.291829301.19830291823', '/static/img/tapete para banheiro.webp'),

    # LAVANDERIA / ORGANIZAÇÃO
    ('Kit Organizador', 'lavanderia', 'https://shopee.com.br/Kit-Organizadores-Hermeticos-Acrilico-i.501928301.22102938129', '/static/img/kit organizador.webp'),
    ('Varal de Chão', 'lavanderia', 'https://shopee.com.br/Varal-de-Chao-3-Andares-Dobravel-i.332019482.15820491823', '/static/img/varal de chao.webp'),
    ('Vassoura Mágica', 'lavanderia', 'https://shopee.com.br/Vassoura-Magica-Rodo-Multifuncional-i.293810293.20102938129', '/static/img/vassoura magica.webp'),
]

for nome, categoria, link, imagem in presentes:
    cursor.execute('''
        INSERT INTO presentes (nome, categoria, link, imagem)
        VALUES (?, ?, ?, ?)
    ''', (nome, categoria, link, imagem))

conn.commit()
conn.close()
print("✅ Banco de dados atualizado com TODAS as imagens!")