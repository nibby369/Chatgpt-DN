import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Dev Nautics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data path: works locally AND on Streamlit Cloud ───────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# ── Color palette ─────────────────────────────────────────────────────────────
TEAL    = "#1D9E75"
DARK    = "#0d3d28"
COLORS  = ["#1D9E75","#0F6E56","#5DCAA5","#9FE1CB","#F4A623",
           "#E85D24","#185FA5","#534AB7","#D4537E","#E1F5EE"]

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Sora:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0a2e1f 0%, #0d3d28 60%, #0f4a30 100%);
    border-right: 1px solid #1a5c38;
}
section[data-testid="stSidebar"] * { color: #d4f0e0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #7ec8a0 !important;
    font-size: 12px !important;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
div[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e0ede6;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 4px rgba(13,61,40,0.06);
}
div[data-testid="metric-container"] label {
    color: #5a8a70 !important;
    font-size: 12px !important;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #0d3d28 !important;
    font-size: 26px !important;
    font-weight: 700;
}
h1 { font-family: 'Sora', sans-serif !important; color: #0d3d28 !important; font-weight: 700 !important; }
h2 { font-family: 'Sora', sans-serif !important; color: #0d3d28 !important; font-weight: 600 !important; }
h3 { color: #1a5c38 !important; font-weight: 600 !important; }
hr { border-color: #d4ead9 !important; }
div[data-testid="stDataFrame"] { border: 1px solid #e0ede6; border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Helper: load CSV safely ───────────────────────────────────────────────────
@st.cache_data
def load(filename):
    path = DATA_DIR / filename
    if not path.exists():
        st.error(f"Data file not found: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def page_overview():
    st.markdown("## 🏠 Executive Overview")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Dev Nautics · Academic Year 2024-25 · Surat</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    students_df = load("students.csv")
    revenue_df  = load("revenue.csv")
    leads_df    = load("leads.csv")
    feedback_df = load("feedback.csv")

    if students_df.empty or revenue_df.empty:
        st.warning("Some data files are missing. Please check the /data folder.")
        return

    active      = students_df[students_df["status"] == "Active"]
    total_rev   = revenue_df["total_collected"].sum()
    total_due   = revenue_df["total_due"].sum()
    enrolled    = len(leads_df[leads_df["status"] == "Enrolled"]) if not leads_df.empty else 0
    avg_rating  = feedback_df["rating"].mean() if not feedback_df.empty else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Active Students", f"{len(active)}", "+8 this month")
    c2.metric("Total Revenue (YTD)",   f"₹{total_rev:,.0f}", "+22% vs last year")
    c3.metric("Fees Outstanding",      f"₹{total_due:,.0f}", "-₹500 MoM")
    c4.metric("Leads Converted",       f"{enrolled}", "+3 this month")
    c5.metric("Avg Parent Rating",     f"{avg_rating:.1f} / 5.0", "⭐ 15 reviews")
    st.markdown("---")

    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("#### 📈 Monthly Revenue Trend")
        fig = px.area(revenue_df, x="month", y="total_collected",
                      color_discrete_sequence=[TEAL], template="plotly_white")
        fig.update_traces(fill="tozeroy", line_width=2.5, fillcolor="rgba(29,158,117,0.15)")
        fig.update_layout(margin=dict(t=20,b=20,l=10,r=10), height=260,
                          xaxis_title="", yaxis_title="Revenue (₹)",
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis=dict(tickfont=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 🧭 Business Health Score")
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number", value=82,
            title={"text": "Health Score", "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": TEAL},
                "steps": [
                    {"range": [0, 50],   "color": "#fde8e8"},
                    {"range": [50, 75],  "color": "#fef3d7"},
                    {"range": [75, 100], "color": "#d4f0e0"},
                ],
            },
            number={"suffix": "/100", "font": {"size": 28, "color": DARK}},
        ))
        fig2.update_layout(height=260, margin=dict(t=30,b=10,l=20,r=20), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("#### 👥 Students by Service")
        svc = students_df.groupby("service").size().reset_index(name="count")
        fig3 = px.pie(svc, values="count", names="service",
                      color_discrete_sequence=COLORS, hole=0.45, template="plotly_white")
        fig3.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           legend=dict(font=dict(size=10)), paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 🏫 Enrollment by Class")
        cls = students_df.groupby("class").size().reset_index(name="count")
        class_order = [f"Class {i}" for i in range(1, 11)]
        cls["class"] = pd.Categorical(cls["class"], categories=class_order, ordered=True)
        cls = cls.sort_values("class")
        fig4 = px.bar(cls, x="class", y="count", color_discrete_sequence=[TEAL],
                      template="plotly_white")
        fig4.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="", yaxis_title="Students",
                           xaxis=dict(tickfont=dict(size=10)),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    with col_c:
        st.markdown("#### 📣 Lead Pipeline")
        pipeline = leads_df["status"].value_counts().reset_index()
        pipeline.columns = ["Status", "Count"]
        order = ["New", "Follow-up", "Enrolled", "Lost"]
        pipeline["Status"] = pd.Categorical(pipeline["Status"], categories=order, ordered=True)
        pipeline = pipeline.sort_values("Status")
        fig5 = px.funnel(pipeline, x="Count", y="Status",
                         color_discrete_sequence=[TEAL], template="plotly_white")
        fig5.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📅 Quick Stats Snapshot")
    male = len(students_df[students_df["gender"] == "Male"])
    female = len(students_df[students_df["gender"] == "Female"])
    avg_att = students_df["attendance_pct"].mean()
    avg_score = students_df["score_avg"].mean()
    fee_rate = total_rev / (total_rev + total_due) * 100 if (total_rev + total_due) > 0 else 0
    conv_rate = enrolled / len(leads_df) * 100 if len(leads_df) > 0 else 0

    s1,s2,s3,s4,s5,s6 = st.columns(6)
    s1.metric("Male Students",        male)
    s2.metric("Female Students",      female)
    s3.metric("Avg Attendance",       f"{avg_att:.1f}%")
    s4.metric("Avg Score",            f"{avg_score:.1f}%")
    s5.metric("Fee Collection Rate",  f"{fee_rate:.1f}%")
    s6.metric("Lead Conversion Rate", f"{conv_rate:.1f}%")


# ─────────────────────────────────────────────────────────────────────────────
def page_students():
    st.markdown("## 👦 Student Management")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Full roster · attendance · enrollment analysis</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df = load("students.csv")
    if df.empty:
        st.warning("No student data found."); return

    sel_class   = st.session_state.get("selected_class", [])
    sel_service = st.session_state.get("selected_service", [])
    filtered = df.copy()
    if sel_class:
        filtered = filtered[filtered["class"].isin(sel_class)]
    if sel_service:
        filtered = filtered[filtered["service"].isin(sel_service)]

    active = filtered[filtered["status"] == "Active"]
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Students",    len(filtered))
    c2.metric("Active",            len(active))
    c3.metric("Inactive",          len(filtered) - len(active))
    c4.metric("Avg Attendance",    f"{filtered['attendance_pct'].mean():.1f}%")
    c5.metric("Avg Score",         f"{filtered['score_avg'].mean():.1f}%")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🚻 Gender Distribution")
        gc = filtered.groupby("gender").size().reset_index(name="count")
        fig = px.pie(gc, values="count", names="gender", hole=0.5,
                     color_discrete_sequence=[TEAL, "#F4A623"], template="plotly_white")
        fig.update_layout(height=240, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📚 Students per Service")
        svc = filtered.groupby("service").size().reset_index(name="count").sort_values("count")
        fig2 = px.bar(svc, x="count", y="service", orientation="h",
                      color_discrete_sequence=[TEAL], template="plotly_white")
        fig2.update_layout(height=240, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="Students", yaxis_title="",
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 🏫 Class-wise Enrollment")
        cls = filtered.groupby("class").size().reset_index(name="count")
        class_order = [f"Class {i}" for i in range(1, 11)]
        cls["class"] = pd.Categorical(cls["class"], categories=class_order, ordered=True)
        cls = cls.sort_values("class")
        fig3 = px.bar(cls, x="class", y="count",
                      color="count", color_continuous_scale=["#9FE1CB", TEAL, "#0d3d28"],
                      template="plotly_white")
        fig3.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="", yaxis_title="Students",
                           coloraxis_showscale=False,
                           xaxis=dict(tickfont=dict(size=10)),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 📅 Attendance Heatmap (Class × Batch)")
        pivot = filtered.groupby(["class","batch"])["attendance_pct"].mean().reset_index()
        pivot_wide = pivot.pivot(index="class", columns="batch", values="attendance_pct")
        fig4 = go.Figure(go.Heatmap(
            z=pivot_wide.values,
            x=pivot_wide.columns.tolist(),
            y=pivot_wide.index.tolist(),
            colorscale=[[0,"#fde8e8"],[0.5,"#9FE1CB"],[1,"#0d3d28"]],
            text=[[f"{v:.1f}%" for v in row] for row in pivot_wide.values],
            texttemplate="%{text}", showscale=True,
        ))
        fig4.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🔍 Score vs Attendance")
    fig5 = px.scatter(filtered, x="attendance_pct", y="score_avg", color="service",
                      hover_data=["name","class"], color_discrete_sequence=COLORS,
                      template="plotly_white",
                      labels={"attendance_pct":"Attendance %","score_avg":"Avg Score %"})
    fig5.update_layout(height=280, margin=dict(t=10,b=10,l=0,r=0),
                       paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Student Roster")
    search = st.text_input("🔍 Search by name, class or service", "")
    status_f = st.selectbox("Filter by Status", ["All","Active","Inactive"])
    display = filtered.copy()
    if search:
        mask = (display["name"].str.contains(search, case=False, na=False) |
                display["class"].str.contains(search, case=False, na=False) |
                display["service"].str.contains(search, case=False, na=False))
        display = display[mask]
    if status_f != "All":
        display = display[display["status"] == status_f]
    st.dataframe(
        display[["name","class","gender","service","batch","status",
                 "attendance_pct","score_avg","fees_paid","fees_due"]]
        .rename(columns={"attendance_pct":"Attendance %","score_avg":"Score %",
                         "fees_paid":"Fees Paid ₹","fees_due":"Fees Due ₹"}),
        use_container_width=True, height=400
    )
    st.caption(f"Showing {len(display)} of {len(filtered)} students")


# ─────────────────────────────────────────────────────────────────────────────
def page_services():
    st.markdown("## 📋 Services Dashboard")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>All 8 services offered by Dev Nautics</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df  = load("students.csv")
    rev = load("revenue.csv")
    if df.empty or rev.empty:
        st.warning("Data files missing."); return

    SERVICES = {
        "Tuition (CBSE/GSEB)":     {"emoji":"📚","color":"#1D9E75","bg":"#E1F5EE","classes":"Jr.Kg – Class 10","timing":"Morning & Evening"},
        "Olympiad Preparation":     {"emoji":"🏆","color":"#F4A623","bg":"#FAEEDA","classes":"Class 3 – Class 10","timing":"Weekends"},
        "Worksheet Practice":       {"emoji":"📝","color":"#185FA5","bg":"#E6F1FB","classes":"Class 1 – Class 10","timing":"Self-paced"},
        "Handwriting Workshop":     {"emoji":"✍️","color":"#D4537E","bg":"#FBEAF0","classes":"All classes","timing":"Weekend workshops"},
        "Online Math Program":      {"emoji":"🌐","color":"#534AB7","bg":"#EEEDFE","classes":"Class 1 – Class 6","timing":"Flexible online"},
        "Math & English Lab":       {"emoji":"🔬","color":"#0F6E56","bg":"#E1F5EE","classes":"Class 1 – Class 8","timing":"Weekdays"},
        "Robotics & ML":            {"emoji":"🤖","color":"#E85D24","bg":"#FAECE7","classes":"Class 7 – Class 10","timing":"Weekends"},
        "Skill Enhancement":        {"emoji":"💡","color":"#5DCAA5","bg":"#E1F5EE","classes":"Class 4 – Class 9","timing":"Monthly"},
    }

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Services",   "8")
    c2.metric("Most Popular",     "Tuition")
    c3.metric("Top Revenue",      "Tuition")
    c4.metric("Fastest Growing",  "Olympiad  +25%")
    st.markdown("---")

    st.markdown("#### 🎯 All Services at a Glance")
    cols = st.columns(4)
    for i, (name, info) in enumerate(SERVICES.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:{info['bg']};border-radius:12px;padding:14px 12px;
                        border-left:4px solid {info['color']};margin-bottom:12px;min-height:160px;">
                <div style="font-size:24px;margin-bottom:4px">{info['emoji']}</div>
                <div style="font-size:12px;font-weight:700;color:{info['color']};margin-bottom:4px;line-height:1.3">{name}</div>
                <div style="font-size:10px;color:#555;margin-bottom:4px">📚 {info['classes']}</div>
                <div style="font-size:10px;color:#555">🕐 {info['timing']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 👥 Enrollment per Service")
        svc_enroll = df.groupby("service").size().reset_index(name="students")
        fig = px.bar(svc_enroll.sort_values("students"),
                     x="students", y="service", orientation="h",
                     color="students",
                     color_continuous_scale=["#9FE1CB", TEAL, "#0d3d28"],
                     template="plotly_white")
        fig.update_layout(height=300, margin=dict(t=10,b=10,l=0,r=0),
                          xaxis_title="Students", yaxis_title="",
                          coloraxis_showscale=False,
                          paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 💰 Revenue by Service (Last 3 Months)")
        rev_last = rev.tail(3)
        svc_rev = {
            "Tuition":     rev_last["tuition"].sum(),
            "Olympiad":    rev_last["olympiad"].sum(),
            "Handwriting": rev_last["handwriting"].sum(),
            "Worksheet":   rev_last["worksheet"].sum(),
            "Online Math": rev_last["online_math"].sum(),
            "Books":       rev_last["books"].sum(),
            "Kits":        rev_last["kits"].sum(),
        }
        rev_df2 = pd.DataFrame({"Service": list(svc_rev.keys()), "Revenue": list(svc_rev.values())})
        fig2 = px.pie(rev_df2, values="Revenue", names="Service",
                      color_discrete_sequence=COLORS, hole=0.4, template="plotly_white")
        fig2.update_layout(height=300, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Service Revenue — Month by Month")
    rev_melt = rev.melt(id_vars=["month"],
                        value_vars=["tuition","olympiad","handwriting","worksheet","online_math","books"],
                        var_name="Service", value_name="Revenue")
    fig3 = px.bar(rev_melt, x="month", y="Revenue", color="Service",
                  barmode="group", color_discrete_sequence=COLORS, template="plotly_white")
    fig3.update_layout(height=280, margin=dict(t=10,b=10,l=0,r=0),
                       paper_bgcolor="white", plot_bgcolor="white",
                       xaxis_title="", yaxis_title="Revenue (₹)",
                       xaxis=dict(tickfont=dict(size=9)))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.markdown("#### ⚡ Service Performance Summary")
    summary = pd.DataFrame({
        "Service":     ["Tuition","Olympiad","Handwriting","Worksheet","Online Math","Robotics","Math Lab","Skill Enhancement"],
        "Students":    [22, 8, 5, 6, 4, 2, 0, 0],
        "Avg Rating":  [4.4, 4.8, 5.0, 3.9, 5.0, 4.5, 4.0, 4.2],
        "Revenue ₹":   [78000, 42000, 18000, 14000, 28000, 12000, 6000, 4000],
        "Growth":      ["+12%", "+25%", "+18%", "+8%", "+22%", "+40%", "+10%", "+15%"],
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
def page_products():
    st.markdown("## 📦 Products & Inventory")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Books · worksheets · kits · activity books · PAN India shipping</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Product Categories", "6")
    c2.metric("Book Titles",        "16")
    c3.metric("Free Worksheets",    "100+ PDFs")
    c4.metric("Paid Worksheet Sets","10 class sets")
    c5.metric("PAN India Shipping", "✅ Active")
    st.markdown("---")

    PRODUCTS = {
        "Books":              {"emoji":"📗","color":"#1D9E75","bg":"#E1F5EE","desc":"Self-published books for all levels. Jr.Kg to Class 10."},
        "Free Worksheets":    {"emoji":"📄","color":"#185FA5","bg":"#E6F1FB","desc":"Downloadable free practice worksheets. Class 1–10."},
        "Paid Worksheets":    {"emoji":"📑","color":"#534AB7","bg":"#EEEDFE","desc":"Premium result-oriented worksheet sets. Class 1–10."},
        "Educational Kits":   {"emoji":"🧰","color":"#F4A623","bg":"#FAEEDA","desc":"Math Express hands-on kits. Class 1 & 2."},
        "Activity Books":     {"emoji":"🎨","color":"#D4537E","bg":"#FBEAF0","desc":"Creative activity books for all classes."},
        "Learn-o-tronics":    {"emoji":"🤖","color":"#E85D24","bg":"#FAECE7","desc":"Interactive tech-based learning. Class 1–6."},
    }

    st.markdown("#### 🗂️ Product Catalog")
    cols = st.columns(3)
    for i, (name, info) in enumerate(PRODUCTS.items()):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:{info['bg']};border-radius:12px;padding:16px 14px;
                        border-left:4px solid {info['color']};margin-bottom:12px;">
                <div style="font-size:26px;margin-bottom:6px">{info['emoji']}</div>
                <div style="font-size:13px;font-weight:700;color:{info['color']};margin-bottom:4px">{name}</div>
                <div style="font-size:11px;color:#555">{info['desc']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 📊 Units Sold by Category")
        sales = pd.DataFrame({
            "Category": ["Books","Paid Worksheets","Kits","Activity Books","Learn-o-tronics"],
            "Units":    [320, 510, 85, 145, 62],
        })
        fig = px.bar(sales, x="Category", y="Units",
                     color_discrete_sequence=[TEAL], template="plotly_white", text="Units")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=280, margin=dict(t=10,b=30,l=0,r=0),
                          paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 💰 Revenue by Product Type")
        rev_prod = pd.DataFrame({
            "Type":    ["Books","Paid Worksheets","Kits","Activity Books","Learn-o-tronics"],
            "Revenue": [96000, 51000, 42500, 21750, 18600],
        })
        fig2 = px.pie(rev_prod, values="Revenue", names="Type",
                      color_discrete_sequence=COLORS, hole=0.4, template="plotly_white")
        fig2.update_layout(height=280, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📥 Free Worksheet Downloads by Class")
    dl = pd.DataFrame({
        "Class":     [f"Class {i}" for i in range(1, 11)],
        "Downloads": [1450, 1320, 1180, 980, 1100, 890, 760, 640, 580, 520],
    })
    fig3 = px.bar(dl, x="Class", y="Downloads",
                  color="Downloads", color_continuous_scale=["#9FE1CB", TEAL, "#0d3d28"],
                  template="plotly_white", text="Downloads")
    fig3.update_traces(textposition="outside")
    fig3.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                       coloraxis_showscale=False,
                       paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🚚 PAN India Orders by State")
    state_data = pd.DataFrame({
        "State":  ["Gujarat","Maharashtra","Rajasthan","Madhya Pradesh","Delhi",
                   "Karnataka","Tamil Nadu","Uttar Pradesh","West Bengal","Telangana"],
        "Orders": [420, 185, 98, 76, 65, 54, 48, 43, 38, 32],
    })
    fig4 = px.bar(state_data.sort_values("Orders"),
                  x="Orders", y="State", orientation="h",
                  color="Orders", color_continuous_scale=["#9FE1CB", TEAL, "#0d3d28"],
                  template="plotly_white")
    fig4.update_layout(height=320, margin=dict(t=10,b=10,l=0,r=0),
                       xaxis_title="Orders Shipped", yaxis_title="",
                       coloraxis_showscale=False,
                       paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏅 Bestsellers")
    bestsellers = pd.DataFrame({
        "Product":    ["Math Express Kit Gr.1","Worksheet Set Cl.10","Activity Book Cl.3",
                       "Book Cl.8 Math","Worksheet Set Cl.9","Learn-o-tronics Cl.5"],
        "Category":   ["Kit","Worksheet","Activity","Book","Worksheet","Learn-o-tronics"],
        "Units Sold": [85, 78, 72, 65, 61, 62],
        "Price ₹":    [499, 299, 149, 199, 299, 349],
        "Revenue ₹":  [42415, 23322, 10728, 12935, 18239, 21638],
    })
    st.dataframe(bestsellers, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
def page_finance():
    st.markdown("## 💰 Revenue & Finance")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Fee collection · monthly trends · service-wise breakdown</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    rev      = load("revenue.csv")
    students = load("students.csv")
    if rev.empty:
        st.warning("Revenue data missing."); return

    total_rev  = rev["total_collected"].sum()
    total_due  = rev["total_due"].sum()
    best_month = rev.loc[rev["total_collected"].idxmax(), "month"]
    best_rev   = rev["total_collected"].max()
    coll_rate  = total_rev / (total_rev + total_due) * 100 if (total_rev + total_due) > 0 else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Revenue (YTD)",    f"₹{total_rev:,.0f}", "+22% vs last year")
    c2.metric("Outstanding Fees",       f"₹{total_due:,.0f}", "-₹500 this month")
    c3.metric("Collection Rate",        f"{coll_rate:.1f}%")
    c4.metric("Best Month",             best_month, f"₹{best_rev:,.0f}")
    c5.metric("Avg Monthly Revenue",    f"₹{rev['total_collected'].mean():,.0f}")
    st.markdown("---")

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown("#### 📈 Monthly Revenue — All Streams")
        rev_melt = rev.melt(id_vars=["month"],
                            value_vars=["tuition","olympiad","handwriting","worksheet","online_math","books","kits"],
                            var_name="Stream", value_name="Revenue")
        fig = px.area(rev_melt, x="month", y="Revenue", color="Stream",
                      color_discrete_sequence=COLORS, template="plotly_white")
        fig.update_layout(height=300, margin=dict(t=10,b=10,l=0,r=0),
                          xaxis_title="", yaxis_title="Revenue (₹)",
                          legend=dict(font=dict(size=10)),
                          paper_bgcolor="white", plot_bgcolor="white",
                          xaxis=dict(tickfont=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 🏦 Collected vs Outstanding")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Collected",   x=rev["month"], y=rev["total_collected"], marker_color=TEAL))
        fig2.add_trace(go.Bar(name="Outstanding", x=rev["month"], y=rev["total_due"],        marker_color="#E85D24"))
        fig2.update_layout(barmode="stack", height=300, margin=dict(t=10,b=10,l=0,r=0),
                           legend=dict(font=dict(size=10)),
                           xaxis=dict(tickfont=dict(size=8)),
                           paper_bgcolor="white", plot_bgcolor="white",
                           template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📊 Revenue Waterfall (Latest Month)")
        latest = rev.iloc[-1]
        labels = ["Tuition","Olympiad","Handwriting","Worksheet","Online Math","Books","Kits"]
        vals   = [latest["tuition"], latest["olympiad"], latest["handwriting"],
                  latest["worksheet"], latest["online_math"], latest["books"], latest["kits"]]
        fig3 = go.Figure(go.Waterfall(
            orientation="v", x=labels, y=vals,
            connector={"line":{"color":"#ccc"}},
            increasing={"marker":{"color":TEAL}},
            totals={"marker":{"color":DARK}},
            texttemplate="₹%{y:,.0f}", textposition="outside",
        ))
        fig3.update_layout(height=300, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis=dict(tickfont=dict(size=10)),
                           paper_bgcolor="white", plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 💳 Fee Payment Status")
        if not students.empty:
            students = students.copy()
            students["fee_status"] = students.apply(
                lambda r: "Fully Paid" if r["fees_due"] == 0
                else ("Partial" if r["fees_paid"] > 0 else "Unpaid"), axis=1
            )
            fee_status = students["fee_status"].value_counts().reset_index()
            fee_status.columns = ["Status","Count"]
            fig4 = px.pie(fee_status, values="Count", names="Status", hole=0.45,
                          color_discrete_sequence=[TEAL, "#F4A623", "#E85D24"],
                          template="plotly_white")
            fig4.update_layout(height=300, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📅 Month-wise Revenue Table")
    disp = rev[["month","tuition","olympiad","handwriting","worksheet",
                "online_math","books","kits","total_collected","total_due"]].copy()
    disp.columns = ["Month","Tuition","Olympiad","Handwriting","Worksheet",
                    "Online Math","Books","Kits","Total Collected ₹","Outstanding ₹"]
    st.dataframe(disp, use_container_width=True, hide_index=True)

    if not students.empty:
        st.markdown("---")
        st.markdown("#### 🏅 Top 10 Fee Payers")
        top = students.nlargest(10, "fees_paid")[["name","class","service","fees_paid","fees_due","status"]]
        top.columns = ["Student","Class","Service","Fees Paid ₹","Fees Due ₹","Status"]
        st.dataframe(top, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
def page_leads():
    st.markdown("## 📣 Leads & Enquiries")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Enquiry pipeline · conversion · source analysis</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df = load("leads.csv")
    if df.empty:
        st.warning("Leads data missing."); return

    total     = len(df)
    enrolled  = len(df[df["status"] == "Enrolled"])
    follow_up = len(df[df["status"] == "Follow-up"])
    new_leads = len(df[df["status"] == "New"])
    lost      = len(df[df["status"] == "Lost"])
    conv_rate = enrolled / total * 100 if total > 0 else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Enquiries",  total)
    c2.metric("Enrolled",         enrolled)
    c3.metric("Follow-up",        follow_up)
    c4.metric("Lost",             lost)
    c5.metric("Conversion Rate",  f"{conv_rate:.1f}%")
    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 🔽 Enrollment Funnel")
        funnel_df = pd.DataFrame({
            "Stage": ["Enquiry Received","Follow-up Done","Enrolled"],
            "Count": [total, follow_up + enrolled, enrolled],
        })
        fig = px.funnel(funnel_df, x="Count", y="Stage",
                        color_discrete_sequence=[TEAL], template="plotly_white")
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 📡 Lead Source Breakdown")
        src = df.groupby("source").size().reset_index(name="count")
        fig2 = px.pie(src, values="count", names="source", hole=0.4,
                      color_discrete_sequence=COLORS, template="plotly_white")
        fig2.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🎯 Service Interest")
        svc = df.groupby("service_interest").size().reset_index(name="count").sort_values("count")
        fig3 = px.bar(svc, x="count", y="service_interest", orientation="h",
                      color_discrete_sequence=[TEAL], template="plotly_white")
        fig3.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="Leads", yaxis_title="",
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 📊 Conversion Rate by Source")
        conv = df.groupby("source").apply(
            lambda x: (x["converted"] == "Yes").sum() / len(x) * 100
        ).reset_index(name="conv_rate")
        fig4 = px.bar(conv.sort_values("conv_rate"),
                      x="conv_rate", y="source", orientation="h",
                      color="conv_rate",
                      color_continuous_scale=["#fde8e8","#F4A623",TEAL],
                      template="plotly_white")
        fig4.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="Conversion %", yaxis_title="",
                           coloraxis_showscale=False,
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 All Leads")
    status_f = st.selectbox("Filter by Status", ["All","New","Follow-up","Enrolled","Lost"])
    display = df.copy() if status_f == "All" else df[df["status"] == status_f]
    st.dataframe(
        display[["name","phone","source","service_interest","enquiry_date","status","follow_up_date","converted"]]
        .rename(columns={"service_interest":"Interested In","enquiry_date":"Enquiry Date",
                         "follow_up_date":"Follow-up Date","converted":"Converted?"}),
        use_container_width=True, height=350
    )
    st.caption(f"Showing {len(display)} of {total} leads")


# ─────────────────────────────────────────────────────────────────────────────
def page_feedback():
    st.markdown("## ⭐ Testimonials & Feedback")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Ratings · NPS · parent reviews · sentiment</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df = load("feedback.csv")
    if df.empty:
        st.warning("Feedback data missing."); return

    avg_r    = df["rating"].mean()
    positive = len(df[df["sentiment"] == "Positive"])
    neutral  = len(df[df["sentiment"] == "Neutral"])
    negative = len(df[df["sentiment"] == "Negative"])
    nps      = int((positive - negative) / len(df) * 100) if len(df) > 0 else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Avg Rating",    f"{avg_r:.1f} / 5.0")
    c2.metric("Total Reviews", len(df))
    c3.metric("😊 Positive",  positive)
    c4.metric("😐 Neutral",   neutral)
    c5.metric("😞 Negative",  negative)
    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 📊 Rating Distribution")
        rc = df["rating"].value_counts().sort_index().reset_index()
        rc.columns = ["Rating","Count"]
        fig = px.bar(rc, x="Rating", y="Count",
                     color="Rating", color_continuous_scale=["#E85D24","#F4A623",TEAL],
                     template="plotly_white", text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=240, margin=dict(t=10,b=10,l=0,r=0),
                          xaxis_title="Stars", yaxis_title="Reviews",
                          coloraxis_showscale=False,
                          paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 🎯 NPS Score")
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number", value=nps,
            title={"text": "Net Promoter Score", "font":{"size":13}},
            gauge={
                "axis":{"range":[-100,100]},
                "bar":{"color":TEAL},
                "steps":[
                    {"range":[-100,0],  "color":"#fde8e8"},
                    {"range":[0,50],    "color":"#fef3d7"},
                    {"range":[50,100],  "color":"#d4f0e0"},
                ],
            },
            number={"suffix":" pts","font":{"size":26,"color":DARK}},
        ))
        fig2.update_layout(height=240, margin=dict(t=20,b=0,l=10,r=10), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 😊 Sentiment Breakdown")
        sent = df["sentiment"].value_counts().reset_index()
        sent.columns = ["Sentiment","Count"]
        fig3 = px.pie(sent, values="Count", names="Sentiment", hole=0.5,
                      color="Sentiment",
                      color_discrete_map={"Positive":TEAL,"Neutral":"#F4A623","Negative":"#E85D24"},
                      template="plotly_white")
        fig3.update_layout(height=220, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 🏷️ Avg Rating by Service")
        svc_r = df.groupby("service")["rating"].mean().reset_index()
        svc_r.columns = ["Service","Avg Rating"]
        fig4 = px.bar(svc_r.sort_values("Avg Rating"),
                      x="Avg Rating", y="Service", orientation="h",
                      color="Avg Rating",
                      color_continuous_scale=["#fde8e8","#F4A623",TEAL],
                      template="plotly_white", range_x=[0,5])
        fig4.update_layout(height=220, margin=dict(t=10,b=10,l=0,r=0),
                           coloraxis_showscale=False,
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 💬 Featured Testimonials")
    featured = [
        {"name":"Dipti Bhatnagar","role":"Housewife","service":"Tuition",
         "comment":"Enrolling my child in Dev Nautics has been a game-changer. The personalized attention and engaging teaching methods have not only improved his grades but also his confidence. Highly recommended!"},
        {"name":"Payal Shah","role":"Fashion Designer","service":"Handwriting Workshop",
         "comment":"The systematic approach and individualized feedback have significantly enhanced my child's handwriting skills. The improvement is visible and impressive!"},
        {"name":"Purvee","role":"CEO – OOi","service":"Olympiad Preparation",
         "comment":"The dedicated tutors and rigorous practice sessions not only prepared my son for the Olympiad exams but also instilled in him a sense of discipline and perseverance."},
    ]
    cols = st.columns(3)
    for i, t in enumerate(featured):
        with cols[i]:
            st.markdown(f"""
            <div style="background:#f7faf8;border-radius:12px;padding:18px;
                        border-top:4px solid {TEAL};min-height:200px;">
                <div style="font-size:13px;color:#333;font-style:italic;line-height:1.6;margin-bottom:12px;">
                    "{t['comment'][:180]}..."</div>
                <div style="color:{TEAL};font-size:14px">⭐⭐⭐⭐⭐</div>
                <div style="margin-top:8px;">
                    <div style="font-size:13px;font-weight:700;color:{DARK}">{t['name']}</div>
                    <div style="font-size:11px;color:#888">{t['role']} · {t['service']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📋 All Feedback")
    svc_f = st.selectbox("Filter by Service", ["All"] + sorted(df["service"].unique().tolist()))
    display = df if svc_f == "All" else df[df["service"] == svc_f]
    st.dataframe(
        display[["name","role","service","rating","sentiment","comment","date"]]
        .rename(columns={"name":"Name","role":"Role","service":"Service",
                         "rating":"Rating","sentiment":"Sentiment","comment":"Comment","date":"Date"}),
        use_container_width=True, height=300
    )


# ─────────────────────────────────────────────────────────────────────────────
def page_performance():
    st.markdown("## 📊 Academic Performance")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Scores · improvement · Olympiad medals · leaderboard</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    perf     = load("performance.csv")
    students = load("students.csv")
    if perf.empty:
        st.warning("Performance data missing."); return

    total_oly    = perf["olympiad_participants"].sum()
    total_gold   = perf["olympiad_gold"].sum()
    total_silver = perf["olympiad_silver"].sum()
    total_bronze = perf["olympiad_bronze"].sum()
    avg_improve  = (perf["avg_score_post"] - perf["avg_score_pre"]).mean()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Olympiad Participants", int(total_oly))
    c2.metric("🥇 Gold Medals",        int(total_gold))
    c3.metric("🥈 Silver Medals",      int(total_silver))
    c4.metric("🥉 Bronze Medals",      int(total_bronze))
    c5.metric("Avg Improvement",       f"+{avg_improve:.1f}%")
    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 📈 Score Improvement — Mathematics")
        math_df = perf[perf["subject"] == "Mathematics"].copy()
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Before", x=math_df["class"], y=math_df["avg_score_pre"],  marker_color="#9FE1CB"))
        fig.add_trace(go.Bar(name="After",  x=math_df["class"], y=math_df["avg_score_post"], marker_color=TEAL))
        fig.update_layout(barmode="group", height=280, margin=dict(t=10,b=10,l=0,r=0),
                          xaxis=dict(tickfont=dict(size=10)), yaxis_title="Avg Score %",
                          paper_bgcolor="white", plot_bgcolor="white", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 📈 Score Improvement — English")
        eng_df = perf[perf["subject"] == "English"].copy()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Before", x=eng_df["class"], y=eng_df["avg_score_pre"],  marker_color="#FAC775"))
        fig2.add_trace(go.Bar(name="After",  x=eng_df["class"], y=eng_df["avg_score_post"], marker_color="#F4A623"))
        fig2.update_layout(barmode="group", height=280, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis=dict(tickfont=dict(size=10)), yaxis_title="Avg Score %",
                           paper_bgcolor="white", plot_bgcolor="white", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🏆 Olympiad Medal Tally by Class")
        oly = perf[perf["olympiad_participants"] > 0].copy()
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="🥇 Gold",   x=oly["class"], y=oly["olympiad_gold"],   marker_color="#F4A623"))
        fig3.add_trace(go.Bar(name="🥈 Silver", x=oly["class"], y=oly["olympiad_silver"], marker_color="#B4B2A9"))
        fig3.add_trace(go.Bar(name="🥉 Bronze", x=oly["class"], y=oly["olympiad_bronze"], marker_color="#E85D24"))
        fig3.update_layout(barmode="stack", height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis=dict(tickfont=dict(size=10)), yaxis_title="Medals",
                           paper_bgcolor="white", plot_bgcolor="white", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 🎯 Attendance vs Score")
        if not students.empty:
            fig4 = px.scatter(students, x="attendance_pct", y="score_avg",
                              color="class", hover_data=["name","service"],
                              color_discrete_sequence=COLORS, template="plotly_white",
                              labels={"attendance_pct":"Attendance %","score_avg":"Avg Score %"})
            fig4.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                               paper_bgcolor="white", plot_bgcolor="white",
                               legend=dict(font=dict(size=9)))
            st.plotly_chart(fig4, use_container_width=True)

    if not students.empty:
        st.markdown("---")
        st.markdown("#### 🏅 Top 10 Performers")
        top = students.nlargest(10,"score_avg")[["name","class","service","score_avg","attendance_pct"]]
        top.columns = ["Student","Class","Service","Score %","Attendance %"]
        top = top.reset_index(drop=True)
        top.index += 1
        st.dataframe(top, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Class-wise Performance Table")
    math_sum = perf[perf["subject"]=="Mathematics"][
        ["class","students_count","avg_score_pre","avg_score_post",
         "olympiad_participants","olympiad_gold","olympiad_silver","olympiad_bronze"]
    ].copy()
    math_sum["improvement"] = (math_sum["avg_score_post"] - math_sum["avg_score_pre"]).round(1)
    math_sum.columns = ["Class","Students","Before","After","Olympiad","Gold","Silver","Bronze","Improvement"]
    st.dataframe(math_sum, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
def page_staff():
    st.markdown("## 👩‍🏫 Staff & Operations")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Faculty · payroll · batch capacity · job pipeline</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df = load("staff.csv")
    if df.empty:
        st.warning("Staff data missing."); return

    active       = df[df["status"] == "Active"]
    total_salary = df["salary"].sum()
    avg_att      = df["attendance_pct"].mean()
    tutors       = len(df[df["role"].str.contains("Tutor", na=False)])
    trainers     = len(df[df["role"].str.contains("Trainer|Coach|Instructor", na=False)])

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Staff",        len(active))
    c2.metric("Tutors / Teachers",  tutors)
    c3.metric("Trainers & Coaches", trainers)
    c4.metric("Monthly Payroll",    f"₹{total_salary:,.0f}")
    c5.metric("Avg Attendance",     f"{avg_att:.1f}%")
    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 👩‍🏫 Staff by Role")
        rc = df["role"].value_counts().reset_index()
        rc.columns = ["Role","Count"]
        fig = px.pie(rc, values="Count", names="Role", hole=0.4,
                     color_discrete_sequence=COLORS, template="plotly_white")
        fig.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("#### 📅 Staff Attendance Rate")
        fig2 = px.bar(df.sort_values("attendance_pct"),
                      x="attendance_pct", y="name", orientation="h",
                      color="attendance_pct",
                      color_continuous_scale=["#fde8e8","#F4A623",TEAL],
                      template="plotly_white", text="attendance_pct")
        fig2.update_traces(texttemplate="%{text}%", textposition="outside")
        fig2.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="Attendance %", yaxis_title="",
                           coloraxis_showscale=False,
                           paper_bgcolor="white", plot_bgcolor="white",
                           xaxis=dict(range=[80,100]))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 💰 Salary Distribution")
        fig3 = px.bar(df.sort_values("salary"),
                      x="salary", y="name", orientation="h",
                      color_discrete_sequence=[TEAL], template="plotly_white", text="salary")
        fig3.update_traces(texttemplate="₹%{text:,}", textposition="outside")
        fig3.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="Monthly Salary (₹)", yaxis_title="",
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 🏫 Batch Capacity Utilization")
        batch = pd.DataFrame({
            "Batch":    ["Morning Tuition","Evening Tuition","Olympiad Morning",
                         "Olympiad Weekend","Handwriting Sat","Online Math"],
            "Capacity": [20, 20, 15, 15, 15, 20],
            "Enrolled": [14, 13,  8,  6,  5, 10],
        })
        batch["Available"] = batch["Capacity"] - batch["Enrolled"]
        fig4 = px.bar(batch, x="Batch", y=["Enrolled","Available"],
                      color_discrete_map={"Enrolled":TEAL,"Available":"#E1F5EE"},
                      barmode="stack", template="plotly_white")
        fig4.update_layout(height=260, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis=dict(tickfont=dict(size=9)), yaxis_title="Students",
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Staff Directory")
    st.dataframe(
        df[["name","role","subject","classes","joining_date","attendance_pct","salary","status"]]
        .rename(columns={"name":"Name","role":"Role","subject":"Subject","classes":"Classes",
                         "joining_date":"Joined","attendance_pct":"Attendance %",
                         "salary":"Salary ₹","status":"Status"}),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")
    st.markdown("#### 📨 Job Applications Pipeline")
    jobs = pd.DataFrame({
        "Position":    ["Tutor – Math","Tutor – English","Robotics Trainer","Admin Assistant","Online Instructor"],
        "Applied":     [12, 8, 5, 7, 6],
        "Shortlisted": [5, 3, 2, 3, 2],
        "Interviewed": [3, 2, 1, 2, 1],
        "Hired":       [1, 1, 0, 1, 0],
    })
    st.dataframe(jobs, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
def page_social():
    st.markdown("## 📡 Social & Digital Presence")
    st.markdown("<p style='color:#5a8a70;margin-top:-8px'>Followers · website traffic · worksheet downloads · WhatsApp leads</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    df = load("social.csv")
    if df.empty:
        st.warning("Social data missing."); return

    latest = df.iloc[-1]
    prev   = df.iloc[-2]

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Facebook",          f"{int(latest['facebook_followers']):,}",  f"+{int(latest['facebook_followers']-prev['facebook_followers'])}")
    c2.metric("Instagram",         f"{int(latest['instagram_followers']):,}", f"+{int(latest['instagram_followers']-prev['instagram_followers'])}")
    c3.metric("YouTube",           f"{int(latest['youtube_subscribers']):,}", f"+{int(latest['youtube_subscribers']-prev['youtube_subscribers'])}")
    c4.metric("Website Visits/Mo", f"{int(latest['website_visits']):,}",      f"+{int(latest['website_visits']-prev['website_visits'])}")
    c5.metric("WhatsApp Leads/Mo", f"{int(latest['whatsapp_leads'])}",        f"+{int(latest['whatsapp_leads']-prev['whatsapp_leads'])}")
    st.markdown("---")

    st.markdown("#### 📈 Follower Growth Trend")
    sm = df.melt(id_vars=["month"],
                 value_vars=["facebook_followers","instagram_followers","youtube_subscribers"],
                 var_name="Platform", value_name="Followers")
    sm["Platform"] = sm["Platform"].map({
        "facebook_followers":  "Facebook",
        "instagram_followers": "Instagram",
        "youtube_subscribers": "YouTube",
    })
    fig = px.line(sm, x="month", y="Followers", color="Platform",
                  color_discrete_sequence=["#1877F2","#E1306C","#FF0000"],
                  markers=True, template="plotly_white", line_shape="spline")
    fig.update_layout(height=280, margin=dict(t=10,b=10,l=0,r=0),
                      xaxis_title="", yaxis_title="Followers",
                      xaxis=dict(tickfont=dict(size=10)),
                      legend=dict(font=dict(size=11)),
                      paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 🌐 Website Traffic")
        fig2 = px.area(df, x="month", y="website_visits",
                       color_discrete_sequence=[TEAL], template="plotly_white")
        fig2.update_traces(fill="tozeroy", fillcolor="rgba(29,158,117,0.12)", line_width=2)
        fig2.update_layout(height=240, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="", yaxis_title="Monthly Visits",
                           xaxis=dict(tickfont=dict(size=9)),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    with col_r:
        st.markdown("#### 📥 Worksheet Downloads")
        fig3 = px.bar(df, x="month", y="worksheet_downloads",
                      color_discrete_sequence=["#534AB7"], template="plotly_white")
        fig3.update_layout(height=240, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="", yaxis_title="Downloads",
                           xaxis=dict(tickfont=dict(size=9)),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 💬 WhatsApp Leads per Month")
        fig4 = px.line(df, x="month", y="whatsapp_leads",
                       color_discrete_sequence=["#25D366"],
                       markers=True, template="plotly_white")
        fig4.update_layout(height=220, margin=dict(t=10,b=10,l=0,r=0),
                           xaxis_title="", yaxis_title="Leads",
                           xaxis=dict(tickfont=dict(size=9)),
                           paper_bgcolor="white", plot_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

    with col_b:
        st.markdown("#### 🔗 Quick Links")
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:10px;margin-top:8px;">
            <a href="https://devnautics.com" target="_blank" style="text-decoration:none;
               background:#E1F5EE;border-radius:8px;padding:10px 14px;color:{DARK};
               font-size:13px;font-weight:600;border-left:4px solid {TEAL};display:block;">
               🌐 devnautics.com</a>
            <a href="https://www.facebook.com" target="_blank" style="text-decoration:none;
               background:#EEF4FF;border-radius:8px;padding:10px 14px;color:#1877F2;
               font-size:13px;font-weight:600;border-left:4px solid #1877F2;display:block;">
               📘 Facebook Page</a>
            <a href="https://www.instagram.com" target="_blank" style="text-decoration:none;
               background:#FFF0F6;border-radius:8px;padding:10px 14px;color:#E1306C;
               font-size:13px;font-weight:600;border-left:4px solid #E1306C;display:block;">
               📸 Instagram</a>
            <a href="https://www.youtube.com" target="_blank" style="text-decoration:none;
               background:#FFF0F0;border-radius:8px;padding:10px 14px;color:#FF0000;
               font-size:13px;font-weight:600;border-left:4px solid #FF0000;display:block;">
               ▶️ YouTube Channel</a>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📊 Full Social Media Data")
    st.dataframe(
        df.rename(columns={
            "month":"Month","facebook_followers":"Facebook","instagram_followers":"Instagram",
            "youtube_subscribers":"YouTube","website_visits":"Website Visits",
            "worksheet_downloads":"Worksheet Downloads","whatsapp_leads":"WhatsApp Leads",
        }),
        use_container_width=True, hide_index=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR & ROUTING
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem;'>
        <div style='font-family:Sora,sans-serif;font-size:22px;font-weight:700;
                    color:#7dffc0;letter-spacing:-0.5px;'>Dev Nautics</div>
        <div style='font-size:11px;color:#7ec8a0;margin-top:2px;'>
            Education CRM · Surat</div>
    </div>
    <hr style='border-color:#1a5c38;margin:0.8rem 0;'/>
    """, unsafe_allow_html=True)

    PAGES = {
        "🏠 Executive Overview":      "Overview",
        "👦 Student Management":      "Students",
        "📋 Services":                "Services",
        "📦 Products & Inventory":    "Products",
        "💰 Revenue & Finance":       "Finance",
        "📣 Leads & Enquiries":       "Leads",
        "⭐ Testimonials & Feedback": "Feedback",
        "📊 Academic Performance":    "Performance",
        "👩‍🏫 Staff & Operations":     "Staff",
        "📡 Social & Digital":        "Social",
    }

    selected = st.radio("", list(PAGES.keys()), label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1a5c38;margin:1rem 0;'/>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:11px;color:#7ec8a0;font-weight:600;
                    letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;'>
                    Global Filters</div>""", unsafe_allow_html=True)

    selected_year = st.selectbox("Academic Year", ["2024-25", "2023-24"], index=0)
    selected_class = st.multiselect(
        "Class Filter",
        ["Jr.Kg","Sr.Kg","Class 1","Class 2","Class 3","Class 4",
         "Class 5","Class 6","Class 7","Class 8","Class 9","Class 10"],
        default=[]
    )
    selected_service = st.multiselect(
        "Service Filter",
        ["Tuition","Olympiad","Handwriting","Worksheet","Online Math","Robotics","Skill Enhancement"],
        default=[]
    )

    st.markdown("""
    <hr style='border-color:#1a5c38;margin:1rem 0;'/>
    <div style='font-size:10px;color:#7ec8a0;text-align:center;line-height:1.8;'>
        U-33 Corner Point, Citylight<br>Surat - 395007<br>
        📞 8866713206<br>
        <a href='https://devnautics.com' style='color:#7dffc0;'>devnautics.com</a>
    </div>
    """, unsafe_allow_html=True)

# Store in session state
st.session_state["selected_year"]    = selected_year
st.session_state["selected_class"]   = selected_class
st.session_state["selected_service"] = selected_service

# ── Route ─────────────────────────────────────────────────────────────────────
page_key = PAGES[selected]

if   page_key == "Overview":    page_overview()
elif page_key == "Students":    page_students()
elif page_key == "Services":    page_services()
elif page_key == "Products":    page_products()
elif page_key == "Finance":     page_finance()
elif page_key == "Leads":       page_leads()
elif page_key == "Feedback":    page_feedback()
elif page_key == "Performance": page_performance()
elif page_key == "Staff":       page_staff()
elif page_key == "Social":      page_social()
