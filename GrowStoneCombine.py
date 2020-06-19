#! python3
"""
================================
Grow Stone Online Stone Combiner
================================
"""
import pyautogui, time, os, logging, sys, random, copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
# logging.disable(logging.DEBUG) # uncomment to block debug log messages

# Stone name constants (don't change: image filenames depend on the values)
COLD_SHURIKEN = 'cold_shuriken'
FOUR_SHURIKEN = 'four_shuriken'
CLOVER = 'clover'
FOUR_CLOVER = 'four_clover'
HADOUKEN = 'hadouken'
DONUT = 'donut'
BRONZE_STAR = 'bronze_star'
SILVER_STAR = 'silver_star'
GOLD_STAR = 'gold_star'
CRESCENT = 'crescent'
HALF_MOON = 'half_moon'
FULL_MOON = 'full_moon'
SNOWBALL = 'snowball'
ICE_CUBE = 'ice_cube'
ICICLE = 'icicle'
FIREBALL = 'fireball'
BUTTERFLY_WING = 'butterfly_wing'
ANGEL_WING = 'angel_wing'
DRAGON_WING = 'dragon_wing'
THREESTARS_BALL = 'threestars_ball'
FIVESTARS_BALL = 'fivestars_ball'
SEVENSTARS_BALL = 'sevenstars_ball'

# Stones to scan for List
ALL_STONE_TYPES = (COLD_SHURIKEN, FOUR_SHURIKEN, CLOVER, FOUR_CLOVER, HADOUKEN, DONUT, BRONZE_STAR, SILVER_STAR, GOLD_STAR, CRESCENT, HALF_MOON, FULL_MOON, SNOWBALL, ICE_CUBE, ICICLE, FIREBALL, BUTTERFLY_WING, ANGEL_WING, DRAGON_WING, THREESTARS_BALL, FIVESTARS_BALL, SEVENSTARS_BALL)

# Game Coordinations
GAME_REGION = () # coordinates value of the entire inventory window

