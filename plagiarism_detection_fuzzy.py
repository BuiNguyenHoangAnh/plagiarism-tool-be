# import thư viện 
# to do: implement lai thuat toan
from re import S
from unittest import result
from fuzzywuzzy import fuzz
import nltk
nltk.download()
from nltk.corpus import wordnet

from utils import *

p_threshold = 0.6

# Nguồn: https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe
def diff_fuzzy(source, input, threshold_fuzzy):
    # print("fuzzy")
    # result = []
    # p = fuzz.partial_ratio(source, input)
    # print(p)
    # #     result.append(fuzz.token_sort_ratio(doc, input)/100)
    # # return result
    # if p >= threshold_fuzzy:
    #     print("WARNING: THIS DOCUMENT IS PLAGIARIZED ")
    #     return True
    # return False

    result = []
    sim = []
    res = []
    f = 0
    for word1 in input.split():
    # print word1
        wordFromList1 = wordnet.synsets(word1)
        for word2 in source.split():
            # print word2
            wordFromList2 = wordnet.synsets(word2)

            if len(wordFromList1) == 0 or len(wordFromList2) == 0:
                f = 0
            else:
                s = wordFromList1[0].wup_similarity(wordFromList2[0])

                if word1 == word2:
                    f = 1
                elif s > p_threshold:
                    f = 0.5
                else:
                    f = 0
            res.append(f)
    Fs = 1
    muy = []
    sum = 0
    for value in res:
        Fs = Fs*(1 - value)
        muy.append(1 - Fs)
    for v in muy:
        sum += v

    print("len: ", len(muy))
    print("sum: ", sum)
    if len(muy) == 0:
        result = 0
    else:
        result = sum/(len(muy))
    print(result)

    if check_plagiarism_with_threshold(result, threshold_fuzzy):
        # result = 1
        return True
    return False