def write(msg, source):
    with open('chat_log.txt', 'a') as outlog:
        outlog.write(source + ': ' + msg + '\n')
        print("Something was written!")

def read():
    try:
        with open('chat_log.txt', 'r') as log:
            for line in log:
                cur_line = line.strip()
                if "TriviaBot: " in cur_line:
                    print("Blue")
                else:
                    print("Red")

    except FileNotFoundError:
        print("Oops! No history.")

def check():
    try:
        

read()