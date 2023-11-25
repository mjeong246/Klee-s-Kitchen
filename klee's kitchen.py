from math import e
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import queue
import random
import math
import time

#CITATIONS FOR IMAGES/CODE: https://docs.google.com/document/d/1lqUpVGEs9GbbKtsAodqEuTjNL7y4yGyBM8FSvEwKCT4/edit 

def getGridLocation(x,y,app):
     row = int(y//app.rowWidth)
     col = int(x//app.colWidth)
     return (row,col)
    
def atEnd(path,finalPosition):
    if path[-1] == finalPosition:
        return True

def canMakeMove(environment,newCoordinate):
    #simply check if the new coordinate is in the environment
    rows = len(environment)
    cols = len(environment[0])
    r,c = newCoordinate
    if (r<0 or r>=rows or c<0 or c>=cols or environment[r][c] != None):
        return False
    return True

#inspired from general BFS ALG: https://www.youtube.com/watch?v=hettiSrJjM4   
def findShortestPath(initialPosition,finalPosition,environment):
    coordinates = queue.Queue()
    coordinates.put([initialPosition])
    path = [initialPosition]

    while not atEnd(path,finalPosition):
        # print(coordinates.queue)
        path = coordinates.get() #Gets a path from the queue
        # print(path)
        for drow,dcol in [(-1,0),(1,0),(0,-1),(0,1)]: #up, down, left, right
            # print(drow,dcol)
            lastRow,lastCol = path[-1]
            newRow = lastRow + drow
            newCol = lastCol + dcol
            newCoordinate = (newRow,newCol)
            if canMakeMove(environment,newCoordinate):
                newPath = path + [(newCoordinate)]
                coordinates.put(newPath)
    return path

class Ingredient():
    def __init__(self):
        self.choppingState = 0 #from 0 to 100, how complete is the chopping process
        self.cookingState = 0 #time since put on a pan
        self.timeSinceCookingStarted = None
        self.previousTotalTimeCooking = 0
        self.totalTimeCooking = 0
        self.chopped = False
        self.cooked = False
    
    def increaseCookingTime(self):
        if self.timeSinceCookingStarted != None:
            currentTime = time.time()
            timeElapsed = (currentTime - self.timeSinceCookingStarted)
            self.totalTimeCooking = self.previousTotalTimeCooking + timeElapsed

    def draw(self,app,x,y,canvas):
        if self.chopped == False:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.rawImage))
            # canvas.create_text(x,y,text=f"Chopping state:{self.choppingState}")
        elif self.cooked == True:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.cookedImage))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.choppedImage))
            # canvas.create_text(x,y,text=f"Cooking state:{self.cookingState}")

        #if self.cooked == True
    def __eq__(self,other):
        return (type(self) == type(other)) and (self.chopped == other.chopped and self.cooked == other.cooked)

class Tomato(Ingredient):
    def __init__(self,app):
        super().__init__()
        self.rawImage = app.loadImage("Dishes/tomatoImageTransparent.png")
        self.rawImage = app.scaleImage(self.rawImage, 1/6)
        self.choppedImage = app.loadImage("Dishes/choppedTomatoTransparent.png")
        self.choppedImage = app.scaleImage(self.choppedImage, 1/6)
        self.cookedImage = app.loadImage("Dishes/tomato sauce.png")
        self.cookedImage = app.scaleImage(self.cookedImage, 1/25)
    
    def __repr__(self):
        return f"Tomato,chopped={self.chopped},cooked={self.cooked}"

class Lettuce(Ingredient):
    def __init__(self,app):
        super().__init__()
        self.rawImage = app.loadImage("Dishes/cabbageImage.png")
        self.rawImage = app.scaleImage(self.rawImage, 1/4)
        self.choppedImage = app.loadImage("Dishes/cabbage chopped image.png")
        self.choppedImage = app.scaleImage(self.choppedImage, 1/6)
    
    def __repr__(self):
        return f"Lettuce,chopped={self.chopped}"

class Pasta(Ingredient):
    def __init__(self,app):
        super().__init__()
        self.rawImage = app.loadImage("Dishes/pastaImage.png")
        self.rawImage = app.scaleImage(self.rawImage, 1/6)
        self.cookedImage = app.loadImage("Dishes/pastaImage.png")
        self.cookedImage = app.scaleImage(self.cookedImage, 1/6)
        self.cookingState = 0 #from 0 to 100, how complete is the cooking process
        self.cooked = False
    
    def draw(self,app,x,y,canvas):
        if self.cooked == False:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.rawImage))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.cookedImage))
    
    def __repr__(self):
        return f"pasta,cooked={self.cooked}"

class Fish(Ingredient):
    def __init__(self,app):
        super().__init__()
        self.rawImage = app.loadImage("Dishes/raw fish image.png")
        self.rawImage = app.scaleImage(self.rawImage, 1/6)
        self.cookedImage = app.loadImage("Dishes/cooked fish image.png")
        self.cookedImage = app.scaleImage(self.cookedImage, 1/6)
        self.cookingState = 0 #from 0 to 100, how complete is the cooking process
        self.cooked = False
    
    def draw(self,app,x,y,canvas):
        if self.cooked == False:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.rawImage))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.cookedImage))
    
    def __repr__(self):
        return f"fish,cooked={self.cooked}"

class Bread(Ingredient):
    def __init__(self,app):
        super().__init__()
        self.rawImage = app.loadImage("Dishes/bread uncooked.png")
        self.rawImage = app.scaleImage(self.rawImage, 1/3)
        self.cookedImage = app.loadImage("Dishes/TOAST.png")
        self.cookedImage = app.scaleImage(self.cookedImage, 1/3)
        self.cookingState = 0 #from 0 to 100, how complete is the cooking process
        self.cooked = False
    
    def draw(self,app,x,y,canvas):
        if self.cooked == False:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.rawImage))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.cookedImage))
    
    def __repr__(self):
        return f"fish,cooked={self.cooked}"

class Equipment():
    def __repr__(self):
        return "Equipment"

class Pan(Equipment):
    def __init__(self,app):
        self.image = app.loadImage("equipment/pan.png")
        self.image = app.scaleImage(self.image,1/5)
        self.container = None
        self.acceptedTypes = [app.choppedTomato,app.rawFish,app.rawBread]

    def draw(self,app,x,y,canvas):
        if self.container == None:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.image))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.image))
            self.container.draw(app,x,y-15,canvas)
    
    def canAccept(self,possibleIngredient):
        return possibleIngredient in self.acceptedTypes
    
    def __repr__(self):
        return f"Pan:{self.container}"

class Pot(Equipment):
    def __init__(self,app):
        self.image = app.loadImage("Dishes/potofwater.png")
        self.image = app.scaleImage(self.image,1/6)
        self.container = None
        self.acceptedTypes = [app.rawPasta]

    def draw(self,app,x,y,canvas):
        if self.container == None:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.image))
        else:
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.image))
            self.container.draw(app,x,y-15,canvas)
    
    def canAccept(self,possibleIngredient):
        return (possibleIngredient in self.acceptedTypes)
    
    def __repr__(self):
        return f"Pot:{self.container}"
    
def ingredientNotInRecipe(ingredient,recipe):
    for item in recipe:
        if item == ingredient:
            return False
    return True

def canCompleteRecipe(subset,recipe):
    for ingredient in subset:
        if ingredientNotInRecipe(ingredient,recipe):
            return False
    return True

def isSubsetOfaRecipe(subset,recipes):
    for recipe in recipes:
        if canCompleteRecipe(subset,recipe):
            return True
    return False

def ingredientNotInGroup(ingredient,ingredientGroup):
    for x in ingredientGroup:
        if ingredient == x:
            return False
    return True

def ingredientGroupsEqual(ingredientGroup1,ingredientGroup2):
    if len(ingredientGroup1) != len(ingredientGroup2):
        return False
    for ingredient in ingredientGroup1:
        if ingredientNotInGroup(ingredient,ingredientGroup2): 
            return False
    return True

