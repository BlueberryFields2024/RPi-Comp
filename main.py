import sys
import googlemaps
import pygame
import math
import regex
from PIL import Image
import QuestMaker as qm
import QuestUtils as utils
from Logger import Logger
import adafruit_gps
import geopy
import serial
import time

logger = Logger("main", active = True) 
#Call logger like a function to log to the console like print.
#Logs will look like "(main): {Message}", so no need to put a space at the beginning.
#Logs can be toggled by setting active to False.
#Otherwise, other than the fact that it implements *args now, it works exactly as it used to.
#The fact that it implements *args means you can use it exactly like print(*args) in most cases.

def call():
    gps.update()
    if not gps.has_fix:
        # Try again if we don't have a fix yet.
        logger("Waiting for GPS satellite fixture...")
        return [False, [0, 0], "N/A", "N/A", "N/A"]
    else:
        timestamp = "{}/{}/{} {:02}:{:02}:{:02}".format(
        gps.timestamp_utc.tm_mon,
        gps.timestamp_utc.tm_mday,
        gps.timestamp_utc.tm_year,
        gps.timestamp_utc.tm_hour,
        gps.timestamp_utc.tm_min,
        gps.timestamp_utc.tm_sec,
        )
        return [True, [gps.latitude, gps.longitude], gps.altitude_m, gps.speed_knots, timestamp]
    # return [True, [53.39294958714515, -2.9163110822775136], "N/A", "N/A", "N/A"]

def bearing():
    global direction
    arduinoData = str(arduino.readline())
    # arduinoData = "r'100.00\b\n'"
    try:
        direction = float(arduinoData[2:-5])
        logger("Bearing = " + str(direction))
    except:
        logger("Warning: arduino data is formatted incorrectly")

def mapGen():
    global map
    f = open("assets/map.png", 'wb')
    for chunk in gmaps.static_map(size=(272,150), format="jpg", zoom=15, maptype="terrain", center=questLoc):
        if chunk:
            f.write(chunk)
    f.close()
    image = Image.open("assets/map.png")
    sepia_filter = ((0.393, 0.769, 0.189), (0.349, 0.686, 0.168), (0.272, 0.534, 0.131))
    apply_filter(image, sepia_filter)
    image.save("assets/mapSepia.png")
    map = pygame.image.load("assets/mapSepia.png")
    logger('Generated new quest')

def apply_filter(image, mask):
    (width, height) = image.size
    for y in range(0, height):
        for x in range(0, width):
            px = image.getpixel((x, y))
            new_px = get_new_pixel(px, mask)
            image.putpixel((x, y), new_px)

def get_new_pixel(old_px, mask):
    (r, g, b) = old_px
    r-=64
    g-=64
    b-=64
    new_r = int((r * mask[0][0] + g * mask[0][1] + b * mask[0][2]) * 0.851)
    new_g = int((r * mask[1][0] + g * mask[1][1] + b * mask[1][2]) * 0.542)
    new_b = int((r * mask[2][0] + g * mask[2][1] + b * mask[2][2]) * 0.256)
    if new_r <= 175 and new_g <= 100 and new_b <= 40:
        if new_r <= 150 and new_g <= 90 and new_b <= 35:
            if new_r <= 125 and new_g <= 75 and new_b <= 25:
                new_r = 125
                new_g = 56
                new_b = 51
            else:
                new_r = 171
                new_g = 81
                new_b = 48
        else:
            new_r = 180
            new_g = 90
            new_b = 46
    return new_r, new_g, new_b

dirs = ["N","NE","E","SE","S","SW","W","NW"]
def directionify(dir):
    dir = (round(dir/45))%8
    return dirs[dir]

pygame.init()
pygame.font.init()
DISPLAYSURF = pygame.display.set_mode((480, 320))
pygame.display.set_caption('Blueberry Fields')
pygame.display.set_icon(pygame.image.load('assets/blueberry.png'))
ui = pygame.image.load("assets/blueberryUI.png")
box = pygame.image.load("assets/blueberryDialogue.png")
narrate = pygame.image.load("assets/blueberryNarration.png")
option2 = pygame.image.load("assets/blueberryOptions2.png")
option3 = pygame.image.load("assets/blueberryOptions3.png")
compass = pygame.image.load("assets/blueberryCompass.png")
xpBar = pygame.image.load("assets/xpBar.png")
compassCenter = [408, 66]
gmaps = googlemaps.Client(key='AIzaSyC48kW3kb2qfwYL5yLoV_HB2ALfVBYHbWg')
clock = pygame.time.Clock()

# Sprite store
sprites = {
    "silhouette.png": pygame.image.load("assets/silhouette.png")
}

questGen = True
questName = "N/A"
questDesc = "You're not supposed to be here."
questLoc = [0,0]
questPay = 0
questDist = 0
questDeg = 0
direction = 0
distance = 0
prevQuestDist = None
timeElapsed = 0
blueberries = 0
calories = 0
items = []
exponential = 1.2
last_call = time.monotonic()
dialogueToggle = False
rewards = []
dialogueList = []
currentDialogue = 0
decision = 1
startText = True

