from typing import Dict, List
from math import sqrt, pi, cos, sin
import numpy as np

import os, sys
sys.path.append(os.getcwd())

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

    def __init__(self, constantes: Dict) -> None:
        self.constantes = self.inicia_as_variaveis(CONSTANTES_DADAS, constantes)
        self.resultado_calculos = utils.QueryDict({})

        # self.calculo_de_dados_do_trafo() 
        # self.calculo_das_dimensoes_do_trafo()
    
    def __repr__(self):
        txt = ", ".join([(f"{i} = {self.constantes[i]}") for i in self.constantes.keys()])
        return f"Trafo ({txt})"


    def inicia_as_variaveis(self, nomes: Dict, items: [Dict]) -> Dict:
        # import ipdb; ipdb.set_trace()
        retorno = utils.QueryDict({})
        for nome in nomes.keys():
            try:
                retorno[nome] = items[nome]
            except KeyError as e:
                raise KeyError(f'"Erro ao iniciar as variáveis: "{nome}" nao existe no dicionário "items" \n')
            except Exception as e:
                raise ValueError(f"Erro desconhecido ocorrido na classe Trafo: {e}")
        return retorno

    
    @staticmethod
    def set_variaveis(variaveis: List):
        retorno = [{i: j} for i, j in zip(VARIAVEIS.keys(), variaveis)]
        return retorno

    def calculo_de_dados_do_trafo(self):
        conexao:list = self.constantes["conexao"].split("-")
        # from ipdb import set_trace; set_trace()
        secundario, primario = conexao
        # import ipdb; ipdb.set_trace()
        V1 = self.constantes["V1"]
        V2 = self.constantes["V2"]

        Vf1, Vf2 = V1, V2

        if primario.lower() == "estrela": Vf1 = V1 / sqrt(3)
        if secundario.lower() == "estrela": Vf2 = V2 / sqrt(3)

        para_teste = {
            "Vf1": Vf1,
            "Vf2": Vf2
        }
        self.resultado_calculos.update(para_teste)

    def run(self, variaveis: dict, penalidade: bool=False, **kw) -> (float, float):
        # import ipdb; ipdb.set_trace()
        # assert VARIAVEIS.keys() == variaveis.keys()

        return self.calculo_das_perdas_do_trafo(variaveis, penalidade=penalidade)

    def calculo_das_perdas_do_trafo(self, variaveis: [dict, List], penalidade=False, debug: bool = False):
        Vf1 = self.resultado_calculos.Vf1
        Vf2 = self.resultado_calculos.Vf2
        
        # constantes
        S = self.constantes["S"]
        f = self.constantes["f"]
        Ke = self.constantes["Ke"] 
        tipo = self.constantes["tipo"]
        Dfe = self.constantes["Dfe"]
        Dal = self.constantes["Dal"]
        
        # variaveis
        try: 
            Jbt = variaveis["Jbt"]
            Jat = variaveis["Jat"]
            Bm = variaveis["Bm"]
            Ksw = variaveis["Ksw"]
            kt = variaveis["kt"]
            Rjan = variaveis["Rjan"]
            rel = variaveis["rel"]
        except: 
            # import ipdb; ipdb.set_trace()
            Jbt, Jat, Bm, Ksw, kt, Rjan, rel = variaveis

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

        # import ipdb; ipdb.set_trace()

        # x = (Ac * 4 / pi) ** .5 # TODO talvez vamos calcular d usando d como o diametro de Ac
        Kw = Ksw / (30 + Vf2)   #   TODO Kw deveria vir da tabela 2.1.
                                # na equação 2.26 usa esse Kw e diz que ele é definido na tabela 2.1

        Aw = S /(3.33 * f * Ac * Bm * Kw * Jbt) * 1e9 # é a área da janela em [mm²]. Ac esta em [mm²]
        
        ww = sqrt(Aw / Rjan)    # TODO essa equação não está na tese. Olhar a página 50

        hw = Aw / ww            # é a altura da janela [m]

        wc = L[0]               # é a maior largura da coluna do núcleo do transformador [m]
        D = ww + wc             # é a distância entre os centros de duas colunas [m]
        W = 2 * D + wc          # é a largura total do núcleo [m]

        # a = (d - wc) / 2
        # Estimativa da corrente de carga
        Abj = rel * Abc     # é a área bruta da culatra [mm²]
        Aj = rel * Ac       # é a área do jugo ou da culatra [mm²]
        hy = Abj / Prof     # é a altura da culatra [mm]
        By = Bm / rel       # densidade de fluxo no jugo (yoke)
                            # TODO entender o que é isso

        # H = hw + 2 * hy     # é a altura total do núcleo [m]
        Vferc = 3 * hw * Ac # Volume de ferro no núcleo [mm³]
        Bfe = Dfe * 1e-9    # Densidade do ferro em [Kg / mm³]
        Mc = Vferc * Bfe    # Massa da culatra  [Kg]

        # import ipdb; ipdb.set_trace()
        #TODO realizar os testes a partir daqui
        
        Pic = tabelas.perda_magnetica_do_nucleo(Bm) #Perda magnética [W/Kg]
        # FIXME Bm nao pode ser superior a 1.85, caso contrario a interpolação resultará em null
        
        assert isinstance(Pic, int) or isinstance(Pic, float) 

        Wic = Pic * Mc          # perda específica no núcleo [W]
        Vferj = Aj * W * 2      # é o volume do ferro nas culatras
        Mj = Vferj * Bfe
        MT = Mj + Mc            # Massa total do Trafo [Kg]

        Pij = tabelas.perda_magnetica_do_nucleo(By) # é a perda magnética específica da densidade de fluxo magnético na culatra [W/kg]
        assert isinstance(Pij, int) or isinstance(Pij, float)
        Wij = Pij * Mj
        Po = (Wic + Wij) * 1.05     # Perdas totais do ferro no transformador. 
                                    # As perdas totais é a soma da perda nas colunas 
                                    # + as perdas nas culatras (culatras e guarnições)
        Ip = Po/(3 * Vf1) * 1e-3    # Componente da corrente ativa Ip da perda no núcleo [A]

        atc = tabelas.curva_BH(Bm)
        atj = tabelas.curva_BH(By)
        
        ATj = 2 * W * atj   # A força magnetomotriz na culatra [Ae]
        ATc = 3 * hw * atc  # A força magnetomotriz na coluna [Ae]

        ATcj = ATc + ATj        # A força magnetomotriz total [Ae]
        Iq = ATcj / N1 * 1e-3   # N1 enrolamento do lado da BT conforme trafo WEG DE 150 KVA

        # Io = sqrt(Ip ** 2 + Iq ** 2) # A corrente a vazio [A]
        # import ipdb; ipdb.set_trace()

        I1 = S / 3 / Vf1   # FIXME S é a potencia total do Trafo
        Fc1 = I1 / Jbt
        Swind1 = Fc1 * N1
        z = (hw * Kw) * 2
        hb = (hw - z) * 1.11
        tbt1 = Swind1/ hb * 1.1     # 10% de folga
        tbt2 = tbt1 * 2

        Dextbt = tbt2 + d           # diametro em mm
        dmbt = (Dextbt + d) / 2     # diâmetro médio na baixa tensão em milímetros
        Lmbt = pi * dmbt            # Comprimento médio em mm
        Compbt1 = Lmbt * N1         # Comprimento do fio na baixa tensão
        #dfc1 = sqrt(4 * Fc1 / pi)
        VALbt = Compbt1 * Fc1 * 3

        Mbt3 = VALbt * Dal * 1e-9
        # I2menor = (S / 3 / Vf2)     # corrente no secundário

        Vmedio2 = 12                # TODO pergutar ao professor se esse valor deve ser dado do usuário
        I2c = S / 3 / Vmedio2       # tap intermediário para dimensionamento dos condutores
        
        Fc2AT = I2c / Jat           # área do condutor em mm2 no secundário
        # dfc2AT  = sqrt(Fc2AT * 4 / pi)  # Diametro do condutor em mm
        SwindAT = Fc2AT * N2            # Area referente a alta tensao
        # dAt = sqrt(SwindAT * 4 / pi)

        tAT1 = SwindAT / hb * 1.1
        # Laxju = hw - hw * Kw / 2

        # tAT2 = tAT1 * 2

        dintAT = Dextbt + 6 * (d - wc) / 2
        DextAT = dintAT + 4 * tAT1

        LmATc = pi * (dintAT + DextAT) / 2              # Comprimento em milímetros
        CompAT = LmATc * N2

        # dfc2 = sqrt(I2c / Jat * 4 / pi)
        VALAT = CompAT * I2c / Jat * 3
        MAT3 = VALAT * Dal * 1e-9
        
        R1 = 0.02857 * Compbt1 / Fc1 * 1e-3     # Resistencia do cobre no lado da baixa tesão
        R2 = 0.02857 * CompAT / Fc2AT * 1e-3    # Resistencia do cobre no lado da alta tesão

        I2 = S / 3 / Vf2
        Pj = (R1 * I1 ** 2 + R2 * I2 ** 2) * 3
        PerdasT = Po + Pj
        Mativa = MAT3 + Mbt3 + MT
        # import ipdb; ipdb.set_trace()
        # Mativa *= 3
        # assert isinstance(penalidade, int)
        if penalidade == 1:
            Fc = np.sqrt(Po / Pj)
            
            #O trafo deve respeitar as restrições de desigualdade pg 82 da tese
            Perda_max = 2000
            Mativa_max = 610
            Fc_max = 0.6
            f_multiplicativo_perdas = 100
            f_multiplicativo_massas = 50
            f_multiplicativo_fc = 700
            
            f1, f2 = PerdasT, Mativa
            
            
            if PerdasT > Perda_max:
                
                f1 = f1 + abs(PerdasT - Perda_max) * f_multiplicativo_perdas + Perda_max
                f2 = f2 + abs(Mativa - Mativa_max) * f_multiplicativo_massas + Mativa_max
                
            
            if Mativa > Mativa_max:
                f1 = f1 + abs(PerdasT - Perda_max) * f_multiplicativo_perdas + Perda_max
                f2 = f2 + abs(Mativa - Mativa_max) * f_multiplicativo_massas + Mativa_max
            
            if Fc > Fc_max:
                f1 = f1 + abs(Fc - Fc_max) * f_multiplicativo_fc + Perda_max
                f2 = f2 + abs(Fc - Fc_max) * f_multiplicativo_fc + Mativa_max
                # import ipdb; ipdb.set_trace(context=30)
                
            PerdasT, Mativa = f1, f2
            
            return np.array([PerdasT, Mativa], dtype=np.float64)

        if debug:
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
                # "H": H,
                "Pic": Pic,
                "Pij": Pij,
                "Wic": Wic,
                "Vferj": Vferj,
                "Mj": Mj,
                "MT": MT,
                "Wij": Wij,
                "Po": Po,
                "Ip": Ip,
                
                "atc": atc,
                "atj": atj,
                "ATc": ATc,
                "ATj": ATj,
                "ATcj": ATcj,
                "Iq": Iq,
                # "Io": Io,
                "I1": I1,
                "Fc1": Fc1,
                "Swind1": Swind1,
                "z": z,
                "hb": hb,
                "tbt1": tbt1,
                "tbt2": tbt2,

                "Dextbt": Dextbt,
                "dmbt": dmbt,
                "Lmbt": Lmbt,
                "Compbt1": Compbt1,
                "VALbt": VALbt,
                "Mbt3": Mbt3,
                "I2c": I2c,
                "Vmedio2": Vmedio2,
                "Fc2AT": Fc2AT,
                "SwindAT": SwindAT,
                # "dAt": dAt,
                # "I2menor": I2menor,
                # "dfc2AT":  dfc2AT,
                # "Laxju": Laxju,
                # "tAT2": tAT2

                "dintAT": dintAT,
                "DextAT": DextAT,
                "LmATc": LmATc,
                "CompAT": CompAT,
                # "dfc2": dfc2,
                "VALAT": VALAT,
                "MAT3": MAT3,
                "R1": R1,
                "R2": R2,
                "I2": I2,
                "Pj": Pj,
                # "PerdasT": PerdasT,
                # "Mativa": Mativa,                
            }
            
            #para_teste.update(teste)
            
            # para_teste = {
            #     "Pic": Pic,
            # }
            # import ipdb; ipdb.set_trace()

            self.resultado_calculos.update(para_teste)
        
        return np.array([PerdasT, Mativa], dtype=np.float64)

