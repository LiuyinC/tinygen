import sqlite3
from app.core.config import settings
from app.models.analytic_event import AnalyticEvent

## Usually the logger will connect to a queue, like kinesis or kafka, but for this example we will use a SQLite database
class EventLogger:
    def __init__(self) -> None:
        self.db_file = settings.SQLITE_EVENT_FILE

    def log_event(self, event: AnalyticEvent) -> None:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS events
              (id TEXT PRIMARY KEY,
               event_name TEXT,
               event_data TEXT,
               ts_created TEXT)''')
        print(event)
        # Insert the event into the table
        cursor.execute('''INSERT INTO events (id, event_name, event_data, ts_created)
              VALUES (?, ?, ?, ?)''', (event.id, event.event_name, event.model_dump_json(), event.ts_created))

        conn.commit()
        conn.close()
