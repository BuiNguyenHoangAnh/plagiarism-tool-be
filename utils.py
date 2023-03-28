#import thư viện
import imp
from operator import truediv
import re, io, os, nltk

from docx import *

from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from nltk.corpus import stopwords
import nltk
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize

# https://github.com/Sudo-VP/Vietnamese-Word-Segmentation-Python
from vws.RDRSegmenter import RDRSegmenter
from vws.Tokenizer import Tokenizer

# khia báo hằng
STOPWORD_PATH = "vietnamese-stopwords-dash.txt"

################
# ĐỌC TÀI LIỆU #
################

# đọc từ file .txt
def read_txt_file(path):
    f = open(path, "r", encoding="utf8")
    document = f.read().lower()
    f.close()
    return document

def read_txt_files(path):
    dirs = os.listdir( path )

    data = []

    for file in dirs:
        if file == '.DS_Store':
                continue
        path_to_file=path+'/'
        file_name = file
        path_to_file += file_name
        # with open(path_to_file, 'r', encoding = 'latin1') as f: #eng
        with open(path_to_file, 'r', encoding = 'utf8') as f: #vie
            mylist = f.read()
            sent_tokenize_list = nltk.sent_tokenize(mylist)
            temp = []
            for i in sent_tokenize_list:
                sent = i.lower()
                sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
                temp.append(sent)
            mylist = re.sub(r"\n", "", mylist)
            data.append(mylist)
    return data

# đọc từ file word
def read_doc_files(path):
    document = Document(path)
    text = []
    for docpara in document.paragraphs:
        text.append(docpara.text)
    return text[0]

# đọc từ file pdf
def read_pdf_files(path):
    with open(path, 'rb') as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
    text = outfp.getvalue()
    return text

# đọc từ file xls
# def read_xls_files():
    # import pandas as pd
    # xl = pd.ExcelFile("corpus_final.xls")

    # df = xl.parse("File list")

    # c = df[['File','Category']]
    # print (c)

##############
# TIỀN XỬ LÝ #
##############

# tách từ (word segmentation)
def  word_segmentation(document):
    rdrsegment = RDRSegmenter()
    tokenizer = Tokenizer()
    doc = rdrsegment.segmentRawSentences(tokenizer, document)
    print("word segmentation: ", doc)
    return doc

# loại bỏ ký tự đặc biệt
def remove_punctuation_marks(document):
    doc = re.sub(r"\W", " ", document)
    print("remove punctuation marks: ", doc)
    return doc

# loại bỏ hư từ (stop word) (từ điển stop word: https://github.com/stopwords/vietnamese-stopwords)
def load_stop_words():
    stop_word_list = []
    with open(STOPWORD_PATH, encoding="utf8") as stop_words:
        for line in stop_words:
            word = re.sub(r"\n", "", line)
            stop_word_list.append(word)
    return stop_word_list

def remove_stop_words(document):
    stop_word_list = load_stop_words()
    doc = document
    # for word in document.split():
        # for stop_word in stop_word_list:
        # if word in stop_word_list:
        #     doc = doc.replace(word, "")
    words = [w for w in document.split() if not w in stop_word_list]
    doc = ' '.join(words)
    print("remove stop words: ", doc)
    return doc

#loại bỏ số
def remove_numbers(document):
    doc = re.sub(r"[0-9]", "", document)
    print("remove numbers: ", doc)
    return doc


# loại bỏ khoảng trắng thừa
def remove_spaces(document):
    doc = re.sub(r"\s+", " ", document, flags=re.I)
    print("remove spaces: ", doc)
    return doc

def preprocessing_doc(doc):
    doc = word_segmentation(doc)
    doc = remove_punctuation_marks(doc)
    # doc = remove_stop_words(doc)
    doc = remove_numbers(doc)
    doc = remove_spaces(doc)
    return doc

def preprocessing(source):
    data =[]
    for doc in source:
        doc = preprocessing_doc(doc)
        data.append(doc)
    return data

# CHECK PLAGIARISM
def check_plagiarism_with_threshold(value, threshold):
    if value>=threshold:
        print("WARNING: THIS DOCUMENT IS PLAGIARIZED")
        return True
    return False

# FOR ENGLISH
def preprocessing_english(text):
    stop_words = set(stopwords.words('english'))

    text_tokens = word_tokenize(text)
    # print(text_tokens)

    # for word in text_tokens_without_pm:
    #     if word in stopwords.words():
    tokens_without_sw_aray = [w for w in text_tokens if not w.lower() in stop_words]
    tokens_without_sw = ' '.join(tokens_without_sw_aray)
    
    text_tokens_without_pm = re.sub(r"\W", " ", tokens_without_sw)

    tokens_without_num = re.sub(r"[0-9]", "", text_tokens_without_pm)

    tokens_remove_spaces = re.sub(r"\s+", " ", tokens_without_num, flags=re.I)

    return tokens_remove_spaces