

% Adelicio Maximiano Sobrinho, Juliana Almansa Malagoli, José Roberto
% Camacho
% Exercício Teste 1 
% Projeto de um transformador monofásico , tipo núcleo envolvido
% as seguintes especificações
% Potência 50KVAA, Relações de tensões 220/13.8
%
% Equação de saída pag 375 livro - DESIGN OF ELECTRICAL MACHINES
%clear all
%Nas simulações no FEMM e Gmsh utilizamos a área bruta tanto na culatra como
%nas colunas
clear
clc
close all
% DADOS DE ENTRADA

% DADOS DE ENTRADA



% k=0.505 %tabela 8.2 pag 342
% Ke=1; %Fornecido pelo fabricante das chapas do núcleo
% %Ku=0.907; %Fator de utilização conforme dissertação de mestrado pag 25
% Ku=0.78; %Fator de utilização conforme dissertação de mestrado pag 25
% 


J1=1.31;% densidade de corrente (A/mm2) - tabela 8.3 - pag 348 ok
J2=1.51;% densidade de corrente (A/mm2) - tabela 8.3 - pag 348 ok
Bm=1.55;% pag 348 ok
Ksw=6;% Fator de espaço  pag 347 ok
%kt=0.45;
kt=0.52 %tabela 8.4 pag 350 ok
Rjan=3.41; %ítem 8.12 pag 353 ok
rel=1.15;%ítem 8.12 pag 353 ok
% Parâmetros alterados:
%Ke para  de  1.0  para 0.945
%K de 0.505 para 0.625
% Ku de 0.78 para 0.907
% Isolação na alta de 8*a para 6*A
% YrAT
Ke=0.945; % Constante de empilhamento  - Fornecido pelo fabricante das chapas do núcleo ok
k=0.505; %tabela 8.2 pag 342 
Ku=0.907; %Fator de utilização conforme dissertação de mestrado pag 25


Bs=1.80;%Valores fornecido pelo usuário - Densdidade na região saturada
Bma=Bm*1.00;
Bmb=Bm*1.00;
Bmc=Bm*1.00;

Br=1.20;%Valores fornecido pelo usuário - Densidade remanescente

f=60; % frequencia (Hz)

