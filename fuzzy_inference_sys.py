import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
import matplotlib.pyplot as plt


def fuzzy_inference_sys(Ax0_peak_densty: float, Ax1_peak_densty: float):
    x_peak_densty = np.arange(-10, 2001, 1)
    y_risk = np.arange(0, 201, 1)

    # member ship func
    bad_events = mf.trapmf(x_peak_densty,[-10,-10,-2,-1])
    good_events = mf.pimf(x_peak_densty,-1,0,20,30)
    bad_events_raining = mf.pimf(x_peak_densty,20,90,510,1653)
    bad_events_dirtyAX = mf.smf(x_peak_densty,193,530)

    # fuzzificaton

    Ax0_fit_good_events, Ax1_fit_good_events = fuzz.interp_membership(x_peak_densty, good_events, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, good_events, Ax1_peak_densty)
    Ax0_fit_bad_events_raining, Ax1_fit_bad_events_raining = fuzz.interp_membership(x_peak_densty, bad_events_raining, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, bad_events_raining, Ax1_peak_densty)
    Ax0_fit_bad_events_dirtyAX, Ax1_fit_bad_events_dirtyAX = fuzz.interp_membership(x_peak_densty, bad_events_dirtyAX, Ax0_peak_densty), fuzz.interp_membership(x_peak_densty, bad_events_dirtyAX, Ax1_peak_densty)




    fig, ax0 = plt.subplots(nrows = 1, figsize =(10, 25))

    ax0.plot(x_peak_densty, bad_events, 'g', linewidth = 2, label = 'bad_events')
    ax0.plot(x_peak_densty, good_events, 'r', linewidth = 2, label = 'good_events')
    ax0.plot(x_peak_densty, bad_events_raining, 'g', linewidth = 2, label = 'bad_events_raining')
    ax0.plot(x_peak_densty, bad_events_dirtyAX, 'b', linewidth = 2, label = 'bad_events_dirtyAX')
    ax0.set_title('age')
    ax0.legend()
    plt.tight_layout()
    plt.show()

    # rules


fuzzy_inference_sys(-1,-1)