class Dish():
    def __init__(self,app):
        self.recipes = [[app.cookedTomato, app.cookedPasta], [app.choppedTomato, app.choppedLettuce],[app.cookedBread,app.cookedFish]] #spaghetti, salad, fish toast
        self.plateImage = app.loadImage("Dishes/plateTransparent.png")
        self.plateImage = app.scaleImage(self.plateImage,1/7) #I CHANGED THIS
        self.spaghettiImage = app.loadImage("Dishes/spaghettiDishes.png")
        self.spaghettiImage = app.scaleImage(self.spaghettiImage,1/6)
        self.saladImage = app.loadImage("Dishes/salad photo.png")
        self.saladImage = app.scaleImage(self.saladImage,1/4)
        self.onlyCookedTomatoImage = app.loadImage("Dishes/tomato sauce.png")
        self.onlyCookedTomatoImage = app.scaleImage(self.onlyCookedTomatoImage, 1/25)
        self.onlyChoppedTomatoImage = app.loadImage("Dishes/choppedTomatoTransparent.png")
        self.onlyChoppedTomatoImage = app.scaleImage(self.onlyChoppedTomatoImage,1/6)

        self.onlyChoppedLettuceImage = app.loadImage("Dishes/cabbage chopped image.png")
        self.onlyChoppedLettuceImage = app.scaleImage(self.onlyChoppedLettuceImage,1/6)

        self.onlyPastaImage =  app.loadImage("Dishes/pastaImage.png")
        self.onlyPastaImage = app.scaleImage(self.onlyPastaImage, 1/6)
        self.onlyCookedBreadImage = app.loadImage("Dishes/TOAST.png")
        self.onlyCookedBreadImage = app.scaleImage(self.onlyCookedBreadImage, 1/3)
        self.onlyCookedFishImage = app.loadImage("Dishes/cooked fish image.png")
        self.onlyCookedFishImage = app.scaleImage(self.onlyCookedFishImage, 1/6)
        self.fishToastImage = app.loadImage("Dishes/fish toast.png")
        self.fishToastImage = app.scaleImage(self.fishToastImage, 1/3)

        self.container = []
        self.acceptedTypes = [app.cookedTomato,app.choppedTomato,app.cookedPasta,app.choppedLettuce,app.cookedFish]
        self.done = False
        self.meal = None

    def draw(self,app,x,y,canvas):
        #draw the plate
        canvas.create_image(x,y,image=ImageTk.PhotoImage(self.plateImage))
        #draw what's on the plate
        if ingredientGroupsEqual(self.container,[app.choppedTomato]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyChoppedTomatoImage))
        elif ingredientGroupsEqual(self.container,[app.cookedTomato]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyCookedTomatoImage))
        elif ingredientGroupsEqual(self.container,[app.cookedPasta]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyPastaImage))
        elif ingredientGroupsEqual(self.container,[app.cookedPasta,app.cookedTomato]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.spaghettiImage))
        elif ingredientGroupsEqual(self.container,[app.choppedLettuce,app.choppedTomato]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.saladImage))
        elif ingredientGroupsEqual(self.container,[app.cookedBread]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyCookedBreadImage))
        elif ingredientGroupsEqual(self.container,[app.cookedBread,app.cookedFish]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.fishToastImage))
        elif ingredientGroupsEqual(self.container,[app.cookedFish]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyCookedFishImage))
        elif ingredientGroupsEqual(self.container,[app.choppedLettuce]):
            canvas.create_image(x,y,image=ImageTk.PhotoImage(self.onlyChoppedLettuceImage))

    def canAdd(self,ingredient):
        if ingredient in self.container:
            return False
        self.container.append(ingredient)
        if isSubsetOfaRecipe(self.container,self.recipes):
            self.container.pop()
            return True 
        else:
            self.container.pop()
            return False
    
    def addIngredient(self,app,ingredient):
        self.container.append(ingredient)
        if ingredientGroupsEqual(self.container,[app.cookedTomato,app.cookedPasta]):
            self.done = True 
            self.meal = Spaghetti(app)
        elif ingredientGroupsEqual(self.container,[app.choppedTomato,app.choppedLettuce]):
            self.done = True
            self.meal = Salad(app)
        elif ingredientGroupsEqual(self.container,[app.cookedFish,app.cookedBread]):
            self.done = True
            self.meal = Fishtoast(app)
        
    def __repr__(self):
        return f"Dish with {self.container}"

class Ash():
    def __init__(self,app):
        self.ashImage = app.loadImage("fires/ashes transparent image.png")
        self.ashImage = app.scaleImage(self.ashImage,1/10)
    def draw(self,app,x,y,canvas):
        canvas.create_image(x,y,image=ImageTk.PhotoImage(self.ashImage))

class FireExtinguisher():
    def __init__(self,app):
        self.FireExtinguisherImage = app.loadImage("fires/fire extinguisher image.png")
        self.FireExtinguisherImage = app.scaleImage(self.FireExtinguisherImage,1/4)
    def draw(self,app,x,y,canvas):
        canvas.create_image(x,y,image=ImageTk.PhotoImage(self.FireExtinguisherImage))
    
class fullMeals():
    def __init__(self):
        self.timeCreated = time.time()
        self.totalTime = 0
    def drawRecipeCard(self,app,x,y,timeLeft,startingTime,canvas):
        canvas.create_image(x,y,image=ImageTk.PhotoImage(self.recipeCardImage))
        barCX = x+10
        barCY = y+46
        halfWidth = 50
        barWidth = 80
        canvas.create_rectangle(barCX-halfWidth,barCY-5,(barCX-halfWidth)+barWidth*(timeLeft/startingTime),barCY+5,fill="green")
        canvas.create_rectangle(barCX-halfWidth,barCY-5,(barCX-halfWidth)+barWidth,barCY+5,outline="black")

class Spaghetti(fullMeals):
    def __init__(self,app):
        super().__init__()
        self.recipe = [app.cookedTomato, app.cookedPasta]
        self.recipeCardImage = app.loadImage("Dishes/spaghetti recipe card.png")
        self.recipeCardImage= app.scaleImage(self.recipeCardImage,1/4)
        self.expiryTime = app.spaghettiExpiryTime
        self.timeLeft = self.expiryTime
    def __repr__(self):
        return "Spaghetti"

class Salad(fullMeals):
    def __init__(self,app):
        super().__init__()
        self.recipe = [app.choppedTomato, app.choppedLettuce]
        self.recipeCardImage = app.loadImage("Dishes/salad recipe card purple.png")
        self.recipeCardImage= app.scaleImage(self.recipeCardImage,1/4)
        self.expiryTime = app.saladExpiryTime
        self.timeLeft = self.expiryTime
    def __repr__(self):
        return "Salad"

class Fishtoast(fullMeals):
    def __init__(self,app):
        super().__init__()
        self.recipe = [app.cookedFish, app.cookedBread]
        self.recipeCardImage = app.loadImage("Dishes/fish toast recipe card image.png")
        self.recipeCardImage= app.scaleImage(self.recipeCardImage,1/4)
        self.expiryTime = app.fishToastExpiryTime
        self.timeLeft = self.expiryTime
    def __repr__(self):
        return "Fish Toast"

def findLocationOfCompletedDish(app,highestPriorityDish):
    #type(app.klee.inventory) == Dish and app.klee.inventory.done == True and type(app.klee.inventory.meal) == type(highestPriorityDish):
    if (type(app.klee.inventory) == Dish) and ingredientGroupsEqual(app.klee.inventory.container,highestPriorityDish.recipe): 
        return app.klee.gridLocation
    for r in range(app.rows):
        for c in range(app.cols):
            item = app.itemLocations[r][c]
            if type(item) == Dish and ingredientGroupsEqual(item.container,highestPriorityDish.recipe):
                return (r,c)
    return None

def findLocationOfUncompleteDish(app,highestPriorityDish):
    if type(app.klee.inventory) == Dish:
        if canCompleteRecipe(app.klee.inventory.container,highestPriorityDish.recipe):
            return app.klee.gridLocation
    for r in range(app.rows):
        for c in range(app.cols):
            item = app.itemLocations[r][c]
            if type(item) == Dish:
                if canCompleteRecipe(item.container,highestPriorityDish.recipe):
                    return (r,c)
    return None

def getRemainingIngredients(uncompletedDish,highestPriorityDish):
    remainingIngredients = []
    for ingredient in highestPriorityDish.recipe:
        if ingredient not in uncompletedDish.container:
            remainingIngredients.append(ingredient)
    return remainingIngredients

def canFurtherProcess(app,ingredientType,possibleIngredient,remainingIngredient):
    for i in range(len(app.Processes[ingredientType])):
        if app.Processes[ingredientType][i][0] == possibleIngredient:
            possibleIngredientIndex = i
        if app.Processes[ingredientType][i][0] == remainingIngredient:
            remainingIngredientIndex = i
    return possibleIngredientIndex <= remainingIngredientIndex

def getPossibleIngredientInInventory(app):
    if isinstance(app.klee.inventory, Ingredient):
        return app.klee.inventory
    elif isinstance(app.klee.inventory,Equipment) and app.klee.inventory.container != None:
        return app.klee.inventory.container
    return None #if there is no ingredient in her inventor

def getNeededVersionOfIngredient(app,possibleIngredient,remainingIngredients):
    for remainingIngredient in remainingIngredients:
        if type(remainingIngredient) == type(possibleIngredient) and canFurtherProcess(app,type(possibleIngredient),possibleIngredient,remainingIngredient):
            return remainingIngredient
    return None

def getPossibleIngredientInEnvironment(app,remainingIngredients):
    for r in range(app.rows):
        for c in range(app.cols):
            if isinstance(app.itemLocations[r][c],Equipment) and app.itemLocations[r][c].container != None:
                currentItem = app.itemLocations[r][c].container
            elif isinstance(app.itemLocations[r][c], Ingredient):
                currentItem = app.itemLocations[r][c]
            else:
                continue
            neededVersionOfIngredient = getNeededVersionOfIngredient(app,currentItem,remainingIngredients)
            if neededVersionOfIngredient != None:
                return (currentItem,(r,c))
    return None #if there is no ingredient in the environment

def getNextProcess(app,possibleIngredient,neededVersionOfIngredient):
    if possibleIngredient == neededVersionOfIngredient:
        return None
    ingredientType = type(possibleIngredient)
    for process in app.Processes[ingredientType]:
        if (possibleIngredient == process[0]): #if it's already at it's most needed stage, return None
            return process[1]
        
