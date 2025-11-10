"""
AWS S3 műveletek
"""

import boto3
from botocore.exceptions import ClientError
import argparse
import os
import uuid

# ==== KÜLSŐ PARAMÉTEREK ====
# Művelet típusok:
# "create" - S3 bucket létrehozása
# "delete" - S3 bucket törlése
# "list" - S3 buckets listázása
#
# Használat:
# python main.py -m create
# python main.py -m delete
# python main.py -m list
# ===========================

# Paraméterek beállítása
# Külső paraméterek kezelése (CLI + környezeti változó fallback)
parser = argparse.ArgumentParser(description="AWS S3 műveletek")
parser.add_argument(
    "-m",
    "--muvelet",
    choices=["create", "delete", "list"],
    default=os.getenv("S3_MUVELET", "list"),
    help="Végrehajtandó művelet (create | delete | list)",
)
args = parser.parse_args()
muvelet = args.muvelet


# ==== PARAMÉTEREK ====
region = "eu-central-1"  # Frankfurt (változtatható)
bucket_name = "mentor-984c61e3"  # Egyedi azonosítók teszthez: 984c61e3, a1b2c3d4, f5e6d7c8, 9a8b7c6d


def main(muvelet):
    """Fő függvény az S3 kezeléséhez"""
    # ======================
    s3_client = boto3.client("s3", region_name=region)

    print("AWS S3 műveletek")
    print("========================")
    
    if muvelet not in ["create", "delete", "list"]:
        print("Nem megfelelő művelet. Kérem, adjon meg egy érvényes műveletet.")
        return

    if muvelet == "list":
        print("S3 buckets listázása...")
        print("========================")
        try:
            response = s3_client.list_buckets()
            buckets = response.get("Buckets", [])
            
            if not buckets:
                print("Nincsenek S3 buckets a fiókban.")
            else:
                print(f"Talált {len(buckets)} bucket(et):")
                for bucket in buckets:
                    print(f"  - {bucket['Name']} (létrehozva: {bucket['CreationDate']})")
        except ClientError as e:
            print("Hiba a buckets listázásakor:", e)

    if muvelet == "create":
        print("S3 bucket létrehozása...")
        print("========================")
        try:
            # EU régióban különleges LocationConstraint szükséges
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region}
                )
            print("S3 bucket létrehozva:", bucket_name)
            print("Régió:", region)
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"Hiba: A bucket név '{bucket_name}' már használatban van (globálisan egyedinek kell lennie).")
            elif e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                print(f"A bucket '{bucket_name}' már létezik a fiókjában.")
            else:
                print("Hiba az S3 bucket létrehozásakor:", e)

    if muvelet == "delete":
        print("S3 bucket törlése...")
        print("========================")
        try:
            # Ellenőrzés: bucket létezik-e
            s3_client.head_bucket(Bucket=bucket_name)
            
            # Bucket tartalmának törlése (objektumok és verziók)
            print(f"Bucket '{bucket_name}' tartalmának törlése...")
            s3_resource = boto3.resource("s3", region_name=region)
            bucket = s3_resource.Bucket(bucket_name)
            
            # Összes objektum és verzió törlése
            bucket.object_versions.all().delete()
            
            # Bucket törlése
            s3_client.delete_bucket(Bucket=bucket_name)
            print(f"S3 bucket törölve: {bucket_name}")
            
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"A bucket '{bucket_name}' nem található.")
            elif e.response['Error']['Code'] == 'BucketNotEmpty':
                print(f"A bucket '{bucket_name}' nem üres. Kérem, először törölje a tartalmát.")
            else:
                print("Hiba az S3 bucket törlésekor:", e)


if __name__ == "__main__":
    main(muvelet)
