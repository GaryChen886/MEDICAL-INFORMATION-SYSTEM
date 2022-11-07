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
    sent = input("Input:")
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
            
print("Location:", location)
print("Person:", person)
print("Time:", time)
print("Object:", Obj)
print("Events:", events)