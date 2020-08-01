import control as ctl
from control.matlab import step
from bokeh.plotting import show, figure
from bokeh.embed import components


def step_plot(numC, denC, numT, denT):

    # Controller C(s) - Transfer Function
    sysC = ctl.tf(numC,denC)

    # System T(s) - Transfer Function
    sysT = ctl.tf(numT, denT)

    sys = ctl.series(sysC,sysT)

    Y, t = ctl.matlab.step(sys)

    p = figure(plot_width=700, plot_height=500, x_axis_label = 'Time(s)',y_axis_label = 'Amplitude', sizing_mode = "scale_width")
    p.circle(t,Y,size=5, color="green", alpha=0.5)
    plot = {'plot': p}

    script, divs = components(plot)

    return script, divs, sysC, sysT, sys

def convert_to_array(i):
    _temp = i.split()
    tempn = []
    for n in _temp:
        tempn.append(float(n))
    return list(tempn)
