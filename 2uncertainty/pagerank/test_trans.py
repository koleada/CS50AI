import pytest
from pagerank import *


corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
page = "1.html"


def test_transition():

    assert (transition_model(corpus, 0.85, 100)) == {
        "1.html": 0.05,
        "2.html": 0.475,
        "3.html": 0.475,
    }


def main():
    # print(sample_pagerank(corpus, 0.85, 10000))
    print(iterate_pagerank(corpus, 0.85))


main()
