import io
import unittest
import hashlib
import getpass
from unittest.mock import patch
from main import *
from contextlib import redirect_stdout

class TestNuap(unittest.TestCase):

    @patch('getpass.getpass', lambda *args: 'eduardo123')
    def test_menu_inicial_1(self):
        inputs = iter([
            1,
            '1959599',
            'eduevaristo@gmail.com',
            '1959599',
            'eduevaristo@gmail.com',
        ])


        with patch('builtins.input', lambda args: next(inputs)):
            dados = menu_inicial()
            self.assertEqual(dados.opcao, 1)
            
            hash_senha = hashlib.sha256('eduardo123'.encode()).hexdigest()
            dadosCadastro = cadastro()

            self.assertEqual(dadosCadastro.ra, '1959599'),
            self.assertEqual(dadosCadastro.email, 'eduevaristo@gmail.com'),
            self.assertEqual(dadosCadastro.senha, hash_senha),
            self.assertEqual(dadosCadastro.confirmacao_senha, hash_senha)

    @patch('getpass.getpass', lambda *args: 'eduardo123')
    def test_menu_inicial_2(self):
        inputs = iter([
            2,
            'sim',
            '1959599',
            ''
        ])
        
        with patch('builtins.input', lambda args: next(inputs)):
            dados = menu_inicial()
            self.assertEqual(dados.opcao, 2)
            with patch('builtins.input', lambda args: next(inputs)):
                output = io.StringIO()
                with redirect_stdout(output):
                    login()
                output_str = output.getvalue().strip()

                try:
                    self.assertIn('Login bem sucedido!!!', output_str)
                except AssertionError:
                    try:
                        self.assertIn('RA ou senha incorretos.', output_str)
                    except:
                        self.assertIn('Saindo do App Nuapa...', output_str)

    
    def test_tratar_senha(self):
        senha = 'eduardo123'
        senha_hash_esperado = hashlib.sha256(senha.encode()).hexdigest()
        carrega_senha = tratar_senha(senha)

        self.assertEqual(carrega_senha, senha_hash_esperado)
            
    
    def test_central_app(self):
        output = io.StringIO()
        with redirect_stdout(output):
            central_app()
        output_str = output.getvalue().strip()
        self.assertIn('Login bem sucedido!!! O usuário, tendo permissões e acesso a serviços deste software.', output_str)
      