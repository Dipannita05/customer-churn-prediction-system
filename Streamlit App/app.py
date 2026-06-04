#Commands to run this code
#.\venv\Scripts\Activate.ps1
#python -m streamlit run app.py
import streamlit as st
import pandas as pd
import joblib
import time
import google.generativeai as genai

# ── CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnAI — Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ── INJECT CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global reset & fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
 
/* ── Dark background ── */
.stApp {
    background-color: #0f172a;
    color: #e2e8f0;
}
 
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    border-right: 1px solid rgba(148,163,184,0.12) !important;
}
[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
    color: #94a3b8;
}
 
/* ── Cards ── */
.dash-card {
    background: #1e293b;
    border: 0.5px solid rgba(148,163,184,0.15);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 14px;
}
 
/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 10px;
    margin-bottom: 14px;
}
.metric-card {
    flex: 1;
    background: #1e293b;
    border: 0.5px solid rgba(148,163,184,0.12);
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}
.metric-val {
    font-size: 22px;
    font-weight: 600;
    color: #f1f5f9;
}
.metric-label {
    font-size: 11px;
    color: #64748b;
    margin-top: 3px;
}
 
/* ── Risk badges ── */
.badge-low {
    background: rgba(34,197,94,0.12);
    color: #4ade80;
    border: 0.5px solid rgba(74,222,128,0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
}
.badge-med {
    background: rgba(234,179,8,0.12);
    color: #facc15;
    border: 0.5px solid rgba(250,204,21,0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
}
.badge-high {
    background: rgba(239,68,68,0.12);
    color: #f87171;
    border: 0.5px solid rgba(248,113,113,0.3);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    display: inline-block;
}
 
/* ── Progress bar ── */
.prog-wrap {
    background: #0f172a;
    border-radius: 4px;
    height: 7px;
    overflow: hidden;
    margin-top: 8px;
}
.prog-fill-low  { height: 100%; border-radius: 4px; background: #4ade80; }
.prog-fill-med  { height: 100%; border-radius: 4px; background: #facc15; }
.prog-fill-high { height: 100%; border-radius: 4px; background: #f87171; }
 
/* ── AI output card ── */
.ai-card {
    background: #1e293b;
    border: 0.5px solid rgba(99,102,241,0.25);
    border-radius: 12px;
    padding: 16px 18px;
}
.ai-section-title {
    font-size: 12px;
    font-weight: 500;
    color: #818cf8;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.ai-section-title::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #818cf8;
}
.ai-risk-title { color: #f87171; }
.ai-risk-title::before { background: #f87171; }
.ai-action-title { color: #4ade80; }
.ai-action-title::before { background: #4ade80; }
 
/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    width: 100% !important;
    font-size: 14px !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
 
/* ── Input fields ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
.stSelectbox > div > div {
    background: #0f172a !important;
    border-color: rgba(148,163,184,0.2) !important;
    color: #f1f5f9 !important;
    border-radius: 6px !important;
}
 
/* ── Slider ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #6366f1 !important;
}
 
/* ── Section titles ── */
.section-label {
    font-size: 11px;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 12px;
    margin-top: 4px;
}
 
/* ── Header ── */
.top-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 0.5px solid rgba(148,163,184,0.12);
}
.top-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.top-title {
    font-size: 18px;
    font-weight: 600;
    color: #f1f5f9;
}
.top-sub { font-size: 12px; color: #64748b; }
 
/* ── Radio ── */
[data-testid="stRadio"] label { color: #94a3b8 !important; }
 
/* ── Divider ── */
hr { border-color: rgba(148,163,184,0.12) !important; }
 
/* ── Text area ── */
textarea {
    background: #0f172a !important;
    border-color: rgba(148,163,184,0.2) !important;
    color: #f1f5f9 !important;
}
 
/* ── Info / success / error boxes ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 0.5px solid rgba(148,163,184,0.15) !important;
}
</style>
""", unsafe_allow_html=True)
 
 
# ── SETUP AI CLIENT ──────────────────────────────────────────────────
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))
 
 
# ── LOAD ML MODEL ────────────────────────────────────────────────────
@st.cache_resource
def load_assets():
    m = joblib.load('churn_model.pkl')
    s = joblib.load('scaler.pkl')
    return m, s
 
ml_model, scaler = load_assets()
 
 
# ── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;padding-bottom:20px;border-bottom:0.5px solid rgba(148,163,184,0.12);margin-bottom:20px'>
        <div style='width:34px;height:34px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px'>📊</div>
        <div>
            <div style='font-size:14px;font-weight:600;color:#f1f5f9'>ChurnAI</div>
            <div style='font-size:11px;color:#64748b'>Analytics Suite</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("**Navigation**")
    page = st.radio("", ["Dashboard", "Customers", "Insights", "Settings"], label_visibility="collapsed")
 
    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#64748b;line-height:1.8'>
        <div style='margin-bottom:4px'>Model: <span style='color:#818cf8'>Random Forest</span></div>
        <div style='margin-bottom:4px'>Accuracy: <span style='color:#4ade80'>89.4%</span></div>
        <div>AUC Score: <span style='color:#4ade80'>0.9626</span></div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("---")
    st.markdown("""
    <div style='display:flex;align-items:center;gap:8px;padding-top:4px'>
        <div style='width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#fff'>AS</div>
        <div>
            <div style='font-size:12px;color:#e2e8f0'>Analyst</div>
            <div style='font-size:10px;color:#64748b'>Pro Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
 
# ── MAIN HEADER ──────────────────────────────────────────────────────
st.markdown("""
<div class="top-header">
    <div class="top-logo">📊</div>
    <div>
        <div class="top-title">Customer Churn Analysis</div>
        <div class="top-sub">Powered by Machine Learning + Generative AI</div>
    </div>
    <div style='margin-left:auto;background:rgba(34,197,94,0.12);color:#4ade80;border:0.5px solid rgba(74,222,128,0.3);padding:4px 10px;border-radius:20px;font-size:11px;font-weight:500'>
        ● LIVE
    </div>
</div>
""", unsafe_allow_html=True)
 
 
# ── TWO-COLUMN LAYOUT ─────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="medium")
 
 
# ── LEFT: CUSTOMER INPUT ─────────────────────────────────────────────
with col_left:
    st.markdown('<div class="section-label">Customer Profile</div>', unsafe_allow_html=True)
 
    with st.container():
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        age = st.number_input("Age", min_value=18, max_value=100, value=35, help="Customer's current age")
        tenure = st.slider("Tenure (years with bank)", 0, 10, 5)
        balance = st.number_input("Account Balance ($)", value=5000.0, step=1000.0, help="Current account balance")
        products = st.selectbox("Number of Products", [1, 2, 3, 4], format_func=lambda x: f"{x} product{'s' if x > 1 else ''}")
        active = st.radio("Active Member?", ["Yes", "No"], horizontal=True)
        salary = st.number_input("Estimated Salary ($)", value=50000.0, step=5000.0)
        st.markdown('</div>', unsafe_allow_html=True)
 
    predict_clicked = st.button("Predict Churn Risk", use_container_width=True)
 
    if predict_clicked:
        input_df = pd.DataFrame({
            'id': [1], 'CreditScore': [650], 'Gender': [1], 'Age': [age],
            'Tenure': [tenure], 'Balance': [balance], 'NumOfProducts': [products],
            'HasCrCard': [1], 'IsActiveMember': [1 if active == "Yes" else 0],
            'EstimatedSalary': [salary], 'Geography_Germany': [0], 'Geography_Spain': [0]
        })
        scaled = scaler.transform(input_df)
        prediction = ml_model.predict(scaled)[0]
        proba = ml_model.predict_proba(scaled)[0][1]
 
        st.session_state['prediction'] = prediction
        st.session_state['proba'] = proba
        st.session_state['customer'] = {
            'age': age, 'tenure': tenure, 'balance': balance,
            'products': products, 'active': active, 'salary': salary
        }
 
    # Mini analytics section
    st.markdown("---")
    st.markdown('<div class="section-label">Analytics Overview</div>', unsafe_allow_html=True)
 
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        import numpy as np
 
        # Line chart — mock activity
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        activity = [65, 72, 68, 80, 75, 88]
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=months, y=activity, fill='tozeroy',
            line=dict(color='#6366f1', width=2),
            fillcolor='rgba(99,102,241,0.1)'
        ))
        fig_line.update_layout(
            height=140, margin=dict(l=0,r=0,t=8,b=0),
            paper_bgcolor='#1e293b', plot_bgcolor='#1e293b',
            font=dict(color='#64748b', size=10),
            xaxis=dict(showgrid=False, color='#475569'),
            yaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.3)', color='#475569'),
            showlegend=False
        )
        st.markdown('<div class="dash-card"><div style="font-size:11px;color:#64748b;margin-bottom:6px">Customer activity trend</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
 
        # Bar chart — products vs churn
        prod_labels = ["1 product", "2 products", "3 products", "4 products"]
        churn_rates = [18, 8, 43, 82]
        bar_colors = ['#4ade80', '#4ade80', '#facc15', '#f87171']
        fig_bar = go.Figure(go.Bar(
            x=prod_labels, y=churn_rates,
            marker_color=bar_colors,
            marker_line_width=0
        ))
        fig_bar.update_layout(
            height=150, margin=dict(l=0,r=0,t=8,b=0),
            paper_bgcolor='#1e293b', plot_bgcolor='#1e293b',
            font=dict(color='#64748b', size=10),
            xaxis=dict(showgrid=False, color='#475569'),
            yaxis=dict(showgrid=True, gridcolor='rgba(71,85,105,0.3)', color='#475569',
                       title=dict(text='Churn %', font=dict(size=10))),
            showlegend=False
        )
        st.markdown('<div class="dash-card"><div style="font-size:11px;color:#64748b;margin-bottom:6px">Products vs churn risk</div>', unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
 
    except ImportError:
        st.info("Install plotly for charts: `pip install plotly`")
 
 
# ── RIGHT: RESULTS + AI STRATEGY ──────────────────────────────────────
with col_right:
    st.markdown('<div class="section-label">Risk Assessment</div>', unsafe_allow_html=True)
 
    if 'prediction' not in st.session_state:
        st.markdown("""
        <div class="dash-card" style="text-align:center;padding:40px 20px;color:#475569">
            <div style="font-size:36px;margin-bottom:10px;opacity:0.3">◎</div>
            <div style="font-size:14px;color:#64748b">Enter customer details and click<br><strong style='color:#818cf8'>Predict Churn Risk</strong> to see results</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        proba = st.session_state['proba']
        prediction = st.session_state['prediction']
        customer = st.session_state['customer']
        pct = round(proba * 100, 1)
 
        # Value and engagement scores
        value_score = min(99, int((customer['salary'] / 2000) * 0.4 + (customer['balance'] / 3000) * 0.3 + (1 - proba) * 40))
        engage_score = 78 if customer['active'] == 'Yes' else 35
 
        # Risk level
        if proba < 0.35:
            risk_level = "Low Risk"
            badge_class = "badge-low"
            fill_class = "prog-fill-low"
            color_hex = "#4ade80"
        elif proba < 0.65:
            risk_level = "Medium Risk"
            badge_class = "badge-med"
            fill_class = "prog-fill-med"
            color_hex = "#facc15"
        else:
            risk_level = "High Risk"
            badge_class = "badge-high"
            fill_class = "prog-fill-high"
            color_hex = "#f87171"
 
        # Metric cards
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-val" style="color:{color_hex}">{pct}%</div>
                <div class="metric-label">Churn Risk</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{value_score}</div>
                <div class="metric-label">Customer Value</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{engage_score}</div>
                <div class="metric-label">Engagement</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # Risk verdict card with progress bar
        st.markdown(f"""
        <div class="dash-card" style="text-align:center;padding:20px">
            <div style="font-size:13px;color:#64748b;margin-bottom:8px">Churn Probability Score</div>
            <div style="font-size:32px;font-weight:600;color:{color_hex};margin-bottom:8px">{pct}%</div>
            <span class="{badge_class}">● {risk_level}</span>
            <div class="prog-wrap" style="margin-top:14px">
                <div class="{fill_class}" style="width:{pct}%"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:10px;color:#475569;margin-top:5px">
                <span>Low</span><span>Medium</span><span>High</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # Try Plotly gauge
        try:
            import plotly.graph_objects as go
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge",
                value=pct,
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#475569',
                             'tickfont': {'color': '#64748b', 'size': 10}},
                    'bar': {'color': color_hex, 'thickness': 0.25},
                    'bgcolor': '#1e293b',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 35], 'color': 'rgba(74,222,128,0.1)'},
                        {'range': [35, 65], 'color': 'rgba(250,204,21,0.1)'},
                        {'range': [65, 100], 'color': 'rgba(248,113,113,0.1)'},
                    ],
                    'threshold': {'line': {'color': color_hex, 'width': 2}, 'thickness': 0.75, 'value': pct}
                }
            ))
            fig_gauge.update_layout(
                height=180, margin=dict(l=16, r=16, t=16, b=0),
                paper_bgcolor='#1e293b', font=dict(color='#94a3b8', size=11)
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        except ImportError:
            pass
 
        # ── AI STRATEGY ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-label">AI Strategy</div>', unsafe_allow_html=True)
 
        ai_query = st.text_input(
            "Ask AI", value="How do I keep this customer?",
            placeholder="e.g. What retention offer should I make?",
            label_visibility="collapsed"
        )
 
        gen_clicked = st.button("Generate Strategy", use_container_width=True)
 
        if gen_clicked and ai_query:
            prompt = f"""You are a customer retention expert for a bank. Customer profile:
- Age: {customer['age']}, Tenure: {customer['tenure']} years
- Balance: ${customer['balance']:,.0f}, Products: {customer['products']}
- Active: {customer['active']}, Salary: ${customer['salary']:,.0f}
- Churn Risk: {risk_level} ({pct}%)

Question: {ai_query}

Reply in plain text only, no HTML, no markdown symbols.
Use these three sections exactly:

INSIGHTS: 2 sentences about this customer.
RISK FACTORS:
- point 1
- point 2
- point 3
RECOMMENDED ACTIONS:
- point 1
- point 2
- point 3

Keep it concise and professional."""

            with st.spinner("AI is analyzing the customer profile..."):
                try:
                    time.sleep(0.3)
                    model = genai.GenerativeModel("gemini-2.5-flash-lite")
                    response = model.generate_content(prompt)
                    raw = response.text

                    # ── Display AI response cleanly using st.markdown ──
                    # Convert plain text response into nice sections
                    lines = raw.strip().split('\n')
                    insights_text = ""
                    risk_lines = []
                    action_lines = []
                    current_section = None

                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        upper = line.upper()
                        if upper.startswith("INSIGHTS:"):
                            current_section = "insights"
                            rest = line[len("INSIGHTS:"):].strip()
                            if rest:
                                insights_text += rest + " "
                        elif upper.startswith("RISK FACTORS"):
                            current_section = "risks"
                        elif upper.startswith("RECOMMENDED ACTIONS"):
                            current_section = "actions"
                        elif current_section == "insights":
                            insights_text += line + " "
                        elif current_section == "risks":
                            risk_lines.append(line.lstrip("-•").strip())
                        elif current_section == "actions":
                            action_lines.append(line.lstrip("-•").strip())

                    risks_html = "".join(
                        f'<li style="margin-bottom:6px;color:#94a3b8">{r}</li>'
                        for r in risk_lines if r
                    )
                    actions_html = "".join(
                        f'<li style="margin-bottom:6px;color:#94a3b8">{a}</li>'
                        for a in action_lines if a
                    )

                    st.markdown(f"""
                    <div class="ai-card">
                        <div class="ai-section-title">Insights</div>
                        <p style="font-size:13px;color:#94a3b8;line-height:1.65;margin-bottom:14px">{insights_text.strip()}</p>
                        <div class="ai-section-title ai-risk-title">Risk factors</div>
                        <ul style="margin-left:16px;margin-bottom:14px;font-size:13px">{risks_html}</ul>
                        <div class="ai-section-title ai-action-title">Recommended actions</div>
                        <ul style="margin-left:16px;font-size:13px">{actions_html}</ul>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    if "429" in str(e):
                        st.warning("Rate limit reached. Please wait 30 seconds and try again.")
                    else:
                        st.error(f"Error: {e}")
 
        # Segmentation pie
        st.markdown("---")
        st.markdown('<div class="section-label">Customer Segmentation</div>', unsafe_allow_html=True)
        try:
            import plotly.graph_objects as go
            fig_pie = go.Figure(go.Pie(
                labels=["High Value", "At-Risk", "Loyal"],
                values=[50, 25, 25],
                hole=0.55,
                marker=dict(colors=["#6366f1", "#f87171", "#4ade80"],
                            line=dict(color='#0f172a', width=2))
            ))
            fig_pie.update_traces(textfont_size=11, textfont_color='#94a3b8')
            fig_pie.update_layout(
                height=180, margin=dict(l=0,r=0,t=8,b=0),
                paper_bgcolor='#1e293b',
                font=dict(color='#94a3b8', size=11),
                legend=dict(orientation='v', x=0.8, y=0.5, font=dict(size=10, color='#64748b')),
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        except ImportError:
            pass