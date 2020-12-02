from spider_utils import *
import time


def get_category(starturl,callback = get_game_urls,**kwargs):

    '''
        Get all game caregories
    '''
    selector = get_selector(starturl,**kwargs)

    category_names = selector.xpath("//div[@class='sift-top']/ul/li/p/a/text()")
    category_urls = selector.xpath("//div[@class='sift-top']/ul/li/p/a/@href")

    for name, url in zip(category_names, category_urls):
        callback(name, 'http:' + url)




def get_game_urls(name, url, callback = get_game_info, **kwargs):

    '''
        Get all game urls
    '''
    selector = get_selector(url, **kwargs)

    game_names = selector.xpath("//ul[@class='newness-list']/li/p[1]/a/text()")
    game_urls = selector.xpath("//ul[@class='newness-list']/li/p[1]/a/@href")

    for name, url in zip(game_names, game_urls):
        callback(name, 'http:' + url)






def get_game_info(name, url,**kwargs):

    print('Working on url: {}'.format(url))

    selector = get_selector(url, **kwargs)


    # ======================== xpath section =================================
    # value: game name
    gamename = get_value(selector,"//h1[@class='name']/text()")
    # list: game type
    gametypes = selector.xpath("//div[@class='gameDesc']/div[@class='des']/p[@class='tag']/a/text()")
    # list: companies [develop, release...]
    companies = selector.xpath("//div[@class='gameDesc']/div[@class='des']/div[@class='txt']/p[@class='green']/a/text()")
    # value: rating
    rating = get_value(selector, "//p[@class='score']/text()")
    #: value: number of people rated
    num_ratings = get_value(selector, "//div[@class='grade']/div[@class='card']/p[@class='num']/text()")
    # a table of values
    game_details = selector.xpath("//div[@class='gameTable']//table/tr/td/text()")

    companies = cvt_kv(companies,'：')
    game_details = cvt_kv(game_details,'：')


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

    time.sleep(1)






if __name__ == '__main__':


    starturl = 'https://www.3839.com/fenlei/'
    get_category(starturl)
