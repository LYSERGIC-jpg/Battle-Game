import random

# ----- WEAPON DATA (hardcoded) -----
weapons = {
    "dagger": {"dmg_min": 4, "dmg_max": 8, "crit_max": 10, "effect": "bleed"},
    "sword":  {"dmg_min": 8, "dmg_max": 14, "crit_max": 18, "effect": "none"},
    "hammer": {"dmg_min": 10, "dmg_max": 16, "crit_max": 20, "effect": "stun"},
    "cheat":  {"dmg_min": 999, "dmg_max":999, "crit_max": 999, "effect": "none"}
}

# ----- PLAYER CHOOSE LOADOUT (before battle) -----
print("Available weapons: dagger, sword, hammer")
primary = input("Choose PRIMARY weapon: ").strip().lower()
while primary not in weapons:
    primary = input("Not valid. Choose PRIMARY (dagger/sword/hammer): ")
secondary = input("Choose SECONDARY weapon (different from primary): ").strip().lower()
while secondary not in weapons or secondary == primary:
    secondary = input("Different weapon. Choose SECONDARY: ")

print(f"\nLoadout set: Primary = {primary}, Secondary = {secondary}\n")

# ----- BATTLE VARIABLES -----
health = 100
enemy_health = 100
healing_potion = 3
max_health = 100
ultimate_cooldown = 0   # 0 = ready, >0 = turns left until ready
enemy_stunned = False
defense_penalty = False  # if True, enemy deals double damage next attack

# ----- BATTLE LOOP -----
while health > 0 and enemy_health > 0:
    print(f"\nYour health: {health} | Enemy health: {enemy_health}")
    if ultimate_cooldown > 0:
        print(f"Ultimate on cooldown: {ultimate_cooldown} turn(s) left.")
    if defense_penalty:
        print("Defense lowered! Enemy will deal extra damage next attack.")

    # ----- PLAYER ACTION MENU -----
    print("\nActions:")
    print("1. Normal Attack")
    if ultimate_cooldown == 0:
        print("2. ULTIMATE Attack (uses both weapons, but lowers defense and goes on cooldown)")
    print("3. Use Healing Potion")
    choice = input("\nChoose (1/2/3): \n")

    if choice == "1":
        weapon_choice = input("primary or secondary?: \n")
        while weapon_choice not in ["primary", "secondary"]:
            weapon_choice = input("Invalid input. Strike with which weapon?: \n")
        if weapon_choice == "primary": chosen_weapon = primary
        else:
            chosen_weapon = secondary
            
        weapon_stats = weapons[chosen_weapon]

        print("\n--- Your Turn ---")

        effect_messages = []
        damage = random.randint(weapon_stats["dmg_min"], weapon_stats["dmg_max"])

        # Critical Hit
        if random.randint(1, weapon_stats["crit_max"]) == 1:
            damage *= 2
            effect_messages.append("CRITICAL HIT!\n")

        total_damage = damage


         # Weapon Effect Bleed
        if weapon_stats["effect"] == "bleed":
            enemy_health -= 5
            effect_messages.append("Bleed! +5 damage\n")
        # Weapon Effect Stun
        elif weapon_stats["effect"] == "stun":
            enemy_stunned = True
            effect_messages.append("Stun! Enemy skips next turn.\n")
       
        enemy_health -= total_damage
        prefix = " ".join(effect_messages) + " " if effect_messages else ""
        print(f"{prefix}You dealt {total_damage} damage. Enemy health: {enemy_health}\n")
        

    elif choice == "2" and ultimate_cooldown == 0:
        
        combined_min = weapons[primary]["dmg_min"] + weapons[secondary]["dmg_min"]
        combined_max = weapons[primary]["dmg_max"] + weapons[secondary]["dmg_max"]

        damage = random.randint(combined_min, combined_max)
        if random.randint(1, 10) == 1:
            damage *= 2
            print("ULTIMATE ATTACK\n")
        enemy_health -= damage
        if weapons[primary]["effect"] == "bleed" or weapons[secondary]["effect"] == "bleed":
            enemy_health -= 5
            print(f"Bleed! +5 damage. Enemy health: {enemy_health}\n")
        if weapons[primary]["effect"] == "stun" or weapons[secondary]["effect"] == "stun":
            enemy_stunned = True
            print(f"Stun! Enemy skips next turn.\n")
        ultimate_cooldown = 2
        defense_penalty = True

    elif choice == "3":
        if healing_potion > 0:
            health = min(health + 10, max_health)
            healing_potion -= 1
            print(f"\nHealed! Health: {health}, Potions left: {healing_potion}")
        else:
            print("\nNo potions left!")
        input("\nPress Enter to continue...")
        continue
    else:
        print("\nInvalid choice or ultimate on cooldown.")
        input("\nPress Enter to continue...")
        continue
    
    # Check if enemy killed the beast after player's attack
    if enemy_health <= 0:
        print("You slayed the beast!", end= " ")
        break

    # ----- ENEMY TURN -----
    print("\n--- Enemy Turn ---")
    if enemy_stunned:
        print("Enemy is stunned and can't attack!")
        enemy_stunned = False
    else:
        damage = random.randint(1, 10)
        if defense_penalty:
            damage *= 2
            defense_penalty = False
            print("Enemy takes advantage of your lowered defense!")
        if random.randint(1, 10) == 1:
            damage *= 2
            print("ENEMY CRITICAL HIT!")
        health -= damage
        print(f"Enemy deals {damage} damage. Your health: {health}")

    if ultimate_cooldown > 0:
        ultimate_cooldown -= 1

# ----- BATTLE RESULT -----
if health <= 0:
    print("You died.")
else:
    print("Victory!")