def kitchenHasFire(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.furnitureLocations[row][col] != None and app.furnitureLocations[row][col].onFire == True:
                return True
    return False

def findNearestFireLocation(app):
    closestDistance = None
    closestFireLocation = None
    for row in range(app.rows):
        for col in range(app.cols):
            if app.furnitureLocations[row][col] != None and app.furnitureLocations[row][col].onFire == True:
                kleeX,kleeY = app.klee.gridLocation
                dRow = abs(kleeX-row)
                dCol = abs(kleeY-col)
                distance = dRow+dCol
                if closestDistance == None or distance < closestDistance:
                    closestDistance = distance
                    closestFireLocation = (row,col)
    return closestFireLocation

def findFireExtinguisherLocation(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if (isinstance(app.furnitureLocations[row][col],storingFurniture) 
                and app.furnitureLocations[row][col].container != None and
                type(app.furnitureLocations[row][col].container) == FireExtinguisher):
                return (row,col)

def findNextDestination(app):
    #if there is a fire
    if kitchenHasFire(app) == True:
        #she already has a fire extinguisher
        if type(app.klee.inventory) == FireExtinguisher:
            return findNearestFireLocation(app)
        else:  #she doesn't already have a fire extinguisher
            return findFireExtinguisherLocation(app)

    #find the highest priority dish on the queue
    highestPriorityDish = app.orderQueue.lineUp[0]
    #check if there's already a completed dish in the environment
    completedDishLocation = findLocationOfCompletedDish(app,highestPriorityDish)
    if completedDishLocation != None:
        if completedDishLocation == app.klee.gridLocation:
            return app.servingStation.gridLocation
        else:
            return completedDishLocation

    #if there's an empty/half completed dish that is on its way to a high priority dish
    uncompletedDishLocation = findLocationOfUncompleteDish(app,highestPriorityDish)
    if uncompletedDishLocation != None:
        #klee has the uncompleted dish in her hands
        if uncompletedDishLocation == app.klee.gridLocation: 
            return app.counter2.gridLocation #FIND AN EMPTY COUNTER
        #find the ingredients that you need to complete the dish
        uncompletedDishLocationR, uncompletedDishLocationC = uncompletedDishLocation
        uncompletedDish = app.itemLocations[uncompletedDishLocationR][uncompletedDishLocationC]
        remainingIngredients = getRemainingIngredients(uncompletedDish,highestPriorityDish)

        #get whatever ingredient might be in Klee's inventory
        possibleIngredient = getPossibleIngredientInInventory(app)
        if possibleIngredient != None:
            neededVersionOfIngredient = getNeededVersionOfIngredient(app,possibleIngredient,remainingIngredients)
            if neededVersionOfIngredient != None: #if it returns none then there was no possible needed version of that ingredient
                nextProcess = getNextProcess(app,possibleIngredient,neededVersionOfIngredient)
                if nextProcess == "Chop":
                    return app.choppingTable1.gridLocation
                elif nextProcess == "Cook":
                    return app.stoveTop1.gridLocation
                elif nextProcess == "Boil":
                    return app.stoveTop3.gridLocation
                elif nextProcess == None:
                    return uncompletedDishLocation

        #if there is no possible ingredient in her inventory, look in the kitchen environmnet
        possibleIngredientAndLocation = getPossibleIngredientInEnvironment(app,remainingIngredients) #get whatever ingredient might be in the kitchen environment
        print(possibleIngredientAndLocation)
        if possibleIngredientAndLocation != None:
            possibleIngredient, possibleIngredientLocation, = possibleIngredientAndLocation
            # neededVersionOfIngredient = getNeededVersionOfIngredient(app,possibleIngredient,remainingIngredients)
            # if neededVersionOfIngredient != None:
            return possibleIngredientLocation
        else:
            return app.fridge.gridLocation  
    else:
        return app.tableWithPlates.gridLocation

class Klee():
    def __init__(self,x,y,app):
        #setting the current orientation of Klee
        self.x = x
        self.y = y
        self.xBoundary = 10
        self.yBoundary = 30
        self.direction = "Down"
        self.previousDirection = "Down"
        self.inventory = None
        self.currentNearObject = None
        self.gridLocation = (5,6)
        #creating a list of Klee's animation sprites
        #sprites taken from: https://www.deviantart.com/chiibits/art/Klee-Walking-Sprite-872586364  
        #sprite sheet generated by: https://codeshack.io/images-sprite-sheet-generator/  
        spritestrip = app.loadImage("kleeAnimations/kleespritesheet.png")
        self.sprites = []
        self.forwardSprites = []
        self.backwardSprites = []
        self.rightSprites = []
        self.leftSprites = []
        self.acceleration = 1
        self.timeSinceLastKeyPressed = 0
        self.timeSinceLastKeyReleased = 0
        self.inventory = None

        for i in range(12):
            left = i*800
            top = 0
            right = (i+1)*800
            bottom = 800
            sprite = spritestrip.crop((left,top,right,bottom))
            self.sprites.append(sprite)
        for i in range(len(self.sprites)):
            self.sprites[i] = app.scaleImage(self.sprites[i], 1/6)
        for i in [1,2]:
            self.backwardSprites.append(self.sprites[i])
            self.backwardSprites.append(self.sprites[i])
            self.backwardSprites.append(self.sprites[i])
            self.backwardSprites.append(self.sprites[i]) #added
        for i in [4,5]:
            self.forwardSprites.append(self.sprites[i])
            self.forwardSprites.append(self.sprites[i])
            self.forwardSprites.append(self.sprites[i])
            self.forwardSprites.append(self.sprites[i]) #added
        for i in [7,8]:
            self.rightSprites.append(self.sprites[i])
            self.rightSprites.append(self.sprites[i])
            self.rightSprites.append(self.sprites[i])
            self.rightSprites.append(self.sprites[i]) #added
        for i in [10,11]:
            self.leftSprites.append(self.sprites[i])
            self.leftSprites.append(self.sprites[i])
            self.leftSprites.append(self.sprites[i])
            self.leftSprites.append(self.sprites[i]) #added
        self.currentSprite = self.sprites[0]
        self.currentSpriteIndex = 0

    #makes sure that klee does not go thorugh a piece of furniture
    def isMoveLegalHelper(self,other,dx,dy):
        newBottom = (self.y+dy)+self.yBoundary+20
        newTop = (self.y+dy)-self.yBoundary
        newLeft = (self.x+dx)-self.xBoundary
        newRight = (self.x+dx)+self.xBoundary
        objBottom = other.y+other.yBoundary
        objTop = other.y-other.yBoundary
        objLeft = other.x-other.xBoundary
        objRight = other.x+other.xBoundary
        if (((objTop<=newBottom<=objBottom) or (objTop<=newTop<=objBottom)) and 
           ((objLeft<=newLeft<=objRight) or (objLeft<=newRight<=objRight))):
           return False
        return True

    def isMoveLegal(self,dx,dy,app):
        newX = self.x + dx
        newY = self.y + dy 
        if (newX < 0 or newX > app.width or
            newY < 0 or newY > app.height):
            return False
        for furniture in app.furniture:
            if self.isMoveLegalHelper(furniture,dx,dy) == False:
                return False
        return True

    def move(self,app):
        #if it changes direction, reset acceleraiton to 1
        if self.previousDirection != self.direction:
            self.acceleration = 1
            self.currentSpriteIndex = 0
        else:
            #if the player had been holding the key, continue to  increase acceleration
            if self.timeSinceLastKeyPressed <= 10:
                self.acceleration += 0.1
            #if the player released the key, set the acceleration back to 1
            elif self.timeSinceLastKeyPressed >= 200:
                self.acceleration = 1
            self.currentSpriteIndex = (self.currentSpriteIndex+1)%8 #used to be two
        if self.direction == "Up":
            if self.isMoveLegal(0,-10*self.acceleration,app):
                self.y -= 10*self.acceleration
            self.currentSprite = self.forwardSprites[self.currentSpriteIndex]
            self.previousDirection = self.direction
        elif self.direction == "Down":
            if self.isMoveLegal(0,10*self.acceleration,app):
                self.y += 10*self.acceleration
            self.currentSprite = self.backwardSprites[self.currentSpriteIndex]
            self.previousDirection = self.direction
        elif self.direction == "Left":
            if self.isMoveLegal(-10*self.acceleration,0,app):
                self.x -= 10*self.acceleration
            self.currentSprite = self.leftSprites[self.currentSpriteIndex]
            self.previousDirection = self.direction
        elif self.direction == "Right":
            if self.isMoveLegal(10*self.acceleration,0,app):
                 self.x += 10*self.acceleration
            self.currentSprite = self.rightSprites[self.currentSpriteIndex]
            self.previousDirection = self.direction
        
        #get her current grid location
        self.gridLocation = getGridLocation(self.x,self.y,app)

    def checkIfNearInteractiveFurniture(self,interactiveFurniture):
        for object in interactiveFurniture:
            objBottom = object.y+object.yBoundary
            objTop = object.y-object.yBoundary
            objLeft = object.x-object.xBoundary
            objRight = object.x+object.xBoundary
            playerBottom = self.y+self.yBoundary
            playerTop = self.y-self.yBoundary
            playerLeft = self.x-self.xBoundary
            playerRight = self.x+self.xBoundary
            #for klee to be near an interactive object we need at least: 
            # 1) one of her borders to be really close to one of the object's borders
            for i in [objBottom,objTop]:
                for j in [playerBottom,playerTop]:
                    distance = abs(i-j)
                    if distance <= 50:
                        #check if one of the player's vertical borders are in between the object's vertical borders
                        if (objLeft<=playerLeft<=objRight) or (objLeft<=playerRight<=objRight):
                            self.currentNearObject = object
                            return
            for i in [objLeft,objRight]:
                for j in [playerLeft,playerRight]:
                    distance = abs(i-j)
                    if distance <= 50:
                        #check if one of the player's horizontal borders are in between the object's horizontal borders
                        if (objTop<=playerBottom<=objBottom) or (objTop<=playerTop<=objBottom):
                            self.currentNearObject = object
                            return
            self.currentNearObject = None

    def draw(self,canvas):
        canvas.create_image(self.x, self.y, 
                        image=ImageTk.PhotoImage(self.currentSprite))

class Furniture():
    def __init__(self,app,x,y,image,xBoundary,yBoundary,gridLocation):
        self.x = x
        self.y = y
        self.image = image
        self.onFire = False
        self.xBoundary = xBoundary
        self.yBoundary = yBoundary
        self.gridLocation = gridLocation
        self.fireSpriteStrip = app.loadImage("startscreen/fire.png")
        self.fireSprites = []
        self.fireSpriteIndex = 0
        self.onFire = False
        self.dousingState = 0
        for i in range(4):
            left = i*170
            top = 0
            right = (i+1)*170
            bottom = 153
            sprite = self.fireSpriteStrip.crop((left,top,right,bottom))
            self.fireSprites.append(sprite)
    
    def draw(self,app,canvas):
        canvas.create_image(self.x, self.y, 
                        image=ImageTk.PhotoImage(self.image))
        #draw out the borders
        # canvas.create_rectangle(self.x-self.xBoundary,
        #                     self.y-self.yBoundary,
        #                     self.x+self.xBoundary,
        #                     self.y+self.yBoundary,
        #                     outline="red")
        if self.onFire == True:
            canvas.create_image(self.x,self.y-70,image=ImageTk.PhotoImage(self.fireSprites[self.fireSpriteIndex]))
            # canvas.create_text(self.x,self.y,text=f"Dousing state: {self.dousingState}")
            if 0 < self.dousingState < 100: 
                canvas.create_rectangle(self.x-50,self.y-5,(self.x-50)+100*(self.dousingState/100),self.y+5,fill="blue")
                canvas.create_rectangle(self.x-50,self.y-5,self.x+50,self.y+5,outline="black")
        
#all the furniture that klee can interact with 
class interactiveFurniture(Furniture):
    def __init__(self,app,x,y,image,xBoundary,yBoundary,popUp,gridLocation):
        super().__init__(app,x,y,image,xBoundary,yBoundary,gridLocation)
        #the thing that pops up when klee goes near it
        self.popUp = popUp

    def draw(self,app,canvas):
        super().draw(app,canvas)

        if app.klee.currentNearObject == self: 
            canvas.create_text(self.x,self.y+10,text=self.popUp,font=30)

        # canvas.create_rectangle(self.x-self.xBoundary,
        #                          self.y-self.yBoundary,
        #                          self.x+self.xBoundary,
        #                          self.y+self.yBoundary,
        #                          outline="red")

class storingFurniture(interactiveFurniture):
    def __init__(self,app,x,y,image,xBoundary,yBoundary,popUp,gridLocation):
        super().__init__(app,x,y,image,xBoundary,yBoundary,popUp,gridLocation)
        self.container = None
    
    def addItemToContainer(self,app,item):
        r,c = self.gridLocation
        app.itemLocations[r][c] = item
        self.container = item
        # print2dList(app.itemLocations)
    
    def removeItemFromContainer(self,app):
        self.container = None
        r,c = self.gridLocation
        app.itemLocations[r][c] = None
        # print2dList(app.itemLocations)

    def draw(self,app,canvas):
        super().draw(app,canvas)
        if self.container != None:
            self.container.draw(app,self.containerX,self.containerY,canvas)

class ChoppingTable(storingFurniture):
    def __init__(self,app,x,y,image,xBoundary,yBoundary,popUp,gridLocation):
        super().__init__(app,x,y,image,xBoundary,yBoundary,popUp,gridLocation)
        self.containerX = self.x
        self.containerY = self.y - 20
        self.acceptedTypes = [type(None),Tomato,Lettuce]
    
    def draw(self,app,canvas):
        super().draw(app,canvas)
        if self.container != None and (type(self.container) != Ash):
            self.container.draw(app,self.containerX,self.containerY,canvas)
            if (0 < self.container.choppingState < 100):
                    canvas.create_rectangle(self.x-50,self.y-5,(self.x-50)+100*(self.container.choppingState/100),self.y+5,fill="green")
                    canvas.create_rectangle(self.x-50,self.y-5,self.x+50,self.y+5,outline="black")


class StoveTop(storingFurniture):
    def __init__(self,app,x,y,image,xBoundary,yBoundary,popUp,equipment,gridLocation):
        super().__init__(app,x,y,image,xBoundary,yBoundary,popUp,gridLocation)
        self.containerX = self.x
        self.containerY = self.y - 20
        self.container = equipment
        self.checkMarkImage = app.loadImage("Dishes/checkmark.png")
        self.checkMarkImage = app.scaleImage(self.checkMarkImage,1/4)
        self.fireWarningImage = app.loadImage("fires/fire warning symbol image.png")
        self.fireWarningImage = app.scaleImage(self.fireWarningImage,1/8)
        self.acceptedTypes = [type(None),Pan,Pot]
        #for the fire
        # self.fireSpriteStrip = app.loadImage("startscreen/fire.png")
        # self.fireSprites = []
        # self.fireSpriteIndex = 0
        # self.onFire = False
        # self.dousingState = 0
        # for i in range(4):
        #     left = i*170
        #     top = 0
        #     right = (i+1)*170
        #     bottom = 153
        #     sprite = self.fireSpriteStrip.crop((left,top,right,bottom))
        #     self.fireSprites.append(sprite)

    def draw(self,app,canvas):
        super().draw(app,canvas)
        if self.container != None:
            self.container.draw(app,self.containerX,self.containerY,canvas)
            if self.container.container != None and type(self.container.container) != Ash: #there is something in the pot 
                if self.container.container.totalTimeCooking <= 15:
                    canvas.create_rectangle(self.x-50,self.y-5,(self.x-50)+100*(self.container.container.totalTimeCooking/15),self.y+5,fill="green")
                    canvas.create_rectangle(self.x-50,self.y-5,self.x+50,self.y+5,outline="black")
                elif (15 < self.container.container.totalTimeCooking <= 40) and (round(self.container.container.totalTimeCooking) % 2 == 0): #% 5 so the checkmark appears periodically
                    canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.checkMarkImage))
                elif (40 < self.container.container.totalTimeCooking <= 50) and (round(self.container.container.totalTimeCooking) % 2 == 0):
                    canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.fireWarningImage))
        # if self.onFire == True:
        #     canvas.create_image(self.x,self.y-70,image=ImageTk.PhotoImage(self.fireSprites[self.fireSpriteIndex]))
        #     # canvas.create_text(self.x,self.y,text=f"Dousing state: {self.dousingState}")
        #     if 0 < self.dousingState < 100: 
        #         canvas.create_rectangle(self.x-50,self.y-5,(self.x-50)+100*(self.dousingState/100),self.y+5,fill="blue")
        #         canvas.create_rectangle(self.x-50,self.y-5,self.x+50,self.y+5,outline="black")

