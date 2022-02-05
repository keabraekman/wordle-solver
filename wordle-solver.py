# import splitLine

f = open("370k-words.txt", "r")
words = f.read().splitlines()
# print(words)

five_letter_words = []

for i in range(len(words)):
    if len(words[i]) == 5:
        five_letter_words.append(words[i])

# print(five_letter_words)


def blacks(candidates, words, numbers):
    black = []
    for i in range(len(words)):
        for j in range(len(words[i])):
            if numbers[i][j] == 0:
                black.append(words[i][j])

    for i in range(len(five_letter_words)):  
        a, b, c, d, e = five_letter_words[i][0], five_letter_words[i][1], five_letter_words[i][2], five_letter_words[i][3], five_letter_words[i][4]    
        l = [a,b,c,d,e]
        for j in range(len(black)):
            if black[j] in l and five_letter_words[i] in candidates:
                candidates.remove(five_letter_words[i])
    return candidates

def yellows(candidates, words, numbers):
    yellowLetters, yellowIndexes = [], []
    for i in range(len(words)):
        for j in range(len(words[i])):
            if numbers[i][j] == 1:
                yellowLetters.append(words[i][j])
                yellowIndexes.append(j)
    # print('YL = ', yellowLetters)
    # print('YI = ', yellowIndexes)
    for i in range(len(five_letter_words)):  
        a, b, c, d, e = five_letter_words[i][0], five_letter_words[i][1], five_letter_words[i][2], five_letter_words[i][3], five_letter_words[i][4]    
        l = [a,b,c,d,e]
        for j in range(len(yellowLetters)):
            if five_letter_words[i] in candidates:
                if l[yellowIndexes[j]]==yellowLetters[j] or yellowLetters[j] not in l:
                    candidates.remove(five_letter_words[i])
    return candidates

def greens(candidates, words, numbers):
    greenLetters, greenIndexes = [], []
    for i in range(len(words)):
        for j in range(len(words[i])):
            if numbers[i][j] == 2:
                greenLetters.append(words[i][j])
                greenIndexes.append(j)

    for i in range(len(five_letter_words)):  
        a, b, c, d, e = five_letter_words[i][0], five_letter_words[i][1], five_letter_words[i][2], five_letter_words[i][3], five_letter_words[i][4]    
        l = [a,b,c,d,e]
        for j in range(len(greenLetters)):
            if l[greenIndexes[j]] != greenLetters[j] and five_letter_words[i] in candidates:
                candidates.remove(five_letter_words[i])
    # print('GL = ', greenLetters)
    # print('GI = ', greenIndexes)
    return candidates

def bestCandidate(words,numbers):
    candidates = five_letter_words[:]
    candidates = blacks(candidates, words, numbers)
    candidates = yellows(candidates, words, numbers)
    candidates = greens(candidates, words, numbers)

    letter_dict = dict()
    frequency = dict()
    for i in range(len(candidates)):
        for j in range(len(candidates[i])):
            if candidates[i][j] in letter_dict:
                letter_dict[candidates[i][j]] += 1
            else:
                letter_dict[candidates[i][j]] = 1
    
    for i in range(len(candidates)):
        for j in range(len(candidates[i])):
            if candidates[i] in frequency:
                if candidates[i][j] not in candidates[i][:j]:
                    frequency[candidates[i]] += letter_dict[candidates[i][j]]
            else:
                frequency[candidates[i]] = letter_dict[candidates[i][j]]

    return print(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

    # return candidates


# print(bestCandidate(['arose','unlit','lymph'],
# [[0,2,2,0,0],
# [1,0,0,0,0],
# [0,0,0,0,0]
# ]))

print(bestCandidate(
    [
        'arose',
    'tired',
    'rebuy',
    # 'singe',
    # 'merry'
    ],
[
    [0,1,0,0,1],
[0,0,1,1,0],
[1,1,0,1,2],
# [2,2,0,2,2],
# [0,2,2,2,2]
]))


remove = ['a','r','o','s','e','u','n','l','i','t']
def perfect_first_word():
    letter_dict = dict()
    frequency = dict()
    for i in range(len(five_letter_words)):
        for j in range(len(five_letter_words[i])):
            if five_letter_words[i][j] in letter_dict:
                letter_dict[five_letter_words[i][j]] += 1
            else:
                letter_dict[five_letter_words[i][j]] = 1
    
    for i in range(len(five_letter_words)):
        for j in range(len(five_letter_words[i])):
            if five_letter_words[i].count(five_letter_words[i][j]) == 1 and five_letter_words[i][j] not in remove:
                if five_letter_words[i] in frequency and five_letter_words[i].count(five_letter_words[i][j]) == 1:
                    frequency[five_letter_words[i]] += letter_dict[five_letter_words[i][j]]
                else:
                    frequency[five_letter_words[i]] = letter_dict[five_letter_words[i][j]]
            else:
                frequency[five_letter_words[i]] = 0
    print(sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10])

# print(perfect_first_word())

# arose
# unlit
# lymph