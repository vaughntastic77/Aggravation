#----------------------------------------------------------------------------------------------------------------------
# Aggravation board game written in python by Jacob Vaughn 04/10/2023
#----------------------------------------------------------------------------------------------------------------------
import pygame as pg
import random
import numpy as np
import os
import sys

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
save_dir = os.path.join(os.path.abspath(os.path.expanduser("~")),f".aggravation")
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
#path_to_img = os.path.abspath(os.path.join(bundle_dir, 'images'))

# Initialize Pygame
pg.init()

# Set the size of the window
winSize = 800
screen = pg.display.set_mode((winSize,winSize))
pg.display.set_caption("Aggravation")

# Create clock for timing
clock = pg.time.Clock()
FPS = 60

# Background Color
BLACK = (0,0,0)
WHITE = (255,255,255)
screen.fill(BLACK) 

# Initialize fonts
titleFont = pg.font.SysFont("Arial",48,bold=True)
menuFont = pg.font.SysFont("Arial",36)
gameFont = pg.font.SysFont("Arial",24)

# Load board image
board = pg.transform.scale(pg.image.load(bundle_dir+"/images/board.png"),(800,800))

# Load marble images
marbSize = 29
red = pg.transform.scale(pg.image.load(bundle_dir+"/images/red.png"),(marbSize,marbSize))
blu = pg.transform.scale(pg.image.load(bundle_dir+"/images/blue.png"),(marbSize,marbSize))
gre = pg.transform.scale(pg.image.load(bundle_dir+"/images/green.png"),(marbSize,marbSize))
yel = pg.transform.scale(pg.image.load(bundle_dir+"/images/yellow.png"),(marbSize,marbSize))
marbs = [red,blu,gre,yel]

# Load the dice face images
diceFaces = [pg.transform.scale(pg.image.load(bundle_dir+f"/images/die{i}.png"),(50,50)) for i in range(1, 7)]

# Marble color order
colors = ["Red","Blue","Green","Yellow"]

# Numbers for move options
mNums = [gameFont.render(f"{i}",True,WHITE) for i in range(1,5)]


#----------------------------------------------------------------------------------------------------------------------
# Initialize marble positions (0 = red, 1 = blue, 2 = green, 3 = yellow)
#----------------------------------------------------------------------------------------------------------------------
dp = 42
# Important game positions
cx = 387
cy = 385
center = np.array([cx,cy])
starts = np.array([[cx-2*dp,cy+7*dp],[cx-7*dp,cy-2*dp],[cx+2*dp,cy-7*dp],[cx+7*dp,cy+2*dp]])
homeins = np.array([[cx,cy+7*dp],[cx-7*dp,cy],[cx,cy-7*dp],[cx+7*dp,cy]])
shortcuts = np.array([[cx+2*dp,cy+2*dp],[cx-2*dp,cy+2*dp],[cx-2*dp,cy-2*dp],[cx+2*dp,cy-2*dp]])
shortcuts = np.append(shortcuts,np.append(shortcuts,shortcuts,axis=0),axis=0)

# Starting base positions
bases = np.zeros((4,4,2))
bases[0] = [[cx-6*dp-16,cy+7*dp-24],[cx-7*dp-16,cy+6*dp-24],[cx-6*dp-16,cy+5*dp-24],[cx-5*dp-16,cy+6*dp-24]]
bases[1] = [[cx-6*dp-17,cy-4*dp-21],[cx-7*dp-17,cy-5*dp-21],[cx-6*dp-17,cy-6*dp-21],[cx-5*dp-17,cy-5*dp-21]]
bases[2] = [[cx+7*dp-28,cy-4*dp-18],[cx+8*dp-28,cy-5*dp-18],[cx+7*dp-28,cy-6*dp-18],[cx+6*dp-28,cy-5*dp-18]]
bases[3] = [[cx+7*dp-28,cy+7*dp-28],[cx+8*dp-28,cy+6*dp-28],[cx+7*dp-28,cy+5*dp-28],[cx+6*dp-28,cy+6*dp-28]]

