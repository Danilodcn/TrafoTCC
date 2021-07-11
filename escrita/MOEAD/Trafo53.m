
%function Perdas=Trafo(x)
function [z , DadosFinais] = Trafo53(x)

n=numel(x);

% f5=x(1)
    
   % g=1+9/(n-1)*sum(x(2:end))
    
    %h=1-sqrt(f1/g)
    
%Estava no dropbox era o arquivo antigo mopso e moed - ser� utilizado este
%mesmo trafo para MOPSO e MOED 07/12/2018
    
    %f2=g*h;

J1=x(1); 
J2=x(2);
Bm=x(3);
Ksw=x(4);
kt=x(5);
Rjan=x(6);
rel=x(7);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Ke=0.945; % Constante de empilhamento  - Fornecido pelo fabricante das chapas do n�cleo ok
k=0.505; %tabela 8.2 pag 342 
Ku=0.907; %Fator de utiliza��o conforme disserta��o de mestrado pag 25
Bs=1.80;%Valores fornecido pelo usu�rio - Densdidade na regi�o saturada
Br=1.20;%Valores fornecido pelo usu�rio - Densidade remanescente
f=60; % frequencia (Hz)
Dfe=7650; %densidade do ferro em mil�metros
V1=0.220; %tens�o no prim�rio do transformador (KV)
V2=13.80; %tens�es no secund�rio AT do transformador 13.8/13.20/12.6
%12.0/11.4(KV)
V2menor=10.2;
Vf1=V1/sqrt(3);
Vf2=V2;
Vmedio2=12.0;
Vf2menor=V2menor;
%Vf2menor=Vf2 % tirar esta esta observa��o.
Q=150; % Potencia em KVA
Qf=Q/3; %Potencia do transformador em (KVA)
%kt=0.4711;%Valor sugerido pelos livros de projetos electrical Machine Design e Design of electrical Machines
kt=kt;
Et=(kt)*(sqrt(Q)); %c�lculo da tens�o por volta
%Et=5.77
N1=(Vf1*10^3)/Et;
N2=(Vf2*10^3)/Et;
Bm=Bm;
Ac=(Et/(4.44*f*Bm)); %�rea efetiva da coluna do n�celo
Ac=(Et/(4.44*f*Bm))*10^6;%C�lculo da �rea l�quida da secc�o do n�cleo em mm2
Abc=Ac/Ke; %�rea bruta da coluna.
So=Abc/Ku; %Se��o circular circunscrita
dc=2*(sqrt(So/pi)); %di�metro da coluna
%Dimens�es do n�cleo e dos degraus do transformador
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
%c�lculo da profundidade do n�cleo
e1=sin(teta1)*(dc/2);
e2=(sin(teta2)*(dc/2))-e1;
e3=(sin(teta3)*(dc/2))-e1-e2;
e4=(sin(teta4)*(dc/2))-e1-e2-e3;
e5=(sin(teta5)*(dc/2))-e1-e2-e3-e4;
Prof=(e1+e2+e3+e4+e5)*2;
Abc=(L1*e1+L2*e2+L3*e3+L4*e4+L5*e5)*2; %Esta �rea � a que deve ser inserida no programa FEMM. Foi colocado esta �rea na largura de Wc ou seja 
% a produndidade no FEMM ser� de igual a Proffem=Abc/Wc
So=pi*(dc^2/4);
d=sqrt(Ac/k); %Di�metro interno do enrolamento ou di�metro t�orico
wc=L1;
a=(d-wc)/2;
Proffem=Abc/L1;
Kw=Ksw/(30+Vf2); %Vf2 � tens�o da fase do enrolamento da alta em KV, foi alterado para 8
Aw=(Q/(3.33*Ac*f*Bm*Kw*J1))*10^9;%D = Distancia entre dois n�cleos adjacentes - original
Acm2=Ac/1000000; %transformar mm2 para m2
Awm2=Aw/1000000; %transformar mm2 para m2
Qm2=3.33*f*Acm2*Bm*J1*Kw*Awm2*10^3;
Q=3.33*f*Ac*Bm*J1*Kw*Aw*10^-9;% Original
Rjan=Rjan;  	
ww=sqrt(Aw/Rjan);%
hw=Aw/ww;
D=ww+wc;
wc=wc;
W=2*D+wc;
%Estimativa de corrente sem carga
%ai=(hw*ww)%nova �rea no n�cleo para c�lculo da profundidade
Abj=rel*Abc;
Aj=rel*Ac;
hy=Abj/Prof;
By=Bm/rel;
By=Bm*(Ac/Aj);%densidade de fluxo no jugo (yoke)
H=hw+2*hy;
Vferc=3*hw*Ac; % volume de ferro no n�cleo
Bfe=Dfe*10^-9; %densidade do ferro em mil�metros
Mc=Bfe*Vferc;
Pic=(peso_especifico(Bm,0));
Dfe=Dfe;
Wic=(Pic*Mc); %Perda espec�fica do n�cleo Wic (watt)
%Wtj=(2*W*Aj)*Bfe*10^-3; %Peso do Yoke (guarni��o do N�cleo) em Kg
Aj=Aj;
W=W;
Vferj=Aj*W*2;
Mj=(Vferj)*Bfe;
MT=Mc+Mj;
Pij=(peso_especifico(By,0));
Wij=(Pij*Mj);%Perda espec�fica do ferro nas culatras (guarni��es de suporte para o n�cleo, s�o duas, uma no topo e a outra na base dos n�cleos
%PESOTOTAL=(Wti+Wiy)*10^3
PESOTOTAL=(Mc+Mj);
Wic=Wic;
Wij=Wij;
Po=(Wic+Wij)*1.05;%Perdas totais do ferro no transformador. As perdas totais � a soma da perda nas colunas + as perdas nas culatras (culatras e guarni��es)
Vf1=V1/sqrt(3);
Ip=(Po/(3*Vf1))*10^-3; %Componente da corrente ativa Ip da perda no n�cleo
atc=curva_BH(Bm,0);
hw=hw;
ATc=(3*hw*atc);
%Similar para By=1.336 T e conforme figura 8.13 da curva B-H
atj=curva_BH(By,0);
ATj=(2*W*atj);
ATcj=ATc+ATj;
ATT=(1.0*ATcj);
Iq=(ATT/(N1))*10^-3;% N1 enrolamento do lado da BT conforme trafo WEG DE 150 KVA
Ip=Ip;
Io=sqrt(Ip^2+Iq^2);
Fpocalculado=Ip/Io;
% Dimensionamento dos condutores e c�lculos das dist�ncia no enrolamentos  prim�rio - LADO DE BT
Vf1=Vf1;
Et=Et;
N1=(Vf1*10^3)/Et;
I1=(Qf/Vf1);
Fc1=I1/J1; %�rea do condutor em mm2 no prim�rio
dfc1=sqrt((Fc1*4)/pi);
Swind1=Fc1*N1;
z=(hw*Kw)*2;
hb=((hw-z))*1.11;
tbt1=(Swind1/(hb))*1.10;% 10% de folga
tbt2=tbt1*2;
Dextbt=tbt2+(d); %di�metro em mil�metros
dmbt=(Dextbt+d)/2; %di�metro m�dio na baixa tens�o em mil�metros
Lmbt=(3.1416*dmbt);% coprimento em metros 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Calculo do peso dos condutores de alum�nio
Compbt1=Lmbt*N1;
Fc1=I1/J1;
dfc1=sqrt((4*Fc1)/pi);
VALbt= (Compbt1*Fc1)*3; %o valor 2.7 g/cm3= 2.7^-6 Kg/mm3  O valor 3 � devido ao
%fato do transformador ser trif�sico. (03 bobinas).
Mbt3=(VALbt*(2.7)*10^-6);
% Dimensionamento dos condutores e c�lculos das dist�ncia no enrolamentos secund�rio - LADO DE AT
I2menor=(Qf/Vf2);
I2c=(Qf/Vmedio2);% tap intermedi�rio para dimensionamento dos condutores
Fc2AT=I2c/J2;%�rea do condutor em mm2 no secund�rio
dfc2AT=sqrt((4*Fc2AT)/pi);
SwindAT=(Fc2AT*N2);
dAt=sqrt((SwindAT*4)/pi);
%
%
tAT1=(SwindAT/(hb))*1.10;
Laxju=hw-((hw*Kw)/2);
tAT2=tAT1*2;
% dintAT=(Dextbt+4*a)
dintAT=(Dextbt+6*a);%adequa��o do projeto GHR
%DextAT=(dintAT+2*a+tAT2)%di�metro em mil�metros
DextAT=(dintAT+2*tAT2);%di�metro em mil�metros
%DextAT=(Dextbt+(2*Kw*ww)+tAT2)
dMAT=(dintAT+DextAT)/2; %di�metro principal na baixa tens�o em mil�metros
LmATc=(pi*dMAT);% % coprimento mil�metros ( valor a ser utilizado na profundidade do FEMM para c�lculo das perdas do cobre na BT)
%Calculo do peso dos condutores de alum�nio
CompAT=LmATc*N2;
Fc2=I2c/J2;
dfc2=sqrt((Fc2*4)/pi);
VALAT= (CompAT*Fc2)*3; %o valor 2.7 g/cm3= 2.7^-6 Kg/mm3  O valor 3 � devido ao
%fato do transformador ser trif�sico. (03 bobinas).
MAT3=(VALAT*(2.7)*10^-6);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Lmbt=(3.1416*dmbt);
%Calculo das perdas no cobre
Cmbt=(Lmbt*N1*10^-3);
CmAT=(LmATc*N2*10^-3);
R1=(0.02857)*((Cmbt)/(Fc1));
R1=(0.02857)*((Lmbt*N1*10^-3)/(Fc1));
R2=(0.02857)*((CmAT)/(Fc2AT));
R2=(0.02857)*((LmATc*N2*10^-3)/(Fc2AT));
%I2menor=(Qf/13.80)
I2=(Qf/V2);
PJ1=(R1*((I1)^2)*3);
PJ2=(R2*((I2)^2)*3);
Pj=PJ1+PJ2;
Fc=sqrt(Po/Pj);
PJ2=(R2*((I2)^2)*3);
Pj=PJ1+PJ2;
Fc=sqrt(Po/Pj);
PerdasT=(Po+Pj);
%Calculo da reat�ncia referida ao prim�rio.
R2ref=R2*((N1/N2)^2);%Resist�ncia do  enrolamento secund�rio (AT) referida para o primario (BT)
Rt=R1+R2ref; %Resist�ncia total referida para o enrolamento prim�rio
%Pj=(Rt*(I1^2))*3 %Perdas no cobre com o enrolamento de At referido ao prim�rio
Ac=(Et/(4.44*f*Bm)); %�rea deve estar em m2
VmL=(V1*1000)*sqrt(2);
Fluxonominal2=(VmL/sqrt(3))/(2*pi*f);
VmAT=(V2*1000)*sqrt(2);
FluxonominalAT=VmAT/(2*pi*f);
Vm=(Vf1*1000)*sqrt(2);
%%%%%%%%%%%%%%%%%%%%%%
Fr=(Br*Ac); %fluxo em wb/m2
Fs=(Bs*Ac);%fluxo em wb/m2
%
VAc=Perda_VA(Bm,0); %Pot�ncia de excita��o por KG nas colunas
VAj=Perda_VA(By,0); %Pot�ncia de excita��o por KG nas culatras
S0=VAc*Mc+VAj*Mj;
Fp2=Po/S0;
Pfo=Po/3; % Calculo do Ramo magnetizante do transformador trif�sico representado pelo diagrama monof�sico, para calcular e Indut�ncia Magn�tica LM
Vo=(Vf1*1000);
Io=sqrt(Ip^2+Iq^2);
Rm=Pfo/(Io^2);
Zm=Vo/Io;
Xm0=sqrt(Zm^2-Rm^2);
%
Pfo=Po/3; % Calculo do Ramo magnetizante do transformador trif�sico representado pelo diagrama monof�sico, para calcular e Indut�ncia Magn�tica LM
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
Wa=2*pi*f;

L=(Mo*(N1^2)*So)/(hb-0.45*dc); % Hayt J.r,W.A Buck J.A 2013 - Eletromagnetismo
XL=(Wa*L)/1000;
f=60;%Entrada da frequencia em Hz
S=Q;%Entrada da pot�ncia em KVA.
VA=13.8;%Entrada da alta tens�o em KV.
VfA=VA;
Vb=220; %Entrada da tens�o de linha do lado de baixa em V.
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
Zp=(Vccb/Vfb)*100;
Rccb=Rb+(RA/(ktrafo^2));
VccRb=Ifb*Rccb;
Rp=(VccRb/Vfb)*100;
Xp=sqrt(Zp^2-Rp^2);
Fpo=Ip/Io;
Iop=(Io/Ifb)*100;
f=60;%Entrada da frequencia em Hz
S=150;%Entrada da pot�ncia em KVA.
VA=13.8;%Entrada da alta tens�o em KV.
VfA=VA;
Vb=220; %Entrada da tens�o de linha do lado de baixa em V.
Vfb=Vb/(sqrt(3));
Zp=Zp; %Entrada da imped�ncia percentual.
Rp=Rp;%Entrada da Resistencia percentual.
Iop=Iop;%Entrada da corrente a vazio em percentual.
Fpo=Fpo; %fator de potencia do transformador a vazio
%C�lculos
%1- Rela��o de transforma��o
ktrafo=(VfA*1000)/(Vfb);
%2- C�lculo das correntes
IfA=(S/3)/VfA;
ILA=IfA*(sqrt(3));
Ifb=(S*1000/3)/Vfb;
ILb=Ifb;
%3- Corrente a vazio
Io=Io;
Iob=Io;
IoA=Iop*(IfA)/100;
IopicoA=IoA*(sqrt(2)); %Este valor � o valor a ser inserido no ATP
Iopicob=IopicoA*ktrafo;
Iob=Iop*(Ifb)/100;
%
%4- Pot�ncia a vazio (Po)
Pof=VA*1000*IoA*Fpo;
Po3=3*Pof;
Po3=Po; %m�todo antigo tira coment�rio
%
%5- Imped�ncia do prim�rio e secund�rio (Zp e Zs)
%Imped�ncia da alta
ZbaseA=(VA)^2/(S/(3*1000));
ZbaseB=(Vfb)^2/(S*1000/3);
ZtA=(ZbaseA*Zp)/100;
ZA=ZtA/2;
%Imped�ncia da baixa
Zb=ZA/ktrafo^2;
%
%6- Resistencia da alta e baixa tens�o - M�todo antigo comentar as duas
%linhas abaixo
%RA=(Rp*ZbaseA)/(2*100)
%Rb=RA/ktrafo^2
%
%7- Pot�ncia de curto-circuito
Pccf=RA*IfA^2+Rb*Ifb^2;
Pcc3=3*Pccf;
%8- Reat�ncia do prim�rio e secund�rio
XA=sqrt(ZA^2-RA^2);
Xb=sqrt(Zb^2-Rb^2);
%
%9- Indut�ncia do prim�rio e secund�rio (LA e Lb)
LA=(XA/Wa)*1000; %Indut�ncia em (mH)
Lb=(Xb/Wa)*1000; %Indut�ncia em (mH)
%
%10- Resist�ncia de Magnetiza��o
RmagA=(VA*1000)^2/Po3;
Rmagb=(Vfb)^2/Po3;
%
%11- Fluxo de magnetiza��o (Y0)
FmagA=VA*1000/(4.44*60);
Fmagb=Vfb/(4.44*60);
LmAT=LA;
Lma=Lm*1.01;%Distribui��o das densidades de fluxo
Lmb=Lm*1.012;%Distribui��o das densidades de fluxo
Lmc=Lm*1.0104;%Distribui��o das densidades de fluxo

LmaAT=LmAT*1.01;%Distribui��o das densidades de fluxo
LmbAT=LmAT*1.012;%Distribui��o das densidades de fluxo
LmcAT=LmAT*1.0104;%Distribui��o das densidades de fluxo

% LmaAT=LaAT

Fp=Pfo/(Vo*Io);
%C�lculo das correntes  do ensaio do transformador conforme  planilha  GHR
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

Lsc=(V1^2)/Q;
LscAT=(V2^2)/Qf;


%
Wa=2*pi*f;
%R1=0.0082
Rt=R1;
RtAT=R2;
Rsc=0;
R=Rt+Rsc;
x=0;

%Adapta��es para o transformador trif�sico
fluxo1=Bm*Ac;
fluxo2=Bs*Ac;
Ln=(hw)*10^-3;
Hs=curva_BH(Bs,0);
Hns=curva_BH(Bm,0);%Busca os valores na planilha da intensidade de campo, arquivo TXT
F1=Hns*Ln; %Hns � a intensidade de campo na regi�o n�o saturada
F2=Hs*Ln; %Hs � a intensidade de campo na regi�o  saturada
La=((N1^2)*fluxo1)/(F1);%C�lculo da indut�ncia na regi�o n�o saturada, conforme f�rmula apostila de convers�o  pag 15 e dados de histerese do material utilizado
Lbs=N1^2*((fluxo2-fluxo1)/(F2-F1)); %C�lculo da indut�ncia na regi�o saturada, conforme f�rmula apostila de convers�o  pag 15 e dados de histerese do material utilizado
Ls=Lbs+Lsc;
LaAT=(N2^2*fluxo1)/F1;
LbsAT=N1^2*((fluxo2-fluxo1)/(F2-F1));
LsAT=LbsAT+LscAT;
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

Limb=(Mo*(N1^2)*So)/(hw);

Imax=([Vm/(Wa*(Lsc+Limb))]*[2-(((Wa*(Br-Bs))*N1*So)/Vm)])/10000;
t1=(acos((((Yr-Ys)*Wa)/Vm)+1)/Wa);
t1AT=(acos((((YrAT-YsAT)*Wa)/VmAT)+1)/Wa);
alfa=0;
% alfa=-((2*pi)/3);
% alfa=((2*pi)/3);

tpk=0.0000:1/6000:1/60;

%Corrente de exita��o
FluxoA=Fluxonominal2*(sin(Wa.*tpk));
alfa=0;
Vma=Vm*cos(alfa);
aa=(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma));
r2=R^2;
Xm=(Wa*Lm);
Ibt=(Vm*(R*sin(Wa*t1)-Wa*Lm*cos(Wa*t1)+Wa*Lm*exp(-(R*t1)/Lm)))/(R^2+(Wa*Lm)^2);
Ibta=((Vma*(R*sin(Wa*t1)-Wa*Lma*cos(Wa*t1)+Wa*Lma*exp(-(R*t1)/Lma)))/(R^2+(Wa*Lma)^2));
Inrush=(Ibt.*(exp(-R.*(tpk-t1))/Ls))+(((Vm*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vm*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacao=Inrush/I1;
Imaximo=max(Inrush);
Irel=Imaximo/I1;
Inrusha=(Ibta.*(exp(-R.*(tpk-t1))/Ls))+(((Vma*R).*[sin(Wa.*tpk)-sin(Wa*t1).*exp((-R.*(tpk-t1))/Ls)])+((Vma*Wa*Ls).*[(cos(Wa*t1).*exp((-R.*(tpk-t1))/Ls)-cos(Wa.*tpk))]))/(R^2+(Wa*Ls)^2);
Irelacaoa=Inrusha/I1;
Imaximoa=max(Inrusha);
Irela=Imaximoa/I1;
%Entre com o valor do tempo de maior corrente da fase desejada
%tpka=0.0013890 %Fase A
%tpkb=0.0069445 % Fase B
%tpkc=0.0041597%Fase C
Mativa=MAT3+Mbt3+MT;
f2=(MAT3+Mbt3+MT);
f1=PerdasT;
%% APLICANDO PUNI��O NOS LIMITES: tira coment�rios abaixo restri��es perdas totais, massa ativa, fator de carga para rendimento m�ximo e imped�ncia percentual
if PerdasT > 2000;
f2=(MAT3+Mbt3+MT)+(PerdasT-2000)*100;  %1000
f1=PerdasT+(PerdasT-2000)*100;    %3000
end 
%%%%%%%%%%%%%%

%%%%%%%%%%%
if Mativa > 610;
f2=(MAT3+Mbt3+MT)+(Mativa-610)*10;  %1000
f1=PerdasT+(Mativa-610)*10;       %3000
end
if PerdasT < 2000;
if Mativa < 610    
if Fc > 0.60;
f2=(MAT3+Mbt3+MT)+(Fc-0.60)*700;  %5000 ok 2000 ok
f1=PerdasT+((Fc-0.60))*700;       %5000 ok 2000 ok
end 
end
end

DadosFinais = [H,W,hw,ww,wc,hy,Prof,Proffem,d,Io,Lb,Po,Pj,f1,MAT3,Mbt3,MT,f2,I1,Imaximoa,Irela,hb,Fc,Zp];
% f2=(MT*22.00+(Mbt3+MAT3)*10.50)/32.50
%
%% SA�DA FINAL
z=[f1
      f2];
   
end
