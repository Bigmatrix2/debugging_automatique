# buggy_script.py
# Script volontairement plein de bugs pour tester le débogueur automatique

import maths   # Erreur : le module s'appelle "math"

def greet(name)
    print("Bonjour " + name)  # Erreur de syntaxe : manque deux-points

def divide(a, b):
    return a / c   # Erreur : variable 'c' non définie

def main():
    result = divide(10, 0)  # Erreur : division par zéro
    print("Résultat:", result)

    greet("Alice")

    print("La racine carrée de 16 est:", maths.sqrt(16))  # Erreur : mauvais module

    for i in range(5)
        print("Itération", i)  # Erreur de syntaxe : manque deux-points

    print("Fin du programme")

if __name__ == "__main__":
    main()

