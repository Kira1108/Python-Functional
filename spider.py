import requests
from lxml import etree
import time

def get_category(starturl):

    '''
        Get all game caregories
    '''

    try:
        html = requests.get(starturl)
        html.encoding = 'utf-8'
        html = html.text
    except:
        print('Unable to parse starturl')

    selector = etree.HTML(html)

    category_names = selector.xpath("//div[@class='sift-top']/ul/li/p/a/text()")
    category_urls = selector.xpath("//div[@class='sift-top']/ul/li/p/a/@href")

    for name, url in zip(category_names, category_urls):
        yield name, 'http:' + url


def get_game_urls(name, url):

    '''
        Get all game urls
    '''
    try:
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.text
    except:
        print('Unable to parse starturl')

    selector = etree.HTML(html)

    game_names = selector.xpath("//ul[@class='newness-list']/li/p[1]/a/text()")
    game_urls = selector.xpath("//ul[@class='newness-list']/li/p[1]/a/@href")

    for name, url in zip(game_names, game_urls):
        yield name, 'http:' + url


def get_game_info(name, url):

    print('Working on url: {}'.format(url))

    try:
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.text
    except:
        print('Unable to parse starturl')

    selector = etree.HTML(html)

    # ======================== xpath section =================================
    # value: game name
    gamename = selector.xpath("//h1[@class='name']/text()")
    # list: game type
    gametypes = selector.xpath("//div[@class='gameDesc']/div[@class='des']/p[@class='tag']/a/text()")
    # list: companies [develop, release...]
    companies = selector.xpath("//div[@class='gameDesc']/div[@class='des']/div[@class='txt']/p[@class='green']/a/text()")
    # value: rating
    rating = selector.xpath("//p[@class='score']/text()")
    #: value: number of people rated
    num_ratings = selector.xpath("//div[@class='grade']/div[@class='card']/p[@class='num']/text()")
    # a table of values
    game_details = selector.xpath("//div[@class='gameTable']//table/tr/td/text()")


    # ========================== parse section ===================================
    gamename = gamename[0] if len(gamename) >0 else ''
    gametypes = gametypes if gametypes else []

    # processing campany data
    tmp = {}
    for company in companies:
        if not "：" in company:
            pass
        kind, corp = company.split('：')
        tmp[kind] = corp

    companies = tmp

    rating = rating[0] if len(rating) >0 else ''
    num_ratings = num_ratings[0] if len(num_ratings) >0 else ''

    tmp = {}
    for d in game_details:
        if not "：" in d:
            pass
        k, v = d.split('：')
        tmp[k] = v

    game_details = tmp

    divs = selector.xpath("//div[@class = 'pd30 tab1']/div")

    info = dict()

    current_key = ''
    current_value = ''
    for div in divs:
        element_class = div.xpath('@class')
        if len(element_class) >0 and element_class[0] == 'tithd cf':
            key = div.xpath('em/text()')[0]
            if not key == '详细信息':
                current_key = key

            continue

        if len(element_class) >0 and element_class[0] == 'txtArea'and current_key != '':
            current_value = div.xpath('.//text()')

            current_value = ''.join(current_value) if len(current_value) >0 else ''
            info[current_key] = current_value

            current_key = ''


    show = """
        Game: {},
        Type: {},
        companies: {}
        rating: {}
        num_ratings: {}
        game_details: {}
        info: {}

    """.format(gamename, gametypes, companies, rating, num_ratings, game_details, info)

    print(show)
    # print(gamename, gametypes, companies, rating, num_ratings, game_details, info)

    time.sleep(1)



if __name__ == '__main__':


    starturl = 'https://www.3839.com/fenlei/'
    for cat_name, cat_url in get_category(starturl):
        for gamename, gameurl in get_game_urls(cat_name, cat_url):
            get_game_info(gamename, gameurl)
