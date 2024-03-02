import os
import sys
import random
import time

run = True
menu = True
play = False
rules = False
key = False
fight = False
standing = True
buy_shop = False
buy_trade = False
special_cards = False
speak = False
boss = False
double_damage_active = False

resistance_active = False
resistance_turns_left = 0

stun_active = False
stun_turns_left = 0


HP = 50
HPMAX = HP
initial_HPMAX = HPMAX
ATK = 5
healing_card = 1
max_healing_card = 0
stun_card = 0
double_dmg_card = 0
resistance_card = 0
gold = 0
x = 0
y = 0


map =  [["plains",   "plains",     "shop",     "plains",    "forest",    "mountain",         "key"],
        ["forest",   "trade1",   "forest",     "forest",    "forest",        "shop",    "mountain"],
        ["forest",   "fields",   "bridge",     "plains",     "hills",      "forest",       "hills"],
        ["plains",     "shop",     "town",  "gymnasium",    "plains",      "trade2",    "mountain"],
        ["plains",   "fields",   "fields",       "shop",     "hills",    "mountain",    "badlands"]]


y_len = len(map) - 1
x_len = len(map[0]) - 1


biom = {
    "plains": {
        "t": "PLAINS",
        "e": True
    },
    "forest": {
        "t": "WOODS",
        "e": True
    },
    "fields": {
        "t": "FIELDS",
        "e": True
    },
    "bridge": {
        "t": "BRIDGE",
        "e": True
    },
    "shop": {
        "t": "Spell Card Shop",
        "e": False
    },
    "trade1": {
        "t": "MASADORA TRADE SHOP",
        "e": False
    },
    "trade2": {
        "t": "ANTOKIBA TRADE SHOP TRADE SHOP",
        "e": False
    },
    "town": {
        "t": "TOWN : SAFE ZONE",
        "e": False
    },
    "gymnasium": {
        "t": "RAZOR'S GYMNASIUM",
        "e": False
    },
    "badlands": {
        "t": "BADLANDS",
        "e": True
    },
    "mountain": {
        "t": "MOUNTAIN",
        "e": True
    },
    "hills": {
        "t": "HILLS",
        "e": True
    },
    "key": {
        "t": "SECRET HIDEOUT",
        "e": False
    },
}

enemies_list = ["Cyclops", "Bubble Horse", "Radio Rat", "King White Stag Beetle", "Melanin Lizard", "Galgaida",
                "Owl NPC", "Hyper Puffball", "Wolf Pack"]

enemies = {
    "Cyclops": {"hp": 30, "at": 5, "gold": 20},
    "Bubble Horse": {"hp": 20, "at": 4, "gold": 15},
    "Radio Rat": {"hp": 10, "at": 2, "gold": 10},
    "King White Stag Beetle": {"hp": 40, "at": 6, "gold": 25},
    "Melanin Lizard": {"hp": 60, "at": 8, "gold": 30},
    "Galgaida": {"hp": 15, "at": 3, "gold": 12},
    "Owl NPC": {"hp": 5, "at": 1, "gold": 5},
    "Hyper Puffball": {"hp": 10, "at": 2, "gold": 8},
    "Wolf Pack": {"hp": 25, "at": 4, "gold": 18},
    "Razor": {"hp": 250, "at": 25, "gold": 1000}
}

sys.stdout = open(os.devnull, 'w')

import pygame

sys.stdout = sys.__stdout__

pygame.init()
pygame.mixer.init()

current_directory = os.path.dirname(os.path.realpath(__file__))

sounds_path = os.path.join(current_directory, "Game_Sounds")
normal_sound_path = os.path.join(sounds_path, "normal_sound.wav")
shop_sound_path = os.path.join(sounds_path, "shop_sound.wav")
trade_shop_sound_path = os.path.join(sounds_path, "trade_shop_sound.wav")
key_found_sound_path = os.path.join(sounds_path, "key_found_sound.wav")
enemy_encounter_sound_path = os.path.join(sounds_path, "enemy_encounter_sound.wav")
boss_battle_sound_path = os.path.join(sounds_path, "boss_battle_sound.wav")

sounds = {
    "normal": normal_sound_path,
    "shop": shop_sound_path,
    "trade_shop": trade_shop_sound_path,
    "key_found": key_found_sound_path,
    "enemy_encounter": enemy_encounter_sound_path,
    "boss_battle": boss_battle_sound_path
}

for event, path in sounds.items():
    try:
        sounds[event] = pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound for {event}: {e}")

current_sound = None

def play_sound(event):
    global current_sound
    try:
        if current_sound and current_sound == sounds[event]:
            pass
        else:
            if current_sound:
                current_sound.stop()
            if event in sounds:
                current_sound = sounds[event]
                current_sound.play()
            else:
                print(f"No sound found for event: {event}")
    except pygame.error as e:
        print("Error playing sound:", e)


def clear():
    os.system("cls")


def draw():
    print("------------------------------------------------------------------------")


def save():
    save_list = [name, str(HP), str(ATK), str(healing_card), str(max_healing_card), str(gold), str(x), str(y),
                 str(key), str(stun_card), str(double_dmg_card), str(resistance_card)]

    file = open("../RGP_Tom-Monty_Loann-Duval/load.txt", "w")

    for item in save_list:
        file.write(item + "\n")
    file.close()


def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    print(name + "'s HP refilled to " + str(HP) + "!")


def battle():
    global fight, play, run, HP, HPMAX, healing_card, max_healing_card, stun_card, double_dmg_card, resistance_card, \
        double_damage_active, resistance_active, stun_active, stun_turns_left, resistance_turns_left, gold, boss

    initial_HPMAX = HPMAX

    if not boss:
        play_sound("enemy_encounter")
        enemy = random.choice(enemies_list)
    else:
        play_sound("boss_battle")
        enemy = "Razor"
    hp = enemies[enemy]["hp"]
    hpmax = hp
    atk = enemies[enemy]["at"]
    g = enemies[enemy]["gold"]
    HPMAX = HP

    while fight:
        clear()
        draw()
        print("Defeat the " + enemy + "!")
        draw()
        if special_cards:
            print(enemy + "'s HP: " + str(hp) + "/" + str(hpmax))
            print(name + "'s HP: " + str(HP) + "/" + str(initial_HPMAX))
            print("HEALING CARDS: " + str(healing_card))
            print("MAX HEALING CARDS: " + str(max_healing_card))
            print("STUN CARDS: " + str(stun_card))
            print("DOUBLE DMG CARDS: " + str(double_dmg_card))
            print("RESISTANCE CARDS: " + str(resistance_card))
            draw()
            print("1 - ATTACK")
            if healing_card > 0:
                print("2 - USE HEALING CARD (30HP)")
            if max_healing_card > 0:
                print("3 - USE MAX HEALING CARD (50HP)")
            if stun_card > 0:
                print("4 - STUN")
            if double_dmg_card > 0:
                print("5 - DOUBLE DAMAGE")
            if resistance_card > 0:
                print("6 - RESISTANCE")
            draw()

            choice = input("# ")

            if resistance_turns_left > 0:
                resistance_turns_left -= 1
                if resistance_turns_left == 0:
                    resistance_active = False

            if stun_turns_left > 0:
                stun_turns_left -= 1
                if stun_turns_left == 0:
                    stun_active = False

            if choice == "1":
                if double_damage_active:
                    hp -= ATK * 2
                    print(name + " with the double damage effect dealt : " + str(ATK*2) + " to the " + enemy + "!")
                else:
                    hp -= ATK
                    print(name + " dealt " + str(ATK) + " damage to the " + enemy + ".")
                if hp > 0:
                    if resistance_active:
                        damage_taken = atk // 2
                    else:
                        damage_taken = atk
                    HP -= damage_taken
                    print(enemy + " dealt " + str(damage_taken) + " damage to " + name + ".")
                input("> ")

            elif choice == "2":
                if healing_card > 0:
                    healing_card -= 1
                    heal(30)
                    HP -= atk
                    if stun_active:
                        continue
                    else:
                        print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    print("No healing cards!")
                input("> ")

            elif choice == "3":
                if max_healing_card > 0:
                    max_healing_card -= 1
                    heal(50)
                    HP -= atk
                    if stun_active:
                        continue
                    else:
                        print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    print("No max healing cards!")
                input("> ")

            elif choice == "4":
                if stun_card > 0:
                    stun_card -= 1
                    stun_active = True
                    stun_turns_left = 2
                    print("You've stunned the enemy for 2 turns!")
                    input("> ")
                    continue
                else:
                    print("No stun cards!")
                    input("> ")

            elif choice == "5":
                if double_dmg_card > 0:
                    double_dmg_card -= 1
                    double_damage_active = True
                    print("Your next attack will deal double damage!")
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    print("No double damage cards!")
                input("> ")

            elif choice == "6":
                if resistance_card > 0:
                    resistance_card -= 1
                    resistance_active = True
                    resistance_turns_left = 5
                    print("You're resistant to damage for the next 5 attacks!")
                else:
                    print("No resistance cards!")
                input("> ")

        else:
            print(enemy + "'s HP: " + str(hp) + "/" + str(hpmax))
            print(name + "'s HP: " + str(HP) + "/" + str(initial_HPMAX))
            print("HEALING CARDS: " + str(healing_card))
            print("MAX HEALING CARDS: " + str(max_healing_card))
            draw()
            print("1 - ATTACK")
            if healing_card > 0:
                print("2 - USE HEALING CARD (30HP)")
            if max_healing_card > 0:
                print("3 - USE MAX HEALING CARD (50HP)")
            draw()

            choice = input("# ")

            if choice == "1":
                hp -= ATK
                print(name + " dealt " + str(ATK) + " damage to the " + enemy + ".")
                if hp > 0:
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                input("> ")

            elif choice == "2":
                if healing_card > 0:
                    healing_card -= 1
                    heal(30)
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    print("No healing cards!")
                input("> ")

            elif choice == "3":
                if max_healing_card > 0:
                    max_healing_card -= 1
                    heal(HPMAX)
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    print("No max healing cards!")
                input("> ")

        if HP <= 0:
            print(enemy + " defeated " + name + "...")
            draw()
            fight = False
            play = False
            run = False
            print("GAME OVER")
            input("> ")

        if hp <= 0:
            print(name + " defeated the " + enemy + "!")
            draw()
            fight = False
            double_damage_active = False
            resistance_active = False
            stun_active = False
            stun_turns_left = 0
            resistance_turns_left = 0
            gold += g
            print("You've found " + str(g) + " gold!")
            play_sound("normal")
            if random.randint(0, 100) < 20:
                healing_card += 1
                print("You've found a healing card!")
            if enemy == "Razor":
                draw()
                story_ending()
                boss = False
                play = False
                run = False
            input("> ")
            clear()


