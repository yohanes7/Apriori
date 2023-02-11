import pandas as pd

import apriory2

#letak data
fileDir = r'./data.xlsx'

if __name__ == '__main__':
    top_item_count = 3
    min_support = 4
    min_confidence = 0.6

    apr = apriory2.Apriori2()
    # Untuk mengolah data supaya lebih mudah membaca pada algoritma apriori (Preprocessing)
    data = apr.get_from_dir(fileDir)
    # Untuk mengambil item yang paling laris
    top_item = apr.get_top_item(fileDir)
    # Mengambil berdasarkan top item count di ubah menjadi file csv
    top_item.reset_index(drop=True).head(top_item_count).to_csv('top_item.csv')

    # Memanggil main fungsi dari class apriory2
    freq2, rules2 = apr.main(data, min_support=min_support, min_confidence=min_confidence)
    # freq2 = ini nama item dengan kombinasi
    # rules2 = kombinasi item dengan nilai confidence

    # Mengubah data dari array ke dataframe supaya bisa menampilkan csv
    pa = pd.DataFrame(rules2)
    pa = pa.sort_values(by=2, ascending=False)
    pa.to_csv('result.csv')



