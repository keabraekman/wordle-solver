# Import the list of words
import pickle


f = open("wordle-answers-alphabetical.txt", "r")
five_letter_words = f.read().splitlines()

# We create a list of only the 5 letter words
def create_five_letter_words(all_words):
    five_letter_words = []
    for w in all_words:
        if len(w) == 5:
            five_letter_words.append(w)
    return five_letter_words

# five_letter_words = create_five_letter_words(all_words)
# pickle.dump(five_letter_words, open('five_letter_words.pkl', 'wb'))
# five_letter_words = pickle.load(open('five_letter_words.pkl', 'rb'))



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

    return sorted(frequency.items(), key=lambda x: x[1], reverse=True)

# Worst candidates : 
# Widow
# Inbox
# Trunk

(bestCandidate(
    [
        'alert',
    'abhor',
    # 'detox',
    # 'cramp',
    # 'cavel'
    ],
[
    [2,0,0,1,0],
[2,0,0,1,1],
# [0,1,2,1,0],
# [2,2,2,0,0],
# [0,2,0,2,2]
]))


remove = ['w','i','d','o','w','i','n','b','o','x']
# remove = []
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
            if five_letter_words[i][j] not in five_letter_words[i][j+1:] and five_letter_words[i][j] not in remove:
                if five_letter_words[i] in frequency and five_letter_words[i].count(five_letter_words[i][j]) == 1:
                    frequency[five_letter_words[i]] += letter_dict[five_letter_words[i][j]]
                else:
                    frequency[five_letter_words[i]] = letter_dict[five_letter_words[i][j]]
            else:
                frequency[five_letter_words[i]] = 0
    print(sorted(letter_dict.items(), key=lambda x: x[1], reverse=True))
    print(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

# print(perfect_first_word())

# alert
# scion
# dumpy


# this function is given a word and returns a list of the numbers that correspond given the answer
def give_numbers(candidate, answer):
    numbers = [1]*5
    for i in range(len(candidate)):
        if candidate[i] == answer[i]:
            numbers[i] = 2
        elif candidate[i] not in answer:
            numbers[i] = 0
    return numbers

# print(give_numbers('alert', 'biome'))

def guesses_single_word(answer):
    if answer == 'alert':
        return 1
    words = ['alert']
    numbers = [give_numbers('alert', answer)]

    for i in range(5):
        candidate = bestCandidate(words, numbers)[0][0]
        numbers.append(give_numbers(candidate, answer))
        words.append(candidate)
        if candidate == answer:
            return (i+2)
    return 0
        # print(candidate)


guesses_single_word('pound')

# print(give_numbers('alert', 'biome'))