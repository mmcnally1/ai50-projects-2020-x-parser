import nltk
import sys
from nltk import word_tokenize

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> NP VP NP
S -> NP VP NP NP
S -> NP VP Conj NP VP
S -> NP VP P NP VP
S -> NP VP Conj VP
NP -> Det N P Det N
NP -> Det N P N
NP -> P Det N P Det N
NP -> N P N
NP -> Det N
NP -> N
VP -> V
VP -> V Adv
VP -> Adv V
VP -> V NP
VP -> V P NP
VP -> V Det NP
VP -> Adv V NP
VP -> V Det Adj NP
VP -> V P Det Adj N
VP -> V P Det NP Adv
VP -> V Det N P N
VP -> V Det Adj NP P NP
VP -> V NP P Det Adj NP
VP -> V Det Adj NP P NP
VP -> V Det Adj Adj Adj NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    word_list = []
    words = sentence.lower()
    words = word_tokenize(words)
    for word in words:
        if word.isalnum():
            word_list.append(word)
    return word_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np = []
    phrase = []
    for subtree in tree:
        s = subtree.label()
        if s == "NP":
            np.append(subtree)
        try:
            for sub in subtree:
                s2 = sub.label()
                if s2 == "NP":
                    np.append(sub)
        except:
            continue
    return np

if __name__ == "__main__":
    main()
