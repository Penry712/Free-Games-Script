import requests
import sqlite3

class GamerPowerAPI:
    def __init__(self):
        self.base_url = "https://gamerpower.com/api"

    def get_pc_giveaways(self):
        url = f"{self.base_url}/giveaways"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der API-Anfrage: {e}")
            return []

class DatabaseManager:
    def __init__(self):
        self.db_name = "giveaways.db"
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE Platform (
                PlatformID INT PRIMARY KEY,
                Platform VARCHAR(255)
            );

            CREATE TABLE GameTyp (
                TypeID INT PRIMARY KEY,
                Type VARCHAR(255)
            );

            CREATE TABLE Game (
                GameID INT PRIMARY KEY,
                Title VARCHAR(255),
                Worth VARCHAR(100),
                Thumbnail VARCHAR(255),
                Image VARCHAR(255),
                Description TEXT,
                Instructions TEXT,
                OpenGiveawayURL VARCHAR(255),
                PublishedDate DATE,
                EndDate DATE,
                Users INT,
                Status VARCHAR(50),
                GamepowerURL VARCHAR(255),
                PlatformID INT,
                TypeID INT,
                FOREIGN KEY (PlatformID) REFERENCES Platform(PlatformID),
                FOREIGN KEY (TypeID) REFERENCES GameTyp(TypeID)
            );
        ''')
        
        conn.commit()
        conn.close()

    def save_giveaways(self, giveaways_list):
        if not giveaways_list:
            print("Keine Daten zum Speichern vorhanden.")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for item in giveaways_list:
            sql = '''
                INSERT OR REPLACE INTO giveaways 
                (id, title, type, platforms, worth, description, gamerpower_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            werte = (
                item.get('id'),
                item.get('title'),
                item.get('type'),
                item.get('platforms'),
                item.get('worth'),
                item.get('description'),
                item.get('gamerpower_url')
            )
            cursor.execute(sql, werte)
            
        conn.commit()
        conn.close()
        
        print(f"Erfolgreich {len(giveaways_list)} Giveaways in der Datenbank gespeichert.")

if __name__ == "__main__":
    print("Hole Daten von der GamerPower API...")
    
    api = GamerPowerAPI()
    pc_games = api.get_pc_giveaways()
    
    print(f" {len(pc_games)} PC-Giveaways gefunden. Speichere in SQLite...")
    
    db = DatabaseManager()
    db.save_giveaways(pc_games)

    print(" Fertig! Die Daten liegen nun in der Datei 'giveaways.db'.")
