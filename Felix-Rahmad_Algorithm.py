import numpy as np
import random
import pandas as pd

def FelixRahmadOptimizer(method, start, stop, function= lambda x: x**2, isminimize=True, variable= 2, candidate= 10, iteration = 10, *args):
    x=[]
    y=[]
    
    ismaximize = False
    if isminimize == False:
        ismaximize = True

    for i in range(variable):
        temp_x=[]
        temp_y=[]
        for j in range(candidate):
            temp_x.append(np.round(random.uniform(start,stop),2))
            temp_y.append(np.round(function(temp_x[j]),2))
        x.append(temp_x)
        y.append(temp_y)
    
    x= np.array(x)
    y= np.array(y)
    y= y.sum(axis=0)

    for a in range(iteration):
        x_new= x.copy()
        #find index of best and worst result
        if isminimize == True:
            best_index = y.argmin()
            worst_index = y.argmax()
        if ismaximize == True:
            best_index = y.argmax()
            worst_index = y.argmin()
        
        #generate new values
        #3 methods available
        #method 1
        if method == 1:        
            for i,j in enumerate(x_new):
                for k in range(len(j)):
                    r = np.round(random.random(),3)
                    x_new[i,k] += np.round(r*(x_new[i,best_index] - x_new[i,worst_index]),2)
            y_new= np.round(function(x_new),3)
            y_new= y_new.sum(axis=0)
        
        if method == 2:
            for i,j in enumerate(x_new):
                for k in range(len(j)):
                    l = int(np.round(random.uniform(0, candidate-1),0))
                    #compare candidate vs candidate from random index
                    if y[k] > y[l]:
                        multiplier = 1
                    if y[k] < y[l]:
                        multiplier = -1
                    #calculating new candidates
                    r1= np.round(random.random(),3)
                    r2= np.round(random.random(),3)
                    x_new[i,k] += r1*(x_new[i, best_index] - x_new[i,worst_index]) + r2*multiplier*(abs(x_new[i, best_index]) - abs(x_new[i,l]))
            y_new= np.round(function(x_new),3)
            y_new= y_new.sum(axis=0)
        
        if method == 3:
            for i, j in enumerate(x_new):
                for k in range(len(j)):
                    l = int(np.round(random.uniform(0, candidate-1),0))
                    #compare candidate vs candidate from random index
                    if y[k] > y[l]:
                        x_better = x_new[i,k]
                        x_worse = x_new[i,l]
                    if y[k] < y[l]:
                        x_better = x_new[i,l]
                        x_worse = x_new[i,k]
                        
                    #calculating new candidates
                    r1= np.round(random.random(),3)
                    r2= np.round(random.random(),3)
                    x_new[i,k] += r1*(x_new[i, best_index] - abs(x_new[i, worst_index])) + r2*(abs(x_better) - x_worse)
            y_new = np.round(function(x_new),3)
            y_new = y_new.sum(axis=0)
        
        #compare f(x) with previous f(x). keep if  f(x) is lower
        if isminimize == True:
            iskeep = y_new > y
        if ismaximize == True:
            iskeep = y_new < y
            
        for index, elements in enumerate(x):
            for inner_index in range(len(x)):
                if iskeep[inner_index] == False:
                    x[index, inner_index]= x_new[index,inner_index]
                    
        if isminimize == True:            
            y = np.fmin(y,y_new)
        if ismaximize == True:
            y = np.fmax(y,y_new)
    
    if isminimize == True:
        best_index = y.argmin()
        worst_index = y.argmax()
    if ismaximize == True:
        best_index = y.argmax()
        worst_index = y.argmin()

    status=[]
    for index in range(candidate):
        status.append('-')

    status[best_index]= 'Best'
    status[worst_index]= 'Worst'

    columns = variable
    col_name=[]
    for column in range(variable):
        col_name.append(f'x{column+1}')
        
    col_name.append('f(x)')
    col_name.append('status')
    result_df = pd.DataFrame(list(zip(*x,y,status)), columns =col_name)

    return result_df

# for testing purposes
# print(FelixRahmadOptimizer(1, -50, 50))
# print(FelixRahmadOptimizer(2, -50, 50, function=lambda x: 100*x+2*x**2, isminimize=False))
