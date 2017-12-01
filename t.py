#!/usr/bin/python
import json
import requests
import argparse


def get_price(ticker):
    rsp = requests.get('https://finance.google.com/finance?q=%s&output=json' % (ticker))
    
    if rsp.status_code == 200:

        # This magic here is to cut out various leading characters from the JSON 
        # response, as well as trailing stuff (a terminating ']\n' sequence), and then
        # we decode the escape sequences in the response
        # This then allows you to load the resulting string
        # with the JSON module.
        try:
            fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
        except:
            print('Unable to load ticker')
            exit(1)

        # print out some quote data
        #print(fin_data)
        #print('Opening Price: {}'.format(fin_data['op']))
        #print('Price/Earnings Ratio: {}'.format(fin_data['pe']))
        #print('52-week high: {}'.format(fin_data['hi52']))
        #print('52-week low: {}'.format(fin_data['lo52']))

        # 'symbol', 'exchange', 'id', 't', 'e', 'name', 'f_reuters_url', 'f_recent_quarter_date', 'f_annual_date', 'f_ttm_date', 'financials', 
        # 'kr_recent_quarter_date', 'kr_annual_date', 'kr_ttm_date', 'keyratios', 'c', 'l', 'cp', 'ccol', 'op', 'hi', 'lo', 'vo', 'avvo', 'hi52', 'lo52',
        # 'mc', 'pe', 'fwpe', 'beta', 'eps', 'dy', 'ldiv', 'shares', 'instown', 'eo', 'sid', 'sname', 'iid', 'iname', 'related', 'summary', 
        # 'management', 'moreresources', 'events'
        return fin_data

    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker',     action='store',      help='the ticker')
    parser.add_argument('--cp',         action='store_true', help='change in percent')
    parser.add_argument('--c',         action='store_true',  help='change in currency')
    parser.add_argument('--down-color', action='store',      help='hex value of the color when the ticker is down')
    parser.add_argument('--up-color',   action='store',      help='hex value of the color when the ticker is up')

    args = parser.parse_args()

    down_color = '%{F#bf0000}'
    up_color   = '%{F#4b9653}'

    if args.down_color:
        down_color = args.down_color

    if args.up_color:
        up_color   = args.up_color



    if args.ticker:
        data = get_price(args.ticker)
        
        if not data:
            print('N/A')

        if args.cp:
            change = float(data['cp'])
            
            if change < 0:
                color = down_color

            elif change > 0:
                color = up_color

            else: 
                color = ''

            print('%s%4.2f (%4.2f%%)' % (color, float(data['l']), change))

        elif args.c:
            change = float(data['c'])

            if change < 0:
                color = down_color

            elif change > 0:
                color = up_color

            else:
                color = '' 

            print('%s%4.2f (%4.2f)' % (color, float(data['l']), change))
        else:
            print(data['l'])
