import requests
from bs4 import BeautifulSoup
import pyodbc

t = 1
SemErro = True
cont = 0


lista_Titulo_Netflix= []
lista_Duracao_Netflix = []
lista_Genero_Netflix = []
lista_AnoLancamento_Netflix = []
lista_Descricao_Netflix = []
lista_Elenco_Netflix = []


lista_URL = ["https://www.imdb.com/search/title/?companies=co0144901&ref_=fn_co_co_1"]
while SemErro:

  # try:
  #   response = requests.get(lista_URL[cont])
  # except:
  #   try:
  #     response = requests.get(f"https://www.imdb.com/search/title/?companies=co0144901&start={t}&ref_=adv_nxt")
  #   except:
  #     SemErro = False
  response = requests.get(lista_URL[cont])


  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    #Titulo
    html_titulo = soup.find_all("a", href=lambda href: href and "/title/" in href)
    titulos_series_completos = [element.text for element in html_titulo]



    #Genero
    html_genero = soup.find_all("span", class_="genre")
    generosCompletos = [element.text for element in html_genero]



    #Ano de Lançamento
    html_anoLancamento = soup.find_all("span", class_="lister-item-year text-muted unbold")
    anoLancamentosCompleto = [element.text for element in html_anoLancamento]



    #Descrição
    html_descricao= soup.find_all("p", class_="text-muted")
    descricoesCompleta = [element.text for element in html_descricao]


    #Elenco
    html_elenco = soup.find_all("a", href=lambda href: href and "/name/" in href)
    elencosCompleto = [element.text for element in html_elenco]


    #Limpeza
    titulos_series = []
    for titulo in titulos_series_completos:
      if titulo != 'The Big Bang Theory':
        titulos_series.append(titulo)
    titulos_series = [x for x in titulos_series if x != 'X']
    titulos_series = [x for x in titulos_series if x != ' \n']
    titulos_series = [x for x in titulos_series if x != 'Next »']
    titulos_series = [x for x in titulos_series if x != '« Previous']
    titulos_series.pop(33)
    titulos_series = titulos_series[13:]



    generos = generosCompletos
    generos = [string.strip() for string in generosCompletos]


    anoLancamentos = [item.split('–')[0] for item in anoLancamentosCompleto]
    for i in range(len(anoLancamentos)):
      anoLancamentos[i] = anoLancamentos[i].replace("(", "").replace(")", "").replace("I ", "").replace("I", "")

    descricoes = descricoesCompleta[1::2]
    for i in range(len(descricoes)):
        descricoes[i] = descricoes[i].replace("\n", "")

    elencos = []
    for i in range(0, len(elencosCompleto), 4):
      grupo = elencosCompleto[i:i+4]
      grupo_combinado = ', '.join(grupo)
      elencos.append(grupo_combinado)



    #Exibição
    for i in range(0,len(duracoes)):
      print("Titulo: " + titulos_series[i] +"         Duração: " + str(duracoes[i]) + " min \n")
      print("Genero: " + generos[i] + "         " + "Ano de Lançamento: " + anoLancamentos[i] + "\n")
      print("Descrição: " + descricoes[i] + '\n')
      print("Elencos: " + elencos[i])
      print("---------------------------------------------------\n")


      #Carregamento
      lista_Titulo_Netflix.append(titulos_series[i])
      lista_Duracao_Netflix.append(duracoes[i])
      lista_Genero_Netflix.append(generos[i])
      lista_AnoLancamento_Netflix.append(anoLancamentos[i])
      lista_Descricao_Netflix.append(descricoes[i])
      lista_Elenco_Netflix.append(elencos[i])


    #Verifica se todos os filmes tem seus dados completos
    if len(lista_Titulo_Netflix) == len(lista_Duracao_Netflix) == len(lista_Genero_Netflix) == len(lista_AnoLancamento_Netflix) == len(lista_Descricao_Netflix):
      print("\n\nESTA TUDO CORRETO\n\n")


    #Limitar o teste para apenas uma guia
    SemErro = False
  else:
      SemErro = False
      print("Falha ao acessar a página do IMdb. Código de status:", response.status_code)

  cont += 1
  t += 50

server = 'DESKTOP-DEIVID'
database = 'CatalogoFilmes'
username = 'sa'
password = 'coxinha123'
driver = '{ODBC Driver 17 for SQL Server}'

conexaoBD = f'SERVER={server};DATABASE={database};UID={username};PWD={password};DRIVER={driver}'

conn = pyodbc.connect(conexaoBD)

cursor = conn.cursor()

for i in range(0, len(lista_Titulo_Netflix)):
  valores = (lista_Titulo_Netflix[i], lista_Duracao_Netflix[i], lista_Genero_Netflix[i], lista_AnoLancamento_Netflix[i], lista_Descricao_Netflix[i], lista_Elenco_Netflix[i])
  query = f"INSERT INTO Netflix (Titulo, Duracao, Genero, AnoLancamento, Descricao, Elenco) VALUES (?,?,?,?,?,?)"
  cursor.execute(query, valores)

  conn.commit()

conn.close()