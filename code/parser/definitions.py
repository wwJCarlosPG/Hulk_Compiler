import json

class Symbol(object):
    def __init__(self, name, grammar):
        self.Name = name
        self.Grammar = grammar

    def __str__(self):
        return self.Name

    def __repr__(self):
        return repr(self.Name)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(self, other)

        raise TypeError(other)

    def __or__(self, other):

        if isinstance(other, (Sentence)):
            return SentenceList(Sentence(self), other)

        raise TypeError(other)

    @property
    def IsEpsilon(self):
        return False

    def __len__(self):
        return 1
    

class NonTerminal(Symbol):
    def __init__(self, name, grammar):
        super().__init__(name, grammar)
        self.productions = []

    def __imod__(self, other):

        if isinstance(other, (Sentence)):
            p = Production(self, other)
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, tuple):
            assert len(other) > 1

            if len(other) == 2:
                other += (None,) * len(other[0])

            assert len(other) == len(other[0]) + 2, "Debe definirse una, y solo una, regla por cada símbolo de la producción"
            # assert len(other) == 2, "Tiene que ser una Tupla de 2 elementos (sentence, attribute)"

            if isinstance(other[0], Symbol) or isinstance(other[0], Sentence):
                p = AttributeProduction(self, other[0], other[1:])
            else:
                raise Exception("")

            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, Symbol):
            p = Production(self, Sentence(other))
            self.Grammar.Add_Production(p)
            return self

        if isinstance(other, SentenceList):

            for s in other:
                p = Production(self, s)
                self.Grammar.Add_Production(p)

            return self

        raise TypeError(other)

    @property
    def IsTerminal(self):
        return False

    @property
    def IsNonTerminal(self):
        return True

    @property
    def IsEpsilon(self):
        return False


class Terminal(Symbol):
    def __init__(self, name, grammar):
        super().__init__(name, grammar)

    @property
    def IsTerminal(self):
        return True

    @property
    def IsNonTerminal(self):
        return False

    @property
    def IsEpsilon(self):
        return False

class EOF(Terminal):
    def __init__(self, Grammar):
        super().__init__('$', Grammar)



class Sentence(object):
    def __init__(self, *args):
        self._symbols = tuple(x for x in args if not x.IsEpsilon)
        self.hash = hash(self._symbols)

    def __len__(self):
        return len(self._symbols)

    def __add__(self, other):
        if isinstance(other, Symbol):
            return Sentence(*(self._symbols + (other,)))

        if isinstance(other, Sentence):
            return Sentence(*(self._symbols + other._symbols))

        raise TypeError(other)

    def __or__(self, other):
        if isinstance(other, Sentence):
            return SentenceList(self, other)

        if isinstance(other, Symbol):
            return SentenceList(self, Sentence(other))

        raise TypeError(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return ("%s " * len(self._symbols) % tuple(self._symbols)).strip()

    def __iter__(self):
        return iter(self._symbols)

    def __getitem__(self, index):
        return self._symbols[index]

    def __eq__(self, other):
        return self._symbols == other._symbols

    def __hash__(self):
        return self.hash

    @property
    def IsEpsilon(self):
        return False


class SentenceList(object):
    def __init__(self, *args):
        self._sentences = list(args)

    def Add(self, symbol):
        if not symbol and (symbol is None or not symbol.IsEpsilon):
            raise ValueError(symbol)

        self._sentences.append(symbol)

    def __iter__(self):
        return iter(self._sentences)

    def __or__(self, other):
        if isinstance(other, Sentence):
            self.Add(other)
            return self

        if isinstance(other, Symbol):
            return self | Sentence(other)


class Epsilon(Terminal, Sentence):
    def __init__(self, grammar):
        super().__init__('epsilon', grammar)

    def __str__(self):
        return "e"

    def __repr__(self):
        return 'epsilon'

    def __iter__(self):
        yield from ()

    def __len__(self):
        return 0

    def __add__(self, other):
        return other

    def __eq__(self, other):
        return isinstance(other, (Epsilon,))

    def __hash__(self):
        return hash("")

    @property
    def IsEpsilon(self):
        return True

class Production(object):
    def __init__(self, nonTerminal, sentence):
        self.Left = nonTerminal
        self.Right = sentence

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right

    def __eq__(self, other):
        return isinstance(other, Production) and self.Left == other.Left and self.Right == other.Right

    def __hash__(self):
        return hash((self.Left, self.Right))

    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon


class AttributeProduction(Production):
    def __init__(self, nonTerminal, sentence, attributes):
        if not isinstance(sentence, Sentence) and isinstance(sentence, Symbol):
            sentence = Sentence(sentence)
        super(AttributeProduction, self).__init__(nonTerminal, sentence)
        self.attributes = attributes

    def __str__(self):
        return '%s := %s' % (self.Left, self.Right)

    def __repr__(self):
        return '%s -> %s' % (self.Left, self.Right)

    def __iter__(self):
        yield self.Left
        yield self.Right


    @property
    def IsEpsilon(self):
        return self.Right.IsEpsilon

    # sintetizar en ingles??????, pending aggrement
    def syntetice(self):
        pass

