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
    sent = input('Input:')
    r = request(sent, token)
    print(r)


sentence_table=["COMMACATEGORY","PERIODCATEGORY","QUESTIONCATEGORY"]
person_table=["Nb","PERSON"]
time_table=["DATE","TIME","Nd"]
location_table=["Nc","Ncd"]
object_table=["Na","ORG"]
verb_table=["VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2"]
person=[]
time=[]
loc=[]
obj=[]
verb=[]
event=[]
event_temp=""
dirty=0
def main():
    
    #ws = WS("./data")
    #pos = POS("./data")
    #ner = NER("./data")
    
    
    # Run WS-POS-NER pipeline
    sentence_list = [
       input()
    ]
    word_sentence_list = ws(sentence_list)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    
    # Release model
    del ws
    del pos
    del ner
    
    # Show results
    def print_word_pos_sentence(word_sentence, pos_sentence):
        global event_temp
        global dirty
        assert len(word_sentence) == len(pos_sentence)
        for word, pos in zip(word_sentence, pos_sentence):
            if(pos in person_table and word not in person):
                person.append(word)
            elif(pos in time_table and word not in time):
                time.append(word)
            elif(pos in location_table and word not in loc):
                loc.append(word)
            elif(pos in object_table and word not in loc and word not in person and word not in obj and word not in time):
                obj.append(word)
            elif(pos in verb_table and word not in verb):
                verb.append(word)
            if(pos not in sentence_table): 
                if(pos in verb_table):
                    dirty=1
                if(dirty==1 and (pos in object_table or pos in verb_table or pos in person_table or pos in location_table or pos in time_table)):
                    event_temp=event_temp+word
            else:
                event.append(event_temp)
                event_temp=""
                dirty=0
            #print(f"{word}({pos})", end="\u3000")
        #print()
        return
    
    for i, sentence in enumerate(sentence_list):
        #print()
        #print(f"'{sentence}'")
        
 #       for entity in sorted(entity_sentence_list[i]):
 #           if(entity[2] in person_table):
   #             person.append(entity[3])
  #          elif(entity[2] in location_table):
  #              loc.append(entity[3])
  #          elif(entity[2] in object_table):
  #              obj.append(entity[3])
  #          elif(entity[2] in verb_table):
  #              verb.append(entity[3])   
        
        print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
    return
def check_cover():#to check whether object cover others list's element
    i=0
    while (i<len(obj)):
        if(obj[i] in loc):
            obj.remove(obj[i])
        else:
            i=i+1
    return

   
main()
check_cover()
print("person")
print(person, "\n")
print("time")
print(time, "\n")
print("location")
print(loc, "\n")
print("object")
print(obj, "\n")
print(verb)
print(verb, "\n")
print("event")
print(event)