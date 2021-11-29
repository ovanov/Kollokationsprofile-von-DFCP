"""
This programm computes the HEATMAPS and STATISTICAL TESTS for the collocators that occur AFTER a dfcp or 'dass'
"""
import re
import pandas as pd
import scipy.stats as stats # import stat calculator
import matplotlib.pyplot as plt # plot graphs
import seaborn as sns # create heatmaps

import pos_plots.dass.plot_10words_pos as dass_pos # import other files functions


def create_lists(filename):
    """
    This function reads a filename and returns a list of lists
    The list consists of the 10 words, that occur after 'dass' and dfcp
    """
    dass_words = []
    listed_words = []
    with open(filename, 'r') as annis:
        for line in annis:
            if re.search(r"\d+\.\t", line) != None: # check if the line holds tabs

                line = re.sub(r'\d+\.\ttok\s\sdass', "", line) # strip dass off 
                dass_words.append(line.split())

            if re.search(r"\d+\.", line) != None: # ckeck if the line holds no tabs
                if re.search(r"\d+\.\ttok\s\sw\w+\sdass?", line) != None: # check if there is a w-element
                    line = re.sub(r'\d+\.\ttok\s\sw\w+\sdass?', "", line) # strip that part off 
                    listed_words.append(line.split())
                    # print(line.split())
                if re.search(r"\d+\.\s\stok\s\s.+\sdass?", line) != None: # check if there is a phrasal element
                    line = re.sub(r'\d+\.\s\stok\s\s.+\sdass?', "", line) # strip that part off 
                    listed_words.append(line.split())
                    # print(line.split())
                if re.search(r"\d+\.\ttok\s\sw\w+\s\w+\sdass?", line) != None: # check if there is a phrasal element and a w- element
                    line = re.sub(r'\d+\.\ttok\s\sw\w+\s\w+\sdass?', "", line) # strip that part off
                    listed_words.append(line.split())
                    # print(line.split())

    return dass_words,listed_words

def create_df(dass_words, dfcp_words):
    """
    this function creates a dictionary, that keeps track of each occurance of a word in a 'dass' context and 'dfcp' context
    it returns this dictionary
    """
    dass = {}
    dfcp = {}

    data = [dass, dfcp]

    for listed_values in dass_words: # acces single list
        for value in listed_values: # access single value
            if value not in data[0].keys(): # if this value is not in the dictionary
                data[0][value] = 0 # create a key value pair
                data[0][value] += 1 # and increment
            else: # if it already is in the dictionary
                data[0][value] += 1 # increment

    for listed_values in dfcp_words: # access single list
        for value in listed_values: # acess single value
            if value not in data[1].keys(): # if this value is not in the dictionary 
                data[1][value] = 0 # creat a key value pari
                data[1][value] += 1 # and increment
            else: # if it already is in the dictionary
                data[1][value] += 1 # increment

    return data

def create_csv(data, outfile_name):
    """
    This function takes the data and output file name and creates a csv, that can be used to create a heatmap
    """
    data = pd.DataFrame(data, index=['dass','dfcp']).transpose() # transpose the dataframe, so 'dass' and 'dfcp' are column names and the words are rows

    data = data.dropna(axis=0, how='all') # drop all NaN (not access) values. This way the calculation does not fail

    data_df = data.sort_values(by='dass',ascending=False) # sort value size by dass, we can create two heatmaps later
    data_df.to_csv(outfile_name, sep='\t') # write file
    return data_df  # return the dataframe


def create_heatmap(data_df):
    """
    This function takes the dataframe, that is sorted by 'dass'. we create two heatmaps
    One shows towards 'dass' sorted values. The other shows 'dfcp' sorted values
    """

    data_other = data_df.sort_values(by='dfcp', ascending=False) # create a copy, that is sorted by dfcp
    plt.figure() 
    sns.heatmap(data_df.head(15), annot=True, cmap="YlGnBu", fmt='g') # plot the heatmap

    plt.show() # show the heatmap, so it can be stored

    plt.figure() 
    sns.heatmap(data_other.head(15), annot=True, cmap="YlGnBu", fmt='g') # plot heatmap for 'dfcp'

    plt.show() # show heatmap, so it can be stored
    return


