# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def analyticalSolution(H, cv, uo, T_range, drainage='tb'):
  '''
  Parameters:
    :param H: Height of 1D model.
    :param cv: Coefficient of consolidation.
    :param uo: Initial excess pore pressure.
    :param T_range: Dimensionless time range, list [T1,T2]. 
    :param drainage: Boundary drainage condition.
      'tb' - Drained top and bottom boundaries.
      't'  - Drained top boundary.
      'b'  - Drained bottom boundary.
  Returns:
    data1: Height versus pore pressure data for a given time range.
    data2: Degree of consolidation versus time data
  '''
  # T range from linear exponent range in dcc.RangeSlider
  T = np.linspace(10**T_range[0], 10**T_range[1], 10)
  
  # Convert linear exponent from dcc.Slider
  cv = 10**cv
  
  N = 50  # Discretization
  u = np.zeros((len(T),N))

  if drainage == 'tb':
    h = H/2.0
    z = np.linspace(-h, h, N)
    u[:,0] = 0.0
    u[:,-1] = 0.0
    z_start = 1
    z_end = len(z) - 1
    h = H/2.0
  elif drainage == 't':
    h = H
    z = np.linspace(0, h, N)
    u[:,-1] = 0.0
    z_start = 0
    z_end = len(z) - 1
  else:
    h = H
    z = np.linspace(-h, 0, N)
    u[:,0] = 0.0
    z_start = 1
    z_end = len(z)   

  # Initial condition just after BCs are applied, at t > 0
  u[:,z_start:z_end] = uo  

  # Positive H range for plotting, len(y) = len(z)
  y = np.linspace(0, H, N)    

  data1 = []
  term1 = np.pi * z[z_start:z_end] / (2*h)  
  for i in range(len(T)):
    trace1 = {}
    term2 = (np.pi/2)**2 * T[i]
    sum1 = 0      
    for k in range(1,100):     
      factor = ((-1.0)**(k-1) / (2*k-1))
      sum1 += factor * np.cos((2*k-1) * term1) * np.exp(-1.0 * (2*k-1)**2 * term2)
    u[i,z_start:z_end] = uo * 4.0/np.pi * sum1
    #plt.plot(u[i,:], y)
    trace1['x'] = u[i,:]
    trace1['y'] = y
    trace1['name'] = 'T = ' + str(T[i])        
    data1.append(trace1)   
  
  
  #plt.show()
  Tu = np.linspace(10**T_range[0], 10**T_range[1], 1000)

  # Real time in days (1 cm2/s = 8.64 m2/day)
  t = np.array([i*h**2/(cv * 8.64) for i in Tu]) 
  
  trace2, trace3 = {}, {}
  sum2 = np.zeros(len(Tu))
  for k in range(1,100):
    factor2 = 1.0 / (2*k - 1)**2
    sum2 += factor2 * np.exp(-1.0 * (2*k-1)**2 * (np.pi/2)**2 * Tu)
  sum2 = 1 - (8/np.pi**2) * sum2
  sum2 *= 100
  trace2['x'] = Tu
  trace2['y'] = sum2
  trace2['name'] = ''
  trace3['x'] = t
  trace3['y'] = sum2,
  trace3['name'] = ''
  trace3['xaxis'] = 'x2'
  data2 = [trace2, trace3]
  #plt.semilogx(t, sum2)
  #plt.show()

  return data1, data2
 
#data = analyticalSolution(1, 1.2e-6, 50, [-2,0], 'tb')
#print(data)

      



