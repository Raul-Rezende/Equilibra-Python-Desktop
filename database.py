import oracledb

###===========================================###
###          CONEXÃO DO BANCO DE DADOS        ###
###===========================================###
def conectar_banco():# Conectar com o banco de dados(SQL Oracle)
    """ Estabelece conexão com o Oracle """
    try:
        conn = oracledb.connect(
            user="rm564002",
            password="190905", 
            host="oracle.fiap.com.br",
            port=1521,
            service_name="orcl"
        )
        return conn
    except oracledb.Error as e:
        raise Exception(f"Erro de conexão: {e}")

###===========================================###
###           FUNÇÕES DE USUÁRIO              ###
###===========================================###
def criar_usuario_db(nome, email, tipo_trabalho):# Inserir um novo usuario ao banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO USUARIOS (NOME, EMAIL, TIPO_TRABALHO) VALUES (:1, :2, :3)"
        cursor.execute(sql, (nome, email, tipo_trabalho))
        conn.commit()
    finally:
        conn.close()

def listar_usuarios_db():# Buscar usuarios no banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ID_USUARIO, NOME, EMAIL, TIPO_TRABALHO FROM USUARIOS ORDER BY NOME")
        return cursor.fetchall()
    finally:
        conn.close()

def deletar_usuario_db(id_usuario):# Deletar usuario, pelo id, do banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM USUARIOS WHERE ID_USUARIO = :1", [id_usuario])
        conn.commit()
    finally:
        conn.close()

###===========================================###
###           FUNÇÕES DE TAREFA               ###
###===========================================###
def criar_tarefa_db(id_usuario, titulo, descricao, tipo):# Inserir uma nova tarefa no banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO TAREFAS (ID_USUARIO, TITULO, DESCRICAO, TIPO) VALUES (:1, :2, :3, :4)"
        cursor.execute(sql, (id_usuario, titulo, descricao, tipo))
        conn.commit()
    finally:
        conn.close()

def listar_tarefas_db():# Buscar tarefas no banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        sql = '''SELECT T.ID_TAREFA, U.NOME, T.TITULO, T.STATUS, T.TIPO, T.DESCRICAO 
                 FROM TAREFAS T
                 JOIN USUARIOS U ON T.ID_USUARIO = U.ID_USUARIO
                 ORDER BY T.ID_TAREFA'''
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()

def atualizar_status_tarefa_db(id_tarefa, novo_status):# Mudar o status da tarefa(Concluida/Pendente) no banco de dados
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE TAREFAS SET STATUS = :1, DATA_CONCLUSAO = CASE WHEN :1 = 'Concluída' THEN SYSDATE ELSE NULL END WHERE ID_TAREFA = :2",
            (novo_status, novo_status, id_tarefa)
        )
        conn.commit()
    finally:
        conn.close()

def deletar_tarefa_db(id_tarefa):# Deletar tarefa, pelo id, do banco de dadso
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TAREFAS WHERE ID_TAREFA = :1", [id_tarefa])
        conn.commit()
    finally:
        conn.close()