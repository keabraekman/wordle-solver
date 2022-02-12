# Import the list of words
import pickle


f = open("370k-words.txt", "r")
all_words = f.read().splitlines()

# We create a list of only the 5 letter words
def create_five_letter_words(all_words):
    five_letter_words = []
    for w in all_words:
        if len(w) == 5:
            five_letter_words.append(w)
    return five_letter_words

# five_letter_words = create_five_letter_words(all_words)
# pickle.dump(five_letter_words, open('five_letter_words.pkl', 'wb'))
five_letter_words = pickle.load(open('five_letter_words.pkl', 'rb'))

for i in range(len(five_letter_words)):
    if five_letter_words.count(five_letter_words[i]) > 1:
        print(five_letter_words[i])


# Black letters
def blacks(candidates, words, numbers):
    # Start with a list of all the black letters
    black = []
    # Cycle through inputted words
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            if numbers[i][j] == 0:
                black.append(words[i][j])
    # Cycle through all the candidates and remove the ones that include the black letters
    # for i in range(len(candidates)):
    i = 0
    while i < len(candidates):
        l = [candidates[i][0], candidates[i][1], candidates[i][2], candidates[i][3], candidates[i][4]]
        for j in range(len(black)):
            if black[j] in l:
                candidates.pop(i)
                i -= 1
                break
        i += 1
    return candidates

# Yellow letters
def yellows(candidates, words, numbers):
    yellowLetters, yellowIndexes = [], []
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            if numbers[i][j] == 1:
                yellowLetters.append(words[i][j])
                yellowIndexes.append(j)
    i = 0
    while i < len(candidates):
        l = [candidates[i][0], candidates[i][1], candidates[i][2], candidates[i][3], candidates[i][4]]
        for j in range(len(yellowLetters)):
            if i < len(candidates) and (l[yellowIndexes[j]]==yellowLetters[j] or yellowLetters[j] not in l):
                candidates.pop(i)
                i -= 1
                break
        i += 1
    return candidates


def greens(candidates, words, numbers):
    greenLetters, greenIndexes = [], []
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            if numbers[i][j] == 2:
                greenLetters.append(words[i][j])
                greenIndexes.append(j)

    i = 0
    while i < len(candidates):
        l = [candidates[i][0], candidates[i][1], candidates[i][2], candidates[i][3], candidates[i][4]]
        for j in range(len(greenLetters)):
            if i < len(candidates) and l[greenIndexes[j]] != greenLetters[j]:
                candidates.pop(i)
                i-= 1
                break
        i += 1
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

    # print('M = ', letter_dict['m'])
    # print('G = ', letter_dict['g'])
    # print('H = ', letter_dict['h'])
    # print('U = ', letter_dict['u'])
    # print('N = ', letter_dict['n'])
    # print('Y = ', letter_dict['y'])

    for i in range(len(candidates)):
        for j in range(len(candidates[i])):
            if candidates[i] in frequency:
                # if candidates[i] == 'might':
                #     print('frequency[candidates[i]] = ', frequency[candidates[i]])
                if candidates[i][j] not in candidates[i][:j]:
                    frequency[candidates[i]] += letter_dict[candidates[i][j]]
            else:
                frequency[candidates[i]] = letter_dict[candidates[i][j]]

    return print(sorted(frequency.items(), key=lambda x: x[1], reverse=True))


print(bestCandidate(
    [
        'arose',
    'outre',
    'corbe',
    # 'looby',
    # 'cavel'
    ],
[
    [0,1,1,0,2],
[1,0,0,1,2],
[0,2,2,0,2],
# [2,2,2,0,2],
# [0,2,0,2,2]
]))


# remove = ['a','r','o','s','e','u','n','l','i','t']
# def perfect_first_word():
#     letter_dict = dict()
#     frequency = dict()
#     for i in range(len(five_letter_words)):
#         for j in range(len(five_letter_words[i])):
#             if five_letter_words[i][j] in letter_dict:
#                 letter_dict[five_letter_words[i][j]] += 1
#             else:
#                 letter_dict[five_letter_words[i][j]] = 1
    
#     for i in range(len(five_letter_words)):
#         for j in range(len(five_letter_words[i])):
#             if five_letter_words[i].count(five_letter_words[i][j]) == 1 and five_letter_words[i][j] not in remove:
#                 if five_letter_words[i] in frequency and five_letter_words[i].count(five_letter_words[i][j]) == 1:
#                     frequency[five_letter_words[i]] += letter_dict[five_letter_words[i][j]]
#                 else:
#                     frequency[five_letter_words[i]] = letter_dict[five_letter_words[i][j]]
#             else:
#                 frequency[five_letter_words[i]] = 0
#     print(sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10])

# print(perfect_first_word())

# arose
# unlit
# lymph