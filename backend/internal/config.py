from pathlib import Path
import os

# В Docker контейнере WORKDIR /app, поэтому пути строим оттуда
BASE_DIR = Path("/app")


# Глобальные переменные

def loadConfig():
    pass