def fischers_exact_test_and_x2(data_df, filename, context):
    """
    This function uses scipy stats to compute the Chi2 and Fisher's exact test in a loop
    It takes the filename (csv) and takes the words and puts a table into a test
    """

    data = data_df.dropna(axis=0, how='all') # make sure, that there are no NaN values
    collocators = dass_pos.calculate_collocators(filename) # compute the collocatiors for each step
    x, y = dass_pos.create_axis(collocators) # separate the collocators in x and y values

    no_context = { # these are the occurances of the words in the corpus. we need these for the calculation of both tests
            'du':9852, 'ich': 13285, 'es':6841, 'me':1316, 'er': 3571, 'rechne':19, 'dir':3345, 'dr':1254, 'das':8866, 'hät':441,
            'bisch':2431, 'bi':5534, 'muesch':580, 'isch':11249, 'zug': 748, 'gässe':42, 'marit': 117, 'lade':92, 'experte':4,
            ':)':9744, 'GA': 14, ',':16575, '?':36708, 'der':2248, 'nur':2541, 'alles':1524, 'dank':77, 'i':8603, 'd':3375, "d'":3375,
            's':2696, 'uf':5436, 'nid':4173, 'und':15031, 'nöd':3608, 'will':1598, 'so':11272, 'aber':6605, 'de':13130, 'no':10438,
            'am':5963, 'au':9613, 'mit':6397, 'gwüsst': 253, 'gfragt':91, 'gmerkt':184, 'gseid':167, 'weiss': 1666, 'nöd':3608,
            'glaub':1196, 'usegfunde':49, 'het':4590, 'wasi':87, 'was':5269, 'gross':201, 'em':1285, 'heisst':486, 'au':9613,
            'wo':3664, 'erst':800, 'ageh':26, 'weisch':599, 'gmeint':411, 'gsi':2861, 'muni':138, 'sie':3506
            }
    
    
    for i in range(len(y[0])): # for the length of one sentence, that holds 'dass' (10)
        for j in range(len(y[i])): # for each index of the words in the sentence
            if x[i][j] in no_context.keys(): # check if the word is in the no_context dictionary
                print(f"Checking the p-value for {context} and '{x[i][j]}'")
                print("")
                ### COMPUTE both CHI2 and Fisher's exact test
                oddsratio, pvalue = stats.fisher_exact([[y[i][j], 1696-y[i][j]], [no_context[x[i][j]]-y[i][j], 213598-y[i][j]]])
                chi, pval, dof, ex = stats.chi2_contingency([[y[i][j], 1696-y[i][j]], [no_context[x[i][j]]-y[i][j], 213598-y[i][j]]])
                ### PRINT the values
                print("Chi Square Value & and critical value and DOF:  ", round(chi,3), pval, dof)
                print("ODD ration, Fisher's p-value                 :  ", round(oddsratio, 6), pvalue)
                print("\n+----------------+\n")
    
    return


def main():
    """
    uncomment or comment certain fucntions that you want to use or test
    please change the path, in order to use the programm propperly
    """
    dass_words, dfcp_words = create_lists("/home/jova/Tresors/organic/Uni/Almanistik/HS21/Bachelorarbeit/python/kollokationsprofile_daten/10Words/all_pos.txt") 
    data = create_df(dass_words, dfcp_words)
    data_df = create_csv(data,"/home/jova/Tresors/organic/Uni/Almanistik/HS21/Bachelorarbeit/python/kollokationsprofile_daten/10Words/all_pos.csv")
    create_heatmap(data_df) # plot heatmaps
    ## 'dass' wörter danach
    # fischers_exact_test_and_x2(data_df, '~/Tresors/organic/Uni/Almanistik/HS21/Bachelorarbeit/python/kollokationsprofile_daten/10Words/dass/annis_10word_po.csv', 'dass')

    ## dfcp wörter danach
    # fischers_exact_test_and_x2(data_df, '~/Tresors/organic/Uni/Almanistik/HS21/Bachelorarbeit/python/kollokationsprofile_daten/10Words/dfcp/w_tot_pos.csv', 'dfcp')



if __name__ == "__main__":
    main()
