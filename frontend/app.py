import streamlit as st
import requests
from api_client import get_prediction, upload_documents
st.set_page_config(page_title="Scholarship Portal", layout="wide")

# ================= SESSION STATE =================
for key, val in [("step", 0), ("gender", ""), ("caste", ""), ("religion", ""),
                 ("single", 0), ("edu", ""), ("marks", 0.0), ("stream", ""),
                 ("income", 0), ("other", 0), ("results", None),("ocr_marks_done",False),("ocr_income_done",False),("ocr_marks",0.0),("ocr_income",0)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ================= CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #f7f4ee; }
#MainMenu, footer, header { visibility: hidden; }

.portal-header {
    background: linear-gradient(90deg, #1e3a8a, #2563eb);
    color: white; padding: 24px 32px; border-radius: 14px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 8px;
}
.portal-header h2 { margin: 0 0 4px; font-size: 1.6rem; font-weight: 700; }
.portal-header p  { margin: 0; opacity: 0.85; font-size: 0.95rem; }

.card {
    background: white; padding: 36px; border-radius: 16px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.1);
    border-left: 6px solid #1e3a8a; margin-top: 24px;
}

.step-bar {
    display: flex; justify-content: space-between;
    margin: 18px 0 4px; font-size: 0.85rem; font-weight: 600;
}
.step-item {
    flex: 1; text-align: center; padding: 6px 4px;
    color: #94a3b8; border-bottom: 3px solid #e2e8f0;
    transition: all 0.2s;
}
.step-item.active   { color: #1e3a8a; border-bottom: 3px solid #1e3a8a; }
.step-item.done     { color: #16a34a; border-bottom: 3px solid #16a34a; }

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #1e3a8a, #2563eb) !important;
    color: white !important; border-radius: 10px !important;
    border: none !important; padding: 10px 28px !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.9 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(30,58,138,0.35) !important;
}

/* Result cards */
.result-card {
    background: white; padding: 22px 28px; border-radius: 12px;
    border-top: 5px solid #1e3a8a; margin-top: 18px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
.result-card h4 { margin: 0 0 8px; color: #1e3a8a; font-size: 1.05rem; }
.result-card p  { margin: 0; color: #475569; font-size: 0.93rem; line-height: 1.6; }

.scheme-tag {
    display: inline-block; background: #eff6ff; color: #1e40af;
    font-size: 0.75rem; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; margin-bottom: 8px;
}

.eligible-badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 700;
}
.eligible   { background: #dcfce7; color: #16a34a; }
.ineligible { background: #fee2e2; color: #dc2626; }

.prob-label {
    display: flex; justify-content: space-between;
    font-size: 0.85rem; font-weight: 600; margin-bottom: 4px;
    color: #334155;
}

.insight-item {
    background: #f8fafc; border-left: 4px solid #2563eb;
    padding: 10px 14px; border-radius: 6px;
    margin-bottom: 10px; font-size: 0.9rem; color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ================= DATA =================
UG = ["Mathematics","Statistics","Physics","Chemistry","Botany","Zoology",
      "Family & Community Science","Computer Science","Textiles & Fashion Technology",
      "Psychology","English Language & Literature","Functional English","Economics",
      "Sociology","Malayalam Language & Literature","Commerce","Web Technology","Food Processing"]

PG = ["English","Economics","Malayalam","Sociology","Master of Commerce",
      "Master of Social Work","Physics","Zoology","Botany","Mathematics",
      "Statistics","Chemistry (self-financing)",
      "Home Science (Nutrition & Dietetics)",
      "Home Science (Textiles & Costume Science)",
      "Computer Science (Data Science)"]

# ================= HELPERS =================
def render_header():
    st.markdown("""
    <div class="portal-header">
        <h2> Scholarship Recommendation Portal</h2>
        <p>AI Powered Eligibility System</p>
    </div>
    """, unsafe_allow_html=True)

def render_steps():
    steps  = ["Welcome", "Personal", "Academic", "Financial", "Results"]
    cur    = st.session_state.step
    html   = "<div class='step-bar'>"
    for i, s in enumerate(steps):
        cls = "active" if i == cur else ("done" if i < cur else "step-item")
        if cls in ("active", "done"):
            html += f"<div class='step-item {cls}'>{'✓ ' if cls=='done' else ''}{s}</div>"
        else:
            html += f"<div class='step-item'>{s}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.progress((cur) / 4)


# ================= RENDER =================
render_header()
render_steps()

# ─────────────────────────────────────────
#  STEP 0 — Welcome
# ─────────────────────────────────────────
if st.session_state.step == 0:
    st.markdown("""
    <div class="card">
        <h3 style="color:#1e3a8a;margin-top:0;">Welcome to the Scholarship Portal</h3>
        <p style="color:#475569;line-height:1.7;">
            This AI-powered system helps students identify eligible scholarships using:
        </p>
        <ul style="color:#475569;line-height:2;">
            <li> Machine Learning Prediction</li>
            <li> Government Rule Engine</li>
            <li> E-Grantz AI Model</li>
            <li> Explainable AI Insights (SHAP)</li>
        </ul>
        <p style="color:#64748b;font-size:0.9rem;">
            Complete the 4-step form. It takes less than 2 minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([2, 1, 2])
    with col:
        if st.button("Start Application", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

# ─────────────────────────────────────────
#  STEP 1 — Personal Information
# ─────────────────────────────────────────
elif st.session_state.step == 1:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("####  Personal Information")

    gender = st.selectbox("Gender *", ["Select", "Male", "Female", "Other"],
                          index=["Select", "Male", "Female", "Other"].index(
                              st.session_state.gender) if st.session_state.gender in ["Select", "Male", "Female",
                                                                                      "Other"] else 0)
    caste = st.selectbox("Caste Category *", ["Select", "General", "OBC", "SC", "ST"],
                         index=["Select", "General", "OBC", "SC", "ST"].index(
                             st.session_state.caste) if st.session_state.caste in ["Select", "General", "OBC", "SC",
                                                                                   "ST"] else 0)
    religion = st.selectbox("Religion *",
                            ["Select", "Hindu", "Muslim", "Christian", "Sikh", "Buddhist", "Jain", "Other"],
                            index=["Select", "Hindu", "Muslim", "Christian", "Sikh", "Buddhist", "Jain", "Other"].index(
                                st.session_state.religion) if st.session_state.religion in ["Select", "Hindu", "Muslim",
                                                                                            "Christian", "Sikh",
                                                                                            "Buddhist", "Jain",
                                                                                            "Other"] else 0)

    # Single girl child — disabled unless Female
    is_female  = (gender == "Female")
    single = st.selectbox(
        "Single Girl Child *" + ("" if is_female else " (applicable for Female only)"),
        ["No", "Yes"],
        index=1 if st.session_state.single == 1 else 0,
        disabled=not is_female,
        help="Enabled only when Gender = Female"
    )
    if not is_female:
        st.caption("ℹ️ This field is enabled only when Gender = Female.")

    st.markdown("</div>", unsafe_allow_html=True)

    c_back, _, _,_, c_next = st.columns([1, 4, 1, 1, 1])
    with c_back:
        if st.button("← Back", key="back1"):
            st.session_state.step = 0
            st.rerun()
    with c_next:
        if st.button("Next →", key="next1"):
            if "Select" in [gender, caste, religion]:
                st.warning("⚠️ Please fill all required fields.")
            else:
                st.session_state.gender   = gender
                st.session_state.caste    = caste
                st.session_state.religion = religion
                st.session_state.single   = 1 if (is_female and single == "Yes") else 0
                st.session_state.step     = 2
                st.rerun()

# ─────────────────────────────────────────
#  STEP 2 — Academic Information
# ─────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown("####  Academic Information")
    with st.expander("Auto-fill from Grade Card (optional)"):
        grade_file = st.file_uploader("Upload Grade Card / Marksheet", type=["pdf", "png", "jpg", "jpeg"],
                                      key="grade_upload")
        if grade_file and not st.session_state["ocr_marks_done"] and "ocr_marks_pending" not in st.session_state:
            with st.spinner("Reading document..."):
                try:
                    files = {"files": (grade_file.name, grade_file.getvalue(), grade_file.type)}
                    ocr_res = upload_documents(files)
                    profile = ocr_res.get("extracted_student_profile", {})
                    pct = profile.get("previous_education_percentage")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Percentage Detected", f"{pct}%" if pct else "Not found")
                    with col2:
                        st.metric("Document Type", ocr_res.get("documents", [{}])[0].get("document_type", "Unknown"))
                    if pct:
                        st.session_state["ocr_marks_pending"] = float(pct)
                        st.rerun()
                    else:
                        st.warning("⚠️ Could not extract percentage. Please enter manually.")
                except Exception as e:
                    st.error(f"OCR failed: {e}")

        if "ocr_marks_pending" in st.session_state and not st.session_state["ocr_marks_done"]:
            st.info(f"📋 Extracted: {st.session_state['ocr_marks_pending']}% — Is this correct?")
            c_yes, c_no, _ = st.columns([1, 1, 4])
            with c_yes:
                if st.button("Yes, autofill", key="marks_yes"):
                    st.session_state.marks = st.session_state["ocr_marks_pending"]
                    st.session_state["ocr_marks_done"] = True
                    del st.session_state["ocr_marks_pending"]
                    st.rerun()
            with c_no:
                if st.button(" No, enter manually", key="marks_no"):
                    st.session_state["ocr_marks_done"] = True
                    del st.session_state["ocr_marks_pending"]
                    st.rerun()

        if st.session_state["ocr_marks_done"]:
            st.success(f"Auto-filled: {st.session_state.marks}%")

    edu = st.selectbox("Current Education Level *", ["Select", "UG", "PG"],
                       index=["Select", "UG", "PG"].index(st.session_state.edu) if st.session_state.edu in ["Select",
                                                                                                            "UG",
                                                                                                            "PG"] else 0)

    marks = st.number_input("Previous Education Percentage *", min_value=0.0, max_value=100.0, step=0.1,
                            value=float(st.session_state.get("marks", 0.0)))

    stream = None
    if edu == "UG":
        stream = st.selectbox("Stream *", UG,
                              index=UG.index(st.session_state.stream) if st.session_state.stream in UG else 0)
    elif edu == "PG":
        stream = st.selectbox("Stream *", PG,
                              index=PG.index(st.session_state.stream) if st.session_state.stream in PG else 0)

    st.markdown("</div>", unsafe_allow_html=True)

    c_back, _, _, _, c_next = st.columns([1, 4, 1, 1, 1])
    with c_back:
        if st.button("← Back", key="back2"):
            st.session_state.step = 1
            st.rerun()
    with c_next:
        if st.button("Next →", key="next2"):
            if edu == "Select":
                st.warning("⚠️ Please select education level.")
            elif marks <= 0:
                st.warning("⚠️ Please enter a valid percentage.")
            elif stream is None:
                st.warning("⚠️ Please select your stream.")
            else:
                st.session_state.edu = edu
                st.session_state.marks = marks
                st.session_state.stream = stream
                st.session_state.step = 3
                st.rerun()

# ─────────────────────────────────────────
#  STEP 3 — Financial Information
# ─────────────────────────────────────────
elif st.session_state.step == 3:
    st.markdown("####  Financial Information")
    with st.expander("Auto-fill from Income Certificate (optional)"):
        income_file = st.file_uploader("Upload Income Certificate", type=["pdf", "png", "jpg", "jpeg"],
                                       key="income_upload")
        if income_file and not st.session_state["ocr_income_done"] and "ocr_income_pending" not in st.session_state:
            with st.spinner("Reading document..."):
                try:
                    files = {"files": (income_file.name, income_file.getvalue(), income_file.type)}
                    ocr_res = upload_documents(files)
                    profile = ocr_res.get("extracted_student_profile", {})
                    inc = profile.get("annual_income")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Annual Income Detected", f"₹{int(inc):,}" if inc else "Not found")
                    with col2:
                        st.metric("Document Type", ocr_res.get("documents", [{}])[0].get("document_type", "Unknown"))
                    if inc:
                        st.session_state["ocr_income_pending"] = int(inc)
                        st.rerun()
                    else:
                        st.warning("⚠️ Could not extract income. Please enter manually.")
                except Exception as e:
                    st.error(f"OCR failed: {e}")

        if "ocr_income_pending" in st.session_state and not st.session_state["ocr_income_done"]:
            st.info(f"📋 Extracted: ₹{st.session_state['ocr_income_pending']:,} — Is this correct?")
            c_yes, c_no, _ = st.columns([1, 1, 4])
            with c_yes:
                if st.button("Yes, autofill", key="income_yes"):
                    st.session_state.income = st.session_state["ocr_income_pending"]
                    st.session_state["ocr_income_done"] = True
                    del st.session_state["ocr_income_pending"]
                    st.rerun()
            with c_no:
                if st.button("No, enter manually", key="income_no"):
                    st.session_state["ocr_income_done"] = True
                    del st.session_state["ocr_income_pending"]
                    st.rerun()

        if st.session_state["ocr_income_done"]:
            st.success(f"Auto-filled: ₹{st.session_state.income:,}")

    income = st.number_input("Annual Family Income (₹) *", min_value=0, step=1000,
                             value=st.session_state.get("income", 0))

    other = st.selectbox("Currently Receiving Any Other Scholarship? *", ["No", "Yes"],
                         index=1 if st.session_state.other == 1 else 0)

    st.markdown("</div>", unsafe_allow_html=True)

    c_back, _, _, _, c_next = st.columns([1, 4, 1, 1, 1])
    with c_back:
        if st.button("← Back", key="back3"):
            st.session_state.step = 2
            st.rerun()
    with c_next:
        if st.button("Check Eligibility ", key="check", use_container_width=True):
            if income <= 0:
                st.warning("⚠️ Annual income must be greater than zero.")
            else:
                st.session_state.income = income
                st.session_state.other  = 1 if other == "Yes" else 0
                st.session_state.step   = 4
                st.rerun()

# ─────────────────────────────────────────
#  STEP 4 — Results
# ─────────────────────────────────────────
elif st.session_state.step == 4:

    # ── Call backend only once ────────────────────────────────────────────
    if st.session_state.results is None:
        payload = {
            "previous_education_percentage": st.session_state.marks,
            "annual_income":                 st.session_state.income,
            "other_scholarship":             st.session_state.other,
            "caste_category":                st.session_state.caste,
            "religion":                      st.session_state.religion,
            "stream":                        st.session_state.stream,
            "gender":                        st.session_state.gender,
            "single_child":                  st.session_state.single
        }
        #st.write("DEBUG PAYLOAD:",payload)
        try:
            with st.spinner("Analysing your eligibility..."):
                res = requests.post(
                    "http://127.0.0.1:5000/predict_full/full",
                    json=payload,
                    timeout=30
                ).json()
            st.session_state.results = res
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Make sure Flask is running on port 5000.")
            st.stop()
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            st.stop()

    res = st.session_state.results

    st.markdown("##  Eligibility Results")

    # ── Rule-based schemes ────────────────────────────────────────────────
    rule_schemes = res.get("rule_based_schemes", [])
    if rule_schemes:
        st.markdown("###  Eligible Government Schemes")
        for scheme in rule_schemes:
            st.markdown(f"""
            <div class="result-card">
                <span class="scheme-tag">Rule-Based</span>
                <h4>{scheme.get("scheme", "Scheme")}</h4>
                <p>{scheme.get("reason", "")}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result-card">
            <p style="color:#64748b;">No rule-based schemes matched your profile.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── ML Predictions ────────────────────────────────────────────────────
    st.markdown("###  ML Predictions")
    ml       = res.get("ml_predictions", {})
    merit    = ml.get("merit_scholarship",  {})
    egrantz  = ml.get("egrantz_scholarship", {})

    merit_eligible   = merit.get("eligible",   False)
    merit_prob       = float(merit.get("probability",   0))
    egrantz_eligible = egrantz.get("eligible", False)
    egrantz_prob     = float(egrantz.get("probability", 0))

    col_m, col_e = st.columns(2)

    with col_m:
        m_badge = "eligible" if merit_eligible else "ineligible"
        m_label = "Eligible" if merit_eligible else "Not Eligible"
        st.markdown(f"""
        <div class="result-card">
            <span class="scheme-tag">ML Model</span>
            <h4>Merit Scholarship</h4>
            <span class="eligible-badge {m_badge}">{m_label}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="prob-label"><span>Probability</span><span>{merit_prob:.1%}</span></div>', unsafe_allow_html=True)
        st.progress(merit_prob)

    with col_e:
        e_badge = "eligible" if egrantz_eligible else "ineligible"
        e_label = "Eligible" if egrantz_eligible else "Not Eligible"
        st.markdown(f"""
        <div class="result-card">
            <span class="scheme-tag">ML Model</span>
            <h4>E-Grantz Scholarship</h4>
            <span class="eligible-badge {e_badge}">{e_label}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<div class="prob-label"><span>Probability</span><span>{egrantz_prob:.1%}</span></div>', unsafe_allow_html=True)
        st.progress(egrantz_prob)

    # ── AI Explanations (SHAP) ────────────────────────────────────────────
    explanations = res.get("explanations", [])
    if explanations:
        st.markdown("###  AI Insights")
        st.markdown('<div class="result-card"><h4>Why these results?</h4>', unsafe_allow_html=True)
        for ex in explanations:
            st.markdown(f'<div class="insight-item">• {ex}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Actions ───────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    _, c1, c2, _ = st.columns([2, 2, 2, 2])
    with c1:
        if st.button("← Update Profile", use_container_width=True):
            st.session_state.results = None
            st.session_state.step    = 1
            st.rerun()
    with c2:
        if st.button(" Return Home", use_container_width=True):
            st.session_state.results = None
            st.session_state.step    = 0
            st.rerun()

    with st.spinner("Analysing your eligibility..."):
        response = requests.post(
            "http://127.0.0.1:5000/predict_full/full",
            json=payload,
            timeout=30
        )
