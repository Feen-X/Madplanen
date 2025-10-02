def clear_screen():
    print("\033[H\033[J", end="")

def print_menu():
    print("--- Hovedmenu ---")
    print("1. Tilføj en ret")
    print("2. Se alle retter")
    print("3. Afslut")

def show_dish(dish, ingredients):
    print(f"--- {dish[0]} ---")
    print(f"Opskrift: {dish[1]}\n")
    if ingredients:
        print("Ingredienser:")
        for ing in ingredients:
            print(f"- {ing[2]} {ing[1]} {ing[0]}")
    else:
        print("Ingen ingredienser tilføjet endnu.")
    input("\nTryk på [Enter] for at vende tilbage.")