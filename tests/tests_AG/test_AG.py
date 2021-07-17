import os
from json import load
from unittest import TestCase

try:
    from AG.AG import AG

except ImportError as error:
    #import ipdb; ipdb.set_trace()
    pass
try:
    from .utils import erro_e_aceitavel, print_dict
except:
    from utils import erro_e_aceitavel, print_dict


class Teste_Criação_do_Objeto_Algoritmo_genético(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + "ag.json"
        # self.json = load(open(self.teste))
        # self.dados = load(open(self.pathjson + "ag.json"))
    
    def teste_se_existe_json_para_criação_do_AG(self):
        existe_arquivo = os.path.isfile(self.teste) 
        self.assertTrue(existe_arquivo, f'O "{self.teste}" arquivo nao existe no ditetório "{self.pathjson}"')
        
    def teste_criação_do_objeto_Algoritmo_genético(self):
        dados = load(open(self.teste, "r"))
        # import ipdb; ipdb.set_trace()
        ag = AG(**dados)
        
