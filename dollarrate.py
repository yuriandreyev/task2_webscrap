'''This module parses sites and prints dollar's rate to console'''

import re
import lxml.html
import urllib.request
import time

url_ya = 'https://www.yandex.ru/'
url_forex = 'http://www.forexpf.ru/currency_usd.asp'
url_cbr = 'http://www.cbr.ru/'

yandex_pattern = re.compile('<span class="inline-stocks__value_inner">[0-9.,]+</span>')
forex_pattern = re.compile('<td align=center class=cell><b><font color="Red">[0-9.,]+</font></b></td>+')
cbr_pattern = re.compile('<ins class="rubl">\\\\xd1\\\\x80\\\\xd1\\\\x83\\\\xd0\\\\xb1.'
                         '</ins>&nbsp;[0-9.,]+</td>\\\\r\\\\n')
pattern_of_dollar_rate = re.compile('[0-9]+[.,][0-9]+')

# Patterns for parsing using regular expressions
patterns_re = {url_ya: yandex_pattern, url_forex: forex_pattern, url_cbr: cbr_pattern}
# Patterns for parsing using lxml library and XPATH
patterns_lxml = {url_ya: '//span[@class="inline-stocks__value_inner"]',
                 url_forex: '//td/b/font[@color="Red"]',
                 url_cbr: '//td[@class="weak"]'}


def read_site(url):
    '''Function takes url and returns text of the site'''

    f = urllib.request.urlopen(url)
    text = f.read()
    return str(text)


def parsing_dollar_re(text, url):
    '''Function returns dollar's rate from text using regular expression.'''
    
    pattern_of_code_line = patterns_re[url]
    line_with_dollar = pattern_of_code_line.findall(text)[0]
    dollar_rate = pattern_of_dollar_rate.findall(line_with_dollar)
    return dollar_rate[0]


def parsing_dollar_lxml(html_text, url):
    '''Function parses dollar's rate in html code using lxml'''

    tree = lxml.html.fromstring(html_text)
    node = tree.xpath(patterns_lxml[url])[0]
    result = node.xpath('./text()')[-1]
    return result


def timer(func):
    '''Function returns result of some function and a time wasted for calculating the result'''

    repeat = 20  # How many times best time will be calculated to achieve more accuracy
    best_time = 1000
    for i in range(repeat):
        start_time = time.clock()
        for x in range(2000):  # How many times function will be executed to achieve more accuracy
            result = func
        wasted_time = time.clock() - start_time
        if wasted_time < best_time:
            best_time = wasted_time
    return result, best_time


def output_results(*args):
    '''Function prints results of parsing dollar's rate'''
    
    print('Dollar\'s rate:')
    for url in args:
        html_text = read_site(url)
        print('-'*50)
        print('{url}'.format(url=url))
        if url in patterns_re:
            rate, best_time = timer(parsing_dollar_re(html_text, url))
            print('{library}\t{rate} rubles, {time: 50.50f}'.format(library='re', rate=rate, time=best_time))
        else:
            print('There is no pattern for parsing %s using regular expressions' % url)
        if url in patterns_lxml:
            rate, best_time = timer(parsing_dollar_lxml(html_text, url))
            print('{library}\t{rate} rubles, {time: 50.50f}'.format(library='lxml', rate=rate, time=best_time))
        else:
            print('There is no pattern for parsing %s using XPATH and lxml' % url)
        
output_results(url_ya, url_forex, url_cbr)



