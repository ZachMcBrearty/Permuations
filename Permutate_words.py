# Zach McBrearty

# Idea:
# Word Ladder, convert the word "alice" into the word "genes" in 13 steps or less.
# You can only change one letter each step,
# You have to create a word in the English Dictionary each step

# Unoptimised, the same letter may change multiple times before moving on,
# e.g. permutations("flame", "zinky", filter_words()) has "winny vinny tinny pinny" before moving on
# Can be slow if words have lots of permutations

# Use:
# permutations( word you want to start with, word you end with, a dictionary of words the same length as the words)
# a visited list is used internally
# no_of_permutations is used as a limit, eg "alice" to "genes" in 13 steps would be:
# permutations("alice", "genes", filter_words(5), no_of_permuations(14))
# 14 as it has to permute "alice" as well



import json # used to load json dictionaries

import tkinter as tk # used for the GUI mode

# .json loading, "words_dictionary.json" and "words.txt" supplied by
# https://github.com/dwyl/english-words
def load_words(dictionary="words.txt"):
    """loads words from a .json or .txt file
dictionary: "words.txt": the file the words are loading from
returns: a dict if .json
returns: a list if .txt"""
    try:
        if dictionary.endswith(".txt"):
            with open(dictionary,"r") as english_dictionary:
                valid_words = [line.strip().lower() for line in english_dictionary]
                return valid_words
        elif dictionary.endswith(".json"):
            with open(dictionary,"r") as english_dictionary:
                valid_words = json.load(english_dictionary)
                return valid_words
        else:
            return "Unknown file extension, use .txt or .json: "+dictionary
    except Exception as e:
        return str(e)

def filter_words(length=5, dictionary="words.txt"):
    """length: 5: length of the word to return
dictionary: "words.txt": the file the words are loading from, see load_words()
returns: a dict"""
    words = load_words(dictionary)
    final_words = {}
    for word in words:
        if len(word) == length:
            final_words[word] = 1
    return final_words

def longOrd(string):
    """string: the string to be converted with ord()
returns: list"""
    return [ord(x) for x in string]

def compareLongOrd(target, guess):
    """"a heuristic that attempts to speed up the permutations
target: the string compared to
guess: the string compared to the guess
returns: int"""
    return sum([abs(x-y) for x, y in zip(longOrd(target), longOrd(guess))])
        
def permutations(word, end_word, word_dict, visited=[], no_of_permuations=100):
    """word: the starting word
end_word: the target or final word
word_dict: a dict of words that can be used, usually from filter_words()
visited: []: internal list used to track words, prevents loops
no_of_permuations: 100: the limit to permute
returns: -1 if no route could be found
returns: string of the word route, not including the start"""
    if no_of_permuations == 0:
        return None # Limit reached
    lst = permute(word, word_dict)
    lst.sort(key=lambda x: compareLongOrd(end_word,x))
    for word_ in lst:
        if word_ == end_word:
            return end_word
        elif word_ in visited:
            continue
        else:
            r = permutations(word_, end_word, word_dict, visited+[word_], no_of_permuations-1)
            if r is None:
                continue
            else:
                return word_+ " " + r
    return None # No words found

def permute(word, word_dict):
    """word: a word to change
word_dict: a dict of words of the same length as the word, see filter_words()
returns: list of words"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    potential_words = []
    for letter in range(len(word)):
        for alpha in alphabet:
            pot_word = word[:letter] + alpha + word[letter+1:]
            if pot_word in word_dict and pot_word != word:
                potential_words.append(pot_word)
    return potential_words

### GUI ###

class permuateGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()
        
        self.wordLabel = tk.Label(text="")
        self.wordLabel.pack()

    def createWidgets(self):
        tk.Label(text="Enter a word:").pack()
        self.word = tk.Entry()
        self.word.pack()
        self.start = tk.Button(text="Start?",command=self.update)
        self.start.pack()


    def update(self):
        self.wordLabel = tk.Label(text=self.word.get())
        self.wordLabel.pack_forget()
        self.wordLabel.pack()












    