def faz_nada():
        R2ref = R2 * (N1 / N2) ** 2
        VmL = V1 * 1000 * sqrt(2)
        Fluxonominal2 = Vf1 * 1000 / (2 * pi * f) * sqrt(2)
        VmAT = V2 * 1000 * sqrt(2)
        FluxonominalAT = Vf2 * 1000 / (2 * pi * f) * sqrt(2)

        Ac = Ac * 1e-6          # converte para m²

        Fr = Ac * Br            # Fluxo em [Wb/m²]
        Fs = Ac * Bs            # Fluxo em [Wb/m²]

        VAc = tabelas.curva_VA(Bm)
        VAj = tabelas.curva_VA(By)
        S0 = VAc * Mc + VAj* Mj

        Rm = Po / 3 / Io ** 2
        Zm = Vf1 * 1000 / Io
        Xm0 = sqrt(Zm ** 2 - Rm ** 2)
        IoAT = Io * N1 / N2
        RmAT = Po / 3 / IoAT ** 2
        ZmAT = Vf2 * 1000 / IoAT
        Xm0AT = sqrt(ZmAT ** 2 - RmAT ** 2)

        Mo = 4 * pi * 1e-7   # 9Permeabilidade do ar
        Wa = 2 * pi * f
       
        L = Mo * N1 ** 2 * So / (hb - 0.45 * dc)  # TODO buscar essa referencia. Indutância: Hayt J.r,W.A Buck J.A 2013 - Eletromagnetismo
        Xb = Wa * L / 1000

        Zb = sqrt(R1 ** 2 + Xb ** 2)
        
        ktrafo = Vf2 / Vf1
        XA = Xb * ktrafo ** 2
        ZA = sqrt(R2 ** 2 + XA ** 2)

        Zccb = Zb + ZA / ktrafo ** 2
        Ifb = S / 3 / Vf1
        Vccb = Ifb * Zccb
        
        Zp = Vccb / Vf1 /1000 * 100

        IfA = S / 3 / Vf2

        ZbaseA = V2 ** 2 * 3 * 1000 / S

        ZA = ZbaseA * Zp / 100 / 2
        XA = sqrt(ZA ** 2 - R2 ** 2)
        import ipdb; ipdb.set_trace()
        #  TODO realizar os testes e calcular os pesos dos condutores de alumínio pg 
        

        teste = {
            "L": L,
            "Xb": Xb,
            "Mo": Mo,
            "Wa": Wa,
            "ktrafo": ktrafo,
            "Zb": Zb,
            "ZA": ZA,
            "XA": XA,
            "R1": R1,
            "R2": R2,
            "Zccb": Zccb,
            "Ifb": Ifb,
            "Vccb": Vccb,
            "Zp": Zp,
            "IfA": IfA,
            "ZbaseA": ZbaseA,
        }

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
            "Pic": Pic,
            "Pij": Pij,
            "Wic": Wic,
            "Vferj": Vferj,
            "Mj": Mj,
            "MT": MT,
            "Wij": Wij,
            "Po": Po,
            "Ip": Ip,
            
            "atc": atc,
            "atj": atj,
            "ATc": ATc,
            "ATj": ATj,
            "ATcj": ATcj,
            "Iq": Iq,
            "Io": Io,
            "I1": I1,
            "Fc1": Fc1,
            "Swind1": Swind1,
            "z": z,
            "hb": hb,
            "tbt1": tbt1,
            "tbt2": tbt2,

            "Dextbt": Dextbt,
            "dmbt": dmbt,
            "Lmbt": Lmbt,
            "Compbt1": Compbt1,
            "VALbt": VALbt,
            "Mbt3": Mbt3,
            "I2c": I2c,
            "Vmedio2": Vmedio2,
            "Fc2AT": Fc2AT,
            "SwindAT": SwindAT,
            "dAt": dAt,
            "I2menor": I2menor,
            "dfc2AT":  dfc2AT,
            "Laxju": Laxju,
            # "tAT2": tAT2

            "dintAT": dintAT,
            "DextAT": DextAT,
            "LmATc": LmATc,
            "CompAT": CompAT,
            "dfc2": dfc2,
            "VALAT": VALAT,
            "MAT3": MAT3,
            "R1": R1,
            "R2": R2,
            "I2": I2,
            "Pj": Pj,

            "R2ref": R2ref,
            "Fluxonominal2": Fluxonominal2,
            "VmAT": VmAT,
            "VmL": VmL,
            "FluxonominalAT": FluxonominalAT,

            "Fr": Fr,
            "Fs": Fs,
            "VAc": VAc,
            "VAj": VAj,
            "S0": S0,
            "VAj": VAj,
            "Rm": Rm,
            "Xm0": Xm0,
            "IoAT": IoAT,
            "Xm0AT": Xm0AT,

        }
        
        para_teste.update(teste)
        
        # para_teste = {
        #     "Pic": Pic,
        # }
        # import ipdb; ipdb.set_trace()

        self.resultado_calculos.update(para_teste)

