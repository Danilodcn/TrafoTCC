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

function y=Crossover(x1,x2,params)
ax1=x1;
ax2=x2;
params=params;
numelx1=numel(x1);
tamanho=size(x1);

    gamma=params.gamma;
    VarMin=params.VarMin;
    VarMax=params.VarMax;
    r = rand() * 5;
    alpha=unifrnd(-gamma * r,gamma * r, size(x1));
%        alpha=unifrnd(-1-gamma ,1+gamma , size(x1));
    %alpha=unifrnd(0, gamma,size(x1));
    
    y=alpha.*x2 +(1-alpha).*x1;

    
    for k = 1:numel(x1)
        a = VarMin(k);
        b = VarMax(k);
        c = y(k);
        y(k) = corrige(a, b, c);
    end
    
end

function d = corrige(a, b, x)
    k = 1 + rand() * 4;
    k = round(k, 4);
    if x < a
       d = b - (b - a) / a * x;;
    elseif x > b
        d = (b - a) * exp(-k * (x - b)) + a;
    else 
        d = x;
    end
    
    
end

function d = media(a, b, c)
    if c < a;
        d = c * (b - a) / a + a;
    elseif c > b
        while c >= b
            c = c / 2;
        end
        if c >= a
            d = c;
        elseif c <= a
            d = c * (b - a) / a + a
        end
    else
        d = c;
    end
end
    