function [x1, x2]  = mutacao( x, params, g, gMax)
    x1 = x;
    x2 = rand(size(x));
    VarMin=params.VarMin;
    VarMax=params.VarMax;
    x2 = VarMax - (VarMax - VarMin).*x2;
    for i = 1:numel(x)
       Min = VarMin(i);
       Max = VarMax(i);
       r1 = rand();
       if r1 <= 0.5
           x1(i) = x(i) + (Max - x(i)) * f(g, gMax);
       else
           x1(i) = x(i) + (x(i) - Min) * f(g, gMax);
       end
    end

end

function r = f(g, gMax)
    r2 = rand();
    b = 6; % Parametro do algoritmo
    r = r2 * (1 - g / gMax);
    r = r ^ b;
end

