function I=fluxo_Corrente(F,exibe_grafico)
% Curva de magnetizacao exata
material='fluxo.txt';
fid = fopen(material,'r');
%
%textscan(fid,'%*s'\1);
%
dados = textscan(fid,'%f32%f32');
fclose(fid);
F_exata = dados{1};
I_exata = dados{2};
% Aproximação da curva de magnetizacao
I = interp1(F_exata,I_exata,F);
% Gráfico da curva de magnetização aproximada
if (exibe_grafico == 1)
plot(I_exata,F_exata,'-b', ...
    I,F,'xk')
grid on;
legend('curva exata', ...
    'ponto aproximada')
ylabel('F (T)')
xlabel('I (A)')
end