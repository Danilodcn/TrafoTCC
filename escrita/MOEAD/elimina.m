function r = elimina( pop, n)

    r = pop;
    if numel(r) > n
        r = sort(r);
    end
    dist = 2.0;
    c = 0;
    while numel(r) > n
        eliminar = [];
        for j = 1:numel(r)-1
            if dist > distancia(r(j), r(j+1))
                eliminar = [eliminar, j];
                c = c + 1;
            end
        end
         r(eliminar) = [];
        dist = dist * 2;
    end
    c
    c;

%     r = pop;
%     if numel(r) > n
%         r = sort(pop);
%     end
%     
%     toDel = apaga(r, n);
%     r(toDel) = [];

end
 
function toDel = apaga(po, n)

    toDel = [];
    dist = 0.1;
    k = 0;
    n = numel(po) - n;
    while k < n
        dist = dist * 1.5;
        for l = 1:numel(po)-1
           if dist > distancia(po(l), po(l+1))
               toDel = [toDel, l];
               k = k + 1;
           end
           if k >= n
               break
           end
        end
    end

end

function pop = sort(pop)

    for j = 2:numel(pop)
        x = pop(j);
        i = j - 1;
        while i >= 1 && pop(i).Cost(1) < x.Cost(1)
            pop(i+1) = pop(i);
            i = i - 1;
        end
        pop(i+1) = x;
    end

end

function d = distancia(x, y)

    x = x.Cost;
    y = y.Cost;
    dx = x(1) - y(1);
    dy = x(2) - y(2);
    d = sqrt(dx * dx + dy * dy);
end