import os
from json import load
from unittest import TestCase

try:
    from AG.Populacao import VARIAVEIS
    from AG.Individuo import Individuo
    from Trafo.CONSTANTES import VARIACOES, CONSTANTES_DADAS
    from Trafo.trafo import Trafo

except ImportError as error:
    print(f"Erro no import em {__name__}: {error}")
    #import ipdb; ipdb.set_trace()
    from .AG.Individuo import Individuo
    from .Trafo.trafo import Trafo

try:
    from .utils import erro_e_aceitavel, print_dict
except:
    from utils import erro_e_aceitavel, print_dict


class Teste_AG_Criação_Individuo(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + f"teste_{self.config['n']}.json"
        self.json = load(open(self.teste))
        variaveis = self.json["variaveis"]
        self.variaveis = dict(zip(VARIACOES.keys(), variaveis))
        self.erro_aceitavel = self.config["error"]
    
    def test_cria_individuo(self):
        try:
            ind = Individuo(variacoes=VARIACOES)
            ind_ = Individuo(self.variaveis)
            # import ipdb; ipdb.set_trace()
        except Exception as e:
            msg = f"{__name__} >> Erro na criação do indivíduo: {e}"
            self.assertTrue(False, msg)

    def test_calculo_dos_objetivos(self):
        ind = Individuo(self.variaveis)
        # import ipdb; ipdb.set_trace()
        ind.set_constantes_trafo(self.json)
        # x = Individuo.trafo.inicia_as_variaveis(CONSTANTES_DADAS, self.json)
        # Individuo.trafo.calculo_de_dados_do_trafo()
        perdas_totais, massa_ativa = ind.calcula_objetivo()

        real_massa_ativa = self.json["Mativa"]
        real_perdas_totais = self.json["PerdasT"]

        texto = "Houve um erro no cálculo em {}, {} != {}. Erro de {}%"
        self.assertTrue(
            erro_e_aceitavel(massa_ativa, real_massa_ativa, self.erro_aceitavel), 
            texto.format(
                __name__, 
                massa_ativa, 
                real_massa_ativa, 
                round(
                    (massa_ativa - real_massa_ativa) / real_massa_ativa) * 100, 3
                )
            )
        
        self.assertTrue(
            erro_e_aceitavel(perdas_totais, real_perdas_totais, self.erro_aceitavel), 
            texto.format(
                __name__, 
                perdas_totais, 
                real_perdas_totais, 
                round((perdas_totais - real_perdas_totais) / real_perdas_totais * 100), 3
                )
            )
        # import ipdb; ipdb.set_trace()

class Teste_AG_Individuo(TestCase):
    def setUp(self):
        self.pathjson = "tests/json/AG/"
        self.config = load(open("tests/config.json", "r"))
        self.teste = self.pathjson + f"teste_{self.config['n']}.json"
        self.json = load(open(self.teste))
        variaveis = self.json["variaveis"]
        self.variaveis = dict(zip(VARIACOES.keys(), variaveis))
        self.erro_aceitavel = self.config["error"]

        self.individuo = Individuo(self.variaveis)
        self.individuo.set_constantes_trafo(self.json)

    def teste_crossover(self):
        import ipdb; ipdb.set_trace()
        individuos = [Individuo(variacoes=VARIACOES) for i in range(3)]
        i1, i2, i3 = individuos

        print(individuos)
    