class Counter(storingFurniture):
    def __init__(self,app,x,y,image,xBoundary,yBoundary,popUp,gridLocation):
        super().__init__(app,x,y,image,xBoundary,yBoundary,popUp,gridLocation)
        self.containerX = self.x
        self.containerY = self.y - 25
        self.container = None
        self.acceptedTypes = [Pan,Pot,Tomato,Pasta,Dish,Lettuce,Bread,Fish,FireExtinguisher]

def updateRateUps(app):
    total = 0
    for dish in app.orderQueue.orderProbabilities:
        total += app.orderQueue.orderProbabilities[dish]
    app.saladRateUp = round(((app.orderQueue.orderProbabilities[Salad]/total)-0.33)*100)
    app.spaghettiRateUp = round(((app.orderQueue.orderProbabilities[Spaghetti]/total)-0.33)*100)
    app.fishToastRateUp = round(((app.orderQueue.orderProbabilities[Fishtoast]/total)-0.33)*100)

class foodQueue():
    def __init__(self,app):
        self.availableFoodOrders = ['Spaghetti','Salad','Fishtoast']
        self.orderProbabilities = {Spaghetti: 33, Salad: 33, Fishtoast: 33}
        self.lineUp = []
        self.initiated = False
    def generateOrder(self,app):
        currentProbabilities = []
        for key in self.orderProbabilities:
            currentProbabilities.append(self.orderProbabilities[key])
        currentProbabilities = tuple(currentProbabilities)
        nextFoodOrder = random.choices(self.availableFoodOrders,weights=currentProbabilities)[0]
        if nextFoodOrder == "Spaghetti":
            self.lineUp.append(Spaghetti(app))
        elif nextFoodOrder == "Salad":
            self.lineUp.append(Salad(app))
        elif nextFoodOrder == "Fishtoast":
            self.lineUp.append(Fishtoast(app))
    
    def decreaseTime(self,app):
        for order in self.lineUp:
            currentTime = time.time()
            timeElapsed = currentTime - order.timeCreated
            order.totalTime = timeElapsed
        app.oneSecondDelay = 0
    
    def checkForExpiry(self,app):
        i = 0
        while i < len(self.lineUp):
            if self.lineUp[i].totalTime >= self.lineUp[i].expiryTime:
                #change the probabiliites if on practice mode
                if app.practiceMode == True:
                    dishType = type(self.lineUp[i])
                    app.orderQueue.orderProbabilities[dishType] += 20
                    if dishType == Spaghetti:
                        app.spaghettiExpiryTime += 20
                    elif dishType == Salad:
                        app.saladExpiryTime += 20
                    elif dishType == Fishtoast:
                        app.fishToastExpiryTime += 20
                    updateRateUps(app)
                self.lineUp.pop(i)
                app.score -= 100
            else:
                i += 1
    
    def serveDish(self,app,dish):
        for i in range(len(self.lineUp)):
            if type(self.lineUp[i]) == type(dish):
                self.lineUp.pop(i)
                break
        app.score += 100
    
    def draw(self,app,canvas):
        for i in range(len(self.lineUp)):
            dish = self.lineUp[i]
            dish.drawRecipeCard(app,1354,(i*120)+100,(dish.expiryTime-dish.totalTime),dish.expiryTime,canvas)
        

