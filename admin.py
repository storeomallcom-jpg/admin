import streamlit as st
import pandas as pd
from supabase import create_client, Client

st.set_page_config(page_title="ZAOUJAL ADMIN", page_icon="👁️", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)

st.title("👁️ ZAOUJAL COMMAND CENTER")

# حماية لوحة التحكم بكلمة سر
admin_pass = st.sidebar.text_input("ADMIN PASSWORD", type="password")
if admin_pass != st.secrets.get("ADMIN_PASS", "zaoujal137"): # يمكنك تغيير كلمة السر هنا أو وضعها في الـ Secrets
    st.warning("UNAUTHORIZED. ENTER ADMIN PASSWORD.")
    st.stop()

# الاتصال بقاعدة البيانات
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_KEY"])

st.sidebar.success("ACCESS GRANTED.")

# جلب البيانات
users_req = supabase.table("zaoujal_users").select("*").execute()
logs_req = supabase.table("zaoujal_logs").select("*").order("created_at", desc=True).execute()

users_df = pd.DataFrame(users_req.data)
logs_df = pd.DataFrame(logs_req.data)

# الإحصائيات العلوية
col1, col2, col3 = st.columns(3)
col1.metric("TOTAL USERS", len(users_df) if not users_df.empty else 0)
col2.metric("TOTAL AI AUDITS", len(logs_df) if not logs_df.empty else 0)
col3.metric("SYSTEM STATUS", "ONLINE")

st.divider()

# عرض المستخدمين
st.subheader("👥 USERS DATABASE")
if not users_df.empty:
    st.dataframe(users_df[['email', 'pro_credits', 'created_at']], use_container_width=True)
else:
    st.info("No users yet.")

st.divider()

# عرض السجلات (من سأل ماذا؟)
st.subheader("🕵️ AUDIT LOGS (REAL-TIME)")
if not logs_df.empty:
    st.dataframe(logs_df[['user_email', 'mode', 'prompt', 'created_at']], use_container_width=True)
    
    # قراءة التفاصيل
    st.write("### READ SPECIFIC RESPONSE:")
    selected_log = st.selectbox("Select ID to view full text:", logs_df['id'])
    detail = logs_df[logs_df['id'] == selected_log].iloc[0]
    st.text_area("USER PROMPT:", detail['prompt'], height=100)
    st.text_area("AI RESPONSE:", detail['response'], height=200)
else:
    st.info("No logs yet.")
