def backward_segment(text, dic):
    word_list = []
    i = len(text) - 1
    while i >= 0: 
        longest_word = text[i]
        
        #if 'A'<=text[i]<='Z' or 'a'<=text[i]<='z' or '0'<=text[i]<='9':
        #    while i>=0 and ('A'<=text[i]<='Z' or 'a'<=text[i]<='z' or '0'<=text[i]<='9'):
        #        longest_word += text[i]
        #        i -= 1
        #        #text[i] = longest_word[i] if i<len(text) else text[i]
        #    word_list.append(longest_word)
        #    longest_word=""
            
        if 'A'<=text[i]<='Z' or 'a'<=text[i]<='z' or '0'<=text[i]<='9':
            for j in range(0,i):
                word = text[j : i + 1]
                if 'A'<=text[j]<='Z' or 'a'<=text[j]<='z' or '0'<=text[j]<='9':
                    if len(word) > len(longest_word):
                        longest_word = word
            word_list.insert(0,longest_word)
            i -= len(longest_word)
        
    
        else:
            for j in range(0, i):  
                word = text[j : i+1]  
                if word in dic:  
                    if len(word) > len(longest_word): 
                        longest_word = word  
            word_list.insert(0, longest_word) 
            i -= len(longest_word)
             
        
    return word_list
dic = open('dict_no_space_editted.txt').read()
dic = ''.join(dic)
sentence = input()
print(backward_segment(sentence, dic))
