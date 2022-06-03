%
% Copyright (c) 2015, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YPEA124
% Project Title: Implementation of MOEA/D
% Muti-Objective Evolutionary Algorithm based on Decomposition
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

clc;
clear;
close all;


tic
CostFunction=@(x) Trafo53(x);  % Cost Function
nVar=7; 
VarSize=[1 nVar];   % Decision Variables Matrix Size
VarMin=[1.2 1.4 1.50 6.0 0.45 3.4 1.10];         % Lower Bound of Variables
VarMax=[1.4 1.6 1.60 7.0 0.55 3.6 1.20];         % Upper Bound of Variables

[nTemp, ~] = CostFunction(unifrnd(VarMin,VarMax,VarSize));
nObj=numel(nTemp);


%% MOEA/D Settings


MaxIt=100;  % Maximum Number of Iterations

nPop=50 ;   % Population Size (Number of Sub-Problems)

% nCrossover = 30;    %Numero de reproduções por geração

nArchive=80; % Número de soluções

%T=max(ceil(0.15*nPop),2);    % Number of Neighbors
T=max(ceil(0.1*nPop),2);

T=min(max(T,2),15);

crossover_params.gamma=0.50;
crossover_params.VarMin=VarMin;
crossover_params.VarMax=VarMax;

%% Initialization

% Create Sub-problems
sp=CreateSubProblems(nObj,nPop,T);
% Empty Individual
empty_individual.Position=[];
empty_individual.Cost=[];
empty_individual.g=[];
empty_individual.IsDominated=[];

% Initialize Goal Point

z=zeros(nObj,1);

% Create Initial Population
pop = repmat(empty_individual,nPop,1);
for i=1:nPop
    pop(i).Position=unifrnd(VarMin,VarMax,VarSize);
    pop(i).Cost=CostFunction(pop(i).Position);
    z=min(z,pop(i).Cost);
end

for i=1:nPop
    pop(i).g=DecomposedCost(pop(i),z,sp(i).lambda);
end

% Determine Population Domination Status
pop=DetermineDomination(pop);

% Initialize Estimated Pareto Front
EP=pop(~[pop.IsDominated]);

iMelhorInd = 1;

%% Main Loop
numeropop=numel(pop)

for it=1:MaxIt
    
    pop2 = [];
    popMutacao = [];
    
%     for i=1:round(nPop)
      for i=1:(nPop)
        
        % Reproduction (Crossover)
        T = 1:numel(pop);
        K=randsample(T,2);

        
%         j1=sp(i).Neighbors(K(1))
%         p1=pop(j1)
%         
%         j2=sp(i).Neighbors(K(2));
%         p2=pop(j2);
        p1 = pop(K(1));
        p2 = pop(K(2));
        
        y=empty_individual;
        y.Position=Crossover(p1.Position,p2.Position,crossover_params)
        
        [y.Cost, ~]=CostFunction(y.Position);
        
        pop2 = [pop2
                y];
            
            
% Comentários abaixo para retirar a mutação Danilo            
        K = randsample(T, 1);
        selecionado = pop(K(1));
        y.Position = mutacao(selecionado.Position, crossover_params, it, MaxIt);
        [y.Cost, ~]=CostFunction(y.Position);
        
        popMutacao = [popMutacao
                      y];
       z=min(z,y.Cost);
        
%         for j=sp(i).Neighbors
%             y.g=DecomposedCost(y,z,sp(j).lambda);
%             if y.g<=pop(j).g
%                 pop(j)=y;
%             end
%         end
        
    end

    pop = [pop
           pop2
           popMutacao
            ];
        
    % Determine Population Domination Status
    pop=DetermineDomination(pop);
    pop=pop(~[pop.IsDominated]);
%     
%     EP=[EP
%         ndpop]; %#ok
    EP = [EP
          pop];
    EP=DetermineDomination(EP);
    EP=EP(~[EP.IsDominated]);
        
%     if numel(EP)>nArchive
%         Extra=numel(EP)-nArchive
%         ToBeDeleted=randsample(numel(EP),Extra)
%         EP(ToBeDeleted)=[];
%     end
    
%     while numel(EP) > nArchive
%         apaga = randsample(numel(EP), 1);
%         EP(apaga) = [];
%     end
    
    EP = elimina(EP, nArchive);
    pop = EP;
    
    % Plot EP se quiser acompanhar o grafico ao vivo    
    figure(1);
    PlotCosts(EP);
    pause(0.01);
    
%  figure(2);
% %plot(BestCost,'LineWidth',2);
% %plot(BestCost,'LineWidth',2);
% PlotCosts(EP);
% legend('ED');
% xlabel('Perdas (Kw)')
% ylabel('Massa Ativa [Kg]')
% grid on;
%PSO=importdata('solutionPSO.TXT')
%X=[1:1:50];
%hold on
%plot(X,PSO,'LineWidth',2,'Color','red','marker','o');
%plot(tpk,Inrushc,'LineWidth',2,'Color','red','marker','s');
%legend('ED','PSO');
%save solutionED10.txt  BestCost -ascii
    
%     figure(2);
%     PlotCosts2(EP);
%     pause(0.01);

    
    % Display Iteration Information
    disp(['Iteration ' num2str(it) ': Number of  Solutions = ' num2str(numel(EP))]);
    
end

%% Reults

disp(' ');

EPC=[EP.Cost];

%for j=1:nPop
 for j=1:numel(EP)
    [~, Projetos(j,:)] = CostFunction(EP(j).Position);
 end

 plot(Projetos(:, 14), Projetos(:, 18),'o');
    xlabel('Perdas Totais [W]');
    ylabel('Massa Total [kg]');
    grid on;

for j=1:nObj
    
    disp(['Objective #' num2str(j) ':']);
    [minEPC, imin] = min(EPC(j,:));
    disp(['      Min = ' num2str(minEPC)]);
    disp(['      Max = ' num2str(max(EPC(j,:)))]);
    disp(['    Range = ' num2str(max(EPC(j,:))-min(EPC(j,:)))]);
    disp(['    St.D. = ' num2str(std(EPC(j,:)))]);
    disp(['     Mean = ' num2str(mean(EPC(j,:)))]);
    [~, DadosFinais]=CostFunction(EP(imin).Position);
    disp(['     Resultado Final = ' num2str(DadosFinais)]);
    disp(['     Position = ' num2str(EP(imin).Position)]);
    Res(j,:)=[(DadosFinais)];
    Pos(j,:)=[(EP(imin).Position)];
    disp(' ');
    
end
xlswrite('0000moedrestricoeszp.xls', Projetos, 'Plan1',  'A2' )

toc