try:
    arduino = serial.Serial(port="COM6", baudrate=9600, timeout=10)
except:
    pygame.quit()
    raise Exception("\n" * 3 + " " * 5 + "WARNING\n" + "=" * 55 + "\n Arduino device not found!" + "\n Please ensure the dongle is attatched before running.\n" + "=" * 55)

arduino.setDTR(False)
time.sleep(1)
arduino.flush()
arduino.setDTR(True)

try:
    uart = serial.Serial(port="COM5", baudrate=9600, timeout=10)
except:
    pygame.quit()
    raise Exception("\n" * 3 + " " * 5 + "WARNING\n" + "=" * 55 + "\n GPS device not found!" + "\n Please ensure the dongle is attatched before running.\n" + "=" * 55)

gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,500")
GPSfix = False

with open("save.txt") as file:
    saveFile = [line.rstrip() for line in file]

font0 = pygame.font.SysFont(name = "dejavuserif", size = 15, italic = True, bold = True)
font1 = pygame.font.SysFont(name = "dejavusans", size = 8, italic = True)
font2 = pygame.font.SysFont(name = "dejavuserif", size = 15, italic = True)
font3 = pygame.font.SysFont(name = "dejavusans", size = 12)
font4 = pygame.font.SysFont(name = "dejavuserif", size = 10)

