import requests
import json

def request(sent, token):
    res = requests.post("http://140.116.245.157:2001", data={"data":sent, "token":token})
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        return None 

sentence_table = ["COMMACATEGORY","PERIODCATEGORY","QUESTIONCATEGORY","SEMICOLONCATEGORY"]
person_table = ["Nb"]
time_table = ["Nd"]
location_table = ["Nc","Ncd"]
object_table = ["Na"]
verb_table = ["VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2"]
person=[]
time=[]
loc=[]
obj=[]
verb=[]
event=[]

def main():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiJ9.eyJ2ZXIiOjAuMSwiaWF0IjoxNjYzMjk0MDM5LCJ1c2VyX2lkIjoiNDQwIiwiaWQiOjQ5OSwic2NvcGVzIjoiMCIsInN1YiI6IiIsImlzcyI6IkpXVCIsInNlcnZpY2VfaWQiOiIxIiwiYXVkIjoid21ta3MuY3NpZS5lZHUudHciLCJuYmYiOjE2NjMyOTQwMzksImV4cCI6MTY3ODg0NjAzOX0.BDNzcja8VzEDEw0pJjGjsA0jBCl4XyHw3Nm7zzuGB84Wv9XT5UwsILoodfBFGw-djSMGLNvHeoHS5uFFSJGlvQCugTMD18hErxOgi5YuG8fsVoPpxT4zPeO9yK3ydAZsBGIzSdJOTQsmvir10CPPs93p-nJ_C1PiISXDzUPUVR4" # Go 'WMMKS API' website to get your token
    sent = input()
    r = request(sent, token)
    word_list = []
    pos_list = []
    prev_word = ""
    prev_pos = ""
    for word, pos in zip(r.get('ws')[0], r.get('pos')[0]):
        if pos == prev_pos:
            prev_word += word
        else:
            word_list.append(prev_word) if prev_word != '' else None
            pos_list.append(prev_pos) if prev_pos != '' else None
            prev_word = word
            prev_pos = pos
    flag = 0
    event_temp = ""
    for word, pos in zip(word_list, pos_list):
        if (pos in person_table and word not in person):
            person.append(word)
        elif (pos in time_table and word not in time):
            time.append(word)
        elif (pos in location_table and word not in loc):
            loc.append(word)
        elif (pos in object_table and word not in loc and word not in person and word not in obj and word not in time):
            obj.append(word)
        elif (pos in verb_table and word not in verb):
            verb.append(word)
        if (pos not in sentence_table):
            if (pos in verb_table):
                flag = 1
            if (flag == 1):
                event_temp += word
        else:
            if(event_temp!="") and len(event_temp)>2:
                event.append(event_temp)
            event_temp = ""
            flag = 0
    return 

main()
print("People:",person)
print("Time:",time)
print("Location:",loc)
print("Object:",obj)
print("Event:",event)
    
