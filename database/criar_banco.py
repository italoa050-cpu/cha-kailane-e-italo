import sqlite3

conexao = sqlite3.connect("database.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS presentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    imagem TEXT,
    link TEXT,
    reservado INTEGER DEFAULT 0,
    reservado_por TEXT,
    whatsapp TEXT
)
""")

conexao.commit()
conexao.close()
print("Banco de dados configurado com sucesso!")