# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 22:42:48 2018

@author: shrin
"""

import numpy as np
from math import *
from AStar import *

global grid

def calc_eucl_dist(start_x, start_y, goal_x, goal_y):
    return sqrt((goal_x - start_x)**2 + (goal_y - start_y)**2)

def is_exit_possible(building_exit, grid):
    x = building_exit[0]
    y = building_exit[1]
    if 0<x<24 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)] ]
    elif x==0 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x,y + 1),(x+1,y)] ]
    elif x==0 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x,y - 1),(x,y + 1),(x+1,y)] ]
    elif x==24 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x,y - 1),(x,y + 1),(x - 1,y)] ]
    elif 0<x<24 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y + 1),(x+1,y)] ]
    elif 0<x<24 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y - 1),(x+1,y)] ]
    elif x==24 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y - 1)] ]
    elif x==0 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x + 1,y),(x,y - 1)] ]
    elif x==24 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y + 1)] ]
    
    if len([link for link in links if link != '%' and (link==0 or link==2 or link==7) ]) == 0:
        return False
    else:
        return True
def get_exit_point(main_x, main_y, unitSizeX, unitSizeY, grid, goal):
    #Check all possible exit points
    exit_points = []
    if is_exit_possible((main_x, main_y), grid) :
        exit_points.append([(main_x, main_y), calc_eucl_dist(main_x, main_y, goal[0], goal[1])])
    if is_exit_possible((main_x + (unitSizeX-1), main_y), grid) :
        exit_points.append([(main_x + (unitSizeX-1), main_y), calc_eucl_dist(main_x + (unitSizeX-1), main_y, goal[0], goal[1])])
    if is_exit_possible((main_x, main_y + (unitSizeX-1)), grid) :
        exit_points.append([(main_x, main_y + (unitSizeX-1)), calc_eucl_dist(main_x, main_y + (unitSizeX-1), goal[0], goal[1])])
    if is_exit_possible((main_x + (unitSizeX-1), main_y + (unitSizeX-1)), grid) :
        exit_points.append([(main_x + (unitSizeX-1), main_y + (unitSizeX-1)), calc_eucl_dist(main_x + (unitSizeX-1), main_y + (unitSizeX-1), goal[0], goal[1])])
#    # sort by dist to gate from all exit points
    return sorted(exit_points, key=lambda p:p[1])

def get_nearest_road(exit_x, exit_y, grid):
    roadPix = np.argwhere(grid == 0)
    min_dist = 100000
    if len(roadPix) == 0:
        return []
    for road in roadPix:
        dist = calc_eucl_dist(exit_x, exit_y, road[0], road[1])
        if dist < min_dist:
            road_x, road_y = road[0], road[1]
            min_dist = dist
    return [(road_x, road_y), min_dist]

def lay_path(exit_points, goal, building):
    global grid
    path_found = False
    for exit_point in exit_points:
           [start, goal_dist] = exit_point
           # Calculate the nearest road from exit point of a building
           road = get_nearest_road(start[0], start[1], grid)
           if len(road) != 0:
               road_exit, road_dist = road[0], road[1]
               # If the road is nearer than gate, Update it as goal.
               if road_dist < goal_dist:
                   goal = (road_exit[0], road_exit[1])
           # Lay the road to updated goal location
           path=[]
           grid1=np.zeros((25,25),dtype=object)
           for x in range(len(grid)):
               for y in range(len(grid[x])):
                    grid1[x][y] = Node(str(grid[x][y]),(x,y))
           path=aStar(grid1[start[0]][start[1]],grid1[goal[0]][goal[1]],grid1)
           if len(path) == 0:
               continue
           else :
               for node in path:
                    x,y=node.point
                    if (x == 24 and y == 13) or (x == 24 and y == 14):
                        break
                    elif ((x == start[0] and y == start[1])):
                        continue
                    else:
                        grid[x][y] = 0
               # Update house dict
               building = ((building[0], building[1]) , (path[1]).point)
               path_found = True
               break
    return path_found, building
   
def build_road_to_building(buildingStart, size):
    h_st_ex = []
    global grid
    for building in buildingStart:
       goal=(24,13)
       start_x, start_y = building[0], building[1]
       # Calculate exit point from building
       exit_points = get_exit_point(start_x, start_y, unitSizeX=size, unitSizeY=size, grid=grid, goal=goal)
       # get path to gate from all exit points
       path_found, building = lay_path(exit_points, goal, building) 
       if not path_found :
            h_st_ex.append((building, building))
       else:
           h_st_ex.append(building)
    return h_st_ex

"""
call this method for each grid in the population

input : member - (grid) - single member of population
        startList - the list of all startpoints of the buildings

output: grid - updated grid with all the roads to the buildings
        start_exit_dict - dictionary having all the starting points and corrosponding exit points of buildings for one building.
"""
def get_all_roads(member, startList):
    start_exit_dict = {}
    global grid
    grid = member
    #show initial grid without roads
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    # Build roads to houses
    start_exit_dict['houses'] = build_road_to_building(sorted(startList['houses'], key=lambda x: (-x[0], x[1])), size=2)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to coffice
    start_exit_dict['coffice'] = build_road_to_building(sorted(startList['coffice'], key=lambda x: (-x[0], x[1])), size=2)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to clubhouse
    start_exit_dict['club'] = build_road_to_building(sorted(startList['club'], key=lambda x: (-x[0], x[1])), size=4)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to playground
    start_exit_dict['play'] = build_road_to_building(sorted(startList['play'], key=lambda x: (-x[0], x[1])), size=4)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to clinic
    start_exit_dict['clinic'] = build_road_to_building(sorted(startList['clinic'], key=lambda x: (-x[0], x[1])), size=4)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to school
    start_exit_dict['school'] = build_road_to_building(sorted(startList['school'], key=lambda x: (-x[0], x[1])), size=5)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)
    
    # Build roads to market
    start_exit_dict['market'] = build_road_to_building(sorted(startList['market'], key=lambda x: (-x[0], x[1])), size=5)
#    fig,axis = pyplot.subplots()
#    axis.matshow(grid, cmap=pyplot.cm.tab10)        
    
    return grid, start_exit_dict

#Uncomment below to test
"""
X=np.load("populationGrids.npy")
start_exit_dict = np.load("startsList.npy")
for i in range(X.shape[0]):
    grid=X[i,:,:]
    startList = start_exit_dict[i]
    X[i,:,:], start_exit_dict[i] = get_all_roads(grid, startList=startList)
print(X)
print(start_exit_dict)
np.save('populationGridsUpdt.npy', X)
np.save('start_exit_dict.npy', start_exit_dict)
"""