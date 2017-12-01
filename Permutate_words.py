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
def loadWords(dictionary="words.txt"):
    """loads words from a .json or .txt file
dictionary: "words.txt": the file the words are loading from
returns: a dict if .json
returns: a list if .txt"""
    try:
        if dictionary.endswith(".txt"):
            with open(dictionary,"r") as englishDictionary:
                validWords = [line.strip().lower() for line in englishDictionary]
                return validWords
        elif dictionary.endswith(".json"):
            with open(dictionary,"r") as englishDictionary:
                validWords = json.load(englishDictionary)
                return validWords
        else:
            return "Unknown file extension, use .txt or .json: "+dictionary
    except Exception as e:
        return str(e)

def filterWords(length=5, dictionary="words.txt"):
    """length: 5: length of the word to return
dictionary: "words.txt": the file the words are loading from, see load_words()
returns: a dict"""
    words = loadWords(dictionary)
    finalWords = {}
    for word in words:
        if len(word) == length:
            finalWords[word] = 1
    return finalWords

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
        
def permutations(word, endWord, wordDict, visited=[], noOfPermuations=100):
    """word: the starting word
end_word: the target or final word
word_dict: a dict of words that can be used, usually from filter_words()
visited: []: internal list used to track words, prevents loops
no_of_permuations: 100: the limit to permute
returns: -1 if no route could be found
returns: string of the word route, not including the start"""
    if len(word) != len(endWord):
        return None
    if noOfPermuations == 0:
        return None # Limit reached
    lst = permute(word, wordDict)
    lst.sort(key=lambda x: compareLongOrd(endWord,x))
    for word_ in lst:
        if word_ == endWord:
            return endWord
        elif word_ in visited:
            continue
        else:
            r = permutations(word_, endWord, wordDict, visited+[word_], noOfPermuations-1)
            if r is None:
                continue
            else:
                return word_+ " " + r
    return None # No words found

def permute(word, wordDict):
    """word: a word to change
word_dict: a dict of words of the same length as the word, see filter_words()
returns: list of words"""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    potentialWords = []
    for letter in range(len(word)):
        for alpha in alphabet:
            potWord = word[:letter] + alpha + word[letter+1:]
            if potWord in wordDict and potWord != word:
                potentialWords.append(potWord)
    return potentialWords

### GUI ###

class permuateGui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        startFrame = tk.Frame(self)
        tk.Label(master=startFrame, text="Enter the starting word:").pack()
        self.startWord = tk.Entry(master=startFrame)
        self.startWord.pack()
        startFrame.pack(side="left")

        endFrame = tk.Frame(self)
        tk.Label(endFrame, text="Enter the ending word").pack()
        self.endWord = tk.Entry(endFrame)
        self.endWord.pack()
        endFrame.pack(side="right")

        self.start = tk.Button(text="Start?",command=self.update)
        self.start.pack()
        self.wordLabel = tk.Label(text="")
        self.wordLabel.pack()
        
        self.permutedWordLabels = [tk.Label(text="") for _ in range(15)]
        for label in self.permutedWordLabels:
            label.pack()
            
    def update(self):
        for label in self.permutedWordLabels:
            label["text"] = ""
        
        startWord = self.startWord.get()
        endWord = self.endWord.get()
        if len(startWord) != len(endWord):
            self.start["text"] = "Words must be the same length"
        else:
            self.wordLabel["text"] = startWord
            wordList = permutations(startWord, endWord, filterWords(len(startWord)), noOfPermuations=15)
            wordList = wordList.split(" ")
            for x in range(0, len(wordList)):
                self.permutedWordLabels[x]["text"] = wordList[x]
        










    
