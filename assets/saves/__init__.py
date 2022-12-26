import json

from assets import SAVE_DIR

def load(number: int) -> dict:
    """load(number: int) -> dict\n
    cette fonction charge les données de sauvegarde allouées à `number`

    Args:
        number (int): 1, 2 ou 3

    Returns:
        dict: les données sauvegardées
    """
    with open(f"{SAVE_DIR}/savefile{number}.json") as f:
        return json.load(f)

def save(data: dict, number: int) -> None:
    """save(data: dict, number: int) -> None

    Args:
        data (dict): données à rajouter au fichier de sauvegarde
        number (int): 1, 2 ou 3
    """
    with open(f"{SAVE_DIR}/savefile{number}.json", "a+") as f:
        json.dump(data, f)
