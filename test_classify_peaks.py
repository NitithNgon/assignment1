from iterate_event_file import *
import csv

def dict_to_csv(dictionary, filename):
    keys = list(dictionary.keys())
    values = list(dictionary.values())

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(zip(*values))

collect_peaks_results_dict = iterate_event_file("to_Peiam")
print(collect_peaks_results_dict)
dict_to_csv(collect_peaks_results_dict, "collect_peaks_results.csv")