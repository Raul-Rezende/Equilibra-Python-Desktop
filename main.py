import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QDialog, QFormLayout, QFrame, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPixmap, QFontDatabase, QIcon
import os
import database as db
import consultas as cons
import api_integra as api

###======================###
### Funções e Interfaces ###
###======================###
class MainWindow(QMainWindow):
    def __init__(self):# Inicializa a janela principal e configura a interface.
        super().__init__()
        self.setWindowTitle("EQUILIBRA - Sistema de Gestão Híbrida")
        self.setGeometry(100, 100, 1100, 720)
        self.setWindowIcon(QIcon("data/assets/logo.png"))

        # Aplica estilos
        self.setStyleSheet(self.load_styles())

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_widget = QWidget()
        header_widget.setObjectName("Header")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(20)

        # Ícone
        icon_label = QLabel()
        pixmap = QPixmap("data/assets/logo.png") 
        icon_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Título
        title_label = QLabel("EQUILIBRA")
        title_label.setObjectName("HeaderText")

        header_layout.addStretch(1)
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        layout.addWidget(header_widget)

        # Tabs
        from PyQt5.QtWidgets import QTabWidget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("ModernTabs")

        # Abas
        self.tab_usuarios = QWidget()
        self.tab_tarefas = QWidget()
        self.tab_consultas = QWidget()
        self.tab_dica = QWidget()

        # Configura cada aba
        self.setup_tab_usuarios()
        self.setup_tab_tarefas()
        self.setup_tab_consultas()
        self.setup_tab_dica()

        self.tabs.addTab(self.tab_usuarios, "Usuários")
        self.tabs.addTab(self.tab_tarefas, "Tarefas")
        self.tabs.addTab(self.tab_consultas, "Relatórios")
        self.tabs.addTab(self.tab_dica, "Dica do Dia")

        layout.addWidget(self.tabs)
        self.setCentralWidget(container)

### ----------------------- #
### ABA: USUÁRIOS
### ----------------------- #
    def setup_tab_usuarios(self):# Configura a interface da aba de usuários.
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Gerenciamento de Usuários")
        title.setObjectName("Title")
        layout.addWidget(title)

        # Formulário Card
        form_card = QFrame()
        form_card.setObjectName("Card")
        form_layout = QHBoxLayout(form_card)
        form_layout.setSpacing(12)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome completo")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("E-mail corporativo")
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Híbrido", "Home Office", "Presencial"])

        btn_add = QPushButton("Adicionar Usuário")
        btn_add.clicked.connect(self.adicionar_usuario)

        form_layout.addWidget(self.input_nome, 3)
        form_layout.addWidget(self.input_email, 3)
        form_layout.addWidget(self.combo_tipo, 1)
        form_layout.addWidget(btn_add, 1)

        layout.addWidget(form_card)

        # Tabela
        self.table_usuarios = QTableWidget()
        self.table_usuarios.setColumnCount(4)
        self.table_usuarios.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Modalidade"])
        self.table_usuarios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_usuarios.verticalHeader().setVisible(False)
        layout.addWidget(self.table_usuarios)

        # Ações
        actions = QHBoxLayout()
        btn_refresh = QPushButton("Atualizar")
        btn_refresh.clicked.connect(self.carregar_usuarios)
        btn_delete = QPushButton("Excluir Usuário")
        btn_delete.clicked.connect(self.excluir_usuario)
        actions.addStretch()
        actions.addWidget(btn_refresh)
        actions.addWidget(btn_delete)

        layout.addLayout(actions)
        self.tab_usuarios.setLayout(layout)

        try:
            self.carregar_usuarios()
        except Exception:
            pass

    def adicionar_usuario(self):# Adiciona um novo usuário ao banco de dados
        nome = self.input_nome.text().strip()
        email = self.input_email.text().strip()
        tipo = self.combo_tipo.currentText()
        if not nome or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return
        try:
            db.criar_usuario_db(nome, email, tipo)
            self.input_nome.clear()
            self.input_email.clear()
            self.carregar_usuarios()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao criar usuário:\n{e}")

    def carregar_usuarios(self):# Carrega os usuários e preenche a tabela.
        try:
            dados = db.listar_usuarios_db() or []
        except Exception as e:
            dados = []
            QMessageBox.critical(self, "Erro", f"Falha ao carregar usuários:\n{e}")

        self.table_usuarios.setRowCount(0)
        for i, row in enumerate(dados):
            self.table_usuarios.insertRow(i)
            for j, val in enumerate(row):
                it = QTableWidgetItem(str(val))
                it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                self.table_usuarios.setItem(i, j, it)

    def excluir_usuario(self):# Exclui o usuário selecionado na tabela.
        row = self.table_usuarios.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um usuário!")
            return
        id_item = self.table_usuarios.item(row, 0)
        nome_item = self.table_usuarios.item(row, 1)
        if not id_item:
            QMessageBox.warning(self, "Erro", "ID inválido.")
            return
        id_usuario = id_item.text()
        nome_usuario = nome_item.text() if nome_item else ""
        resp = QMessageBox.question(self, "Confirmar", f"Excluir usuário: {nome_usuario} (ID {id_usuario})?")
        if resp == QMessageBox.Yes:
            try:
                db.deletar_usuario_db(id_usuario)
                self.carregar_usuarios()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir:\n{e} \n\n!!!Tente excluir as tarefas do usuário primeiro!!!")

