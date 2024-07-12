from cmu_graphics import *
import random
import math
import os, pathlib

# Citation from Sound Tech Demo
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

def onAppStart(app):
    app.bestScore = 0
    onGameStart(app)

class Bird:
    def __init__(self,cx,cy,radius):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.bodyColor = 'darkOrange'
        self.border = 'black'

        self.mouthX = self.cx + self.radius + self.radius//3 - 5
        self.mouthY = self.cy
        self.mouthRX = 20
        self.mouthRY = 10
        
        self.wingX = self.cx - 5 - self.radius//2
        self.wingY = self.cy
        self.wingAngle = 0
        self.wingRX = 50
        self.wingRY = 30

        self.eyeWhiteX = self.cx + self.radius//2
        self.eyeWhiteY = self.cy - self.radius//2
        self.eyeBlackX = self.eyeWhiteX + self.radius//5
        self.eyeBlackY = self.eyeWhiteY - self.radius//5
        
    def updateMouthWingEye(self,dy):
        self.mouthY += dy
        self.wingY += dy
        if 0 <= self.wingAngle <= 45:
            self.wingAngle -= 20
        elif -45 <= self.wingAngle <= 0:
            self.wingAngle += 20
        self.eyeWhiteY += dy
        self.eyeBlackY += dy

    def __hash__(self):
        return hash(str(self))
    
# These two classes are implemented when app.score >= 30 in hard mode.

class Award: # Score + 5
    def __init__(self,cx,cy):
        self.cx = cx
        self.cy = cy
        self.radius = 30
        self.sinex = 0

    def motion(self):
        self.cx -= 10
        self.sinex += 1
        self.cy = 300+10*(math.sin(self.sinex))

    def __hash__(self):
        return hash(str(self))
    
class BadBird: # Punishment: Player bird gets bigger
    def __init__(self,cx,cy):
        self.cx = cx
        self.cy = cy
        self.radius = 20
        self.bodyColor = 'royalBlue'
        self.border = 'black'

        self.mouthX = self.cx - self.radius - self.radius//3 + 5
        self.mouthY = self.cy
        
        self.wingX = self.cx + 5 + self.radius//2
        self.wingY = self.cy
        self.wingAngle = 0

        self.eyeWhiteX = self.cx - self.radius//2
        self.eyeWhiteY = self.cy - self.radius//2
        self.eyeBlackX = self.eyeWhiteX - self.radius//5
        self.eyeBlackY = self.eyeWhiteY - self.radius//5
        
    def updateMouthWingEye(self,dx):
        self.mouthX += dx
        self.wingX += dx
        if 0 <= self.wingAngle <= 45:
            self.wingAngle -= 20
        elif -45 <= self.wingAngle <= 0:
            self.wingAngle += 20
        self.eyeWhiteX += dx
        self.eyeBlackX += dx
        
    def motion(self):
        self.cx -= 8

    def __hash__(self):
        return hash(str(self))

