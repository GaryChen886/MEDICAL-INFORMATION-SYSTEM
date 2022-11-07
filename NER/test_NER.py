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
sentence_table=["COMMACATEGORY","PERIODCATEGORY","QUESTIONCATEGORY"]
person_table=["Nb"]
time_table=["Nd"]
location_table=["Nc"]
object_table=["Na"]
verb_table=["VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2"]
person = []
Obj = []
time = []
location = []
events = []

word_list = r["ws"][0]
pos = r["pos"][0]

for i in range(len(word_list)):
    if pos[i] == "Na":
        Obj.append(word_list[i])
    if pos[i] == "Nb":
        person.append(word_list[i])
    if pos[i] == "Nc":
        location.append(word_list[i])
    if pos[i] == "Nd":
        time.append(word_list[i])

start = 0
count = 0
flag = 0
event_temp = ""
for word, pos in zip(word_list, pos):
        if (pos in person_table and word not in person):
            person.append(word)
        elif (pos in time_table and word not in time):
            time.append(word)
        elif (pos in location_table and word not in location):
            location.append(word)
        elif (pos in object_table and word not in location and word not in person and word not in Obj and word not in time):
            Obj.append(word)
        if (pos not in sentence_table):
            if (pos in verb_table):
                flag = 1
            if (flag == 1):
                event_temp += word
        else:
            if(event_temp!="") and len(event_temp)>2:
                events.append(event_temp)
            event_temp = ""
            flag = 0
            
print("地:", location)
print("人:", person)
print("時:", time)
print("物:", Obj)
print("事件:", events)