### ----------------------- #
### ABA: TAREFAS
### ----------------------- #
    def setup_tab_tarefas(self):# Configura a interface da aba de tarefas.
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Gerenciamento de Tarefas")
        title.setObjectName("Title")
        layout.addWidget(title)

        # Botão nova tarefa à direita
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_nova = QPushButton("➕ Nova Tarefa")
        btn_nova.clicked.connect(self.abrir_dialogo_tarefa)
        btn_row.addWidget(btn_nova)
        layout.addLayout(btn_row)

        # Tabela
        self.table_tarefas = QTableWidget()
        self.table_tarefas.setColumnCount(6)
        self.table_tarefas.setHorizontalHeaderLabels(["ID", "Usuário", "Título", "Status", "Tipo", "Descrição"])
        self.table_tarefas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_tarefas.verticalHeader().setVisible(False)
        layout.addWidget(self.table_tarefas)

        # Ações
        actions = QHBoxLayout()
        btn_refresh = QPushButton("Atualizar")
        btn_refresh.clicked.connect(self.carregar_tarefas)
        btn_toggle = QPushButton("Alternar Status")
        btn_toggle.clicked.connect(self.alternar_status_tarefa)
        btn_delete = QPushButton("Excluir")
        btn_delete.clicked.connect(self.excluir_tarefa)
        actions.addStretch()
        actions.addWidget(btn_refresh)
        actions.addWidget(btn_toggle)
        actions.addWidget(btn_delete)
        layout.addLayout(actions)

        self.tab_tarefas.setLayout(layout)

        try:
            self.carregar_tarefas()
        except Exception:
            pass

    def carregar_tarefas(self):# Carrega as tarefas e preenche a tabela.
        try:
            dados = db.listar_tarefas_db() or []
        except Exception as e:
            dados = []
            QMessageBox.critical(self, "Erro", f"Falha ao carregar tarefas:\n{e}")

        self.table_tarefas.setRowCount(0)
        for i, row in enumerate(dados):
            self.table_tarefas.insertRow(i)
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                # Colorir coluna Status
                if j == 3:
                    if str(val).lower() in ("concluída", "concluida", "concluido"):
                        item.setForeground(QColor("#2ecc71"))
                        font = QFont()
                        font.setBold(True)
                        item.setFont(font)
                    else:
                        item.setForeground(QColor("#f39c12"))
                self.table_tarefas.setItem(i, j, item)

    def abrir_dialogo_tarefa(self):# Abre uma janela para criar uma nova tarefa.
        dialog = QDialog(self)
        dialog.setWindowTitle("Nova Tarefa")
        dialog.setModal(True)
        dialog.setMinimumWidth(420)
        layout = QVBoxLayout(dialog)

        form = QFormLayout()
        # Carrega usuários (id, nome)
        try:
            usuarios = db.listar_usuarios_db() or []
        except Exception:
            usuarios = []

        combo_user = QComboBox()
        if usuarios:
            for u in usuarios:
                # u expected: (id, nome, email, tipo)
                combo_user.addItem(f"{u[1]} (ID:{u[0]})", u[0])
        else:
            combo_user.addItem("Nenhum usuário cadastrado", None)
            combo_user.setEnabled(False)

        input_titulo = QLineEdit()
        input_desc = QLineEdit()
        combo_tipo = QComboBox()
        combo_tipo.addItems(["Pessoal", "Profissional"])

        form.addRow("Usuário:", combo_user)
        form.addRow("Título:", input_titulo)
        form.addRow("Descrição:", input_desc)
        form.addRow("Tipo:", combo_tipo)
        layout.addLayout(form)

        # Botões
        btns = QHBoxLayout()
        btns.addStretch()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(dialog.reject)
        btn_save = QPushButton("Salvar")
        def salvar():
            if not input_titulo.text().strip():
                QMessageBox.warning(dialog, "Atenção", "Título é obrigatório.")
                return
            if not combo_user.currentData():
                QMessageBox.warning(dialog, "Atenção", "Selecione um usuário válido.")
                return
            try:
                db.criar_tarefa_db(combo_user.currentData(), input_titulo.text().strip(),
                                   input_desc.text().strip(), combo_tipo.currentText())
                dialog.accept()
                self.carregar_tarefas()
            except Exception as e:
                QMessageBox.critical(dialog, "Erro", f"Falha ao criar tarefa:\n{e}")

        btn_save.clicked.connect(salvar)
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_save)
        layout.addLayout(btns)

        dialog.exec_()

    def alternar_status_tarefa(self):# Alterna o status da tarefa selecionada.
        row = self.table_tarefas.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma tarefa.")
            return
        id_item = self.table_tarefas.item(row, 0)
        status_item = self.table_tarefas.item(row, 3)
        if not id_item or not status_item:
            QMessageBox.warning(self, "Erro", "Seleção inválida.")
            return
        id_tarefa = id_item.text()
        status_atual = status_item.text()
        novo = "Concluída" if status_atual.lower() != "concluída" and status_atual.lower() != "concluida" else "Pendente"
        try:
            db.atualizar_status_tarefa_db(id_tarefa, novo)
            self.carregar_tarefas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao atualizar status:\n{e}")

    def excluir_tarefa(self):# Exclui a tarefa selecionada na tabela.
        row = self.table_tarefas.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma tarefa.")
            return
        id_item = self.table_tarefas.item(row, 0)
        titulo_item = self.table_tarefas.item(row, 2)
        if not id_item:
            QMessageBox.warning(self, "Erro", "ID inválido.")
            return
        id_tarefa = id_item.text()
        titulo = titulo_item.text() if titulo_item else ""
        resp = QMessageBox.question(self, "Confirmar", f"Excluir tarefa: {titulo}?")
        if resp == QMessageBox.Yes:
            try:
                db.deletar_tarefa_db(id_tarefa)
                self.carregar_tarefas()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir:\n{e}")

