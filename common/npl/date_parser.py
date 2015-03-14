from pyparsing import Keyword
from pyparsing import Word
from pyparsing import nums
from pyparsing import NoMatch
from pyparsing import MatchFirst
from pyparsing import CaselessLiteral
from pyparsing import Suppress
from pyparsing import Optional

from pluralize import pluralize
from datetime import datetime, timedelta

time_units = {
    "day": 1,
    "week": 7,
    "month": 31,
    "year": 365,
}

add_modifiers = {
    "couple": 2,
    "few": 3,
    "several": 4,
}

special = {
    "yesterday": 1,
    "last night": 1,
}


def pluralize_units(time_units):
    """
        update the give dict of time units and add plural entries.
    """
    plural_units = {}
    for key in time_units:
        plural_units[pluralize(key)] = time_units[key]
    time_units.update(plural_units)
    return time_units


def get_match_first(lits, parseAction=None):
    el = MatchFirst(NoMatch())
    for lit in lits:
        el = el.__ior__(lit)
    if parseAction:
        el.setParseAction(parseAction)
    return el


CL = CaselessLiteral
time_units = pluralize_units(time_units)


class DateRangeParser():

    def __init__(self):
        """
        access the start and end date the string represents
        """
        self.parser = self.setup()

    def parse(self, date_string):
        try:
            start, end = self.parser.parseString(date_string)[0]
        except Exception as e:
            print e
            # for now just return the last week
            return self.parse("last week")
        return start, end

    def combineTokens(self, tok):
        base_unit = tok['unit']
        total = base_unit * tok.get('multiply', 1)
        total += tok.get('add', 0)
        return total

    def parseRange(self, a, b, tok):
        delta = self.combineTokens(tok)
        start = datetime.today() - timedelta(days=delta)
        end = datetime.today() + timedelta(days=1)  # plus 1 to include today
        return (start, end)

    def parseMulti(self, a, b, tok):
        if tok:
            return int(tok[0])
        return 1

    def parseAdd(self, a, b, tok):
        return add_modifiers[tok[0]]

    def parseAgo(self, s, l, tok):
        ago = self.combineTokens(tok)
        delta = tok["unit"]
        start = datetime.today() - timedelta(days=ago)
        end = start + timedelta(days=delta)
        return (start, end)

    def setup(self):
        # some expressions that will be reused
        units = []
        for unit in time_units:
            units.append(Keyword(unit))
        units = get_match_first(units)
        units = units.setResultsName("unit")
        units.setParseAction(lambda s, l, tok: time_units[tok[0]])

        multiplier = Word(nums)
        multiplier = multiplier.setResultsName("multiply")
        multiplier.setParseAction(self.parseMulti)

        adder = []
        for add in add_modifiers:
            adder.append(CL(add))
        adder = get_match_first(adder)
        adder = adder.setResultsName("add")
        adder.setParseAction(self.parseAdd)
        modifier = (multiplier | adder)  # + FollowedBy(units)

        # ago
        #
        # e.g 5 days ago
        ago = Optional(modifier) + units + Suppress(Word("ago"))
        ago.setParseAction(self.parseAgo)

        # time range
        #
        # e.g in the lat 10 days
        time_range = Suppress(Optional(
            CL("in the"))) + \
            Suppress(Word("last") |
                     Word("past")) + \
            Optional(modifier) + \
            units
        time_range.setParseAction(self.parseRange)

        # special keyword handling
        #
        # e.g yesterday
        # only handles yesterday right now, maybe need to be modified to do
        # more
        special_expr = []
        for expr in special:
            special_expr.append(
                Keyword(expr).setParseAction(
                    lambda s, l, tok: special[tok[0]]))
        special_expr = get_match_first(special_expr)
        special_expr = special_expr.setResultsName("unit")
        special_expr.setParseAction(self.parseAgo)

        parser = (special_expr | ago | time_range)

        return parser


if __name__ == "__main__":
    tests = """in the last week
    last night
    last day
    last week
    last 2 days
    in the past week
    in the last 3 years
    2 days ago
    5 weeks ago
    few days ago
    in the last few days
    yesterday"""

    parser = DateRangeParser()

    for test in tests.splitlines():
        print "\n" + test.strip()
        start, end = parser.parse(test)
        print "Start: %s, End: %s" % (start, end)
