from django.db import models

# Create your models here.


class Poem:
    def __init__(self, id, title, description, score, category):
        self.id = id
        self.title = title
        self.description = description
        self.score = score
        self.category = category


poems = []

poem1 = Poem(
    1, "Jack and Jill", ["Jack and Jill,", "They got a pill,", "To experience thrill,"], 46, "humor")
poems.append(poem1)

poem2 = Poem(
    2, "Blue Eyes", ["Blue eyes,", "Blond hair,", "Pig stys,"], 5, "humor"
)
poems.append(poem2)

poem3 = Poem(
    3, "The Bush Pooper", ["There once was a man from Nantucket,", "Who liked to poop in a bucket,", "He ate a worm and saw a fern,", "And thought to himself,", " Screw it!"], -6, "humor"
)
poems.append(poem3)


class Suggestion:
    def __init__ (self, id, poem_id, line, score):
        self.id = id
        self.poem_id = poem_id
        self.line = line
        self.score = score

suggestions = []

suggestion1 = Suggestion(1, 3, "There once was a woman from Maine,",10)
suggestions.append(suggestion1)

suggestion2 = Suggestion(2, 3, "He hunched over the fern,",-2)
suggestions.append(suggestion2)

suggestion3 = Suggestion(3, 3, "He was stupid,",-7)
suggestions.append(suggestion3)





