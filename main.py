import time
import numpy as np
from db import *
from ui import *

def main_menu():
    clear_screen()
    while True:
        print_menu()
        choice = input("\nVælg en mulighed (1-3): ")
        clear_screen()
        
        if choice == "1": # Tilføj en ret
            add_dish_menu()
        elif choice == "2": # Se alle retter
            all_dishes_menu()
        elif choice == "3":
            print("Later Alligator! 🐊" if np.random.rand() > 0.8 else "Farvel! 👋")
            time.sleep(1)
            break
        else:
            print("Ugyldigt valg. Prøv igen.")

def add_dish_menu():
    name = input("Indtast rettens navn: ")
    recipe = input("Skriv opskriften: ")
    add_dish(name, recipe)
    input("\n[Enter] for at vende tilbage.")
    clear_screen()

def all_dishes_menu():
    dishes = get_all_dishes()

    if not dishes:
        input("Ingen retter fundet. Tilføj en ret først.")
        clear_screen()
        return

    for dish in dishes:
        print(f"{dish[0]}: {dish[1]}")
    print("0: Tilbage til hovedmenu")
    print()
    choice = input("Indtast ID: ")
    clear_screen()
    
if __name__ == "__main__":
    init_db()
    clear_screen()
    main_menu()
