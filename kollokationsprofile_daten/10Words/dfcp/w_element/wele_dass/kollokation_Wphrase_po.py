import re
from typing import Dict, List

import pandas as pd
from pandas.core.frame import DataFrame


def preprocess_text(filename: str) -> List:

    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.\t", line) != None:

                line = re.sub(r'\d+\.\ttok\s\sdass', "", line)
                listed_words.append(line.split())
                print(line.split())

    return listed_words


def count_collocations(preprocessed_list: List) -> Dict:
    word_count_dict = {}

    for listed_values in preprocessed_list:
        for value in listed_values:
            if value not in word_count_dict.keys():
                word_count_dict[value] = [
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                ]
                word_count_dict[value][listed_values.index(value)] += 1
            else:
                word_count_dict[value][listed_values.index(value)] += 1

    return word_count_dict


def save_as_csv(collocations: Dict, outfile_name: str) -> DataFrame:
    df = pd.DataFrame.from_dict(collocations, orient='index')

    return df.to_csv(outfile_name, sep='\t')


def main():

    preprocessed_text = preprocess_text('./annis_10word_po.txt')
    collocations = count_collocations(preprocessed_text)
    save_as_csv(collocations, './annis_10word_po.csv')


if __name__ == "__main__":
    main()
