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
        
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Platform (
                PlatformID INTEGER PRIMARY KEY AUTOINCREMENT,
                Platform TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS GameTyp (
                TypeID INTEGER PRIMARY KEY AUTOINCREMENT,
                Type TEXT UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Game (
                GameID INTEGER PRIMARY KEY,
                Title TEXT,
                Worth TEXT,
                Thumbnail TEXT,
                Image TEXT,
                Description TEXT,
                Instructions TEXT,
                OpenGiveawayURL TEXT,
                PublishedDate TEXT,
                EndDate TEXT,
                Users INTEGER,
                Status TEXT,
                GamepowerURL TEXT,
                TypeID INTEGER,
                FOREIGN KEY (TypeID) REFERENCES GameTyp(TypeID)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS GamePlatform (
                GameID INTEGER,
                PlatformID INTEGER,
                PRIMARY KEY (GameID, PlatformID),
                FOREIGN KEY (GameID) REFERENCES Game(GameID),
                FOREIGN KEY (PlatformID) REFERENCES Platform(PlatformID)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_giveaways(self, giveaways_list):
        if not giveaways_list:
            print("Keine Daten zum Speichern vorhanden.")
            return

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        for item in giveaways_list:
            type_name = item.get('type')
            cursor.execute('INSERT OR IGNORE INTO GameTyp (Type) VALUES (?)', (type_name,))
            cursor.execute('SELECT TypeID FROM GameTyp WHERE Type = ?', (type_name,))
            type_id = cursor.fetchone()[0]
            
            game_id = item.get('id')
            sql_game = '''
                INSERT OR REPLACE INTO Game 
                (GameID, Title, Worth, Thumbnail, Image, Description, Instructions, 
                 OpenGiveawayURL, PublishedDate, EndDate, Users, Status, GamepowerURL, TypeID)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            werte_game = (
                game_id,
                item.get('title'),
                item.get('worth'),
                item.get('thumbnail'),
                item.get('image'),
                item.get('description'),
                item.get('instructions'),
                item.get('open_giveaway_url'),
                item.get('published_date'),
                item.get('end_date'),
                item.get('users'),
                item.get('status'),
                item.get('gamerpower_url'),
                type_id
            )
            cursor.execute(sql_game, werte_game)

            platforms_string = item.get('platforms', '')
            platform_list = [p.strip() for p in platforms_string.split(',') if p.strip()]
            
            for platform_name in platform_list:
                cursor.execute('INSERT OR IGNORE INTO Platform (Platform) VALUES (?)', (platform_name,))
                cursor.execute('SELECT PlatformID FROM Platform WHERE Platform = ?', (platform_name,))
                platform_id = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT OR IGNORE INTO GamePlatform (GameID, PlatformID)
                    VALUES (?, ?)
                ''', (game_id, platform_id))
            
        conn.commit()
        conn.close()
        
        print(f"Erfolgreich {len(giveaways_list)} Giveaways in der Datenbank gespeichert.")

if __name__ == "__main__":
    print("Hole Daten von der GamerPower API...")
    
    api = GamerPowerAPI()
    pc_games = api.get_pc_giveaways()
    
    print(f" {len(pc_games)} Giveaways gefunden. Speichere in SQLite...")
    
    db = DatabaseManager()
    db.save_giveaways(pc_games)

    print(" Fertig! Die Daten liegen nun in der Datei 'giveaways.db'.")