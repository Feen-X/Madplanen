import sqlite3
DB_NAME = "recipes.db"

def init_db():
    """Opret tabeller hvis de ikke findes i forvejen"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dishes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE COLLATE NOCASE,
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

def add_dish(name, recipe):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Dishes (name, recipe) VALUES (?, ?)", (name, recipe))
        conn.commit()
        print(f"✅ Retten '{name}' blev tilføjet!")
    except sqlite3.IntegrityError:
        print(f"⚠️ Retten '{name}' findes allerede!")
    finally:
        conn.close()

def get_all_dishes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Dishes")
    dishes = cursor.fetchall()
    conn.close()
    return dishes

def get_dish_name(dish_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Dishes WHERE id = ?", (dish_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_dish_recipe(dish_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT recipe FROM Dishes WHERE id = ?", (dish_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_dish_ingredients(dish_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Ingredients.name, Ingredients.unit, DishIngredients.amount
        FROM DishIngredients
        JOIN Ingredients ON DishIngredients.ingredient_id = Ingredients.id
        WHERE DishIngredients.dish_id = ?
    """, (dish_id,))
    ingredients = cursor.fetchall()
    conn.close()
    return ingredients