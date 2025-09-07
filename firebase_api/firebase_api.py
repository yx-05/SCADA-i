import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
import time
import threading

class FirebaseAPI:
    """
    A class to handle communication between a local SQLite database and Google Firestore.
    - Sends the current state of devices from SQLite to Firestore.
    - Listens for new control commands from Firestore and saves them to SQLite.
    """

    def __init__(self, cred_path, db_path):
        """
        Initializes the Firebase Admin SDK and connects to the local SQLite database.

        Args:
            cred_path (str): The file path to the Firebase service account credentials JSON.
            db_path (str): The file path to the local SQLite database.
        """
        try:
            # Initialize Firebase Admin
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            self.firestore_db = firestore.client()
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise

        try:
            # Connect to the local SQLite database
            self.sqlite_conn = sqlite3.connect(db_path, check_same_thread=False)
            self.sqlite_conn.row_factory = sqlite3.Row # Allows accessing columns by name
            print(f"Successfully connected to SQLite database at {db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise

    def sync_current_state_to_firestore(self):
        """
        Fetches the most recent data from the 'realtime_state' table in SQLite
        and overwrites it in the 'realtime_state' collection in Firestore.
        This ensures Firestore only holds the current data.
        """
        print("\nStarting sync from SQLite to Firestore...")
        try:
            cursor = self.sqlite_conn.cursor()
            cursor.execute("SELECT * FROM realtime_state")
            all_devices_state = cursor.fetchall()

            if not all_devices_state:
                print("No device states found in local DB to sync.")
                return

            for device_state in all_devices_state:
                # Convert the sqlite3.Row object to a dictionary
                state_dict = dict(device_state)
                device_id = str(state_dict['device_id'])

                # Use the device_id as the document ID in Firestore
                doc_ref = self.firestore_db.collection('realtime_state').document(device_id)

                # Use .set() to create or completely overwrite the document
                doc_ref.set(state_dict)
                print(f"  - Synced data for device_id: {device_id}")

            print("Sync to Firestore completed successfully.")

        except sqlite3.Error as e:
            print(f"An error occurred while reading from SQLite: {e}")
        except Exception as e:
            print(f"An error occurred during Firestore sync: {e}")

    def _save_command_to_local_db(self, command_data):
        """
        Saves a single command received from Firestore into the local SQLite DB.
        (Internal method)
        """
        print(f"  - Saving new command {command_data['command_id']} to local DB...")
        try:
            # Ensure required fields are present
            required_fields = ['command_id', 'device_id', 'timestamp', 'command', 'source', 'status']
            for field in required_fields:
                if field not in command_data:
                    print(f"    - Command missing required field: {field}. Skipping.")
                    return

            cursor = self.sqlite_conn.cursor()
            cursor.execute(
                """
                INSERT INTO control_commands (command_id, device_id, timestamp, command, source, status)
                VALUES (:command_id, :device_id, :timestamp, :command, :source, :status)
                """,
                command_data
            )
            self.sqlite_conn.commit()
            print(f"  - Successfully saved command {command_data['command_id']}.")

        except sqlite3.IntegrityError:
            # This can happen if two listeners try to write the same command.
            print(f"  - Command with ID {command_data['command_id']} already exists in local DB. Skipping.")
        except sqlite3.Error as e:
            print(f"  - SQLite error while saving command: {e}")


    def listen_for_control_commands(self):
        """
        Sets up a real-time listener on the 'control_commands' collection in Firestore.
        Listens for newly added documents with status 'pending'.
        """
        # A callback to run when a snapshot is received
        def on_snapshot(col_snapshot, changes, read_time):
            print("\nReceived new snapshot from 'control_commands'...")
            for change in changes:
                if change.type.name == 'ADDED':
                    command_doc = change.document
                    command_data = command_doc.to_dict()
                    command_data['command_id'] = command_doc.id # Use firestore doc id as primary key

                    print(f"New command detected: ID {command_doc.id}")
                    # Save the new command to the local database
                    self._save_command_to_local_db(command_data)

                    # Optional: Update the status in Firestore to 'received'
                    # to prevent re-processing
                    command_doc.reference.update({'status': 'received by server'})


        collection_ref = self.firestore_db.collection('control_commands').where('status', '==', 'pending')

        # Watch the collection for changes
        self.command_listener = collection_ref.on_snapshot(on_snapshot)
        print("--> Now listening for new control commands from Firestore...")

        # Keep the main thread alive to allow the listener to run in the background
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping listener...")
            self.command_listener.unsubscribe()


if __name__ == '__main__':
    # --- CONFIGURATION ---
    # IMPORTANT: Replace with the actual path to your files
    FIREBASE_CREDENTIALS_PATH = 'firebase-service-account-key.json'
    SQLITE_DATABASE_PATH = 'database.db'

    # --- EXECUTION ---
    try:
        # 1. Initialize the API class
        firebase_comm = FirebaseAPI(FIREBASE_CREDENTIALS_PATH, SQLITE_DATABASE_PATH)

        # 2. Perform an initial sync of data from local DB to Firestore
        firebase_comm.sync_current_state_to_firestore()

        # 3. Start listening for commands from Firestore in a separate thread
        # This allows you to run other tasks in your main application if needed
        listener_thread = threading.Thread(target=firebase_comm.listen_for_control_commands)
        listener_thread.daemon = True # Allows main program to exit even if thread is running
        listener_thread.start()

        # The main thread can do other things or just wait.
        # Here we'll just keep it alive to see listener output.
        while listener_thread.is_alive():
            listener_thread.join(timeout=1)

    except FileNotFoundError:
        print(f"FATAL ERROR: The credential file was not found at '{FIREBASE_CREDENTIALS_PATH}'.")
        print("Please download your service account key from Firebase and update the path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")