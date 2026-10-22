import os
import sqlite3

try:
    import psycopg2
except ImportError:
    psycopg2 = None

def migrar_dados():
    database_url = os.environ.get('DATABASE_URL')
    if not database_url or not psycopg2:
        print("DATABASE_URL não configurada ou psycopg2 não instalado localmente.")
        print("Para enviar os dados ao Render, rode este script através do servidor/terminal ou adicione a DATABASE_URL.")
        return

    # Caminho do banco local
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

    if not os.path.exists(db_path):
        print("Banco de dados SQLite local não encontrado.")
        return

    # Conectar ao SQLite local
    conn_local = sqlite3.connect(db_path)
    cursor_local = conn_local.cursor()

    # Conectar ao PostgreSQL do Render
    conn_remote = psycopg2.connect(database_url)
    cursor_remote = conn_remote.cursor()

    # 1. Migrar Presenças
    try:
        cursor_local.execute("SELECT nome, whatsapp, acompanhantes FROM presencas")
        presencas = cursor_local.fetchall()
        for p in presencas:
            cursor_remote.execute(
                "INSERT INTO presencas (nome, whatsapp, acompanhantes) VALUES (%s, %s, %s)",
                (p[0], p[1], p[2])
            )
        print(f"Migradas {len(presencas)} presenças.")
    except Exception as e:
        print(f"Erro ao migrar presenças: {e}")

    # 2. Migrar Presentes Escolhidos
    try:
        # Verifica a tabela de presentes no SQLite
        cursor_local.execute("SELECT id, item, nome_convidado, whatsapp FROM presentes_escolhidos")
        presentes = cursor_local.fetchall()
        for pr in presentes:
            cursor_remote.execute(
                "INSERT INTO presentes_escolhidos (id, item, nome_convidado, whatsapp) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                (pr[0], pr[1], pr[2], pr[3])
            )
        print(f"Migrados {len(presentes)} presentes.")
    except Exception as e:
        print(f"Erro ao migrar presentes: {e}")

    conn_remote.commit()
    conn_local.close()
    conn_remote.close()
    print("Migração concluída com sucesso!")

if __name__ == '__main__':
    migrar_dados()