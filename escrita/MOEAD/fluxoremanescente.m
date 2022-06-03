function Br=Densidade_BR(B,exibe_grafico)
% Curva de magnetizacao exata
material='fluxomanescente.txt';
fid = fopen(material,'r');
%
%textscan(fid,'%*s'\1);
%
dados = textscan(fid,'%f32%f32');
fclose(fid);
B_exata = dados{1};
Br_exata = dados{2};
% Aproximação da curva de magnetizacao
Br = interp1(B_exata,Br_exata,B);
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(Br_exata,B_exata,'-b', ...
    Br,B,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('B (T)')
xlabel('Br (T)')
end