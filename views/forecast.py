import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.page_header import show_page_header
from sklearn.linear_model import LinearRegression
from utils.helper import get_revenue_column


def show_forecast_page():

    show_page_header(
        "🔮",
        "Forecast Penjualan",
        "Prediksi performa penjualan berdasarkan data historis."
    )

    if st.session_state.clean_data is None:
        st.warning("Lakukan data cleaning terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()
    revenue_col = get_revenue_column(df)

    if revenue_col is None:
        st.error("Kolom revenue tidak ditemukan.")
        return

    if "Tanggal_Hari" not in df.columns:
        st.error("Kolom Tanggal_Hari tidak ditemukan.")
        return

    daily_sales = (
        df.groupby("Tanggal_Hari", as_index=False)[revenue_col]
        .sum()
        .rename(columns={
            "Tanggal_Hari": "Tanggal",
            revenue_col: "Revenue"
        })
    )

    daily_sales["Tanggal"] = pd.to_datetime(daily_sales["Tanggal"])
    daily_sales = daily_sales.sort_values("Tanggal")

    if len(daily_sales) < 7:
        st.warning("Data minimal 7 hari diperlukan untuk forecast yang lebih stabil.")
        return

    st.info(
        "Forecast ini menggunakan kombinasi tren linear dan moving average "
        "untuk memperkirakan revenue beberapa hari ke depan."
    )

    forecast_days = st.slider(
        "Pilih jumlah hari forecast",
        min_value=7,
        max_value=30,
        value=14
    )

    daily_sales["Day_Index"] = range(len(daily_sales))

    X = daily_sales[["Day_Index"]]
    y = daily_sales["Revenue"]

    model = LinearRegression()
    model.fit(X, y)

    last_index = daily_sales["Day_Index"].max()

    future_index = list(
        range(last_index + 1, last_index + 1 + forecast_days)
    )

    future_dates = pd.date_range(
        start=daily_sales["Tanggal"].max() + pd.Timedelta(days=1),
        periods=forecast_days
    )

    trend_prediction = model.predict(
        pd.DataFrame({"Day_Index": future_index})
    )

    moving_average = (
        daily_sales["Revenue"]
        .rolling(window=7)
        .mean()
        .iloc[-1]
    )

    forecast_values = (trend_prediction * 0.6) + (moving_average * 0.4)

    forecast_values = [max(0, value) for value in forecast_values]

    historical_std = daily_sales["Revenue"].std()

    forecast_df = pd.DataFrame({
        "Tanggal": future_dates,
        "Forecast Revenue": forecast_values
    })

    forecast_df["Lower Estimate"] = (
        forecast_df["Forecast Revenue"] - historical_std
    ).clip(lower=0)

    forecast_df["Upper Estimate"] = (
        forecast_df["Forecast Revenue"] + historical_std
    )

    total_actual = daily_sales["Revenue"].sum()
    avg_actual = daily_sales["Revenue"].mean()
    total_forecast = forecast_df["Forecast Revenue"].sum()
    avg_forecast = forecast_df["Forecast Revenue"].mean()

    growth_estimate = (
        (avg_forecast - avg_actual) / avg_actual * 100
        if avg_actual > 0 else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rata-rata Revenue Harian",
        f"Rp {avg_actual:,.0f}"
    )

    col2.metric(
        f"Forecast {forecast_days} Hari",
        f"Rp {total_forecast:,.0f}"
    )

    col3.metric(
        "Rata-rata Forecast",
        f"Rp {avg_forecast:,.0f}"
    )

    col4.metric(
        "Estimasi Growth",
        f"{growth_estimate:.2f}%"
    )

    st.subheader("Grafik Actual vs Forecast")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=daily_sales["Tanggal"],
            y=daily_sales["Revenue"],
            mode="lines+markers",
            name="Actual Revenue"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast_df["Tanggal"],
            y=forecast_df["Forecast Revenue"],
            mode="lines+markers",
            name="Forecast Revenue"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=list(forecast_df["Tanggal"]) + list(forecast_df["Tanggal"])[::-1],
            y=list(forecast_df["Upper Estimate"]) + list(forecast_df["Lower Estimate"])[::-1],
            fill="toself",
            name="Forecast Range",
            opacity=0.25,
            line=dict(width=0)
        )
    )

    fig.update_layout(
        title="Forecast Revenue Penjualan",
        xaxis_title="Tanggal",
        yaxis_title="Revenue",
        hovermode="x unified"
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("Tabel Forecast")

    forecast_display = forecast_df.copy()
    forecast_display["Tanggal"] = forecast_display["Tanggal"].dt.date

    st.dataframe(
        forecast_display,
        width="stretch",
        hide_index=True
    )

    st.subheader("Insight Forecast")

    best_day = forecast_df.sort_values(
        "Forecast Revenue",
        ascending=False
    ).iloc[0]

    lowest_day = forecast_df.sort_values(
        "Forecast Revenue",
        ascending=True
    ).iloc[0]

    if growth_estimate > 0:
        st.success(
            f"Forecast menunjukkan potensi kenaikan rata-rata revenue sebesar "
            f"**{growth_estimate:.2f}%** dibanding rata-rata historis."
        )
    elif growth_estimate < 0:
        st.warning(
            f"Forecast menunjukkan potensi penurunan rata-rata revenue sebesar "
            f"**{abs(growth_estimate):.2f}%** dibanding rata-rata historis."
        )
    else:
        st.info(
            "Forecast menunjukkan revenue cenderung stabil dibanding rata-rata historis."
        )

    st.info(
        f"Estimasi revenue tertinggi diprediksi terjadi pada "
        f"**{best_day['Tanggal'].date()}** sebesar "
        f"**Rp {best_day['Forecast Revenue']:,.0f}**."
    )

    st.warning(
        f"Estimasi revenue terendah diprediksi terjadi pada "
        f"**{lowest_day['Tanggal'].date()}** sebesar "
        f"**Rp {lowest_day['Forecast Revenue']:,.0f}**."
    )

    csv = forecast_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Hasil Forecast CSV",
        data=csv,
        file_name="forecast_penjualan.csv",
        mime="text/csv"
    )