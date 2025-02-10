from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuration de la base PostgreSQL sur Render
DB_HOST = "dpg-cuksmo23esus73avnce0-a.frankfurt-postgres.render.com"
DB_NAME = "esp32_data_k1gb"
DB_USER = "esp32_data_k1gb_user"
DB_PASSWORD = "WDVKFIkynbLNFDcHUMAlWNVY6KjDvsi2"
DB_PORT = "5432"

# Connexion à PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
)
cursor = conn.cursor()

@app.route('/store', methods=['POST'])
def store_data():
    try:
        data = request.json
        poids = data['poids']  # Récupération du poids envoyé par l'ESP32
        
        cursor.execute("INSERT INTO mesures (poids) VALUES (%s)", (poids,))
        conn.commit()
        
        return jsonify({"message": "Poids enregistré avec succès"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        cursor.execute("SELECT * FROM mesures ORDER BY timestamp DESC LIMIT 10;")
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
