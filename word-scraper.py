import requests
from bs4 import BeautifulSoup
import pickle


def create_all_words():
    page1 = requests.get("https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/1-10000")
    page2 = requests.get("https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/10001-20000")
    page3 = requests.get("https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/20001-30000")
    page4 = requests.get("https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2006/04/30001-40000")
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    soup3 = BeautifulSoup(page3.content, 'html.parser')
    soup4 = BeautifulSoup(page4.content, 'html.parser')
    list11 = soup1.find_all('a')
    list12 = []
    for i in range(len(list11)):
        list12.append(list11[i].text)
    list1 = list12[5:10016]
    list21 = soup2.find_all('a')
    list22 = []
    for i in range(len(list21)):
        list22.append(list21[i].text)
    list2 = list22[5:10007]
    list31 = soup3.find_all('a')
    list32 = []
    for i in range(len(soup3.find_all('a'))):
        list32.append(list31[i].text)
    list3 = list32[5:10005]
    list41 = soup4.find_all('a')
    list42 = []
    for i in range(len(soup4.find_all('a'))):
        list42.append(list41[i].text)
    list4 = list42[5:6668]
    all_words = list1+list2+list3+list4
    pickle.dump(all_words, open('all_words.pkl', 'wb'))

all_words = pickle.load(open('all_words.pkl', 'rb'))


def create_five_letter_words(all_words):
    five_letter_words = []
    for i in range(len(all_words)):
        if len(all_words[i]) == 5:
            five_letter_words.append(all_words[i])
    pickle.dump(five_letter_words, open('five_letter_words.pkl', 'wb'))

five_letter_words = pickle.load(open('five_letter_words.pkl', 'rb'))


black = ['e','n','i','a','f','o','h']
yellowLetter = ['t','r','t']
yellowIndex = [0,2,3]
greenLetter = []
greenIndex = []
duplicateLetters = False

candidates = five_letter_words[:]

for i in range(len(five_letter_words)):
    a, b, c, d, e = five_letter_words[i][0], five_letter_words[i][1], five_letter_words[i][2], five_letter_words[i][3], five_letter_words[i][4]
    l = [a,b,c,d,e]
    if duplicateLetters or ((a in [b,c,d,e] or b in [a,c,d,e] or c in [a,b,d,e] or d in [a,b,c,e]) and five_letter_words[i] in candidates):
        candidates.remove(five_letter_words[i])    
    for j in range(len(black)):
        if black[j] in l and five_letter_words[i] in candidates:
            candidates.remove(five_letter_words[i])

    for j in range(len(yellowLetter)):
        if l[yellowIndex[j]]==yellowLetter[j] or yellowLetter[j] not in l:
            if five_letter_words[i] in candidates:
                candidates.remove(five_letter_words[i])
    
    for j in range(len(greenLetter)):
        if l[greenIndex[j]] != greenLetter[j] and five_letter_words[i] in candidates:
            candidates.remove(five_letter_words[i])


print(candidates)




def perfectFirstWord():
    letters = {}
    # letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
    # 'x','y','z']
    # numbers = [0]*26
    for i in range(len(five_letter_words)):
        for j in range(len(five_letter_words[i])):
            if five_letter_words[i][j] in letters:
                letters[five_letter_words[i][j].lower()] += 1
            else:
                letters[five_letter_words[i][j].lower()] = 1
    
    five_letter_dict = {}
    for i in range(len(five_letter_words)):
        a,b,c,d,e = five_letter_words[i][0].lower(),five_letter_words[i][1].lower(),five_letter_words[i][2].lower(),five_letter_words[i][3].lower(),five_letter_words[i][4].lower()
        if a not in [b,c,d,e] and b not in [a,c,d,e] and c not in [a,b,d,e] and d not in [a,b,c,e] and e not in [a,b,c,d]:
            five_letter_dict[five_letter_words[i]] = 0
            for j in range(len(five_letter_words[i])):
                five_letter_dict[five_letter_words[i]] += letters[five_letter_words[i][j].lower()]
    
    print(sorted(five_letter_dict.items(), key=lambda x: x[1], reverse=True))


