import pyxel
import random
import time

NUMBEROFBUGSMODEL = 16


class YouLost:
    def draw(self):
        pyxel.cls(0)
        pyxel.text(50, 50, "YOU LOST!\nPress R to restart\nPress Q to quit", 7)


class Menu:
    def __init__(self):
        self.optionSelected = 0
        self.bugs = [Bug() for x in range(8)]

    def draw(self):
        pyxel.circb(118, 128, pyxel.frame_count % 32/2, 1)
        pyxel.circb(118, 128, (pyxel.frame_count-5) % 16, 7)
        pyxel.rect(102, 112, 40, 16, 0)
        pyxel.circb(133, 120, pyxel.frame_count % 33/2, 1)
        pyxel.circb(133, 120, (pyxel.frame_count-5) % 15, 7)
        pyxel.rect(117, 104, 40, 16, 0)
        pyxel.circb(39, 128, pyxel.frame_count % 32/2, 1)
        pyxel.circb(39, 128, pyxel.frame_count % 16, 7)
        pyxel.rect(22, 112, 40, 16, 0)
        pyxel.circb(22, 118, pyxel.frame_count % 33/2, 1)
        pyxel.circb(22, 118, pyxel.frame_count % 15, 7)
        pyxel.rect(5, 102, 40, 16, 0)

        pyxel.blt(105, 8+pyxel.frame_count % 2, 0, 64, 32, 32, 128, 0)
        pyxel.blt(120, pyxel.frame_count % 2, 0, 64, 32, 32, 128, 0)
        pyxel.blt(22, 8+pyxel.frame_count % 2, 0, 64, 32, -32, 128, 0)
        pyxel.blt(4, pyxel.frame_count % 2, 0, 64, 32, -32, 128, 0)
        pyxel.blt(11, 10+pyxel.frame_count % 2, 0, 16, 0, 128, 32, 0)

        pyxel.rect(52, 56, 1, 64, 7)
        pyxel.rect(98, 56, 1, 64, 7)
        pyxel.text(57, 64+16*self.optionSelected, '>', pyxel.frame_count % 16)
        pyxel.text(67, 64, "PLAY!", 7)
        pyxel.text(67, 80, "Credits", 7)
        pyxel.text(67, 96, "Quit", 7)

    def update(self, app):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.optionSelected = (self.optionSelected+1) % 3
        if pyxel.btnp(pyxel.KEY_UP):
            self.optionSelected = (self.optionSelected-1) % 3
        if pyxel.btn(pyxel.KEY_ENTER):
            if self.optionSelected == 0:
                app.state = 2

            if self.optionSelected == 1:
                app.state = 1

            if self.optionSelected == 2:
                pyxel.quit()


class Incipit:
    def __init__(self):
        self.read = 0

    def draw(self):
        pyxel.rect(16, 16, 118, 118, 9)
        pyxel.text(
            20, 32, "You've just discovered \n you live in a simulation.".upper(), 0)
        pyxel.text(
            20, 52, "Your bugs collection is your \n only way out of it.".upper(), 0)
        pyxel.text(
            20, 72, "Buy them!\nbreed them!\nfeed them!\nto create the perfect bug\nto corrupt the simulation.".upper(), 0)
        pyxel.rect(58, 110, 70, 20, 0)
        pyxel.text(62, 115, "OK (press ENTER)", 9)

    def update(self, app):
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.read = 1
        if pyxel.btn(pyxel.KEY_ENTER) and self.read:
            self.read = 0
            app.state = 3


