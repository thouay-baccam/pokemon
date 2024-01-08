from code.file.file_paths import *
from code.personnage.personnage import Personnage


if __name__ == "__main__":
    mr_test = Personnage("Mr Test", "M", select_sprites("abra.png"), None, 0, 0)
    print(mr_test.name)
    print(mr_test.gender)
    print(mr_test.overworld_sprite)
    print(mr_test.battle_sprite)
