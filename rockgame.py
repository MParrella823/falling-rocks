import pygame
import random
import serial
import time
import random
import sys
from item import *
from rock import *
from ice import *

pygame.init()
display_width = 800
display_height = 600

# color definitions
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# game character
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(
    'Rocky Start - Copyright 2018, The College of Saint Rose')
clock = pygame.time.Clock()

rocklist = []     # Create an empty list to hold our rocks
numRocks = 7    # Specify the number of rocks to create

icelist = []  # Create list for Ice objects
numIce = 3

rockImage = 'rock.png'
iceImage = 'ice.png'

itemList = [] # Create list for all falling objects
numItems = len(itemList)
print(numItems)
imageWidth = 125
imageHeight = 125
playerImg = pygame.image.load('you-rock2.png')
playerImg_width = 125
playerImg_height = 100


rockImageFile = "rock2.png"
iceImageFile = "ice.gif"

rockImage = pygame.image.load(rockImageFile)
iceImage = pygame.image.load(iceImageFile)


use_port = False


def serialRead(ser):
    line = ser.readline().decode('ascii')
    xy = line.strip().split(',')
    return xy

def speedDelta(ser):
    delta = 0
    accel = serialRead(ser)
    print(accel)

    if len(accel) == 2:
        if len(accel[0]) > 0 and float(accel[0]) < -0.25:
            delta = -1
        elif len(accel[0]) > 0 and float(accel[0]) > 0.25:
            delta = 1

    return delta

# Create our rocks using the the specified image
# Initially, our position (x,y) will be set to (0,0) and speed will be 0.

def init_rocks():
    for i in range(0, numRocks):
        item = Item(0, 0, 0, rockImage, Rock)
        itemList.append(item)


def init_ice():
    for i in range(0, numIce):
        item = Item(0, 0, 0, iceImage, Ice)
        itemList.append(item)




def show_item(item):
    # blit is displaying image xy is a tuple
    gameDisplay.blit(item.getImage(), (item.getXpos(), item.getYpos()))


#def show_ice(ice):
 #   gameDisplay.blit(ice.getImage(), (ice.getXpos(), ice.getYpos()))

# a function to place the player ioon in our surface


def player(x, y):
    # blit is displaying image xy is a tuple
    gameDisplay.blit(playerImg, (x, y))


def score(s):
    scoretext = myfont.render("Score: {0}".format(s), 1, (0, 0, 0))
    gameDisplay.blit(scoretext, (5, 5))


def gameover():
    gameovertext = gofont.render("GAME OVER", 1, (0, 0, 0))
    gameDisplay.blit(gameovertext, (display_width/2 - 150, display_height/2))

# check if there was a collision between 2 items


def check_collision(r1, r2, width, height):
    x1 = r1.getXpos()
    y1 = r1.getYpos()
    x2 = r2.getXpos()
    y2 = r2.getYpos()
    if abs(x2-x1) < width-20 and abs(y2-y1) < height-50:
        return True
    else:
        return False


def player_collide(x1, y1, x2, y2):
    if abs(x2-x1) < 50 and abs(y2-y1) < 50:
        return True
    else:
        return False

# Combine all object lists
itemList = icelist + rocklist