def onGameStart(app):
    #Sounds
    app.backgroundMusic = loadSound("Sound/Sakura-Girl-Daisy-chosic.com_.mp3")
    app.birdSound = loadSound("Sound/mixkit-explainer-video-game-alert-sweep-236.wav")
    app.startSound = loadSound("Sound/mixkit-arcade-video-game-bonus-2044.wav")
    app.startPlay = False
    app.gameOverSound = loadSound("Sound/mixkit-final-level-bonus-2061.wav")
    #App Variables
    app.stepsPerSecond = 16
    app.shift = 5
    app.start = False
    app.easy = False # Used for split modes
    app.hard = False # Used for split modes
    #Tree Variables
    app.upTreeHeight = [random.randrange(150,250), random.randrange(150,250), random.randrange(150,250), random.randrange(150,250), random.randrange(150,250)]
    app.bottomTreeHeight = [random.randrange(400,450)-app.upTreeHeight[0], random.randrange(400,450)-app.upTreeHeight[1], random.randrange(400,450)-app.upTreeHeight[2], random.randrange(400,450)-app.upTreeHeight[3], random.randrange(400,450)-app.upTreeHeight[4]]
    app.treeWidth = 50
    app.upTopLeft = 200
    app.bottomTopLeft = 250
    #Bird
    player = Bird(100,app.height//2,30)
    app.player = [player]
    app.ascend = False
    #TimeCount
    app.startTime = 0
    app.currTime  = 0
    #Score
    app.score = 0
    #Button Colors
    app.easyColor = 'orange'
    app.hardColor = 'orange'
    app.backColor = rgb(118, 174, 245)
    app.helpColor = rgb(194, 62, 52)
    #Bad Bird
    app.badBird = []
    app.badDict=dict()
    #Awards
    app.award = []
    app.awardDict=dict()
    #ObjectCounter
    app.objectCounter = 0
    #Countdown
    app.countDownCounter = 0
    app.startCountDown = False
    #Help
    app.help = False
    
def redrawAll(app):
    if app.start == False:
        app.backgroundMusic.play()
        if app.help == True:
            drawHelpMenu(app)
        else:
            drawSky(app)
            drawClouds(app)
            drawBush(app)
            drawTrees(app)
            drawBird(app)
            drawGround(app)
            drawLabel('Fab Flap',app.width//2,app.height//2-50,size=100,fill='white',border='black')
            drawButtons(app)
        
    elif app.startCountDown == True and app.start == True:
        drawSky(app)
        drawClouds(app)
        drawBush(app)
        drawTrees(app)
        drawBird(app)
        drawGround(app)
        drawCountDown(app)
        
    elif app.startCountDown == False and app.start == True: # Game Start!
        app.backgroundMusic.play(restart=True)
        drawSky(app)
        drawClouds(app)
        drawBush(app)
        drawTrees(app)
        drawGround(app)
        drawBird(app)
        drawAwards(app)
        drawBadBirds(app)
        if collisionDetect(app) == False:
            drawScore(app)
        if collisionDetect(app) == True:
            drawRect(app.width//2, app.height//2, 200, 400, align = 'center',fill='lightSalmon',opacity=70,border='black',borderWidth=0.5)
            drawLabel('Game Over:(',app.width//2,app.height//2-100,size = 30,bold=True)
            #Show Scores:
            drawLabel(f'Current Score: {app.score}',app.width//2,app.height//2,size=20)
            drawLabel(f'Best Score: {app.bestScore}',app.width//2,app.height//2+100,size=20)
            # Direction to player
            drawLabel('Press r to restart',app.width//2,app.height-25,size=20,bold=True)
            
def drawHelpMenu(app):
    drawSky(app)
    drawClouds(app)
    drawBush(app)
    drawTrees(app)
    drawGround(app)
    drawBird(app)
    drawRect(app.width//2, app.height//2, 300, 600, align = 'center',fill=rgb(118, 174, 245),opacity=70,border='black',borderWidth=0.5)
    drawLabel('Game Guide',app.width//2,app.height//2-200,size = 30,bold=True)
    drawLabel("Press space key to move bird upward",app.width//2,app.height//2-120,size=16)
    drawLabel("and don't let it collide with trees!",app.width//2,app.height//2-100,size=16)
    drawLabel("In hard mode:",app.width//2-75,app.height//2-20,size=16,bold=True)
    #AwardScheme
    drawCircle(app.width//2-75,app.height//2+50,30,fill='hotPink',border='black')
    drawLabel('If you hit the award,',app.width//2+50,app.height//2+35,size=12)
    drawLabel('you get 5 extra points',app.width//2+50,app.height//2+55,size=12)
    #BadBirdScheme
    drawOval(app.width//2-97,app.height//2+175,10,5,fill='yellow',border = 'black')
    drawCircle(app.width//2-75,app.height//2+175,20,fill='royalBlue',border = 'black')
    drawOval(app.width//2-60,app.height//2+175,30,10,fill='lemonChiffon',border='black')
    drawCircle(app.width//2-85,app.height//2+165,10,fill='white',border='black')
    drawCircle(app.width//2-89,app.height//2+161,5,fill='black')
    drawLabel('If you hit the bad birds,',app.width//2+50,app.height//2+170,size=12)
    drawLabel('your bird gets bigger (e.g. harder!)',app.width//2+50,app.height//2+190,size=12)
    
    #BackButton
    drawRect(app.width//2,app.height-50,100,50,fill=app.backColor,opacity=70,align='center')
    drawLabel('Back',app.width//2,app.height-50,size=16,bold=True)
    
            
def drawCountDown(app):
    if app.countDownCounter//(app.stepsPerSecond) == 0:
        drawLabel('3',app.width//2,app.height//2,size=80,border='black',fill='white')
    elif app.countDownCounter//(app.stepsPerSecond*2) == 0:
        drawLabel('2',app.width//2,app.height//2,size=80,border='black',fill='white')
    elif app.countDownCounter//(app.stepsPerSecond*3) == 0:
        drawLabel('1',app.width//2,app.height//2,size=80,border='black',fill='white')
      
def drawScore(app):
    drawLabel(f'Score: {app.score}',app.width//2,app.height-25,size=20,bold=True)
            
def drawButtons(app):
    drawRect(app.width//2,app.height//2+75,150,80,align='center',fill=app.easyColor,border='black') #EASY
    drawRect(app.width//2+75,app.height//2+36,5,80,fill='lightYellow') # 3D Borders
    drawRect(app.width//2-70,app.height//2+115,150,5,fill='lightYellow')
    drawRect(app.width//2,app.height//2+200,150,80,align='center',fill=app.hardColor,border='black') #HARD
    drawRect(app.width//2+75,app.height//2+161,5,80,fill='lightYellow') # 3D Borders
    drawRect(app.width//2-70,app.height//2+240,150,5,fill='lightYellow')
    drawRect(app.width-50,app.height-25,100,50,align='center',fill=app.helpColor,opacity=70,border='black') #HELP
    drawLabel('EASY',app.width//2,app.height//2+75,size=40)
    drawLabel('HARD',app.width//2,app.height//2+200,size=40)
    drawLabel('HELP',app.width-50,app.height-25,size=20)

def drawSky(app):
    drawRect(0, 0, app.width, app.height, fill=gradient('lightBlue', 'lightSkyBlue', 'deepSkyBlue', start='top'))
    
def drawTrees(app):
    for i in range(5):
        topRectLeft = app.upTopLeft + i * 5 * app.treeWidth
        topRectTop = 0
        drawRect(topRectLeft,topRectTop,app.treeWidth,app.upTreeHeight[i],fill='seaGreen',border='black')
        drawRect(topRectLeft,topRectTop,app.treeWidth//5,app.upTreeHeight[i],fill='paleGreen')
    for i in range(5):
        bottomRectLeft = app.bottomTopLeft + i * 5 * app.treeWidth
        bottomRectTop = app.height - app.bottomTreeHeight[i]
        drawRect(bottomRectLeft,bottomRectTop,app.treeWidth,app.bottomTreeHeight[i],fill='seaGreen',border='black')
        drawRect(bottomRectLeft,bottomRectTop,app.treeWidth//5,app.bottomTreeHeight[i],fill='paleGreen')

def drawBird(app):
    for player in app.player:
        #Mouth
        drawOval(player.mouthX,player.mouthY,player.mouthRX,player.mouthRY,fill='yellow',border = 'black')
        #Body
        drawCircle(player.cx,player.cy,player.radius,fill=player.bodyColor,border = player.border)
        #Wing
        drawOval(player.wingX,player.wingY,player.wingRX,player.wingRY,fill='lemonChiffon',border='black',rotateAngle = player.wingAngle)
        #Eyes
        drawCircle(player.eyeWhiteX,player.eyeWhiteY,player.radius//2,fill='white',border='black')
        drawCircle(player.eyeBlackX,player.eyeBlackY,player.radius//4,fill='black')

def drawClouds(app):
    for i in range(4):
        center = 30+i*(app.width//3)
        drawRect(center, 100, 40, 40,fill='white')
        drawRect(center-10,110,50,20,fill='white')
        drawRect(center+10,110,50,20,fill='white')

def drawBush(app):
    for i in range(8):
        drawArc(50+i*100,app.height-50,100,50,0,270,fill='mediumSpringGreen')

def drawGround(app):
    drawRect(0,app.height-50,app.width,app.height-50,fill='khaki')
    drawRect(0,app.height-50,app.width,10,fill='gold')

def drawAwards(app):
    for award in app.award:
        drawCircle(award.cx,award.cy,30,fill='hotPink',border='black')

def drawBadBirds(app):
    for bad in app.badBird:
        #Mouth
        drawOval(bad.mouthX,bad.mouthY,10,5,fill='yellow',border = 'black')
        #Body
        drawCircle(bad.cx,bad.cy,bad.radius,fill=bad.bodyColor,border = bad.border)
        #Wing
        drawOval(bad.wingX,bad.wingY,30,10,fill='lemonChiffon',border='black',rotateAngle = bad.wingAngle)
        #Eyes
        drawCircle(bad.eyeWhiteX,bad.eyeWhiteY,bad.radius//2,fill='white',border='black')
        drawCircle(bad.eyeBlackX,bad.eyeBlackY,bad.radius//4,fill='black')

def awardCollision(app):
    # Collision with Awards
    for player in app.player:
        for award in app.award:
            if distance(player.cx,player.cy,award.cx,award.cy) <= player.radius+award.radius:
                return True
    return False

def badBirdCollision(app):
    # Collision with BadBirds
    for player in app.player:
        for badBird in app.badBird:
            if distance(player.cx,player.cy,badBird.cx,badBird.cy) <= player.radius + badBird.radius:
                return True
    return False

def collisionDetect(app):
    # Rectangular Collision
    for player in app.player:
    # Bird with Ground and ceiling
        if player.cy + player.radius >= app.height-50 or player.cy - player.radius <= 0:
            return True
    # Bird with Upper Tree
        else:
            for i in range(5):
                topRectLeft = app.upTopLeft + i * 5 * app.treeWidth
                if distance(player.cx,player.cy,topRectLeft,app.upTreeHeight[i]) <= player.radius:
                    return True
                elif distance(player.cx,player.cy,topRectLeft+app.treeWidth,app.upTreeHeight[i]) <= player.radius:
                    return True
                elif (player.cx + player.radius == topRectLeft and player.radius <= player.cy <= app.upTreeHeight[i]+player.radius) or (player.cx - player.radius == topRectLeft+app.treeWidth and player.radius <= player.cy <= app.upTreeHeight[i]+player.radius):
                    return True
    # Bird with Bottom tree
            for i in range(5):
                bottomRectLeft = app.bottomTopLeft + i * 5 * app.treeWidth
                if distance(player.cx,player.cy,bottomRectLeft,app.height-app.bottomTreeHeight[i]) <= player.radius:
                    return True
                elif distance(player.cx,player.cy,bottomRectLeft+app.treeWidth,app.height-app.bottomTreeHeight[i]) <= player.radius:
                    return True
                elif (player.cx + player.radius == bottomRectLeft and app.height-app.bottomTreeHeight[i] <= player.cy) or (player.cx - player.radius == bottomRectLeft+app.treeWidth and app.height-app.bottomTreeHeight[i] <= player.cy): 
                    return True
    return False

def distance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

def scoring(app):
    for i in range(5):
        topRectLeft = app.upTopLeft + i * 5 * app.treeWidth
        for player in app.player:
            #When the bird successfully passes the right end of the tree without collision
            if player.cx - player.radius == topRectLeft + app.treeWidth and collisionDetect(app) == False:
                app.score += 1
    for i in range(5):
        bottomRectLeft = app.bottomTopLeft + i * 5 * app.treeWidth
        for player in app.player:
            if player.cx - player.radius == bottomRectLeft + app.treeWidth and collisionDetect(app) == False:
                app.score += 1

def bestScore(app):
    if app.score > app.bestScore:
        app.bestScore = app.score
        
def velocity(app):
    vf = abs(2*(app.currTime-app.startTime))# elapsedTime * a
    return vf

def acceleration(app):
    vf = velocity(app)
    a = 2
    dy = (vf**2)/(a*2) # 2*acceleration
    return dy   

def onKeyPress(app,key):
    if app.start == True and app.startCountDown == False:
        if collisionDetect(app) == False:
            if key == 'space':
                app.birdSound.play(restart=True)

                app.currTime = 0
                app.ascend = True
    if key == 'r':
        onGameStart(app)
            
def onMousePress(app,mouseX,mouseY):
    leftButtonE = app.width//2-150//2
    rightButtonE = leftButtonE + 150
    upperButtonE = app.height//2+75-80//2
    lowerButtonE = upperButtonE + 80
    
    leftButtonH = app.width//2-150//2
    rightButtonH = leftButtonH + 150
    upperButtonH = app.height//2+200-80//2
    lowerButtonH = upperButtonH + 80
    if app.help == False and app.start == False:
        if leftButtonE <= mouseX <= rightButtonE and upperButtonE <= mouseY <= lowerButtonE:
            app.start = True
            app.startCountDown = True
            app.easy = True
            app.startplay = True
            if app.startplay:
                app.startSound.play()
            app.startplay = False
        elif leftButtonH <= mouseX <= rightButtonH and upperButtonH <= mouseY <= lowerButtonH:
            app.start = True
            app.startCountDown = True
            app.hard = True
            app.startplay = True
            if app.startplay:
                app.startSound.play()
            app.startplay = False    
        elif app.width-100 <= mouseX <= app.width and app.height-50 <= mouseY <= app.height:
            app.help = True
    if app.help == True and app.start == False:
        if app.width//2-50 <= mouseX <= app.width//2+50 and app.height-75 <= mouseY <= app.height-25:
            app.help = False
    
def onMouseMove(app,mouseX,mouseY):
    leftButtonE = app.width//2-150//2
    rightButtonE = leftButtonE + 150
    upperButtonE = app.height//2+75-80//2
    lowerButtonE = upperButtonE + 80
    
    leftButtonH = app.width//2-150//2
    rightButtonH = leftButtonH + 150
    upperButtonH = app.height//2+200-80//2
    lowerButtonH = upperButtonH + 80
    
    if app.help == False:
        if leftButtonE <= mouseX <= rightButtonE and upperButtonE <= mouseY <= lowerButtonE:
            app.easyColor = rgb(196, 180, 98)    
        elif leftButtonH <= mouseX <= rightButtonH and upperButtonH <= mouseY <= lowerButtonH:
            app.hardColor = rgb(196, 180, 98)
        elif app.width-100 <= mouseX <= app.width and app.height-50 <= mouseY <= app.height:
            app.helpColor = rgb(201, 112, 105)
        else:
            app.easyColor = 'orange'
            app.hardColor = 'orange'
            app.helpColor = rgb(194, 62, 52)
    
    if app.help == True:
        if app.width//2-50 <= mouseX <= app.width//2+50 and app.height-75 <= mouseY <= app.height-25:
            app.backColor = rgb(189, 223, 242)
        else:
            app.backColor = rgb(118, 174, 245)
    
def onStep(app):
    if app.start == True and app.startCountDown == True:
        app.countDownCounter += 1
        if 0 <= app.countDownCounter <= (app.stepsPerSecond*3):
            app.startCountDown = True
        else:
            app.startCountDown = False
    elif app.start == True and app.startCountDown == False:
        scoring(app)
        bestScore(app)
        if collisionDetect(app) == False:
            app.currTime += 0.5
            for player in app.player: # update bird
                if app.ascend == True:
                    dy = 10 # keep changing
                    dy += 8
                    player.cy -= dy
                    player.updateMouthWingEye(-dy)
                    if app.currTime == 2:
                        app.ascend = False # Stops ascending motion
                player.cy += acceleration(app)
                player.updateMouthWingEye(acceleration(app))
            updateTrees(app)
            if app.hard == True:
                if app.score >= 0:
                    app.objectCounter += 1
                    implementAward(app)
                    awardOperation(app)
                    implementBadBird(app)
                    badBirdOperation(app)
                    
def updateTrees(app):
    app.upTopLeft -= app.shift
    app.bottomTopLeft -= app.shift
    if app.upTopLeft == -app.treeWidth:
        app.upTopLeft = 4 * app.treeWidth
        app.upTreeHeight.pop(0)
        app.upTreeHeight.append(random.randrange(150,250))
    if app.bottomTopLeft == -app.treeWidth:
        app.bottomTopLeft = 4 * app.treeWidth
        app.bottomTreeHeight.pop(0)
        if app.easy == True:
            app.bottomTreeHeight.append(random.randrange(400,450)-app.upTreeHeight[4]) 
    # Hard Version
        elif app.hard == True:
            app.bottomTreeHeight.append(random.randrange(400,450)-app.upTreeHeight[4]) 

def implementAward(app):
    if app.objectCounter % 60 == 0:
        cx = app.width
        cy = random.randrange(app.height//2-100,app.height//2+100)
        award = Award(cx,cy)
        app.award.append(award)
        app.awardDict[award] = len(app.award)-1 # Its index in the list.
        
def implementBadBird(app):
    if app.objectCounter % 60 == 0:
        cx = app.width
        cy = random.choice([200,400])
        badBird = BadBird(cx,cy)
        app.badBird.append(badBird)
        app.badDict[badBird] = len(app.badBird)-1    
        
def awardOperation(app):
    for award in app.award:
        award.motion()
        if awardCollision(app):
            app.score += 5
            awardIndex = app.awardDict[award]
            app.award.pop(awardIndex)
            app.awardDict.pop(award)
            for award in app.award:
                if app.awardDict[award] > awardIndex: # Behind the popped item
                    app.awardDict[award] -= 1 # shifting all indexes to the left by 1.

def badBirdOperation(app):
    for badBird in app.badBird:
        badBird.motion()
        badBird.updateMouthWingEye(-8)
        if badBirdCollision(app):
            for player in app.player: # The player bird will become bigger if it hits a bad bird.
                player.radius += 1
                player.mouthRX += 2
                player.mouthRY += 2
                player.wingRX += 2
                player.wingRY += 2
            badIndex = app.badDict[badBird]
            app.badBird.pop(badIndex)
            app.badDict.pop(badBird)
            for badBird in app.badBird:
                if app.badDict[badBird] > badIndex:
                    app.badDict[badBird] -= 1

def main():
    runApp(width=800,height=600)
    
main()

#Citations:
# 1. Background Music: https://www.chosic.com/download-audio/58136/
# 2. Other sounds (Bird-bouncing sound, startGameMusic, and gameOverMusic): https://mixkit.co/free-sound-effects/game/
# 3. Sound algorithm: from Piazza tech demo @2147 post https://piazza.com/class/lkq6ivek5cg1bc/post/2147

