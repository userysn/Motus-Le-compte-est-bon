import itertools
import operator
import random
def motus():
    print("Bienvenue dans le jeu Motus!")
    jouer = input("Voulez-vous jouer une partie? (oui/non): ")
    if jouer.lower() != "oui":
        print("Merci d'être venu ! A bientôt !")
        return

    # Lecture du fichier des mots
    with open("dico.txt", "r") as f:
        mots = f.readlines()

    # Sélection d'un mot de 6 à 10 lettres
    mot_a_trouver = random.choice([mot.strip() for mot in mots if 6 <= len(mot.strip()) <= 10])
    nb_lettres = len(mot_a_trouver)
    print(f"Le mot à trouver contient {nb_lettres} lettres et commence par '{mot_a_trouver[0]}'")

    essais = 0
    while True:
        essais += 1
        proposition = input(f"Essai {essais}: Entrez un mot de {nb_lettres} lettres: ").strip().lower()

        # Vérification de la validité du mot
        if len(proposition) != nb_lettres:
            print("Erreur: Le mot ne contient pas le bon nombre de lettres!")
            continue

        # Comparaison du mot proposé avec le mot à trouver
        resultat = ""
        for i in range(nb_lettres):
            if proposition[i] == mot_a_trouver[i]:
                resultat += proposition[i].upper()  # lettre bien placée
            elif proposition[i] in mot_a_trouver:
                resultat += proposition[i].lower()  # lettre présente mais mal placée
            else:
                resultat += "."  # lettre absente

        print(f"Résultat: {resultat}")

        if proposition == mot_a_trouver:
            print(f"Bravo ! Vous avez trouvé le mot en {essais} essais.")
            break

"///////////////////////////////////////////////////////////////////////////////////////////"
def demande_nombres():
    choix = input("Voulez-vous entrer vos propres nombres ? (oui/non): ")
    if choix.lower() == "oui":
        nombres = []
        for i in range(6):
            nb = int(input(f"Entrez le nombre {i+1} entre 1 et 100: "))
            nombres.append(nb)
    else:
        nombres = [random.randint(1, 100) for _ in range(6)]
    return nombres

def demande_cible():
    choix = input("Voulez-vous choisir le nombre cible ? (oui/non): ")
    if choix.lower() == "oui":
        cible = int(input("Entrez le nombre cible entre 1 et 100: "))
    else:
        cible = random.randint(1, 100)
    return cible


def evaluer_expression(ops, nums):
    result = nums[0]
    expression = str(nums[0])
    steps = [expression]  # Commencer l'enregistrement des étapes avec le premier nombre

    for num, op in zip(nums[1:], ops):
        if op == operator.truediv and num == 0:  # Éviter la division par zéro
            return None, None, None
        try:
            new_result = op(result, num)
            if new_result < 0 or new_result != int(new_result):  # Valider le résultat positif et entier
                return None, None, None
            result = new_result
        except ZeroDivisionError:
            return None, None, None

        # Construire l'expression pour l'affichage
        op_symbol = '+' if op == operator.add else '-' if op == operator.sub else '*' if op == operator.mul else '/'
        expression += f" {op_symbol} {num}"
        steps.append(expression)  # Enregistrer chaque étape du calcul

    return result, expression, steps


def trouver_solution(nombres, cible):
    operations = [operator.add, operator.sub, operator.mul, operator.truediv]
    best_approximation = (None, float('inf'), None)  # Inclure les étapes dans le suivi de la meilleure approximation

    # Générer toutes les combinaisons possibles de nombres et d'opérations
    for nums in itertools.permutations(nombres):
        for ops in itertools.product(operations, repeat=len(nums) - 1):
            result, expr, steps = evaluer_expression(ops, nums)
            if result is not None:
                error = abs(result - cible)
                if result == cible:
                    return expr, steps  # Retourner immédiatement si on atteint la cible
                if error < best_approximation[1]:
                    best_approximation = (expr, error, steps)

    return best_approximation[0], best_approximation[2] if best_approximation[0] else (
    "Aucune solution valable trouvée.", None)


def le_compte_est_bon():
    print("Bienvenue dans le jeu 'Le compte est bon'!")
    if input("Souhaitez-vous jouer une partie? (oui/non): ").lower() != "oui":
        print("Merci d'être venu ! À bientôt !")
        return

    nombres = demande_nombres()
    cible = demande_cible()
    print(f"Les nombres sont : {nombres}")
    print(f"Le nombre cible est : {cible}")

    solution, etape = trouver_solution(nombres, cible)
    if solution:
        print(f"Solution trouvée : {solution}")
        if etape:
            print("Voici les étapes du calcul :")
            for step in etape:
                print(step)
    else:
        print("Aucune solution exacte ou approximative n'a été trouvée.")

le_compte_est_bon()