# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 16:54:27 2014

@author: olgis
Conway's Game of Life.

TO DO: not populating all field if 600x480 

"""
import game_logic as gl
import pygame          

playground_size = [150, 120] #width, height
screen_size = (600, 480)
cell_size = [screen_size[0] / playground_size[0], 
             screen_size[1] / playground_size[1] ]


#total number of cells on playground
total_num =  playground_size[0] * playground_size[1]   

#initial number of randomly populated cells
seed_num = total_num // 5

#background colour
back_colour = (0, 0, 0)
cell_colour = (0, 75, 255)

#To store [n-3, n-2, n-1, n] playground, for Oscillators: Pulsar
playground_history = [0, 0] #[n-3, n-2]
    
        
if __name__ == '__main__':
    #init playground and it history
    previous, playground = gl.seed(seed_num, total_num)
    
    playground_history.append(previous) #[n-3, n-2, n-1]
    playground_history.append(playground) #[n-3, n-2, n-1, n]
    
    neighbours_dict = gl.get_neighbours(playground_size, total_num)

    pygame.init()
    
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Conway's Game of Life")
    
    
    mainloop = True

    
    while mainloop:
        screen.fill(back_colour) #fill the background with BLACK
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False #pygame window closed by user
                print "Game over by QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False #user pressed ESC
                    print "Game over by ESC"
        
        #drawing rectangules on a screen         
        gl.drawing_obj(screen, playground_size, cell_size, playground,
                       cell_colour)       
        
        #update playground
        playground = gl.values_update(playground, neighbours_dict) 
        # add n-th playground and remove n-4
        playground_history.append(playground)
        playground_history.pop(0)
        
        #check if the game is over
        mainloop = gl.game_over(mainloop, playground_history)

        pygame.time.delay(300)  #delay in mSeconds
        pygame.display.update()