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
    prompt="Teste", 
    required=True, 
    type=int,
    help='realiza os testes usando o arquivo "teste_{n}.json"'
    )
@click.option(
    "-error", 
    required=True, 
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
def teste(t, error, verbose, npop):
    """
        Exemplo de uso: python .\manager.py teste -t 13 -error 0.001 -v
    """
    
    print("=" * 100)
    error /= 100            # TODO ola mundo, isso
    config = {"n": t, "error": error, "npop": npop}
    dump(config, open("tests/config.json", "w"))
    loader = TestLoader()
    test = loader.discover("tests/")
    verbose = 2 if verbose else 1
    testrunner = runner.TextTestRunner(verbosity=verbose)
    testrunner.run(test)


if __name__ == "__main__":
    c()