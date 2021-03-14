from unittest import TestCase
from json import load
import os
from Utils import utils

try: 
    from Trafo import trafo, CONSTANTES
except Exception as e:
    print(f"o erro foi {e}") 
    from .Trafo import trafo, CONSTANTES

CONSTANTES_DADAS = CONSTANTES.CONSTANTES_DADAS 
VARIAVEIS = CONSTANTES.VARIAVEIS




class TestTrafo(TestCase):
   
    def setUp(self):
        self.pathjson = "tests/json/"
        self.config = load(open(self.pathjson + "config.json", "r"))
        self.filename = "teste_{}.json".format(self.config["n"])
        # import ipdb; ipdb.set_trace()

    def test_se_existe_json(self):
        "Testa se existe o arquivo JSON na pasta raiz do projeto"
        dirs = os.listdir(self.pathjson)
        #import ipdb; ipdb.set_trace()
        self.assertIn(self.filename, dirs, "Nao existe o objeto JSON")

    def test_se_json_de_teste_tem_todas_as_variaveis_nescessarias(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        try:
            _trafo = trafo.Trafo(json_variables, json_variables)
        except Exception as err: 
            self.assertTrue(False, f"houve um erro na criação do objeto Trafo\nErro: {err}")
        import ipdb; ipdb.set_trace()

