#!/usr/bin/env python
"""
Script de démarrage simplifié pour l'application HomeSuites
"""
import os
import sys
import subprocess

def setup_environment():
    """Configure l'environnement de développement"""
    print("Configuration de l'environnement...")
    
    # Vérifier si l'environnement virtuel existe
    if not os.path.exists("venv"):
        print("Création de l'environnement virtuel...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    
    # Déterminer le chemin de l'activation
    if sys.platform == "win32":
        activate_script = os.path.join("venv", "Scripts", "activate")
        command_prefix = []
    else:
        activate_script = os.path.join("venv", "bin", "activate")
        command_prefix = ["source"]
    
    # Installer les dépendances
    print("Installation des dépendances...")
    if sys.platform == "win32":
        python_path = os.path.join("venv", "Scripts", "python")
    else:
        python_path = os.path.join("venv", "bin", "python")
    
    subprocess.check_call([python_path, "-m", "pip", "install", "-e", "."])
    
    # Instructions pour activer l'environnement
    print("\nPour activer l'environnement virtuel:")
    if sys.platform == "win32":
        print(f"    {activate_script}")
    else:
        print(f"    source {activate_script}")
    
    # Instructions pour lancer le serveur
    print("\nPour lancer le serveur de développement:")
    print(f"    {python_path} manage.py runserver")
    
    return True

def main():
    """Fonction principale"""
    print("=" * 80)
    print("HomeSuites - Outil de configuration")
    print("=" * 80)
    
    try:
        setup_environment()
        print("\nConfiguration terminée avec succès!")
        print("\nVous pouvez maintenant lancer l'application en suivant les instructions ci-dessus.")
    except Exception as e:
        print(f"\nErreur durant la configuration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())