def imPath(filename):
    """A shortcut for joining the 'images/'' file path.
    Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)

def getGameRegion():
    """Obtains the region of game on the screen.
    Assigns value to GAME_REGION."""
    global GAME_REGION

    # identify the bottom-right corner
    logging.debug('Finding game region...')
    region = pyautogui.locateOnScreen(imPath('top_right_corner.png'), confidence = 0.93)
    if region is None:
        raise Exception('Could not find game on screen.')

    # calculate the region of entire game (top,left,width,height)
    """Total inventory size approx w 530 h 290"""
    topRightX = region[0] + region[2] # left + width
    topRightY = region[1] # top
    GAME_REGION = (topRightX - 520, topRightY - 15, 530, 290)
    logging.debug('Game region found: %s' % (GAME_REGION,))
    ##im = pyautogui.screenshot('screen.png', region = (GAME_REGION))

def getStones():
    """Scans the screen for duplicate stones.
    Returns with dictionary (left, top, width, height) tuple of integersstones = {}"""
    stones = {}
    for stoneType in (ALL_STONE_TYPES):
        allStones = pyautogui.locateAllOnScreen(imPath('%s_stone.png' % stoneType), region=(GAME_REGION[0] + 5, GAME_REGION[1] + 60, 470, 180), confidence = 0.88)
        for stone in allStones:
            stones[stone] = stoneType
    return stones

def index(lst, element):
    """When stone matches found, find all occurences in the list."""
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
        except ValueError:
            return result
        result.append(offset)
        

def combineStones():
    """Searches through dictionary to find matches.
    Uses coordinates to combine stones."""
    itemList = []
    stones_list = getStones()
    valueList = list(stones_list.values())
    itemList.append(list(stones_list.keys()))
    
    #Going through each stone item sequentially
    for i in ALL_STONE_TYPES: 
        counter = 0
        #search through the list for matching name
        for entry in valueList: 
            if entry == i: 
                counter += 1
                #confirmed duplicate
                if counter >= 2:
                    #find all occurances of the stone
                    coords = []
                    falsePos = []
                    dup = index(valueList,entry)
                    print ('There is a duplicate of: %s' % (entry))
                    #Found position in valueList, find coordinates
                    for itm in dup:
                        posX = itemList[0][itm][0]
                        posY = itemList[0][itm][1]
                        coords.append([posX,posY])                  
                    #Filter out False Positives
                    """Check for any false positives in image recognition.
                    Also remove the last item if it's an odd number."""
                    for i in range(len(coords)):
                        curX,curY = coords[i]
                        prevX, prevY = coords[i-1]
                        diffX = abs(curX - prevX)
                        diffY = abs(curY - prevY)
                
                        if diffX + diffY >= 20: #20 pixel threshold in X,Y direction
                            falsePos.append(coords[i])
                        else:
                            continue
                        
                    ##print ('FP list: %s' % (falsePos))

                    correctList = []
                    #Make sure all odd lists are corrected (drop the last item)
                    if len(falsePos) % 2 != 0:
                        for i in range(len(falsePos)-1):
                            correctList.append(falsePos[i])
                    else:
                         correctList = falsePos
                    print('Final Coordinates list is: %s' % (correctList))

                    #Combine matched stones using list of coordinates
                    """Using the correctList of coordinates.
                    They should all be ordered sequentially."""

                    if len(correctList) >= 4:
                        """In big list, sequential list drags around combined stone.
                        causes issue."""
                        for i in range(0,len(correctList)-1,2):
                            firstPosX = correctList[i][0]
                            firstPosY = correctList[i][1]
                            secPosX = correctList[i+1][0]
                            secPosY = correctList[i+1][1]

                            #Generate some randomness to the coordinates to simulate human
                            """Hardcoded the adjustment so cursor is approximately in center of
                            item. Add additional random offset of +-10"""
                            offset = random.randint(-10,10)
                            timeOffset = random.uniform(0.8,3.0)
                                                
                            #Move to first position, then click and drag items together
                            pyautogui.moveTo(firstPosX + 20, firstPosY + 15, timeOffset, pyautogui.easeInBounce)  # move mouse to XY over num_second seconds               
                            pyautogui.dragTo(secPosX + 20 + offset, secPosY + 15 + offset, timeOffset , pyautogui.easeInBounce)  # drag mouse to XY
                    elif len(correctList) == 0:
                        logging.debug('Skipping an empty list of %s' % (entry) + ' found.')
                        continue
                    else:
                        for i in range(len(correctList)-1):
                            #print('List is only 2')
                            firstPosX = correctList[i][0]
                            firstPosY = correctList[i][1]
                            secPosX = correctList[i+1][0]
                            secPosY = correctList[i+1][1]
                            #print ('List in coordinates function: %s' % (correctList))

                            #Generate some randomness to the coordinates to simulate human
                            """Hardcoded the adjustment so cursor is approximately in center of
                            item. Add additional random offset of +-10"""
                            offset = random.randint(-10,10)
                            timeOffset = random.uniform(0.1,0.6)
                                                
                            #Move to first position, then click and drag items together
                            pyautogui.moveTo(firstPosX + 20, firstPosY + 15, timeOffset, pyautogui.easeInBounce)  # move mouse to XY over num_second seconds               
                            pyautogui.dragTo(secPosX + 20 + offset, secPosY + 15 + offset, timeOffset , pyautogui.easeInBounce)  # drag mouse to XY
                else:
                    logging.debug('There are no duplicates of %s' % (entry) + ' found.')
        #print ('Sleeping before next item scan')
        #time.sleep(2)

print ('=' * 80)
print ('Grow Stone Combiner')
print ('=' * 80)
logging.debug('Program Started. Press Ctrl-C to abort at any time.')
logging.debug('To interrupt mouse movement, move mouse to upper left corner.')
getGameRegion()
logging.debug('Bot will start in 5 seconds.')
while True:
    try:
        time.sleep(5)
        getStones()
        combineStones()
    except:
        KeyboardInterrupt
        sys.exit()
