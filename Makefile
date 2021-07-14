teste:
	@echo REALIZANDO OS TESTES
	python ./manager.py teste -v -error 0.001 -t 13 -npop 10

shell:
	pipenv shell
