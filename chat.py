import random
import json
import torch
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
while True:
    sentence = input("You: ")
    if sentence == "quit":
        break
    
    sentence = tokenize(sentence)
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
                print(f"{bot_name}: {random.choice(type['response'])}")
    else:
        print(f"{bot_name}: I don't understand, nimrod.")
