 clc;
% VarMin=[1.2 1.4 1.50 6.0 0.45 3.4 1.10];        
% VarMax=[1.4 1.6 1.60 7.0 0.55 3.6 1.20];
% n = size(VarMax);
% p.gamma = 0.5;
% p.VarMin = VarMin;
% p.VarMax = VarMax;
% 
% i1 = unifrnd(VarMin, VarMax, n);
% i2 = unifrnd(VarMin, VarMax, n);
% x = Crossover(i1, i2, p);
% x.*rand(n);
% numel(i1);
% size(i1);
% x = pop;
% x = 1:10;
% y = 21:30;
% z = zeros(1, 2*numel(x));
% c = 1;
% for i = 1:numel(x)
%     z(c) = x(i);
%     c = c + 1;
%     z(c) = y(i);
%     c = c + 1;
% end
vetor.Cost = [];
vetor.Y = [];

po = repmat(vetor, 1, 10);

for i = 1:10
    po(i).Cost = rand();
    po(i).Y = rand() ;
end
s = elimina(po);
s1 = po;



