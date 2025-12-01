class Card:
    """
    suite defined by:
        * 1 = heart
        * 2 = diamond
        * 3 = spades
        * 4 = clubs

    suit automatically defines color
    
    pips defined by:
        * 1 through 10 = the typical numbers
        * 11 = jacks
        * 12 = queens
        * 13 = kings

    attribs
        * suit : int
        * pips : int
        * color : int

    methods
        * getsuit()
        * getpips()
        * getcolor()

    """

    def __init__(self, suit : int, pips : int) -> None:
        self.suit = suit
        self.pips = pips
        match suit:
            case 0:
                self.color = "NA"
            case 1:
                self.color = 'R'
            case 2:
                self.color = 'R'
            case 3:
                self.color = 'B'
            case 4:
                self.color = 'B'

    def __str__(self) -> str:
        stringy = ''
        stringy += self.color + ' '

        match self.suit:
            case 1:
                stringy += 'Heart' + ' '
            case 2:
                stringy += 'Diamond' + ' '
            case 3:
                stringy += 'Spade' + ' '
            case 4:
                stringy += 'Club' + ' '

        match self.pips:
            case 11:
                stringy += 'J'
            case 12:
                stringy += 'Q'
            case 13:
                stringy += 'K'
            case _:
                stringy += str(self.pips)
        return stringy

    def getpips(self) -> int:
        return self.pips

    def getsuit(self) -> int:
        return self.suit
    
    def getcolor(self) -> str:
        return self.color

