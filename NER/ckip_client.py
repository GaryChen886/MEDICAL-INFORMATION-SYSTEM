import requests
import json

def request(sent, token):
    res = requests.post("http://140.116.245.157:2001", data={"data":sent, "token":token})
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return None 


if __name__ == "__main__":
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ2ZXIiOjAuMSwiaWF0IjoxNjYzNDAyNzEzLCJ1c2VyX2lkIjoiNDUxIiwiaWQiOjUxOCwic2NvcGVzIjoiMCIsInN1YiI6IiIsImlzcyI6IkpXVCIsInNlcnZpY2VfaWQiOiIxIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJuYmYiOjE2NjM0MDI3MTMsImV4cCI6MTY3ODk1NDcxM30.WJjyXdaViPw1ezzgH6KB-_Ploc0untuAP9dZujdnGCaEDXPRwNUXuYyJwQmr6gbcSoge7BZRg2BlqQDOTnMiLsJDPAtnvZreM8bdimn_p1T3d_7ZYkCOpARGSdBTCF47RmUpOhmSUqtTORxpuFaErrjLkk8LVvChkGWv97y5oU4" # Go 'WMMKS API' website to get your token
    sent = "今天的天氣很不錯"
    r = request(sent, token)
    print(r)
