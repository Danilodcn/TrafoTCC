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
        tipo = self.constantes.tipo
        Dfe = self.constantes.Dfe


        # variaveis 
        Bm = self.variaveis.Bm
        kt = self.variaveis.kt
        Rjan = self.variaveis.Rjan
        Ksw = self.variaveis.Ksw
        Jbt = self.variaveis.Jbt
        rel = self.variaveis.rel


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
        
        k = tabelas.tabela_2_5(tipo, numero_degraus)
        d = sqrt(Ac / k)

        Kw = Ksw / (30 + Vf2)   #   TODO Kw deveria vir da tabela 2.1.
                                # na equação 2.26 usa esse Kw e diz que ele é definido na tabela 2.1

        Aw = S /(3.33 * f * Ac * Bm * Kw * Jbt) * 1e9 # é a área da janela em [mm²]. Ac esta em [mm²]
        
        ww = sqrt(Aw / Rjan)    # TODO essa equação não está na tese. Olhar a página 50

        hw = Aw / ww            # é a altura da janela [m]

        wc = L[0]               # é a maior largura da coluna do núcleo do transformador [m]
        D = ww + wc             # é a distância entre os centros de duas colunas [m]
        W = 2 * D + wc          # é a largura total do núcleo [m]

        # import ipdb; ipdb.set_trace()
        
        # Estimativa da corrente de carga
        Abj = rel * Abc     # é a área bruta da culatra [mm²]
        Aj = rel * Ac       # é a área do jugo ou da culatra [mm²]
        hy = Abj / Prof     # é a altura da culatra [mm]
        By = Bm / rel       # densidade de fluxo no jugo (yoke)
                            # TODO entender o que é isso

        H = hw + 2 * hy     # é a altura total do núcleo [m]
        Vferc = 3 * hw * Ac # Volume de ferro no núcleo [mm³]
        Bfe = Dfe * 1e-9    # Densidade do ferro em milímetros
        Mc = Vferc * Bfe

        #TODO realizar os testes a partir daqui

        para_teste = {
            "Et": Et,
            "N1": N1,
            "N2": N2,
            "Ac": Ac,
            "Abc": Abc,
            "So": So,
            "Ku": Ku,
            "dc": dc,
            "Prof": Prof,
            "k": k,
            "d": d,
            "Kw": Kw,
            "Aw": Aw,
            "ww": ww,
            "hw": hw,
            "wc": wc,
            "D": D,
            "W": W,
            "Abj": Abj,
            "Aj": Aj,
            "hy": hy,
            "By": By,
            "Vferc": Vferc,
            "Bfe": Bfe,
            "Mc": Mc,
            "H": H,

        }
        # para_teste = {
        #     "Prof": Prof
        # }
        self.resultado_calculos.update(para_teste)
        
