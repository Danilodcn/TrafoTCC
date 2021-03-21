from unittest import TestCase
from json import load
import os, sys
sys.path.append(os.getcwd())

try: 
    from Trafo import trafo, CONSTANTES
    from Utils import utils

except Exception as e:
    print(f"o erro foi {e}")
    from .Utils import utils
    from .Trafo import trafo, CONSTANTES

CONSTANTES_DADAS = CONSTANTES.CONSTANTES_DADAS 
VARIAVEIS = CONSTANTES.VARIAVEIS


def print_dict(dicionario: dict[float, float], simbolo: str = "-") -> str:
    lista = []
    for key, value in dicionario.items():
        txt = str(key) + " = " + f"{simbolo} ".join(map(str, value))
        lista.append(txt)
    
    return ", ".join(lista)

def erro_e_aceitavel(a: float, b: float, error: float) -> bool:
    if a == 0:
        if b == 0: return True
        else: return False
    return abs((a - b) / a) <= error 


class TestTrafo(TestCase):
   
    def setUp(self):
        self.pathjson = "tests/json/trafo/"
        self.config = load(open("tests/config.json", "r"))
        self.filename = "teste_{}.json".format(self.config["n"])
        self.error_aceitavel = self.config["error"]
        # import ipdb; ipdb.set_trace()

    def test_se_existe_json(self):
        "Testa se existe o arquivo JSON na pasta raiz do projeto"
        dirs = os.listdir(self.pathjson)
        #import ipdb; ipdb.set_trace()
        self.assertIn(self.filename, dirs, "Nao existe o objeto JSON")
        
    def test_se_json_de_teste_tem_todas_as_variaveis_nescessarias(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        
        # from ipdb import set_trace; set_trace()
        
        try:
            _trafo = trafo.Trafo(json_variables)
        except Exception as err: 
            self.assertTrue(False, f"houve um erro na criação do objeto Trafo\nErro: {err}")
        # import ipdb; ipdb.set_trace()
    
    def test_calculo_de_dados_do_trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        tests_variables = _trafo.resultado_calculos
        not_pass = {}
        for key, value in tests_variables.items():
            try:
                if value != json_variables[key]:
                    not_pass[key] = [value, f"é diferente de {json_variables[key]}"]
            except:
                not_pass[key] = [value, "não existe no JSON " + self.filename]

        msg = print_dict(not_pass, " -> ")
        txt = "Erros encontrados ao executar o teste do calculo das dimenções do trafo. "
        txt += "Os erros foram: [{}]".format(msg)
        
        self.assertDictEqual(not_pass, {}, txt)


    def test_calculo_das_dimensoes_do_trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        variaveis = _trafo.inicia_as_variaveis(VARIAVEIS, json_variables)
        _trafo.calculo_das_dimensoes_do_trafo(variaveis, debug=True)

        # import ipdb; ipdb.set_trace()

        tests_variables = _trafo.resultado_calculos
        not_pass = {}
        for key, value in tests_variables.items():
            
            try:
                y = json_variables[key]

                if key in []:
                    if not erro_e_aceitavel(value, json_variables[key], self.error_aceitavel * 1000000):
                        not_pass[key] = [value, f"é diferente de {json_variables[key]}"]

                    # import ipdb; ipdb.set_trace()
                    
                    continue
                if key in []:
                    if not erro_e_aceitavel(value, y, self.error_aceitavel * 20):
                        r = abs((value - y) / value)
                        not_pass[key] = [value, f"é diferente de {y}. Erro de {r * 100} %"]

                    # import ipdb; ipdb.set_trace()
                    
                    continue

                if not erro_e_aceitavel(value, json_variables[key], self.error_aceitavel):
                    r = abs((value - y) / value)
                    not_pass[key] = [value, f"é diferente de {y}. Erro de {r * 100} %"]
            except:
                
                not_pass[key] = [value, "não existe no JSON " + self.filename]

            if key == "atc":
                # import ipdb; ipdb.set_trace()
                ...

        msg = print_dict(not_pass, " -> ")
        txt = "Erros encontrados ao executar o teste do calculo das dimenções do trafo. "
        txt += "Os erros foram: [{}]".format(msg)
        
        # import ipdb; ipdb.set_trace()
        self.assertDictEqual(not_pass, {}, txt)
   
                        


    def test_resultado_calculos_a_partir_do_atributo_no_objeto_Trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        tests_variables = _trafo.resultado_calculos
        not_pass = {}
        
        for key, value in tests_variables.items():
            sucess = value == json_variables[key]
            if not sucess: 
                not_pass[key] = [value, json_variables[key]]

        msg = print_dict(not_pass, " != ")
        #import ipdb; ipdb.set_trace()

        txt =   "Alguns do calculos não estão corretos. Os valores sao: [{}]".format(msg)
        self.assertDictEqual(not_pass, {}, txt)

        