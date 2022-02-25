import pickle

all_guesses = pickle.load(open('all_guesses.pkl', 'rb'))

f = open("wordle-answers-alphabetical.txt", "r")
all_answers = f.read().splitlines()

# print('length of guesses = ', len(all_guesses))
# print('length of answers = ', len(all_answers))


# print('vache index = ', all_guesses.index('vache'))
# print('progress = ', 100*all_guesses.index('vache')/len(all_guesses))



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


def give_numbers(candidate, answer):
    numbers = [1]*5
    for i in range(len(candidate)):
        if candidate[i] == answer[i]:
            numbers[i] = 2
        elif candidate[i] not in answer:
            numbers[i] = 0
    return numbers

def number_of_candidates(guess, numbers):
    candidates = len(all_answers)
    for a in all_answers:
        for i in range(5):
            if numbers[i] == 0 and guess[i] in a:
                candidates -= 1
                break
            elif (numbers[i] == 1 and guess[i] not in a) or (numbers[i] == 1 and a[i] == guess[i]):
                candidates -= 1
                break
            elif numbers[i] == 2 and a[i] != guess[i]:
                candidates -= 1
                break
    return candidates


def perfect_first_word():
    first_word_dict_test = dict()
    for g in all_guesses:
        candidates = []
        for a in all_answers:
            candidates.append(number_of_candidates(g, give_numbers(g, a)))
        median = statistics.median(candidates)
        first_word_dict_test[g] = median
        print('Adding : ', g, ' candidates = ', median)
    return first_word_dict_test
    



# Averages
first_word_dict = pickle.load(open('first_word_dict.pkl', 'rb'))
# print(sorted(first_word_dict.items(), key=lambda x: x[1], reverse=True))

# Medians
first_word_dict = pickle.load(open('first_word_dict_test.pkl', 'rb'))
# print(sorted(first_word_dict.items(), key=lambda x: x[1], reverse=True))



def update_candidates(word, numbers, candidates):
    candidates2 = candidates[:]
    c = 0
    while c < len(candidates2):
        for i in range(5):
            if numbers[i] == 0 and word[i] in candidates2[c] and word.count(word[i]) == 1:
                candidates2.pop(c)
                c-=1
                break
            elif numbers[i] == 1 and (word[i] not in candidates2[c] or candidates2[c][i] == word[i]):
                candidates2.pop(c)
                c-=1
                break
            elif numbers[i] == 2 and candidates2[c][i] != word[i]:
                candidates2.pop(c)
                c-=1
                break
        c += 1
    return candidates2


# We need to make a function that takes in words, numbers, and all_answers (updated)
# Then we take the updated list of answers
# Cycle through all the guesses
# Compare with the guess and potential answer from updated all_answers
# Get the median number of removes (or length of remaining answers)
# Put in dict[guess] = median length of remaining answers
# Sort in ascending order

# OPTIMIZE : If length is too big (beyond top 10 guesses, do not compute)

def length_of_remaining(guess, answer, answers):
    candidates = len(answers)
    numbers = give_numbers(guess, answer)

    for j in range(len(answers)):
        for i in range(5):
            if numbers[i] == 0 and guess[i] in answers[j]:
                candidates -= 1
                break
            elif (numbers[i] == 1 and guess[i] not in answers[j]) or (numbers[i] == 1 and answers[j][i] == guess[i]):
                candidates -= 1
                break
            elif numbers[i] == 2 and answers[j][i] != guess[i]:
                candidates -= 1
                break
    return candidates



def guess(words, numbers):
    candidates = all_answers
    for i in range(len(words)):
        temp = update_candidates(words[i], numbers[i], candidates)
        candidates = temp
    
    guesses = dict()
    guesses_mean = dict()
    remainings_dict = dict()
    # print('candidates = ', candidates)
    index = 0
    for g in all_guesses:
        print(g, ' : ', int(100*index/len(all_guesses)),'%')
        index += 1
        number_of_remaining = []
        for c in candidates:
            number_of_remaining.append(length_of_remaining(g,c,candidates))
        guesses[g] = statistics.median(number_of_remaining)
        remainings_dict[g] = number_of_remaining
        # guesses_mean[g] = statistics.mean(number_of_remaining)
    
    # Formatting answer better
    min_median = guesses[min(guesses, key=guesses.get)]
    for g in guesses:
        if guesses[g] == min_median:
            guesses_mean[g] = statistics.mean(remainings_dict[g])
            
    answer = dict()
    for g in guesses_mean:
        if g in candidates:
            answer[g] = guesses_mean[g]
    
    print('MEDIAN = ', min_median)
    
    print('BEST impossible answers = ', sorted(guesses_mean.items(), key=lambda x: x[1], reverse=True))
    print('BEST possible answers = ', sorted(answer.items(), key=lambda x: x[1], reverse=True))
    
    print('CANDIDATES = ', candidates, ' AND length ', len(candidates))
        

guess(['reist',
'alone',
'bicep',
# 'wrong'
], 
[[0,1,0,0,0],
[0,2,2,0,2],
[2,0,0,1,0],
# [1,1,0,0,0]
])






# candidates =  ['after', 'alter', 'brute', 'cater', 'crate', 'earth', 'eater', 'enter', 'entry', 'ether', 'extra', 'forte', 'grate', 'hater', 'later', 'other', 'otter', 'outer', 'taker', 'tamer', 'taper', 'there', 'three', 'threw', 'tower', 'trace', 'trade', 'tread', 'trend', 'trope', 'trove', 'truce', 'truer', 'tuber', 'utter', 'voter', 'water', 'wrote']
# print(length_of_remaining('after', 'wrote', candidates))
def worst_candidate(guess):
    answer_length_candidates = dict()
    for a in all_answers:
        print(a)
        candidates = all_answers
        numbers = give_numbers(guess, a)
        temp = update_candidates(guess, numbers, candidates)
        candidates = temp
        answer_length_candidates[a] = len(candidates)
    print(sorted(answer_length_candidates.items(), key=lambda x: x[1], reverse=False))

print(worst_candidate('reist'))
