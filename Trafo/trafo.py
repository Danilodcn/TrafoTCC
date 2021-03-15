from typing import Dict
from math import sqrt, pi, cos, sin
import numpy as np


try: 
    from Utils import utils, tabelas
except Exception as e: 
    print(f"O erro foi:  {e}")
    from .Utils import utils, tabelas
try: 
    from .CONSTANTES import CONSTANTES_DADAS, VARIAVEIS
except: 
    from CONSTANTES import CONSTANTES_DADAS, VARIAVEIS

class TrafoError(Exception): pass



class Trafo(object):

    def __init__(self, cons: Dict, variaveis: Dict) -> None:
        self.variaveis = self.inicia_as_variaveis(VARIAVEIS, variaveis)
        self.constantes = self.inicia_as_variaveis(CONSTANTES_DADAS, cons)
        self.resultado_calculos = utils.QueryDict({})

        # self.calculo_de_dados_do_trafo()
        # self.calculo_das_dimensoes_do_trafo()
    
    def __repr__(self):
        txt = ", ".join([(f"{i} = {self.variaveis[i]}") for i in self.variaveis.keys()])
        return f"Trafo ({txt})"


    @staticmethod
    def inicia_as_variaveis(nomes: Dict, items: Dict) -> Dict:
        # import ipdb; ipdb.set_trace()
        retorno = utils.QueryDict({})
        for nome in nomes.keys():
            try:
                retorno[nome] = items[nome]
            except KeyError as e:
                raise KeyError(f'"Erro ao iniciar as variáveis: "{nome}" nao existe no dicionário "items" \n')
            except Exception as e:
                raise ValueError(f"Erro desconhecido ocorrido na classse Trafo: {e}")
        return retorno

    def calculo_de_dados_do_trafo(self):
        conexao:list = self.constantes.conexao.split("-")
        # from ipdb import set_trace; set_trace()
        secundario, primario = conexao

        V1 = self.constantes.V1
        V2 = self.constantes.V2

        Vf1, Vf2 = V1, V2

        if primario.lower() == "estrela": Vf1 = V1 / sqrt(3)
        if secundario.lower() == "estrela": Vf2 = V2 / sqrt(3)

        para_teste = {
            "Vf1": Vf1,
            "Vf2": Vf2
        }
        self.resultado_calculos.update(para_teste)

    def get_variavel(self, item: str):
        try:
            return self.variaveis[item]
        except:
            try: 
                return self.constantes[item]
            except:
                raise KeyError(f'A variável "{item}" nao existe')


    def calculo_das_dimensoes_do_trafo(self):
        Vf1, Vf2 = self.resultado_calculos.Vf1,  self.resultado_calculos.Vf2
        
        # constantes
        S = self.constantes.S
        f = self.constantes.f
        Ke = self.constantes.Ke 

        # variaveis 
        Bm = self.variaveis.Bm
        kt = self.variaveis.kt


        Et = kt * sqrt(S) #  é a tensão eficaz por espiras [V/e]
        N1 = (Vf1 * 1000) / Et
        N2 = (Vf2 * 1000) / Et
        

        Ac = Et / (4.44 * f * Bm) * 1e6         # é a área efetiva da coluna  [mm2]
        Abc = Ac / Ke                           #  é a área bruta da coluna [mm2]
        numero_degraus = tabelas.tabela_2_3(Abc / 1000) # numero de degraus conforme a tabela 2.3 pg 44 tese
        Ku, LD = tabelas.tabela_2_4(numero_degraus)     # Dimensões do núcleo em função do número de degraus. pg 48 tese
        LD = np.asarray(LD, np.float64)                 # LD é um vetor que contem todos os valores existentes na tabela 2.4


        So = Abc / Ku                           # Seção circular circunscrita
        dc = 2 * sqrt(So / pi)                  #  é o diâmetro da coluna do núcleo
        
        L = LD * dc
        teta = np.arccos(LD)

        # Calculo da profundidade do núcleo [n]
        e = [np.sin(teta[0]) * dc / 2]
        for i, _ in enumerate(teta[1:]):
            x = np.sin(teta[i+1]) * dc / 2 - sum(e)
            e.append(x)
        
        Abc = np.sum(L * np.asarray(e, np.float64)) * 2

        Prof = np.sum(e) * 2            #é a profundidade total do núcleo do transformador
        # import ipdb; ipdb.set_trace()
        

        para_teste = {
            "Et": Et,
            "N1": N1,
            "N2": N2,
            "Ac": Ac,
            "Abc": Abc,
            "So": So,
            "Ku": Ku,
            "dc": dc,
            "Prof": Prof
        }
        # para_teste = {
        #     "Prof": Prof
        # }
        self.resultado_calculos.update(para_teste)
        
