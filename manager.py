import click
from unittest import TestLoader, runner
import unittest
from json import dump


@click.group()
def c():
    ...

@c.command()
def tests():
    loader = TestLoader()
    test = loader.discover("tests/")
    testrunner = runner.TextTestRunner()
    testrunner.run(test)

@c.command()
@click.option(
    "-t",
    required=False, 
    type=int,
    help='realiza os testes usando o arquivo "teste_{n}.json"'
    )
@click.option(
    "-error", 
    required=False, 
    type=float,
    help='Erro máximo aceitável para os testes em %'
    )
@click.option(
    "-npop", 
    required=False, 
    type=int,
    help='Número de indivíduos na população'
    )
@click.option(
    "-v", "--verbose",
    required=False,
    is_flag=True,
    help="Modo verboso",
)
@click.option(
    "-g", "grafico",
    required=False,
    is_flag=True,
    help="mostrar testes com gráficos"
)
@click.option(
    "--ag",
    required=False,
    is_flag=True,
    help="Realizar apenas os testes referentes ao própria implementação do AG"
)
def teste(t, error, verbose, npop, grafico, ag):
    """
        Exemplo de uso: python .\manager.py teste -t 13 -error 0.001 -v
    """

    print("==#==" * 22)
    error /= 100            # TODO ola mundo, isso
    config = {"n": t, "error": error, "npop": npop, "grafico": grafico, "ag": ag}
    dump(config, open("tests/config.json", "w"))
    loader = TestLoader()
    test = loader.discover("tests/")
    verbose = 2 if verbose else 1
    testrunner = runner.TextTestRunner(verbosity=verbose)
    testrunner.run(test)


if __name__ == "__main__":
    c()