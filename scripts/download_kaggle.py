import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import argparse

# Charger les variables d'environnement
load_dotenv(find_dotenv())

# Configuration des chemins
DATA_RAW_PATH = os.getenv('DATA_RAW_PATH')
KAGGLE_DATASET = "yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018"

# Années attendues
EXPECTED_YEARS = list(range(2009, 2019))  # 2009 à 2018 inclus

def check_csv_files():
    """
    Vérifie la présence de tous les fichiers CSV annuels.
    
    Returns:
        tuple: (list_of_missing_files, list_of_present_files)
    """
    data_dir = Path(DATA_RAW_PATH)
    
    # Créer le répertoire s'il n'existe pas
    data_dir.mkdir(parents=True, exist_ok=True)
    
    missing_files = []
    present_files = []
    
    for year in EXPECTED_YEARS:
        filename = f"{year}.csv"
        filepath = data_dir / filename
        
        if filepath.exists() and filepath.stat().st_size > 0:
            present_files.append(filename)
            print(f"{filename} - présent ({filepath.stat().st_size / 1e6:.1f} MB)")
        else:
            missing_files.append(filename)
            print(f"{filename} - manquant ou vide")
    
    return missing_files, present_files

def check_alternative_formats():
    """
    Vérifie si les fichiers existent dans d'autres formats possibles.
    """
    data_dir = Path(DATA_RAW_PATH)
    alternatives = []
    
    # Vérifier les noms alternatifs possibles
    patterns = [
        "airline_delay_*.csv",
        "delays_*.csv",
        "flights_*.csv"
    ]
    
    for pattern in patterns:
        for filepath in data_dir.glob(pattern):
            if filepath.suffix == '.csv':
                # Extraire l'année si possible
                alternatives.append(filepath.name)
    
    return alternatives

def print_instructions(missing_files, alternatives):
    """
    Affiche les instructions pour télécharger les fichiers manquants.
    """
    print("\n" + "="*60)
    print("TÉLÉCHARGEMENT REQUIS")
    print("="*60)
    
    if alternatives:
        print("\nFichiers alternatifs détectés:")
        for alt in alternatives:
            print(f"   - {alt}")
        print("\n   Renommez-les selon le format YYYY.csv")
        print("   Exemple: mv 'airline_delay_2009.csv' '2009.csv'\n")
    
    print(f"Fichiers manquants ({len(missing_files)}):")
    for f in missing_files:
        print(f"   - {f}")
    
    print(f"\nINSTRUCTIONS DE TÉLÉCHARGEMENT:")
    print(f"   1. Accédez au dataset Kaggle:")
    print(f"      https://www.kaggle.com/datasets/{KAGGLE_DATASET}")
    print(f"\n   2. Téléchargez les 10 fichiers CSV annuels (2009.csv à 2018.csv)")
    print(f"\n   3. Placez-les dans le dossier:")
    print(f"      {Path(DATA_RAW_PATH).absolute()}")
    
    print(f"\nASTUCES:")
    print(f"   - Téléchargez les fichiers depuis la page du dataset:")
    print(f"     https://www.kaggle.com/datasets/{KAGGLE_DATASET}")
    print(f"   - Ou téléchargez manuellement depuis le site puis placez les fichiers dans le dossier ci-dessus")
    
    print(f"\nTaille estimée: ~6.5-7 GB non compressé")
    print(f"   Alternativement, vous pouvez travailler avec 2015.csv seulement pour le prototypage")

def check_disk_space():
    """
    Vérifie l'espace disque disponible.
    """
    data_dir = Path(DATA_RAW_PATH)
    try:
        # Obtenir l'espace disque disponible (Unix/Windows compatible)
        import shutil
        free_space = shutil.disk_usage(data_dir.parent if data_dir.exists() else data_dir).free
        free_gb = free_space / (1024**3)
        
        if free_gb < 7:  # Moins de 7GB disponible
            print(f"\nATTENTION: Espace disque faible ({free_gb:.1f} GB disponible)")
            print(f"   Les données nécessitent ~7 GB non compressés")
            return False
        else:
            print(f"\nEspace disque disponible: {free_gb:.1f} GB")
            return True
    except Exception:
        # Ne pas bloquer si on ne peut pas vérifier l'espace
        return True

def main():
    parser = argparse.ArgumentParser(description='Vérification des données CSV Kaggle')
    parser.add_argument('--skip-check', action='store_true',
                       help='Ignorer la vérification (toujours succès)')
    args = parser.parse_args()
    
    if args.skip_check:
        print("Vérification ignorée (--skip-check)")
        sys.exit(0)
    
    print("="*60)
    print("VÉRIFICATION DES DONNÉES KAGGLE")
    print("="*60)
    print(f"Dossier de données: {Path(DATA_RAW_PATH).absolute()}")
    print(f"Période attendue: 2009-2018\n")
    
    # Vérifier l'espace disque
    check_disk_space()
    
    # Vérifier les fichiers CSV
    missing_files, present_files = check_csv_files()
    
    # Vérifier les formats alternatifs
    alternatives = check_alternative_formats()
    
    # Afficher le résumé
    print(f"\nRÉSUMÉ:")
    print(f"   Présents: {len(present_files)}/10 fichiers")
    print(f"   Manquants: {len(missing_files)}/10 fichiers")
    
    if len(present_files) == 10:
        print("\n" + "="*60)
        print("SUCCÈS - Tous les fichiers CSV sont présents!")
        print("="*60)
        print("\nLes fichiers vérifiés sont prêts pour la conversion en Parquet.")
        print("   Lancez 'make convert' ou 'python scripts/convert_to_parquet.py'")
        sys.exit(0)
    else:
        print_instructions(missing_files, alternatives)
        
        
        
        # Sortie avec erreur pour arrêter le pipeline
        print("\n" + "="*60)
        print("PIPELINE ARRÊTÉ - Fichiers CSV manquants")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()