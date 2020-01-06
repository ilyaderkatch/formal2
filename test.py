import pytest
import main

def test_basic_func():
    assert main.IsCapital("C") == True
    assert main.IsCapital("c") == False
    assert main.IsLowercase("z") == True
    assert main.IsLowercase("*") == True
    assert main.input_grammar(["S -> abS", "S -> *"]) == {main.Rule("S", "abS", 0, 0), main.Rule("S", "*", 0, 0)}

def test_algo_init():
    algo = main.Algo(main.input_grammar(["S -> aSbS", "S -> *"]))
    assert algo.rules == {main.special_simb : "S", "S" : {"aSbS", "*"}}
    assert algo.correct_steps == list()

def test_erli_predict():
    algo = main.Algo(main.input_grammar(["S -> aS", "S -> *"]))
    algo.correct_steps.append({main.Rule("$", "S", 0, 0)})
    algo.Predict(0)
    assert algo.correct_steps[0] == {main.Rule("$", "S", 0, 0), main.Rule("S", "aS", 0, 0),
                                     main.Rule("S", "*", 0, 0)}

def test_erli_complete():
    algo = main.Algo(main.input_grammar(["S -> aS", "S -> *"]))
    algo.correct_steps.append({main.Rule("$", "S", 0, 0), main.Rule("S", "aS", 0, 0),
                               main.Rule("S", "*", 0, 0)})
    algo.Complete(0, "aaa")
    assert algo.correct_steps[0] == {main.Rule("$", "S", 0, 0), main.Rule("S", "aS", 0, 0),
                                     main.Rule("S", "*", 1, 0), main.Rule("S", "*", 0, 0)}
    algo.Complete(0, "aaa")
    assert algo.correct_steps[0] == {main.Rule("$", "S", 0, 0), main.Rule("S", "aS", 0, 0),
                                     main.Rule("S", "*", 1, 0), main.Rule("S", "*", 0, 0),
                                     main.Rule("$", "S", 1, 0)}

def test_erli_scan():
    algo = main.Algo(main.input_grammar(["S -> aS", "S -> *", "S -> aaS"]))
    algo.correct_steps.append({main.Rule("$", "S", 0, 0), main.Rule("S", "aS", 0, 0),
                               main.Rule("S", "*", 0, 0), main.Rule("S", "aaS", 0, 0)})
    algo.correct_steps.append(set())
    algo.Scan(0, "aaa")
    assert algo.correct_steps[1] == {main.Rule("S", "aS", 1, 0), main.Rule("S", "aaS", 1, 0)}

def test_algo_simple():
    algo = main.Algo(main.input_grammar(["S -> aS", "S -> *"]))
    assert algo.predict("aaaaaa") == True
    assert algo.predict("aaabaaca") == False
    assert algo.predict("") == True

def test_algo_bracket_sequence():
    algo = main.Algo(main.input_grammar(["S -> aSbS", "S -> *"]))
    assert algo.predict("abababab") == True
    assert algo.predict("aababaabbb") == True
    assert algo.predict("abaababbbabba") == False
    assert algo.predict("aabbb") == False
    assert algo.predict("") == True

def test_algo_gr1():
    algo = main.Algo(main.input_grammar(["S -> Sa", "S -> Dc", "S -> SaSb", "S -> C", "S -> Z", "C -> dD", "D -> *"]))
    assert algo.predict("cacbadacbb") == True
    assert algo.predict("dacadbb") == True
    assert algo.predict("cadbdacb") == False
    assert algo.predict("aacbbbdb") == False
    assert algo.predict("caadbbac") == False
    assert algo.predict("") == False

def test_algo_gr2():
    algo = main.Algo(main.input_grammar(["S -> C", "S -> CS", "C -> Dc", "D -> aDb", "D -> *"]))
    assert algo.predict("aabbcabcc") == True
    assert algo.predict("abcabcabcaabbc") == True
    assert algo.predict("abcabcccca") == False
    assert algo.predict("aacccb") == False
    assert algo.predict("") == False
