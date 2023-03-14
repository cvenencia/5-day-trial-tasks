from datetime import datetime, date
import requests


def get_cop_usd_convertion(cop):
    now = date.today()
    with open('conversion_rate.txt', 'r') as f:
        timestamp_string, rate_string = f.read().split(',')
        timestamp = datetime.strptime(timestamp_string, "%Y-%m-%d").date()
        rate = float(rate_string)

    if (timestamp - now).days != 0:
        print('\nNEW DATE, NEW RATE\n')
        try:
            new_rate = requests.get(
                'https://open.er-api.com/v6/latest/COP').json()['rates']['USD']
            with open('conversion_rate.txt', 'w') as f:
                f.write(f'{now},{new_rate}')
            return new_rate * cop
        except:
            print('\nERROR IN NEW RATE\n')
            return rate * cop
    else:
        return rate * cop
