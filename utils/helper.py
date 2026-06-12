import pandas as pd


def load_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)

    return pd.read_excel(file)


def get_revenue_column(df):

    if "Sub Total" in df.columns:
        return "Sub Total"

    if "Jumlah" in df.columns:
        return "Jumlah"

    if "Total" in df.columns:
        return "Total"

    return None


def get_staff_column(df):

    if "Pelayan" in df.columns:
        return "Pelayan"

    if "Kasir" in df.columns:
        return "Kasir"

    return None