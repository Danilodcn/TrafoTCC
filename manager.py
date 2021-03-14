import click
from unittest import TestLoader, runner
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
    required=False, 
    type=int,
    help='realiza os testes usando o arquivo "teste_{n}.json"'
    )
def teste(t):
    config = {"n": t}
    dump(config, open("tests/config.json", "w"))
    loader = TestLoader()
    test = loader.discover("tests/")
    testrunner = runner.TextTestRunner()
    testrunner.run(test)


if __name__ == "__main__":
    c()