# import thư viện
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils import *

# LCS - Longest Common Subsequence
# Nguồn: https://blog.katastros.com/a?ID=00700-9d6c6da8-f25b-48ec-8eb8-d97bd291364e
def lcs(source, input):
    s1 = source.split()
    s2 = input.split()
    m=[[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)] #Generate 0 matrix, in order to facilitate subsequent calculations, one more column than the string length

    mmax=0 #The length of the longest match

    p=0 #The longest match corresponds to the last bit in s1

    for i in range(len(s1)):

        for j in range(len(s2)):

            if s1[i]==s2[j]:

                m[i+1][j+1]=m[i][j]+1

                if m[i+1][j+1]>mmax:

                    mmax=m[i+1][j+1]

                    p=i+1

    return s1[p-mmax:p],mmax #Return the longest substring and its length

def diff_lcs(source, input):
    s, m = lcs(source, input)
    p = 0
    if len(source.split()) == 0 or len(input.split()) == 0:
        return 0, s
    else:
        p = m/min(len(source.split()), len(input.split()))
    # print("lcs result: ", m/min(len(source.split()), len(input.split())))
    return p, s

# CS - Cosine Word Similarity
# Nguồn: https://towardsdatascience.com/what-is-cosine-similarity-how-to-compare-text-and-images-in-python-d2bb6e411ef0
def diff_cs(source, input):
    corpus = [source, input]
    count_vect = CountVectorizer()

    X_train_counts = count_vect.fit_transform(corpus)
    pd.DataFrame(X_train_counts.toarray(), columns=count_vect.get_feature_names_out(), index = corpus)

    vectorizer = TfidfVectorizer()
    trsfm=vectorizer.fit_transform(corpus)
    pd.DataFrame(trsfm.toarray(), columns=vectorizer.get_feature_names_out(), index = corpus)

    print("cs result: ", cosine_similarity(trsfm[0:1], trsfm)[0][1])

    return cosine_similarity(trsfm[0:1], trsfm)[0][1]

# Combine LCS & CS
def diff_lcs_cs(source, input, threshold_lcs_cs):
    print("LCS-CS")
    # value = []
    result = 0
    result_lcs, m = diff_lcs(source, input)
    result_cs = diff_cs(source, input)
    p = (result_lcs + result_cs)/2
    # value.append(p)
    if check_plagiarism_with_threshold(p, threshold_lcs_cs):
        # result = 1
        return True
    return False
