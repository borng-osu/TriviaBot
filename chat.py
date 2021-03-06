import random
import json

from nltk.tokenize import destructive
import torch
import wikipedia
from model import NeuralNet
from input_handler import word_bag, tokenize
import cryptocompare
from datetime import date
from factoid import date_factoid, quantity_factoid

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('text-data/conversation.json', 'r') as con:
    convo = json.load(con)

FILE = "text-data/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "TriviaBot"

def convert(sentence):
    origin = ""
    dest = ""

    for i in range(1, len(sentence)):
        if sentence[i] == "to":
            continue
        else:
            if not origin:
                origin = sentence[i].upper()
            elif not dest:
                dest = sentence[i].upper()
        
    check = cryptocompare.get_price(origin, currency=dest)

    if check:
        conversion = str(check[origin][dest]) + dest
        return conversion
    else:
        check = cryptocompare.get_price(dest, currency=origin)
        if not check:
            return "Hmm, can't convert " + origin + " to " + dest
        else:
            conversion = str(check[dest][origin]) + "  " + origin
            return conversion

def summarize(sentence):
    search_term = ""

    for i in range(len(sentence)):
        search_term += sentence[i] + " "

    if wikipedia.search(search_term) is None:
        return "Hmm, even I don't know what that is."

    return wikipedia.summary(search_term, sentences=3)   

def chat(msg):
    
    sentence = tokenize(msg)

    if sentence[0].lower() == "quiz":
        if sentence[1].lower() == "again":
            return "How many countries are in Asia?"
        return "How many episodes are in The Simpsons?"

    if sentence[0].lower() == "706":
        return "Correct!"

    if sentence[0].lower() == "50":
        return "Sorry, the answer is 49 countries."

    if sentence[0].lower() == "date" or sentence[0].lower() == "today" or sentence[0].lower() == "today's":
        return "Today is " + date.today().strftime("%B %d, %Y")
        
    if sentence[0].lower() == "convert":
        return convert(sentence)

    if sentence[0].lower() == "how" and sentence[1].lower() == "many":
        return quantity_factoid(sentence)

    if sentence[0].lower() == "when":
        return date_factoid(sentence)
        
    if sentence[0].lower() == "what" and (sentence[1] == "is" or sentence[1] == "are"):
        sentence = sentence[2:len(sentence) - 1]
        return summarize(sentence)
        
    X = word_bag(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for type in convo["types"]:
            if tag == type["tag"]:
                return random.choice(type['response'])
    return "I don't understand, nimrod."

