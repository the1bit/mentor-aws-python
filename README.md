# Mentor AWS Pyrthon

Ez a repository a Mentoráláshoz kapcsolódó AWS Python kódokat tartalmazza.

## Tartalom

- `ec2/main.py`: EC2 példányok létrehozása és kezelése Python segítségével.
- `s3/main.py`: S3 bucket létrehozása és fájlok kezelése Python segítségével.

## Előfeltételek

- Python 3.x telepítve a gépeden. (3.10 vagy újabb ajánlott)
- AWS fiók és hozzáférési kulcsok (Access Key ID és Secret Access Key).
- AWS CLI telepítve és konfigurálva a gépeden.


## AWS-cli beállítása

1. Ellenőrizd, hogy az AWS CLI telepítve van-e:

   ```bash
   aws --version
   ```

2. Ha nincs telepítve,m akkor telepítsd.
3. Állítsd be az AWS hozzáférési kulcsaidat:

   ```bash
   aws configure
   ```

   Add meg a következő adatokat, amikor kéri:

   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name (pl. eu-central-1)
   - Default output format (pl. json)

4. Ellenőrizd a beállításokat:

   ```bash
   aws sts get-caller-identity
   ```

   Ha helyesen vannak beállítva a kulcsok, akkor megjelenik a fiókod azonosítója.

5. 


## Használat

1. Klónozd a repository-t:

   ```bash
   git clone https://github.com/the1bit/mentor-aws-python.git
    cd mentor-aws-python
   ```

2. Hozz létre és aktiváld a virtuális környezetet.

Lépj be a megfelelő könyvtárba (ec2 vagy s3), majd futtasd:

- Windows:

  ```bash
  python -m venv venv
  venv\Scripts\activate     # Windows
  ```

_Deaktiváld a virtuális környezetet, ha végeztél:_

```bash
deactivate
```

- macOS/Linux:

  ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
  ```

  _Deaktiváld a virtuális környezetet, ha végeztél:_

  ```bash
   deactivate
  ```

3. Telepítsd a szükséges csomagokat:

   ```bash
   pip install -r requirements.txt
   ```

4. Futtasd a kívánt szkriptet a megfelelő módon

   ```bash
    python main.py -h
   ```
