import wikipedia
from input_handler import *

string = "How many states are in the United States?"

w = tokenize(string)
print(w)

query = False
count_q = ["how", "many", "are", "in"]
date_q = ["when", "did", "was"]
person_q = ["who"]

if w[len(w) - 1] == "?":
    query = True
    w.pop()
    print(w)

check = [0 for i in w]

c = False
d = False
p = False

print(query)
print(check)

q_set = []

if query:
    for i in range(2):
        if w[0].lower() == "how":
            q_set = count_q
        if w[0].lower() == "when":
            q_set = date_q
        if w[0].lower() == "who":
            q_set = person_q
    print(q_set)
    print(c)
    for i in range(len(w)):
        if w[i].lower() in q_set:
            check[i] = 1
    print(check)
    variables = []
    for i in range(len(w)):
        if check[i] == 0:
            variables.append(w[i])
    print(variables)