Jm=(J1+J2)/2;
J=Jm;
Dfe=7650; %densidade do ferro em milímetros
V1=0.220; %tensão no primário do transformador (KV)
V2=13.80; %tensões no secundário AT do transformador 13.8/13.20/12.6
%12.0/11.4(KV)
V2menor=10.2;
Vf1=V1/sqrt(3);
Vf2=V2;
Vmedio2=12.0;
Vf2menor=V2menor;
%Vf2menor=Vf2 % tirar esta esta observação.
Q=150; % Potencia em KVA
Qf=Q/3; %Potencia do transformador em (KVA)
%kt=0.4711;%Valor sugerido pelos livros de projetos electrical Machine Design e Design of electrical Machines
kt=kt;
Et=(kt)*(sqrt(Q)) %cálculo da tensão por volta
%Et=5.77
N1=(Vf1*10^3)/Et
N2=(Vf2*10^3)/Et
Bm=Bm
Ac=(Et/(4.44*f*Bm)) %área efetiva da coluna do núcelo
Profteste=sqrt((4*Ac)/pi);
Ac=(Et/(4.44*f*Bm))*10^6%Cálculo da área líquida da seccão do núcleo em mm2
Ke=Ke;
Abc=Ac/Ke %Área bruta da coluna.
Ku=Ku;
So=Abc/Ku; %Seção circular circunscrita
dc=2*(sqrt(So/pi)) %diâmetro da coluna
%Dimensões do núcleo e dos degraus do transformador
col10=Abc/(dc^2);
Ku=col10*(4/pi);
L1=dc*0.95; % 
L2=dc*0.846;
L3=dc*0.707;
L4=dc*0.534;
L5=dc*0.313;
teta1=acos(0.95);
teta2=acos(0.846);
teta3=acos(0.707);
teta4=acos(0.534);
teta5=acos(0.313);
%
%cálculo da profundidade do núcleo
e1=sin(teta1)*(dc/2);
e2=(sin(teta2)*(dc/2))-e1;
e3=(sin(teta3)*(dc/2))-e1-e2;
e4=(sin(teta4)*(dc/2))-e1-e2-e3;
e5=(sin(teta5)*(dc/2))-e1-e2-e3-e4;
Prof=(e1+e2+e3+e4+e5)*2
Abc=(L1*e1+L2*e2+L3*e3+L4*e4+L5*e5)*2; %Esta área é a que deve ser inserida no programa FEMM. Foi colocado esta área na largura de Wc ou seja 
% a produndidade no FEMM será de igual a Prof=Abc/Wc
So=pi*(dc^2/4);
Ac=Ac;
k=k;
d=sqrt(Ac/k); %Diâmetro interno do enrolamento ou diâmetro téorico
%T1=18.20
%T2=32.22
%T3=46
%T4=57.7
%T5=71.75
%Afe=d^2{(0.5*sin(2*T1)+[0.5*sin(2*T2)-sin(T1)*cos(T2)]+[0.5*sin(2*T2)-sin(T1)*cos(T2)]+[0.5*sin(2*T2)-sin(T1)*cos(T2)]+[0.5*sin(2*T2)-sin(T1)*cos(T2)]}
wc=L1;
a=(d-wc)/2
b=a
Proffem=Abc/L1

Kw=Ksw/(30+Vf2) %Vf2 É tensão da fase do enrolamento da alta em KV, foi alterado para 8
Ac=Ac;
J1=J1;




Aw=(Q/(3.33*Ac*f*Bm*Kw*J1))*10^9%D = Distancia entre dois núcleos adjacentes

Q=3.33*f*Ac*Bm*J1*Kw*Aw*10^-9;
Rjan=Rjan;  	
ww=sqrt(Aw/Rjan);%
hw=Aw/ww;
D=ww+wc;
wc=wc;
W=2*D+wc;
W=2*ww+3*wc;
%Estimativa de corrente sem carga
%ai=(hw*ww)%nova área no núcleo para cálculo da profundidade
rel=rel;
Abc=Abc;
Abj=rel*Abc;
Aj=rel*Ac;
Abj=rel*Abc;
Prof=Prof

hy=Abj/Prof;
By=Bm/rel
By=Bm*(Ac/Aj);%densidade de fluxo no jugo (yoke)

H=hw+2*hy;

hw=hw;
Ac=Ac;
Vferc=3*hw*Ac; % volume de ferro no núcleo

Bfe=Dfe*10^-9; %densidade do ferro em milímetros
Mc=Bfe*Vferc;
Pic=(peso_especifico(Bm,0))
Dfe=Dfe;
Wic=(Pic*Mc); %Perda específica do núcleo Wic (watt)
%Wtj=(2*W*Aj)*Bfe*10^-3; %Peso do Yoke (guarnição do Núcleo) em Kg
Aj=Aj;
W=W;
Vferj=Aj*W*2;
Mj=(Vferj)*Bfe;
MT=Mc+Mj;
Pij=(peso_especifico(By,0))
%
%
%Pij=1.54
%
%Pij=1.10; %Perda específica do ferro no Yoke (guarnições Para By = 1.336
%(PiY = 1.10, conforme  fig. 8.12)
Wij=(Pij*Mj);%Perda específica do ferro nas culatras (guarnições de suporte para o núcleo, são duas, uma no topo e a outra na base dos núcleos
%PESOTOTAL=(Wti+Wiy)*10^3

PESOTOTAL=(Mc+Mj);
Wic=Wic;
Wij=Wij;
Po=(Wic+Wij)*1.05;%Perdas totais do ferro no transformador. As perdas totais é a soma da perda nas colunas + as perdas nas culatras (culatras e guarnições)
Vf1=V1/sqrt(3)
Ip=(Po/(3*Vf1))*10^-3; %Componente da corrente ativa Ip da perda no núcleo
%Ip=(Po/(Vf1))*10^-3
%calculo da componente da Corrente de magnetização  Iq
%atc=curva_BH(Bm,0)*0.10
atc=curva_BH(Bm,0)
hw=hw;
ATc=(3*hw*atc);
%Similar para By=1.336 T e conforme figura 8.13 da curva B-H
%atj=curva_BH(By,0)*0.10
atj=curva_BH(By,0)
W=W
ATj=(2*W*atj)
ATcj=ATc+ATj;
%Pode acrescentar até 5% de ATcj devido estar juntos no transformador
ATT=(1.0*ATcj);
N1=N1;
Iq=(ATT/(N1))*10^-3;% N1 enrolamento do lado da BT conforme trafo WEG DE 150 KVA
Ip=Ip;
Io=sqrt(Ip^2+Iq^2);
Fpocalculado=Ip/Io;
% Dimensionamento dos condutores e cálculos das distância no enrolamentos  primário - LADO DE BT
Vf1=Vf1;
Et=Et;
N1=(Vf1*10^3)/Et;
I1=(Qf/Vf1);
Fc1=I1/J1 %área do condutor em mm2 no primário

Swind1=Fc1*N1;
%dbt=sqrt((Swind1*4)/3.1416)
%Swind1=Fc1*N1*2 %área do enrolamento da BT este valor é multiplicado por
%dois, pois, em cada volta os condutores aumentam a área nas duas direções, frente e na parte do fundo

z=(hw*Kw)*2;
hb=((hw-z))*1.11;
tbt1=(Swind1/(hb))*1.10;% 10% de folga
tbt2=tbt1*2;
%tbt2=(Swind1)/(hw-65)
%tbt1=tbt2/2


Dextbt=tbt2+(d); %diâmetro em milímetros
dmbt=(Dextbt+d)/2; %diâmetro médio na baixa tensão em milímetros
Lmbt=(3.1416*dmbt);% coprimento em metros ( valor a ser utilizado na profundidade do FEMM para cálculo das perdas do cobre na BT)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculo do peso dos condutores de alumínio
Compbt1=Lmbt*N1;
Fc1=I1/J1;
dfc1=sqrt((4*Fc1)/pi)
VALbt= (Compbt1*Fc1)*3; %o valor 2.7 g/cm3= 2.7^-6 Kg/mm3  O valor 3 é devido ao
%fato do transformador ser trifásico. (03 bobinas).
Mbt3=(VALbt*(2.7)*10^-6);
%
%
% Dimensionamento dos condutores e cálculos das distância no enrolamentos secundário - LADO DE AT
N2=((Vf2*10^3)/Et);
N2=((Vf2*10^3)/Et);
I2menor=(Qf/Vf2);
I2c=(Qf/Vmedio2);% tap intermediário para dimensionamento dos condutores
Fc2AT=I2c/J2;%área do condutor em mm2 no secundário
dfc2AT=sqrt((4*Fc2AT)/pi);
SwindAT=(Fc2AT*N2);
dAt=sqrt((SwindAT*4)/pi);
%
%o valor 65 pode ser calculado por: (hw*kw)/2 ou seja altura da janela
%vezes a fator de espaço
%tAT1=SwindAT/(hw-65)
hb=hb;
tAT1=(SwindAT/(hb))*1.10;
Laxju=hw-((hw*Kw)/2);
tAT2=tAT1*2;
%SwindAT=(Fc2AT*N2*2)
%área do enrolamento da BT este valor é multiplicado por dois, pois, em cada volta os condutores aumentam a área nas duas direções, frente e na parte do fundo
%tAT2=SwindAT/(hw-65)
%tAT1=tAT2/2
% dintAT=(Dextbt+4*a)
dintAT=(Dextbt+6*a);%adequação do projeto GHR
%DextAT=(dintAT+2*a+tAT2)%diâmetro em milímetros
DextAT=(dintAT+2*tAT2);%diâmetro em milímetros
%DextAT=(Dextbt+(2*Kw*ww)+tAT2)
dMAT=(dintAT+DextAT)/2; %diâmetro principal na baixa tensão em milímetros

% dintATR=Dextbt+tAT2;
% DextATR=Dextbt+tAT2;
% dMatR=(dintATR+DextATR)/2;
LmAT=(pi*dMAT);% % coprimento milímetros ( valor a ser utilizado na profundidade do FEMM para cálculo das perdas do cobre na BT)
%Calculo do peso dos condutores de alumínio
Compbt1=LmAT*N2;
Fc2=I2c/J2;
VALAT= (Compbt1*Fc2)*3; %o valor 2.7 g/cm3= 2.7^-6 Kg/mm3  O valor 3 é devido ao
%fato do transformador ser trifásico. (03 bobinas).
MAT3=(VALAT*(2.7)*10^-6);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Lmbt=(3.1416*dmbt);
%Calculo das perdas no cobre
N1=N1;
Fc1=Fc1;
R1=(0.02857)*((Lmbt*N1*10^-3)/(Fc1));
LmAT=LmAT;
N2=N2;
Fc2AT=Fc2AT
dfc2AT=sqrt((4*Fc2AT)/pi)
R2=(0.02857)*((LmAT*N2*10^-3)/(Fc2AT));
N1=(Vf1*10^3)/Et;% apenas para acompanhar cálculos
N2=((Vf2*10^3)/Et);% apenas para acompanhar cálculos
%R2REF=R2*((N1/N2)^2)
%RT1=R1+R2REF
I1=(Qf/Vf1);% apenas para acompanhar cálculos
I2=(Qf/V2);
%I2menor=(Qf/13.80)
PJ1=(R1*((I1)^2)*3);
PJ2=(R2*((I2)^2)*3);
Pj=PJ1+PJ2;
Fc=sqrt(Po/Pj);
PerdasT=(Po+Pj);
Pt=(Po+Pj)/1000;
%PERDA (kW)
n=((Q*0.80)/((Q*0.80)+Pt)); %Considerando fator de potência 0.80
% A corrente de magnetização Io é 9.4929 bem maio do que o informado no
% projeto
% o condutor na AT deve ser considerado para a menor tensão, ou seja, para
% o maio valor de corrente na alta tensão.
%
%Calculo da reatância referida ao primário.
R2ref=R2*((N1/N2)^2);%Resistência do  enrolamento secundário (AT) referida para o primario (BT)
Rt=R1+R2ref; %Resistência total referida para o enrolamento primário
Pj=(Rt*(I1^2))*3; %Perdas no cobre com o enrolamento de At referido ao primário
Lc=hw-65 %Comprimento axial das bobinas
%a=0.05; 
Ac=(Et/(4.44*f*Bm)); %área deve estar em m2

VmL=(V1*1000)*sqrt(2)
Fluxonominal2=(VmL/sqrt(3))/(2*pi*f)
Fluxonominalbt=(Vf1*sqrt(2)*1000)/(2*pi*f)
Bn=(Fluxonominal2/(Ac*N1))
Bn2=(Fluxonominal2/(Ac*N1))

V2=V2;
VmAT=(V2*1000)*sqrt(2);
FluxonominalAT=VmAT/(2*pi*f);
BnAT=(FluxonominalAT/(Ac*N2));


Vm=(Vf1*1000)*sqrt(2);

l=hw-65;
l=496;
Ac=(Et/(4.44*f*Bm));%Cálculo da área da seccão do núcleo em m2
%Fr=(Br*ww*Prof*10^8*l*10^-1);
Fr=(Br*Ac); %fluxo em wb/m2
Fm=(Bm*Ac);%fluxo em wb/m2
Fs=(Bs*Ac);%fluxo em wb/m2
Fmze=(Vf1*1000*sqrt(2))/(2*pi*f*N1);
%Fm=(Vf1*10^3*(sqrt(2)))/(N1*2*pi*f)
%Fs=(Bs*ww*Prof*10^8*l*10^-1);
Swind1=N1*Fc1;
%
VAc=Perda_VA(Bm,0); %Potência de excitação por KG nas colunas
VAj=Perda_VA(By,0); %Potência de excitação por KG nas culatras
S0=VAc*Mc+VAj*Mj;
Fp2=Po/S0;
%
Po=Po;

Pfo=Po/3; % Calculo do Ramo magnetizante do transformador trifásico representado pelo diagrama monofásico, para calcular e Indutância Magnética LM
Vo=(Vf1*1000)
Io=sqrt(Ip^2+Iq^2);
Rm=Pfo/(Io^2);
Zm=Vo/Io;
Xm0=sqrt(Zm^2-Rm^2);
%Lm=Xm0/(2*pi*f);
%Lm=Lm/2;


%Lado de alta tensão
Pfo=Po/3; % Calculo do Ramo magnetizante do transformador trifásico representado pelo diagrama monofásico, para calcular e Indutância Magnética LM
VoAT=(Vf2*1000);
IoAT=Io*(N1/N2);
IpAT=Ip*(N1/N2);
IqAT=Iq*(N1/N2);
RmAT=Pfo/(IoAT^2);
ZmAT=VoAT/IoAT;
Xm0AT=sqrt(ZmAT^2-RmAT^2);
LmAT=Xm0AT/(2*pi*f);
LmAT=LmAT/2;




%Valores a serem inseridos no ATP
Mo=4*pi*10^-7; %Permeabilidade do ar
hw=hw
hb=hb
dc=dc
So=So
Wa=2*pi*f;
N1=N1;


a=a


L=(Mo*(N1^2)*So)/(hb-0.45*dc) % Hayt J.r,W.A Buck J.A 2013 - Eletromagnetismo



%L=((Mo*(N1^2)*So)/(hb))*1.15 % S. E. Zirka, Y.I. Moroz, C. M. Arturi, Member, IEEE, N. Chiesa, and H. K Hoidalen, Member, IEEE - Topology-Correct Reversible Transformer Model

Lzirka=(Mo*(N1^2)/(hw))*((pi*d^2)/4) % S. E. Zirka, Y.I. Moroz, C. M. Arturi

Sd=((d^2)*pi)/4;
Sw=((wc^2)*pi)/4;
Aei=(6*a*2);% distância entre as bobinas AT e BT multiplicado por 2, devido ao fato de ter espaço nos dois lados da coluna
Sei=((Aei^2)*pi)/4;
Lelise=((Mo*(N1^2)*((Sei)))/hw)



% L indutância da bobina
% Mo é a Permeabilidade do ar
% N1 é o número de espiras do enrolamento de baixa tensão
% So é é a secção transversal do núcleo
% hw é a altura da janela do núcleo
% d é o diâmetro interno da bobina


XL=(Wa*L)/1000


f=60;%Entrada da frequencia em Hz
S=Q;%Entrada da potência em KVA.
VA=13.8;%Entrada da alta tensão em KV.
VfA=VA;
Vb=220; %Entrada da tensão de linha do lado de baixa em V.
Vfb=Vb/(sqrt(3));

Xb=XL;

Lm=L;
%Lm=Lbb*1000

Rb=R1;
Zb=sqrt(Rb^2+Xb^2);
RA=R2;
ktrafo=(VfA*1000)/(Vfb);
XA=Xb*(ktrafo^2);
ZA=sqrt(RA^2+XA^2);
Zccb=Zb+(ZA/(ktrafo^2));
Ifb=(S*1000/3)/Vfb;
Vccb=Ifb*Zccb;
Zp=(Vccb/Vfb)*100
Rccb=Rb+(RA/(ktrafo^2));
VccRb=Ifb*Rccb;
Rp=(VccRb/Vfb)*100;
Xp=sqrt(Zp^2-Rp^2);
Fpo=Ip/Io;
Io=Io;
%Iofa=Io      %As correntes se dividem nesta proporção.
%Iofb=Io*0.75 %As correntes se dividem nesta proporção.
%Iofc=Io*0.80 %As correntes se dividem nesta proporção.
%Iomedio=(Iofa+Iofb+Iofc)/3
%Iop=(Iomedio/Ifb)*100;
Iop=(Io/Ifb)*100;


% f=60;%Entrada da frequencia em Hz
% S=300%Entrada da potência em KVA.
% VA=13.8%Entrada da alta tensão em KV.
% VfA=VA
% Vb=380 %Entrada da tensão de linha do lado de baixa em V.
% Vfb=Vb/(sqrt(3))
% Zp=4.5; %Entrada da impedância percentual.
% Rp=1.12;%Entrada da Resistencia percentual.
% Iop=1.8;%Entrada da corrente a vazio em percentual.
% Fpo=0.20 %fator de potencia do transformador a vazio

%Cálculos
%1- Relação de transformação
ktrafo=(VfA*1000)/(Vfb);
%2- Cálculo das correntes
IfA=(S/3)/VfA;
ILA=IfA*(sqrt(3));

Ifb=(S*1000/3)/Vfb;
ILb=Ifb;
%3- Corrente a vazio
Io=Io;
Iob=Io;
IoA=Iop*(IfA)/100;
IopicoA=IoA*(sqrt(2)); %Este valor é o valor a ser inserido no ATP
Iopicob=IopicoA*ktrafo;
Iob=Iop*(Ifb)/100
%
%4- Potência a vazio (Po)
%Pof=VA*1000*IoA*Fpo
Po3=Po;
%
%5- Impedância do primário e secundário (Zp e Zs)
%Impedância da alta
ZbaseA=(VA)^2/(S/(3*1000));
ZbaseB=(Vfb)^2/(S*1000/3);

ZtA=(ZbaseA*Zp)/100;
ZA=ZtA/2;
%Impedância da baixa
Zb=ZA/ktrafo^2;
%
%6- Resistencia da alta e baixa tensão
% RA=(Rp*ZbaseA)/(2*100)
% Rb=RA/ktrafo^2
%

%7- Potência de curto-circuito
Pccf=RA*IfA^2+Rb*Ifb^2;
Pcc3=3*Pccf;
%
%8- Reatância do primário e secundário
XA=sqrt(ZA^2-RA^2)
Xb=sqrt(Zb^2-Rb^2)
%
%9- Indutância do primário e secundário (LA e Lb)
LA=(XA/Wa)*1000 %Indutância em (mH)
Lb=(Xb/Wa)*1000 %Indutância em (mH)
%
%10- Resistência de Magnetização
RmagA=(VA*1000)^2/Po3;
Rmagb=(Vfb)^2/Po3;
%
%11- Fluxo de magnetização (Y0)
FmagA=VA*1000/(4.44*60);
Fmagb=Vfb/(4.44*60);



LmAT=LA;




Lma=Lm*1.01;%Distribuição das densidades de fluxo
Lmb=Lm*1.012;%Distribuição das densidades de fluxo
Lmc=Lm*1.0104;%Distribuição das densidades de fluxo

LmaAT=LmAT*1.01;%Distribuição das densidades de fluxo
LmbAT=LmAT*1.012;%Distribuição das densidades de fluxo
LmcAT=LmAT*1.0104;%Distribuição das densidades de fluxo

% LmaAT=LaAT

Fp=Pfo/(Vo*Io);
%Cálculo das correntes  do ensaio do transformador conforme  planilha  GHR
Vo=(Vf1*1000);
Ia=8.34;
Pa=181;
Rma=Pa/(Ia^2);
Zma=Vo/Ia;
Xma=sqrt(Zma^2-Rma^2);
% Lma=Xma/(2*pi*f)
%Lma=Lma/2
Cosa=Pa/(Vo*Ia);

Vo=(Vf1*1000);
Ib=6.81;
Pb=238;
Rmb=Pb/(Ib^2);
Zmb=Vo/Ib;
Xmb=sqrt(Zmb^2-Rmb^2);
% Lmb=Xmb/(2*pi*f);
% Lmb=Lmb/2
Cosb=Pb/(Vo*Ib);
% Lmb=Lm


Vo=(Vf1*1000);
Ic=7.16;
Pc=348;
Rmc=Po/(Ic^2);
Zmc=Vo/Ic;
Xmc=sqrt(Zmc^2-Rmc^2);
% Lmc=Xmc/(2*pi*f);
% Lmc=Lmc/2
Cosc=Pc/(Vo*Ic);
Pf=(Pa+Pb+Pc)/3;
If=(Ia+Ib+Ic)/3;
Cosf=Pf/(If*Vo);

V1=V1
V2=V2
Q=Q
Lsc=(V1^2)/Q
LscAT=(V2^2)/Qf;


%
Wa=2*pi*f;
%R1=0.0082
Rt=R1;
RtAT=R2;
Rsc=0;
R=Rt+Rsc
x=0;

%Adaptações para o transformador trifásico
Ac=Ac

Bm=Bm;
Bs=Bs;
Ac=Ac;
fluxo1=Bm*Ac;
fluxo2=Bs*Ac;
Area=Ac;
hw=hw
Ln=(hw)*10^-3
Hs=curva_BH(Bs,0);
Hns=curva_BH(Bm,0);%Busca os valores na planilha da intensidade de campo, arquivo TXT
F1=Hns*Ln %Hns é a intensidade de campo na região não saturada

Rel1=F1/(fluxo1) %Relutância 
F2=Hs*Ln %Hs é a intensidade de campo na região  saturada
Rel2=F2/fluxo2
La=N1^2*fluxo1/F1;%Cálculo da indutância na região não saturada, conforme fórmula apostila de conversão  pag 15 e dados de histerese do material utilizado


Lbs=N1^2*((fluxo2-fluxo1)/(F2-F1)) %Cálculo da indutância na região saturada, conforme fórmula apostila de conversão  pag 15 e dados de histerese do material utilizado
Lma=Lma;
La=La
Lbs=Lbs
Lsc=Lsc
Ls=Lbs+Lsc

LaAT=(N2^2*fluxo1)/F1;
LbsAT=N1^2*((fluxo2-fluxo1)/(F2-F1));
LsAT=LbsAT+LscAT;

N1=N1;
Br=Br;
Ac=Ac;
Bs=Bs;
Yr=N1*Br*Ac;
Ys=N1*Bs*Ac;
Yn=N1*Bm*Ac;
YrAT=N2*Br*Ac;
YsAT=N2*Bs*Ac;
YnAT=N1*Bm*Ac;



Lsat=Lbs;
LsatAT=LbsAT;

%Lsat=Lsat1+Lsc
XLsat=(Wa*Lsat);
XLsatAT=(Wa*LsatAT);
Wa=Wa;


Limb=(Mo*(N1^2)*So)/(hb)

Imaxzirka1=([Vm/(Wa*(Lsc+Limb))]*[2-(((Wa*(Br-Bs))*N1*So)/Vm)])/10000



t1=(acos((((Yr-Ys)*Wa)/Vm)+1)/Wa)

t1AT=(acos((((YrAT-YsAT)*Wa)/VmAT)+1)/Wa);




alfa=0;
% alfa=-((2*pi)/3);
% alfa=((2*pi)/3);

tpk=0.0000:1/6000:1/60;

%Corrente de exitação
FluxoA=Fluxonominal2*(sin(Wa.*tpk));
Bteste=FluxoA/(Ac*N1);
Hteste=curva_BH(Bteste,0);
IfluxoA=(Hteste*Ln)/N1;
F1a=Hteste*Ln;
fluxo1a=Bteste*Ac;
LnsA=N1^2*fluxo1a/F1a;


alfa=0;
Vmax=Vm;
Vma=Vm*cos(alfa);
Vmb=Vm*cos(alfa+((2*pi)/3));
Vmc=Vm*cos((alfa)-((2*pi)/3));
t1=t1;
R=R;
Lm=Lm;

Wa=Wa;
Lm=Lm;
expoente=exp(-(R*t1)/Lm);

Lm=Lm;



aa=(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma));


Vma=Vma;
aa=aa;
R=R;
seno=sin(Wa*t1);
cosseno=cos(Wa*t1);
Lma=Lma;

r2=R^2;
Xm=(Wa*Lm);
Xm2=(Wa*Lm)^2;
Z=sqrt(r2 +Xm2);
tpk=0.0083;
Ls=Ls;
bb=(exp(-R.*(tpk-t1))/Ls);

cc=sin(Wa.*tpk)-sin(Wa*t1);

Ibt=(Vm*(R*sin(Wa*t1)-Wa*Lm*cos(Wa*t1)+Wa*Lm*exp(-(R*t1)/Lm)))/(R^2+(Wa*Lm)^2)

Ibta=(Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2);


Ibta=(Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2);



Ibtb=(Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2);
Ibtc=(Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2);

Ibt=(Vm*aa)/(R^2+(Wa*Lm)^2)
Ibt=(Vm*(R*sin(Wa*t1)-Wa*Lm*cos(Wa*t1)+Wa*Lm*exp(-(R*t1)/Lm)))/(R^2+(Wa*Lm)^2)

Lma=Lma;
R=R;
Wa=Wa;
t1=t1;

Ibta=(Vma*aa)/(R^2+(Wa*Lma)^2);

t1=t1;

aa=aa;
Lm=Lm;
Ls=Ls;
bb=(exp(-R.*(tpk-t1))/Ls);
dd=exp((-R.*(tpk-t1))/Ls);

bbb=exp((-R.*(tpk-t1))/Ls);

%expoent=exp(bb)
cc=sin(Wa.*tpk)-sin(Wa*t1);
cosenot1=cos(Wa*t1);
cosenotpk=cos(Wa.*tpk);

Z=(R^2+(Wa*Ls)^2);

Inrush=(Ibt.*(exp(-R.*(tpk-t1))/Ls))+(((Vm*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vm*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cosenotpk)]))/(R^2+(Wa*Ls)^2);




xa=((Vma/Vma)+((abs(Vma+Vmb)/3)/Vma));





Ibta=((Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2))
Ibtb=((Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2))*xa;
Ibtc=((Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2))*xa;

Inrush=(Ibt.*(exp(-R.*(tpk-t1))/Ls))+(((Vm*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vm*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacao=Inrush/I1;
Imaximo=max(Inrush);
Irel=Imaximo/I1;


Ibta=Ibta
aa=(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma));
senotpk=sin(Wa.*tpk);
senot1=sin(Wa*t1);
cost1=cos(Wa*t1);
costpk=cos(Wa.*tpk);
Vma=Vma;
R=R;
Ls=Ls;
Vmr1=Vma*R;
VmXs=Vma*Wa*Ls;


Ibtabb=(Ibta.*bb);
ccbb=[cc.*bb];

e=((VmXs).*[(cost1).*dd-(costpk)]);


Ippa=(Ibta.*bb)+(((Vmr1).*[cc.*bb])+((VmXs).*[(cost1).*dd-(costpk)]))/(R^2+(Wa*Ls)^2);

Ippa=(Ibta.*bb)+(((Vmr1).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((VmXs).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2)

Inrusha=(Ibta.*(exp(-R.*(tpk-t1))/Ls))+(((Vma*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vma*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2)
Irelacaoa=Inrusha/I1
Imaximoa=max(Inrusha);
Irela=Imaximoa/I1;

Inrushb=(Ibtb.*(exp(-R.*(tpk-t1))/Ls))+(((Vmb*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmb*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaob=Inrushb/I1;
Imaximob=max(Inrushb);
Irelb=Imaximob/I1;

Inrushc=(Ibtc.*(exp(-R.*(tpk-t1))/Ls))+(((Vmc*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmc*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoc=Inrushc/I1;
Imaximoc=max(Inrushc);
Irelc=Imaximoc/I1;

% figure(1);
% plot(tpk,Inrusha,'LineWidth',2,'Color','black','marker','^');
% hold on;
% plot(tpk,Inrushb,'LineWidth',2,'marker','o');
% plot(tpk,Inrushc,'LineWidth',2,'Color','red','marker','s');
% legend('Fase a','Fase b','Fase c')
% xlabel('Tempo [s]'), ylabel('Corrente [PU]');
% grid on;



alfa=-(2*pi)/3;

Vmax=Vm;
Vma=Vm*cos(alfa);
Vmb=Vm*cos(alfa+((2*pi)/3));
Vmc=Vm*cos((alfa)-((2*pi)/3));
Ibt=(Vm*(R*sin(Wa*t1)-Wa*Lm*cos(Wa*t1)+Wa*Lm*exp(-(R*t1)/Lm)))/(R^2+(Wa*Lm)^2);

Ibta=(Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2);
Ibtb=(Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2);
Ibtc=(Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2);

xb=((Vmb/Vmb)+((abs(Vmb+Vma)/3)/Vmb));%Fluxo resultante
Ibta=((Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2))*xb;
Ibtb=((Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2));
Ibtc=((Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2))*xb;

Inrush=(Ibt.*(exp(-R.*(tpk-t1))/Ls))+(((Vm*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vm*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacao=Inrush/I1;
Imaximo=max(Inrush);
Irel=Imaximo/I1;

Inrusha120=(Ibta.*(exp(-R.*(tpk-t1))/Ls))+(((Vma*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vma*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoa120=Inrusha120/I1;
Imaximoa120=max(Inrusha120);
Irela120=Imaximoa120/I1;

Inrushb120=(Ibtb.*(exp(-R.*(tpk-t1))/Ls))+(((Vmb*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmb*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaob120=Inrushb120/I1;
Imaximob120=max(Inrushb120);
Irelb120=Imaximob120/I1;

Inrushc120=(Ibtc.*(exp(-R.*(tpk-t1))/Ls))+(((Vmc*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmc*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoc120=Inrushc120/I1;
Imaximoc120=max(Inrushc120);
Irelc120=Imaximoc120/I1;

% figure(2);
% plot(tpk,Inrusha120,'LineWidth',2,'Color','black','marker','^');
% hold on;
% plot(tpk,Inrushb120,'LineWidth',2,'marker','o');
% plot(tpk,Inrushc120,'LineWidth',2,'Color','red','marker','s');
% legend('Fase a','Fase b','Fase c')
% xlabel('Tempo [s]'), ylabel('Corrente [PU]');
% grid on;


alfa=(2*pi)/3;

Vmax=Vm;
Vma=Vm*cos(alfa);
Vmb=Vm*cos(alfa+((2*pi)/3));
Vmc=Vm*cos((alfa)-((2*pi)/3));

Ibta=(Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2);
Ibtb=(Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2);
Ibtc=(Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2);

xc=((Vmc/Vmc)+((abs(Vma+Vmc)/3)/Vmc));%Fluxo resultante
Ibta=((Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2))*xc;
Ibtb=((Vmb*(R*sin(Wa*t1)-Wa*Lmb*cos(Wa*t1)+Wa*Lmb*exp(-(R*t1)/Lmb)))/(R^2+(Wa*Lmb)^2))*xc;
Ibtc=((Vmc*(R*sin(Wa*t1)-Wa*Lmc*cos(Wa*t1)+Wa*Lmc*exp(-(R*t1)/Lmc)))/(R^2+(Wa*Lmc)^2));



Inrusha240=(Ibta.*(exp(-R.*(tpk-t1))/Ls))+(((Vma*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vma*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoa240=Inrusha240/I1;
Imaximoa240=max(Inrusha240);
Irela240=Imaximoa240/I1;

Inrushb240=(Ibtb.*(exp(-R.*(tpk-t1))/Ls))+(((Vmb*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmb*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaob240=Inrushb240/I1;
Imaximob240=max(Inrushb240);
Irelb240=Imaximob240/I1;

Inrushc240=(Ibtc.*(exp(-R.*(tpk-t1))/Ls))+(((Vmc*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vmc*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoc240=Inrushc240/I1;
Imaximoc240=max(Inrushc240);
Irelc240=Imaximoc240/I1;

% figure(3);
% plot(tpk,Inrusha240,'LineWidth',2,'Color','black','marker','^');
% hold on;
% plot(tpk,Inrushb240,'LineWidth',2,'marker','o');
% plot(tpk,Inrushc240,'LineWidth',2,'Color','red','marker','s');
% legend('Fase a','Fase b','Fase c')
% xlabel('Tempo [s]'), ylabel('Corrente [PU]');
% grid on;



%Entre com o valor do tempo de maior corrente da fase desejada

%tpka=0.0013890 %Fase A
%tpkb=0.0069445 % Fase B
%tpkc=0.0041597%Fase C



alfa=0;

VmaAT=VmAT*cos(alfa);
VmbAT=VmAT*cos(alfa+((2*pi)/3)); %Corrente Inrush na AT
VmcAT=VmAT*cos((alfa)-((2*pi)/3));
IbtAT=(VmAT*(R2*sin(Wa*t1AT)-Wa*LmAT*cos(Wa*t1AT)+Wa*LmAT*exp(-(R2*t1AT)/LmAT)))/(R2^2+(Wa*LmAT)^2);

Ibta=(VmaAT*(R2*sin(Wa*t1AT)-Wa*LmaAT*cos(Wa*t1AT)+Wa*LmaAT*exp(-(R2*t1AT)/LmaAT)))/(R2^2+(Wa*LmaAT)^2);
Ibtb=(VmbAT*(R2*sin(Wa*t1AT)-Wa*LmbAT*cos(Wa*t1AT)+Wa*LmbAT*exp(-(R2*t1AT)/LmbAT)))/(R2^2+(Wa*LmbAT)^2);
Ibtc=(VmcAT*(R2*sin(Wa*t1AT)-Wa*LmcAT*cos(Wa*t1AT)+Wa*LmcAT*exp(-(R2*t1AT)/LmcAT)))/(R2^2+(Wa*LmcAT)^2);

xaAT=((VmaAT/VmaAT)+((abs(VmaAT+VmbAT)/3)/VmaAT));
Ibta=((VmaAT*(R2*sin(Wa*t1AT)-Wa*LmaAT*cos(Wa*t1AT)+Wa*LmaAT*exp(-(R2*t1AT)/LmaAT)))/(R2^2+(Wa*LmaAT)^2));%Corrente Inrush na AT
Ibtb=((VmbAT*(R2*sin(Wa*t1AT)-Wa*LmbAT*cos(Wa*t1AT)+Wa*LmbAT*exp(-(R2*t1AT)/LmbAT)))/(R2^2+(Wa*LmbAT)^2))*xaAT;
Ibtc=((VmcAT*(R2*sin(Wa*t1AT)-Wa*LmcAT*cos(Wa*t1AT)+Wa*LmcAT*exp(-(R2*t1AT)/LmcAT)))/(R2^2+(Wa*LmcAT)^2))*xaAT;

InrushAT=(IbtAT.*(exp(-R2.*(tpk-t1AT))/LsAT))+(((VmAT*R2).*[sin(Wa.*tpk)-sin(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)])+((VmAT*Wa*LsAT).*[(cos(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)-cos(Wa.*tpk))]))/(R2^2+(Wa*LsAT)^2);
IrelacaoAT=InrushAT/I2; %Corrente InrushAT na AT
ImaximoAT=max(InrushAT);
IrelAT=ImaximoAT/I2;

InrushaAT=(Ibta.*(exp(-R2.*(tpk-t1AT))/LsAT))+(((VmaAT*R2).*[sin(Wa.*tpk)-sin(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)])+((VmaAT*Wa*LsAT).*[(cos(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)-cos(Wa.*tpk))]))/(R2^2+(Wa*LsAT)^2);
Irelacaoa=InrushaAT/I2; %Corrente InrushAT na AT
ImaximoaAT=max(InrushaAT);
IrelaAT=ImaximoaAT/I2;

InrushbAT=(Ibtb.*(exp(-R2.*(tpk-t1AT))/LsAT))+(((VmbAT*R2).*[sin(Wa.*tpk)-sin(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)])+((VmbAT*Wa*LsAT).*[(cos(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)-cos(Wa.*tpk))]))/(R2^2+(Wa*LsAT)^2);
IrelacaobAT=InrushbAT/I2;
ImaximobAT=max(InrushbAT);
IrelbAT=ImaximobAT/I2;

InrushcAT=(Ibtc.*(exp(-R2.*(tpk-t1AT))/LsAT))+(((VmcAT*R2).*[sin(Wa.*tpk)-sin(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)])+((VmcAT*Wa*LsAT).*[(cos(Wa*t1AT).*exp((-R2.*(tpk-t1AT))/LsAT)-cos(Wa.*tpk))]))/(R2^2+(Wa*LsAT)^2);
IrelacaocAT=InrushcAT/I2;
ImaximocAT=max(InrushcAT);%Corrente InrushAT na AT
IrelcAT=ImaximocAT/I2;


H=H
W=W
hw=hw
hb=hb
ww=ww
wc=wc
hy=hy
Prof=Prof
d=d
Io=Io
Po=Po
Pj=Pj
Pt=Pj+Po
Lb=Lb
MT=MT
Mbt3=Mbt3
MAT3=MAT3
Mativa=MT+Mbt3+MAT3
I1=I1
Inrusha=Inrusha
Irel=Irel
a=a
tbt1=tbt1
tbt2=tbt2

Massa=PESOTOTAL
nst=1.8; % conforme Manual ATP pag 156 e Apostila conversão pag 48 (perdas por histerese)
k1=0.009; %conforme livro eletrotécnica autor Alfonso Martignoni pagina 286 Lâminas de ferro silício
%PH=k1*(f^1.1)*(Bm^nst)*Massa% Perdas por histerese conforme Manual ATP pag 156
Wh=k1*f*(Bm^nst)*Massa % Perdas por histerese conforme livro eletrotécnica autor Alfonso Martignoni pagina 402

Mh=Wh/Massa

MT=MT;
esp=0.27/1000;
Rolam=5000*(10^-6); %resistividade aproximada da da Lâmina de aço silício ohm.m
%Pci=(Massa*(pi*f*esp*Bm)^2)/(6*Rolam) %perdas por Foucault ou correntes induzidas

Wp=(((pi*f*esp*Bm)^2*Massa)/(8*Rolam)) %perdas por Foucalt ou correntes conforme livro eletrotécnica do autor Alfonso Martignoni página 403
Mp=Wp/Massa

Perdakg=Mh+Mp
Pic=Pic
Pij=Pij


Perdaspo=Wh+Wp
Po=Po


Imaximoa=Imaximoa
Imaximob=Imaximob
Imaximoc=Imaximoc
Imaximoa120=Imaximoa120
Imaximob120=Imaximob120
Imaximoc120=Imaximoc120
Imaximoa240=Imaximoa240
Imaximob240=Imaximob240
Imaximoc240=Imaximoc240


%Dados de entrada ATP
Zp=Zp
Rp=Rp
Fpo=Fpo
Iop=Iop
IfA=I2
Ifb=I1
IoA=IoA
Iob=Iob
IopicoA=IopicoA
Iopicob=IopicoA*ktrafo
RA=RA
Rb=Rb
% ZA=ZA
% Zb=Zb

XA=XA
Xb=Xb
LA=LA
Lb=Lb
% Iob=Iop*(Ifb)/100
% Iopicob=Iob*(sqrt(2))
% Bm=Bm
RmagA=RmagA
Rmagb=Rmagb
FmagA=FmagA
Fmagb=Fmagb

% 
% ww=ww
% 
% Prof=Prof
% hy=hy
% 
% Po=Po
% Fc1=Fc1
% Fc2AT=Fc2AT
% Dextbt=Dextbt
% DextAT=DextAT
% a=a
% 
% d=d
% 
% 
% 
% 
% Po3=Po3
% 

% IfA=IfA
% Ifb=Ifb

% La=La
% Lma=Lma
% Lmb=Lmb
% Lmc=Lmc
Po=Po
Pj=Pj
PerdasT=PerdasT
n=n
Fc=Fc
Imaximoa=Imaximoa
% 
% Imaximob=Imaximob
% Imaximoc=Imaximoc
% 
% Imaximoa120=Imaximoa120
% Imaximob120=Imaximob120
% Imaximoc120=Imaximoc120
% 
% Imaximoa240=Imaximoa240
% Imaximob240=Imaximob240
% Imaximoc240=Imaximoc240
% 
% ImaximoaAT=ImaximoaAT
% ImaximobAT=ImaximobAT
% ImaximocAT=ImaximocAT
Ac=Ac
E1max=Wa*Bm*Ac*N1
E1=4.44*f*Bm*Ac*N1
E1=E1max/sqrt(2)
Iq=Iq
Iqmax=Iq*sqrt(2)
F=N1*Iq %valor eficaz
Fmax=N1*Iqmax %Força magnetomotriz máxima em A.e
Fluxomax=Bm*Ac %fluxo em (Wb)
Relutancia=Fmax/Fluxomax %(H)

%Relutancia=l/(Mo*Mr*Ac)
%Relutancia=l/Mi*Ac

%Mo= 4*pi*10^-7 permeabilidade do ar 
%Mr= permeabilidade relativa do material aproxidamente 20.000
%Mi= permeabilidade do material
Mo=4*pi*10^-7
Mr=5000 %Permeabilidade do ferro silício grão orientado
Mi=Mo*Mr
%Relutancia=l/(Mo*Mr*Ac)
Relutancia=(hw/1000)/(Mo*Mr*Ac);
Relutancia=(hw/1000)/(Mi*Ac)


Vmax=Vf1*1000*sqrt(2);
Vf1=Vf1*1000
Fluxomax=(Vmax/(Wa*N1))*5000;
Bmax=Fluxomax/Ac*N1*1000000
XLb=2*pi*f*Lb
VLbef=(XLb/(R1+XLb))*Vf1
VR1ef=(R1/(R1+XLb))*Vf1
IR1ef=VR1ef/R1
ILbef=VLbef/XLb
WL=1/2*(XLb*ILbef^2)

t=0.0000:1/6000:1/60;
v=Vmax*sin(Wa*t);
Fluxo=-Fluxomax*cos(Wa*t);

figure(7);
plot(t,v,'LineWidth',2,'Color','black','marker','^');
hold on;
plot(t,Fluxo);
grid on;


syms x

d=int(((Vmax*sin(Wa*x))))
Corrente1=-((11*6^(1/2)*cos(120*pi*0.0004167))/(18*pi))*(1/Lb)
Corrente2=-((11*6^(1/2)*cos(120*pi*0.0083333))/(18*pi))*(1/Lb)
Corrente3=-((11*6^(1/2)*cos(120*pi*016667))/(18*pi))*(1/Lb)


Corrente2=(-(127*2^(1/2)*cos(120*pi*0.0083333))/(120*pi))*(1/Lb);
Corrente3=(-(127*2^(1/2)*cos(120*pi*0.016667))/(120*pi))*(1/Lb);









