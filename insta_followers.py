import  requests
import  pandas as pd
from    multiprocessing import Pool, freeze_support
from    dataclasses import dataclass


@dataclass
class instagramAPI:
    url = "https://i.instagram.com/api/v1/users/web_profile_info"
    payload = ""
    headers = {
        # "cookie": "csrftoken=ZgPs7y0GqW5VspLv2BBi1pOJvYMZviEA; rur=%22RVA%5C05455117407996%5C0541695040786%3A01f71d9f6280b930e943391416b8b70f164697f9c49a695f5b4b732a77b817a58fb7b697%22; ds_user_id=55117407996",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "i.instagram.com",
        "Origin": "https://www.instagram.com",
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
        "Referer": "https://www.instagram.com/",
        "Connection": "keep-alive",
        # "Cookie": "_js_datr=9BAnY590VPcz3K6z7_NHHMxz; dpr=2; csrftoken=ZgPs7y0GqW5VspLv2BBi1pOJvYMZviEA; ds_user_id=55117407996; rur="RVA\05455117407996\0541695040628:01f73845f530a4b34c5fffe887966e6be6e95487d5ca03d1931fba6e6abe5b9b9fa01f77"; sessionid=55117407996%3A9XHE0yTle5Xhtt%3A5%3AAYeoHZCLvpkRH2U_KclBi7oxOOSqjEmO8iOOLndj9A; ig_did=1A26F683-F5F9-46E1-B578-AEB143FF3D88; mid=YoeGggAEAAHCGs-7STo2LbPn3kMm",
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