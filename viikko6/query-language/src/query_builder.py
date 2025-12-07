from matchers import All, And, HasAtLeast, HasFewerThan, Or, PlaysIn


class QueryBuilder:
    def __init__(self, matcher=None):
        self._matcher = matcher if matcher else All()

    def build(self):
        return self._matcher

    def plays_in(self, team):
        return QueryBuilder(And(self._matcher, PlaysIn(team)))

    def has_at_least(self, value, attr):
        return QueryBuilder(And(self._matcher, HasAtLeast(value, attr)))

    def has_fewer_than(self, value, attr):
        return QueryBuilder(And(self._matcher, HasFewerThan(value, attr)))

    def one_of(self, *queries):
        return QueryBuilder(Or(*[query.build() for query in queries]))
