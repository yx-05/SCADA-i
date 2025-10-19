# # file: api_server.py
# from flask import Flask, jsonify
# from flask_cors import CORS
# import sqlite3

# # --- IMPORTANT: SET YOUR DATABASE PATH ---
# # It should match the DB_PATH used in mqtt_connection.py
# DB_PATH = "your_database_file.db" 

# app = Flask(__name__)
# # Allows Next.js to fetch data from this API
# CORS(app) 

# @app.route('/api/dashboard/stats', methods=['GET'])
# def dashboard_stats():
#     conn = None
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row 
#         cursor = conn.cursor()

#         # Fetch ALL latest device states
#         # The realtime_state table holds the most current value for each device_id
#         cursor.execute("SELECT * FROM realtime_state")
#         devices_data = cursor.fetchall()

#         # --- Aggregation Logic (Calculate totals for Stat Cards) ---
#         total_power = sum(float(d['power_usage'] or 0) for d in devices_data)
#         total_occupancy = sum(int(d['occupancy'] or 0) for d in devices_data)
        
#         # NOTE: Carbon/Energy are usually historical calculations; using placeholders
#         carbon_level = 425 
#         energy_saved = 2250 
        
#         # Total seats (replace 60 with your actual total capacity)
#         total_seats = 18 

#         response_data = {
#             "carbonLevel": carbon_level,
#             "powerConsumption": round(total_power, 2),
#             "occupancy": {
#                 "current": total_occupancy,
#                 "total": total_seats
#             },
#             "energySaved": energy_saved,
#             # Pass detailed device data (optional, but useful for the map)
#             "devices": [dict(row) for row in devices_data]
#         }
        
#         return jsonify(response_data)
#     except Exception as e:
#         print(f"API Error: {e}")
#         return jsonify({"error": "Could not retrieve data"}), 500
#     finally:
#         if conn:
#             conn.close()

# if __name__ == '__main__':
#     # Run the API on port 5000 (standard port for Flask)
#     app.run(host='0.0.0.0', port=5000, debug=True)