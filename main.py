import asyncio
import os
import sys

# Garante que o Python encontre o pacote src
sys.path.append(os.getcwd())

# Importa o main original de dentro da pasta src
from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
