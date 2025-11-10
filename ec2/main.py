"""
AWS EC2 műveletek
"""

import boto3
from botocore.exceptions import ClientError
import argparse
import os

# ==== KÜLSŐ PARAMÉTEREK ====
# Művelet típusok:
# "ssh_key" - SSH kulcspár létrehozása
# "create" - EC2 példány létrehozása
# "delete" - EC2 példány törlése
#
# Használat:
# python main.py -muvelet ssh_key
# python main.py -muvelet create
# python main.py -muvelet delete
# ===========================

# Paraméterek beállítása
# Külső paraméterek kezelése (CLI + környezeti változó fallback)
parser = argparse.ArgumentParser(description="AWS EC2 műveletek")
parser.add_argument(
    "-m",
    "--muvelet",
    choices=["ssh_key", "create", "delete"],
    default=os.getenv("EC2_MUVELET", "none"),
    help="Végrehajtandó művelet (ssh_key | create | delete)",
)
args = parser.parse_args()
muvelet = args.muvelet


# ==== PARAMÉTEREK ====
region = "eu-central-1"  # Frankfurt (változtatható)
instance_name = "mentor-vm"
instance_type = "t3.micro"
key_pair_name = "mentor-keypair"

# Ezt AZ ADOTT RÉGIÓHOZ való Amazon Linux 2 AMI-ra kell frissíteni!
# Konzolról vagy AWS dokumentációból.
ami_id = "ami-004e960cde33f9146"


def main(muvelet):
    """Fő függvény az EC2 kezeléséhez"""
    # ======================
    ec2_client = boto3.resource("ec2", region_name=region)

    print("AWS EC2 műveletek")
    print("========================")
    if muvelet not in ["ssh_key", "create", "delete"]:
        print("Nem megfelelő művelet. Kérem, adjon meg egy érvényes műveletet.")
        return
    if muvelet == "ssh_key":
        print("SSH kulcspár létrehozása...")
        print("========================")
        try:
            key = ec2_client.create_key_pair(KeyName=key_pair_name)
            # Mentés fájlba
            pem_file = "./" + key_pair_name + ".pem"
            with open(pem_file, "w") as f:
                f.write(key.key_material)
            # Jogosultságok beállítása (csak olvasható a tulajdonos számára)
            os.chmod(pem_file, 0o400)
            print("SSH kulcspár létrehozva:", key_pair_name)
            print("Privát kulcs mentve:", pem_file)
        except ClientError as e:
            print("Hiba az SSH kulcspár létrehozásakor:", e)

    if muvelet == "create":
        print("EC2 példány létrehozása...")
        print("========================")
        try:
            # SSH kulcspár ellenőrzése
            try:
                ec2_client.KeyPair(key_pair_name).load()
                print("SSH kulcspár megtalálva:", key_pair_name)
            except ClientError:
                print(
                    "SSH kulcspár nem található. Kérem, előbb hozzon létre egy kulcspárt a 'ssh_key' művelettel."
                )
                return

            # EC2 példány létrehozása SSH kulcspárral és címkével
            instances = ec2_client.create_instances(
                ImageId=ami_id,
                InstanceType=instance_type,
                MinCount=1,
                MaxCount=1,
                TagSpecifications=[
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": "Name", "Value": instance_name}],
                    }
                ],
                KeyName=key_pair_name,
            )

            instance = instances[0]
            print("EC2 létrehozva, instance ID:", instance.id)

        except ClientError as e:
            print("Hiba az EC2 létrehozásakor:", e)

    if muvelet == "delete":
        print("EC2 példány törlése...")
        print("========================")
        try:
            # Példány keresése név alapján
            instances = ec2_client.instances.filter(
                Filters=[{"Name": "tag:Name", "Values": [instance_name]}]
            )

            instance_ids = [instance.id for instance in instances]

            if not instance_ids:
                print("Nincs törölhető példány ezzel a névvel:", instance_name)
                return

            # Példányok leállítása és törlése
            ec2_client.instances.filter(InstanceIds=instance_ids).terminate()
            print("EC2 példány(ok) törölve, instance ID-k:", instance_ids)

        except ClientError as e:
            print("Hiba az EC2 törlésekor:", e)


if __name__ == "__main__":
    main(muvelet)
