from flask import Flask, flash, jsonify, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import os
import mpld3
from mpld3 import plugins
import control as ctl
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
from step import step_plot, convert_to_array
from bode import bode_diagram
from complex_converter import rect2pol, pol2rect

# Observations

#The function root locus and bode has changed to return the variable 'f' (figure) besides the default function return
# The function root locus has changed in line 512 to be forced to plot in color green.

# Configure application

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/info")
def info ():
    if request.method == "GET":
        return render_template('info.html')

@app.route("/contact")
def contact ():
    return render_template('contact.html')

@app.route("/",methods=["GET","POST"])
def index ():
    if request.method == "POST":

        select = str(request.form.get("select"))

        if (select == "Root Locus"):
            return render_template("rlocus.html")
        elif (select == "Bode Diagram"):
            return render_template("bode.html")
        elif (select == "Routh–Hurwitz"):
            return render_template("routh-hurwitz.html")
        elif (select == "Complex Converter"):
            return render_template("complex-converter.html")
        elif (select == "Step Response"):
            return render_template("step-response.html")
    else:
        return render_template("index.html")

@app.route("/rlocus", methods=["GET","POST"])
def rootlocus():

    if (request.method == "POST"):

        num = str(request.form.get("num"))
        den = str(request.form.get("den"))
        kmin = int(request.form.get("kmin"))
        kmax = int(request.form.get("kmax"))

        # Convert input numerator to a integer list
    num_temp = num.split()
    tempn = []

    for n in num_temp:
        tempn.append(float(n))
    num = tempn

    # Convert input denominator to a integer list

    den_temp = den.split()
    tempd = []
    for d in den_temp:
        tempd.append(float(d))

    den = tempd

    # Transfer Function
    sys = ctl.tf(num,den)
    print(sys)

    # Gain array
    K = np.arange(kmin,kmax,0.1)

    rlist, klist, f = ctl.root_locus(sys, kvect=K, xlim=0, ylim=0, plotstr=None, plot=True, print_gain=True, \
                grid=False, ax=None)

    xmax = 0
    ymax = 0
    xmin = 0
    ymin = 0
    for r in rlist:
        for c in r:
            if c.real > xmax:
                xmax = c.real
            if c.real < xmin:
                xmin = c.real
            if c.imag > ymax:
                ymax = c.imag
            if c.imag < ymin:
                ymin = c.imag
        plt.ylim(bottom = ymin - 10,top = ymax + 15)
        plt.xlim(left = xmin - 10, right = xmax + 15)

        plugins.connect(f, plugins.MousePosition(fontsize=14))
        figure_html = mpld3.fig_to_html(f)

        return render_template("rlocus-result.html", figure_html = figure_html, sys = sys, klist = klist , rlist = rlist, kmin = kmin, kmax = kmax)

    else:
        return render_template("rlocus.html")

@app.route("/step-response", methods=["GET","POST"])
def step_response():

    if (request.method == "POST"):
        numC = str(request.form.get("numC"))
        denC = str(request.form.get("denC"))
        numT = str(request.form.get("numT"))
        denT = str(request.form.get("denT"))

        numC = list(convert_to_array(numC))
        denC = list(convert_to_array(denC))
        numT = list(convert_to_array(numT))
        denT = list(convert_to_array(denT))

        script, divs, sysC, sysT, sys = step_plot(numC, denC, numT, denT)

        return render_template("step-response-result.html", script = script, divs = divs, sysC = sysC, sysT = sysT, sys = sys)

    else:

        return render_template("step-response.html")

@app.route("/complex-converter", methods=["GET","POST"])
def complex_converter():

    if (request.method == "POST"):
        converter = request.form.get("complex-conv")
        in1 = float(request.form.get("in1")) # rect2pol -> real / pol2rect - r
        in2 = float(request.form.get("in2")) # rect2pol -> imag / pol2rect - phi
        angle_unit = request.form.get("angle")

        print(converter)
        print(angle_unit)
        if angle_unit == '2':
            angle = True;
        else:
            angle = False;

        if converter == '1':
            z = rect2pol(in1,in2)
            conv = 'rect2pol'
        else:
            z = pol2rect(in1, in2, angle)
            conv = 'pol2rect'
        print(z)
        return render_template("complex-converter-result.html", z = z, conv = conv, in1 = in1, in2 = in2)
    else:
        return render_template('complex-converter.html')

@app.route("/bode", methods=["GET","POST"])
def bode():
    if (request.method == 'POST'):

        num = request.form.get('num')
        den = request.form.get('den')

        figure_html, sys = bode_diagram(num, den)

        return render_template('bode-plot.html', figure_html = figure_html, sys = sys)
    else:
        return render_template('bode.html')



