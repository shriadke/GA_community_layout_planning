from random import randint
import numpy as np
import os
import math
import sys
#import pandas as pd
import matplotlib.pyplot as pyplot

#Setting working directory to location of input file
#os.chdir('/Users/hemanth/Desktop/MSAI/Artificial Intelligence CSCI 6550/Project/')
sys.setrecursionlimit(50000)

#########################################################################################################################
#Functions for Population generation
#########################################################################################################################

#Function to check if any unit exists in the assignment location
def unit_exists(unitSizeX,unitSizeY):
    unitArray = []
    for i in range(0,unitSizeX):
        for j in range(0,unitSizeY):
            unitArray.append(f'grid[x+{i}][y+{j}] != 0')
    return f' or '.join(unitArray)

#Function to assign a unit
def unit_assign(unitSizeX,unitSizeY,unitCode):
    unitArray = []
    for i in range(0,unitSizeX):
        for j in range(0,unitSizeY):
            unitArray.append(f'grid[x+{i}][y+{j}]')
    assigned = (f' = '.join(unitArray)) + f'= {unitCode}'
    return assigned

#Function to randomly assign a unit
def place_randomly(gridSizeX,gridSizeY,unitSizeX,unitSizeY,unitCode,startPoints):
       x = randint(0, gridSizeX - unitSizeX - 1)
       y = randint(0, gridSizeY - unitSizeY - 1)
       #print(x,y)
       if(eval(unit_exists(unitSizeX,unitSizeY))):
           place_randomly(gridSizeX,gridSizeY,unitSizeX,unitSizeY,unitCode,startPoints)
       else:
           exec(unit_assign(unitSizeX,unitSizeY,unitCode))
           startPoints.append((x,y))
       return

#########################################################################################################################
#Population Generation
#########################################################################################################################

grids = []
gridSizeX = 25
gridSizeY = 25
startsList = []
#{"houses","coffice","club","play","clinic","school","market"}

for i in range(100):
    
    print("Generating population number ",i)
    #Making a Grid
    grid = np.zeros((gridSizeY,gridSizeX),dtype = int)
    
    #Placing 1 Gate. Gate has unitSize 2 and unitCode 
    #Gate is fixed
    grid[gridSizeX-1][int(math.ceil(gridSizeY/2))] = grid[gridSizeX-1][int(math.ceil(gridSizeY/2))+1] = 7
    
    #Placing 20 houses. Houses has unitSize 4 and unitCode 1
    housesStart = []
    for i in range(20):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 2,unitSizeY = 2,unitCode = 1,startPoints = housesStart)
    
    #Placing 1 Community office. Community office has unitSize 4 and unitCode 4
    cofficeStart = []
    for i in range(1):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 2,unitSizeY = 2,unitCode = 4,startPoints = cofficeStart)
    
    #Placing 1 Club House. Club House has unitSize 16 and unitCode 6
    clubStart = []
    for i in range(1):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 6,startPoints = clubStart)
      
    #Placing 2 Playgrounds. Playground has unitSize 16 and unitCode 5
    playStart = []
    for i in range(2):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 5,startPoints = playStart)
        
    #Placing 1 Clinic. Clinic has unitSize 16 and unitCode 3
    clinicStart = []
    for i in range(1):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 3,startPoints = clinicStart)
    
    #Placing 1 School. School has unitSize 25 and unitCode 9
    schoolStart = []
    for i in range(1):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 5,unitSizeY = 5,unitCode = 9,startPoints = schoolStart)
    
    #Placing 1 Market. Market has unitSize 25 and unitCode 8
    marketStart = []
    for i in range(1):
        place_randomly(gridSizeX,gridSizeY,unitSizeX = 5,unitSizeY = 5,unitCode = 8,startPoints = marketStart)
    
    startsList.append({"houses":housesStart,"coffice":cofficeStart,"club":clubStart,"play":playStart,"clinic":clinicStart,"school":schoolStart,"market":marketStart})
    #2 for grass
    #0 for road
        
    #Placing roads for all empty grids spaces
    #for i in range(gridSizeX):
    #    for j in range(gridSizeY):
    #        if(grid[i][j] == 0):
    #            grid[i][j] = 7
    ##Converting grid into a dataframe
    #df = pd.DataFrame (grid) 
    #
    ##Save to xlsx file
    #df.to_excel('gridsample.xlsx', index=False)

    #fig,axis = pyplot.subplots()
    #axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    #Randomly changing some roads to grass with probabilty of 0.40
    for i in range(gridSizeX):
        for j in range(gridSizeY):
            if(grid[i][j] == 0):
#               if(np.random.choice(2,1,p =[0.4,0.6])[0] == 0):
                grid[i][j] = 2
                    
    grids.append(grid)           

np.save('populationGrids.npy',grids)
np.save('startsList.npy',startsList)