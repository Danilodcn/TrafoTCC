import sys, os

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
        self.connect_button_menu()
        self.connect_buttons()
        
        self.show()
    

    def connect_button_menu(self):
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
    
    def connect_buttons(self):
        self.ui.botao_novo_adicionar_json.clicked.connect(
            self.seleciona_json
        )   
    
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
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(app)
    win.show()
    sys.exit(app.exec_())