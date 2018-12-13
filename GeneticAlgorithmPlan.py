# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 03:02:23 2018

@author: shrin
"""
import numpy as np
from LayRoad import *
from Fitness import *
from random import randint
import copy

#Function to check if any unit exists in the assignment location
def unit_position_check(unitSizeX,unitSizeY,unitCode):
    unitArray = []
    for i in range(0,unitSizeX):
        for j in range(0,unitSizeY):
            if(i == 0 and j == 0):
                unitArray.append(f'grid[x][y] == {unitCode}')
            else:
                unitArray.append(f'grid[x+{i}][y+{j}] == 2')
    return f' and '.join(unitArray)

#Function to assign a unit
def unit_assign_upsample(unitSizeX,unitSizeY,unitCode):
    unitArray = []
    for i in range(0,unitSizeX):
        for j in range(0,unitSizeY):
            unitArray.append(f'grid[x+{i}][y+{j}]')
    assigned = (f' = '.join(unitArray)) + f'= {unitCode}'
    return assigned

#Function to upsample a grid
def place_upsample(grid,gridSizeX,gridSizeY,unitSizeX,unitSizeY,unitCode,startPoints):
    for x in range(gridSizeX):
        for y in range(gridSizeY):
            if grid[x][y] == unitCode:
                startPoints.append((x,y))
    
    for x,y in startPoints:
        if(eval(unit_position_check(unitSizeX,unitSizeY,unitCode))):
            exec(unit_assign_upsample(unitSizeX,unitSizeY,unitCode))
        else:
            print("Grid not possible")
    return

def upscale(grid,gridSizeX,gridSizeY):    
    housesStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 2,unitSizeY = 2,unitCode = 1,startPoints = housesStart)
          
    cofficeStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 2,unitSizeY = 2,unitCode = 4,startPoints = cofficeStart)
         
    clubStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 6,startPoints = clubStart)
           
    playStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 5,startPoints = playStart)
                
    clinicStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 4,unitSizeY = 4,unitCode = 3,startPoints = clinicStart)   
        
    schoolStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 5,unitSizeY = 5,unitCode = 9,startPoints = schoolStart)
        
    marketStart = []
    place_upsample(grid,gridSizeX,gridSizeY,unitSizeX = 5,unitSizeY = 5,unitCode = 8,startPoints = marketStart)
        
     
    startsList = {"houses":housesStart,"coffice":cofficeStart,"club":clubStart,"play":playStart,"clinic":clinicStart,"school":schoolStart,"market":marketStart}

    return(startsList)
def crossover(a,b):
    for i in range(randint(5,8)):
        x=randint(0,24)
        y=randint(0,24)
        temp=a[x][y]
        temp1=b[x][y]
        a[x][y]=temp1
        b[x][y]=temp
        i=i+1

    return a,b

def change(point,value,grid1):
    a=point[0]
    b=point[1]
    grid1[a][b]=value
    return grid1

def genetic_algorithm(grids, start_exit_dict):
    #Calculate fitness of all grids
    fitness_list = []
    for i in range(grids.shape[0]):
        grid=grids[i,:,:]
        startList = start_exit_dict[i]
        fitness_list.append((i, calculate_fitness(grid, startList)))
    
    fitness_list = sorted(fitness_list, key=lambda x:-x[1])
    
    # get the best 
    best_fit = fitness_list[:20]
    best_grids = np.empty((0,25,25), dtype=int)
    best_start_exit_dict = []
    for best in best_fit:
        best_grids = np.append(best_grids, [grids[best[0],:,:]], axis = 0)
        best_start_exit_dict.append(start_exit_dict[best[0]])
#    np.save("best_fit20.npy", best_grids)
 #   np.save("best_fit_start.npy", best_start_exit_dict)
    # Ready for crossover
    #Do crossover here 
    # Pool the data
    for a in range(len(best_start_exit_dict)):
        houses=[best_start_exit_dict[a].get('houses'),2,1]
        coffice=[best_start_exit_dict[a].get('coffice'),2,4]
        club=[best_start_exit_dict[a].get('club'),4,6]
        play=[best_start_exit_dict[a].get('play'),4,5]
        clinic=[best_start_exit_dict[a].get('clinic'),4,3]
        school=[best_start_exit_dict[a].get('school'),5,9]
        market=[best_start_exit_dict[a].get('market'),5,8]
    A=np.empty((0,25,25), dtype=int)
    for i in range(20):
        grid1=np.full((25,25),2, dtype=int)
        #grid1[24][13]= 7
        #grid1[24][14] = 7
        # PLEASE DEAL WITH HARD_CODED RANGES OF HOUSES, BUILDINGS 
        for i in range(20):
            b=change(houses[0][i][0],houses[2],grid1 )
        for i in range(2):
            b=change(play[0][i][0], play[2], grid1)
        b=change(coffice[0][0][0], coffice[2],grid1)
        b=change(school[0][0][0],school[2],grid1)
        b=change(market[0][0][0],market[2],grid1)
        b=change(clinic[0][0][0],clinic[2],grid1)
        b=change(club[0][0][0],club[2],grid1)  
        A=np.append(A,[b],axis=0)
    #Got the pooled data
    best_grids = copy.deepcopy(A)
    offspring=np.empty((0,25,25), dtype=int)
    for i in range(10):
        for j in range(10,20):
            new_a,new_b=crossover(best_grids[i,:,:],best_grids[j,:,:])
        offspring=np.append(offspring,[new_a],axis=0)
        offspring=np.append(offspring,[new_b],axis=0)
    #print(offspring.shape)
    #Got the offsprings of crossover   

    # this gridmin.py should be final 20 max pooled grids after crossover
    gridsMin = offspring #np.load('min.npy')
    gridSizeX = 25
    gridSizeY = 25
    
    #these are the two new lists for 20 grids
    startsListMin = []
    gridsMinUp = []
       
    for gridID in range(len(gridsMin)):
        grid = gridsMin[1]
        grid = gridsMin[gridID]
        startsListMin.append(upscale(grid,gridSizeX,gridSizeY))
        gridsMinUp.append(grid)

    #build roads for these 20 and then add these to population worst 20.
    for i in range(len(gridsMinUp)):
        grid=gridsMinUp[i]
        startList = startsListMin[i]
        gridsMinUp[i], startsListMin[i] = get_all_roads(grid, startList=startList)    
    
    #Replace new 20 members with lowest fit 20
    worst_fit = fitness_list[80:]
    for i in range(20) :
        grids[worst_fit[i][0]] =  gridsMinUp[i]
        start_exit_dict[worst_fit[i][0]] = startsListMin[i]
  
    return grids, start_exit_dict
    
    
#Initial pops
grids=np.load("populationGrids.npy")
start_exit_dict = np.load("startsList.npy")
#Lay roads on initial population
for i in range(grids.shape[0]):
    grid=grids[i,:,:]
    startList = start_exit_dict[i]
    grids[i,:,:], start_exit_dict[i] = get_all_roads(grid, startList=startList)
#print(grids)
#print(start_exit_dict)
# call genetic algorithm
for i in range(50):
    print("Running Iteration : ", i+1)
    grids, start_exit_dict = genetic_algorithm(grids, start_exit_dict)
    print("After One Iteration Following is the best grid")
    fitness_list = []
    for i in range(grids.shape[0]):
        grid=grids[i,:,:]
        startList = start_exit_dict[i]
        fitness_list.append((i, calculate_fitness(grid, startList)))
    
    fitness_list = sorted(fitness_list, key=lambda x:-x[1])
    
    # get the best 
    best_fit = fitness_list[0]
    print(best_fit)
    fig,axis = pyplot.subplots()
    axis.matshow(grids[best_fit[0]], cmap=pyplot.cm.tab10)