# Home positions
homes = np.zeros((4,4,2))
for i in range(0,4):
    homes[0,i] = [homeins[0,0],homeins[0,1]-(i+1)*dp]
    homes[1,i] = [homeins[1,0]+(i+1)*dp,homeins[1,1]]
    homes[2,i] = [homeins[2,0],homeins[2,1]+(i+1)*dp]
    homes[3,i] = [homeins[3,0]-(i+1)*dp,homeins[3,1]]

# Full position list in clockwise order
nextPos = np.array([[cx-2*dp,cy+7*dp],[cx-2*dp,cy+6*dp],[cx-2*dp,cy+5*dp],[cx-2*dp,cy+4*dp],[cx-2*dp,cy+3*dp],[cx-2*dp,cy+2*dp],[cx-3*dp,cy+2*dp],[cx-4*dp,cy+2*dp],[cx-5*dp,cy+2*dp],[cx-6*dp,cy+2*dp],[cx-7*dp,cy+2*dp],[cx-7*dp,cy+1*dp],[cx-7*dp,cy+0*dp],[cx-7*dp,cy-1*dp],[cx-7*dp,cy-2*dp],[cx-6*dp,cy-2*dp],[cx-5*dp,cy-2*dp],[cx-4*dp,cy-2*dp],[cx-3*dp,cy-2*dp],[cx-2*dp,cy-2*dp],[cx-2*dp,cy-3*dp],[cx-2*dp,cy-4*dp],[cx-2*dp,cy-5*dp],[cx-2*dp,cy-6*dp],[cx-2*dp,cy-7*dp],[cx-1*dp,cy-7*dp],[cx-0*dp,cy-7*dp],[cx+1*dp,cy-7*dp],[cx+2*dp,cy-7*dp],[cx+2*dp,cy-6*dp],[cx+2*dp,cy-5*dp],[cx+2*dp,cy-4*dp],[cx+2*dp,cy-3*dp],[cx+2*dp,cy-2*dp],[cx+3*dp,cy-2*dp],[cx+4*dp,cy-2*dp],[cx+5*dp,cy-2*dp],[cx+6*dp,cy-2*dp],[cx+7*dp,cy-2*dp],[cx+7*dp,cy-1*dp],[cx+7*dp,cy+0*dp],[cx+7*dp,cy+1*dp],[cx+7*dp,cy+2*dp],[cx+6*dp,cy+2*dp],[cx+5*dp,cy+2*dp],[cx+4*dp,cy+2*dp],[cx+3*dp,cy+2*dp],[cx+2*dp,cy+2*dp],[cx+2*dp,cy+3*dp],[cx+2*dp,cy+4*dp],[cx+2*dp,cy+5*dp],[cx+2*dp,cy+6*dp],[cx+2*dp,cy+7*dp],[cx+1*dp,cy+7*dp],[cx-0*dp,cy+7*dp],[cx-1*dp,cy+7*dp]])
nextPos = np.append(nextPos,np.append(nextPos,nextPos,axis=0),axis=0)

# Actual positions matrix (initially at base)
pos = np.copy(bases)
optPos = np.zeros((4,3,2))

# At base, start, home, and center boolean matrix
atBase = np.array([[True]*4]*4)
atStart = np.array([[False]*4]*4)
atHome = np.array([[False]*4]*4)
atCenter = np.array([[False]*4]*4)

# Color's turn [Red,Blue,Green,Yellow]
turn = 0

# Number of players and computers
nPlayers = 1
computers = True

#----------------------------------------------------------------------------------------------------------------------
# Rolling die animation and final value
#----------------------------------------------------------------------------------------------------------------------
def roll():
    i = 0
    for x in range(0,10):
        i = random.randint(0,5)
        screen.blit(diceFaces[i],(210,710))
        pg.display.update()
        clock.tick(10)
    clock.tick(1.5)
    return i+1

#----------------------------------------------------------------------------------------------------------------------
# Display a dice value
#----------------------------------------------------------------------------------------------------------------------
def dice(n):
    screen.blit(diceFaces[n-1],(210,710))
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)

