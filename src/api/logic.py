from src.database.setup import db
from src.utils.dataframe import DataFrameUtils
import os


class ApiLogic:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "../data/")
        pass

    def run_query(self, query, filename):
        try:
            result_df = db.execute_query(query, filename)

            print(result_df.head(2))

            # save dataframe result to csv
            DataFrameUtils.save_to_csv(
                result_df, self.data_path, filename=f"{filename}.csv"
            )
        except Exception as e:
            print(f"Error fetching & saving {filename} data: {e}")

    def get_shinkansen_data(self) -> None:
        query = """SELECT * FROM "test"."shinkansen_station" """
        filename = "shinkansen"

        self.run_query(query, filename)

    def get_tokyo_data(self) -> None:
        query = """select * from "test"."shinkansen_station"
                where  "Prefecture" ilike '%tokyo%'
        """
        filename = "tokyo"

        self.run_query(query, filename)


ApiLogicInstance = ApiLogic()
