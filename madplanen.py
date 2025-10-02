import sqlite3
import numpy as np
import time

DB_NAME = "recipes.db"

def init_db():
    """Opret tabeller hvis de ikke findes i forvejen"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        recipe TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        unit TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DishIngredients (
        dish_id INTEGER,
        ingredient_id INTEGER,
        amount REAL,
        FOREIGN KEY (dish_id) REFERENCES Dishes(id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
    )
    """)
    
    conn.commit()
    conn.close()


def add_dish():
    """Tilføj en ny ret"""
    name = input("Indtast rettens navn: ")
    recipe = input("Skriv opskriften: ")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Dishes (name, recipe) VALUES (?, ?)", (name, recipe))
    conn.commit()
    conn.close()

    input(f"✅ Retten '{name}' blev tilføjet!")
    clear_screen()


def list_dishes():
    """        Alle retter"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM Dishes")
    dishes = cursor.fetchall()
    
    conn.close()
    
    if not dishes:
        print("⚠️ Der er endnu ingen retter i databasen.")
    else:
        print("           Alle retter")
        print("-----------------------------------")
        print("Vælg en ret ved at indtaste dens ID\n")
        for dish in dishes:
            print(f"{dish[0]}: {dish[1]}")
        print("0: Tilbage til hovedmenu")
        print()
        choice = input("Indtast ID: ")
        clear_screen()

        if choice.isdigit() and choice != "0":
            show_dish_details(int(choice))

def show_dish_details(dish_id):
    """Vis detaljer for en specifik ret"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, recipe FROM Dishes WHERE id = ?", (dish_id,))
    dish = cursor.fetchone()
    
    if not dish:
        print("⚠️ Retten blev ikke fundet.")
        conn.close()
        time.sleep(1)
        clear_screen()
        return
    
    print(f"\n--- {dish[0]} ---")
    print(f"Opskrift: {dish[1]}\n")
    
    cursor.execute("""
    SELECT Ingredients.name, Ingredients.unit, DishIngredients.amount
    FROM DishIngredients
    JOIN Ingredients ON DishIngredients.ingredient_id = Ingredients.id
    WHERE DishIngredients.dish_id = ?
    """, (dish_id,))
    
    ingredients = cursor.fetchall()
    
    if ingredients:
        print("Ingredienser:")
        for ing in ingredients:
            print(f"- {ing[2]} {ing[1]} {ing[0]}")
    else:
        print("Ingen ingredienser tilføjet endnu.")
    
    conn.close()
    
    input("\nTryk på [Enter] for at vende tilbage.")
    clear_screen()

def main_menu():
    """Hovedmenu"""
    while True:
        print("--- Madplan Program ---")
        print("1. Tilføj en ret")
        print("2. Se alle retter")
        print("3. Afslut")
        
        choice = input("\nVælg en mulighed (1-3): ")
        # print("\033[4A", end="")
        clear_screen()

        if choice == "1":
            add_dish() # Tilføj en ret
        elif choice == "2":
            list_dishes() # Se alle retter
        elif choice == "3":
            if np.random.rand() > 0.8:
                print("Later gator! 🐊")
            else:
                print("Farvel! 👋")
            time.sleep(1)
            break
        else:
            print("Ugyldigt valg. Prøv igen.")

def clear_screen():
    print("\033[H\033[J", end="")

if __name__ == "__main__":
    clear_screen()
    init_db()
    main_menu()
