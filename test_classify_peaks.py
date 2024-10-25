from itertools import zip_longest
from iterate_event_file import iterate_event_file
import csv

def dict_to_csv(dictionary, filename):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    print(len(keys))
    print(len(values))
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(list(zip_longest(*values,fillvalue="")))

collect_peaks_results_dict = iterate_event_file("to_Peiam")
print(collect_peaks_results_dict)
dict_to_csv(collect_peaks_results_dict, "collect_peaks_results.csv")