# README - EQUILIBRA: Sistema de Gestão Híbrida

O **Equilibra** é um sistema desktop desenvolvido em Python utilizando a biblioteca `PyQt5`, focado na gestão de tarefas e utilizadores em ambientes de trabalho híbrido.

## 📋 Pré-requisitos

* **Python 3.x**: Certifique-se de que o Python está instalado no sistema e acessível via terminal do VS Code.
* **Base de Dados Oracle**: O sistema requer acesso a uma base de dados Oracle ativa para persistência dos dados.
* **Conexão à Internet**: Necessária para a funcionalidade "Dica do Dia", que consulta APIs externas.

## 🚀 Instalação e Configuração no VS Code

Siga estes passos utilizando o terminal integrado do Visual Studio Code:

1.  **Abrir o Projeto**:
    Abra a pasta do projeto `Equilibra_projeto_gs` no Visual Studio Code.

2.  **Abrir o Terminal Integrado**:
    No menu superior, clique em `Terminal` -> `New Terminal` (ou use o atalho `Ctrl + '`).

3.  **Instalar Dependências**:
    Execute o seguinte comando para instalar as bibliotecas necessárias (`PyQt5`, `oracledb`, `requests`) no seu ambiente Python atual:

    ```
    python -m pip install -r requirements.txt
    ```
   

## ⚙️ Configuração da Base de Dados

Antes de executar a aplicação, se achar necessário, pode criar as próprias tabelas e configurar a conexão.

1.  **Criar Tabelas**:
    Utilize a sua ferramenta de base de dados (como SQL Developer ou a extensão Oracle no VS Code) para executar o script `script_banco.sql`. Isto criará:
    * Tabela `USUARIOS`.
    * Tabela `TAREFAS`.

2.  **Configurar Credenciais**:
    No VS Code, abra o ficheiro `database.py` e edite a função `conectar_banco` com as suas credenciais reais (utilizador, palavra-passe e host):
    
    ```python
    # Linha 6 em database.py
    conn = oracledb.connect(
        user="SEU_UTILIZADOR",
        password="SUA_PASSWORD",
        host="SEU_HOST",
        # ...
    )
    ```

## ▶️ Como Executar

Com o ambiente configurado, inicie o `main.py` normalmente através do VS Code, ou através do terminal do mesmo:

```
python main.py
```
