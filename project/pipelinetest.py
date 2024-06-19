import os
import sqlite3
import pytest


def test_online_assert_pipeline_output_exists():
    assert os.path.isfile("../data/data.sqlite")


def test_online_pipeline_assert_output_table_carbonprice_exists():
    conn = sqlite3.connect("../data/data.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='carbonPrice';")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Table 'carbonPrice' does not exist."


def test_online_pipeline_assert_output_table_emissions_exists():
    conn = sqlite3.connect("../data/data.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emissions';")
    result = cursor.fetchone()

    conn.close()
    assert result is not None, "Table 'emissions' does not exist."
