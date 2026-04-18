import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Medica Dashboard", page_icon="🩺", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_excel("Medica_Test_Rates.xlsx")
df.columns = ["S.No", "Test Name", "Rate (INR)"]

# ---------------- CATEGORY FUNCTION ----------------
def get_category(name):
    name = name.lower()
    if "urine" in name or "stool" in name:
        return "Urine / Stool"
    elif "vit" in name:
        return "Vitamin"
    elif "thyroid" in name or "t3" in name or "t4" in name or "tsh" in name:
        return "Thyroid"
    elif "blood" in name or "cbc" in name or "hb" in name or "esr" in name:
        return "Blood"
    else:
        return "General"

df["Category"] = df["Test Name"].apply(get_category)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {background:#f4f8ff;}
h1,h2,h3 {color:#0A4FA3;}
.stButton>button {
    border-radius:10px;
    height:45px;
}
div[data-testid="metric-container"]{
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🩺 Medica Dashboard")
st.caption("Smart Medical Test Search, Analytics & Bestseller Dashboard")

# ---------------- TOP METRICS ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Total Tests", len(df))
c2.metric("Lowest Price", f"₹{df['Rate (INR)'].min()}")
c3.metric("Highest Price", f"₹{df['Rate (INR)'].max()}")

st.divider()

# ---------------- FILTER + SEARCH ----------------
left, right = st.columns([1,2])

with left:
    category = st.selectbox("Select Category", ["All"] + sorted(df["Category"].unique().tolist()))

with right:
    search = st.selectbox("Search Test Name", ["Select Test"] + df["Test Name"].tolist())

filtered = df.copy()

if category != "All":
    filtered = filtered[filtered["Category"] == category]

if search != "Select Test":
    filtered = filtered[filtered["Test Name"] == search]

st.subheader("🔍 Search Results")
st.dataframe(filtered, use_container_width=True, height=250)

st.divider()

# ---------------- ADD TESTS + TOTAL ----------------
st.subheader("🧾 Add Tests & Calculate Total")

selected_tests = st.multiselect("Select Multiple Tests", df["Test Name"].tolist())

if selected_tests:
    bill_df = df[df["Test Name"].isin(selected_tests)][["Test Name", "Rate (INR)"]]
    total_amount = bill_df["Rate (INR)"].sum()

    st.write("### Selected Tests")
    st.dataframe(bill_df, use_container_width=True)
    st.success(f"💰 Total Amount: ₹{total_amount}")

st.divider()

# ---------------- ANALYTICS ----------------
st.subheader("📊 Analytics Dashboard")

chart_df = filtered.copy()
if len(chart_df) == 0:
    chart_df = df.copy()

col1, col2 = st.columns(2)

with col1:
    pie_data = chart_df["Category"].value_counts().reset_index()
    pie_data.columns = ["Category", "Count"]

    fig1 = px.pie(
        pie_data,
        values="Count",
        names="Category",
        title="Category Share",
        hole=0.45
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    top_data = chart_df.sort_values("Rate (INR)", ascending=False).head(10)

    fig2 = px.bar(
        top_data,
        x="Rate (INR)",
        y="Test Name",
        orientation="h",
        title="Top Priced Tests",
        text="Rate (INR)"
    )
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    chart_df,
    x="Rate (INR)",
    nbins=10,
    title="Price Distribution"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------------- BESTSELLER ----------------
st.subheader("🏆 Bestseller Tests")

bestseller = df.sort_values("Rate (INR)", ascending=False).head(5)[["Test Name", "Rate (INR)"]]
st.dataframe(bestseller, use_container_width=True)

st.divider()

# ---------------- POPULAR TESTS ----------------
st.subheader("⭐ Popular Tests")

p1, p2, p3, p4 = st.columns(4)

with p1:
    if st.button("CBC"):
        st.write(df[df["Test Name"].str.contains("CBC", case=False, na=False)])

with p2:
    if st.button("Sugar"):
        st.write(df[df["Test Name"].str.contains("Sugar", case=False, na=False)])

with p3:
    if st.button("TSH"):
        st.write(df[df["Test Name"].str.contains("TSH", case=False, na=False)])

with p4:
    if st.button("Lipid"):
        st.write(df[df["Test Name"].str.contains("Lipid", case=False, na=False)])

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2026 Medica Diagnostic Center | Dashboard with Analytics")