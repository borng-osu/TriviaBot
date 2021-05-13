import random
import json
import torch
import wikipedia
from model import NeuralNet
from input_handler import word_bag, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('conversation.json', 'r') as con:
    convo = json.load(con)

FILE = "data.pth"
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

def chat(msg):
    if msg == "How many states are in the United States?":
        return 50

    if msg == "quiz":
        return "How many states are in the United States?"

    if msg == "50":
        return "Correct!"

    if msg == "I don't know":
        return "Sorry, the answer is on July 1, 2002"
    
    sentence = tokenize(msg)

    if sentence[0].lower() == "what" and (sentence[1] == "is" or sentence[1] == "are"):
        sentence = sentence[2:len(sentence) - 1]

        search_term = ""

        for i in range(len(sentence)):
            search_term += sentence[i] + " "

        return wikipedia.summary(search_term, sentences=3)

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
