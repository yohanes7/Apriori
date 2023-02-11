import numpy
import pandas as pd

import apriory2

fileDir = r'./data.xlsx'

if __name__ == '__main__':
    top_item_count = 3
    min_support = 4
    min_confidence = 0.6

    apr = apriory2.Apriori2()
    data = apr.get_from_dir(fileDir)
    top_item = apr.get_top_item(fileDir)
    top_item.reset_index(drop=True).head(top_item_count).to_csv('top_item.csv')

    freq2, rules2 = apr.main(data, min_support=min_support, min_confidence=min_confidence)
    for k, v in freq2.items():
        freq2[k] = [list(n) for n in v]

    pa = pd.DataFrame(rules2)
    pa = pa.sort_values(by=2, ascending=False)
    pa.to_csv('result.csv')



