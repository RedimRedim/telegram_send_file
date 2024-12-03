from src.database.setup import db
from src.utils.dataframe import DataFrameUtils
import os


class ApiLogic:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "../data/")
        pass

    def get_shinkansen_data(self) -> None:
        try:
            result_df = db.execute_query(
                query="""SELECT * FROM "test"."shinkansen" """, filename="shinkansen"
            )

            # save dataframe result to csv
            DataFrameUtils.save_to_csv(result_df, self.data_path, filename="shinkansen")
        except Exception as e:
            print(f"Error fetching & saving shinkansen data: {e}")


ApiLogicInstance = ApiLogic()
