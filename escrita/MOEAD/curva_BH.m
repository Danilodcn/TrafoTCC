function H=curva_BH(B,exibe_grafico)
% Curva de magnetizacao exata
material='curvaBH.txt';
fid = fopen(material,'r');
%
%textscan(fid,'%*s'\1);
%
dados = textscan(fid,'%f32%f32');
fclose(fid);
B_exata = dados{1};
H_exata = dados{2};
% Aproximação da curva de magnetizacao
H = interp1(B_exata,H_exata,B);
% H = interp1(B_exata,H_exata,B,'spline');
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(H_exata,B_exata,'-b', ...
    H,B,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('B (T)')
xlabel('H (A*esp)')
end