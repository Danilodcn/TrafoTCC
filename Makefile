modo_grafico:
	@echo "Executando a interface grafica"
	pyuic5.exe .\GUI\main.ui -o .\GUI\main.py
	python .\GUI\teste.py

algoritmo:
	@echo REALIZANDO OS TESTES APENAS DO AG
	python ./manager.py teste -v --ag -error 0.001 -t 13 -npop 20

ag_grafico:
	@echo REALIZANDO OS TESTES APENAS DO AG
	python ./manager.py teste -v --ag -g -error 0.001 -t 13 -npop 20

teste:
	@echo REALIZANDO OS TESTES
	python ./manager.py teste -v -error 0.001 -t 13 -npop 20

grafico:
	@echo REALIZANDO OS TESTES
	python ./manager.py teste -v -g -error 0.001 -t 13 -npop 20

shell:
	pipenv shell
