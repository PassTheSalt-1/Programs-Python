"Simple program to practice class declarations "

class Counter: ## Creates the class
    def __init__(self): ## initialize the class 
        self.count = 0 ## create count, state belongs to an object not the program.

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0 
## create increment and reset logic

c = Counter() ## set alias for class


c.increment() ## access the increment method INSIDE the Counter class and increment 
c.increment()
print(c.count) ## print count
c.reset() ## reset to 0
print(c.count) ## print zeroized count