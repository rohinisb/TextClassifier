import sys
import os
import re
import math


model_file = open("nbmodel.txt", "r")
out = open("nboutput.txt", "w")

# list of words to be omitted while building model
stop_words = ["mk", "fi", "ft", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against",
              "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst",
              "amongst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere",
              "are", "around", "as", "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been",
              "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill",
              "both", "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry",
              "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either",
              "eleven", "else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything",
              "everywhere", "except", "few", "fifteen", "fifty", "fill", "find", "fire", "first", "five", "for", "former", "formerly",
              "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have",
              "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
              "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its",
              "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile",
              "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name",
              "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not",
              "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others",
              "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather",
              "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side",
              "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
              "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there",
              "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this",
              "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards",
              "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were",
              "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein",
              "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why",
              "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]


def read_test(dir_path):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if f.endswith(".txt"):
                files_list.append(os.path.join(root, f))
    return files_list


def read_file(fl):
    d = dict()
    header = fl.readline().split()
    for i in range(int(header[1])):
        entry = fl.readline().split()
        d[str(entry[0])] = int(entry[1])
    return d


def classify():
    positive = read_file(model_file)
    negative = read_file(model_file)
    truthful = read_file(model_file)
    deceptive = read_file(model_file)

    p_total = len(positive.keys()) + sum(positive.values())
    n_total = len(negative.keys()) + sum(negative.values())
    t_total = len(truthful.keys()) + sum(truthful.values())
    d_total = len(deceptive.keys()) + sum(deceptive.values())

    files_list = read_test(sys.argv[1])
    for fl in files_list:
        word = open(fl, "r").read()
        word = re.sub('[^a-zA-Z\n]', ' ', word).lower()
        pos_prob = math.log(0.5)
        neg_prob = math.log(0.5)
        truthful_prob = math.log(0.5)
        deceptive_prob = math.log(0.5)
        for w in word.split():
            if w not in stop_words:
                if w in positive:
                    pos_prob += math.log((float(positive[w]) + 1) / p_total)
                if w in negative:
                    neg_prob += math.log((float(negative[w]) + 1) / n_total)
                if w in truthful:
                    truthful_prob += math.log((float(truthful[w]) + 1) / t_total)
                if w in deceptive:
                    deceptive_prob += math.log((float(deceptive[w]) + 1) / d_total)
        if truthful_prob > deceptive_prob:
            out.write("truthful ")
        else:
            out.write("deceptive ")
        if pos_prob > neg_prob:
            out.write("positive "+fl+"\n")
        else:
            out.write("negative "+fl+"\n")
    out.close()


classify()
