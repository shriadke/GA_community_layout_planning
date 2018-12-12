# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 01:59:57 2018

@author: shrin
"""

import numpy as np
import matplotlib.pyplot as pyplot

class Node:
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
        
    def move_cost(self,other):
        return 0 if self.value == '.' else 1
        
def children(point,grid):
    x,y = point.point
    links=[]
    if 0<x<24 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)] ]
    if x==0 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x,y + 1),(x+1,y)] ]
    if x==0 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x,y - 1),(x,y + 1),(x+1,y)] ]
    if x==24 and 0<y<24:
        links = [grid[d[0]][d[1]] for d in [(x,y - 1),(x,y + 1),(x - 1,y)] ]
    if 0<x<24 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y + 1),(x+1,y)] ]
    if 0<x<24 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y - 1),(x+1,y)] ]
    if x==24 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y - 1)] ]
    if x==0 and y==24:
        links = [grid[d[0]][d[1]] for d in [(x + 1,y),(x,y - 1)] ]
    if x==24 and y==0:
        links = [grid[d[0]][d[1]] for d in [(x - 1,y),(x,y + 1)] ]
    
    return [link for link in links if link.value != '%' and (link.value=='0' or link.value=='2'or link.value=='7') ]
def manhattan(point,point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])
def aStar(start, goal, grid):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        for node in children(current,grid):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)
    # If 'No Path Found' return empty path
    return []