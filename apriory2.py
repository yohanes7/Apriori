import numpy
import pandas
import pandas as pd
from collections import defaultdict
from itertools import chain, combinations


class Apriori2:
    def main(self, item_list, min_support, min_confidence):
        # Tahap 1
        C1_item_set = self.get_item_set(item_list)
        global_freq_item_set = dict()

        # Tahap 2
        global_item_set_with_sup = defaultdict(int)
        L1_item_set = self.get_above_min_sup(C1_item_set, item_list, min_support, global_item_set_with_sup)
        current_L_set = L1_item_set
        k = 2

        # Tahap 3 - 6
        while current_L_set:
            global_freq_item_set[k - 1] = current_L_set

            # Menggabungkan item_set dan eliminasi yang kembar
            candidate_set = self.get_union(current_L_set, k)
            # membuat Kombinasi item yang tidak ada pada current_L_set sebelum nya
            candidate_set = self.pruning(candidate_set, current_L_set, k - 1)

            # Mencari item yang berada di atas nilai min_support
            current_L_set = self.get_above_min_sup(
                candidate_set,
                item_list,
                min_support,
                global_item_set_with_sup
            )
            k += 1

        # Melakukan asosiasi rule
        rules = self.association_rule(global_freq_item_set, global_item_set_with_sup, min_confidence)
        return global_freq_item_set, rules

        #Pengambilan data dari excell
    def get_from_dir(self, file_dir):
        data = pd.read_excel(file_dir, sheet_name="2020-2021")
        a = data.groupby("TID")
        list_item = []
        for i in a.groups:
            groups = a.get_group(i)
            arr_groups = []
            for j in range(len(groups)):
                name = groups['Nama Barang'].iloc[j]
                arr_groups.append(name)
            list_item.append(arr_groups)
        return list_item

        # Menghitung penjualan terbanyak
    def get_top_item(self, filDir):
        data = pd.read_excel(filDir, sheet_name="2020-2021")
        unique = data.drop('TID', axis=1)
        unique['Jumlah'] = data.groupby('Nama Barang')['Jumlah'].transform('sum')
        unique = unique.drop_duplicates('Nama Barang')
        data_sort = unique.sort_values('Jumlah', ascending=False)
        return data_sort

        # Merger item dengan nama yang sama dalam 1 baris
    def get_item_set(self, item_list):
        tempItemSet = set()
        for item_set in item_list:
            for item in item_set:
                tempItemSet.add(frozenset([item]))

        return tempItemSet

    # Mencari item yang berada di atas nilai min_support
    def get_above_min_sup(self, item_set, item_set_list, min_sup, global_itemset_with_sup):
        freq_item_set = set()
        local_itemset_with_sup = defaultdict(int)

        # Mengitung frequensi item pada setiap transaksi
        for item in item_set:
            for item_seta in item_set_list:
                if item.issubset(item_seta):
                    global_itemset_with_sup[item] += 1
                    local_itemset_with_sup[item] += 1

        # Mengambil frequensi item sesuai min_support
        for item, sup_count in local_itemset_with_sup.items():
            if sup_count >= min_sup:
                freq_item_set.add(item)

        return freq_item_set

    # Menggabungkan item_set dan eliminasi yang kembar
    def get_union(self, item_set, length):
        return set([i.union(j) for i in item_set for j in item_set if len(i.union(j)) == length])

    # Kombinasi item yang tidak ada pada item_set sebelum nya
    def pruning(self, candidate_set, prev_freq_set, length):
        temp_candidate_set = candidate_set.copy()
        for item in candidate_set:
            subsets = combinations(item, length)
            for subset in subsets:
                if frozenset(subset) not in prev_freq_set:
                    temp_candidate_set.remove(item)
                    break

        return temp_candidate_set

    def powerset(self, s):
        return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

    # Melakukan asosiasi rule
    def association_rule(self, freq_item_set, itemset_with_sup, min_conf):
        rules = []
        for k, item_set in freq_item_set.items():
            for item in item_set:

                subsets = self.powerset(item)
                for s in subsets:
                    confidence = float(
                        itemset_with_sup[item] / itemset_with_sup[frozenset(s)]
                    )
                    if confidence > min_conf:
                        rules.append([set(s), set(item.difference(s)), int(confidence * 100)])

        return rules
