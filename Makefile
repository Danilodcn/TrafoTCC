algoritmo:
	@echo REALIZANDO OS TESTES APENAS DO AG
	python ./manager.py teste -v --ag -error 0.001 -t 13 -npop 20

teste:
	@echo REALIZANDO OS TESTES
	python ./manager.py teste -v -error 0.001 -t 13 -npop 20

grafico:
	@echo REALIZANDO OS TESTES
	python ./manager.py teste -v -g -error 0.001 -t 13 -npop 20

shell:
	pipenv shell
