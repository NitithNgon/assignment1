import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
import matplotlib.pyplot as plt
from typing import List

def events_situation(fuzzificaton_dict: dict) -> dict:
    filtered_dict = dict(filter(lambda d: d[1]>0, fuzzificaton_dict.items()))
    filtered_dict.update((x, float(round(y*100,2))) for x, y in filtered_dict.items())
    sorted_by_values_dict = dict(sorted(filtered_dict.items(), key=lambda item: item[1] , reverse=True))
    return sorted_by_values_dict

def fuzzy_inference_sys(Ax0_peak_densty: float, Ax1_peak_densty: float) -> List:
    x_peak_densty = np.arange(-10, 2001, 1)
    y_durability = np.arange(0, 109, 1)

    # member ship func
    bad_events = mf.trapmf(x_peak_densty,[-10,-10,-2,-1])
    good_events = mf.pimf(x_peak_densty,-2,0,20,30)
    bad_events_raining = mf.pimf(x_peak_densty,20,90,510,1650)
    bad_events_dirtyAX = mf.smf(x_peak_densty,310,990)
    
    durability_verylow = mf.trapmf(y_durability, [0, 0, 12, 24])
    durability_low = mf.trapmf(y_durability, [12, 24, 36, 48])
    durability_mid = mf.trapmf(y_durability, [36, 48, 60, 72])
    durability_high = mf.trapmf(y_durability, [60, 72, 84, 96])
    durability_veryhigh = mf.trapmf(y_durability, [84, 96, 108, 108])

    # fuzzificaton
    Ax0_fit_good_events, Ax1_fit_good_events = fuzz.interp_membership(x_peak_densty, good_events, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, good_events, Ax1_peak_densty)
    Ax0_fit_bad_events_raining, Ax1_fit_bad_events_raining = fuzz.interp_membership(x_peak_densty, bad_events_raining, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, bad_events_raining, Ax1_peak_densty)
    Ax0_fit_bad_events_dirtyAX, Ax1_fit_bad_events_dirtyAX = fuzz.interp_membership(x_peak_densty, bad_events_dirtyAX, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, bad_events_dirtyAX, Ax1_peak_densty)
    Ax0_fit_bad_events, Ax1_fit_bad_events = fuzz.interp_membership(x_peak_densty, bad_events, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, bad_events, Ax1_peak_densty)
    # print("Ax0_fit_good_events | Ax1_fit_good_events : ", Ax0_fit_good_events*100, "% | ", Ax1_fit_good_events*100, "%")
    # print("Ax0_fit_bad_events_raining | Ax1_fit_bad_events_raining : ", Ax0_fit_bad_events_raining*100, "% | ", Ax1_fit_bad_events_raining*100, "%")
    # print("Ax0_fit_bad_events_dirtyAX | Ax1_fit_bad_events_dirtyAX : ", Ax0_fit_bad_events_dirtyAX*100, "% | ", Ax1_fit_bad_events_dirtyAX*100, "%")
    # print("Ax0_fit_bad_events | Ax1_fit_bad_events : ", Ax0_fit_bad_events*100, "% | ", Ax1_fit_bad_events*100, "%")


    # fig, (ax0, ax1) = plt.subplots(nrows = 2, figsize =(15, 8))
    # ax0.plot(x_peak_densty, bad_events, 'g', linewidth = 2, label = 'bad_events')
    # ax0.plot(x_peak_densty, good_events, 'r', linewidth = 2, label = 'good_events')
    # ax0.plot(x_peak_densty, bad_events_raining, 'm', linewidth = 2, label = 'bad_events_raining')
    # ax0.plot(x_peak_densty, bad_events_dirtyAX, 'b', linewidth = 2, label = 'bad_events_dirtyAX')
    # ax0.set_xticks(np.arange(-50, 2001, step=50))
    # ax0.set_title('member ship func')
    # ax0.legend()
    
    # ax1.plot(y_durability, durability_verylow, 'r', linewidth = 2, label = 'verylow')
    # ax1.plot(y_durability, durability_low, 'g', linewidth = 2, label = 'low')
    # ax1.plot(y_durability, durability_mid, 'b', linewidth = 2, label = 'mid')
    # ax1.plot(y_durability, durability_high, 'y', linewidth = 2, label = 'high')
    # ax1.plot(y_durability, durability_veryhigh, 'm', linewidth = 2, label = 'veryhigh')
    # ax1.set_xticks(np.arange(0, 109, step=10))
    # ax1.set_title('Risk')
    # ax1.legend()

    # plt.tight_layout()
    # plt.show()


    # rules layer1 (MIN=AND)
    durability_unacceptable_rule1 = np.fmin( np.fmin(Ax0_fit_bad_events, Ax1_fit_bad_events), durability_verylow)
    durability_unacceptable_rule2 = np.fmin( np.fmin(Ax0_fit_bad_events, Ax1_fit_bad_events_dirtyAX), durability_verylow)
    durability_unacceptable_rule3 = np.fmin( np.fmin(Ax0_fit_bad_events_dirtyAX, Ax0_fit_bad_events), durability_verylow)
    durability_unacceptable_rule4 = np.fmin( np.fmin(Ax0_fit_bad_events, Ax1_fit_bad_events_raining), durability_verylow)
    durability_unacceptable_rule5 = np.fmin( np.fmin(Ax0_fit_bad_events_raining, Ax1_fit_bad_events), durability_verylow)
    durability_unacceptable_rule6 = np.fmin( np.fmin(Ax0_fit_bad_events, Ax1_fit_good_events), durability_verylow)
    durability_unacceptable_rule7 = np.fmin( np.fmin(Ax0_fit_good_events, Ax1_fit_bad_events), durability_verylow)


    durability_verylow_rule1 = np.fmin(np.fmin(Ax0_fit_bad_events_dirtyAX, Ax1_fit_bad_events_dirtyAX), durability_verylow)

    durability_low_rule1 = np.fmin( np.fmin(Ax0_fit_bad_events_raining, Ax1_fit_bad_events_dirtyAX), durability_low)
    durability_low_rule2 = np.fmin( np.fmin(Ax0_fit_bad_events_dirtyAX, Ax1_fit_bad_events_raining), durability_low)

    durability_mid_rule1 = np.fmin( np.fmin(Ax0_fit_bad_events_raining, Ax1_fit_bad_events_raining), durability_mid)
    durability_mid_rule2 = np.fmin( np.fmin(Ax0_fit_good_events, Ax1_fit_bad_events_dirtyAX), durability_mid)
    durability_mid_rule3 = np.fmin( np.fmin(Ax0_fit_bad_events_dirtyAX, Ax1_fit_good_events), durability_mid)

    durability_high_rule1 = np.fmin( np.fmin(Ax0_fit_good_events, Ax1_fit_bad_events_raining), durability_high)
    durability_high_rule2 = np.fmin( np.fmin(Ax0_fit_bad_events_raining, Ax1_fit_good_events), durability_high)

    durability_veryhigh_rule1 = np.fmin( np.fmin(Ax0_fit_good_events, Ax1_fit_good_events), durability_veryhigh)

    
    # rules layer2 (output layer) (MAX=OR)
    output_durability_verylow = np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(np.fmax(durability_verylow_rule1, durability_unacceptable_rule1), durability_unacceptable_rule2), durability_unacceptable_rule3), durability_unacceptable_rule4), durability_unacceptable_rule5), durability_unacceptable_rule6), durability_unacceptable_rule7)
    output_durability_low = np.fmax(durability_low_rule1, durability_low_rule2)
    output_durability_mid = np.fmax( np.fmax(durability_mid_rule2, durability_mid_rule3), durability_mid_rule1)
    output_durability_high = np.fmax(durability_high_rule1, durability_high_rule2)
    output_durability_veryhigh = durability_veryhigh_rule1
    output_durability0 = np.zeros_like(y_durability)
    
    # outputs of model
    output_durability = np.fmax(np.fmax(np.fmax(np.fmax(output_durability_verylow, output_durability_low), output_durability_mid), output_durability_high), output_durability_veryhigh)
    
    # defuzzification
    defuzzified  = fuzz.defuzz(y_durability, output_durability, 'centroid')
    result = fuzz.interp_membership(y_durability, output_durability, defuzzified)


    # display situation
    Ax0_situation_dict= events_situation(dict(
        Good_events=Ax0_fit_good_events,
        Raining_events=Ax0_fit_bad_events_raining,
        Dirty_events=Ax0_fit_bad_events_dirtyAX,
        Bad_events=Ax0_fit_bad_events
        ))

    Ax1_situation_dict= events_situation(dict(
        Good_events=Ax1_fit_good_events,
        Raining_events=Ax1_fit_bad_events_raining,
        Dirty_events=Ax1_fit_bad_events_dirtyAX,
        Bad_events=Ax1_fit_bad_events
        ))

    output_layer_situation_dict= events_situation(dict(
        Durability_verylow=max(output_durability_verylow),
        Durability_low=max(output_durability_low),
        Durability_mid=max(output_durability_mid),
        Durability_high=max(output_durability_high),
        Durability_veryhigh=max(output_durability_veryhigh),
        ))

    textstr = '\n'.join((
        "Axle_sensors_durability=%.2f%%" % (defuzzified, ),
        "  Ax0 situation=%s%%" % (Ax0_situation_dict, ),
        "  Ax1 situation=%s%%" % (Ax1_situation_dict, ),
        "  output situation=%s%%" % (output_layer_situation_dict, )))

    fig, ax0 = plt.subplots(figsize=(15, 8))
    ax0.plot(y_durability, durability_verylow, 'r', linewidth = 0.5, linestyle = '--', label = 'verylow')
    ax0.plot(y_durability, durability_low, 'g', linewidth = 0.5, linestyle = '--', label = 'low')
    ax0.plot(y_durability, durability_mid, 'b', linewidth = 0.5, linestyle = '--', label = 'mid')
    ax0.plot(y_durability, durability_high, 'y', linewidth = 0.5, linestyle = '--', label = 'high')
    ax0.plot(y_durability, durability_veryhigh, 'm', linewidth = 0.5, linestyle = '--', label = 'veryhigh')
    ax0.fill_between(y_durability, output_durability0, output_durability, facecolor = 'Orange', alpha = 0.7)
    ax0.plot([defuzzified , defuzzified], [0, result], 'k', linewidth = 1.5, alpha = 0.9)
    ax0.legend()
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax0.text(0.05 , 0.45, textstr, transform=ax0.transAxes, bbox=props)
    ax0.set_title('centroid deffuzification sensor durability')
    ax0.set_xticks(np.arange(0, 109, step=10))
    plt.tight_layout()
    plt.show()

    return [defuzzified, Ax0_situation_dict, Ax1_situation_dict, output_layer_situation_dict]

fuzzy_inference_sys(500,500)