class countDownTimer():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.started = False
        self.initialTime = time.time()
        self.totalTime = 600
        self.timeElapsed = 0

        self.radius1 = 50
        self.radius2 = 45
    
    def countDown(self):
        currentTime = time.time()
        self.timeElapsed = currentTime-self.initialTime
    def draw(self,canvas):
        canvas.create_oval(self.x-self.radius1,self.y-self.radius1,self.x+self.radius1,self.y+self.radius1,fill="green")
        canvas.create_arc(self.x-self.radius2,self.y-self.radius2,self.x+self.radius2,self.y+self.radius2,start=90,extent=(-self.timeElapsed/self.totalTime)*360,fill="white",style="pieslice")

class practiceButton():
    def __init__(self,image,hoverImage,x,y):
        self.x = x
        self.y = y
        self.image = image
        self.hoverImage = hoverImage
        self.left = self.x-(self.image.width//2)
        self.right = self.x+(self.image.width//2)
        self.top = self.y-(self.image.height//2)
        self.bottom = self.y+(self.image.height//2)

    def mouseHoveringOver(self,app):
        if (self.left <= app.mouseX <= self.right) and (self.top<= app.mouseY <=self.bottom):
            return True
    
    def checkIfClicked(self,app,clickX,clickY):
        if (self.left <= clickX <= self.right) and (self.top<= clickY <=self.bottom):
            return True
        
    def draw(self,app,canvas):
        if self.mouseHoveringOver(app):
            if app.paused == False:
                canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.hoverImage))
        else:
            canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.image))

