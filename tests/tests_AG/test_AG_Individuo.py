import os
from json import load
from unittest import TestCase

try:
    from AG.Populacao import VARIAVEIS
    from AG.Individuo import Individuo
    from AG.funcoes import verifica_dominancia, e_dominado
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
    
    def teste_cria_individuo(self):
        try:
            ind = Individuo(variacoes=VARIACOES)
            ind_ = Individuo(self.variaveis, variacoes=VARIACOES)
            # import ipdb; ipdb.set_trace()
        except Exception as e:
            msg = f"{__name__} >> Erro na criação do indivíduo: {e}"
            self.assertTrue(False, msg)

    def teste_calculo_dos_objetivos(self):
        ind = Individuo(self.variaveis, variacoes=VARIACOES)
        # import ipdb; ipdb.set_trace()
        ind.set_constantes_trafo(self.json, CONSTANTES_DADAS)
        # x = Individuo.trafo.inicia_as_variaveis(CONSTANTES_DADAS, self.json)
        # Individuo.trafo.calculo_de_dados_do_trafo()
        perdas_totais, massa_ativa = ind.calcular_objetivos()

        real_massa_ativa = self.json["Mativa"]
        real_perdas_totais = self.json["PerdasT"]

        # ind = Individuo(variacoes=VARIACOES)
        # perda, massa = ind.calcula_objetivo()
        # import ipdb; ipdb.set_trace()
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

        self.individuo = Individuo(self.variaveis, variacoes=VARIACOES)
        self.individuo.set_constantes_trafo(self.json, CONSTANTES_DADAS)

    def teste_crossover_aritmético(self):
        # import ipdb; ipdb.set_trace()
        individuos = [Individuo(variacoes=VARIACOES) for i in range(3)]
        i1, i2, i3 = individuos
        # x = [1.233292088175284,1.524191728787062,1.557370976484120,6.052077890285870,0.543120138460825,3.545732336335654,1.173784165379759]
        # i = Individuo(variaveis=x, variacoes=VARIACOES)        
        # import ipdb; ipdb.set_trace()

        filho_1_2 = i1.crossover_aritmetico(i2)
        filho_1_3 = i1.crossover_aritmetico(i3)
        filho_2_1 = i2.crossover_aritmetico(i1)
        filho_2_3 = i2.crossover_aritmetico(i3)
        filho_3_1 = i3.crossover_aritmetico(i1)
        filho_3_2 = i3.crossover_aritmetico(i2)
        
        self.assertIsNotNone(filho_1_2)
        self.assertIsNotNone(filho_1_3)
        self.assertIsNotNone(filho_2_1)
        self.assertIsNotNone(filho_2_3)
        self.assertIsNotNone(filho_3_1)
        self.assertIsNotNone(filho_3_2)
        
    def teste_crossover_heuristico(self):
        # import ipdb; ipdb.set_trace()
        individuos = [Individuo(variacoes=VARIACOES) for i in range(3)]
        i1, i2, i3 = individuos
        # x = [1.233292088175284,1.524191728787062,1.557370976484120,6.052077890285870,0.543120138460825,3.545732336335654,1.173784165379759]
        i = Individuo(variaveis=None, variacoes=VARIACOES)        
        # import ipdb; ipdb.set_trace()

        filho_1_2 = i1.crossover_heuristico(i2)
        filho_1_3 = i1.crossover_heuristico(i3)
        filho_2_1 = i2.crossover_heuristico(i1)
        filho_2_3 = i2.crossover_heuristico(i3)
        filho_3_1 = i3.crossover_heuristico(i1)
        filho_3_2 = i3.crossover_heuristico(i2)
        
        self.assertIsNotNone(filho_1_2)
        self.assertIsNotNone(filho_1_3)
        self.assertIsNotNone(filho_2_1)
        self.assertIsNotNone(filho_2_3)
        self.assertIsNotNone(filho_3_1)
        self.assertIsNotNone(filho_3_2)
        
    def teste_função_de_dominacia(self):
        i1 = [1.21042245, 1.55302933, 1.58285085, 6.03063618, 0.46366941, 3.46164068, 1.15117212]
        i2 = [1.35239765, 1.51491666, 1.55278227, 6.27495765, 0.49484197, 3.43497921, 1.12710451]
        i1 = Individuo(variaveis=i1, variacoes=VARIACOES)
        i2 = Individuo(variaveis=i2, variacoes=VARIACOES)
        # Individuo (Jbt = 1.352, Jat = 1.515, Bm = 1.553, Ksw = 6.275, kt = 0.495, Rjan = 3.435, rel = 1.127 
        # (objetivo = [1866.35443328  548.68636667]))
        _, domina = verifica_dominancia(i1, i2)
        assert_ = domina[0] == i2
        self.assertTrue(assert_)
        
        # import ipdb; ipdb.set_trace()
    
    def teste_mutacao_do_individuo(self):
        # import ipdb; ipdb.set_trace()
        # x = [1.233292088175284,1.524191728787062,1.557370976484120,6.052077890285870,0.543120138460825,3.545732336335654,1.173784165379759]
        i = Individuo(variaveis=None, variacoes=VARIACOES)        
        
        filho = i.mutacao_uniforme(.3)
        self.assertIsNotNone(filho)
        
        import ipdb; ipdb.set_trace()