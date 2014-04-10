# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:59:43 2013

@author: olgis
Conway's Game of Life

    Any live cell with fewer than two live neighbours dies, 
                as if caused by under-population.
    Any live cell with two or three live neighbours
                lives on to the next generation.
    Any live cell with more than three live neighbours dies,
                as if by overcrowding.
    Any dead cell with exactly three live neighbours becomes a live cell,
               as if by reproduction.
"""
import numpy.random as nprnd
import pygame.draw as pydr

def seed(seed_num, total):
    """Generate an inital position of cells, based on seed number.
        fun(int, int) --> list, list"""
    ground = [0]*(total) #generate a playground populated by 0
    play_ground = ground[:]
    rand_list = nprnd.randint(0, total, seed_num) #list of rnd values
    for rnd_num in rand_list:
        play_ground[rnd_num] = 1 #assigning rnd values to 1
    
    return ground, play_ground

def get_neighbours(num_size, total):
    """Generate dict of neighbours' indexes for every cell.
        fun(list, int) --> dict{int sq: [neighbout index]}"""
    neigh_dict = {}
    w_num, h_num = num_size
    left_edge = range(0, total, w_num)
    right_edge = range(w_num-1, total, w_num)
    
    for row in range(1, w_num+1):
        for col in range(h_num):
            now = (row - 1) + (col * w_num) #calculate index of the cell

            #calculate all 9 possible neightbours
            all_neigh = [(now - 1) - w_num, now - w_num, (now + 1) - w_num,
                          now - 1,                        now + 1, 
                         (now - 1) + w_num, now + w_num, (now + 1) + w_num] 
            if now < w_num:
                #remove all values bellow 0
                all_neigh = [i for i in all_neigh if i > 0]
            if now in left_edge:
                #remove false right edge neighbours
                all_neigh = [j for j in all_neigh if j not in right_edge]
            if now in right_edge:
                #remove false left edge neighbours
                all_neigh = [k for k in all_neigh if k not in left_edge]
            if now > (w_num*(h_num-1)-2):
                #remove valuse greater then total
                all_neigh = [f for f in all_neigh if f < total]                
            
            neigh_dict[now] = all_neigh


    return neigh_dict
    
    
    
def values_update(playground, neighbours_dict):
    """Update playground acording to rules of the game
       fun(list, list) --> list new_playground, list old_playground"""
    new_playground = playground[:]
    
    for ind, val in [[i, x] for i, x in enumerate(new_playground)]:
        
        new_val = [playground[n_index] for n_index in neighbours_dict[ind]]
       
        new_playground[ind] = rules_of_game(val, new_val)
        
    return new_playground
    
    
      
def rules_of_game(sq_value, neigh_value):
    """Change value of cells acording to it neighbours
       fun(int, list) --> int """
    
    #under-population
    if sq_value == 1 and neigh_value.count(1) < 2:
        sq_value = 0

    # by overcrowding
    if sq_value == 1 and neigh_value.count(1) > 3:
        sq_value = 0
        
    #by reproduction
    if sq_value == 0 and neigh_value.count(1) == 3:
        sq_value = 1
    
    return sq_value
    
def game_over(running, ground_history):
    """Finish the game by setting running to 0, acording to 3 cases
       fun(boolean, list of lists) --> boolean"""
    current = ground_history[-1]
    if 1 not in current:
        print "Game over, because all cells are dead"
        running = False
    elif  ground_history[:-1].count(current) == 1:
        print "Game over, in a loop"
        running = False          
        
    return running      


def drawing_obj(display, ground_size, rect_size, current_ground, rect_colour):
    """ draw only alive cells on the display
        fun(obj,[width, height], [width, height], list,
            tupl(R,G,B)) --> 0"""
    #select only alive
    c_list = [i for i, x in enumerate(current_ground) if x == 1]
    
    for cell in c_list:
        x_pos = (cell % ground_size[0] ) * rect_size[0]
        y_pos = (cell // ground_size[1]) * rect_size[1]

        pydr.rect(display, rect_colour, (x_pos, y_pos, rect_size[0],
                                                   rect_size[1]), 1)
                                        
    return 0