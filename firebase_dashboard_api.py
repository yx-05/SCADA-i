import os
import firebase_admin
from firebase_admin import credentials, firestore, auth

class FirebaseDashboardAPI:
    def __init__(self, cred_filename=".json"):
        """
        Initializes the connection to the Firebase project.

        Args:
            cred_filename (str): The file name of the Firebase service account key JSON file.
        """
        try:
            # Build absolute path (safe even if script is run from another folder)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cred_path = os.path.join(script_dir, cred_filename)

            # Initialize Firebase only once
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)

            self.db = firestore.client()
            print("Connected to Firestore database.")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            self.db = None

    def verify_user_token(self, id_token):
        """
        Verifies the Firebase ID token sent from the frontend.

        Args:
            id_token (str): The JWT token from the client.

        Returns:
            dict: The decoded user token information, or None if invalid.
        """
        if not firebase_admin._apps:
            print("Firebase app not initialized.")
            return None
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying auth token: {e}")
            return None

    def get_dashboard_data(self, user_id):
        """
        Fetches live dashboard data from Firestore for a specific user.

        Args:
            user_id (str): The unique ID of the user.

        Returns:
            dict: A dictionary containing the dashboard data, or None on error.
        """
        if not self.db:
            print("Firestore client not initialized.")
            return None
        try:
            doc_ref = self.db.collection('dashboards').document(user_id)
            doc = doc_ref.get()

            if doc.exists:
                return doc.to_dict()
            else:
                print(f"No dashboard data found for user: {user_id}")
                self._create_default_dashboard_data(user_id)
                return self.get_dashboard_data(user_id)
        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            return None

    def _create_default_dashboard_data(self, user_id):
        """Creates a default data structure for a new user."""
        try:
            default_data = {
                "live_data": {
                    "carbon_level": 420,
                    "power_consumption": 6430,
                    "occupancy": 23,
                    "occupancy_total": 60,
                    "energy_saved_today": 2200
                },
                "devices": {
                    "ac_units": False,
                    "computers": True,
                    "lights": True,
                    "microwave": False
                },
                "ai_predictions": {
                    "optimize_active": False
                },
                "occupancy_grid": {
                    "A01": "Available",
                    "A02": "Occupied",
                    "A03": "Occupied"
                }
            }
            self.db.collection('dashboards').document(user_id).set(default_data)
            print(f"Created default dashboard for user: {user_id}")
        except Exception as e:
            print(f"Error creating default data: {e}")

    def stream_dashboard_data(self, user_id, callback):
        """
        Sets up a real-time listener for dashboard data changes.

        Args:
            user_id (str): The unique ID of the user.
            callback (function): The function to call with updates.
        """
        if not self.db:
            print("Firestore client not initialized.")
            return None

        doc_ref = self.db.collection('dashboards').document(user_id)
        doc_watch = doc_ref.on_snapshot(lambda docs, changes, read_time: callback(docs))
        return doc_watch

    def toggle_device_control(self, user_id, device_id, new_state):
        """
        Updates the state of a device (e.g., AC, lights) in Firestore.
        """
        if not self.db:
            print("Firestore client not initialized.")
            return False
        try:
            doc_ref = self.db.collection('dashboards').document(user_id)
            doc_ref.update({f'devices.{device_id}': new_state})
            print(f"Set device '{device_id}' to '{new_state}' for user '{user_id}'")
            return True
        except Exception as e:
            print(f"Error updating device state: {e}")
            return False

    def toggle_ai_prediction(self, user_id, new_state):
        """
        Toggles the AI prediction feature on or off.
        """
        if not self.db:
            print("Firestore client not initialized.")
            return False
        try:
            doc_ref = self.db.collection('dashboards').document(user_id)
            doc_ref.update({'ai_predictions.optimize_active': new_state})
            print(f"Set AI optimization to '{new_state}' for user '{user_id}'")
            return True
        except Exception as e:
            print(f"Error toggling AI prediction: {e}")
            return False


# ---------------- Example Usage ----------------
if __name__ == '__main__':
    # Initialize the API with default "serviceAccountKey.json"
    firebase_api = FirebaseDashboardAPI()

    if firebase_api.db:
        test_user_id = "user_abc_123"

        # Fetch data
        print(f"\n--- Fetching data for user: {test_user_id} ---")
        dashboard_data = firebase_api.get_dashboard_data(test_user_id)
        if dashboard_data:
            print("Current Power Consumption:", dashboard_data.get('live_data', {}).get('power_consumption'))
            print("AC Units On:", dashboard_data.get('devices', {}).get('ac_units'))

        # Toggle a device
        print("\n--- Toggling AC units to ON ---")
        firebase_api.toggle_device_control(test_user_id, 'ac_units', True)

        updated_data = firebase_api.get_dashboard_data(test_user_id)
        if updated_data:
            print("Updated AC Units On:", updated_data.get('devices', {}).get('ac_units'))

        # Toggle AI predictions
        print("\n--- Toggling AI Optimize to ON ---")
        firebase_api.toggle_ai_prediction(test_user_id, True)