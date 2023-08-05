import builtins
import sqlite3
import contextlib
import pandas as pd
from pypadel import Match, Player
from .schemas import MATCHES_TABLE, PLAYERS_TABLE
from .crud import MatchCRUD, PlayerCRUD
from .stats import MatchStats


class SqlDatabase:
    def __init__(self, name: str, existing: bool = False) -> None:
        # If the 'existing' flag is True, we assume that the given name already contains the '.db' extension
        self.db_name = name if existing else name + ".db"
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row

        # Initialize tables
        self.tables = {
            "matches": SqlTable(self.conn, "matches", MATCHES_TABLE),
            "players": SqlTable(self.conn, "players", PLAYERS_TABLE),
        }

        # Initialize the CRUD managers
        self.match_manager = MatchCRUD(self)
        self.player_manager = PlayerCRUD(self)

    def table_to_dataframe(self, table_name: str) -> pd.DataFrame:
        """Retrieve the entire table content and return it as a pandas DataFrame."""
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            print(f"An error occurred while fetching the table '{table_name}': {e}")
            return None

    @classmethod
    def init_from_existing(cls, db_filename: str):
        return cls(db_filename, existing=True)

    def _record_to_match_object(self, record):
        return Match.from_record(record)

    def load_db(self, file, **kwargs):
        data_manager = ExcelDataManager(file, self)
        data_manager.load_data(**kwargs)

    def add_match(self, m, cat):
        self.match_manager.add_match(m, cat)

    def get_match_stats(self, match_id, img_export=False):
        match_stats_instance = MatchStats(self.conn, match_id)
        if img_export:
            summary = match_stats_instance.get_match_summary()
            return match_stats_instance.export_summary_to_image(summary)
        return match_stats_instance.get_match_summary()

    def export_all(self):
        try:
            with contextlib.closing(self.conn.cursor()) as cursor:
                cursor.execute("SELECT * FROM matches")
                matches = cursor.fetchall()
                for match_record in matches:
                    m = self._record_to_match_object(match_record)
                    m.export()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
            raise

    def export_raw(self, file: str = None) -> None:
        """Export raw match and player data to an Excel file."""
        if not file:
            file = f"database_export_{self.db_name.replace('.db', '')}.xlsx"

        # Fetch match data
        matches_df = self.table_to_dataframe("matches")

        # Fetch player data
        players_df = self.table_to_dataframe("players")

        with pd.ExcelWriter(file, engine="xlsxwriter") as writer:
            matches_df.to_excel(writer, sheet_name="Matches", index=False)
            players_df.to_excel(writer, sheet_name="Players", index=False)

    def open_database(self):
        """Reopen the database connection if it's closed."""
        if self.conn is None or self.conn.closed:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


class SqlTable:
    def __init__(self, conn, name, schema):
        self.conn = conn
        self.name = name
        self.schema = schema
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.conn.execute(self.schema)
        except sqlite3.Error as e:
            print(
                f"An error occurred while creating the {self.name} table: {e.args[0]}"
            )
            self.conn.rollback()
            raise


class ExcelDataManager:
    def __init__(self, file_path, db_instance):
        self.file_path = file_path
        self.db = db_instance

    def load_data(self, **kwargs):
        xls = pd.ExcelFile(self.file_path)  # Open the Excel file
        for (
            sheet_name
        ) in xls.sheet_names:  # Loop through all the sheets in the Excel file
            df = pd.read_excel(self.file_path, sheet_name=sheet_name, **kwargs)
            df.columns = df.columns.str.strip().str.lower()
            for index, row in df.iterrows():
                self._create_match(
                    row, sheet_name
                )  # Pass the sheet name to the _create_match method

        # After processing all matches, update player statistics
        players_to_update = (
            builtins.set()
        )  # This set keeps track of the players whose stats need to be updated.
        for index, row in df.iterrows():
            players_to_update.update(
                [row.player_1, row.player_2, row.player_3, row.player_4]
            )

        for player_name in players_to_update:
            self.db.player_manager.update_player_stats(player_name)

    def _create_match(self, row, cat):
        # Step 1: Attempt to Convert Timestamp to a datetime.date object
        try:
            converted_date = row.date.to_pydatetime().date()
        except AttributeError:
            print(
                f"Error: Could not convert the date for the match with details: {row}. Using today's date as fallback."
            )
            from datetime import date

            converted_date = date.today()

        # Check if adv_game is present, if not default to False
        if "adv_game" in row:
            if isinstance(row.adv_game, str):
                adv_game = row.adv_game.lower() == "true"
            else:
                adv_game = bool(row.adv_game)  # Convert to bool if it's not a string
        else:
            adv_game = False

        print(f"Creating match with details: {row}")

        pl_name = [row.player_1, row.player_2, row.player_3, row.player_4]
        players = [Player(name) for name in pl_name]

        m = Match.create(
            int(row.match_type),
            players=players,
            date=converted_date,
            tournament=row.tournament,
            r=str(row.r),
            adv_game=adv_game,
        )
        data = [x.strip(" ") for x in row.data.split(",")]
        m.play_match(data)
        m.sets_score = m.get_set_scores()

        # Step 2: Add the match to the database
        self.db.match_manager.add_match(m, cat)
