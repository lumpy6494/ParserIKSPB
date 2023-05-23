from environs import Env

env = Env()
env.read_env()

SAVEFILE = env.str("SAVEFILE")  # Куда сохраняем файл
TIK = env.int("TIK") # Общее Количество коммисий
PATHCHROME=env.str("PATHCHROME")