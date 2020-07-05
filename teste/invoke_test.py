import json, requests
from flask import jsonify

x = '''{"xesquedele": "brelelele"}'''
meujson = json.loads(x)

resposta = json.loads(requests.post("http://127.0.0.1:5000/pacotesapi", data={"xesquedele":"brelelele"}).content)
#resposta = json.loads(requests.post("http://127.0.0.1:5000/pacotesapi", data=meujson).content)

print(resposta)