import requests
import datetime
from collections import defaultdict
from json.decoder import JSONDecodeError


URL = 'https://api.vk.com/method'
ACCESS_TOKEN = 'fdfdb1ecfdfdb1ecfdfdb1ec0cfd897949ffdfdfdfdb1eca258cedc82af22a4ab2c5e12'
VERSION = '5.71'


def calc_age(uid):
    # Get user id
    user_id = get_id(uid)

    # Get friends info
    friends = get_friends(user_id)

    # Get ages
    ages = defaultdict(int)
    today = datetime.date.today().year
    for user in friends:
        bdate = user.get('bdate', None)
        if bdate:
            bdate = bdate.split('.')
            if len(bdate) == 3:
                age = today - int(bdate[-1])
                ages[age] += 1

    # Cast to list of tuples
    zipped = [(key, value) for key, value in ages.items()]

    # Return sorted
    return sorted(zipped, key=lambda z: (z[1], -z[0]), reverse=True)


def get_id(uid):
    """Get user info & return id."""
    url_id = f'{URL}/users.get'
    r = requests.get(url_id, params={'access_token': ACCESS_TOKEN, 'user_ids': uid, 'v': VERSION})
    return r.json()['response'][0]['id']


def get_friends(user_id):
    """Get users friends info & return as dicts."""
    url_friends = f'{URL}/friends.get?v=5.71&access_token={ACCESS_TOKEN}' \
                  f'&user_id={user_id}&fields=bdate'
    r = requests.get(url_friends)
    try:
        return r.json()['response']['items']
    except (JSONDecodeError, IndexError, KeyError):
        pass


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