### ----------------------- #
### ABA: RELATÓRIOS
### ----------------------- #
    def setup_tab_consultas(self):# Configura a interface da aba de relatórios.
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        title = QLabel("Relatórios e Consultas")
        title.setObjectName("Title")
        layout.addWidget(title)

        btns = QHBoxLayout()
        b1 = QPushButton("Tarefas Concluídas")
        b1.clicked.connect(lambda: self.executar_consulta(cons.get_dados_quantidade_tarefas))
        b2 = QPushButton("Tarefas por Usuário")
        b2.clicked.connect(lambda: self.executar_consulta(cons.get_dados_tarefas_concluidas_usuario))
        b3 = QPushButton("Tempo Médio de Conclusão")
        b3.clicked.connect(lambda: self.executar_consulta(cons.get_dados_tempo_medio))
        b4 = QPushButton("Percentuais de Conclusão")
        b4.clicked.connect(lambda: self.executar_consulta(cons.get_dados_percentual))
        for b in (b1, b2, b3, b4):
            b.setMinimumHeight(40)
            btns.addWidget(b)
        layout.addLayout(btns)

        self.table_rel = QTableWidget()
        self.table_rel.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_rel.verticalHeader().setVisible(False)
        layout.addWidget(self.table_rel)
        
        actions = QHBoxLayout()
        self.lbl_path = QLabel("Nenhum relatório exportado nesta sessão.")
        self.lbl_path.setObjectName("LabelPath")
        btn_open = QPushButton("Abrir Exportação")
        btn_open.clicked.connect(self.abrir_pasta_exportacao)
        actions.addStretch()
        actions.addWidget(self.lbl_path)
        actions.addWidget(btn_open)
        layout.addLayout(actions)
        
        self.tab_consultas.setLayout(layout)

    def abrir_pasta_exportacao(self):# Abre a pasta onde os relatórios JSON são salvos.
        path = os.path.join(os.getcwd(), "data", "resultados")
        os.makedirs(path, exist_ok=True)
        try:
            # A maneira mais compatível de abrir um diretório
            os.startfile(path)
        except AttributeError:
            # Fallback para macOS e Linux
            import subprocess
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

    def executar_consulta(self, func):# Exibe os dados da consulta selecionada na tabela.
        try:
            dados, path = func()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na consulta:\n{e}")
            return
        self.table_rel.setRowCount(0)
        if not dados:
            QMessageBox.information(self, "Resultado", "Nenhum dado retornado pela consulta.")
            return
        self.lbl_path.setText(f"Exportado para: {path}")
        cols = list(dados[0].keys())
        self.table_rel.setColumnCount(len(cols))
        self.table_rel.setHorizontalHeaderLabels([c.replace("_", " ").title() for c in cols])
        for i, row in enumerate(dados):
            self.table_rel.insertRow(i)
            for j, key in enumerate(cols):
                self.table_rel.setItem(i, j, QTableWidgetItem(str(row.get(key, ""))))

