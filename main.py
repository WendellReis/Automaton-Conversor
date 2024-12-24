import json

with open('args.json') as arquivo:
    dados = json.load(arquivo)
    
print(dados)