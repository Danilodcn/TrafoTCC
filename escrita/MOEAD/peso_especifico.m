function P=pesoespecifico_BP(B,exibe_grafico)
%H=curva_BH(B,exibe_grafico)
% Curva de magnetizacao exata
material='pesoespecifico.txt';
fid = fopen(material,'r');
dados = textscan(fid,'%f32%f32');
fclose(fid);
B_exata = dados{1};
P_exata = dados{2};
% Aproximação da curva de magnetizacao
P = interp1(B_exata,P_exata,B);
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(P_exata,B_exata,'-b', ...
    P,B,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('B (T)')
xlabel('P (A*esp)')
end