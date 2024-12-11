from PIL import Image
import os, sys, psutil, glob
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from Data.Data import *
from Data.Hub import Hub
from Code.Start.Controler_Program import *

#My Class
class Console:
    def __init__(self):
        self.buffer = ""
        
    def log(self, Text):
        with open("DeBug\\Console.log" , "a") as file:  file.write(Text + "\n")
    
    def defee(self):
        with open("DeBug\\Console.log" , "w") as file:  file.write("")

class Data:
    def __init__(self):
        self.buffer = ""
        
    def write_new_data(self, data , data_Text):
        with open("Data\\Data.py", "a", encoding="utf-8") as file:  file.write(f"{data} = {data_Text}\n")
            
    def wrile_data(self, data, data_Text):
        with open("Data\\Data.py", "r", encoding="utf-8") as file:  lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith(data):
                lines[i] = f"{data} = \"{data_Text}\"\n"
                break
            
        with open("Data\\Data.py", "w", encoding="utf-8") as file:  file.writelines(lines)

Console = Console()

#/My Class

def is_notepad_running():
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if "notepad.exe" in proc.info["name"].lower():  return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):  pass
    return False

def calculate_image_size(TXT):
    if TXT > 10000:
        Console.log("File too big | Max 10Kb") ; input("File too big | Max 10Kb")
        return None, None
    X = math.ceil(math.sqrt(TXT))
    Y = TXT // X
    
    if TXT % X != 0:  Y += 1
    
    Console.log(f"Image size ({X}X, {Y}Y)")
    return X, Y

def process_metadata(image):
    image_tyre = image.getpixel((0, 0))
    index, index_2 = image_tyre[1], image_tyre[2]

    while index <= 0 and index_2 > 0:
        index += 255
        index_2 -= 1
    if index_2 < 0:
        Console.log("Error: Invalid metadata")
        return None

    if 0 <= index < len(Program):  return Program[index]
    else:
        Console.log(f"Error: index {index} is out of range")
        return None

def DeBug():
    def Create_file(files, Do="R", file_text=""):
        with open(f"{files}.{Do}", "w", encoding="utf-8") as file:  file.write(file_text)
    os.makedirs("Images", exist_ok=True)
    os.makedirs("DeBug", exist_ok=True)
    Create_file("DeBug/Console","log", "")
    Create_file("DeBug/Edit","txt", "")

def Edit_Control(file="Edit", Data_pack=None):
    try:
        os.rename(f"DeBug/{file}",f"DeBug/{file}.{Data_pack}")
        Console.log(f"File renamed from DeBug/{file} to DeBug/{file}.{Data_pack}")
    except FileNotFoundError:  Console.log(f"File not found: DeBug/{file}")
    except Exception as e:  Console.log(f"Error renaming file: {e}")

def Main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        X_D, Y_D = 1, 0
        index = 0

        A = input(" 1 - Create \n 2 - Open \n > ")
        try:  A = int(A)
        except ValueError:
            Console.log("Enter a number") ; input("Enter a number")
            continue

        if A == 1:
            image_name = input("Enter image name \n >")
            if not image_name.isalnum():
                input("Name must be alphanumeric!")
                continue

            try:
                image_tyre = int(input("Enter tyre (1 - Text / 2 - Program): \n > "))
                if image_tyre not in [1, 2]:
                    raise ValueError
                if image_tyre == 2:
                    input("in file format {\nMain():\n   Code\n}")
                    while True:
                        image_tyre_Program = input("Enter (Program = (py - css - ...)) \n >")
                        if image_tyre_Program.lower() in Program:
                            index = Program.index(image_tyre_Program.lower())
                            break
            except ValueError:
                input("Enter (1) or (2 and (.Code) )!")
                continue

            os.startfile("DeBug\\edit.txt")
            while is_notepad_running():  pass

            try:
                with open("DeBug\\edit.txt", "r", encoding="utf-8") as file:
                    image_txt = file.read()
            except Exception as e:
                Console.log(f"Error while reading (Edit): {e}") ; input(f"Error while reading (Edit): {e}")
                continue
            len_image_txt = len(image_txt)
            X, Y = calculate_image_size(len_image_txt+2)
            if X is None or Y is None:
                Console.log("Error in calculating image size") ; input("Error in calculating image size")
                continue

            image = Image.new("RGB", (X, Y), (0, 0, 0))
            pixels = image.load()
            Console.log(f"Creating image size ({X}X | {Y}Y)")

            if image_tyre == 1: pixels[0,0] = (0,0,0)
            if image_tyre == 2: pixels[0,0] = (1,index,0)

            Console.log("Image tyre = ")
            for i in range(len_image_txt):
                D = image_txt[i]
                if X_D >= X:
                    X_D = 0
                    Y_D += 1

                pixels[X_D, Y_D] = Hub.get(D, (0, 0, 0))
                X_D += 1

            pixels[X_D,Y_D] = (255,255,255)

            try:
                image.save(os.path.join("Images", f"{image_name}.png"))
                Console.log(f"Image saved to Images/{image_name}.png")
            except Exception as e:
                input(f"Error saving image: {e}")
                continue

            image.show()

        elif A == 2:
            X_D, Y_D = 1,0
            Text = ""
            image_name = input("Enter image name (Image.png or Image) \n >")
            image_path = f"Images\\{image_name}" if image_name in [".png"] else f"Images\\{image_name}.png"
            if not os.path.exists(image_path):
                Console.log(f"Image not found: {image_path}") ; input(f"Image not found: {image_path}")
                continue

            image = Image.open(image_path)
            width, height = image.size
            pixel_count = width * height
            if image.getpixel((0,0)) == (0,0,0):                
                for i in range(pixel_count):
                    if X_D < width and Y_D < height:
                        if image.getpixel((X_D, Y_D)) != (255, 255, 255):
                            pixel = image.getpixel((X_D, Y_D))
                            Text += Reversed_Hub.get(pixel)
                        else: break

                        X_D += 1
                        if X_D >= width:
                            X_D = 0
                            Y_D += 1
                    else: break
                with open("DeBug\\edit.txt", "w", encoding="utf-8") as file:
                    file.write(Text)
                    Console.log(f"Text saved to DeBug/edit.txt")
                    os.startfile("DeBug\\edit.txt")
            while is_notepad_running():  pass
            else:
                image_tyre = image.getpixel((0,0))
                index = image_tyre[1]
                Edit_Control(Data_pack=Program[index])
                os.startfile(f"DeBug\\edit.{Program[index]}")

        else:
            input("Error enter 1 - 2")


def Code_Start():
    global Reversed_Hub
    DeBug()
    input("Version 0.0.0.3")
    Console.defee()
    Reversed_Hub = {v: k for k, v in Hub.items()}
    Main()
    
Code_Start()