class hintButton():
    def __init__(self,app,x,y):
        self.dodocoImage = app.loadImage("hint/hint button image.png")
        self.dodocoImage = app.scaleImage(self.dodocoImage,1/3)
        self.x = x
        self.y = y
        self.step = 0
        self.left = self.x-(self.dodocoImage.width//2)
        self.right = self.x+(self.dodocoImage.width//2)
        self.top = self.y-(self.dodocoImage.height//2)
        self.bottom = self.y+(self.dodocoImage.height//2)

    def mouseHoveringOver(self,app):
        if (self.left <= app.mouseX <= self.right) and (self.top<= app.mouseY <=self.bottom):
            return True
    
    def checkIfClicked(self,app,clickX,clickY):
        if (self.left <= clickX <= self.right) and (self.top<= clickY <=self.bottom):
            return True
        
    def draw(self,app,canvas):
        if self.mouseHoveringOver(app):
            if app.paused == False:
                self.y = 734+(-1 * math.sin(self.step) * 20) #idea taken from https://inventwithpython.com/blog/2012/07/18/using-trigonometry-to-animate-bounces-draw-clocks-and-point-cannons-at-a-target/
                self.top = self.y-(self.dodocoImage.height//2)
                self.bottom = self.y+(self.dodocoImage.height//2)
            canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.dodocoImage))
            self.step += 1
        else:
            self.y = 734
            self.top = self.y-(self.dodocoImage.height//2)
            self.bottom = self.y+(self.dodocoImage.height//2)
            self.step = 0
            canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.dodocoImage))

class Primogem():
    def __init__(self,app,x,y):
        self.image = app.loadImage("gameover/primogem.png")
        self.image = app.scaleImage(self.image,3/8)
        self.x = x
        self.y = y
    def draw(self,app,canvas):
        canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.image))

def appStarted(app):
    app.step = 0
    app.paused = False
    app.practiceMode = False
    app.mode = "splashScreenMode"
    app.startScreenImage = app.loadImage("startscreen/startscreen.jpg")
    app.fire1 = startFire(app,185,550)
    app.fire2 = startFire(app,1250,550)
    app.fires = []
    app.fires.extend([app.fire1,app.fire2])
    app.startButtons = []
    app.startButtonImage = app.loadImage("startscreen/start button image.jpg")
    app.startButtonHoverImage = app.loadImage("startscreen/start button image hover.jpg")
    app.startButton = Button(app.startButtonImage,app.startButtonHoverImage,708,665,153,43,"gameMode")
    app.startButtons.extend([app.startButton])

    #gameover screen
    app.gameoverButtons = []
    app.restartButtonImage = app.loadImage("gameover/restart button image transparent.png")
    app.restartButtonImage = app.scaleImage(app.restartButtonImage,1/3)
    app.restartButtonHoverImage = app.loadImage("gameover/restart button hover image.png")
    app.restartButtonHoverImage = app.scaleImage(app.restartButtonHoverImage,1/3)
    app.restartButton = RestartButton(app.restartButtonImage,app.restartButtonHoverImage,443,680,160,45,"gameMode")
    app.menuButtonImage = app.loadImage("gameover/menu button image.png")
    app.menuButtonImage = app.scaleImage(app.menuButtonImage,1/3)
    app.menuButtonHoverImage = app.loadImage("gameover/menu button hover image.png")
    app.menuButtonHoverImage = app.scaleImage(app.menuButtonHoverImage,1/3)
    app.menuButton = MenuButton(app.menuButtonImage,app.menuButtonHoverImage,1000,680,160,45,"splashScreenMode")
    app.gameoverButtons.extend([app.restartButton,app.menuButton])
    app.gameOverTextImage = app.loadImage("gameover/game over text image.png")
    primogem1 = Primogem(app,app.width+100,app.height//2+80)
    primogem2 = Primogem(app,app.width+100,app.height//2+80)
    primogem3 = Primogem(app,app.width+100,app.height//2+80)
    app.primogems = [primogem1,primogem2,primogem3]
    app.starsDrawn = [True,True,True]

    #pause screen
    app.pauseButtons = []
    app.pausePopupImage = app.loadImage("pausescreen/PAUSE SCREEN TRANSPARENT.png")
    app.pauseRestartButton = RestartButton(app.restartButtonImage,app.restartButtonHoverImage,551,549,160,45,"gameMode")
    app.pauseMenuButton = MenuButton(app.menuButtonImage,app.menuButtonHoverImage,900,549,160,45,"splashScreenMode")
    app.pauseButtons.extend([app.pauseRestartButton,app.pauseMenuButton])

    #fires
    app.timeSinceLastFireSpread = 0

    #countdown timer
    app.countDownT = countDownTimer(78,65)

    #hint button
    app.hintButton = hintButton(app,1043,734)
    app.timePassed = 0
    app.timeSinceHintKeyPressed = 0

    #practice button
    app.gameButtons = []
    app.practiceButtonImage = app.loadImage("practiceMode/PRACTICE MODE BUTTON IMAGE.png")
    app.practiceButtonImage = app.scaleImage(app.practiceButtonImage,1/6)
    app.practiceButtonHoverImage = app.loadImage("practiceMode/practice mode hover image.png")
    app.practiceButtonHoverImage = app.scaleImage(app.practiceButtonHoverImage,1/6)
    app.practiceButton = practiceButton(app.practiceButtonImage,app.practiceButtonHoverImage,87,570)
    app.gameButtons.append(app.practiceButton)
    
    #expiry times and rate ups
    app.spaghettiExpiryTime = 200
    app.spaghettiRateUp = 0
    app.saladExpiryTime = 200
    app.saladRateUp = 0
    app.fishToastExpiryTime = 200
    app.fishToastRateUp = 0

    # app.floorImage = app.scaleImage(app.floorImage,2)
    #calculate and draw the centers of the grid
    #grid is 9 X 7
    app.score = 0
    app.rows = 7
    app.cols = 9
    app.colWidth = app.width//app.cols
    app.rowWidth = app.height//app.rows
    app.hintMode = False
    # app.rowWidth = app.height//app.rows
    app.environment = [[None]*app.cols for i in range(app.rows)]

    app.environment = [
        [None, 'STOVETOP', 'STOVETOP', 'STOVETOP', 'STOVETOP', 'COUNTER', None, 'FRIDGE', 'FRIDGE'], 
        ['TABLE', None, None, None, None, None, None, 'FRIDGE', 'FRIDGE'], 
        ['TABLE', None, None, None, None, None, None, None, None], 
        ['TABLE', 'CHOP', 'CHOP', 'TABLE', 'TABLE', 'TABLE', None, None, None], 
        [None, None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None, None], 
        ['SERVE', None, 'PLATETABLE', 'TABLE', 'TABLE', 'TABLE', 'HINTBUTTON', 'TRASH',None]
          ]

    #for the hint sysetem
    app.itemLocations = [[None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None],      
                         [None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None]]

    app.hintPath = None
    app.mouseX = 0
    app.mouseY = 0
    app.lastKeyPressed = None
    app.timeSinceLastcKeyPressed = 0
    app.timeSinceLastcKeyReleased = 0
    app.timeSinceLastOrderGenerated = time.time()
    app.oneSecondDelay = 0
    app.klee = Klee(1040,610,app)

    #comparisons 

    app.rawTomato = Tomato(app)

    app.choppedTomato = Tomato(app)
    app.choppedTomato.chopped = True

    app.cookedTomato = Tomato(app)
    app.cookedTomato.cooked = True
    app.cookedTomato.chopped = True

    app.rawLettuce = Lettuce(app)

    app.choppedLettuce = Lettuce(app)
    app.choppedLettuce.chopped = True

    app.rawPasta = Pasta(app)

    app.cookedPasta = Pasta(app)
    app.cookedPasta.cooked = True

    app.rawFish = Fish(app)

    app.cookedFish = Fish(app)
    app.cookedFish.cooked = True

    app.rawBread = Bread(app)

    app.cookedBread = Bread(app)
    app.cookedBread.cooked = True

    app.Processes = {Lettuce: [[app.rawLettuce,"Chop"],[app.choppedLettuce,None]],
                     Tomato:  [[app.rawTomato,"Chop"],[app.choppedTomato,"Cook"],[app.cookedTomato,None]],
                     Pasta:   [[app.rawPasta,"Boil"],[app.cookedPasta,None]],
                     Bread:   [[app.rawBread,"Cook"],[app.cookedBread,None]],
                     Fish:    [[app.rawFish,"Cook"],[app.cookedFish,None]]
                }

    app.orderQueue = foodQueue(app)
    #start off with a single order
    app.orderQueue.generateOrder(app)

    app.furniture = []
    app.interactiveFurniture = []
    app.storingFurniture = []
    app.choppingTables = []
    app.stoveTops = []

    # kitchenTableImage = app.loadImage("Furniture/furniture 1.png")
    # app.kitchenTable = Furniture(493,560,kitchenTableImage,182,40)
    # app.furniture.append(app.kitchenTable)

    fridgeImage = app.loadImage("Furniture/fridgeTransparent.png")
    fridgePopUp = "Press 1 to get tomato\nPress 2 to get pasta\nPress 3 to get lettuce\nPress 4 to get fish\nPress 5 to get bread"
    app.fridge = interactiveFurniture(app,1196,117,fridgeImage,65,110,fridgePopUp,gridLocation=(1,7))
    app.furniture.append(app.fridge)
    app.interactiveFurniture.append(app.fridge)

    tableWithPlatesImage = app.loadImage("Furniture/tableWithPlatesTransparent.png")
    tableWithPlatesImage = app.scaleImage(tableWithPlatesImage,9/16)
    tableWithPlatesPopUp = "Press space to get plate"
    app.tableWithPlates = interactiveFurniture(app,400,741,tableWithPlatesImage,80,80,tableWithPlatesPopUp,gridLocation=(6,2))
    app.furniture.append(app.tableWithPlates)
    app.interactiveFurniture.append(app.tableWithPlates)

    trashImage = app.loadImage("Furniture/trashcanTransparent.png")
    trashImage = app.scaleImage(trashImage, 1/2)
    trashPopUp = "Press c to throw"
    app.trash = interactiveFurniture(app,1200,743,trashImage,46,50,trashPopUp,gridLocation=(6,8))
    app.furniture.append(app.trash)
    app.interactiveFurniture.append(app.trash)

    servingStationImage = app.loadImage("Furniture/servingStationImage.png")
    servingStationImage = app.scaleImage(servingStationImage,1/5)
    servingStationPopUp = "Press c to serve"
    app.servingStation = interactiveFurniture(app,79,743,servingStationImage,60,60,servingStationPopUp,gridLocation=(6,0))
    app.furniture.append(app.servingStation)
    app.interactiveFurniture.append(app.servingStation)

    choppingTableImage = app.loadImage("Furniture/choppingboardTableImage.png")
    choppingTableImage = app.scaleImage(choppingTableImage,1.72)
    choppingTablePopUp = "Press c to chop"
    app.choppingTable1 = ChoppingTable(app,237,399,choppingTableImage,80,80,choppingTablePopUp,gridLocation=(3,1))
    app.furniture.append(app.choppingTable1)
    app.interactiveFurniture.append(app.choppingTable1)
    app.storingFurniture.append(app.choppingTable1)
    app.choppingTables.append(app.choppingTable1)

    app.choppingTable2 = ChoppingTable(app,399,399,choppingTableImage,80,80,choppingTablePopUp,gridLocation=(3,2))
    app.furniture.append(app.choppingTable2)
    app.interactiveFurniture.append(app.choppingTable2)
    app.storingFurniture.append(app.choppingTable2)
    app.choppingTables.append(app.choppingTable2)

    stoveTopImage = app.loadImage("Furniture/stovetopTransparent.png")
    stoveTopImage = app.scaleImage(stoveTopImage,1.7)
    stoveTopPopUp = "cook"

    pan1 = Pan(app)
    app.stoveTop1 = StoveTop(app,239,56,stoveTopImage,80,80,stoveTopPopUp,pan1,gridLocation=(0,1))
    app.itemLocations[0][1] = pan1
    app.furniture.append(app.stoveTop1)
    app.interactiveFurniture.append(app.stoveTop1)
    app.storingFurniture.append(app.stoveTop1)
    app.stoveTops.append(app.stoveTop1)

    pan2 = Pan(app)
    app.stoveTop2 = StoveTop(app,400,56,stoveTopImage,80,80,stoveTopPopUp,pan2,gridLocation=(0,2))
    app.itemLocations[0][2] = pan2
    app.furniture.append(app.stoveTop2)
    app.interactiveFurniture.append(app.stoveTop2)
    app.storingFurniture.append(app.stoveTop2)
    app.stoveTops.append(app.stoveTop2)

    pot1 = Pot(app)
    app.stoveTop3 = StoveTop(app,561,58,stoveTopImage,80,80,stoveTopPopUp,pot1,gridLocation=(0,3))
    app.itemLocations[0][3] = pot1
    app.furniture.append(app.stoveTop3)
    app.interactiveFurniture.append(app.stoveTop3)
    app.storingFurniture.append(app.stoveTop3)
    app.stoveTops.append(app.stoveTop3)

    pot2 = Pot(app)
    app.stoveTop4 = StoveTop(app,722,56,stoveTopImage,80,80,stoveTopPopUp,pot2,gridLocation=(0,4))
    app.itemLocations[0][4] = pot2
    app.furniture.append(app.stoveTop4)
    app.interactiveFurniture.append(app.stoveTop4)
    app.storingFurniture.append(app.stoveTop4)
    app.stoveTops.append(app.stoveTop4)

    counterImage = app.loadImage("Furniture/counter.png")
    counterImage = app.scaleImage(counterImage,0.8)
    counterPopUp = ""
    app.counter1 = Counter(app,880,56,counterImage,80,80,counterPopUp,gridLocation=(0,5))
    app.furniture.append(app.counter1)
    app.interactiveFurniture.append(app.counter1)
    app.storingFurniture.append(app.counter1)

    app.counter2 = Counter(app,560,399,counterImage,80,80,counterPopUp,gridLocation=(3,3))
    app.furniture.append(app.counter2)
    app.interactiveFurniture.append(app.counter2)
    app.storingFurniture.append(app.counter2)

    app.counter3 = Counter(app,721,399,counterImage,80,80,counterPopUp,gridLocation=(3,4))
    app.furniture.append(app.counter3)
    app.interactiveFurniture.append(app.counter3)
    app.storingFurniture.append(app.counter3)

    app.counter4 = Counter(app,881,399,counterImage,80,80,counterPopUp,gridLocation=(3,5))
    app.furniture.append(app.counter4)
    app.interactiveFurniture.append(app.counter4)
    app.storingFurniture.append(app.counter4)

    app.counter5 = Counter(app,560,741,counterImage,80,80,counterPopUp,gridLocation=(6,3))
    app.furniture.append(app.counter5)
    app.interactiveFurniture.append(app.counter5)
    app.storingFurniture.append(app.counter5)

    app.counter6 = Counter(app,722,741,counterImage,80,80,counterPopUp,gridLocation=(6,4))
    app.furniture.append(app.counter6)
    app.interactiveFurniture.append(app.counter6)
    app.storingFurniture.append(app.counter6)

    app.counter7 = Counter(app,881,741,counterImage,80,80,counterPopUp,gridLocation=(6,5))
    app.furniture.append(app.counter7)
    app.interactiveFurniture.append(app.counter7)
    app.storingFurniture.append(app.counter7)
    app.counter7.container = FireExtinguisher(app)

    app.counter8 = Counter(app,78,399,counterImage,80,80,counterPopUp,gridLocation=(3,0))
    app.furniture.append(app.counter8)
    app.interactiveFurniture.append(app.counter8)
    app.storingFurniture.append(app.counter8)

    #shelfless counters
    tallCounterImage = app.loadImage("Furniture/tall counter.png")
    tallCounterImage = app.scaleImage(tallCounterImage,0.8)
    app.counter9 = Counter(app,80,230,tallCounterImage,80,90,counterPopUp,gridLocation=(2,0))
    app.furniture.append(app.counter9)
    app.interactiveFurniture.append(app.counter9)
    app.storingFurniture.append(app.counter9)

    # app.counter10 = Counter(app,80,180,counterNoShelfImage,80,45,counterPopUp,gridLocation=(1,0))
    # app.furniture.append(app.counter10)
    # app.interactiveFurniture.append(app.counter10)
    # app.storingFurniture.append(app.counter10)
    
    app.chunkyCounterNoShelfImage = app.loadImage("Furniture/chunkycounter.png")
    app.chunkyCounterNoShelfImage = app.scaleImage(app.chunkyCounterNoShelfImage,0.8)
    # app.furniture.append(app.counter11)
    # app.interactiveFurniture.append(app.counter11)

    app.furnitureLocations = [
        [None, app.stoveTop1, app.stoveTop2, app.stoveTop3, app.stoveTop4, app.counter1, None, app.fridge, app.fridge], 
        [app.counter9, None, None, None, None, None, None, app.fridge, app.fridge], 
        [app.counter9, None, None, None, None, None, None, None, None], 
        [app.counter8, app.choppingTable1, app.choppingTable2, app.counter2, app.counter3, app.counter4, None, None, None], 
        [None, None, None, None, None, None, None, None, None], 
        [None, None, None, None, None, None, None, None, None], 
        [app.servingStation, None, app.tableWithPlates, app.counter5, app.counter6, app.counter7, None, app.trash,None]
          ]

def spreadFire(app):
    firesToAdd = []
    for row in range(app.rows):
        for col in range(app.cols):
            if app.furnitureLocations[row][col] != None and app.furnitureLocations[row][col].onFire == True:
                #spread the fire
                for drow in [-1,0,1]:
                    for dcol in [-1,0,1]:
                        if (drow,dcol) == (0,0):
                            continue
                        else:
                            newRow = row + drow
                            newCol = col + dcol
                            if (newRow >= 0 and newRow < app.rows and
                                newCol >= 0 and newCol < app.cols and
                                app.furnitureLocations[newRow][newCol] != None):
                                firesToAdd.append((newRow,newCol))
    for row,col in firesToAdd:
        app.furnitureLocations[row][col].onFire = True
        #IF IT HAD AN EQUIPMENT ON IT, TURN THE THING INSIDE THE EQUIPMENT TO ASH
        if (isinstance(app.furnitureLocations[row][col],storingFurniture) and 
            isinstance(app.furnitureLocations[row][col].container,Equipment)):
            if app.furnitureLocations[row][col].container.container != None: #something in pan
                app.furnitureLocations[row][col].container.container = Ash(app)
            else:
                continue
        #IF IT HAD SOMETHING ON IT, TURN IT TO ASH
        elif (isinstance(app.furnitureLocations[row][col],storingFurniture) and 
              app.furnitureLocations[row][col].container != None):
            app.furnitureLocations[row][col].container = Ash(app)

def gameMode_timerFired(app):
    if app.paused == False:
        if app.countDownT.started == False:
            app.countDownT.started = True
            app.countDownT.initialTime = time.time()
        app.step += 1
        app.timePassed += 100
        app.timeSinceHintKeyPressed += 100
        if app.timeSinceHintKeyPressed >= 3000:
            app.hintMode = False
        app.timeSinceLastcKeyPressed += 100
        app.timeSinceLastcKeyReleased += 100
        app.klee.timeSinceLastKeyPressed += 100
        app.klee.timeSinceLastKeyReleased += 100
        # app.timeSinceLastOrderGenerated += 100
        app.oneSecondDelay += 100
        if time.time() - app.timeSinceLastOrderGenerated >= 40:
            if len(app.orderQueue.lineUp) <= 5:
                app.orderQueue.generateOrder(app)
            app.timeSinceLastOrderGenerated = time.time()
        if app.oneSecondDelay == 1000:
            app.orderQueue.decreaseTime(app)
            app.orderQueue.checkForExpiry(app)
        app.timeSinceLastFireSpread += 100
        if app.timeSinceLastFireSpread == 10000:
            spreadFire(app)
            app.timeSinceLastFireSpread = 0
        if isinstance(app.klee.currentNearObject,ChoppingTable):
            if app.klee.currentNearObject.container != None and type(app.klee.currentNearObject.container) != Ash and app.klee.currentNearObject.container.chopped == False:
                if app.timeSinceLastcKeyReleased > 100:
                    app.klee.currentNearObject.container.choppingState = 0
        
        for stove in app.stoveTops:
            #check if the stove has a pan with an ingredient to be cooked
            if stove.container != None: # the stove has a pot or a pan
                if stove.container.container != None and type(stove.container.container) != Ash: #the pot/pan has an ingredient
                    stove.container.container.increaseCookingTime()
                    # stove.container.container.cookingState += 5
                    if stove.container.container.totalTimeCooking >= 15:
                        stove.container.container.cooked = True
                    if (stove.container.container.totalTimeCooking > 50):
                        stove.onFire = True
                        stove.container.container = Ash(app)
                # print(stove.fireSpriteIndex)

        for furniture in app.furniture:
            if furniture.onFire == True:
                furniture.fireSpriteIndex = (furniture.fireSpriteIndex+1)%4

        #update the countdown timer
        app.countDownT.countDown()
        if app.countDownT.timeElapsed >= app.countDownT.totalTime:
            app.mode = "gameOver"
            if app.score <= 500:
                app.starsDrawn = [False, True, True]
            elif 500 < app.score <= 1000:
                app.starsDrawn = [False, False, True]
            elif app.score > 1500:
                app.starsDrawn = [False,False,False]

def gameMode_mouseReleased(app, event):
    app.mouseX = event.x
    app.mouseY = event.y
    if app.paused == True:
        for button in app.pauseButtons:
            button.checkIfClicked(app,event.x,event.y)
    else:
        if app.hintButton.checkIfClicked(app,event.x,event.y):
            app.hintMode = not app.hintMode
            nextDestination = findNextDestination(app)
            if nextDestination != None:
                nextDestinationR, nextDestinationC = nextDestination
                tempObject = app.environment[nextDestinationR][nextDestinationC]
                app.environment[nextDestinationR][nextDestinationC] = None
                app.hintPath = findShortestPath(app.klee.gridLocation,nextDestination,app.environment)
                app.environment[nextDestinationR][nextDestinationC] = tempObject
            app.timeSinceHintKeyPressed = 0

        if app.practiceButton.checkIfClicked(app,event.x,event.y):
            app.practiceMode = not app.practiceMode
            app.spaghettiExpiryTime = 200
            app.saladExpiryTime = 200
            app.fishToastExpiryTime = 200

def gameMode_mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def gameMode_keyPressed(app,event):
    if app.paused == False:
        #keep track of the direction which is defined in the class 
        #end goal: the longer you hold down the more she accelerates
        app.klee.direction = event.key
        app.klee.move(app)

        #checks if klee has walked any interactive furniture
        app.klee.checkIfNearInteractiveFurniture(app.interactiveFurniture)
        if app.klee.currentNearObject == app.fridge  and app.klee.inventory == None:
            if event.key == "1":
                app.klee.inventory = Tomato(app)
            elif event.key == "2":
                app.klee.inventory = Pasta(app)
            elif event.key == "3":
                app.klee.inventory = Lettuce(app)
            elif event.key == "4":
                app.klee.inventory = Fish(app)
            elif event.key == "5":
                app.klee.inventory = Bread(app)

        elif event.key == "c":
            if app.klee.currentNearObject == app.trash:
                if isinstance(app.klee.inventory,Equipment) and app.klee.inventory.container != None: #at trash
                    app.klee.inventory.container = None
                elif isinstance(app.klee.inventory,Dish) and app.klee.inventory.container != []: 
                    app.klee.inventory.container = []
                elif isinstance(app.klee.inventory,Equipment) == False and isinstance(app.klee.inventory,FireExtinguisher) == False:
                    app.klee.inventory = None
            elif app.klee.currentNearObject == app.servingStation: #at serving station
                if (app.klee.inventory != None and #check if they have a completed dish
                    type(app.klee.inventory) == Dish and
                    app.klee.inventory.done == True):
                    app.orderQueue.serveDish(app,app.klee.inventory.meal) #serve the dish
                    app.klee.inventory = None 
    
            elif isinstance(app.klee.currentNearObject,ChoppingTable):
                if app.klee.currentNearObject.container != None and type(app.klee.currentNearObject.container) != Ash and app.klee.currentNearObject.container.chopped == False: #if there is something to chop
                    if app.timeSinceLastcKeyPressed <= 100:
                        app.klee.currentNearObject.container.choppingState += 4
                        if app.klee.currentNearObject.container.choppingState == 100:
                            app.klee.currentNearObject.container.chopped = True
                    elif app.timeSinceLastcKeyPressed >= 200:
                        app.klee.currentNearObject.container.choppingState = 0
            app.timeSinceLastcKeyPressed = 0

            if (type(app.klee.inventory) == FireExtinguisher): #holding fire extiguisher
                if app.klee.currentNearObject != None and app.klee.currentNearObject.onFire == True: #if she is next to something on fire
                    if app.timeSinceLastcKeyPressed <= 100:
                        app.klee.currentNearObject.dousingState += 4
                        if app.klee.currentNearObject.dousingState == 100:
                            app.klee.currentNearObject.onFire = False
                            app.klee.currentNearObject.dousingState = 0
                    elif app.timeSinceLastcKeyPressed >= 200:
                        app.klee.currentNearObject.dousingState = 0
            app.timeSinceLastcKeyPressed = 0
        
        elif event.key == 'Space':
            #check if Klee is near the plate table
            if (app.klee.currentNearObject == app.tableWithPlates) and app.klee.inventory == None:
                app.klee.inventory = Dish(app)
            #storing space is empty and klee is occupied
            for object in app.storingFurniture:
                if app.klee.currentNearObject == object: 
                    if object.onFire == True:
                        return
                    #if klee has a full inventory but the storing space doesn't
                    if app.klee.inventory != None and object.container == None: #if klee has something to put in an empty storing space
                        
                        if (type(app.klee.inventory) in object.acceptedTypes): #if the storing space allows that type of object
                            #object.container = app.klee.inventory
                            if (isinstance(app.klee.inventory,Equipment) and #klee has a pan
                                app.klee.inventory.container != None and #pan has ingredient
                                isinstance(app.klee.currentNearObject,StoveTop)): #3) it's on a stove -> start the cookingtime
                                print("hey")
                                app.klee.inventory.container.timeSinceCookingStarted = time.time()
                            object.addItemToContainer(app,app.klee.inventory)
                            app.klee.inventory = None

                    #if klee's inventory is empty but the storing space has something
                    elif app.klee.inventory == None and object.container != None:
                        #if the thing she is picking up is a pan w/ ingredient, set the timeSinceCookingStarted back to 0
                        if isinstance(object.container,Equipment):
                            if object.container.container != None and (type(object.container.container) != Ash): #pan has ingredient
                                print("picking up a pot/pan with an ingredient!")
                                object.container.container.timeSinceCookingStarted = None
                                object.container.container.previousTotalTimeCooking = object.container.container.totalTimeCooking
                        app.klee.inventory = object.container
                        object.removeItemFromContainer(app)

                    #storing space and klee are both occupied
                    elif app.klee.inventory != None and object.container != None:
                        if isinstance(object.container,Equipment):
                            if (object.container.container == None): #an empty pot or pan is in the storing space
                                if object.container.canAccept(app.klee.inventory): #check whether the pot or pan accepts klee's inventory
                                    app.klee.inventory.timeSinceCookingStarted = time.time()
                                    object.container.container = app.klee.inventory
                                    app.klee.inventory = None
                            else:
                                continue

                        elif (isinstance(object.container,Dish) and #klee has a pan/pot with a cooked ingredient and is standing in front of a plate
                            isinstance(app.klee.inventory,Equipment) and 
                            app.klee.inventory.container != None):
                            if object.container.canAdd(app.klee.inventory.container):
                                object.container.addIngredient(app,app.klee.inventory.container)
                                app.klee.inventory.container = None
                        
                        elif (isinstance(object.container,Dish)): #if klee is standing in front of a dish
                            if object.container.canAdd(app.klee.inventory):
                                object.container.addIngredient(app,app.klee.inventory)
                                app.klee.inventory = None
                            # if type(app.klee.inventory) == Tomato and app.klee.inventory.chopped == True: #if it's a pan, only accept chopped ingredients
                        else:
                            object.container, app.klee.inventory = app.klee.inventory,object.container
        elif event.key == "g":
            app.mode = "gameOver"
            if app.score <= 500:
                app.starsDrawn = [False, True, True]
            elif 500 < app.score <= 1000:
                app.starsDrawn = [False, False, True]
            elif app.score > 1500:
                app.starsDrawn = [False,False,False]
        elif event.key == "s":
            app.score += 100
        
        elif event.key == "a":
            app.counter2.onFire = True

    if event.key == "p":
        app.paused = not app.paused
    
    app.klee.timeSinceLastKeyPressed = 0
    app.lastKeyPressed = event.key

def gameMode_keyReleased(app,event):
    if app.paused == False:
        if app.klee.direction == "Down":
            app.klee.currentSprite = app.klee.sprites[0]
        elif app.klee.direction == "Up":
            app.klee.currentSprite = app.klee.sprites[3]
        elif app.klee.direction == "Right":
            app.klee.currentSprite = app.klee.sprites[6]
        elif app.klee.direction == "Left":
            app.klee.currentSprite = app.klee.sprites[9]
        if app.klee.timeSinceLastKeyReleased > 200:
            app.klee.acceleration = 1
        app.klee.timeSinceLastKeyReleased = 0
        app.timeSinceLastcKeyReleased = 0

def getCenterCoords(app,row,col):
    cx = app.colWidth*(col+1)-app.colWidth*0.5
    cy = app.rowWidth*(row+1)-app.rowWidth*0.5
    return cx,cy

def drawHintPath(app,hintPath,canvas):
    if (0<=app.timeSinceHintKeyPressed%10<=4):
        if hintPath == None:
            return
        for i in range(len(hintPath)-1):
            r0,c0 = hintPath[i]
            cx0,cy0 = getCenterCoords(app,r0,c0)
            r1,c1 = hintPath[i+1]
            cx1,cy1 = getCenterCoords(app,r1,c1)
            canvas.create_line(cx0,cy0,cx1,cy1,fill="red",width=4)

def gameMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill="#e6844c")
    if app.hintMode == True and app.timeSinceHintKeyPressed%500 == 0:
        drawHintPath(app,app.hintPath,canvas)
    
    #draw fridge
    for furniture in app.furniture:
        furniture.draw(app,canvas)

    #draw klee
    app.klee.draw(canvas)
    if app.klee.inventory != None:
        additionalY = (-1 * math.sin(app.step) * 20)
        app.klee.inventory.draw(app,app.klee.x,app.klee.y+additionalY-20,canvas)

    app.orderQueue.draw(app,canvas)
    
    #score
    canvas.create_text(1041,37,text=f"Score: {app.score}",font="GB18030Bitmap 20")


    #practice mode
    if app.practiceMode == True:
        canvas.create_text(10,630,text=f"Practice mode: ON\nSalad expiry time:{app.saladExpiryTime} (Rateup:{app.saladRateUp}%)\nSpaghetti expiry time:{app.spaghettiExpiryTime} (Rateup:{app.spaghettiRateUp}%)\nFish toast expiry time: {app.fishToastExpiryTime} (Rateup:{app.fishToastRateUp}%)",anchor = 'w')

    app.hintButton.draw(app,canvas)
    app.practiceButton.draw(app,canvas)


    canvas.create_image(80,55,image=ImageTk.PhotoImage(app.chunkyCounterNoShelfImage))
    app.countDownT.draw(canvas)

    if app.paused == True:
        canvas.create_image(app.width//2,app.height//2,image=ImageTk.PhotoImage(app.pausePopupImage))
        for button in app.pauseButtons:
            button.draw(app,canvas)



class Button():
    def __init__(self,image,hoverImage,x,y,xBound,yBound,mode):
        self.image = image
        self.hoverImage = hoverImage
        self.x = x 
        self.y = y
        self.left = self.x-xBound
        self.right = self.x+xBound
        self.top = self.y-yBound
        self.bottom = self.y+yBound
        self.mode = mode
    
    def checkIfClicked(self,app,clickX,clickY):
        if (self.left <= clickX <= self.right) and (self.top<=clickY<=self.bottom):
            app.mode = self.mode
    
    def hovering(self,app,mouseX,mouseY):
        if (self.left <= mouseX <= self.right) and (self.top<= mouseY <=self.bottom):
            return True
        else:
            return False
    
    def draw(self,app,canvas):
        #draw button
        if self.hovering(app,app.mouseX,app.mouseY):
            canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.hoverImage))
        else:
            canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.image))

class RestartButton(Button):
    def checkIfClicked(self,app,clickX,clickY):
        if (self.left <= clickX <= self.right) and (self.top<=clickY<=self.bottom):
            appStarted(app)
            app.mode = "gameMode"

class MenuButton(Button):
    def checkIfClicked(self,app,clickX,clickY):
        if (self.left <= clickX <= self.right) and (self.top<=clickY<=self.bottom):
            appStarted(app)

class startFire():
    def __init__(self,app,x,y):
        self.x = x
        self.y = y
        self.spritestrip = app.loadImage("startscreen/fire.png")
        self.sprites = []
        self.spriteIndex = 0
        for i in range(4):
            left = i*170
            top = 0
            right = (i+1)*170
            bottom = 153
            sprite = self.spritestrip.crop((left,top,right,bottom))
            self.sprites.append(sprite)
        for i in range(len(self.sprites)):
            self.sprites[i] = app.scaleImage(self.sprites[i],3.5)
            
    def animate(self):
        self.spriteIndex = (self.spriteIndex+1)%4
    
    def draw(self,app,canvas):
        canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.sprites[self.spriteIndex]))
        
