import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_dist = {}
    curr_links = corpus[page]

    damp_prob = (1 / len(corpus)) * (1 - damping_factor)

    for key in corpus.keys():
        if key not in curr_links:
            prob_dist[key] = damp_prob
        else:
            prob_dist[key] = ((1 / len(curr_links)) * damping_factor) + damp_prob

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    first_page = random.choice(list(corpus.keys()))
    master_dict = transition_model(corpus, first_page, damping_factor)
    prev_page = first_page
    for _ in range(n - 1):
        decision_num = round(random.random(), 2)
        if decision_num <= 0.84:
            if len(corpus[prev_page]) > 0:
                page = random.choice(list(corpus[prev_page]))
            else:
                page = random.choice(list(corpus.keys()))
        else:
            page = random.choice(list(corpus.keys()))
        new_prob = transition_model(corpus, page, damping_factor)
        for key in master_dict.keys():
            master_dict[key] += new_prob[key]
        prev_page = page

    for key in master_dict.keys():
        master_dict[key] = master_dict[key] / n

    return master_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    master_dict = {}
    num_elem = len(corpus)
    init_prob = 1 / num_elem
    for key in corpus.keys():
        master_dict[key] = init_prob
    while True:
        prev_copy = copy.deepcopy(master_dict)
        first_part = (1 - damping_factor) / len(corpus)
        for key in corpus.keys():

            total = 0
            link_list = get_link_list(corpus, key)
            for i in link_list:
                if len(corpus[i]) > 0:
                    total += master_dict[i] / len(corpus[i])
                else:
                    total += master_dict[i] / len(corpus)
            total_prob = (damping_factor * total) + first_part
            master_dict[key] = total_prob
        stop = True
        for key in master_dict.keys():
            dif = abs(prev_copy[key] - master_dict[key])
            if dif > 0.001:
                stop = False
        if stop:
            return master_dict


def get_link_list(corpus, page):
    """
    _summary_ : returns a list of all pages that link to a certain page
    """
    pages = []
    for key in corpus.keys():
        if key == page:
            if len(corpus[page]) == 0:
                pages.append(key)
            else:
                pass
        else:
            if page in corpus[key]:
                pages.append(key)
            elif len(corpus[key]) == 0:
                pages.append(key)
            else:
                pass
    return pages


if __name__ == "__main__":
    main()
