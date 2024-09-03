"""
Doc String Part:
This module implements indexing and retrieval functionalities for text documents.

Functions:
1. printMenu: Displays a menu to the user and prompts for input to perform indexing or exit the program.
2. readFolderContent: Reads the contents of text files in a specified folder.
3. stopWordRemoval: Removes stop words from a given text.
4. punctuationRemoval: Removes punctuation marks from a given text.
5. appendTermDocFreq: Appends term-document frequency information to a file.
6. genIndex: Generates an index of terms with their corresponding document frequencies.
7. indexing: Performs indexing of text documents in a folder and generates an index.
8. get_term_frequency: Retrieves the term frequency of a term in a document.
9. get_number_of_documents: Retrieves the number of documents containing a specific term.
10. search: Performs a search operation based on a query and returns scores for documents.

"""
import os
import math

#indexing module

def printMenu():
    print("Menu: ")
    choice = input("Please enter 1 for indexing and 3 to exit: ")
    while True: 
        if choice == '1':
            print("1. Indexing")
            break
        elif choice == '3':
            print("3. Exit")
            break
        else:
            choice = input("Invalid input. Please enter 1 for indexing and 3 to exit: ")
            
    return int(choice)

printMenu() #testing

def readFolderContent():
    dataset_folder = input("Enter your folder: ")
    if not os.path.exists(dataset_folder):
        print("Dataset folder does not exist")
        return []
    
    file_content = []
    for files in os.listdir(dataset_folder):
        if files.endswith(".txt"):
            file_path = os.path.join(dataset_folder, files)
            with open(file_path, "r") as file: 
                file_content.append(file.read())
    return file_content


def stopWordRemoval(text):
    stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself','yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their','theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be','been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as','until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above','below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when','where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own','same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're','ve', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',"haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"}
    output = []
    for word in text.split():
        if word.lower() not in stop_words:
            output.append(word)
    filtered_word = ' '.join(output)
    return filtered_word

# print(stopWordRemoval("The monkeys jump on the bed")) #testing

def punctuationRemoval(text):
    punctuations =  '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    txt = ""
    for char in text:
        if char not in punctuations:
            txt += char         
    return txt

# print(punctuationRemoval("The monkeys jump on the bed !!!")) #testing

def appendTermDocFreq(cleanText, termDocFreqFile):
    output = ""
    with open(termDocFreqFile, "a") as file:
        print("Term doc #freq")
        doc_id = 0  
        for term in cleanText.split():
            term_frequency = cleanText.count(term)
            file.write(term + " " + str(doc_id) + " " + str(term_frequency) + "\n")
            output += term + " " + str(doc_id) + " " + str(term_frequency) + "\n" 
            doc_id += 1  
            if doc_id > 300: 
                doc_id = 0
    return output
      
# print(appendTermDocFreq("recipe sweet sugar", "term.txt")) #testing

def genIndex(termDocFreqFile):
    index = {}
    with open(termDocFreqFile, "r") as file:
        for line in file: 
            term, docID, freq = line.split()
            docID = int(docID)
            freq = int(freq)
            
            if term not in index: 
                index[term] = {docID:freq}
            else:
                index[term][docID] = freq


    return index
         
# print(genIndex("term.txt")) #testing
         
def indexing():
    doc_contents = readFolderContent()
    termDocFreqFile = "term_and_frequency.txt"
   
    for content in doc_contents:
        content_without_punctuations = punctuationRemoval(content)
        content_without_stopwords = stopWordRemoval(content_without_punctuations)
        appendTermDocFreq(content_without_stopwords, termDocFreqFile)
       
    index = genIndex(termDocFreqFile)        
    
    return index
            
print(indexing()) #module implementation

#retrieval module
def get_term_frequency(term, doc_id, termDocFreqFile):
    with open(termDocFreqFile, "r") as file: 
        for line in file:
            term_file, doc_id_file, freq = line.split()
            if term_file == term and int(doc_id_file) == doc_id:
                return int(freq)
    return 0      
        
def get_number_of_documents(term, termDocFreqFile):
    document_ids = set()  
    with open(termDocFreqFile, "r") as file:
        for line in file:
            data = line.split()
            if len(data) == 3:  
                term_file, doc_id, _ = data
                if term_file == term:
                    document_ids.add(int(doc_id))
    return len(document_ids)
                

def search(query):
    scores = {} 
    query_terms = query.split()
    total_docs = 300
    
    for doc_id in range(1, total_docs + 1):
        score = 0
        for term in query_terms:
            tf = get_term_frequency(term, doc_id, "term_and_frequency.txt")
            df = get_number_of_documents(term, "term_and_frequency.txt")
            if tf > 0 and df > 0:
                score += tf * math.log(total_docs/df)
        scores[doc_id] = score
    return scores
    
print(search("Ontario")) #testing