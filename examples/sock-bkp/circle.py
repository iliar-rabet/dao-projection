import pygame
import math
 
def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta) 
 
def main():
    pygame.display.set_caption("Oribit")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
     
    coords =0,0
    angle = 0
    rect = pygame.Rect(*coords,20,20)
    speed = 100
    next_tick = 0
     
    running = True
    while angle!=360:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
         
        ticks = pygame.time.get_ticks() 
        vel=coords
        if ticks > next_tick:
            next_tick += speed
            angle += 1
            old_coords=coords
            coords = move_coords(angle, 0.1, coords)
            vel=coords[0]-old_coords[0],coords[1]-old_coords[1]
            rect.topleft = coords
            # print(str(ticks/1000))
            ti=float(ticks/1000)
            print("0 " +str("{:.1f}".format(ti)) + " " +str("{:.2f}".format(coords[0])) + " " + str("{:.2f}".format(coords[1])))

            # print("vel: " + str("{:.2f}".format(ti)) + " "+ str(vel))
            # print(vel)
            
        screen.fill((0,0,30))
        screen.fill((0,150,0), rect)
        pygame.display.flip()
        clock.tick(30)
     
    pygame.quit()
 
if __name__ == '__main__':
    main()