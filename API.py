from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pyodbc
from googletrans import Translator

translator = Translator()

app = Flask(_name_)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Configuração de conexão com o banco de dados
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-R28C6PJL\SQLEXPRESS;'
                      'Database=CatalogoFilmes;'
                      'Trusted_Connection=yes;')

# Função para realizar o Web Scraping do IMDb e inserir dados no banco de dados


@app.route('/api/filmes', methods=['GET'])
def get_filmes():
    # Consulta o banco de dados para obter os filmes de todas as tabelas
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 'Netflix' as Origem, Titulo, Genero, AnoLancamento, Descricao, Elenco FROM Netflix
        UNION ALL
        SELECT 'PrimeVideo' as Origem, Titulo, Genero, AnoLancamento, Descricao, Elenco  FROM PrimeVideo
        UNION ALL
        SELECT 'HBOMax' as Origem, Titulo, Genero, AnoLancamento, Descricao, Elenco FROM HBOMax
        UNION ALL
        SELECT 'Crunchyroll' as Origem, Titulo, Genero, AnoLancamento, Descricao, Elenco FROM Crunchyroll
        UNION ALL
        SELECT 'Paramount' as Origem, Titulo, Genero, AnoLancamento, Descricao, Elenco FROM Paramount
    """)
    filmes = cursor.fetchall()

    # Formate os dados como JSON
    filmes_json = [{'Origem': filme.Origem, 'Titulo': filme.Titulo, 'Genero': filme.Genero, 'AnoLancamento': filme.AnoLancamento, 'Descricao': filme.Descricao, 'Elenco': filme.Elenco} for filme in filmes]

    return jsonify(filmes_json)


if _name_ == '_main_':
    # Rota para realizar o Web Scraping e armazenar dados no banco de dados
    t = 51
    cont = 1
    SemErro = True 

    url_Netflix = 'https://www.imdb.com/search/title/?companies=co0144901&ref_=fn_co_co_1'
    url_PrimeVideo = 'https://www.imdb.com/search/title/?companies=co0476953&ref_=fn_co_co_2'
    url_HBOMax = 'https://www.imdb.com/search/title/?companies=co0754095&ref_=fn_co_co_1'
    url_Crunchyroll = 'https://www.imdb.com/search/title/?companies=co0251163&ref_=fn_co_co_1'
    url_Paramount = 'https://www.imdb.com/search/title/?companies=co0023400&ref_=fn_co_co_1'
    url_GloboPlay = 'https://www.imdb.com/search/title/?companies=co0593772&ref_=fn_co_co_1'

    onde_Gravar = ''
    while SemErro:
        
        if cont == 1:
            onde_Gravar = 'Netflix'
            response = requests.get(url_Netflix)
        elif cont == 2:
                response = requests.get(f'https://www.imdb.com/search/title/?companies=co0144901&start={t}&ref_=adv_nxt')
                #t += 50
                

        elif cont == 3:
            onde_Gravar = 'PrimeVideo'
            response = requests.get(url_PrimeVideo)
        elif cont == 4:
                response = requests.get(f'https://www.imdb.com/search/title/?companies=co0476953&start={t}&ref_=adv_nxt')
                #t += 50
            

        elif cont == 5:
            onde_Gravar = 'HBOMax'
            response = requests.get(url_HBOMax)
        elif cont == 6:
                response = requests.get(f'https://www.imdb.com/search/title/?companies=co0754095&start={t}&ref_=adv_nxt')
                #t += 50

        elif cont == 7:
            onde_Gravar = 'Crunchyroll'
            response = requests.get(url_Crunchyroll)
        elif cont == 8:
                response = requests.get(f'https://www.imdb.com/search/title/?companies=co0251163&start={t}&ref_=adv_nxt')
                #t += 50

        elif cont == 9:
            onde_Gravar = 'Paramount'
            response = requests.get(url_Paramount)
        elif cont == 10:
                response = requests.get(f'https://www.imdb.com/search/title/?companies=co0023400&start={t}&ref_=adv_nxt')
                #t += 50

        cont += 1 
        if cont == 11:
            SemErro = False

        

        soup = BeautifulSoup(response.text, 'html.parser')

    
        html_titulo = soup.find_all("a", href=lambda href: href and "/title/" in href)
        titulos_seriesCompletos = [element.text for element in html_titulo]

        titulos_series = []
        for serie in titulos_seriesCompletos:
            if serie != 'Big Bang: A Teoria':
                titulos_series.append(serie)

        titulos_series = [x for x in titulos_series if x != 'X']
        titulos_series = [x for x in titulos_series if x != ' \n']
        titulos_series = [x for x in titulos_series if x != 'Next »']
        titulos_series = [x for x in titulos_series if x != '« Previous']
        titulos_series = titulos_series[13:]




        html_genero = soup.find_all("span", class_="genre")
        generosCompletos = [element.text for element in html_genero]
        generos = []
        generos = [string.strip() for string in generosCompletos]



        html_anoLancamento = soup.find_all("span", class_="lister-item-year text-muted unbold")
        anoLancamentosCompleto = [element.text for element in html_anoLancamento]
        anoLancamentos = [item.split('–')[0] for item in anoLancamentosCompleto]
        for i in range(len(anoLancamentos)):
            anoLancamentos[i] = anoLancamentos[i].replace("(", "").replace(")", "").replace("I ", "").replace("I", "").replace('V ', '').replace(' TMovie', '').replace(' Video', '').replace(' TSpecial', '')




        html_descricao= soup.find_all("p", class_="text-muted")
        descricoesCompleta = [element.text for element in html_descricao]
        descricoes = descricoesCompleta[1::2]
        for i in range(len(descricoes)):
            descricoes[i] = descricoes[i].replace("\n", "")



        html_elenco = soup.find_all("a", href=lambda href: href and "/name/" in href)
        elencosCompleto = [element.text for element in html_elenco]
        elencos = []
        for i in range(0, len(elencosCompleto), 4):
            grupo = elencosCompleto[i:i+4]
            grupo_combinado = ', '.join(grupo)
            elencos.append(grupo_combinado)
        cursor = conn.cursor()


        cursor.execute("SELECT Titulo FROM Netflix")
        banco_Netflix = [row.Titulo for row in cursor.fetchall()]

        cursor.execute("SELECT Titulo FROM PrimeVideo")
        banco_PrimeVideo = [row.Titulo for row in cursor.fetchall()]

        cursor.execute("SELECT Titulo FROM HBOMax")
        banco_HBOMax = [row.Titulo for row in cursor.fetchall()]

        cursor.execute("SELECT Titulo FROM Crunchyroll")
        banco_Crunchyroll = [row.Titulo for row in cursor.fetchall()]

        cursor.execute("SELECT Titulo FROM Paramount")
        banco_Paramount = [row.Titulo for row in cursor.fetchall()]

        for i in range(50):
            titulo = titulos_series[i]
            genero = generos[i]
            anoLancamento = anoLancamentos[i]
            descricao = descricoes[i]
            elenco = elencos[i]


            if (onde_Gravar == 'Netflix') and titulo not in banco_Netflix:
                cursor.execute("INSERT INTO Netflix (Titulo, Genero, AnoLancamento, Descricao, Elenco) VALUES (?, ?, ?, ?, ?)", (titulo, genero, anoLancamento, descricao, elenco))
                conn.commit()
                
            elif (onde_Gravar == 'PrimeVideo') and titulo not in banco_PrimeVideo:
                cursor.execute("INSERT INTO PrimeVideo (Titulo, Genero, AnoLancamento, Descricao, Elenco) VALUES (?, ?, ?, ?, ? )", (titulo, genero, anoLancamento, descricao, elenco))
                conn.commit()
            
            elif (onde_Gravar == 'HBOMax') and titulo not in banco_HBOMax:
                cursor.execute("INSERT INTO HBOMax (Titulo, Genero, AnoLancamento, Descricao, Elenco) VALUES (?, ?, ?, ?, ? )", (titulo, genero, anoLancamento, descricao, elenco))
                conn.commit()
        
            elif (onde_Gravar == 'Crunchyroll') and titulo not in banco_Crunchyroll:
                cursor.execute("INSERT INTO Crunchyroll (Titulo, Genero, AnoLancamento, Descricao, Elenco) VALUES (?, ?, ?, ?, ? )", (titulo, genero, anoLancamento, descricao, elenco))
                conn.commit()
            
            elif (onde_Gravar == 'Paramount') and titulo not in banco_Paramount:
                cursor.execute("INSERT INTO Paramount (Titulo, Genero, AnoLancamento, Descricao, Elenco) VALUES (?, ?, ?, ?, ? )", (titulo, genero, anoLancamento, descricao, elenco))
                conn.commit()


    # Inicie o servidor Flask
    app.run(debug=True)