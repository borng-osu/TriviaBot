from bs4 import GuessedAtParserWarning
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from input_handler import *

count_q = ["how", "many", "are", "in"]
date_q = ["when", "did", "was"]

def date_factoid(w):

    if w[len(w) - 1] == "?":
        w.pop()

    check = [0 for i in w]
    q_set = date_q

    for i in range(len(w)):
        if w[i].lower() in q_set:
            check[i] = 1
    
    query = []

    for i in range(len(w)):
        if check[i] == 0:
            query.append(w[i])

    verb = [query.pop().lower()]

    if query:
        page = ""
        for i in range(len(query)):
            page += query[i] + " "
        print(page)
        try: 
            if wikipedia.search(page) == None:
                return "Could not find a wikipedia page for " + page
            
            summary = wikipedia.summary(page)

            q_checker = tokenize(summary)
            found = 0
            year = 0
            for i in range(len(q_checker)):
                if found and q_checker[i].isnumeric():
                    year = int(q_checker[i])
                    break
                if verb[0].lower() == q_checker[i].lower():
                    found = 1
                if q_checker[i] == "." and found:
                    break

            if not year:
                whole_page = wikipedia.page(page)

                scraped = tokenize(whole_page.content)

                scraped = scraped[len(q_checker):]

                found = 0
                for i in range(len(scraped)):
                    if found and scraped[i].isnumeric():
                        year = int(scraped[i])
                        break
                    if scraped[i].lower() == verb[0]:
                        found = 1
                    if scraped[i] == "." and found:
                        break

                if not year:
                    return "Sorry, I couldn't find the date on the Wikipedia page for " + page
            
            return page + "was " + verb[0] + " in " + str(year)

        except GuessedAtParserWarning:
            return "Uh oh, something went wrong in checking the quantity."
        except DisambiguationError:
            return "Uh oh, something went wrong in checking the quantity."
        except PageError:
            return "Looks like the Wikipedia module failed. Sorry!"
            

def quantity_factoid(w):

    if w[len(w) - 1] == "?":
        w.pop()

    check = [0 for i in w]
    q_set = count_q

    for i in range(len(w)):
        if w[i].lower() in q_set:
            check[i] = 1
    
    quantity = []
    entry = []
    q_flag = 0
    e_flag = 0

    for i in range(len(w)):
        if i < len(w) - 1:
            if check[i+1] == 0:
                if not q_flag:
                    q_flag = 1
                elif not e_flag:
                    e_flag = 1
        if check[i] == 0 and e_flag:
            entry.append(w[i])
        elif check[i] == 0 and q_flag:
            quantity.append(w[i])

    if entry:
        page = ""
        for i in range(len(entry)):
            page += entry[i] + " "
        
        try:
            if wikipedia.search(page) is None:
                return "Hmm, even I don't can't find a summary for " + page

            summary = wikipedia.summary(page)

            q_checker = tokenize(summary)

            answer = ""
            for i in range(len(q_checker)):
                if q_checker[i].lower() == quantity[0]:
                    if q_checker[i-1].isnumeric():
                        answer = q_checker[i-1] + " " + q_checker[i]
                        break
                    else:
                        continue
            
            if not answer:
                try:
                    whole_page = wikipedia.page(page)
                    
                    scraped = whole_page.content

                    scrape_check = tokenize(scraped)

                    response = ""
                    for i in range(len(scrape_check)):
                        if scrape_check[i].lower() == quantity[0]:
                            if scrape_check[i-1].isnumeric():
                                response = scrape_check[i-1] + " " + scrape_check[i]
                                break
                            else:
                                continue
                    
                    if not response:
                        return "Sorry, I couldn't find anything on the Wikipedia page for " + page

                    return response

                except PageError:
                    return "Sorry, I'm running into an issue with the Wikipedia module for Python."
            
            return answer


        except GuessedAtParserWarning:
            return "Uh oh, something went wrong in checking the quantity."
        except DisambiguationError:
            return "Uh oh, something went wrong in checking the quantity."
        except PageError:
            return "Looks like the Wikipedia module failed. Sorry!"
    
    else:
        return "Uh oh, something went wrong in checking the quantity."

def determine_type(w):

    if w[len(w) - 1] == "?":
        w.pop()

    count = False
    time = False

    for i in range(1):
        if w[0].lower() == "how":
            count = True
        elif w[0].lower() == "when":
            time = True

    if time:
        date_factoid(w)
    elif count:
        quantity_factoid(w)
    else:
        return "Something went wrong with your factoid query."
