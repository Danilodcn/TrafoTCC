from typing import Dict

try: 
    from Utils import utils
except Exception as e: 
    print(f"O erro foi:  {e}")
    from Utils import utils
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
    
    def __repr__(self):
        txt = ", ".join([(f"{i} = {self.variaveis[i]}") for i in self.variaveis.keys()])
        return f"Trafo ({txt})"


    @staticmethod
    def inicia_as_variaveis(nomes: Dict, items: Dict) -> Dict:
        retorno = utils.QueryDict({})
        for nome in nomes.keys():
            try:
                retorno[nome] = items[nome]
            except KeyError as e:
                raise KeyError(f'"Erro ao iniciar as variáveis: "{nome}" nao existe no dicionário "items" \n')
            except Exception as e:
                raise ValueError(f"Erro desconhecido ocorrido na classse Trafo: {e}")
        return retorno

    def algum_calculo(self):
        ...
