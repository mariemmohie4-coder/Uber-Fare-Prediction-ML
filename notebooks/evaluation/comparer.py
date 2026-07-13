import pandas as pd

class Comparer:

    @staticmethod
    def compare(results):

         comparison_df = pd.DataFrame(results).T

         comparison_df = comparison_df.sort_values(
          by="R2",
         ascending=False
         )

         return comparison_df