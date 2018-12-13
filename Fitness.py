# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:26:29 2018

@author: shrin
"""
import numpy as np
import math
from AStar import *
import time

# calculates distance from start point to goal point using A*
def calc_dist(start, goal, grid):
   # print(start, goal)
    path=[]
    grid1=np.zeros((25,25),dtype=object)
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid1[x][y] = Node(str(grid[x][y]),(x,y))
    #print(grid1[start[0]][start[1]], grid1[goal[0]][goal[1]])
    path=aStar(grid1[start[0]][start[1]], grid1[goal[0]][goal[1]], grid1, fromWay = 'road')
    if len(path) == 0:
        return 100000
    else :
        dist = 0    
        for node in path:
           x,y=node.point
           if (x == 24 and y == 13) or (x == 24 and y == 14):
               continue
           else:
               dist = dist + 1
    return dist

# calculates path cost from list of start points to list of goal points
def calc_path_cost(start_points, goal_points, grid):
    path_cost = 0
    for i in range(len(start_points)):
        for j in range(len(goal_points)):
                path_cost = path_cost + calc_dist((start_points[i])[1], (goal_points[j])[1], grid)
    return path_cost 

# calculate 
def calc_dist_house_to_gate(grid, startList):
    start_points = []
    for points in startList['houses']:
        start_points.append(points)
    goal_points = [((24,13),(24,13))]  
    return calc_path_cost(start_points=start_points, goal_points=goal_points, grid= grid)

def calc_dist_house_to_other_build(grid, startList):
    start_points = []
    goal_points = []
    for points in startList['houses']:
        start_points.append(points)
    for key, value in startList.items():
        if key != 'houses' :
            goal_points.extend(value)
    return calc_path_cost(start_points=start_points, goal_points=goal_points, grid= grid)

def calc_dist_house_to_house(grid, startList):
    start_points = []
    goal_points = []
    for points in startList['houses']:
        start_points.append(points)
    for points in startList['houses']:
        goal_points.append(points)
    return calc_path_cost(start_points=start_points, goal_points=goal_points, grid= grid)


def calc_dist_coffice_gate(grid,startList):
    start_points = []
    for points in startList['coffice']:
        start_points.append(points)
    goal_points = [((24,13),(24,13))]  
    return calc_path_cost(start_points=start_points, goal_points=goal_points, grid= grid)

"""
This function will calculate the percentage of green blocks present in grid
input: 
returns:
"""
def calc_greenery_percent(grid):
    return (np.count_nonzero(grid == 2))/np.prod(grid.shape)

#Function to check count of a particular unitCode in the entire grid
def valueCounts(grid,unitCode,gridSizeX,gridSizeY):
    counter = 0
    for x in range(gridSizeX):
        for y in range(gridSizeY):
            if(grid[x][y] == unitCode):
                counter = counter + 1
    return counter
        
#Function to check if the total counts of buildings match to the required count according to initial design
def unitsCheck(grid,gridSizeX,gridSizeY):
    Count7 = valueCounts(grid,7,gridSizeX,gridSizeY)
    Count1 = valueCounts(grid,1,gridSizeX,gridSizeY)
    Count4 = valueCounts(grid,4,gridSizeX,gridSizeY)
    Count6 = valueCounts(grid,6,gridSizeX,gridSizeY)
    Count5 = valueCounts(grid,5,gridSizeX,gridSizeY)
    Count3 = valueCounts(grid,3,gridSizeX,gridSizeY)
    Count9 = valueCounts(grid,9,gridSizeX,gridSizeY)
    Count8 = valueCounts(grid,8,gridSizeX,gridSizeY)
    if(Count7 == 2 and Count1 == 80 and Count4 == 4 and Count6 == 16 and Count5 == 32 and Count3 == 16 and Count9 == 25 and Count8 == 25):
        return True
    else:
        return False

#Function to output the check condition for intact check
def unit_intact_check_condition(unitSizeX,unitSizeY,unitCode):
    unitArray = []
    for i in range(0,unitSizeX):
        for j in range(0,unitSizeY):
            unitArray.append(f'grid[x+{i}][y+{j}]')
    assigned = (f' == '.join(unitArray)) + f' == {unitCode}'
    return assigned

#Function to check if a given  unit is intact
def units_intact_check(grid,startsListUnit,unitSizeX,unitSizeY,unitCode):
    number = len(startsListUnit)
    counter = 0
    for n in startsListUnit:
        x = n[0][0]
        y = n[0][1]
        if(eval(unit_intact_check_condition(unitSizeX,unitSizeY,unitCode))):
            counter = counter + 1
    if counter == number:
        return True
    else:
        return False

#Function to check if all units are intact
def unitsIntact(grid,startsList,gridSizeX,gridSizeY):
    houseCheck = units_intact_check(grid,startsList['houses'],unitSizeX = 2,unitSizeY = 2,unitCode = 1)
    cofficeCheck = units_intact_check(grid,startsList['coffice'],unitSizeX = 2,unitSizeY = 2,unitCode = 4)
    clubCheck = units_intact_check(grid,startsList['club'],unitSizeX = 4,unitSizeY = 4,unitCode = 6)
    playCheck = units_intact_check(grid,startsList['play'],unitSizeX = 4,unitSizeY = 4,unitCode = 5)
    clinicCheck = units_intact_check(grid,startsList['clinic'],unitSizeX = 4,unitSizeY = 4,unitCode = 3)
    schoolCheck = units_intact_check(grid,startsList['school'],unitSizeX = 5,unitSizeY = 5,unitCode = 9)
    marketCheck = units_intact_check(grid,startsList['market'],unitSizeX = 5,unitSizeY = 5,unitCode = 8)
    gateCheck = True if(grid[gridSizeX-1][int(math.ceil(gridSizeY/2))] == grid[gridSizeX-1][int(math.ceil(gridSizeY/2))+1] == 7) else False
    if(houseCheck == True and cofficeCheck == True and clubCheck == True and playCheck == True and clinicCheck == True and schoolCheck == True and marketCheck == True and gateCheck == True):
        return True
    else:
        return False

def surround(point,size,grid):
    x=point[0]
    y=point[1]
    if 0<x<24 and 0<y<24:
        count = 0
        for a in range((x-1),x+size+1): 
            for b in range(y-1,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
        if (count==4*(size+1)):
            return 1
    elif x==0 and y==0:
        count = 0
        for a in range((x),x+size+1): 
            for b in range(y,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
        if (count==(2*(size+1)-1)):
            return 1
    elif x==0 and 0<y<24:
        count = 0
        for a in range((x),x+size+1): 
            for b in range(y-1,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
               
        if (count==(3*(size+1)-1)):
            return 1
    elif 0<x<24 and y==0:
        count = 0
        for a in range((x-1),x+size+1): 
            for b in range(y,y+size+1):
                if(x<=a<=x+size-1  and y<=b<=y+size-1) :
                    continue
                else:       
                    if (grid[a][b]==2 or grid[a][b]==0):
                        count=count+1
        if (count==(3*(size+1)-1)):
            return 1
    return 0

def check_surroundings(grid, startList):
    houses=[startList.get('houses'),2,1]
    coffice=[startList.get('coffice'),2,4]
    club=[startList.get('club'),4,6]
    play=[startList.get('play'),4,5]
    clinic=[startList.get('clinic'),4,3]
    school=[startList.get('school'),5,9]
    market=[startList.get('market'),5,8]
    A=[]
    A.append(surround(coffice[0][0][0], coffice[1],grid))
    for i in range(2):
        b=surround(play[0][i][0], play[1], grid)
        A.append(b)
    A.append(surround(club[0][0][0],club[1],grid))
    A.append(surround(school[0][0][0],school[1],grid))
    for i in range(20):
        b=surround(houses[0][i][0],houses[1],grid)
        A.append(b)
    
    A.append(surround(clinic[0][0][0],clinic[1],grid))
    A.append(surround(market[0][0][0],market[1],grid))
    precision = sum(A)/len(A)
        
    return precision

def calculate_fitness(grid, startList):
    fitness = 0
    gridSizeX = 25
    gridSizeY = 25
    percent_greenery = calc_greenery_percent(grid = grid)
    #print(percent_greenery)
    house_gate_cost = calc_dist_house_to_gate(grid, startList) 
    coffice_gate_cost = calc_dist_coffice_gate(grid, startList)
    house_other_build_cost = calc_dist_house_to_other_build(grid, startList)
    #all_path_costs = house_gate_cost + coffice_gate_cost + house_other_build_cost
    units_intact = int(unitsIntact(grid,startList,gridSizeX,gridSizeY))
    units_check = int(unitsCheck(grid,gridSizeX,gridSizeY))
    #print("units_intact", units_intact)
    #print("units_check", units_check)
    surround_precision = check_surroundings(grid, startList)
    #print(surround_precision)
    
    fitness = 2*percent_greenery + 3*(units_check + units_intact + surround_precision) \
            + (1 / house_gate_cost) + (2 / house_other_build_cost) + (2 / coffice_gate_cost)
    #print(fitness)
    return fitness

#fitness = []
#X=np.load("populationGridsUpdt.npy")
#start_exit_dict = np.load("start_exit_dict.npy")
#grid=X[0,:,:]
#startList = start_exit_dict[0]
#
#fitness.append(calculate_fitness(grid=grid, startList=startList))
#end = time.time()
#print(end - start)