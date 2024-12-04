import psycopg2
import pandas as pd
from pandas import DataFrame
import os


class DatabaseConnection:
    def __init__(self, host, database, user, password, port) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None
        self.data_path = os.path.join(os.path.dirname(__file__), "../data")
        # Initialize connection
        self.initialize()

    def initialize(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                )
                self.cursor = self.connection.cursor()
                print("Connected to database")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error connecting to PostgreSQL database: {error}")

    def execute_query(self, query, filename) -> DataFrame:
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]  # Get column names
            result_df = pd.DataFrame(result, columns=columns)

            return result_df
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error executing query: {error}, Connection error")
            return None

    async def close(self):
        """Close the database connection and cursor"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None
