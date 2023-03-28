from utils import *
from plagiarism_detection_ngram import *
from plagiarism_detection_lcs_cs import *
from plagiarism_detection_fuzzy import *

def plagiarism_detection(source, input, n, threshold_ngram, threshold_lcs_cs, threshold_fuzzy):
    temp = False
    count = 1
    for data in source:
        print("doc: ", count)
        # temp = [pool.apply(diff_ngram(data, input, n, threshold_ngram)) for data in source]
        temp = diff_ngram(data, input, n, threshold_ngram)
        count += 1
        if temp:
            # pool.close() 
            return 1

    count = 1
    for data in source:
        print("doc: ", count)
        temp = diff_lcs_cs(data, input, threshold_lcs_cs)
        count += 1
        if temp:
            # pool.close() 
            return 1

    count = 1
    for data in source:
        print("doc: ", count)
        temp = diff_fuzzy(data, input, threshold_fuzzy)
        count += 1
        if temp:
            # pool.close() 
            return 1
    # pool.close() 
    return 0