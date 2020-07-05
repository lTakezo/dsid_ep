import requests,json
import sys # sys.argv[1]

#querylist = [input('Escolha um destino ou lugar :'), input('O que deseja procurar? (Restaurantes, Atracoes, Hoteis): ')] #se querylist[1] for vazio, irá retornar informações gerais
querylist = []

#query = querylist[1]

headers = {}
locationid = 0

def set_headers():
    global headers
    headers = {'x-rapidapi-host': "tripadvisor1.p.rapidapi.com",
               'x-rapidapi-key': "7e0cb6767amshc461cd7ff6549bap157edajsne90dd1378186"
            }

set_headers()

def set_localid(list):
    global locationid

    url = "https://tripadvisor1.p.rapidapi.com/locations/auto-complete"

    querystring = {"lang":"pt_BR","units":"km","query":list[0]}

    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonid = json.loads(response.text)
    locationid = jsonid['data'][0]['result_object']['location_id']

def default(list):
    global locationid

    url = "https://tripadvisor1.p.rapidapi.com/locations/auto-complete"

    querystring = {"lang":"pt_BR","units":"km","query":list[0]}

    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonid = json.loads(response.text)
    locationid = jsonid['data'][0]['result_object']['location_id']

    return response.json()

def queryrestaurant(price):
    url = "https://tripadvisor1.p.rapidapi.com/restaurants/list"

    querystring = {"restaurant_tagcategory_standalone":"10591","lunit":"km","restaurant_tagcategory":"10591","limit":"30","prices_restaurants":price,"currency":"BRL","lang":"pt_BR","location_id":locationid}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def queryhotels(hotelparam):
    url = "https://tripadvisor1.p.rapidapi.com/hotels/list"

    querystring = {"offset":"0","pricesmax":hotelparam[4],"currency":"BRL","limit":"30","order":"asc","lang":"pt_BR","sort":"recommended","location_id":locationid,"adults":hotelparam[0],"checkin":hotelparam[1],"rooms":hotelparam[2],"nights":hotelparam[4]}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

def queryatractions(rating):
    url = "https://tripadvisor1.p.rapidapi.com/attractions/list"

    querystring = {"lang":"pt_BR","currency":"BRL","sort":"recommended","lunit":"km","min_rating":rating,"location_id":locationid}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()

'''
if not querylist[1]:
    default(querylist)
else:
    set_localid(querylist)

if querylist[1] == 'Restaurantes':
    #inp1 = input('Preco minimo restaurante:')
    inp1 = sys.argv[3]
    #inp2 = input('Preco maximo restaurante:')
    inp2 = sys.argv[4]
    price = str(inp1) + '%2C' + str(inp2)
    print(queryrestaurant(price))

if querylist[1] == 'Atracoes':
    #rate = input('Avaliaçao (Min 3 Max 5) : ')
    rate = sys.argv[3]
    print(queryatractions(rate))
    #print(json.dumps(queryatractions(rate), ensure_ascii=False))

    
if querylist[1] == 'Hoteis':
    #hotel_parameters = [input('Quantos adultos serao hospedados? '), input('Dia do Check-in (YYYY-MM-DD): '), input('Numero de quartos: '), input('Numero de noites: '), input('Preco maximo para diaria: ')]
    hotel_parameters = [sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]] 
    #for x in hotel_parameters:
    #    print(x)
    #print(hotel_parameters[0]) # teste
    print(queryhotels(hotel_parameters))
'''
