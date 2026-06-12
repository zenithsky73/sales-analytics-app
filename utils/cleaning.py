import pandas as pd

def clean_currency_column(series):
    return (
        series.astype(str)
        .str.replace("Rp", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

def clean_sales_data(df):
    df_clean = df.copy()
    df_clean = df_clean.dropna(how="all")

    fill_columns = [
        "Nomor",
        "Tanggal",
        "Tipe Penjualan",
        "Kasir",
        "Pelayan",
        "Metode Pembayaran",
        "Pelanggan",
        "Total"
    ]

    for col in fill_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].ffill()

    # =====================
    # CLEANING TANGGAL
    # =====================
    if "Tanggal" in df_clean.columns:
        df_clean["Tanggal"] = df_clean["Tanggal"].ffill()

        bulan_indonesia = {
            "Januari": "January",
            "Februari": "February",
            "Maret": "March",
            "April": "April",
            "Mei": "May",
            "Juni": "June",
            "Juli": "July",
            "Agustus": "August",
            "September": "September",
            "Oktober": "October",
            "November": "November",
            "Desember": "December"
        }

        df_clean["Tanggal"] = df_clean["Tanggal"].astype(str)

        for indo, eng in bulan_indonesia.items():
            df_clean["Tanggal"] = df_clean["Tanggal"].str.replace(
                indo,
                eng,
                regex=False
            )

        df_clean["Tanggal"] = pd.to_datetime(
            df_clean["Tanggal"],
            errors="coerce",
            dayfirst=True
        )

        df_clean["Tanggal_Hari"] = df_clean["Tanggal"].dt.date
        df_clean["Jam"] = df_clean["Tanggal"].dt.hour

    numeric_columns = [
        "Qty",
        "Harga Satuan",
        "Sub Total",
        "Jumlah",
        "Total"
    ]

    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = clean_currency_column(df_clean[col])
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce").fillna(0)

    if "Item" in df_clean.columns:
        df_clean = df_clean.dropna(subset=["Item"])
        df_clean["Item"] = df_clean["Item"].astype(str).str.strip()

    if "Kategori" in df_clean.columns:
        df_clean["Kategori"] = df_clean["Kategori"].astype(str).str.strip()

    if "Pelayan" in df_clean.columns:
        df_clean["Pelayan"] = (
            df_clean["Pelayan"]
            .astype(str)
            .str.replace(r'[^A-Za-z0-9\s]', '', regex=True)
            .str.strip()
        )

    if "Metode Pembayaran" in df_clean.columns:
        df_clean["Metode Pembayaran"] = (
            df_clean["Metode Pembayaran"]
            .astype(str)
            .str.strip()
        )

    df_clean = df_clean.drop_duplicates()

    return df_clean