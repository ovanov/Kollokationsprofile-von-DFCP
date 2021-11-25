import re
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame


def preprocess_text(filename: str) -> List:
    """
    This function reads a filename and returns a list of lists
    The list consists of the 10 words, that occur before 'dass'
    """
    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.", line) != None: # take only the correct lines
                line = re.sub(r'\d+\.\s\stok\s\s', "", line) # strip off the beginning, which is not needed

                if re.search(r"w\w+\sdass?\s$", line): # check if there is a w-element dfcp
                    line = re.sub(r'w\w+\sdass?\s$', "", line) # strip that part off
                    if len(line.split()[::-1]) == 11: # if the words still do contain one word to much, pop that remaining element
                        reverse = line.split()[::-1]
                        listed_words.append(reverse[1:])
                    else: # else, just append the list, if the length is sufficient
                        listed_words.append(line.split()[::-1])

                if re.search(r"w\w+\s\w+\sdass?\s$", line): # check if there is a w-element and a phrasal component
                    line = re.sub(r'w\w+\s\w+\sdass?\s$', "", line) # strip that part off
                    if len(line.split()[::-1]) == 11:  # if the words still do contain one word to much, pop that remaining element 
                        reverse = line.split()[::-1]
                        listed_words.append(reverse[1:])
                    else: # else, just append the list, if the length is sufficient
                        listed_words.append(line.split()[::-1])

                if re.search(r'uf\s\w+\s\w+\sdass?\s$',line) != None: # check if there is an 'uf' preposition with a phrasal component
                    line = re.sub(r'uf\s\w+\s\w+\sdass?\s$', "", line) # strip that part off
                    if len(line.split()[::-1]) == 11:# if the words still do contain one word to much, pop that remaining element 
                        reverse = line.split()[::-1]
                        listed_words.append(reverse[1:])
                    else: # else, just append the list, if the length is sufficient
                        listed_words.append(line.split()[::-1])

                if re.search(r'\w+\sw\w+\sdass?\s$',line) != None: # check if the is a preposition and a w-element 
                    line = re.sub(r'\w+\sw\w+\sdass?\s$', "", line) # strtip that part off 
                    if len(line.split()[::-1]) == 11: # if the words still do contain one word to much, pop that remaining element
                        reverse = line.split()[::-1]
                        listed_words.append(reverse[1:])
                    else: # else, just append the list, if the lenght is sufficient
                        listed_words.append(line.split()[::-1])

    return listed_words


def count_collocations(preprocessed_list: List) -> Dict:
    """
    This function reads a list and counts the 10 most occuring collocators in the 10 position before 'dass'
    The dictionary takes the word as a key and the occurances as a enumeration as values
    """
    word_count_dict = {}

    for listed_values in preprocessed_list: # access single list 
        for value in listed_values: # access single value
            if value not in word_count_dict.keys(): # if no value is in the dictionary
                word_count_dict[value] = [ # create list of 10 zeros, in order to represent the 10 positions
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
                word_count_dict[value][listed_values.index(value)] += 1 # increment at the correct number 
            else:
                word_count_dict[value][listed_values.index(value)] += 1

    return word_count_dict


def save_as_csv(collocations: Dict, outfile_name: str) -> DataFrame:
    df = pd.DataFrame.from_dict(collocations, orient='index')

    return df.to_csv(outfile_name, sep='\t')


def main():

    preprocessed_text = preprocess_text('./w_tot_pre.txt') # read file (txt) : change file path, if needed
    collocations = count_collocations(preprocessed_text)
    save_as_csv(collocations, './w_tot_pre.csv') # write csv from collocations (list[list[(tuple)]])



if __name__ == "__main__":
    main()
