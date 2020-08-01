import control as ctl
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
from step import convert_to_array

def bode_diagram(num,den):

    num = list(convert_to_array(num))
    den = list(convert_to_array(den))

    sys = ctl.tf(num,den)

    fig, mag, phase, omega = ctl.bode_plot(sys, color = 'green')

    plugins.connect(fig, plugins.MousePosition(fontsize=14))
    figure_html = mpld3.fig_to_html(fig)

    return figure_html, sys