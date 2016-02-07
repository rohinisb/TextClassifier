import sys
import os
import re

# first argument will be the path containing sub directories with .txt files
path = sys.argv[1]

# directory structure for training data
positive = "/positive_polarity/"
negative = "/negative_polarity/"
positive_truth = "/positive_polarity/truthful_from_TripAdvisor"
positive_deceptive = "/positive_polarity/deceptive_from_MTurk"
negative_truth = "/negative_polarity/truthful_from_Web"
negative_deceptive = "/negative_polarity/deceptive_from_MTurk"

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

# list of unique words
vocabulary = []

# output model file
out = open("nbmodel.txt", "w")


# get all word count from files ending with .txt extension from the given directory path
def get_word_count(dir_path, word_count):
    files_list = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            if f.endswith(".txt"):
                files_list.append(os.path.join(root, f))
    for fl in files_list:
        word = open(fl, "r").read()
        word = re.sub('[^a-zA-Z\n]', ' ', word).lower()
        for w in word.split():
            if w not in stop_words:
                if w not in vocabulary:
                    vocabulary.append(w)
                if w in word_count:
                    word_count[w] += 1
                else:
                    word_count[w] = 1
    return word_count


# build the total count of each of the classes
def build_model(dic, header):
    out.write(header + " " + str(len(dic.keys())) + " " + str(sum(dic.values())) + "\n")
    for key, val in dic.items():
        out.write(key + " " + str(val) + "\n")


# add vocab words to the dictionary if not already present
def add_vocab(dic):
    for word in vocabulary:
        if word not in dic:
            dic[word] = 0
    return dic


def main():
    pos = dict()
    neg = dict()
    truthful = dict()
    deceptive = dict()
    pos = get_word_count(path+positive, pos)
    neg = get_word_count(path+negative, neg)
    pos = add_vocab(pos)
    neg = add_vocab(neg)
    print (len(pos.items()))
    print (len(neg.items()))
    del vocabulary[:]
    truthful = get_word_count(path+positive_truth, truthful)
    truthful = get_word_count(path+negative_truth, truthful)
    deceptive = get_word_count(path+positive_deceptive, deceptive)
    deceptive = get_word_count(path+negative_deceptive, deceptive)
    truthful = add_vocab(truthful)
    deceptive = add_vocab(deceptive)
    print (len(truthful.items()))
    print (len(deceptive.items()))
    build_model(pos, "POSITIVE")
    build_model(neg, "NEGATIVE")
    build_model(truthful, "TRUTHFUL")
    build_model(deceptive, "DECEPTIVE")
    out.close()

if __name__ == '__main__':
    main()
