class Data:
    def __init__(self):
        self.buffer = ""
    
    def write_new_data(self, data , data_Text):
        with open("Data\\Data.py", "a", encoding="utf-8") as file:
            file.write(f"{data} = {data_Text}\n")
    def wrile_data(self, data, data_Text):
        with open("Data\\Data.py", "r", encoding="utf-8") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith(data):
                lines[i] = f"{data} = \"{data_Text}\"\n"
                break
            
        with open("Data\\Data.py", "w", encoding="utf-8") as file:
            file.writelines(lines)