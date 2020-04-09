import requests
from bs4 import BeautifulSoup

def get_main_news():
    url = 'https://www.cmmedia.es/noticias/castilla-la-mancha/'

    respuesta = launch_request(url)

    contenido_web = BeautifulSoup(respuesta.text, 'lxml')


    noticias = contenido_web.find('ul', attrs={'class':'news-list'})
    articulos = noticias.findChildren('div', attrs={'class':'media-body'})

    noticias = [];

    for articulo in articulos:
        noticias.append({
            'url': articulo.find('h3').a.get('href'),
            'titulo': articulo.find('h3').get_text()
        })

    return noticias


def get_all_info_by_new(noticia):
    
    print(f'Scrapping {noticia["titulo"]}')

    respuesta = launch_request(noticia["url"])

    contenido_web = BeautifulSoup(respuesta.text, 'lxml')

    articulo = contenido_web.find('article', attrs={'class':'post'})

    noticia['fecha'] = articulo.find('time').get_text()
    noticia['articulo'] = articulo.find('div', attrs={'class':'', 'id':''}).get_text()

    return noticia

def launch_request(url):
    try:
        respuesta = requests.get(
            url,
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
        )
        respuesta.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return respuesta


if __name__ == '__main__':
    noticias = get_main_news()

    for noticia in noticias:
        noticia = get_all_info_by_new(noticia)
        print('=================================')
        print(noticia)
        print('=================================')