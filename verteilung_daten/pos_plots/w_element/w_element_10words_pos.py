from typing import Tuple, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def calculate_collocators(filename: str) -> List[List[Tuple]]:
    df_pos = pd.read_csv(f'{filename}', sep='\t')
    freq_collocators = []

    for n in range(10):
        # print(f"SORTED AT COLUMN: {n}")
        sorted_pos = df_pos.sort_values(f'{str(n)}',ascending=False)
        freq_collocators.append([])
        for m in range(10):
            counter = n
            freq_collocators[n].append(tuple([sorted_pos.iloc[m][counter+1], sorted_pos.iloc[m][0]]))

    return freq_collocators


def create_axis(collocators: List[List[Tuple]]):
    x = []
    y = []

    for position in collocators:
        x.append([])
        y.append([])
            
    for m in range(10):
        for n in range(10):
            x[m].append(collocators[m][n][1])
            y[m].append(collocators[m][n][0])

    return x, y


def draw_plot(x_ax, y_ax): # all after dass

    plt.title("10 häuffigste Kollokatoren in 10 positionen nach DFCP mit W-Element")
    plt.xlabel("Positionen")
    plt.ylabel("Häuffigkeit")

    for i in range(len(y_ax[0])):
        # plt.plot([pt[i] for pt in x_ax[0]], [pt[i] for pt in y_ax[0]], label = f'id {i}')
        # plt.plot(np.asarray(x_ax), np.asarray(y_ax), label = f'id {i}')
        
        label = ""
        for l in [pt for pt in x_ax[i]]:
            label += f'{l} , '
        plt.plot([i+1,i+1,i+1,i+1,i+1,i+1,i+1,i+1,i+1,i+1], [pt for pt in y_ax[i]], 'o', label = label)
    # plt.plot([1,2,3,4,5,6,7,8,9,10], [pt for pt in y_ax[0]], 'o', label = f'{[pt for pt in x_ax[0]]}')

    plt.legend(prop={'size':7})
    plt.show()

    return


def draw_plot_1dass(x_ax, y_ax, pos): # first pos after dass

    positionen = ['erste', 'zweite', 'dritte', 'vierte', 'fünfte', 'sechste', 'siebte', 'achte', 'neunte', 'zehnte']
    plt.title("10 häuffigste Kollokatoren in 10 positionen nach DFCP mit W-Element")
    plt.xlabel(f"Kollokatoren ({positionen[pos]} Position nach DFCP)")
    plt.ylabel("Häuffigkeit")

    x_ax[pos] = [
            pt if not str(pt).startswith('emoji')
            else 'emoji'
            for pt in x_ax[pos]
            ]

    x_ax[pos] = [
            pt if not str(pt).startswith('media')
            else 'media'
            for pt in x_ax[pos]
            ]
    
    x_ax[pos] = [
            pt if not str(pt).startswith('redacted')
            else 'media'
            for pt in x_ax[pos]
            ]

    for i in range(len(y_ax[0])):
        barlist = plt.bar(x_ax[pos][i], y_ax[pos][i])
        barlist[0].set_color('blue')
        plt.xticks(rotation=45)

    plt.show()

    return


def main():
    freq_collocators = calculate_collocators('~/Tresors/organic/Uni/Almanistik/HS21/Bachelorarbeit/python/kollokationsprofile_daten/10Words/dfcp/w_element/w_pos.csv')

    x_ax, y_ax = create_axis(freq_collocators) 

    draw_plot(x_ax, y_ax)

    for pos in range(10):
        draw_plot_1dass(x_ax, y_ax, pos)


if __name__ == '__main__':
    main()
