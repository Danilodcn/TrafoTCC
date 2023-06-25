import os
import sys
from json import load
from unittest import TestCase

sys.path.append(os.getcwd())

from tcc.trafo import CONSTANTES, trafo
from tcc.utils import utils

CONSTANTES_DADAS = CONSTANTES.CONSTANTES_DADAS
VARIAVEIS = CONSTANTES.VARIAVEIS

try:
    from .utils import erro_e_aceitavel, print_dict
except:
    from utils import erro_e_aceitavel, print_dict


class TestTrafo(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/trafo/"
        self.config = load(open("tests/config.json", "r"))
        self.filename = "teste_{}.json".format(self.config["n"])
        self.error_aceitavel = self.config["error"]

    def teste_se_existe_json(self):
        "Testa se existe o arquivo JSON na pasta raiz do projeto"
        dirs = os.listdir(self.pathjson)

        self.assertIn(self.filename, dirs, "Nao existe o objeto JSON")

    def teste_se_json_de_teste_tem_todas_as_variaveis_nescessarias(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))

        # from ipdb import set_trace; set_trace()

        try:
            _trafo = trafo.Trafo(json_variables)
        except Exception as err:
            self.assertTrue(
                False, f"houve um erro na criação do objeto Trafo\nErro: {err}"
            )

    def teste_calculo_de_dados_do_trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        tests_variables = _trafo.resultado_calculos
        not_pass = {}
        for key, value in tests_variables.items():
            try:
                if value != json_variables[key]:
                    not_pass[key] = [
                        value,
                        f"é diferente de {json_variables[key]}",
                    ]
            except:
                not_pass[key] = [value, "não existe no JSON " + self.filename]

        msg = print_dict(not_pass, " -> ")
        txt = "Erros encontrados ao executar o teste do calculo das dimenções do trafo. "
        txt += "Os erros foram: [{}]".format(msg)

        self.assertDictEqual(not_pass, {}, txt)

    def teste_calculo_das_dimensoes_do_trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        variaveis = _trafo.inicia_as_variaveis(VARIAVEIS, json_variables)
        _trafo.calculo_das_perdas_do_trafo(variaveis, debug=True)

        tests_variables = _trafo.resultado_calculos
        not_pass = {}
        for key, value in tests_variables.items():
            try:
                y = json_variables[key]

                if key in []:
                    if not erro_e_aceitavel(
                        value,
                        json_variables[key],
                        self.error_aceitavel * 1000000,
                    ):
                        not_pass[key] = [
                            value,
                            f"é diferente de {json_variables[key]}",
                        ]

                    continue
                if key in []:
                    if not erro_e_aceitavel(
                        value, y, self.error_aceitavel * 20
                    ):
                        r = abs((value - y) / value)
                        not_pass[key] = [
                            value,
                            f"é diferente de {y}. Erro de {r * 100} %",
                        ]

                    continue

                if not erro_e_aceitavel(
                    value, json_variables[key], self.error_aceitavel
                ):
                    r = abs((value - y) / value)
                    not_pass[key] = [
                        value,
                        f"é diferente de {y}. Erro de {r * 100} %",
                    ]
            except:
                not_pass[key] = [value, "não existe no JSON " + self.filename]

            if key == "atc":
                ...

        msg = print_dict(not_pass, " -> ")
        txt = "Erros encontrados ao executar o teste do calculo das dimenções do trafo. "
        txt += "Os erros foram: [{}]".format(msg)

        self.assertDictEqual(not_pass, {}, txt)

    def teste_resultado_calculos_a_partir_do_atributo_no_objeto_Trafo(self):
        json_variables = load(open(self.pathjson + self.filename, "r"))
        _trafo = trafo.Trafo(json_variables)
        _trafo.calculo_de_dados_do_trafo()
        tests_variables = _trafo.resultado_calculos
        not_pass = {}

        for key, value in tests_variables.items():
            sucesso = value == json_variables[key]
            if not sucesso:
                not_pass[key] = [value, json_variables[key]]

        msg = print_dict(not_pass, " != ")

        txt = "Alguns do calculos não estão corretos. Os valores sao: [{}]".format(
            msg
        )
        self.assertDictEqual(not_pass, {}, txt)
