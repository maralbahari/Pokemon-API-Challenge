from pokemon import Pokemon

def main():
    user_action=input("Enter 1 : to catche pokemons \nEnter 2 : to find your pokemons \nEnter 0 : to exit ").strip()
    if user_action.isnumeric():
        match int(user_action):
            case 1:
                print("Catching...\nPlease wait")
                user_pokemon=Pokemon(None,None)
                user_pokemon.catche_all_pokemon()
            case 2:
                find_pokemon()
            case 0:
                print("Exiting Program...")
    else:
        print("Invalid Input")
def find_pokemon():
    user_input=input("Please enter a pokemon id or name:").strip()
    if user_input.isnumeric():
        user_pokemon=Pokemon(None,int(user_input))
        print(user_pokemon.retrieve_pokemon_detail())
    else:
        user_pokemon=Pokemon(user_input,None)
        print(user_pokemon.retrieve_pokemon_detail())
if __name__ == "__main__":
    main()