class Collection:
    def __init__(self, game):
        self.game = game
        self.readyForMenu = 0
        self.optionSelected = 0
        self.jarSelectionMode = 0
        self.parentSelectionMode = 0
        self.readyToSelect = 0
        self.selectedJar = 0
        self.feeding = 0
        self.parents = []
        self.jars = [Jar() for j in range(12)]
        [self.jars[i].put(self.game.bugCollection[i])
         for i in range(len(self.game.bugCollection))]

    def draw(self):

        pyxel.rect(110, 0, 40, 150, 1)
        pyxel.text(117, 4, "Balance", 7)
        pyxel.rect(111, 14, 40, 10, 0)
        pyxel.blt(112, 10, 0, 16, 32, 16, 16, 0)
        pyxel.text(127, 16, str(self.game.balance), 7)

        pyxel.text(117, 32, "Luck", 7)
        pyxel.rect(110, 38, 40, 10, 0)
        pyxel.rect(122, 40, 3, 3, 2)
        pyxel.rect(126, 40, 3, 3, 8)
        pyxel.rect(130, 40, 3, 3, 10)
        pyxel.rect(134, 40, 3, 3, 11)
        pyxel.rect(138, 40, 3, 3, 3)

        pyxel.pset(123+4*self.game.luck, 44, 7)
        pyxel.pset(122+4*self.game.luck, 45, 7)
        pyxel.pset(124+4*self.game.luck, 45, 7)

        pyxel.rect(110, 105, 40, 45, 8)
        pyxel.text(112, 110, "Scores", 7)
        pyxel.rect(118, 125, 26, 17, 0)
        pyxel.rectb(118, 125, 26, 17, 1)
        for i, bug in enumerate(self.game.bugCollection):
            for c in range(bug.colorCheck):
                pyxel.pset(120+i*2, 140-c, 7)

        pyxel.rect(110, 0, 1, 150, 7)
        if not self.jarSelectionMode and self.parentSelectionMode == 0:
            pyxel.rect(115, [66, 76, 86, 96]
                       [self.optionSelected]-2, 30, 10, 3)

            pyxel.rect(115, [66, 76, 86, 96]
                       [self.optionSelected]+6, 30, 2, 12)

        pyxel.text(117, 66, "Buy", 7)
        pyxel.text(117, 76, "Sell", 7)
        pyxel.text(117, 86, "Breed", 7)
        pyxel.text(117, 96, "Feed", 7)
        if not self.jarSelectionMode and self.parentSelectionMode == 0:
            self.clickableButtons = [True, len(
                self.game.bugCollection) > 0, self.game.balance > 49, self.game.balance >= 5*len(self.game.bugCollection)]
            self.clickableButton = self.clickableButtons[self.optionSelected]
            pyxel.text(112, [66, 76, 86, 96]
                       [self.optionSelected], ">"*self.clickableButton + "X"*(not self.clickableButton), pyxel.frame_count % 16*self.clickableButton+8*(not self.clickableButton))

        for i in range(12):
            x = i % 3
            y = i//3
            self.jars[i].draw(
                x*35, y*35, (self.jarSelectionMode or self.parentSelectionMode != 0) and i == self.selectedJar, feeding=self.feeding)
        if self.jarSelectionMode:
            pyxel.text(6, 143, "Arrows, Enter or backspace", 13)

    def update(self, app):
        if pyxel.btnp(pyxel.KEY_DOWN) and not self.jarSelectionMode and self.parentSelectionMode == 0:
            self.optionSelected = (self.optionSelected+1) % 4
        if pyxel.btnp(pyxel.KEY_UP) and not self.jarSelectionMode and self.parentSelectionMode == 0:
            self.optionSelected = (self.optionSelected-1) % 4
        if pyxel.btnp(pyxel.KEY_ENTER) and not self.jarSelectionMode and self.readyForMenu and self.parentSelectionMode == 0:
            if self.optionSelected == 0:
                app.state = 4
            if self.optionSelected == 1:
                self.jarSelectionMode = True
                self.readyToSelect = False
            if self.optionSelected == 2 and self.clickableButtons[2]:
                self.readyToSelect = 0
                self.parentSelectionMode = 1
            if self.optionSelected == 3 and self.clickableButtons[3]:
                self.game.balance -= 5*len(self.game.bugCollection)
                self.feeding = 1
                app.store.__init__(self.game)
                [bug.alterReality(self.game)
                 for bug in self.game.bugCollection]
        if pyxel.btnr(pyxel.KEY_ENTER) and (self.jarSelectionMode or self.parentSelectionMode != 0):
            self.readyToSelect = True
        if pyxel.btnr(pyxel.KEY_ENTER) and self.feeding:
            self.feeding = False
        if pyxel.btnr(pyxel.KEY_ENTER) and self.parentSelectionMode != 1:
            self.readyForMenu = 1
        if (pyxel.btnp(pyxel.KEY_ENTER) and self.jarSelectionMode) and self.readyToSelect:
            if self.jars[self.selectedJar].bug:
                self.jars.pop(self.selectedJar)
                self.game.balance += self.game.bugCollection[self.selectedJar].value
                self.game.bugCollection.pop(self.selectedJar)
                self.jars.append(Jar())
            self.readyToSelect = False
        if (pyxel.btnp(pyxel.KEY_ENTER) and self.parentSelectionMode != 0) and self.readyToSelect:
            self.parents.append(self.jars[self.selectedJar].bug)

            self.parentSelectionMode = (self.parentSelectionMode+1) % 3
            if self.parentSelectionMode == 0:
                newBug = self.parents[0].breed(self.parents[1])
                self.parents = []
                self.jars[len(self.game.bugCollection)].put(newBug)
                self.game.bugCollection.append(newBug)
                self.game.balance -= 50

            self.readyToSelect = False
        if pyxel.btnp(pyxel.KEY_DOWN) and (self.jarSelectionMode or self.parentSelectionMode != 0):
            self.selectedJar = (self.selectedJar+3) % 12
        if pyxel.btnp(pyxel.KEY_UP) and (self.jarSelectionMode or self.parentSelectionMode != 0):
            self.selectedJar = (self.selectedJar-3) % 12
        if pyxel.btnp(pyxel.KEY_LEFT) and (self.jarSelectionMode or self.parentSelectionMode != 0):
            self.selectedJar = (self.selectedJar-1) % 12
        if pyxel.btnp(pyxel.KEY_RIGHT) and (self.jarSelectionMode or self.parentSelectionMode != 0):
            self.selectedJar = (self.selectedJar+1) % 12
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.jarSelectionMode = False
            self.parentSelectionMode = 0
        if self.game.balance < 0:
            app.state = 5