class Deck:
    """
        a deck is a collection of card.
        this class is very simple on purpose to allow for 
        very specific subclasses.

        defining deck creation for specific instaces :
        * standard = 52
        * doublestandard = 104
        * empty = 0

        52 and 104 begin facing down
        0 begins facing up

        standard and double standard have what you would expect for a deck of cards, primaraly serve as 'before play' deck.
        empty has no cards, empty is intended to serve as a 'in play' deck.

        no parameters for type will default to creating a standard deck facing down.

    attribs
        * facing : bool (down = True, up = False)
        * pile : list (serving the roll of a proper stack)
        
    methods
        * shuffle()
        * sort()
        * getsize()
        * draw()
        * put()
        * flip()
        * static createpile()
        * look()
    """
    def __init__(self, type = 52) -> None:

        self.pile : list[Card]
        match type:
            case 0:
                self.facing = False
                self.pile = []
            case 52:
                self.facing = True
                self.pile = Deck.createpile(52)
            case 104:
                self.facing = True
                self.pile = Deck.createpile(104)

    def __add__(self, deck):
        """adding decks together puts the other deck ontop of this one"""
        for card in deck.pile:
            self.pile.append(card)

    def __str__(self) -> str:
        stringy = ''
        for numcard in enumerate(self.pile):
            if ((numcard[0] + 1) % 2) == 0:
                stringy += str(numcard[1]) + '\n'
            else:
                stringy += str(numcard[1]) + ', '
        
        return stringy
    
    @staticmethod
    def createpile(form) -> list:
        """creates a deck with standard or doublestandard ammount of cards.
        
            Args:
                form (int) : 52 or 104
            
            Returns:
                pile (list) : list of cards presorted
        """
        pile = []
        if form == 52:
            for suit in [4,3,2,1]:
                #suit loop
                for rank in range(1,14):
                #rank loop
                    pile.append(Card(suit, rank))

        if form == 104:
            for i in [0,1]:
                for suit in [4,3,2,1]:
                    #suit loop
                    for rank in range(1,14):
                    #rank loop
                        pile.append(Card(suit, rank))
        print(len(pile))
        return pile

    @staticmethod
    def createSuitedDeck(suitNumber):
        """creates a small deck of only one suit.
        suite defined by:
        * 1 = heart
        * 2 = diamond
        * 3 = spades
        * 4 = clubs
        
            Args:
                suitNumber (int) : 1,2,3,4
            
            Returns:
                deck (DECK) : list of cards of one suit
        """
        pile = []
        for rank in range(1,14):
            pile.append(Card(suitNumber, rank))
        turner = Deck(0)
        turner.pile = pile
        # print(turner)
        return turner

    def removeFaceCards(self) -> None:
        """gets rid of face cards. (11,12,13)"""
        temp = []
        for card in self.pile:
            if not(card.getpips() > 10):
                temp.append(card)
        self.pile = temp

    def removeSpecificPipValue(self, pipCount) -> None:
        """gets rid of a specific ranked cards
        
            Args:
            pipCount (int) = the specific card rank to disappear
        """
        temp = []
        for card in self.pile:
            if not(card.getpips() == pipCount):
                temp.append(card)
        self.pile = temp

    def getsize(self) -> int:
        """returns size of pile"""
        return len(self.pile)
    
    def flip(self) -> None:
        """ flips the pile order and facing direction"""
        self.pile.reverse()
        self.facing = not(self.facing)
    
    def shuffle(self, fineness) -> None:
        """randomly shuffle the deck, keep facing direction. if deck is empty it doesn't do anything.

            Args:
            fineness (int) = the ammount of iterations you want to do for even more shuffliness.
        """
        if len(self.pile) == 0:
            return None
        
        import random as r

        for i in range(0,fineness):
            auxpile = []
            while self.getsize() != 1:
                auxpile.append(self.pile.pop(r.randint(0,self.getsize()-1)))
            
            self.pile.extend(auxpile)
        
        del r
        
    def sort(self) -> None:
        """sorts the deck in this form:

            * clubs 1 -> K
            * spades 1 -> K
            * diamonds 1 -> K
            * hearts  1 -> K

            in other words : clubs on bottom hearts on top. 

            color sorted first, than suit, than rank.

            uses bucket sort, bucket sort, than built in sorted
            if deck is empty it doesn't bother with computing anything.
        """
        card : Card
        auxRed = []
        auxBlack = []

        if len(self.pile) == 0:
            return None

        #fist bucket sort : colors
        for card in self.pile:
            if card.getcolor() == 'R':
                auxRed.append(card)
            else:
                auxBlack.append(card)
        
        self.pile.clear()

        auxHeart = []
        auxDiamond = []

        #second bucket sort : suits
        for card in auxRed:
            if card.getsuit() == 1:
                auxHeart.append(card)
            else:
                auxDiamond.append(card)
        
        del auxRed

        auxSpade = []
        auxClub = []

        for card in auxBlack:
            if card.getsuit() == 3:
                auxSpade.append(card)
            else:
                auxClub.append(card)
        
        del auxBlack

        #built in sorted and insertion
        self.pile.extend(sorted(auxClub, key = lambda card : card.getpips()))
        self.pile.extend(sorted(auxSpade, key = lambda card : card.getpips()))
        self.pile.extend(sorted(auxDiamond, key = lambda card : card.getpips()))
        self.pile.extend(sorted(auxHeart, key = lambda card : card.getpips()))

    def draw(self) -> Card:
        """draws/pops the top card from the pile and returns it. if deck is empty return a blank card

            Returns:
            card (Card) = your card"""
        

        if len(self.pile) != 0:
            return self.pile.pop()
        else:
            return Card(0,0)
        
    def put(self, card : Card) -> None:
        """puts a card on the top of the deck

            Args:

            card (Card) : the card you want to put"""
        
        if type(card) == Card:
            self.pile.append(card)

    def look(self) -> Card:
        """looks at top card, doesn't remove it, top card is the last indexed card.
            if deck is empty it does nothing"""
        if len(self.pile) != 0:
            return self.pile[-1]
        else:

            Blank = Card(0,0)

            return Blank
    
    def arbitrarylook(self, negativeindex) -> Card:
        """looks at an arbitrary card in the deck. TAKES NEGATIVE INDEXES ONLY"""
        if (len(self.pile) != 0) and (len(self.pile) >= -1*negativeindex):
            return self.pile[negativeindex]
        else:

            Blank = Card(0,0)

            return Blank