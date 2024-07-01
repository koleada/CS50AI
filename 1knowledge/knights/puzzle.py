from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # game rules implications
    Or(AKnave, AKnight),
    Biconditional(AKnight, Not(AKnave)),
    # sentence implications
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnight, BKnave),
    # if A is a Knight A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # if B is a knight B is not a knave
    Biconditional(BKnight, Not(BKnave)),
    # A is a Knight if an only id A and B are Knaves thus we arrive at a contradiction becuase A cant be a Knight and Knave
    Biconditional(AKnight, And(AKnave, BKnave)),
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnave, AKnight),
    Or(BKnight, BKnave),
    # if A is a Knight A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # if B is a knight B is not a knave
    Biconditional(BKnight, Not(BKnave)),
    #
    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(Biconditional(AKnave, AKnight)),
    Not(Biconditional(BKnave, BKnight)),
    Not(Biconditional(CKnave, CKnight)),
    #
    # If A is a Knight then B is a Knave
    Implication(AKnight, BKnave),
    # If B is a Knight then C is a Knave and B is a Knave hence we arrive at a contradiction
    Implication(BKnight, And(CKnave, BKnave)),
    # If B is a Knave (which it is), A and C are Knights
    Implication(BKnave, And(CKnight, AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
