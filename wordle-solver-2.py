# Import the list of words
import pickle
import statistics


# Idea 1 : 
# Guess the word that reduces the list the most on average
# Idea 2 : 
# Use the longer list of words as guesses and the wordle answers for answers

f = open("wordle-answers-alphabetical.txt", "r")
all_answers = f.read().splitlines()


def create_all_guesses(all_words):
    five_letter_words = []
    for w in all_words:
        if len(w) == 5:
            print('adding : ', w)
            five_letter_words.append(w)
    return five_letter_words

f = open("370k-words.txt", "r")
all_words = f.read().splitlines()

# all_guesses = create_all_guesses(all_words)
# pickle.dump(all_guesses, open('all_guesses.pkl', 'wb'))

all_guesses = pickle.load(open('all_guesses.pkl', 'rb'))



def blacks(candidates, words, numbers):
    black, yellow, green = [], [], []
    for i in range(len(numbers)):
        for j in range(len(numbers[i])):
            if numbers[i][j] == 0:
                black.append(words[i][j])
            if numbers[i][j] == 1:
                yellow.append(words[i][j])
            if numbers[i][j] == 2:
                green.append(words[i][j])
    i = 0
    while i < len(candidates):
        l = [candidates[i][0], candidates[i][1], candidates[i][2], candidates[i][3], candidates[i][4]]
        for j in range(len(black)):
            if black[j] in l and black[j] not in green and black[j] not in yellow:
                candidates.pop(i)
                i -= 1
                break
        i += 1
    return candidates

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


def give_numbers(candidate, answer):
    numbers = [1]*5
    for i in range(len(candidate)):
        if candidate[i] == answer[i]:
            numbers[i] = 2
        elif candidate[i] not in answer:
            numbers[i] = 0
    return numbers

def number_of_removes(guess, answer):
    candidates = all_answers[:]
    numbers = [give_numbers(guess, answer)]
    candidates = blacks(candidates, [guess], numbers)
    candidates = yellows(candidates, [guess], numbers)
    candidates = greens(candidates, [guess], numbers)
    return len(all_answers) - len(candidates)


def average_of_removes(guess):
    removes = []
    for a in all_answers:
        removes.append(number_of_removes(guess, a))
    return statistics.mean(removes)



def perfect_first_word():
    first_word = dict()
    for g in all_guesses:
        removes = average_of_removes(g)
        first_word[g] = removes
        print('Added : ', g, ' = ', removes)
    sorted(first_word.items(), key=lambda x: x[1], reverse=True)
    return first_word

# first_word_dict = perfect_first_word()
# pickle.dump(first_word_dict, open('first_word_dict.pkl', 'wb'))
        
first_word_dict = pickle.load(open('first_word_dict.pkl', 'rb'))
print(sorted(first_word_dict.items(), key=lambda x: x[1], reverse=True))




first_word_dict = pickle.load(open('first_word_dict_test.pkl', 'rb'))
print(sorted(first_word_dict.items(), key=lambda x: x[1], reverse=True))




# Make a function with words, numbers and candidates
#  1. Update the list of all answers given a word and numbers
# 2. Calculate the number of removes on average per guess


def update_candidates(word, numbers, candidates):
    for i in range(5):
        for c in candidates:
            if numbers[i] == 0 and word[i] in c and word.count(word[i]) == 1:
                candidates.pop(c, None)
            elif numbers[i] == 1 and (word[i] not in c or c[i] == word[i]):
                candidates.pop(c, None)
            elif numbers[i] == 2 and c[i] != word[i]:
                candidates.pop(c, None)
    return candidates




def average_of_removes2(guess, answers):
    removes = []
    for a in answers:
        removes.append(number_of_removes(guess, a))
    return statistics.mean(removes)


def number_of_removes2(guess, answer):
    candidates = all_answers[:]
    numbers = [give_numbers(guess, answer)]
    candidates = blacks(candidates, [guess], numbers)
    candidates = yellows(candidates, [guess], numbers)
    candidates = greens(candidates, [guess], numbers)
    return len(all_answers) - len(candidates)


def guess(words, numbers):
    candidates = all_answers[:]
    for i in range(len(words)):
        candidates = update_candidates(words[i], numbers[i], candidates)
    
    for g in all_guesses:
        removes = average_of_removes2(g)
        candidates[g] = removes
        print('Added : ', g, ' = ', removes)
    # sorted(answers.items(), key=lambda x: x[1], reverse=True)
    return 0









# print(len(all_answers))
# print(len(all_guesses))


# print(average_of_removes('alert'))