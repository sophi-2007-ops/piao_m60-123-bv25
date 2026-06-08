from src.db.backend.memory import MemoryDB
from src.db.tui import Interface


def main():
    repository = MemoryDB()
    app = Interface(repository=repository)
    app.run()


if __name__ == "__main__":
    main()