def game_loop():
    game_score = 0
    delta_speed = 0
    delta = 0
    player_x = (display_width*0.5) - (0.5*playerImg_width)
    player_y = (display_height-playerImg_height)
    gameExit = False
    ser = None
    key_x = 0


    # Update each rock in the rocklist
    #for rock in rocklist:
        # subtract the width of the image
       # rock.setXpos(random.randrange(0, display_width-imageWidth))
        #rock.setYpos(-125)
        #rock.setSpeed(random.randrange(1, 7))

   # for ice in icelist:
    #    ice.setXpos(random.randrange(0, display_width-imageWidth))
     #   ice.setYpos(-125)
      #  ice.setSpeed(random.randrange(1, 7))


    #for ice in icelist:
     #   ice.setXpos(random.randrange(0, display_width-imageWidth))
      #  ice.setYpos(-125)
       # ice.setSpeed(random.randrange(1, 7))


    for item in itemList:
        item.setXpos(random.randrange(0, display_width - imageWidth))
        item.setYpos(-125)
        item.setSpeed(random.randrange(1,7))


    #TODO: Comment out below code, check functionality of accelerometer
    # open port to read accelerometer data from Arduino
    if use_port:
        # Arduino serial communication
        ser = serial.Serial('COM3', 9600, timeout=1)

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            key_x = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_x = -0.20
                if event.key == pygame.K_RIGHT:
                    key_x = 0.20
                if event.key == pygame.K_DOWN:
                    delta_speed = 0

        if use_port:
            delta = speedDelta(ser)
        else:
            delta = key_x

        delta_speed += delta  # accumulate increases/decreases from iteration to iteration
        player_x += delta_speed  # change x by current delta
        if player_x < -25:
            player_x = -25
            delta_speed = 0
        if player_x > display_width-100:
            player_x = display_width-100
            delta_speed = 0

        gameDisplay.fill(white)
        j = 0
        """
        for rock in rocklist:
            # changing the y coordinate to make rocks move
            rock.setYpos(rock.getYpos() + rock.getSpeed())
            show_rock(rock)

            # Reset rock to top of screen if it fell below bottom

            if rock.getYpos() > display_height:
                rock.setYpos(-125)
                # subtract the width of the image
                rock.setXpos(random.randrange(0, display_width-imageWidth))
                rock.setSpeed(random.randrange(1, 7))

            j += 1
            for i in range(j, numRocks):
                if check_collision(rock, rocklist[i], imageWidth, imageHeight)and(not (rock.getYpos == -125)):
                    rock.setYpos(-125)
                    # subtract the width of the image
                    rock.setXpos(random.randrange(0, display_width-imageWidth))
                    rock.setSpeed(random.randrange(1, 7))

        for ice in icelist:
            ice.setYpos(rock.getYpos() + ice.getSpeed())
            show_ice(ice)

            if ice.getYpos() > display_height:
                ice.setYpos(-125)
                ice.setXpos(random.randrange(0, display_width-imageWidth))
                ice.setSpeed(random.randrange(1, 7))


            for i in range(j, numIce):
                if check_collision(ice, icelist[i], imageWidth, imageHeight) and (not(ice.getYpos == -125)):
                    ice.setYpos(-125)
                    ice.setXpos(random.randrange(0, display_width-imageWidth))
                    ice.setSpeed(random.randrange(1, 7))
            """

        for item in itemList:

                item.setYpos(item.getYpos() + item.getSpeed())
                show_item(item)

                if item.getYpos() > display_height:
                    item.setYpos(-125)
                    item.setXpos(random.randrange(0, display_width-imageWidth))


                j+=1
                for i in range(j, len(itemList)):
                    if check_collision(item, itemList[i], imageWidth, imageHeight) and (not(item.getYpos == -125)):
                        item.setYpos(-125)
                        item.setXpos(random.randrange(0, display_width))
                        item.setSpeed(random.randrange(1, 7))

        for item in itemList:
            if player_collide(item.getXpos(), item.getYpos(), player_x, player_y):
                
                # Implement frozen character logic (greatly slows player speed)
                if (item.getType() == Ice):

                    # Set duration of effect
                    i = 10

                    while i > 0:
                        # stop player character when Ice is encountered
                        delta_speed = -.5
                        delta_speed = .5

                        # ignore keyboard input
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                key_x = -0.00
                            if event.key == pygame.K_RIGHT:
                                key_x = 0.00
                            if event.key == pygame.K_DOWN:
                                delta_speed = 0
                        i-=1
                else:
                    gameExit = True
        """
        for ice in icelist:
           if player_collide(ice.getXpos(), ice.getYpos(), player_x, player_y):
               for i in 100:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        key_x = -0.00
                    if event.key == pygame.K_RIGHT:
                        key_x = 0.00
                    if event.key == pygame.K_DOWN:
                        delta_speed = 0
                i+=1
        """

        player(player_x, player_y)
        #gameDisplay.blit(disclaimertext, (5, 5))
        game_score += 10
        score(game_score)
        pygame.display.update()
        clock.tick(50)

      # how many frames per second is updated

    gameDisplay.fill(white)
    player(player_x, player_y)
    # gameDisplay.blit(disclaimertext, (5, 5))
    game_score += 10
    score(game_score)
    gameover()
    pygame.display.update()
    time.sleep(5)


if __name__ == "__main__":
    # gameDisplay.fill(white)
    myfont = pygame.font.SysFont('arial', 18)
    gofont = pygame.font.SysFont('arial', 40)
    disclaimertext = myfont.render(
        "Copyright 2018, The College of Saint Rose", 1, (0, 0, 0))

    init_ice()
    init_rocks()
    game_loop()
    # to quit you need to stop pygame
    pygame.quit()
    quit()  # this will quit if not in IDLE when you run
