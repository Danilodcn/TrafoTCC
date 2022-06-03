function S=PerdaVA_BS(B,exibe_grafico)
% Curva de magnetizacao exata
material='Perdaaparente.txt';
fid = fopen(material,'r');
%
%textscan(fid,'%*s'\1);
%
dados = textscan(fid,'%f32%f32');
fclose(fid);
B_exata = dados{1};
S_exata = dados{2};
% Aproximação da curva de magnetizacao
S = interp1(B_exata,S_exata,B);
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(S_exata,B_exata,'-b', ...
    S,B,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('B (T)')
xlabel('S (A*esp)')
end