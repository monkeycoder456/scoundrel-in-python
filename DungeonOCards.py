import PokerNight
import random
import os

class DungeonOCards:
    """
    scoundrel, but on a COMPUTER *gasp*!!

    attribs
        * Dungeon : Deck
        * Room : list of Cards
        * Discard : Deck
        * Sword : Deck
        * health : int (0 <-> 20)
    """
    def __init__(self) -> None:
        """creates all the things we need"""
        self.Dungeon = PokerNight.Deck(0)
        temp = [PokerNight.Deck.createSuitedDeck(1),PokerNight.Deck.createSuitedDeck(2),PokerNight.Deck.createSuitedDeck(3),PokerNight.Deck.createSuitedDeck(4)]
        temp[0].removeFaceCards()
        temp[0].removeSpecificPipValue(1)
        temp[1].removeFaceCards()
        temp[1].removeSpecificPipValue(1)

        self.Dungeon + temp[0]
        self.Dungeon + temp[1]
        self.Dungeon + temp[2]
        self.Dungeon + temp[3]

        self.Room = list() # length never to exceed 4
        self.Discard = PokerNight.Deck(0)
        self.Sword = PokerNight.Deck(0)
        self.health = 20
        self.hasRanBefore = False # you cannont run twice in a row (vanilla rule)
        self.hasHealedBefore = False # you cannont heal in the same room twice (vanillia rule)
        self.swordIsClean = True #if sword deck has only 1 element (diamond) it is true, else false
        self.canProceed = False #if there is only one element in the room array, true, else false
        self.monsterList = ["slime", "goblin", "orc", "rogue swordsman", "hopping zombie", "sentient boulder", "haunted armor", "crayon mimic", "coked-up wizard", "Python"]
        self.sillymessage = ["you stare at the wall blankly.", "you pick your nose.", "you whistle a song you heard on the radio.", "you juggle some stones you see on the ground.", "you space out for a while.", "you think about that comment that girl made to you yesterday.", "you feel as if you need iron tablets.", "you kneel down and graffiti a small doodle on the stone floor.","you sneeze.","you suck your thumb.","you do a few push-ups", "you shout like a little girl.", "your stomach gurgles loudly.","you count on your fingers to pass the time.","you fart.","you drool onto the floor."]
    
    def FillOutRoom(self) -> None:
        """fills the room array with card until it has four elements"""
        while(len(self.Room) < 4):
            self.Room.append(self.Dungeon.draw())
        
    def replaceBlankCards(self) -> None:
        """replaces blanks with real cards"""
        for index in range(4):
            focus = self.Room[index]
            if focus.pips == 0:
                self.Room[index] = self.Dungeon.draw()

    def FillOutRoomEmpty(self):
        """fills the room with a blank card so errors dont happen"""
        while(len(self.Room)<4):
            self.Room.append(PokerNight.Card(0,0))

    def runAwayRoom(self):
        """takes cards in the room and puts them at bottom of deck"""
        self.Dungeon.flip()
        while len(self.Room) != 0:
            card = self.Room.pop()
            if card.pips != 0:
                self.Dungeon.put(card)
        self.Dungeon.flip()
        self.FillOutRoom()

    def roomGet(self, index) -> str:
        # * 1 = heart
        # * 2 = diamond
        # * 3 = spades
        # * 4 = clubs
        """gets the thing on the floor to look pretty for user"""
        inspect = self.Room[index]
        # print(inspect)
        strung = ''
        # if inspect 
        if inspect.pips == 0:
            return "   "
        match inspect.getsuit():
            case 1:
                strung += "<3 "
            case 2:
                strung += "<> "
            case 3:
                strung += "<- "
            case 4:
                strung += "o- "
        strung += str(inspect.getpips())
        return strung

    def swordStatusGet(self) -> str:
        if self.swordIsClean == True:
            return "O"
        else:
            return "X"

    def swordpowerget(self) -> str:
        exam = self.Sword.look()

        if exam.suit == 0:
            return "0"
        else:
            return exam.pips
    
    def thingsInRoom(self) -> int:
        """returns the number of non-blank cards in the room"""
        count = 0
        for card in self.Room:
            if card.pips != 0:
                count += 1
        return count

    def display(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        """print me bruh"""
        strong = ''
        strong += ' ________________________\n' 
        strong += '|\         ___          /|\n'
        strong += '| \       |   |        / |\n'
        strong += '|  \__5___|{:^3}|_______/  |\n'.format(self.Dungeon.getsize())
        strong += '| 1|      {:^5}       |  |\n'.format(self.roomGet(0))
        strong += '| 2|      {:^5}       |  |\n'.format(self.roomGet(1))
        strong += '| 3|      {:^5}       |  |\n'.format(self.roomGet(2))
        strong += '| 4|      {:^5}       |  |\n'.format(self.roomGet(3))
        strong += '|__|__________________|__|\n'
        strong += '\         _____          /\n'
        strong += ' \________|{:^3}|_________/\n'.format(self.Discard.getsize())
        strong += '     _                   \n'
        strong += ' ___| |_________________\n'
        strong += '|   |{}| HP = {:^2}         \\\n'.format(self.swordStatusGet(), self.health)
        strong += '|___| |_POW_=_{:^2}________/\n'.format(self.swordpowerget())
        strong += '    |_|                    '
        print(strong)

    def gameLoop(self) -> None:
        #to begin, fill the room array, only with 4 cards
        #then, the player must choose from the room array or dungeon deck
        #dungeon deck option only works if room array only has one/no element(s)
        #if dungeon deck condition is met, fill the room array, reset hasRanBefore and hasHealedBefore flags
        #if the player chose one of the four cards in the room array do the following
        #if the card was hearts, heal the player based on pips, to a max of 20, then discard
            #mark the hasHealedBefore Flag to prevent multiple heals in one room
        #if the card was diamonds, check if the user has a Sword (aka sword deck has stuff), if yes, empty sword and put that card there
            #if the user has no sword, just give the card to the user
        #if the card was a spade or club, do some more complex logic

        #battle flow chart

        #ask user if they want to use their sword or not
        #if not: the user takes full damage (equal to pips of card) and the card is discarded, END LOGIC
        #if yes: check if the user's sword is "clean" (aka only the diamond is in the deck)
            #if yes: the user takes the difference of the the monster's pips against the swords pips (no damage is sword is stronger), the monster is put onto the sword deck, the sword is not clean
            #if no: check if the current monster on the top of the sword deck's pips are higher then or equal to the attacking monster
                #if yes: user takes no damage and that monster is placed ontop of the sword deck
                #if no: user is forced to not use their sword and takes full damage
        print("welcome to scoundrel!")
        self.Dungeon.shuffle(5)

        self.FillOutRoom()
        self.display()
        while not((self.health == 0) or (self.Dungeon.getsize() == 0 and self.thingsInRoom() == 0)):
            inn = input("1-4 to pick a room object, 5 to go to next room\n")
            #5 selected logic
            if inn.isdigit() and int(inn) == 5:
                if self.canProceed:
                    print("you explore deeper")
                    self.hasHealedBefore = False
                    self.hasRanBefore = False
                    self.replaceBlankCards()
                    #loop back to roomfilling and take input again
                else:
                    print("you can only move on if there is only one object in the room!!")
                    inn = input("do you want to try to run away? Y/N\n")
                    if str.capitalize(inn) == 'Y':
                        if self.hasRanBefore == False and self.thingsInRoom() == 4:
                            print("you successfully ran away from the room!!\nthough what lurks in it will find you later.")
                            self.runAwayRoom()
                            self.hasHealedBefore = False
                            self.hasRanBefore = True
                            #use a method to flush the room of the contents and put those at the bottom of the deck.
                            #loop back to roomfilling and take input again
                        elif self.hasRanBefore == True:
                            print("you cannot run away twice in a row!!\nclear the room until one object remains to move on.")
                            #loop back to grab input again
                        else:
                            print("you already stepped into the threshold by interacting with an object, handle the remaining objects.")
                    elif str.capitalize(inn) == 'N':
                        print("you decide to remain in the room.")
                        #loop back to grab input again
                    #loop back to grab input again
                    else:
                        print("you decide to remain in the room.\nalso next time don't mash your keyboard.")
                        #loop back to grab input again
                    #loop back to grab input again
            #1-4 logic
            elif inn.isdigit() and (int(inn) > 0 and int(inn) < 5):
                inn = int(inn)
                focus = self.Room[inn-1]
                match focus.suit:
    #         * 1 = heart
    #         * 2 = diamond
    #         * 3 = spades
    #         * 4 = clubs
                    case 1:
                        print("you go for the potion on the ground.")
                        if self.hasHealedBefore == False:
                            self.health = min(20,self.health + focus.pips)
                            self.hasHealedBefore = True
                            print("you feel invigorated!!\nbut now you feel the weight of the potion sloshing in your belly...")
                            self.Discard.put(self.Room.pop(inn-1))
                            #loop back to grab input again
                        else:
                            print("you are too full to heal more.\nmaybe you will feel lighter in the next room.")
                            pinn = input("want to smash the bottle? this does nothing but empty the room up. Y\\N")
                            if str.capitalize(pinn) == 'Y':
                                print("with a loud CRASH you smash the bottle on the ground.\n the red liquid splashing everywhere.")
                                self.Discard.put(self.Room.pop(inn-1))
                            elif str.capitalize(pinn) == 'N':
                                print("you show mercy to the potion and back off.")
                            else:
                                print("you show mercy to the potion and back off. also next time don't slap the keyboard.")
                            #loop back to grab input again
                    case 2:
                        print("you go for the sword on the ground.")
                        if self.Sword.getsize() == 0:
                            print("you finally have a sword!")
                            self.Sword.put(self.Room.pop(inn-1))
                            #loop back to grab input again
                        else:
                            pinn = input("do you want to toss out your old sword for the new one? Y\\N")
                            if str.capitalize(pinn) == 'Y':
                                print("You throw your old sword to the side,\nnow you have a new blade!!")
                                self.swordIsClean = True
                                while self.Sword.getsize() != 0:
                                    self.Discard.put(self.Sword.draw())
                                self.Sword.put(self.Room.pop(inn-1))
                                #loop back to grab input again
                            elif str.capitalize(pinn) == 'N':
                                print("You leave the sword alone.")
                                #loop back to grab input again
                            else:
                                print("You leave the sword alone. next time don't fat finger keys.")
                                #loop back to grab input again
                    case 3 | 4:
                        print("you approach the {}".format(random.choice(self.monsterList)))
                        if self.Sword.getsize() == 0:
                            print("you try to fight the monster with just your hands.\nthe monster roughs you up!!")
                            self.health = self.health - focus.pips
                            self.Discard.put(self.Room.pop(inn-1))
                                #loop back to grab input again
                                #NOTE: check if the user has died from this while looping.
                        else:
                            pinn = input("do you want to use your sword? Y\\N ")
                            if str.capitalize(pinn) == 'Y':
                                if self.swordIsClean == True:
                                    print("your clean blade... ",end='')
                                    if self.Sword.look().pips >= focus.pips:
                                        print("slays the monster with ease!!")
                                    else:
                                        print("slays the monster but it manages to damage you.")
                                        self.health = self.health - (focus.pips - self.Sword.look().pips)
                                    print("you sword is now dirty.\nyou can only slay a monster who is weaker or just as strong than the one you just defeated.")
                                    self.Sword.put(self.Room.pop(inn-1))
                                    self.swordIsClean = False
                                    #loop back to grab input again
                                    #NOTE: check if the user has died from this while looping.
                                else:
                                    if self.Sword.look().pips >= focus.pips:
                                        print("your blade slays the monster!!\nyou can only slay a monster who is weaker or just as strong than the one you just defeated.")
                                        self.Sword.put(self.Room.pop(inn-1))
                                        #loop back to grab input again
                                        #NOTE: check if the user has died from this while looping.
                                    else:
                                        print("your sword is too weak to defeat the monster.\nyou already commited and use your hands instead,\nthe monster roughs you up!!")
                                        self.health = self.health - focus.pips
                                        self.Discard.put(self.Room.pop(inn-1))
                                        #loop back to grab input again
                            elif str.capitalize(pinn) == 'N':
                                print("you try to fight the monster with just your hands.\nthe monster roughs you up!!")
                                self.health = self.health - focus.pips
                                self.Discard.put(self.Room.pop(inn-1))
                                #loop back to grab input again
                                #NOTE: check if the user has died from this while looping.
                            else:
                                print("you try to fight the monster with just your hands.\nthe monster roughs you up!!\nthe monster also comments on your keyboard etiquette...")
                                self.health = self.health - focus.pips
                                self.Discard.put(self.Room.pop(inn-1))
                                #loop back to grab input again
                                #NOTE: check if the user has died from this while looping.
                    case _: #for when the rooms card is a blank
                        print(random.choice(self.sillymessage))
            #nonsense input logic
            else:
                print(random.choice(self.sillymessage))
            self.FillOutRoomEmpty()

            if self.thingsInRoom() == 1 or self.thingsInRoom() == 0:
                self.canProceed = True
            else:
                self.canProceed = False
            self.display()
            # for thing in self.Room:
            #     print(thing,end='')
            #     print()
        if self.health == 0:
            print("YOU DIED!!")
            input()
        if self.Dungeon.getsize() == 0:
            print("YOU SURVIVED AND MADE IT OUT ALIVE!!")
            input()

game = DungeonOCards()
game.gameLoop()