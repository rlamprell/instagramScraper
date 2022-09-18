import  requests
import  pandas as pd
from    multiprocessing import Pool, freeze_support
from    dataclasses import dataclass


@dataclass
class instagramAPI:
    url = "https://i.instagram.com/api/v1/users/web_profile_info"
    payload = ""
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "i.instagram.com",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/",
        "Connection": "keep-alive",
        "X-ASBD-ID": "198387",
        "X-IG-App-ID": "936619743392459",
        "Priority": "u=3, i",
        "X-Instagram-AJAX": "1006222884",
        "X-IG-WWW-Claim": "hmac.AR0M4mwv15LNfJNm8YpUxGs46-yeRhs5W4EWxVLCmSr4-G-J",
        "X-CSRFToken": "ZgPs7y0GqW5VspLv2BBi1pOJvYMZviEA"
    }


class accounts:
    def __init__(self, fileName="accounts.txt"):
        with open('accounts.txt') as f:
            self.accounts = f.read().strip().splitlines()

    def __call__(self):
        return self.accounts

    def getList(self):
        return self.accounts


def getFollowerCount(instagramUsername):
    url             = instagramAPI.url
    payload         = instagramAPI.payload
    headers         = instagramAPI.headers
    querystring     = {"username":f'{instagramUsername}'}
    response        = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    followers       = response.json()['data']['user']['edge_followed_by']['count']

    return followers


def constructDataFrame(usernameList, followersList):
    d   = {'Name':usernameList, 'Followers': followersList}
    df  = pd.DataFrame(d)
    df  = pd.DataFrame(d, columns=['Name','Followers'])

    return df


def main(workerCount=3):
    usernameList    = accounts()()
    with Pool(workerCount) as p:
        followersList = p.map(getFollowerCount, usernameList)

    followersList   = list(followersList)
    df              = constructDataFrame(usernameList, followersList)

    return df


if __name__ == '__main__':
    freeze_support()
    df = main(10)
    print(df)