if __name__ == "__main__":
    x = {"x":[1.3021543128344217,1.5635255416644525,1.5794831416883455,6.6443181301936916,0.48786093826602683,3.5623160916564953,1.1532825588799454],"z":235.72047565797871,"n":7,"J1":1.3021543128344217,"J2":1.5635255416644525,"Bm":1.5794831416883455,"Ksw":6.6443181301936916,"kt":0.48786093826602683,"Rjan":3.5623160916564953,"rel":1.1532825588799454,"Jbt":1.3021543128344217,"Jat":1.5635255416644525,"Ke":0.945,"k":0.505,"Ku":0.923,"Bs":1.8,"Br":1.2,"f":60,"Dfe":7650,"V1":0.22,"V2":13.8,"Vf1":0.12701705922171769,"Vf2":13.8,"Vmedio2":12,"Q":150.00000000000003,"Qf":50,"Et":5.9750518209360495,"N1":21.257900856468094,"N2":2309.6033998644211,"conexao":"delta-estrela","Ac":14200.134594495996,"Abc":15023.496285398611,"So":16280.170589916701,"dc":143.97415389616404,"S":150,"Nfases":3,"constantes":[150,60,3],"tipo":"seco","L1":138.07121358642132,"L2":125.97738465914354,"L3":110.57215019225399,"L4":92.143458493544983,"L5":69.539516331847224,"L6":40.4567372448221,"teta1":0.28734394299515853,"teta2":0.50536051028415729,"teta3":0.69508385432977249,"teta4":0.87629806116834064,"teta5":1.0667186967433886,"teta6":1.2859603924440046,"e1":20.401574503510474,"e2":14.449019266748714,"e3":11.253518280559966,"e4":9.2089516117657411,"e5":7.7202859597560547,"e6":6.0532073218644626,"Prof":138.17311388841082,"d":167.68744259765717,"wc":138.07121358642132,"a":14.808114505617922,"Proffem":108.80976486814993,"Kw":0.15169676096332629,"Aw":169453.11546824532,"Acm2":0.014200134594495996,"Awm2":0.16945311546824532,"ww":218.10144986280284,"hw":776.9463044598748,"D":356.17266344922416,"W":850.41654048486964,"Abj":17326.336239347864,"Aj":16376.767561579978,"hy":125.39585851224778,"By":1.3695543468743003,"H":1027.7380214843704,"Vferc":3.3098226288079463E+7,"Bfe":7.6500000000000013E-6,"Mc":253.20143110380795,"Pic":1.1767627,"Wic":297.958,"Vferj":2.7854148028087359E+7,"Mj":213.08423241486832,"MT":466.2856635186763,"Pij":0.84900862,"Wij":180.910355,"PESOTOTAL":466.2856635186763,"Po":502.811768,"Ip":1.31953871,"atc":58.1432,"ATc":135522.438,"atj":32.4908447,"ATj":55261.5039,"ATcj":190783.938,"ATT":190783.938,"Iq":8.97473049,"Io":9.07121658,"Fpocalculado":0.145464361,"I1":393.64791081110843,"Fc1":302.30511616879591,"dfc1":19.619042496561043,"Swind1":6426.3721879193336,"hb":600.76066997010469,"tbt1":11.766764637011006,"tbt2":23.533529274022012,"Dextbt":191.22097187167918,"dmbt":179.45420723466816,"Lmbt":563.77333744843349,"Compbt1":11984.637712998931,"VALbt":1.0869051888207221E+7,"Mbt3":29.346440098159498,"I2menor":3.6231884057971011,"I2c":4.166666666666667,"Fc2AT":2.6649175569150207,"dfc2AT":1.8420310575349219,"SwindAT":6154.902649809319,"dAt":88.524942517532665, "Dal": 2.7e-6}
    from time import time

    t0 = time()
    t1 = Trafo(x)
    t2 = Trafo(x)
    
    
    print(t1)

