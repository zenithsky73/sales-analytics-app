import streamlit as st
import pandas as pd
import plotly.express as px

from io import BytesIO
from utils.page_header import show_page_header
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def show_apriori_page():

    show_page_header(
        "🧠",
        "Market Basket Analysis",
        "Analisis pola pembelian menggunakan algoritma Apriori."
    )

    if st.session_state.clean_data is None:
        st.warning("Lakukan data cleaning terlebih dahulu.")
        return

    df = st.session_state.clean_data.copy()

    if "Nomor" not in df.columns or "Item" not in df.columns:
        st.error("Kolom Nomor dan Item wajib tersedia untuk analisis Apriori.")
        return

    st.info(
        "Analisis Apriori digunakan untuk menemukan produk yang sering dibeli bersamaan "
        "dan menghasilkan rekomendasi bundling produk."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        min_support = st.slider(
            "Minimum Support",
            min_value=0.01,
            max_value=0.50,
            value=0.02,
            step=0.01
        )

    with col2:
        min_confidence = st.slider(
            "Minimum Confidence",
            min_value=0.01,
            max_value=1.00,
            value=0.20,
            step=0.01
        )

    with col3:
        top_n = st.slider(
            "Top Rules",
            min_value=5,
            max_value=30,
            value=10,
            step=5
        )

    transactions = (
        df.groupby("Nomor")["Item"]
        .apply(lambda x: list(set(x.dropna())))
        .tolist()
    )

    total_transactions = len(transactions)
    total_items = df["Item"].nunique()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Transaksi", f"{total_transactions:,}")
    kpi2.metric("Total Produk Unik", f"{total_items:,}")
    kpi3.metric("Parameter Support", f"{min_support:.0%}")

    with st.expander("Lihat Preview Transaksi", expanded=False):
        preview_data = []

        for i, trx in enumerate(transactions[:10], start=1):
            preview_data.append({
                "No": i,
                "Jumlah Item": len(trx),
                "Daftar Item": ", ".join(trx)
            })

        st.dataframe(
            pd.DataFrame(preview_data),
            width="stretch",
            hide_index=True
        )

    if st.button("🚀 Jalankan Analisis Apriori"):

        if total_transactions == 0:
            st.error("Data transaksi kosong.")
            return

        te = TransactionEncoder()
        te_array = te.fit(transactions).transform(transactions)

        df_encoded = pd.DataFrame(
            te_array,
            columns=te.columns_
        )

        frequent_itemsets_raw = apriori(
            df_encoded,
            min_support=min_support,
            use_colnames=True
        )

        if frequent_itemsets_raw.empty:
            st.warning("Tidak ada frequent itemset ditemukan. Coba turunkan minimum support.")
            return

        rules_raw = association_rules(
            frequent_itemsets_raw,
            metric="confidence",
            min_threshold=min_confidence
        )

        if rules_raw.empty:
            st.warning("Tidak ada association rules ditemukan. Coba turunkan minimum confidence.")
            return

        st.toast(
            "🎯 Association Rules berhasil dibuat",
            icon="✅"
        )

        st.success(
            f"✅ Analisis selesai! Ditemukan {len(rules_raw)} association rules."
        )
        
        rules_raw = rules_raw.sort_values(
            ["lift", "confidence", "support"],
            ascending=False
        )

        rules = rules_raw.copy()

        rules["antecedents"] = rules["antecedents"].apply(
            lambda x: ", ".join(list(x))
        )

        rules["consequents"] = rules["consequents"].apply(
            lambda x: ", ".join(list(x))
        )

        rules = rules[
            [
                "antecedents",
                "consequents",
                "support",
                "confidence",
                "lift"
            ]
        ]

        rules_display = rules.copy()
        rules_display["support"] = rules_display["support"].apply(lambda x: f"{x:.2%}")
        rules_display["confidence"] = rules_display["confidence"].apply(lambda x: f"{x:.2%}")
        rules_display["lift"] = rules_display["lift"].apply(lambda x: f"{x:.2f}")

        st.subheader("📋 Association Rules")
        st.dataframe(
            rules_display.head(top_n),
            width="stretch",
            hide_index=True
        )

        st.subheader("🎯 Top Bundling Recommendation")

        top_bundling = rules.head(top_n).copy()

        for i, row in top_bundling.iterrows():
            st.success(
                f"Bundle: **{row['antecedents']} + {row['consequents']}** | "
                f"Confidence: **{row['confidence']:.2%}** | "
                f"Lift: **{row['lift']:.2f}**"
            )

        st.subheader("📊 Top Rules by Lift")

        fig_lift = px.bar(
            top_bundling,
            x="lift",
            y="antecedents",
            orientation="h",
            color="confidence",
            title="Top Association Rules Berdasarkan Lift",
            labels={
                "lift": "Lift",
                "antecedents": "Produk Awal",
                "confidence": "Confidence"
            }
        )

        st.plotly_chart(
            fig_lift,
            width="stretch"
        )

        st.subheader("📌 Insight Apriori")

        best_rule = rules.iloc[0]

        st.info(
            f"Rule terbaik menunjukkan bahwa pelanggan yang membeli "
            f"**{best_rule['antecedents']}** memiliki kecenderungan membeli "
            f"**{best_rule['consequents']}** dengan confidence "
            f"**{best_rule['confidence']:.2%}** dan lift **{best_rule['lift']:.2f}**."
        )

        st.warning(
            "Rekomendasi bisnis: gunakan pasangan produk dengan nilai lift tinggi "
            "sebagai paket bundling, promo kasir, atau rekomendasi upselling."
        )

        frequent_itemsets = frequent_itemsets_raw.copy()
        frequent_itemsets["itemsets"] = frequent_itemsets["itemsets"].apply(
            lambda x: ", ".join(list(x))
        )

        st.subheader("📦 Frequent Itemsets")
        st.dataframe(
            frequent_itemsets.sort_values("support", ascending=False),
            width="stretch",
            hide_index=True
        )

        csv_rules = rules.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Rules CSV",
            data=csv_rules,
            file_name="hasil_apriori_rules.csv",
            mime="text/csv"
        )

        excel_buffer = BytesIO()

        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            frequent_itemsets.to_excel(
                writer,
                index=False,
                sheet_name="Frequent Itemsets"
            )

            rules.to_excel(
                writer,
                index=False,
                sheet_name="Association Rules"
            )

        st.download_button(
            label="Download Hasil Apriori Excel",
            data=excel_buffer.getvalue(),
            file_name="hasil_apriori.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )