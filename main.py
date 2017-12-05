from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


#Black Magic = fight
fire = Spell("Fire", 60, 600, "black")
thunder = Spell("Thunder", 80, 900, "black")
blizzard = Spell("Blizzard", 30, 800, "black")
meteor = Spell("Meteor", 90, 1060, "black")
quake = Spell("Quake", 20, 120, "black")

#White Magic = heal
cure = Spell("Cure", 80, 620, "white")
cura = Spell("Cura", 90, 1500, "white")


#Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "fully resores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "fully resores party's MP/HP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5}, {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

#instance of People
player1 = Person("Kat   :", 3460, 132, 300, 34, player_spells, player_items)
player2 = Person("Kevin :", 2460, 188, 288, 34, player_spells, player_items)
player3 = Person("Lauren:", 4460, 174, 311, 34, player_spells, player_items)

enemy1 = Person("Mozzarella :", 1200, 130, 525, 25, [], [])
enemy2 = Person("Cheddar    :", 15000, 701, 525, 25, [], [])
enemy3 = Person("Colby      :", 1200, 130, 525, 25, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

#the bcolors.ENDC ends the colors that are wrapping the text.
print("\n" + bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks" + bcolors.ENDC)

while running:
    print("===================")

    print("\n\n")
    print("NAME                       HP                                           MP")

    for player in players:
         player.get_stats()

    print("\n")
    print("NAME                                 HP                                          ")

    for enemy in enemies:
         enemy.get_enemy_stats()

    for player in players:

      player.choose_action()
      choice = input("    Choose action: ")
      index = int(choice) - 1

      if index == 0:
          dmg = player.generate_damage()
          enemy = player.choose_target(enemies)

          enemies[enemy].take_damage(dmg)
          print("You attacked " + enemies[enemy].name + " for", dmg, "points of damage.")

          if enemies[enemy].get_hp() == 0:
              print(enemies[enemy].name.replace(" ", "") + " has been eaten.")
              del enemies[enemy]

      elif index == 1:
          player.choose_magic()
          magic_choice = int(input("    Choose magic:")) - 1

          if magic_choice == -1:
              continue

          #this is the spell itself
          spell = player.magic[magic_choice]
          #targets function inside magic
          magic_dmg = spell.generate_damage()

          current_mp = player.get_mp()

          if spell.cost > current_mp:
              print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
              #this allows no penalty to the user because the enemy does not attack it just starts the loop over again
              continue

          player.reduce_mp(spell.cost)


          if spell.type == "white":
              player.heal(magic_dmg)
              print(bcolors.OKBLUE + "\n" + spell.name + " heals for :", str(magic_dmg), "HP." + bcolors.ENDC)
          elif spell.type == "black":

              enemy = player.choose_target(enemies)

              enemies[enemy].take_damage(magic_dmg)

              print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to" + enemies[enemy].name + bcolors.ENDC)

              if enemies[enemy].get_hp() == 0:
                 print(enemies[enemy].name.replace(" ", "") + " has been eaten.")
                 del enemies[enemy]
      elif index == 2:
          player.choose_item()
          item_choice = int(input("    Choose item: ")) -1

          if item_choice == -1:
              continue

          item = player.items[item_choice]["item"]

          if player.items[item_choice]["quantity"] == 0:
              print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
              continue

          player.items[item_choice]["quantity"] -= 1

          if item.type == "potion" :
              player.heal(item.prop)
              print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
          elif item.type == "elixer":
              if item.name == "MegaElizer":
                  for i in players:
                      i.hp = i.get_max_hp
                      i.mp = i.maxmp
              else:
                player.hp = player.maxhp
                player.mp = player.maxmp
              print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
          elif item.type == "attack":
              enemy = player.choose_target(enemies)
              enemies[enemy].take_damage(item.prop)

              enemy.take_damage(item.prop)
              print(bcolors.FAIL + "\n" + item. name + " deals", str(item.prop), "points of damage to "+ enemies[enemy].name + bcolors.ENDC)

              if enemies[enemy].get_hp() == 0:
                  print(enemies[enemy].name.replace(" ", "") + " has been eaten.")
                  del enemies[enemy]
    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemies[0].generate_damage()

    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies  == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you" + bcolors.ENDC)
        running = False
