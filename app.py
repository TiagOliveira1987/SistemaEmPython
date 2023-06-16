import sqlite3
import datetime

print("-------------------------------------------- ")
print(" CLÍNICA DE CONSULTAS ÁGIL ")
print("-------------------------------------------- ")
print()
class Paciente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Agendamento:
    def __init__(self, paciente, dia, hora, especialidade):
        self.paciente = paciente
        self.dia = dia
        self.hora = hora
        self.especialidade = especialidade

# Função para criar a tabela de pacientes no banco de dados
def criar_tabela_pacientes():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nome TEXT NOT NULL,
                      telefone TEXT NOT NULL UNIQUE)''')
    conn.commit()
    conn.close()

# Função para adicionar um novo paciente ao banco de dados
def adicionar_paciente(nome, telefone):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO pacientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
        conn.commit()
        print("Paciente adicionado ao cadastro com sucesso!")
    except sqlite3.IntegrityError:
        print("Paciente já cadastrado!")
    conn.close()

# Função para buscar todos os pacientes cadastrados
def buscar_pacientes():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

# Função para realizar um agendamento de consulta
def marcar_consulta(paciente_id, dia, hora, especialidade):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE id=?", (paciente_id,))
    paciente = cursor.fetchone()
    if paciente is None:
        print("Paciente não encontrado.")
        conn.close()
        return

    cursor.execute("SELECT * FROM agendamentos WHERE dia=? AND hora=?", (dia, hora))
    agendamento_existente = cursor.fetchone()
    if agendamento_existente:
        print("Horário indisponível para agendamento.")
        conn.close()
        return

    data_atual = datetime.date.today()
    data_consulta = datetime.datetime.strptime(dia, "%d/%m/%Y").date()
    if data_consulta < data_atual:
        print("Não é possível agendar consultas retroativas.")
        conn.close()
        return

    cursor.execute("INSERT INTO agendamentos (paciente_id, dia, hora, especialidade) VALUES (?, ?, ?, ?)",
                   (paciente_id, dia, hora, especialidade))
    conn.commit()
    print("Consulta marcada com sucesso!")
    conn.close()

    # Função para criar a tabela de agendamentos no banco de dados
def criar_tabela_agendamentos():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS agendamentos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      paciente_id INTEGER NOT NULL,
                      dia TEXT NOT NULL,
                      hora TEXT NOT NULL,
                      especialidade TEXT NOT NULL,
                      FOREIGN KEY (paciente_id) REFERENCES pacientes (id))''')
    conn.commit()
    conn.close()

# Criar a tabela de agendamentos no banco de dados (se não existir)
criar_tabela_agendamentos()


# Função para buscar todos os agendamentos de consulta
def buscar_agendamentos():
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT agendamentos.id, pacientes.nome, agendamentos.dia, agendamentos.hora, agendamentos.especialidade FROM agendamentos INNER JOIN pacientes ON agendamentos.paciente_id=pacientes.id")
    agendamentos = cursor.fetchall()
    conn.close()
    return agendamentos

# Função para cancelar um agendamento de consulta
def cancelar_consulta(agendamento_id):
    conn = sqlite3.connect('pacientes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agendamentos WHERE id=?", (agendamento_id,))
    agendamento = cursor.fetchone()
    if agendamento is None:
        print("Agendamento não encontrado.")
        conn.close()
        return

    cursor.execute("DELETE FROM agendamentos WHERE id=?", (agendamento_id,))
    conn.commit()
    print("Consulta cancelada com sucesso!")
    conn.close()

# Criar a tabela de pacientes no banco de dados (se não existir)
criar_tabela_pacientes()

# Loop principal do programa
while True:
    print("1 - Adicionar paciente")
    print("2 - Exibir pacientes cadastrados")
    print("3 - Marcar consulta")
    print("4 - Exibir agendamentos de consulta")
    print("5 - Cancelar consulta")
    print("6 - Sair")
    opcao = input("Escolha uma opção: ")

    print("------------------------------------------")

    if opcao == "1":
        nome = input("Digite o nome do paciente: ")
        telefone = input("Digite o telefone do paciente: ")
        adicionar_paciente(nome, telefone)
        print("-------------------------------------------")

    elif opcao == "2":
        pacientes = buscar_pacientes()
        print("Pacientes cadastrados:")
        for paciente in pacientes:
            print(f"ID: {paciente[0]}, Nome: {paciente[1]}, Telefone: {paciente[2]}")
        print("-------------------------------------------")

    elif opcao == "3":
        pacientes = buscar_pacientes()
        print("Pacientes cadastrados:")
        for paciente in pacientes:
            print(f"ID: {paciente[0]}, Nome: {paciente[1]}, Telefone: {paciente[2]}")
        paciente_id = int(input("Escolha o ID do paciente para agendar a consulta: "))
        dia = input("Digite o dia da consulta (DD/MM/AAAA): ")
        hora = input("Digite a hora da consulta (HH:MM): ")
        especialidade = input("Digite a especialidade desejada para a consulta: ")
        marcar_consulta(paciente_id, dia, hora, especialidade)
        print("---------------------------------------------")

    elif opcao == "4":
        agendamentos = buscar_agendamentos()
        
        
        print("Agendamentos de consulta:")
        for agendamento in agendamentos:
            print(f"ID: {agendamento[0]}, Paciente: {agendamento[1]}, Dia: {agendamento[2]}, Hora: {agendamento[3]}, Especialidade: {agendamento[4]}")
        print("-------------------------------------------------")
    elif opcao == "5":
        agendamentos = buscar_agendamentos()
        print("Agendamentos de consulta:")
        for agendamento in agendamentos:
            print(f"ID: {agendamento[0]}, Paciente: {agendamento[1]}, Dia: {agendamento[2]}, Hora: {agendamento[3]}, Especialidade: {agendamento[4]}")
        agendamento_id = int(input("Escolha o ID do agendamento para cancelar a consulta: "))
        cancelar_consulta(agendamento_id)
    elif opcao == "6":
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida. Digite novamente.")





