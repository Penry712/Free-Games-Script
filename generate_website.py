import sqlite3

def erstelle_webseite():
    conn = sqlite3.connect('giveaways.db')
    cursor = conn.cursor()
    
    query = '''
        SELECT Game.Title, Game.Worth, GameTyp.Type, GROUP_CONCAT(Platform.Platform, ', '), Game.Thumbnail, Game.OpenGiveawayURL
        FROM Game
        LEFT JOIN GameTyp ON Game.TypeID = GameTyp.TypeID
        LEFT JOIN GamePlatform ON Game.GameID = GamePlatform.GameID
        LEFT JOIN Platform ON GamePlatform.PlatformID = Platform.PlatformID
        GROUP BY Game.GameID
    '''
    
    cursor.execute(query)
    games = cursor.fetchall()
    conn.close()

    html_content = """
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>Free Games Übersicht</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; color: #333; }
            h1 { text-align: center; margin-bottom: 40px; }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
            }
            .card {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                overflow: hidden;
                transition: transform 0.2s;
            }
            .card:hover {
                transform: translateY(-5px);
            }
            .card img {
                width: 100%;
                height: auto;
                border-bottom: 1px solid #ddd;
            }
            .card-content {
                padding: 15px;
            }
            .card-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .card-info {
                font-size: 0.9em;
                color: #555;
                margin-bottom: 5px;
            }
            .card-info strong {
                color: #222;
            }
            .btn {
                display: block;
                text-align: center;
                margin-top: 15px;
                padding: 10px;
                background-color: #007BFF;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Aktuelle Free Games</h1>
        <div class="grid-container">
    """

    for game in games:
        titel = game[0]
        wert = game[1] if game[1] != "N/A" else "Kostenlos"
        kategorie = game[2]
        plattformen = game[3]
        bild_url = game[4]
        link = game[5]
        
        html_content += f"""
            <div class="card">
                <img src="{bild_url}" alt="Bild von {titel}">
                <div class="card-content">
                    <div class="card-title">{titel}</div>
                    <div class="card-info"><strong>Wert:</strong> {wert}</div>
                    <div class="card-info"><strong>Kategorie:</strong> {kategorie}</div>
                    <div class="card-info"><strong>Plattformen:</strong> {plattformen}</div>
                    <a href="{link}" target="_blank" class="btn">Zum Giveaway</a>
                </div>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)
        
    print("Fertig! Die Datei 'index.html' wurde mit dem neuen Karten-Design erstellt.")

if __name__ == "__main__":
    erstelle_webseite()