import pandas as pd


def generate_insights(df, revenue_col, staff_col=None):
    insights = []

    if df.empty:
        return ["Tidak ada data untuk dianalisis."]

    if "Item" in df.columns and "Qty" in df.columns:
        top_product = (
            df.groupby("Item", as_index=False)["Qty"]
            .sum()
            .sort_values("Qty", ascending=False)
            .iloc[0]
        )

        insights.append(
            f"Produk terlaris adalah {top_product['Item']} dengan total {top_product['Qty']:,.0f} item terjual."
        )

    if "Kategori" in df.columns:
        top_category = (
            df.groupby("Kategori", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        insights.append(
            f"Kategori dengan revenue tertinggi adalah {top_category['Kategori']} sebesar Rp {top_category[revenue_col]:,.0f}."
        )

    if "Metode Pembayaran" in df.columns:
        top_payment = (
            df.groupby("Metode Pembayaran", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        insights.append(
            f"Metode pembayaran paling dominan adalah {top_payment['Metode Pembayaran']} dengan revenue Rp {top_payment[revenue_col]:,.0f}."
        )

    if "Jam" in df.columns:
        top_hour = (
            df.groupby("Jam", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        insights.append(
            f"Jam dengan revenue tertinggi terjadi pada pukul {int(top_hour['Jam'])}:00 dengan revenue Rp {top_hour[revenue_col]:,.0f}."
        )

    if "Tanggal_Hari" in df.columns:
        top_day = (
            df.groupby("Tanggal_Hari", as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        insights.append(
            f"Hari dengan revenue tertinggi adalah {top_day['Tanggal_Hari']} dengan total revenue Rp {top_day[revenue_col]:,.0f}."
        )

    if staff_col and staff_col in df.columns:
        top_staff = (
            df.groupby(staff_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
            .iloc[0]
        )

        insights.append(
            f"{staff_col} dengan revenue tertinggi adalah {top_staff[staff_col]} sebesar Rp {top_staff[revenue_col]:,.0f}."
        )

    return insights