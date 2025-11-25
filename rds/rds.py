"""
AWS RDS Module
"""

import boto3
import pymysql


# ==== PARAMÉTEREK ====
region = "eu-central-1"  # Frankfurt (változtatható)
rds_endpoint = "xxxxxxxxxx.eu-central-1.rds.amazonaws.com"
rds_port = 3306
rds_user = "admin"
rds_password = "xxxxxxxxxx"
rds_database = "xxxxxxx"
rds_table = "xxxxxxxxx"

# ==== RDS KLIENS LÉTREHOZÁSA ====


def client():
    rds_client = boto3.client("rds", region_name=region)
    """Kapcsolódás az RDS adatbázishoz és visszaadja a kapcsolatot"""
    try:
        connection = pymysql.connect(
            host=rds_endpoint,
            user=rds_user,
            password=rds_password,
            database=rds_database,
            port=rds_port,
        )
        print("Sikeres kapcsolódás az RDS adatbázishoz.")

        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            result = cursor.fetchone()
            print(f"Csatlakozva az adatbázishoz: {result[0]}")

        return connection

    except pymysql.MySQLError as e:
        print(f"Hiba történt az RDS adatbázishoz való kapcsolódás során: {e}")
        return None


# ==== Adatlekérdezés példa ====
def fetch_data_from_rds():
    """Egyszerű adatlekérdezés az RDS adatbázisból"""
    connection = client()

    if connection is None:
        print("Nem sikerült kapcsolódni az adatbázishoz.")
        return

    try:
        print("Adatlekérdezés az RDS adatbázisból...")

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {rds_table} LIMIT 5;")
            results = cursor.fetchall()
            for row in results:
                print(row)

    except pymysql.MySQLError as e:
        print(f"Hiba történt az adatlekérdezés során: {e}")
    finally:
        if connection and connection.open:
            connection.close()


def main():
    """Fő függvény az RDS kezeléséhez"""
    print("AWS RDS műveletek")
    print("========================")

    fetch_data_from_rds()


if __name__ == "__main__":
    main()
