class Item:

    def __init__(self, production, pos, lookaheads=[]):
        """
        Initialize an LR(0) item with the given production, position, and lookaheads.

        Parameters:
        - production: The production associated with the item.
        - pos: The current position within the production.
        - lookaheads: A list of symbols representing the lookaheads for the item.
        """
        self.production = production
        self.pos = pos
        self.lookaheads = frozenset(look for look in lookaheads)

    def __str__(self):
        s = str(self.production.Left) + " -> "
        if len(self.production.Right) > 0:
            for i,c in enumerate(self.production.Right):
                if i == self.pos:
                    s += "."
                s += str(self.production.Right[i])
            if self.pos == len(self.production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.lookaheads)[10:-1]
        return s

    def __repr__(self):
        return str(self)


    def __eq__(self, other):
        return (
            (self.pos == other.pos) and
            (self.production == other.production) and
            (set(self.lookaheads) == set(other.lookaheads))
        )

    def __hash__(self):
        return hash((self.production,self.pos,self.lookaheads))

    @property
    def IsReduceItem(self):
        """
        Check if the LR(0) item is a reduce item. Has the (.) at the end

        Returns:
        - bool: True if the item is a reduce item, False otherwise.
        """
        return len(self.production.Right) == self.pos

    @property
    def NextSymbol(self):
        """
        Get the next symbol in the production.

        Returns:
        - Symbol or None: The next symbol in the production, or None if at the end.
        """
        if self.pos < len(self.production.Right):
            return self.production.Right[self.pos]
        else:
            return None

    def NextItem(self):
        """
        Get the next LR(0) item.

        Returns:
        - Item or None: The next LR(0) item, or None if at the end.
        """
        if self.pos < len(self.production.Right):
            return Item(self.production,self.pos+1,self.lookaheads)
        else:
            return None

    def Preview(self, skip=1):
        """
        Get a list of possible previews of the LR(0) item.

        Parameters:
        - skip: The number of symbols to skip in the preview.

        Returns:
        - list: A list of possible previews for the LR(0) item.
        """
        unseen = self.production.Right[self.pos+skip:]
        return [ unseen + (lookahead,) for lookahead in self.lookaheads ]

    def Center(self):
        """
        Get a new LR(0) item with the position reset to the center.

        Returns:
        - Item: A new LR(0) item with the position reset to the center.
        """
        return Item(self.production, self.pos)