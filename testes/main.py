import getpass
import hashlib
from dataclasses import dataclass, asdict
import json

print("Bem-vindo ao NUAP")


@dataclass
class Usuario:
  ra: int
  email: str
  senha: str
  confirmacao_senha: str

@dataclass
class Dados:
  opcao: int

usuarios_obj = []

def menu_inicial():
  print("BEM VINDO AO NUAPA")
  print("Opção 1 - Cadastro")
  print("Opção 2 - Login")
  print("Opção 3 - Sair")

  opcao = int(input('Digite a opção desejada: '))
  if opcao == 1:
    cadastro()
    return Dados(opcao)
  elif opcao == 2:
    login()
    return Dados(opcao)
  else:
    print("Opção inválida. Por favor, digite novamente..")


def cadastro():
  ra = input("Informe o seu RA, apenas em números: \n")
  email = input("Informe por gentileza o seu e-mail: \n")
  senha = tratar_senha(getpass.getpass('Informe por gentileza qual será a sua senha: \n'))
  confirmacao_senha = tratar_senha(getpass.getpass("Confirme a senha inserida por gentileza: \n"))

  while senha != confirmacao_senha:
    print("Senhas não coincidem. Por favor, preencha o cadastro novamente.")

    if senha == confirmacao_senha:
      print("Senhas coincidem, prosseguindo para o cadastro...")
      break

  print(f"Usuário com o RA: {ra} cadastrado com sucesso! Guardando no banco de arquivos...")
  usuario_gerado = Usuario(ra, email, senha, confirmacao_senha)
  usuarios_obj.append(usuario_gerado)

  with open('usuarios.txt', 'w+') as arquivo:
    usuarios_dict = list(map(asdict, usuarios_obj))
    usuarios_json = json.dumps(usuarios_dict, indent=4)
    arquivo.write(usuarios_json)
  
  return usuario_gerado


def login():
  while True:
    valida_login = input("Olá, bem-vindo! Você já possui cadastro do sistema? Diga SIM para realizar o login, caso contrário, informe NÃO para realização do cadastro. \n").lower()
    valida_confirmacao = ['sim', 'ss', 's']

    if valida_login in valida_confirmacao:
      ra_login = input("Informe seu RA: \n")
      senha_login = getpass.getpass("Informe sua senha: \n")
      senha_hash = tratar_senha(senha_login)

      with open('usuarios.txt', 'r') as arquivo:
        usuarios_json = arquivo.read()
        usuarios_dict = json.loads(usuarios_json)
        usuarios_obj = list(map(lambda d : Usuario(**d), usuarios_dict))

      for usuario in usuarios_obj:
        if usuario.ra == ra_login and usuario.senha == senha_hash:
          central_app()
          break
        else:
          print("RA ou senha incorretos.")
      break

    else:
        print("Saindo do App Nuapa...")
        break

def central_app():
  print(f"Login bem sucedido!!! O usuário, tendo permissões e acesso a serviços deste software.")

def tratar_senha(senha):
  hash_sha256 = hashlib.sha256()
  hash_sha256.update(senha.encode('utf8'))
  return hash_sha256.hexdigest()



# if __name__ == '__main__':
#   menu_inicial()