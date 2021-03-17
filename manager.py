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
    help='Para todos os os testes aceita esse erro em %'
    )
def teste(t, error):
    error /= 100
    config = {"n": t, "error": error}
    dump(config, open("tests/json/config.json", "w"))
    loader = TestLoader()
    test = loader.discover("tests/")
    testrunner = runner.TextTestRunner()
    testrunner.run(test)


if __name__ == "__main__":
    c()