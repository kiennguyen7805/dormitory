from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import engine


def main() -> None:
    with engine.connect() as db:
        seed_identity(db)
    print("Seeded Admin, Staff and Student demo accounts.")


if __name__ == "__main__":
    main()