### ----------------------- #
### ABA: DICA DO DIA
### ----------------------- #
    def setup_tab_dica(self):# Configura a interface da aba "Dica do Dia".
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("💡 Dica do Dia")
        title.setObjectName("Title")
        layout.addWidget(title)

        self.dica_card = QFrame()
        self.dica_card.setObjectName("Card")
        dica_layout = QVBoxLayout(self.dica_card)
        self.lbl_dica = QLabel("Clique em 'Obter Nova Dica' para carregar uma reflexão.")
        self.lbl_dica.setWordWrap(True)
        dica_layout.addWidget(self.lbl_dica)
        layout.addWidget(self.dica_card)

        btn = QPushButton("Obter Nova Dica")
        btn.clicked.connect(self.mostrar_dica)
        layout.addWidget(btn, alignment=Qt.AlignLeft)

        self.tab_dica.setLayout(layout)

    def mostrar_dica(self):# Busca e exibe uma nova dica do dia.
        try:
            ok, texto = api.obter_dica_do_dia()
        except Exception as e:
            ok, texto = False, f"Erro: {e}"
        self.lbl_dica.setText(texto if ok else f"❌ {texto}")

### ----------------------- #
### Estilos
### ----------------------- #
    def load_styles(self):# Carrega a folha de estilos(CSS).
        return """
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 25px;
            color: #e6eef8;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #151515, stop:1 #1e1e1e);
        }
        QLabel#Header {
            background:#0f1720;
            padding:18px;
            font-size:30px;
            font-weight:700;
            color:#DBEAFE;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }
        QLabel#HeaderText {
            background: transparent;
            border: none;
            font-family: 'Ubuntu';
            font-size: 35px;
        }
        QLabel#LabelPath {
            font-size: 12px;
            color: #999;
            background: transparent;
            border: none;
        }
        QLabel#Title {
            font-size:25px;
            color:#7fb3ff;
            margin-bottom:8px;
            font-weight:600;
        }
        QFrame#Card {
            background: #111217;
            border-radius:10px;
            border: 1px solid rgba(255,255,255,0.03);
            padding:14px;
        }
        QLineEdit, QComboBox {
            background: #0f1113;
            border: 1px solid rgba(255,255,255,0.03);
            padding:8px;
            border-radius:8px;
            color:#e6eef8;
        }
        QPushButton {
            background-color: #3d7afe;
            color: white;
            border-radius:8px;
            padding:8px 16px;
            font-weight:600;
        }
        QPushButton:hover {
            background-color: #5a8cff;
        }
        QPushButton:pressed {
            background-color: #2c5edb;
        }
        QTableWidget {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.03);
            gridline-color: rgba(255,255,255,0.03);
        }
        QHeaderView::section {
            background: #0b1220;
            color: #cfe8ff;
            padding:6px;
            border: none;
        }
        QTabBar::tab {
            background: #2d2d2d;
            color: #000000;
            padding: 10px 20px;
            margin-right: 2px;
            border-radius: 8px 8px 0 0;
        }
        QTabBar::tab:selected {
            background: #3a3a3a;
            color: white;
            font-weight: bold;
        }
        """

###======================###
###  Executar o Sistema  ###
###======================###
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carrega a fonte personalizada do arquivo
    font_path = os.path.join("data", "assets", "Ubuntu-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)

    # Executa a interface com o sistema
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