class Store:
    def __init__(self, game):
        self.jars = [Jar() for x in range(4)]
        [jar.put(Bug(useLuck=True,game=game)) for jar in self.jars]
        self.jarSelectionMode = 1
        self.selectedJar = 0
        self.readyToSelect = 0
        self.game = game

    def update(self, app, collection):
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            app.state = 3
            self.readyToSelect = 0
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selectedJar = (self.selectedJar+1) % 4
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selectedJar = (self.selectedJar-1) % 4
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.readyToSelect = 1
        if pyxel.btnp(pyxel.KEY_ENTER) and self.readyToSelect and self.jars[self.selectedJar].bug:
            self.readyToSelect = 0
            self.game.balance -= self.jars[self.selectedJar].bug.value
            selectedJar = self.jars.pop(self.selectedJar)
            app.collection.jars[len(app.game.bugCollection)] = selectedJar
            app.game.bugCollection.append(selectedJar.bug)
            self.jars.append(Jar())

    def draw(self):
        for i in range(4):
            self.jars[i].draw(
                i*35, 35, self.jarSelectionMode and i == self.selectedJar, feeding=False)
        if self.jarSelectionMode:
            pyxel.text(6, 143, "Arrows, Enter or backspace", 13)

        pyxel.text(117, 4, "Balance", 7)
        pyxel.rect(111, 14, 40, 10, 0)
        pyxel.blt(112, 10, 0, 16, 32, 16, 16, 0)
        pyxel.text(127, 16, str(self.game.balance), 7)


