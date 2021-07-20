import sys, os, json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
        QApplication, 
        QMainWindow, 
        QFileDialog,
        QMessageBox 
    )

from qt_material import apply_stylesheet, QtStyleTools, list_themes

from main import Ui_MainWindow

class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self, app, tema="dark_cyan", *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.temas = dict(zip(map(lambda nome: " ".join(os.path.splitext(nome)[0].split("_")), list_themes()), list_themes()))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
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
        
        self.tema = tema.replace("_", " ")
        self.app = app
        self.init_ui()
        apply_stylesheet(app, self.temas[self.tema])
        self.show()
    
    def init_ui(self):
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
        # Botao de salvar JSON
        self.ui.botao_novo_salvar.clicked.connect(
            lambda: self.salvar_json(file_name="")
        )
        self.ui.botao_novo_limpar.clicked.connect(
            lambda: self.__carregar_json(None, "")
        )
        self.ui.botao_novo_run.clicked.connect(
            lambda: print("Foi")
        )
        
        #carrega combo_box
        self.ui.combo_box_tipo_conexao.addItem("estrela-delta")
        self.ui.combo_box_tipo_conexao.addItem("delta-estrela")
        self.ui.combo_box_tipo_conexao.addItem("estrela-estrela")
        self.ui.combo_box_tipo_conexao.addItem("delta-delta")
        
        self.ui.combo_box_tipo_refrigeracao.addItem("seco")
        self.ui.combo_box_tipo_refrigeracao.addItem("oleo")
        
        self.ui.comboBox_themes.addItem(self.tema)
        
        def f(nome):
            nome, _ = os.path.splitext(nome)
            return " ".join(nome.split("_"))
        
        self.ui.comboBox_themes.addItems(self.temas.keys())
        
        self.ui.comboBox_themes.currentTextChanged.connect(
            lambda tema: (
                self.ui.comboBox_themes.setCurrentText(tema),
                apply_stylesheet(self.app, self.temas[tema])
            )
        )
        
        # import ipdb; ipdb.set_trace(context=10)
        
         #Aplica validadores nos campos lineEdit
        self.ui.lineEdit_Ke.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        self.ui.lineEdit_potencia_trafo.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        self.ui.lineEdit_tensao_primario.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        self.ui.lineEdit_tensao_secundario.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        self.ui.lineEdit_densidade_fe.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        self.ui.lineEdit_densidade_al.setValidator(QtGui.QDoubleValidator(0, 1e12, 2))
        
        self.ui.label_novo_nome_do_json_adicionado.setOpenExternalLinks(True)
        # self.ui.label_novo_nome_do_json_adicionado.setTextInteractionFlags(QtWidgets.QtTextBrowserInteraction)
        
        
        #Inicializa a tela NOVO
        self.__carregar_json()
        
    def salvar_json(self, file_name=""):
        if file_name == "":
            path = os.environ["HOMEPATH"]
            path = r"C:\Users\dacon\git\TrafoTCC\GUI"
            file = QFileDialog.getSaveFileName(self, "Save File", path, "json file (*.json)")
            file_name = file[0]
            # import ipdb; ipdb.set_trace(context=10)
            if file_name == "":
                return
            
        dados = self.__get_json()
        with open(file_name, "w") as file:
            json.dump(dados, file, indent=4)
            
    
    def seleciona_json(self, *args, **kwargs):
        # print("clicando", args)
        path = os.environ["HOMEPATH"]
        path = r"C:\Users\dacon\git\TrafoTCC\GUI"
        file = QFileDialog.getOpenFileName(self, "Open File", path, "json file (*.json)")
        diretorio, file_name = os.path.split(file[0])
        _, extensao = os.path.splitext(file_name)
        
        if extensao == ".json":
            dados_lidos_json = json.load(open(diretorio + "/" + file_name, "r"))
            self.__carregar_json(dados_lidos_json, limpar_nome=False)
            url_link = r'<a href=file:///{0}> {1}</a>'.format(file[0], file_name)
            self.ui.label_novo_nome_do_json_adicionado.setText(url_link.format(url_link))
            
        else:  
            # print("Houve um erro")
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Você não selecionou um arquivo json")
            error.setWindowTitle("Erro encontrado")
            # error.setDetailedText("Detalhe do erro: ")
            error.setStandardButtons(QMessageBox.Ok)
            error.show()
            # error.buttonClicked(msgbox)
            error.exec_()
            # valor = error.exec_()
            # print("Valor clicado: ", valor)
        # import ipdb; ipdb.set_trace(context=10)
            

    def __carregar_json(self, __json=None, file="", limpar_nome=True):
        if __json == None:
            if file == "":
                file = "./GUI/json_padrao.json"
            __json = json.load(open(file, "r"))
        
        self.ui.spinBox_numero_max_geracoes.setValue(__json["max_geracoes"])
        self.ui.spinBox_max_individuos_populacao.setValue(__json["numero_populacao"])
        
        constantes_ag = __json["constantes_ag"]
        
        self.ui.doubleSpinBox_taxa_mutacao.setValue(constantes_ag["taxa_mutacao"]*100)
        self.ui.doubleSpinBox_taxa_crossover.setValue(constantes_ag["taxa_crossover"]*100)
        self.ui.spinBox_numero_frentes_selecionar.setValue(constantes_ag["n_frentes"])
        
        variacoes = __json["variacoes"]
        
        self.ui.doubleSpinBox_min_Jbt.setValue(variacoes["Jbt"][0])
        self.ui.doubleSpinBox_max_Jbt.setValue(variacoes["Jbt"][1])
        
        self.ui.doubleSpinBox_min_Jat.setValue(variacoes["Jat"][0])
        self.ui.doubleSpinBox_max_Jat.setValue(variacoes["Jat"][1])
        
        self.ui.doubleSpinBox_min_Bm.setValue(variacoes["Bm"][0])
        self.ui.doubleSpinBox_max_Bm.setValue(variacoes["Bm"][1])
        
        self.ui.doubleSpinBox_min_Ksw.setValue(variacoes["Ksw"][0])
        self.ui.doubleSpinBox_max_Ksw.setValue(variacoes["Ksw"][1])
        
        self.ui.doubleSpinBox_min_kt.setValue(variacoes["kt"][0])
        self.ui.doubleSpinBox_max_kt.setValue(variacoes["kt"][1])
        
        self.ui.doubleSpinBox_min_Rjan.setValue(variacoes["Rjan"][0])
        self.ui.doubleSpinBox_max_Rjan.setValue(variacoes["Rjan"][1])
        
        self.ui.doubleSpinBox_min_rel.setValue(variacoes["rel"][0])
        self.ui.doubleSpinBox_max_rel.setValue(variacoes["rel"][1])
        
        constantes = __json["constantes"]
        
        self.ui.combo_box_tipo_conexao.setCurrentText(constantes["conexao"])
        self.ui.lineEdit_Ke.setText(str(constantes["Ke"]))
        self.ui.lineEdit_potencia_trafo.setText(str(constantes["S"]))
        self.ui.spinBox_n_fases.setValue(constantes["Nfases"])
        self.ui.spinBox_frequencia_hz.setValue(constantes["f"])
        self.ui.lineEdit_tensao_primario.setText(str(constantes["V1"]))
        self.ui.lineEdit_tensao_secundario.setText(str(constantes["V2"]))
        self.ui.combo_box_tipo_refrigeracao.setCurrentText(constantes["tipo"])
        self.ui.lineEdit_densidade_fe.setText(str(constantes["Dfe"]))
        self.ui.lineEdit_densidade_al.setText(str(constantes["Dal"]))
        
        if limpar_nome:
           self.ui.label_novo_nome_do_json_adicionado.setText("")
            
        
        # import ipdb; ipdb.set_trace(context=10)
    
    def __get_json(self):
        dados = {}
        
        dados["max_geracoes"] = self.ui.spinBox_numero_max_geracoes.value()
        dados["numero_populacao"] = self.ui.spinBox_max_individuos_populacao.value()
        
        constantes = {}
        constantes["taxa_mutacao"] = self.ui.doubleSpinBox_taxa_mutacao.value() / 100
        constantes["taxa_crossover"] = self.ui.doubleSpinBox_taxa_crossover.value() / 100
        constantes["n_frentes"] = self.ui.spinBox_numero_frentes_selecionar.value()
        
        dados["constantes_ag"] = constantes
        
        variacoes = {}
        variacoes["Jbt"] = [
            self.ui.doubleSpinBox_min_Jbt.value(),
            self.ui.doubleSpinBox_max_Jbt.value()
        ]
        variacoes["Jat"] = [
            self.ui.doubleSpinBox_min_Jat.value(),
            self.ui.doubleSpinBox_max_Jat.value()
        ]
        variacoes["Bm"] = [
            self.ui.doubleSpinBox_min_Bm.value(),
            self.ui.doubleSpinBox_max_Bm.value()
        ]
        variacoes["Ksw"] = [
            self.ui.doubleSpinBox_min_Ksw.value(),
            self.ui.doubleSpinBox_max_Ksw.value()
        ]
        variacoes["kt"] = [
            self.ui.doubleSpinBox_min_kt.value(),
            self.ui.doubleSpinBox_max_kt.value()
        ]
        variacoes["Rjan"] = [
            self.ui.doubleSpinBox_min_Rjan.value(),
            self.ui.doubleSpinBox_max_Rjan.value()
        ]
        variacoes["rel"] = [
            self.ui.doubleSpinBox_min_rel.value(),
            self.ui.doubleSpinBox_max_rel.value()
        ]
        
        dados["variacoes"] = variacoes
        
        constantes = {}
        constantes["conexao"] = self.ui.combo_box_tipo_conexao.currentText()
        constantes["Ke"] = self.ui.lineEdit_Ke.text()
        constantes["S"] = self.ui.lineEdit_potencia_trafo.text()
        constantes["Nfases"] = self.ui.spinBox_n_fases.value()
        constantes["f"] = self.ui.spinBox_frequencia_hz.value()
        constantes["V1"] = self.ui.lineEdit_tensao_primario.text()
        constantes["V2"] = self.ui.lineEdit_tensao_secundario.text()
        constantes["tipo"] = self.ui.combo_box_tipo_refrigeracao.currentText()
        constantes["Dfe"] = self.ui.lineEdit_densidade_fe.text()
        constantes["Dal"] = self.ui.lineEdit_densidade_fe.text()
        
        dados["constantes"] = constantes
        # x = json.load(open(r"C:\Users\dacon\git\TrafoTCC\tests\json\AG\ag.json"))
        # import ipdb; ipdb.set_trace(context=10)
        return dados
    
if __name__ == "__main__":
    cor1, cor2, cor3, cor4, cor5 = ("#1D1B59", "#363973", "#253259", "#38F2F2", "#591202")
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    os.environ["QTMATERIAL_PRIMARYCOLOR"] = cor1
    os.environ["QTMATERIAL_PRIMARYTEXTCOLOR"] = cor5
    
    
    win = MainWindow(app)
    win.show()
    sys.exit(app.exec_())