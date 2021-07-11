function B=curva_HB(H,exibe_grafico)
% Curva de magnetizacao exata
material='curvaHB.txt';
fid = fopen(material,'r');
%
%textscan(fid,'%*s'\1);
%
dados = textscan(fid,'%f32%f32');
fclose(fid);
H_exata = dados{1};
B_exata = dados{2};
% Aproximação da curva de magnetizacao
B = interp1(H_exata,B_exata,H);
%B = interp1(H_exata,B_exata,H);
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(B_exata,H_exata,'-b', ...
    B,H,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('H (A*esp)')
xlabel('B (T)')
end