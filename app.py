import streamlit as st
from datetime import datetime

# Initialize session state if first load

if "status" not in st.session_state:
    st.session_state.status = {
        "A1": "available", "A2": "available", "A3": "available", "A4": "available",
        "B1": "available", "C1": "available", "C2": "available",
        "D1": "available", "D2": "available",
        **{f"M{i}": "available" for i in range(1, 23)}
    }
    st.session_state.booked_by = {}
    st.session_state.booked_at = {}
    st.session_state.booked_until = {}
    st.session_state.overnight = {}




st.set_page_config(page_title="Apartment Parking", layout="wide")
st.title("🏢 Apartment Parking System")

st.sidebar.markdown("### 👤 User Info")
username = st.sidebar.text_input("Enter your name to book a spot:", "")

from datetime import timedelta

st.sidebar.markdown("### ⏱ Parking Time")

duration_minutes = st.sidebar.slider("Parking Duration (in minutes)", 15, 480, 60, step=15)
is_overnight = st.sidebar.checkbox("🌙 Overnight Parking (Ignore time)")


def render_spot(col, spot_id):
    status = st.session_state.status[spot_id]
    color = "#28a745" if status == "available" else "#dc3545"

    booked_by = st.session_state.booked_by.get(spot_id, "")
    booked_at = st.session_state.booked_at.get(spot_id, "")
    booked_until = st.session_state.booked_until.get(spot_id, "")
    overnight = st.session_state.overnight.get(spot_id, False)

    info_line = ""
    if status == "occupied":
        if overnight:
            info_line = f"<br><small>{booked_by}<br>{booked_at}<br>🌙 Overnight</small>"
        else:
            info_line = f"<br><small>{booked_by}<br>{booked_at}<br>Until {booked_until}</small>"

    col.markdown(f"""
        <div style='
            padding:14px;
            background-color:{color};
            color:white;
            border-radius:10px;
            text-align:center;
            font-weight:bold;
            margin-bottom:6px;
            font-size:14px;
        '>
            {spot_id}<br>{status.capitalize()}{info_line}
        </div>
    """, unsafe_allow_html=True)

    if status == "available" and username.strip():
        if col.button(f"Book {spot_id}", key=f"btn_{spot_id}"):
            now = datetime.now()
            end_time = (now + timedelta(minutes=duration_minutes)).strftime("%I:%M %p") if not is_overnight else ""
            st.session_state.status[spot_id] = "occupied"
            st.session_state.booked_by[spot_id] = username
            st.session_state.booked_at[spot_id] = now.strftime("%I:%M %p")
            st.session_state.booked_until[spot_id] = end_time
            st.session_state.overnight[spot_id] = is_overnight
            st.rerun()

# --- A Wing ---
st.markdown("### 🅰️ A Wing (Car Spots)")
a_cols = st.columns(4)
for i, sid in enumerate(["A1", "A2", "A3", "A4"]):
    render_spot(a_cols[i], sid)

# --- B1 next to A ---
st.markdown("### 🚗 B1 (Side Car Spot)")
render_spot(st, "B1")

# --- Motorcycle row below A Wing ---
st.markdown("### 🏍️ Two-Wheelers (Below A Wing)")
m_a_cols = st.columns(6)
for i in range(6):
    render_spot(m_a_cols[i], f"M{i+1}")

# --- C1, C2 ---
st.markdown("### 🚗 Lower Left (C1, C2 Car Spots)")
c_cols = st.columns(2)
render_spot(c_cols[0], "C1")
render_spot(c_cols[1], "C2")

# --- Top-Right Motorcycle Spots (Near B Wing) ---
st.markdown("### 🏍️ Top Right Motorbike Spots (Near B Wing)")
m_top_cols = st.columns(6)
for i in range(6, 12):
    render_spot(m_top_cols[i-6], f"M{i+1}")

# --- Right Block (D1, D2 Car Spots) ---
st.markdown("### 🚗 Right Block (D1, D2 Car Spots)")
d_cols = st.columns(2)
render_spot(d_cols[0], "D1")
render_spot(d_cols[1], "D2")

# --- Bottom Row Motorcycle Spots ---
st.markdown("### 🏍️ Bottom Edge Two-Wheeler Spots")
m_bottom_cols = st.columns(10)
for i in range(12, 22):
    render_spot(m_bottom_cols[i-12], f"M{i+1}")

# --- Developer-only: Reset button ---
if st.button("🔄 Reset All Spots (Dev Only)"):
    for k in st.session_state.status.keys():
        st.session_state.status[k] = "available"
        st.session_state.booked_by[k] = ""
        st.session_state.booked_at[k] = ""
    st.rerun()

