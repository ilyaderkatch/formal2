import copy

special_simb = "$" # S стартовый вспомогательный символ, $ - новый, * - пустое слово
start_simb = "S"
empty_symb = "*"

def MyHash (str):
    a = 1
    for i in str:
        a *= ord(i) + 1
    return a

class Rule:
    def __init__(self, symb, val, ind, start_ind):
        self.symbol = symb
        self.value = val
        self.point_index = ind
        self.start_index = start_ind

    def __str__(self):
        return "{} -> {} and {} {}".format(self.symbol, self.value, self.point_index, self.start_index)

    def __hash__(self):
        return MyHash(self.symbol) * MyHash(self.value)

    def __eq__(self, other):
        return self.start_index == other.start_index and \
               self.point_index == other.point_index and \
               self.value == other.value and self.symbol == other.symbol



def IsCapital(letter):
    return 'A' <= letter <= 'Z' or letter == special_simb

def IsLowercase(letter):
    return 'a' <= letter <= 'z' or letter == empty_symb

def input_data():
    res = list()
    num_of_rules = int(input())
    for i in range(num_of_rules):
        str = input()
        res.append(str)
    return res

def input_grammar(l):
    res = set()
    for str in l:
        str = str.split()
        res.add(Rule(str[0], str[-1], 0, 0))
    return res

class Algo:

    def __init__(self, input_grammar):
        self.rules = {special_simb : start_simb}
        set_of_rules = input_grammar
        while len(set_of_rules) != 0:
            s = set_of_rules.pop()
            symbol = s.symbol
            new_set = {s.value}
            old_set_of_rules = set_of_rules.copy()
            for a in old_set_of_rules:
                if a.symbol == symbol:
                    new_set.add(a.value)
                    set_of_rules.remove(a)
            self.rules[symbol] = frozenset(new_set)
        self.correct_steps = list()

    def predict(self, word):
        self.correct_steps.append({Rule(special_simb, start_simb, 0, 0)})
        for i in range(len(word) + 2):
            self.correct_steps.append(set())

        len_i = 0
        while len_i != len(self.correct_steps[0]):
            len_i = len(self.correct_steps[0])
            self.Complete(0, word)
            self.Predict(0)

        for i in range(1, len(word) + 1):
            self.Scan(i - 1, word)
            len_i = 0
            while len_i != len(self.correct_steps[i]):
                len_i = len(self.correct_steps[i])
                self.Complete(i, word)
                self.Predict(i)
        ans = Rule(special_simb, start_simb, 1, 0) in self.correct_steps[len(word)]
        self.Clear()
        return ans

    def Predict(self, cur_ind):
        copy_steps = self.correct_steps[cur_ind].copy()
        for i in copy_steps:
            if len(i.value) != i.point_index and IsCapital(i.value[i.point_index]):
                symb = i.value[i.point_index]
                if symb in self.rules.keys():
                    for r in self.rules[symb]:
                        self.correct_steps[cur_ind].add(Rule(symb, r, 0, cur_ind))

    def Scan(self, cur_ind, word):
        copy_steps = self.correct_steps[cur_ind].copy()
        for i in copy_steps:
            if len(i.value) != i.point_index and i.value[i.point_index] == word[cur_ind]:
                self.correct_steps[cur_ind + 1].add(Rule(i.symbol, i.value, i.point_index + 1, i.start_index))

    def Complete(self, cur_ind, word):
        copy_steps = copy.deepcopy(self.correct_steps)
        for i in copy_steps[cur_ind]:
            if len(i.value) != i.point_index and i.value[i.point_index] == empty_symb:
                self.correct_steps[cur_ind].add(Rule(i.symbol, i.value, i.point_index + 1, i.start_index))
            if len(i.value) == i.point_index:
                for j in copy_steps[i.start_index]:
                    if len(j.value) != j.point_index and j.value[j.point_index] == i.symbol:
                        self.correct_steps[cur_ind].add(Rule(j.symbol, j.value, j.point_index + 1, j.start_index))

    def Clear(self):
        self.correct_steps.clear()

if __name__ == '__main__':
    algo = Algo(input_grammar(input_data()))
    print(algo.predict(input()))
