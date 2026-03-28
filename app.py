
import streamlit as st
from modules import student_crm, leads, finance, analytics

st.set_page_config(page_title="Dev Nautics Dashboard", layout="wide")

st.title("🚀 Dev Nautics Command Center")

menu = ["Executive Dashboard", "Students", "Leads", "Finance", "Analytics"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Executive Dashboard":
    st.header("Executive Overview")
    analytics.show_overview()

elif choice == "Students":
    student_crm.show()

elif choice == "Leads":
    leads.show()

elif choice == "Finance":
    finance.show()

elif choice == "Analytics":
    analytics.show_detailed()
