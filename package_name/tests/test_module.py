import pytest
import pandas as pd
from module import dataplot


class TestTestDataCorrect:
    def test_testdata(self):
        df = get_test_data()
        assert (df.x.shape[0] - df.y.shape[0], 0)

    def test_dataplotdataframe(self):
        test_df = get_test_data()
        dp = dataplot(test_df)


class TestDataPlotInitializesCorrectly:
    def test_check(self):
        pass


def get_test_data():
    test_data = pd.DataFrame(
        data={
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "y": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "z": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        }
    )
    return test_data
