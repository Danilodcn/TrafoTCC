import sys, os, json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
        QApplication, 
        QMainWindow, 
        QFileDialog,
        QMessageBox 
    )

from qt_material import apply_stylesheet

from main import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        apply_stylesheet(app, "dark_cyan.xml")
        
        ##nao sei mais o que estou fazendo kkk
        
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))
        
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        
        self.setWindowIcon(QtGui.QIcon(":/icons/svg/ic_wifi_tethering_48px.svg"))
        self.setWindowTitle("Trafo App")
        
        # QtWidgets.QSizeGrip(self.ui.size_gripe)
        self.init_ui()
        
        self.show()
    
    def init_ui(self):
        self.ui.botao_menu_home.clicked.connect(lambda *args, **wargs: print(args, wargs))
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        self.ui.label_titulo_app.setText("App Trafo")
        
        self.ui.botao_home_home.clicked.connect(
            lambda: (
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home),
                self.ui.label_titulo_app.setText("App Trafo"),
            )
        )
        self.ui.botao_novo_home.clicked.connect(
            lambda: (
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_novo),
                self.ui.label_titulo_app.setText("Inserir Novos Dados Para Simulação"),
            )
        )
        self.ui.botao_historico_home.clicked.connect(
            lambda: (
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_historico),
                self.ui.label_titulo_app.setText("Histórico de Execuções"),
            )
        )
        
        self.ui.botao_info_home.clicked.connect(
            lambda: (
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_info),
                self.ui.label_titulo_app.setText("Informações Sobre o Software"),
            )
        )
        # Botao de adicionar JSON
        self.ui.botao_novo_adicionar_json.clicked.connect(
            self.seleciona_json
        )
        
        #carrega combo_box
        self.ui.combo_box_novo_dados_trafo_conexao.addItem("Delta-Estrela")
        self.ui.combo_box_novo_dados_trafo_conexao.addItem("Estrela-Delta")
        self.ui.combo_box_novo_dados_trafo_conexao.addItem("Estrela-Estrela")
        self.ui.combo_box_novo_dados_trafo_conexao.addItem("Delta-Delta")
        
        self.ui.combo_box_novo_dados_tipo_refrigeracao.addItem("a seco")
        self.ui.combo_box_novo_dados_tipo_refrigeracao.addItem("a óleo")
        
        #Inicializa a tela NOVO
        self.__carregar_json()
        
        
    def seleciona_json(self, *args, **kwargs):
        # print("clicando", args)
        path = os.environ["HOMEPATH"]
        file = QFileDialog.getOpenFileName(self, "Open File", path, "json file (*.json)")
        diretorio, file_name = os.path.split(file[0])
        _, extensao = os.path.splitext(file_name)
        
        if extensao == ".json":
            print("Certo!!")
        else:  
            # print("Houve um erro")
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Você não selecionou um arquivo json")
            error.setWindowTitle("Erro encontrado")
            error.setDetailedText("Detalhe do erro: ")
            error.setStandardButtons(QMessageBox.Ok)
            error.show()
            # error.buttonClicked(msgbox)
            error.exec_()
            # valor = error.exec_()
            # print("Valor clicado: ", valor)
        # import ipdb; ipdb.set_trace(context=10)
            

    def __carregar_json(self, __json=None, file=""):
        if __json == None:
            if file == "":
                file = "./GUI/json_padrao.json"
            __json = json.load(open(file, "r"))
        
        self.ui.spinBox_numero_max_geracoes.setValue(__json["max_geracoes"])
        self.ui.spinBox_max_individuos_populacao.setValue(__json["numero_populacao"])
        
        constantes_ag = __json["constantes_ag"]
        
        self.ui.doubleSpinBox_taxa_mutacao.setValue(constantes_ag["taxa_mutacao"])
        
        
        
        # import ipdb; ipdb.set_trace(context=10)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(app)
    win.show()
    sys.exit(app.exec_())