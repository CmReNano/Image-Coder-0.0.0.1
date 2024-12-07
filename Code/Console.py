class Console:
    def __init__(self):
        self.buffer = ""
        
    def log(self, Text):
        with open("DeBug\\Console.log" , "a") as file:
            file.write(Text + "\n")
    
    def defee(self):
        with open("DeBug\\Console.log" , "w") as file:
            file.write("")