#----------------------------------------------------------------------------------------------------------------------
# Draw all images on screen in current position
#----------------------------------------------------------------------------------------------------------------------
def draw(opts):
    # Draw board
    screen.fill(BLACK) 
    screen.blit(board,(0,0))
    # Display each marble at current position
    for c in range(0,4):
        for m in range(0,4):
            screen.blit(marbs[c],pos[c,m]) 
    # if nPlayers > 1:
    #     screen.blit(pg.transform.rotate(screen, turn*90), (0, 0))
    # Waiting to roll text
    if opts == 1:
        textTurn = gameFont.render(colors[turn]+"'s turn.",True,WHITE)
        screen.blit(textTurn,(winSize//2 - textTurn.get_width()//2,710))
        textRoll = gameFont.render("Press Space to roll.",True,WHITE)
        screen.blit(textRoll,(winSize//2 - textRoll.get_width()//2,740))
    # Choosing marble text
    elif opts == 2:
        textMarb = gameFont.render("Choose which to move.",True,WHITE)
        screen.blit(textMarb,(winSize//2 - textMarb.get_width()//2,725))
    # Choosing move text
    elif opts == 3:
        textMove1 = gameFont.render("Choose where to move",True,WHITE)
        screen.blit(textMove1,(winSize//2 - textMove1.get_width()//2,710))
        textMove2 = gameFont.render("or press Esc to go back.",True,WHITE)
        screen.blit(textMove2,(winSize//2 - textMove2.get_width()//2,740))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)

#----------------------------------------------------------------------------------------------------------------------
# Write data to savedGame.npz
#----------------------------------------------------------------------------------------------------------------------
def saveGame():
    np.savez(save_dir+"/savedGame.npz",pos=pos,atBase=atBase,atStart=atStart,atHome=atHome,atCenter=atCenter,turn=turn,nPlayers=nPlayers,computers=computers)

#----------------------------------------------------------------------------------------------------------------------
# Load data from savedGame.npz
#----------------------------------------------------------------------------------------------------------------------
def loadGame():
    global pos, atBase, atStart, atHome, atCenter, turn, nPlayers, computers
    if os.path.isfile(save_dir+"/savedGame.npz"):
        fLoaded = np.load(save_dir+"/savedGame.npz")
        # Actual positions matrix
        pos = fLoaded["pos"]
        # At base, start, home, and center boolean matrix
        atBase = fLoaded["atBase"]
        atStart = fLoaded["atStart"]
        atHome = fLoaded["atHome"]
        atCenter = fLoaded["atCenter"]
        # Color's turn [Red,Blue,Green,Yellow]
        turn = fLoaded["turn"]
        # Number of players and computers
        nPlayers = fLoaded["nPlayers"]
        computers = fLoaded["computers"]
    else:
        newGame()

#----------------------------------------------------------------------------------------------------------------------
# Reinitialize positions
#----------------------------------------------------------------------------------------------------------------------
def newGame():
    global pos, atBase, atStart, atHome, atCenter, turn, nPlayers, computers
    # Actual positions matrix (initially at base)
    pos = np.copy(bases)
    # At base, start, home, and center boolean matrix
    atBase = np.array([[True]*4]*4)
    atStart = np.array([[False]*4]*4)
    atHome = np.array([[False]*4]*4)
    atCenter = np.array([[False]*4]*4)
    # Color's turn [Red,Blue,Green,Yellow]
    turn = 0
    # Number of players and computers
    nPlayers = 1
    computers = True

#----------------------------------------------------------------------------------------------------------------------
# Gather all possible moves for given n and store in optPos
#----------------------------------------------------------------------------------------------------------------------
def moves(n):
    global pos, optPos, atBase, atStart, atHome
    optPos = np.zeros((4,3,2))
    canMove = np.array([True]*4)
    # Get each marble move options
    for m in range(0,4):
        optPos[m,0] = pos[turn,m]
        # Check if in base or start
        if atBase[turn,m]:
            if n == 1 or n == 6:
                # Check for same color in start
                if np.invert(atStart[turn]).all(axis=0): 
                    optPos[m,0] = starts[turn]
            else:
                optPos[m,0] = bases[turn,m]
        # Get center move options
        elif atCenter[turn,m]:
            if n==1:
                if np.invert((pos[turn] == shortcuts[turn]).all(axis=1)).all(axis=0):
                    optPos[m,0] = shortcuts[turn]
                    if np.invert((pos[turn] == shortcuts[turn+3]).all(axis=1)).all(axis=0):
                        optPos[m,1] = shortcuts[turn+3]
                        if np.invert((pos[turn] == shortcuts[turn+2]).all(axis=1)).all(axis=0):
                            optPos[m,2] = shortcuts[turn+2]
                    elif np.invert((pos[turn] == shortcuts[turn+2]).all(axis=1)).all(axis=0):
                        optPos[m,1] = shortcuts[turn+2]
                elif np.invert((pos[turn] == shortcuts[turn+3]).all(axis=1)).all(axis=0):
                    optPos[m,0] = shortcuts[turn+3]
                    if np.invert((pos[turn] == shortcuts[turn+2]).all(axis=1)).all(axis=0):
                        optPos[m,1] = shortcuts[turn+2]
                elif np.invert((pos[turn] == shortcuts[turn+2]).all(axis=1)).all(axis=0):
                    optPos[m,0] = shortcuts[turn+2]
        # Get normal move option if marble can move
        else:
            breakout = False
            for i in range(0,n):
                # Check for nearing home or at home
                if np.array_equal(optPos[m,0],homeins[turn]):
                    optPos[m,0] = homes[turn,0]
                elif np.array_equal(optPos[m,0],homes[turn,0]):
                    optPos[m,0] = homes[turn,1]
                elif np.array_equal(optPos[m,0],homes[turn,1]):
                    optPos[m,0] = homes[turn,2]
                elif np.array_equal(optPos[m,0],homes[turn,2]):
                    optPos[m,0] = homes[turn,3]
                elif np.array_equal(optPos[m,0],homes[turn,3]):
                    optPos[m,0] = pos[turn,m]
                    break
                # Normal move option
                else:
                    optPos[m,0] = nextPos[1 + np.where((nextPos == optPos[m,0]).all(axis=1))[0][0]]
                # Check for landing on or passing same color
                for mTurn in range(0,4):
                    if np.array_equal(optPos[m,0],pos[turn,mTurn]):
                        optPos[m,0] = pos[turn,m]
                        breakout = True
                if breakout:
                    break
        # Center option from start
        clearPath = True
        if np.array_equal(optPos[m,0],pos[turn,m]):
            clearPath = False
            for i in range(0,4):
                if np.array_equal(pos[turn,i],nextPos[6 + np.where((nextPos == starts[turn]).all(axis=1))[0][0]]):
                    clearPath = True
        if atStart[turn,m] and n==6 and np.invert(atCenter[turn]).all(axis=0) and clearPath:
            optPos[m,2] = center
        # Check for landing on other color on its own start
        for c in range(0,4):
            if np.array_equal(optPos[m,0],starts[c]) and atStart[c].any():
                optPos[m,0] = pos[turn,m]
        # Get shortcut move option if on shortcut
        for i in range(0,4):
            if np.array_equal(pos[turn,m],shortcuts[i]):
                if n==1 and np.invert(atCenter[turn]).all(axis=0):
                    optPos[m,2] = center
                optPos[m,1] = shortcuts[i]
                breakout = False
                for j in range(0,n):
                    optPos[m,1] = shortcuts[1 + np.where((shortcuts == optPos[m,1]).all(axis=1))[0][0]]
                    # Check for landing on or passing same color
                    for mTurn in range(0,4):
                        if np.array_equal(optPos[m,1],pos[turn,mTurn]) and m!=mTurn:
                            optPos[m,1] = [0,0]
                            breakout = True
                    if breakout:
                        break
                break
        # Check if can only move in shortcuts
        if np.array_equal(optPos[m,0],pos[turn,m]) and not np.array_equal(optPos[m,1],[0,0]):
            optPos[m,0] = optPos[m,1]
            optPos[m,1] = [0,0]

    # Number marbles that can move
    for m in range(0,4):
        if np.array_equal(optPos[m,0],pos[turn,m]) and np.array_equal(optPos[m,1],[0,0]) and np.array_equal(optPos[m,2],[0,0]):
            canMove[m] = False
    if np.invert(canMove).all(axis=0):
        draw(0)
    else:
        draw(2)
    dice(n)
    for m in range(0,4):
        if canMove[m]:
            screen.blit(mNums[m],(pos[turn,m,0] + marbSize//4,pos[turn,m,1]))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose marble to move
    m = -1
    if np.invert(canMove).all(axis=0):
        m = 0
    while m < 0:
        # Computer chooses random marble that can move
        if computers and turn >= nPlayers:
            opts = np.array(range(0,4))[canMove]
            m = random.choice(opts)
            for mc in range(0,4):
                if atCenter[turn,mc] and n==1:
                    m = mc
            marb_move(m,n)
        # Choose marble to move
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1 and canMove[0]:
                        m = 0
                        marb_move(m,n)
                    elif event.key == pg.K_2 and canMove[1]:
                        m = 1
                        marb_move(m,n)
                    elif event.key == pg.K_3 and canMove[2]:
                        m = 2
                        marb_move(m,n)
                    elif event.key == pg.K_4 and canMove[3]:
                        m = 3
                        marb_move(m,n)
    # Check for landing on other color to send to base
    for c in range(0,4):
        if not (c == turn):
            for moc in range(0,4):
                if np.array_equal(pos[turn,m],pos[c,moc]):
                    pos[c,moc] = bases[c,moc]
    # Update position booleans
    for c in range(0,4):
        for m in range(0,4):
            atBase[c,m] = np.array_equal(pos[c,m],bases[c,m])
            atStart[c,m] = np.array_equal(pos[c,m],starts[c])
            for i in range(0,4):
                atHome[c,m] = np.array_equal(pos[c,m],homes[c,i])
                if atHome[c,m] == True:
                    break
            atCenter[c,m] = np.array_equal(pos[c,m],center)

#----------------------------------------------------------------------------------------------------------------------
# Move chosen marble
#----------------------------------------------------------------------------------------------------------------------
def marb_move(m,n):
    global pos
    draw(3)
    dice(n)
    # Draw move options for selected marble
    for o in range(0,3):
        if not np.array_equal(optPos[m,o],[0,0]):
            pg.draw.circle(screen,BLACK,(optPos[m,o,0] + 15,optPos[m,o,1] + 14),12,width=2)
            screen.blit(mNums[o],(optPos[m,o,0] + 20,optPos[m,o,1] - 20))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose where to move
    o = -1
    while o < 0:
        # Computer chooses to move shortcuts then regular
        if computers and turn >= nPlayers:
            if atStart[turn,m] and (not np.array_equal(optPos[m,2],[0,0])):
                o = 2
            elif (not np.array_equal(optPos[m,1],[0,0])) and (not np.array_equal(pos[turn,m],shortcuts[turn])) and (not atCenter[turn,m]):
                o = 1
            else:
                o = 0
        # Choose which option
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1 and (not np.array_equal(optPos[m,0],[0,0])):
                        o = 0
                    elif event.key == pg.K_2 and (not np.array_equal(optPos[m,1],[0,0])): 
                        o = 1
                    elif event.key == pg.K_3 and (not np.array_equal(optPos[m,2],[0,0])):
                        o = 2
                    elif event.key == pg.K_ESCAPE:
                        return moves(n)
    # Update marble postion for chosen marble and move option
    pos[turn,m] = optPos[m,o]

#----------------------------------------------------------------------------------------------------------------------
# Show main menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def menu():
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize//2 - menuSize//2,winSize//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Aggravation",True,BLACK)
    screen.blit(title,(winSize//2 - title.get_width()//2,winSize//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[R] Resume Last Game",True,BLACK)
    screen.blit(text1,(winSize//2 - text1.get_width()//2,winSize//2 - text1.get_height()//2 - 50))
    text2 = menuFont.render("[N] New Game",True,BLACK)
    screen.blit(text2,(winSize//2 - text2.get_width()//2,winSize//2 - text2.get_height()//2 - 0))
    textE = menuFont.render("[Esc] Exit",True,BLACK)
    screen.blit(textE,(winSize//2 - textE.get_width()//2,winSize//2 - textE.get_height()//2 + 150))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # Load game
                if event.key == pg.K_r:
                    return loadGame()
                # New game
                elif event.key == pg.K_n:
                    return newMenu()
                # Quit (ESC)
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

#----------------------------------------------------------------------------------------------------------------------
# Show new game menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def newMenu():
    global nPlayers, computers
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize//2 - menuSize//2,winSize//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Aggravation",True,BLACK)
    screen.blit(title,(winSize//2 - title.get_width()//2,winSize//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[1] One Player",True,BLACK)
    screen.blit(text1,(winSize//2 - text1.get_width()//2,winSize//2 - text1.get_height()//2 - 50))
    text2 = menuFont.render("[2] Two Players",True,BLACK)
    screen.blit(text2,(winSize//2 - text2.get_width()//2,winSize//2 - text2.get_height()//2 - 0))
    text3 = menuFont.render("[3] Three Players",True,BLACK)
    screen.blit(text3,(winSize//2 - text3.get_width()//2,winSize//2 - text3.get_height()//2 + 50))
    text4 = menuFont.render("[4] Four Players",True,BLACK)
    screen.blit(text4,(winSize//2 - text4.get_width()//2,winSize//2 - text4.get_height()//2 + 100))
    textE = menuFont.render("[Esc] Back",True,BLACK)
    screen.blit(textE,(winSize//2 - textE.get_width()//2,winSize//2 - textE.get_height()//2 + 150))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Reinitialize positions
    newGame()
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # One Player
                if event.key == pg.K_1:
                    nPlayers = 1
                    compMenu()
                    return
                # Two Player
                elif event.key == pg.K_2:
                    nPlayers = 2
                    compMenu()
                    return
                # Three Player
                elif event.key == pg.K_3:
                    nPlayers = 3
                    compMenu()
                    return
                # Four Player
                elif event.key == pg.K_4:
                    nPlayers = 4
                    return
                # No Players
                elif event.key == pg.K_0:
                    nPlayers = 0
                    computers = True
                    return
                # Back to main menu (ESC)
                elif event.key == pg.K_ESCAPE:
                    return menu()

#----------------------------------------------------------------------------------------------------------------------
# Computers option menu
#----------------------------------------------------------------------------------------------------------------------
def compMenu():
    global computers
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize//2 - menuSize//2,winSize//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Aggravation",True,BLACK)
    screen.blit(title,(winSize//2 - title.get_width()//2,winSize//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("Computer players?",True,BLACK)
    screen.blit(text1,(winSize//2 - text1.get_width()//2,winSize//2 - text1.get_height()//2 - 50))
    text2 = menuFont.render("Yes [Y] / No [N]",True,BLACK)
    screen.blit(text2,(winSize//2 - text2.get_width()//2,winSize//2 - text2.get_height()//2 - 0))
    textE = menuFont.render("[Esc] Back",True,BLACK)
    screen.blit(textE,(winSize//2 - textE.get_width()//2,winSize//2 - textE.get_height()//2 + 150))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Key pressed
            if event.type == pg.KEYDOWN:
                # Computers on
                if event.key == pg.K_y:
                    computers = True
                    return
                # Computers off
                elif event.key == pg.K_n:
                    computers = False
                    return
                # Go Back
                elif event.key == pg.K_ESCAPE:
                    return newMenu()

#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def pause():
    draw(0)
    # Draw menu background
    menuSize = 350
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize//2 - menuSize//2,winSize//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Aggravation",True,BLACK)
    screen.blit(title,(winSize//2 - title.get_width()//2,winSize//2 - title.get_height()//2 - 100))
    text1 = menuFont.render("[R] Resume Game",True,BLACK)
    screen.blit(text1,(winSize//2 - text1.get_width()//2,winSize//2 - text1.get_height()//2 - 0))
    text2 = menuFont.render("[S] Save and Quit",True,BLACK)
    screen.blit(text2,(winSize//2 - text2.get_width()//2,winSize//2 - text2.get_height()//2 + 50))
    textE = menuFont.render("[Esc] Quit to Menu",True,BLACK)
    screen.blit(textE,(winSize//2 - textE.get_width()//2,winSize//2 - textE.get_height()//2 + 100))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # Resume game
                if event.key == pg.K_r:
                    return True
                # Save and quit game
                elif event.key == pg.K_s:
                    saveGame()
                    return False
                # Quit to main menu (ESC)
                elif event.key == pg.K_ESCAPE:
                    return False

#----------------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------------
def main():
    global turn
    running = True
    while running:
        menu()
        # In game loop
        inGame = True
        winners = [False]*4
        while inGame:
            # Events
            for event in pg.event.get():
                # Close window
                if event.type == pg.QUIT:
                    inGame = False
                    running = False
                # Key pressed
                elif event.type == pg.KEYDOWN:
                    # Roll die (return)
                    if event.key == pg.K_SPACE:
                        if not winners[turn]:
                            n = roll()
                            moves(n)
                        else:
                            n = 1
                        if n != 6:
                            turn += 1
                        if computers:
                            if turn == 4:
                                turn = 0
                        else:
                            if turn == nPlayers:
                                turn = 0
                    # Pause (p)
                    elif event.key == pg.K_p:
                        inGame = pause()

            # Skip winner turn
            if winners[turn]:
                turn += 1
                if computers:
                    if turn == 4:
                        turn = 0
                else:
                    if turn == nPlayers:
                        turn = 0

            # Check for winner
            for c in range(0,4):
                if atHome[c].all(axis=0) and (not winners[c]):
                    winners[c] = True
                    draw(0)
                    # Draw menu background
                    menuSize = 500
                    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize//2 - menuSize//2,winSize//2 - menuSize//4,menuSize,menuSize//2))
                    # Draw menu text
                    title = titleFont.render(colors[c]+" wins!",True,BLACK)
                    screen.blit(title,(winSize//2 - title.get_width()//2,winSize//2 - title.get_height()//2 - 75))
                    text1 = menuFont.render("[Space] Return to menu",True,BLACK)
                    screen.blit(text1,(winSize//2 - text1.get_width()//2,winSize//2 - text1.get_height()//2 - 15))
                    text2 = menuFont.render("[C] Continue playing",True,BLACK)
                    screen.blit(text2,(winSize//2 - text2.get_width()//2,winSize//2 - text2.get_height()//2 + 35))
                    textE = menuFont.render("[Esc] Exit.",True,BLACK)
                    screen.blit(textE,(winSize//2 - textE.get_width()//2,winSize//2 - textE.get_height()//2 + 85))
                    # Update screen
                    pg.event.pump()
                    pg.display.update()
                    clock.tick(FPS)
                    # Choose menu option
                    doneRunning = False
                    while not doneRunning:
                        for event in pg.event.get():
                            # Close window
                            if event.type == pg.QUIT:
                                pg.quit()
                                sys.exit()
                            # Key pressed
                            elif event.type == pg.KEYDOWN:
                                # Back to menu
                                if event.key == pg.K_SPACE:
                                    doneRunning = True
                                    inGame = False
                                # Continue playing
                                elif event.key == pg.K_c:
                                    doneRunning = True
                                # Quit (ESC)
                                elif event.key == pg.K_ESCAPE:
                                    pg.quit()
                                    sys.exit()

            # Display game
            draw(1)
            clock.tick(FPS)

            # Computer roll
            if turn >= nPlayers:
                n = roll()
                moves(n)
                if n != 6:
                    turn += 1
                if computers:
                    if turn == 4:
                        turn = 0
                else:
                    if turn == nPlayers:
                        turn = 0

    # Close pygame
    pg.quit()

main()
