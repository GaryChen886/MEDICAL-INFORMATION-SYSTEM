import requests
import json

def request(sent, token):
    res = requests.post("http://140.116.245.157:2001", data={"data":sent, "token":token})
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return None 


if __name__ == "__main__":
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ2ZXIiOjAuMSwiaWF0IjoxNjYzNDg5MTk3LCJ1c2VyX2lkIjoiNDU1IiwiaWQiOjUyMiwic2NvcGVzIjoiMCIsInN1YiI6IiIsImlzcyI6IkpXVCIsInNlcnZpY2VfaWQiOiIxIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJuYmYiOjE2NjM0ODkxOTcsImV4cCI6MTY3OTA0MTE5N30.ZltJY3H0vY9HL4zUPaLQGYNOnda1bYMVh1dU40h0sMPM4Ldjo9LY1XmRDNFvM_TsNopCoG0KdYGQNsQ563PH3BeDWSl7qJXZK1J-6d2jh78Cvk_cNcELYdmRkC0Lm38Adj48bvwvknqhBqAqxtXJtsvuowwHsINMK6H4Jh21ZX8" # Go 'WMMKS API' website to get your token
    sent = input()
    r = request(sent, token)
    
people = []
thing = []
timing = []
place = []
events = []

words = r["ws"][0]
pos = r["pos"][0]

for i in range(len(words)):
    if pos[i] == "Na":
        thing.append(words[i])
    if pos[i] == "Nb":
        people.append(words[i])
    if pos[i] == "Nc":
        place.append(words[i])
    if pos[i] == "Nd":
        timing.append(words[i])
start = 0
cnt = 0
while cnt < len(words):
    for j in range(start, len(words)):
        #print(j)
        cnt += 1
        if pos[j] == "VC" or pos[j] == "VCL" or pos[j] == "VI" or pos[j] == "VJ":
            stri = words[j]
            chk = False
            for k in range(j + 1, len(pos)):
                cnt += 1
                if pos[k] != "A" and pos[k] != "Cab" and pos[k] != "Cba" and pos[k] != "I" and pos[k] != "SHI" and pos[k] != "VG" and pos[k] != "VH" and pos[k] != "VHC" and pos[k] != "VK" and pos[k] != "VL" and pos[k] != "COMMACATEGORY" and pos[k] != "EXCLAMATIONCATEGORY" and pos[k] != "PERIODCATEGORY" and pos[k] != "QUESTIONCATEGORY" and pos[k] != "SEMICOLONCATEGORY" and pos[k] != "VB" and pos[k] != "Dfa":
                    stri = stri + words[k]
                if pos[k] == "COMMACATEGORY" or pos[k] == "EXCLAMATIONCATEGORY" or pos[k] == "PERIODCATEGORY" or pos[k] == "QUESTIONCATEGORY" or pos[k] == "SEMICOLONCATEGORY":
                    if stri != words[j]:
                        events.append(stri)
                    start = k + 1
                    chk = True
                    #print(start)
                    break
            if chk == True:
                break

print("Location:", place)
print("Person:", people)
print("Time:", timing)
print("Object:", thing)
print("Events:", events)