def card_shop():
    global buy_shop, gold, healing_card, max_healing_card, resistance_card, double_dmg_card, stun_card, ATK, HP

    while buy_shop:
        play_sound("shop")
        clear()
        if special_cards:
            draw()
            print("Welcome to the shop!")
            draw()
            print("GOLD: " + str(gold))
            print("HEALING CARDS: " + str(healing_card))
            print("MAX HEALING CARDS: " + str(max_healing_card))
            print("STUN CARD: " + str(stun_card))
            print("DOUBLE DMG CARD: " + str(double_dmg_card))
            print("RESISTANCE CARD: " + str(resistance_card))
            print("ATK: " + str(ATK))
            print("HP: " + str(HP))
            draw()
            print("1 - BUY HEALING CARD (30HP) - 8 GOLD")
            print("2 - BUY MAX HEALING CARD (50HP) - 10 GOLD")
            print("3 - STUN CARD (2 TURNS) - 20 GOLD")
            print("4 - DOUBLE DMG CARD (NEXT TURN)- 10 GOLD")
            print("5 - RESISTANCE CARD (TAKE 50% LESS DMG FOR 5 TURNS) - 30 GOLD")
            print("6 - WEAPON CARD (+2ATK) - 10 GOLD")
            print("7 - MYTHICAL WEAPON CARD (+10ATK) - 30 GOLD")
            print("8 - MYTHICAL HEALTH CARD (+10HP) - 20 GOLD")
            print("9 - LEAVE")
            draw()

            choice = input("# ")

            if choice == "1":
                if gold >= 5:
                    healing_card += 1
                    gold -= 5
                    print("You've bought a healing card!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "2":
                if gold >= 8:
                    max_healing_card += 1
                    gold -= 8
                    print("You've bought a max healing card!")
                else:
                    print("Not enough gold!")
                input("> ")
            if choice == "3":
                if gold >= 30:
                    stun_card += 1
                    gold -= 30
                    print("You've bought a stun card!")
                else:
                    print("Not enough gold!")
                input("> ")
            if choice == "4":
                if gold >= 30:
                    double_dmg_card += 1
                    gold -= 30
                    print("You've bought a double damage card!")
                else:
                    print("Not enough gold!")
                input("> ")
            if choice == "5":
                if gold >= 30:
                    resistance_card += 1
                    gold -= 30
                    print("You've bought a resistance card!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "6":
                if gold >= 10:
                    ATK += 2
                    gold -= 10
                    print("You've upgraded your weapon by 2!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "7":
                if gold >= 50:
                    ATK += 10
                    gold -= 50
                    print("You've upgraded your weapon by 10!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "8":
                if gold >= 20:
                    HP += 10
                    gold -= 20
                    print("You gained 10 health!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "9":
                buy_shop = False
                play_sound("normal")
        else:
            draw()
            print("Welcome to the shop!")
            draw()
            print("GOLD: " + str(gold))
            print("HEALING CARDS: " + str(healing_card))
            print("MAX HEALING CARDS: " + str(max_healing_card))
            print("ATK: " + str(ATK))
            draw()
            print("1 - BUY HEALING CARD (30HP) - 5 GOLD")
            print("2 - BUY MAX HEALING CARD (50HP) - 8 GOLD")
            print("3 - WEAPON CARD (+2ATK) - 10 GOLD")
            print("4 - LEAVE")
            draw()

            choice = input("# ")

            if choice == "1":
                if gold >= 5:
                    healing_card += 1
                    gold -= 5
                    print("You've bought a healing card!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "2":
                if gold >= 8:
                    max_healing_card += 1
                    gold -= 8
                    print("You've bought a max healing card!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "3":
                if gold >= 10:
                    ATK += 2
                    gold -= 10
                    print("You've upgraded your weapon!")
                else:
                    print("Not enough gold!")
                input("> ")
            elif choice == "4":
                buy_shop = False
                play_sound("normal")


def trade_shop():
    global buy_trade, special_cards, gold

    enemy = "Razor"
    hp = enemies[enemy]["hp"]
    atk = enemies[enemy]["at"]
    g = enemies[enemy]["gold"]

    while buy_trade:
        play_sound("trade_shop")
        clear()
        draw()
        print("Welcome to the Trade Shop!")
        draw()
        print("GOLD: " + str(gold))
        draw()
        print("1 - Buy boss stats information (20 gold)")
        print("2 - Unlock Special Cards (10 gold)")
        print("3 - Leave")
        draw()

        choice = input("# ")

        if choice == "1":
            if gold >= 20:
                print("Boss' stats: ")
                print("HP: " + str(hp) + ", ATK: " + str(atk) + ", WORTH: " + str(g) + "g")
                gold -= 20
            else:
                print("Not enough gold!")
            input("> ")
        elif choice == "2":
            if gold >= 10:
                print("Special Cards unlocked!")
                special_cards = True
                gold -= 10
            else:
                print("Not enough gold!")
            input("> ")
        elif choice == "3":
            buy_trade = False
            play_sound("normal")


def gymnasium():
    global boss, key, fight

    while boss:
        clear()
        draw()
        print("Razor's Gymnasium needs a special card to be opened. What will you do?")
        draw()
        if key:
            print("1 - USE KEY CARD")
        print("2 - TURN BACK")
        draw()

        choice = input("# ")

        if choice == "1":
            if key:
                fight = True
                battle()

        elif choice == "2":
            boss = False


def story_telling():

    story_text = [
        "Welcome to Greed Island!",
        "You find yourself trapped in the virtual world of Greed Island, \n"
        "a place known for its dangerous challenges and not being escapable.",
        "Thrown into this world against your will by an unknown force, \n"
        "you must navigate through its dangers to find a way back to the real world.",
        "Rumors circulate among players of an extremely rare card hidden within Greed Island, \n"
        "said to be able to make whoever finds it exit the world of Greed Island.",
        "Can you uncover the secrets of Greed Island and escape its grasp, \n"
        "or will you be forever trapped in its virtual madness?"
    ]

    for line in story_text:
        for char in line:
            print(char, end='', flush=True)
            time.sleep(0.05)
        print()
        input("Press Enter to continue...")

        if line == "Welcome to Greed Island!" or \
                line == ("You find yourself trapped in the virtual world of Greed Island, \n"
                         "a place known for its dangerous challenges and not being escapable.") or \
                line == ("Thrown into this world against your will by an unknown force, \n"
                         "you must navigate through its dangers to find a way back to the real world.") or \
                line == ("Rumors circulate among players of an extremely rare card hidden within Greed Island, \n"
                         "said to be able to make whoever finds it exit the world of Greed Island.") or \
                line == ("Can you uncover the secrets of Greed Island and escape its grasp, \n"
                         "or will you be forever trapped in its virtual madness?"):
            clear()


    while True:

        clear()
        draw()

        choice = input("Do you take the risk of adventuring through the island? (Y/N): ").upper()

        draw()

        if choice == "Y":
            clear()
            break
        elif choice == "N":
            print("Trapped forever in Greed Island, you spend eternity wandering around.")
            print("You realize the only choice you have left.")
            input("Press Enter to end your journey once and for all....")
            return
        else:
            print("Invalid choice. Please enter 'Y' or 'N'.")


def story_ending():
    clear()

    ending_text = [
        "Congratulations, you've gotten the exit card!",
        "You wake up and realize you are still in the game.",
        "Tired, you decide to end your sufferings and leave once and for all.",
        "In Greed Island, only despair awaits.........."
    ]

    for line in ending_text:
        print(line)
        if line == "Congratulations, you've gotten the exit card!" or\
           line == "Tired, you decide to end your sufferings and leave once and for all.":
            input("> ")
            clear()


while run:
    global name

    while menu:
        draw()
        print("1, NEW GAME")
        print("2, LOAD GAME")
        print("3, RULES")
        print("4, QUIT GAME")
        draw()

        choice = input("# ")

        if choice == "1":
            clear()
            story_telling()
            name = input("# What's your name, Hunter? ")
            menu = False
            play = True
        elif choice == "2":
            try:
                f = open("../RGP_Tom-Monty_Loann-Duval/load.txt", "r")
                load_list = f.readlines()
                if len(load_list) == 9:
                    name = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    ATK = int(load_list[2][:-1])
                    healing_card = int(load_list[3][:-1])
                    max_healing_card = int(load_list[4][:-1])
                    stun_card = int(load_list[5][:-1])
                    double_dmg_card = int(load_list[6][:-1])
                    resistance_card = int(load_list[7][:-1])
                    gold = int(load_list[8][:-1])
                    x = int(load_list[9][:-1])
                    y = int(load_list[10][:-1])
                    key = bool(load_list[11][:-1])
                    clear()
                    print("Welcome back, " + name + "!")
                    input("> ")
                    menu = False
                    play = True
                else:
                    print("Corrupt save file!")
                    input("> ")
            except OSError:
                print("No loadable save file!")
                input("> ")
        elif choice == "3":
            print("Welcome to Greed Island! You, as a Hunter, are tasked with exploring this world, defeating enemies, "
                  "and ultimately challenging Razor, the final boss of this game. Gather gold, upgrade your skills, "
                  "and prepare for the ultimate showdown!")
            input("> ")
        elif choice == "4":
            quit()
        else:
            print("Invalid input, please try again.")
            input("> ")
            clear()

    while play:
        save()
        clear()

        if not standing:
            if biom[map[y][x]]["e"]:
                if random.randint(0, 100) < 40:
                    fight = True
                    battle()

        if play:
            play_sound("normal")
            draw()
            print("LOCATION: " + biom[map[y][x]]["t"])
            draw()
            print("NAME: " + name)
            print("HP: " + str(HP) + "/" + str(HPMAX))
            print("ATK: " + str(ATK))
            print("HEALING CARDS: " + str(healing_card))
            print("MAX HEALING CARDS: " + str(max_healing_card))
            print("GOLD: " + str(gold))
            print("COORD:", x, y)
            draw()
            print("0 - SAVE AND QUIT")
            draw()
            if y > 0:
                print("1 - NORTH")
            if x < x_len:
                print("2 - EAST")
            if y < y_len:
                print("3 - SOUTH")
            if x > 0:
                print("4 - WEST")
            if healing_card > 0:
                print("5 - USE HEALING CARD (30HP)")
            if max_healing_card > 0:
                print("6 - USE MAX HEALING CARD (50HP)")
            if map[y][x] == "shop" or map[y][x] == "gymnasium" or map[y][x] == "trade1" or map[y][x] == "trade2":
                print("7 - ENTER")
            draw()

            if map[y][x] == "key":
                play_sound("key_found")
                print("You have found the key card for Razor's Gymnasium.\n")
                print("May you prevail against him and finally beat Greed Island!!")
                draw()
                key = True

            dest = input("# ")

            if dest == "0":
                play = False
                menu = True
                save()
            elif dest == "1":
                if y > 0:
                    y -= 1
                    standing = False
            elif dest == "2":
                if x < x_len:
                    x += 1
                    standing = False
            elif dest == "3":
                if y < y_len:
                    y += 1
                    standing = False
            elif dest == "4":
                if x > 0:
                    x -= 1
                    standing = False
            elif dest == "5":
                if healing_card > 0:
                    healing_card -= 1
                    heal(30)
                else:
                    print("No healing cards!")
                input("> ")
                standing = True
            elif dest == "6":
                if max_healing_card > 0:
                    max_healing_card -= 1
                    heal(50)
                else:
                    print("No max healing cards!")
                input("> ")
                standing = True
            elif dest == "7":
                if map[y][x] == "gymnasium":
                    boss = True
                    gymnasium()
                elif map[y][x] == "shop":
                    buy_shop = True
                    card_shop()
                elif map[y][x] == "trade1" or map[y][x] == "trade2":
                    buy_trade = True
                    trade_shop()
            else:
                standing = True