# wordle-solver

The important scripts in this repo are wordle-solver.py and test.py (to be renamed).

Wordle is a word puzzle where the user seeks to guess a 5 letter word. 
The user gets 6 guesses and is told if each letter is : 
0: not in the final word
1: in the final word but in the wrong position
2: in the final word in the right position

Using a list of over 370 thousand words (including the ones that are not 5 letters long)
And using a list of over 2 thousand words (possible wordle solutions)
We use two different approaches in finding the optimal guess to input in wordle
The first (naive approach) is in wordle-solver.py (only uses the possible wordle solutions):
  The script runs through all the possible wordle answers and deletes the ones that are not 
  possible given the feedback
  Then, the script sums the frequency of each letter (minus duplicates) in the
  list of remaining answers, and returns a dictionary with a sorted dictionary using these sums

Using this strategy I have found that the ideal first word to use is ALERT

This is an efficient way to solve wordle puzzles but it is not optimal.
The optimal solution uses information theory. Instead of using letter frequency as our main 
criteria to determine a good guess, we use the guess' median length of remaining answers.
Essentially, we are not seeking to input a word with the highest sum of frequency letters
We are seeking to input a word that would minimize the size of the possible remaining answers.

We use a larger set of potential guesses (hence the initial longer list of 370k words)
We cycle through each potential guess and compare that guess to each potential answer
We save the length of the remaining answers in an array (one for each answer)
We then save this in a dictionary as dict[guess] = median length of remaining answers
We then sort this dictionary (with minimum values as being optimal).

Using this strategy I have found that the ideal first word to use is REIST

I then added some formatting conditions to further help. 
If we get a lot of answers with the same minimal median value, we sort further by sorting this 
sub-dictionary by mean (with minimum values as being optimal). 
This gives us the ideal solution.

I have been inspired by this youtube video if you want to check it out : 
https://www.youtube.com/watch?v=v68zYyaEmEA


The next step would be to find the average number of guesses necessary to find a random answer
Unfortunately this would take a very very long time. Some solutions can take a couple minutes
to compute and this compounded average would probably take days or weeks to compute.

The next step is to create a web service that allows users to input their wordle guesses in a 
web page that would then compute the ideal next guess. Although including such code in a browser 
is quite tricky...
