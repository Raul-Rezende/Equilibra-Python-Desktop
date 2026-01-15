import json
import os
from database import conectar_banco

def exportar_json(dados, nome_arquivo):#Exportar dados para arquivo JSON
    os.makedirs("data/resultados", exist_ok=True)
    filepath = f"data/resultados/{nome_arquivo}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    return filepath

def get_dados_quantidade_tarefas():# Exportar Quantidade de tarefas concluidas(p/ usuario)
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT U.NOME, COUNT(T.ID_TAREFA) AS TOTAL
            FROM USUARIOS U
            JOIN TAREFAS T ON U.ID_USUARIO = T.ID_USUARIO
            WHERE T.STATUS = 'Concluída'
            GROUP BY U.NOME
        """)
        dados = [{"nome": n, "total_tarefas": int(t)} for n, t in cursor]
        path = exportar_json(dados, "num_tarefas_concluidas")
        return dados, path
    finally:
        conn.close()

def get_dados_tarefas_concluidas_usuario():# Exportar quais tarefas foram concluídas(p/ usuario)
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT U.NOME, T.TITULO
            FROM USUARIOS U
            JOIN TAREFAS T ON U.ID_USUARIO = T.ID_USUARIO
            WHERE T.STATUS = 'Concluída'
            ORDER BY U.NOME, T.TITULO
        """)
        dados = []
        for nome_usuario, titulo_tarefa in cursor:
            dados.append({"usuario": nome_usuario, "tarefa_concluida": titulo_tarefa})
        path = exportar_json(dados, "tarefas_concluidas_usuario")
        return dados, path
    finally:
        conn.close()

def get_dados_tempo_medio():# Exportar tempo medio(em dias) do usuario para concluir as tarefas
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT U.NOME, AVG(T.DATA_CONCLUSAO - T.DATA_CRIACAO) AS MEDIA_DIAS
            FROM USUARIOS U
            JOIN TAREFAS T ON U.ID_USUARIO = T.ID_USUARIO
            WHERE T.STATUS = 'Concluída' AND T.DATA_CONCLUSAO IS NOT NULL
            GROUP BY U.NOME
            ORDER BY U.NOME
        """)
        dados = []
        for nome_usuario, media_dias in cursor:
            media_formatada = round(float(media_dias or 0), 2)
            dados.append({"usuario": nome_usuario, "media_de_dias": media_formatada})
        path = exportar_json(dados, "tempo_medio_conclusao")
        return dados, path
    finally:
        conn.close()

def get_dados_percentual():# Exportar porcentagem de conclusões do usuario(p/ tipo de tarefa) 
    conn = conectar_banco()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT U.NOME, T.TIPO, COUNT(T.ID_TAREFA)
            FROM USUARIOS U
            JOIN TAREFAS T ON U.ID_USUARIO = T.ID_USUARIO
            GROUP BY U.NOME, T.TIPO
            ORDER BY U.NOME, T.TIPO
        """)
        usuarios_dados = {}
        for nome_usuario, tipo, quantidade in cursor:
            if nome_usuario not in usuarios_dados:
                usuarios_dados[nome_usuario] = {
                    "usuario": nome_usuario,
                    "tipos_tarefa": []
                }
            usuarios_dados[nome_usuario]["tipos_tarefa"].append({
                "tipo": tipo,
                "quantidade": int(quantidade)
            })
        dados = list(usuarios_dados.values())
        path = exportar_json(dados, "percentual_tarefas")
        return dados, path
    finally:
        conn.close()