if __name__ == "__main__":
    while True:
        bearing()
        current = time.monotonic()
        if current - last_call >= 0.5:
            last_call = current
            GPSdata = call()
            GPSfix = GPSdata[0]
            location = GPSdata[1]

        if GPSfix:
            if not dialogueToggle:
                if questGen:
                    questObj = qm.QuestMaster.generateQuest(location, "SimpleFetch")
                    questName = questObj.name[0]
                    questPay = questObj.rewards[0]
                    questLoc = questObj.targetLocation
                    dialogueList = utils.Generic.DecomposeDialogue(questObj.start()[0])
                    currentDialogue = 0
                    dialogueToggle = True
                    startText = True
                    mapGen()
                    questGen = False
                else:
                    advance = questObj.advance(location)
                    logger(advance)
                    if advance != False:
                        dialogueList = utils.Generic.DecomposeDialogue(advance[0])
                        currentDialogue = 0
                        dialogueToggle = True
                        if len(advance) > 1:
                            rewards = advance[1]
                            questGen = True
                        else:
                            questLoc = questObj.targetLocation
                            mapGen()

            ##
            ##
            questDist = questObj.getDistance(location)
            questDeg = questObj.getBearing(location)
            questLoc = questObj.targetLocation
            questDesc = questObj.guide()[0]
            ##
            ##
            if prevQuestDist != None:
                distance += abs(questDist - prevQuestDist)
            prevQuestDist = questDist
    
            experience = int(distance * 0.02)
            try:
                level = math.log(experience, exponential)
            except:
                level = 0
    
            questNameR = font0.render(questName, True, (59, 32, 39))
            questDescR = regex.findall(
              pattern = r"(.{0,50})(?: |$)",
              string = questDesc
            )
            questDesc0R = font1.render("- " + questDescR[0], True, (59, 32, 39))
            questDesc1R = font1.render(questDescR[1], True, (59, 32, 39))
            questPayR = font2.render("Reward: " + str(questPay) + "ƀ", True, (64, 73, 115))
            questDistR = font3.render(str(int(questDist)) + "m", True, (59, 32, 39))
            questDir = directionify(questDeg)
            questDirR = font3.render(questDir, True, (59, 32, 39))
            blueberriesStat = font4.render(str(blueberries) + " ƀ", True, (100, 200, 255))
            experienceStat = font4.render(str(experience) + " xp", True, (153, 229, 80))
            distanceStat = font4.render(str(int(distance)) + " m", True, (255, 238, 131))
            timeStat = font4.render(str(int(timeElapsed)) + " s", True, (255, 238, 131))
            caloriesStat = font4.render(str(calories) + " kcal", True, (255, 238, 131))
            itemsNumStat = font4.render(str(len(items)) + " items", True, (255, 238, 131))
            totalDistanceStat = font4.render(str(int(saveFile[0])/1000) + " km", True, (255, 238, 131))
            questsStat = font4.render(str(saveFile[1]) + " quests", True, (255, 238, 131))
            levelStat = font4.render("LVL " + str(math.floor(level)), True, (153, 229, 80))
            expReqStat = font4.render(str(int((exponential**level) - math.floor(exponential**level))) + "/" + str(math.floor(exponential**(level+1)) - math.floor(exponential**level)), True, (153, 229, 80))
        
            DISPLAYSURF.blit(ui, (0, 0))
            DISPLAYSURF.blit(questNameR, (30, 48))
            DISPLAYSURF.blit(questDesc0R, (32, 68))
            DISPLAYSURF.blit(questDesc1R, (32, 78))
            DISPLAYSURF.blit(questPayR, (28, 94))
            DISPLAYSURF.blit(questDistR, questDistR.get_rect(center = (300, 110)))
            DISPLAYSURF.blit(questDirR, questDirR.get_rect(center = (300, 95)))
            DISPLAYSURF.blit(map, (0, 198))
            needle = pygame.transform.rotate(compass, -direction)
            DISPLAYSURF.blit(needle, (compassCenter[0] - int(needle.get_width()/2), compassCenter[1] - int(needle.get_height()/2)))
            DISPLAYSURF.blit(font4.render("Session:", True, (245, 255, 232)), font4.render("Session:", True, (245, 255, 232)).get_rect(center = (408, 178)))
            DISPLAYSURF.blit(blueberriesStat, blueberriesStat.get_rect(center = (378, 226)))
            DISPLAYSURF.blit(experienceStat, experienceStat.get_rect(center = (438, 226)))
            DISPLAYSURF.blit(distanceStat, distanceStat.get_rect(center = (378, 194)))
            DISPLAYSURF.blit(timeStat, timeStat.get_rect(center = (438, 194)))
            DISPLAYSURF.blit(caloriesStat, caloriesStat.get_rect(center = (378, 210)))
            DISPLAYSURF.blit(itemsNumStat, itemsNumStat.get_rect(center = (438, 210)))
            DISPLAYSURF.blit(font4.render("Lifetime:", True, (245, 255, 232)), font4.render("Lifetime:", True, (245, 255, 232)).get_rect(center = (408, 250)))
            DISPLAYSURF.blit(totalDistanceStat, totalDistanceStat.get_rect(center = (378, 266)))
            DISPLAYSURF.blit(questsStat, questsStat.get_rect(center = (438, 266)))
            DISPLAYSURF.blit(xpBar, xpBar.get_rect(center = (408, 295)))
            DISPLAYSURF.blit(levelStat, levelStat.get_rect(center = (378, 282)))
            DISPLAYSURF.blit(expReqStat, expReqStat.get_rect(center = (438, 282)))
        
            if dialogueToggle:

                if dialogueList[currentDialogue].type == "Speech":
                    DISPLAYSURF.blit(box, (0, 0))
                    DISPLAYSURF.blit(sprites[dialogueList[currentDialogue].speakerImage], (34, 164))
                    DISPLAYSURF.blit(font0.render(dialogueList[currentDialogue].speaker, True, (245, 255, 232)), (147, 175))
                    dialogueLines  = regex.findall(
                            pattern = r"(.{0,55})(?: |$)",
                            string = dialogueList[currentDialogue].text
                        )
                    for x in range(len(dialogueLines)):
                        dialogueRender = font3.render(dialogueLines[x], True, (59, 32, 39))
                        DISPLAYSURF.blit(dialogueRender, (180, 210 + (x * 20)))
                    if currentDialogue == len(dialogueList)-1 and startText:
                        decision = 2
                        DISPLAYSURF.blit(option2, (0, 0))
                        DISPLAYSURF.blit(font3.render("Accept", True, (245, 255, 232)), font3.render("Accept", True, (245, 255, 232)).get_rect(center = (271, 111)))
                        DISPLAYSURF.blit(font3.render("Reject", True, (245, 255, 232)), font3.render("Reject", True, (245, 255, 232)).get_rect(center = (399, 111)))

                if dialogueList[currentDialogue].type == "Narration":
                    DISPLAYSURF.blit(narrate, (0, 0))
                    dialogueLines  = regex.findall(
                            pattern = r"(.{0,60})(?: |$)",
                            string = dialogueList[currentDialogue].text
                        )
                    for x in range(len(dialogueLines)):
                        dialogueRender = font3.render(dialogueLines[x], True, (59, 32, 39))
                        DISPLAYSURF.blit(dialogueRender, (180, 200 + (x * 20)))

                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if decision == 2:
                        if (
                            (pygame.mouse.get_pos()[0] >= 218 and pygame.mouse.get_pos()[0] <= 326)
                            and
                            (pygame.mouse.get_pos()[1] >= 90 and pygame.mouse.get_pos()[1] <= 134)
                        ):
                            dialogueList = utils.Generic.DecomposeDialogue(questObj.accept()[0])
                            currentDialogue = 0
                            startText = False
                            decision = 1
                        if (
                            (pygame.mouse.get_pos()[0] >= 346 and pygame.mouse.get_pos()[0] <= 454)
                            and
                            (pygame.mouse.get_pos()[1] >= 90 and pygame.mouse.get_pos()[1] <= 134)
                        ):
                            dialogueList = utils.Generic.DecomposeDialogue(questObj.reject()[0])
                            currentDialogue = 0
                            startText = False
                            decision = 1
                            questGen = True
                    else:
                        if currentDialogue < len(dialogueList)-1 and dialogueToggle:
                            currentDialogue += 1
                        else: 
                            currentDialogue = 0
                            dialogueToggle = False
        pygame.display.update()
        clock.tick(20)
        