class Bug:
    def __init__(self, randomImage=True,useLuck=False,game=None):
        if randomImage:
            id = random.randint(0, NUMBEROFBUGSMODEL-1)
            bodycolor = random.randint(1, 15)
            bordercolor = random.randint(2, 15)
            self.image1 = []
            for i in range(id*16, id*16+16):
                self.image1 += pyxel.image(0).data[i][:16]
            self.image1 = [x if x != 7 else 16 for x in self.image1]
            self.image1 = [x if x != 8 else bodycolor for x in self.image1]
            self.image1 = [x if x != 16 else bordercolor for x in self.image1]
            self.image2 = self.image1.copy()

        else:
            self.image1 = [0 for x in range(256)]
            self.image2 = [0 for x in range(256)]
        self.move()
        self.energy = random.randint(1, 3)
        if useLuck:
            self.alterations = random.choices([-1, 0, 1], [0.4, 0.3, 0.3+game.luck/5], k=3)
        else:
            self.alterations = random.choices([-1, 0, 1], [0.4, 0.3, 0.3], k=3)
        self.calculatePrice()

    def draw(self, x, y):
        if pyxel.frame_count % 16 < 8:
            image = self.image1
        else:
            image = self.image2
        for pixel in range(256):
            u = pixel % 16
            v = pixel//16
            pyxel.pset(x+u, y+v, image[pixel])

    def move(self):
        self.image2 = self.image1.copy()
        for i in range(16):
            self.image2[1+i*16] = self.image1[(17+i*16) % 256]
            self.image2[2+i*16] = self.image1[(18+i*16) % 256]
            self.image2[14+i*16] = self.image1[(30+i*16) % 256]
            self.image2[13+i*16] = self.image1[(29+i*16) % 256]

    def breed(self, bug):
        self.energy = max([0, self.energy-1])
        bug.energy = max([0, bug.energy-1])
        son = Bug(randomImage=False)
        alterations = [random.choice(
            [self.alterations[i], bug.alterations[i]]) for i in range(3)]

        image = []
        for i in range(16):
            r = random.randint(0, 1)
            if r:
                image += self.image1[i*16:(i+1)*16]
            else:
                image += bug.image1[16*i:16*(i+1)]
        son.image1 = image
        son.move()
        son.calculatePrice()
        son.alterations = alterations
        return son

    def alterReality(self, game):
        if self.energy != 3:
            for a in self.alterations:
                game.balance += a*self.energy
            game.luck = max([0, game.luck+sum(self.alterations)])
            game.luck = min([4, game.luck])
        self.energy = min([3, self.energy+1])

    def calculatePrice(self):
        self.colorCheck = sum([x in self.image1 for x in range(16)])
        pixelCheck = sum([x != 0 for x in self.image1])
        self.value = sum([self.colorCheck*pixelCheck //
                         10, sum(5*self.alterations)])


class Jar:
    def __init__(self, bug=None):
        self.bug = bug
        self.feeding = 0
        self.animationFrame = 0

    def draw(self, x, y, selected=False, feeding=False):
        if feeding:
            self.feeding = True
            self.animationFrame = 0
        border = 7*(not selected) + selected*pyxel.frame_count % 16
        pyxel.rectb(5+x, 5+y, 1, 27, border)
        pyxel.rectb(34+x, 5+y, 1, 27, border)
        pyxel.rectb(5+x, 32+y, 5, 1, border)
        pyxel.rectb(10+x, 33+y, 5, 1, border)
        pyxel.rectb(15+x, 34+y, 10, 1, border)
        pyxel.rectb(30+x, 32+y, 5, 1, border)
        pyxel.rectb(25+x, 33+y, 5, 1, border)
        pyxel.blt(4+x, 1+y, 0, 16, 64, 32, 7, 0)
        pyxel.rect(7+x, 9+y, 1, 13, 7)
        pyxel.rect(7+x, 24+y, 1, 4, 7)
        if self.bug == None:
            pyxel.text(10+x, 9+y, "Empty", 7)
        else:
            self.bug.draw(12+x, 15+y)
            for e in range(self.bug.energy):
                pyxel.pset(9+x+e*4, 9+y, 8)
                pyxel.pset(11+x+e*4, 9+y, 8)
                pyxel.pset(9+x+e*4, 10+y, 8)
                pyxel.pset(10+x+e*4, 10+y, 8)
                pyxel.pset(11+x+e*4, 10+y, 8)
                pyxel.pset(10+x+e*4, 11+y, 8)
            for i, a in enumerate(self.bug.alterations):
                if a == -1:
                    pyxel.pset(22+x+i*4, 10+y, 8)
                    pyxel.pset(23+x+i*4, 11+y, 8)
                    pyxel.pset(24+x+i*4, 10+y, 8)
                if a == 0:
                    pyxel.rect(22+x+i*4, 11+y, 3, 1, 1
                               )
                if a == 1:
                    pyxel.pset(22+x+i*4, 11+y, 3)
                    pyxel.pset(23+x+i*4, 10+y, 3)
                    pyxel.pset(24+x+i*4, 11+y, 3)
        if selected and self.bug:
            pyxel.rect(4+x, 3+y, 33, 7, 7)
            pyxel.rectb(3+x, 2+y, 35, 9, 8)
            pyxel.text(5+x, 4+y, str(self.bug.value)+" bucks", 0)
        if self.feeding and self.bug:
            pyxel.rect(7+x, 7+y, 26, 8, 7)
            pyxel.rectb(6+x, 6+y, 28, 10, 0)
            if self.animationFrame > 8:
                pyxel.pset(18+x, 8+y, 0)
                pyxel.pset(18+x, 9+y, 0)
                pyxel.pset(21+x, 8+y, 0)
                pyxel.pset(21+x, 9+y, 0)
                pyxel.rect(16+x, 12+y, 8, 1, 0)
                pyxel.pset(15+x, 11+y, 0)
                pyxel.pset(24+x, 11+y, 0)
            else:
                for e in range(4):
                    pyxel.pset(12+x+e*4, 9+y, 8)
                    pyxel.pset(14+x+e*4, 9+y, 8)
                    pyxel.pset(12+x+e*4, 10+y, 8)
                    pyxel.pset(13+x+e*4, 10+y, 8)
                    pyxel.pset(14+x+e*4, 10+y, 8)
                    pyxel.pset(13+x+e*4, 11+y, 8)
            self.animationFrame += 1
        if self.animationFrame == 16:
            self.feeding = 0
            self.animationFrame = 0

    def put(self, bug):
        self.bug = bug


