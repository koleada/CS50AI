import nltk
import sys
import re
import copy

nltk.download("punkt")

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
D -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
    S -> NP VP | S Conj S | S PP S 
    NP -> D N | N | D N PP | PP NP | D Adj N | N VP | Conj NP | D AP Adj N
    VP -> V | V NP | Conj N V | V PP | Adv VP | Conj V | V Adv NP 
    PP -> P NP | P | 
    AP -> Adj | Adj Adj
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
    words = nltk.tokenize.word_tokenize(sentence.lower())
    # check for at least 1 letter if none then remove
    for i in copy.deepcopy(words):
        if bool(re.search(r"[a-zA-Z]", i)) == False:
            words.remove(i)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np = []
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            if not any(
                isinstance(child, nltk.Tree) and child.label() == "NP"
                for child in subtree
            ):
                np.append(subtree)
    return np


if __name__ == "__main__":
    main()
