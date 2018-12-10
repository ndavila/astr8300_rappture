import sys
import Rappture
import numpy as np
from scipy.integrate import odeint
from scipy import optimize
from math import *

def f(m, t, formula):
    return eval(formula)

def calc(t, a, formula):
    m = odeint(f, -a, [0,t], args=(formula,))
    return m[1]  # y[0] is int m(t) from 0 to 0

def g(t, formula):
    return eval(formula)

def model(y, t, formula):
    return eval(formula)

def main():

    # Load library--create object

    io = Rappture.library(sys.argv[1])

    # Get input

    tmin = float(io.get('input.number(min).current'))
    tmax = float(io.get('input.number(max).current'))
    a = float(io.get('input.number(a).current'))
    y0 = float(io.get('input.number(Y0).current'))
    npts = int(io.get('input.number(Npts).current'))
    formula = io.get('input.string(formula).current')

    t = np.linspace(tmin, tmax, npts)
    sol = odeint(model, y0, t, args=(formula,))

    io.put('output.curve(result2).about.label','dM(t)/dt vs t',append=0)
    io.put('output.curve(result2).yaxis.label','dM(t)/dt')
    io.put('output.curve(result2).xaxis.label','t')

    io.put('output.curve(result3).about.label','Integral of M(t) vs t',append=0)
    io.put('output.curve(result3).yaxis.label','Integral of M(t)')
    io.put('output.curve(result3).xaxis.label','t')

    for i in range(npts):
        io.put(
                'output.curve(result2).component.xy',
                '%g %g\n' % (t[i],g(t[i],formula)), append=1
              )
        io.put(
                'output.curve(result3).component.xy',
                '%g %g\n' % (t[i],sol[i][0]), append=1
              )

    # Get base string

    my_str_base = 'int_0^root (' + formula + ') dt - ' + str(a)

    # Compute root of \int_0^x f(t') dt' - a

    root = optimize.brentq(calc, tmin, tmax, args=(a, formula))

    my_str = '\nRoot of ' + my_str_base +  ' in [' + str(tmin) + \
            ', ' + str(tmax) + '] is ' + str(root)

    io.put('output.string(result1).about.label', 'Root')
    io.put('output.string(result1).current', my_str)

    # Check

    check = calc(root, a, formula)

    my_str2 = '\nCheck: ' + my_str_base + ' = ' + str(check[0])

    io.put('output.string(result2).about.label', 'Diagnostic')
    io.put('output.string(result2).current', my_str2)

    # Output results

    Rappture.result(io)


if __name__ == "__main__":
    main()