class Game:
    def __init__(self):
        self.balance = 100
        self.luck = 2
        self.bugCollection = [Bug() for x in range(2)]


class Credits:
    def __init__(self):
        self.read = 0

    def draw(self):
        pyxel.rect(16, 16, 118, 118, 9)
        pyxel.text(
            20, 32, "This game was created for \n GAME OFF 2021", 0)
        pyxel.text(
            20, 52, "By\nSimone Albani".upper(), 0)
        pyxel.text(
            20, 72, "Using Pyxel\ngithub.com/kitao/pyxel", 0)
        pyxel.rect(58, 110, 70, 20, 0)
        pyxel.text(62, 115, "OK (press ENTER)", 9)

    def update(self, app):
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.read = 1
        if pyxel.btnp(pyxel.KEY_ENTER) and self.read:
            self.read = 0
            time.sleep(0.5)
            app.state = 0


class App:
    def __init__(self):
        pyxel.init(150, 150, caption="Build-a-Bug", fps=15)
        self.loadImage()
        self.game = Game()
        self.menu = Menu()
        self.incipit = Incipit()
        self.credits = Credits()
        self.collection = Collection(self.game)
        self.store = Store(self.game)
        self.youlost = YouLost()
        # [menu,credits,incipit,collection,store,youlost,youwon]
        self.state = 0
        pyxel.run(self.update, self.draw)

    def loadImage(self):
        for i in range(NUMBEROFBUGSMODEL):
            pyxel.image(0).load(0, i*16, f"bugs/{i+1}.png")
        pyxel.image(0).load(16, 0, f"logo.png")
        pyxel.image(0).load(16, 32, "bugcoin.png")
        pyxel.image(0).load(16, 64, "lid.png")
        pyxel.image(0).load(64, 32, "leg.png")

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.state == 0:
            self.menu.update(self)
        if self.state == 1:
            self.credits.update(self)
        if self.state == 2:
            self.incipit.update(self)
        if self.state == 3:
            self.collection.update(self)
        if self.state == 4:
            self.store.update(self, self.collection)
        if self.state == 5:
            self.youlost.update(self)
        if pyxel.btnp(pyxel.KEY_R):
            self.game = Game()
            self.store = Store(self.game)
            self.collection = Collection(self.game)
            self.state = 0

    def draw(self):
        pyxel.cls(0)
        if self.state == 0:
            self.menu.draw()
        if self.state == 1:
            self.credits.draw()
        if self.state == 2:
            self.incipit.draw()
        if self.state == 3:
            self.collection.draw()
        if self.state == 4:
            self.store.draw()
        if self.state == 5:
            self.youlost.draw()


App()
