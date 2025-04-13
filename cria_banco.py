import sqlite3

# Conectando ao banco de dados (cria o arquivo banco.db se não existir)
conn = sqlite3.connect('banco.db')

# Criando a tabela "usuarios"
conn.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    nome TEXT PRIMARY KEY,
                    saldo REAL)''')

# Inserindo alguns dados iniciais para teste
conn.execute("INSERT OR IGNORE INTO usuarios (nome, saldo) VALUES ('user1', 100.000.0)")
conn.execute("INSERT OR IGNORE INTO usuarios (nome, saldo) VALUES ('user2', 50.000.0)")

# Salvando as alterações e fechando a conexão
conn.commit()
conn.close()

print("Banco de dados e tabela criados com sucesso!")