def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image(app.width//2,app.height//2,image=ImageTk.PhotoImage(app.startScreenImage))
    for fire in app.fires:
        fire.draw(app,canvas)

    for button in app.startButtons:
        button.draw(app,canvas)

def splashScreenMode_mouseReleased(app, event):
    app.mouseX = event.x
    app.mouseY = event.y
    for button in app.startButtons:
        button.checkIfClicked(app,event.x,event.y)
  
def splashScreenMode_mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y
    
def splashScreenMode_timerFired(app):
    for fire in app.fires:
        fire.animate()

#gameover mode
def gameOver_mouseReleased(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def gameOver_timerFired(app):
    if app.starsDrawn[0] == False:
        app.primogems[0].x -= 60
        if app.primogems[0].x <= app.width//2-150:
            app.starsDrawn[0] = True
    elif app.starsDrawn[1] == False:
        app.primogems[1].x -= 60
        if app.primogems[1].x <= app.width//2:
            app.starsDrawn[1] = True
    elif app.starsDrawn[2] == False:
        app.primogems[2].x -= 60
        if app.primogems[2].x <= app.width//2+200:
            app.starsDrawn[2] = True

def gameOver_redrawAll(app, canvas):
    canvas.create_image(app.width//2,app.height//2-100,image=ImageTk.PhotoImage(app.gameOverTextImage))
    canvas.create_text(711,600,text=f"SCORE:{app.score}",font="GB18030Bitmap 40")

    for button in app.gameoverButtons:
        button.draw(app,canvas)
    
    for primogem in app.primogems:
        primogem.draw(app,canvas)
    
def gameOver_mouseReleased(app,event):
    for button in app.gameoverButtons:
        button.checkIfClicked(app,event.x,event.y)

def gameOver_mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

runApp(width=1440, height=798)


