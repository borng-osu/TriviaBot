import wikipedia
from input_handler import *
import json
import numpy
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

# nltk.download('punkt')

input_train = []
response_train = []
all_words = []
tags = []
word_tag = []
with open('text-data/conversation.json', 'r') as con:
    convo = json.load(con)
for type in convo["types"]:
    tag = type["tag"]
    tags.append(tag)
    for input in type["input"]:
        token_w = tokenize(input)
        all_words.extend(token_w)
        word_tag.append((token_w, tag))
ign_punct = [".", "!", ",", ";", "?"]
print(all_words)
all_words = [stem(word) for word in all_words if word not in ign_punct]
all_words = sorted(set(all_words))
tags = sorted(set(tags))
print(tags)

    
for (pattern_sentence, tag) in word_tag:
    bag = word_bag(pattern_sentence, all_words)
    input_train.append(bag)
    response_train.append(tags.index(tag))

input_train = numpy.array(input_train)
response_train = numpy.array(response_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(input_train)
        self.x_data = input_train
        self.y_data = response_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(input_train[0])
learning_rate = 0.001
num_epochs = 1000


dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)

        outputs = model(words)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if (epoch + 1) % 100 == 0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

print(f'final loss, loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags    
}

FILE = "text-data/data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')