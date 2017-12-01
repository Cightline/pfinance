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

        return fin_data

    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', action='store')
    parser.add_argument('--change', action='store_true')
    parser.add_argument('--down-color', action='store')
    parser.add_argument('--up-color', action='store')

    args = parser.parse_args()

    down_color = '%{F#bf0000}'
    up_color   = '%{F#bf0000}'

    if args.down_color:
        down_color = args.down_color

    if args.up_color:
        up_color   = args.up_color



    if args.ticker:
        data = get_price(args.ticker)
        
        if not data:
            print('N/A')

        if args.change:
            color = ''
            change = float(data['c'])
            
            if change < 0:
                color = down_color

            elif change > 0:
                color = up_color

            elif change == 0:
                color = ''

            print('%s%4.2f (%4.2f)' % (color, float(data['l']), change))

        else:
            print(data['l'])