# perfectFirstWord()







        # for i in range(len(yellowLetter)):
        #     if yellowLetter[i] == l[yellowIndex[i]] or yellowLetter[i] not in l:
        #         break
        # break



        
        # if 'w' not in l and 'u' not in l and 'd' not in l and 't' not in l and 'h' not in l and 'e' not in l and 'i' not in l and 'r' not in l:
        #     if 'o' == b:
        #         if a == 'f':
        #             if 'l'!=c and 'l'!=d and 'l' in [a,b,e]:
        #                 print(five_letter_words[i])
            
            
            
            # if 'h' not in [a,b] and 'h' in [a,c,d,e]:
            #     if 's'!= e and 's' in [a,b,c,d]:
            #         print(five_letter_words[i])




    # if 's' not in l and 'n' not in l and 'p' not in l and 'l' not in l and 'c' not in l and 't' not in l and 'h' not in l and 'i' not in l and 'r' not in l:
    #     if c == 'a' and e=='e' and 'k'==d:
            # print(five_letter_words[i])

                



    # if 'b' not in l and 'm' not in l and 'l' not in l and 'g' not in l and 'n' not in l and 'o' not in l and 'd' not in l and 't' not in l and 'h' not in l and 'e' not in l and 'r' not in l:
    #     if b == 'i':
    #         if 's' in [a,c,d]:
    #             print(five_letter_words[i])
    #             break




        
        # if 'x' not in l and 'a' not in l and 'w' not in l and 'o' not in l and 'h' not in l and 'i' not in l:
        #     if 't'!= c and 't' != a and 't' !=d and 't' in [b,e]:
        #         if 'e'!=a and 'e' != c and 'e' != e and 'e' in [b,d]:
        #             if 'r'!= d and 'r' != e and 'r' != b and 'r' in [a,c]:
        #                 print(five_letter_words[i])
        #                 break

        
        #     if 'r' == e:
        #         if 'a' != b and 'a' in [a,c,d]:
        #             print(five_letter_words[i])
        #             break


        # if 'n' not in l and 's' not in l and 'o' not in l and 't' not in l and 'e' not in l and 'i' not in l and 'r' not in l:
        #     if 'h' == b:
        #         if 'w' != d and 'w' in [a,b,c,e]:
        #             print(five_letter_words[i])
        #             break



        # if 'c' not in l and 'a' not in l and 'b' not in l and 'h' not in l and 'e' not in l and 'i' not in l and 'r' not in l:
        #     if b == 'o' and c == 'u' and d == 'n' and e == 't':
        #         # if 'o' in [a,b,d] and 'o'!=c and 'u' in [a,b,c] and 'u'!=d:
        #         print(five_letter_words[i])
        #         break






        # if 'l' not in [a,b,c,d,e] and 'a' not in [a,b,c,d,e] and 's' not in [a,b,c,d,e] and 't' not in [a,b,c,d,e] and 'h' not in [a,b,c,d,e] and 'i' not in [a,b,c,d,e]:
        #     if 'e' == b and 'e' != c and c == 'r' and 'r' not in [a,d,e]:
        #         if 'y' == e:
        #             if 'p' in [a,c,d] and 'p' != c:
        #                 print(five_letter_words[i])
        #                 break



        # if 't' not in [a,b,c,d,e] and 'h' not in [a,b,c,d,e] and 'e' not in [a,b,c,d,e] and 'i' not in [a,b,c,d,e] and 'r' not in [a,b,c,d,e]:
        #     print(five_letter_words[i])
        #     break

        # if a== 'w' and b == 'r' and d == 'n' and e == 'g':
        #     if 'g' in [b,c,d,e] and a != 'g':
        #         if 't' not in [a,b,c,d,e] and 'h' not in [a,b,c,d,e] and 'e' not in [a,b,c,d,e] and 'i' not in [a,b,c,d,e] and 'a' not in [a,b,c,d,e] and 'o' not in [a,b,c,d,e]:
        #             print(five_letter_words[i])
        #             break   
    
    # if a == 't' and b == 'h':
    #     if 'i' not in [a,b,c,d,e] and 'r' not in [a,b,c,d,e] and 'n' not in [a,b,c,d,e] and 'k' not in [a,b,c,d,e] and 'a' not in [a,b,c,d,e]:
    #         if c != 'e' and (d == 'e' or e == 'e'):
    #             print(five_letter_words[i])
    #             break

    


# print(list22.index('pence'))
# print(list22.index('ussr'))