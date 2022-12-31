from dataclasses import dataclass


@dataclass
class Quote:
    author: str = None
    content: str = ""


def load_data():
    quotes_list = []
    with open("data/quotes.txt", "r", encoding="utf-8") as file:
        line = file.readline()
        q = Quote()
        while line:
            if line != "----\n":
                if "    " in line:
                    q.author = line.replace("\n", "")
                else:
                    q.content += line
            if line == "----\n":
                quotes_list.append(q)
                q = Quote()

            line = file.readline()

    return quotes_list
