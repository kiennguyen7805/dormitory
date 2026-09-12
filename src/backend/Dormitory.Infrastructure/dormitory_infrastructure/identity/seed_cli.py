from dormitory_infrastructure.identity.seeder import seed_identity
from dormitory_infrastructure.persistence import SessionLocal


def main() -> None:
    with SessionLocal() as db:
        seed_identity(db)
    print("Seeded Admin, Staff and Student demo accounts.")


if __name__ == "__main__":
    main()
