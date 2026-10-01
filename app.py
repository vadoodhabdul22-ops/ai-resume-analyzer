import streamlit as st
from pypdf import PdfReader


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Skills List
# -----------------------------
skills_list = [
    "Python", "Java", "SQL", "Machine Learning",
    "Deep Learning", "Artificial Intelligence",
    "HTML", "CSS", "JavaScript", "React",
    "Pandas", "NumPy", "Streamlit",
    "Power BI", "AWS", "Docker", "Git"
]


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Analyze your resume against a job description</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("📌 About")

    st.write(
        "AI Resume Analyzer compares your resume "
        "with a job description and identifies "
        "matching and missing skills."
    )

    st.header("🔍 Features")

    st.write("• PDF Resume Analysis")
    st.write("• Skill Detection")
    st.write("• Matching Skills")
    st.write("• Missing Skills")
    st.write("• Resume Match Score")
    st.write("• Improvement Suggestions")


# -----------------------------
# Resume Upload
# -----------------------------
st.header("📄 Resume Analysis")

st.write("Upload your resume in PDF format.")

resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)


# -----------------------------
# Job Description
# -----------------------------
st.header("💼 Job Description")

st.write(
    "Paste the job description you want to compare "
    "your resume with."
)

job_description = st.text_area(
    "Paste the job description here",
    height=200
)


# -----------------------------
# Buttons
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button(
        "🔍 Analyze Resume",
        use_container_width=True
    )

with col2:
    reset_button = st.button(
        "🔄 Reset",
        use_container_width=True
    )


# -----------------------------
# Reset
# -----------------------------
if reset_button:
    st.rerun()


# -----------------------------
# Resume Analysis
# -----------------------------
if analyze_button:

    # Check resume
    if resume is None:
        st.warning("⚠️ Please upload your resume.")

    # Check job description
    elif job_description.strip() == "":
        st.warning("⚠️ Please enter the job description.")

    else:

        st.success("✅ Resume uploaded successfully!")


        # -----------------------------
        # Extract Resume Text
        # -----------------------------
        reader = PdfReader(resume)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""


        # -----------------------------
        # Display Resume Text
        # -----------------------------
        with st.expander("📄 View Extracted Resume Text"):
            st.write(resume_text)


        # -----------------------------
        # Find Skills in Resume
        # -----------------------------
        found_skills = []

        for skill in skills_list:
            if skill.lower() in resume_text.lower():
                found_skills.append(skill)


        st.subheader("🛠️ Skills Found in Resume")

        if found_skills:
            for skill in found_skills:
                st.success(f"✓ {skill}")
        else:
            st.warning("No matching skills found in the resume.")


        # -----------------------------
        # Find Skills in Job Description
        # -----------------------------
        job_skills = []

        for skill in skills_list:
            if skill.lower() in job_description.lower():
                job_skills.append(skill)


        st.subheader("💼 Skills Required by Job Description")

        if job_skills:
            for skill in job_skills:
                st.info(f"• {skill}")
        else:
            st.warning(
                "No matching skills found in the job description."
            )


        # -----------------------------
        # Matching Skills
        # -----------------------------
        matching_skills = []

        for skill in job_skills:
            if skill in found_skills:
                matching_skills.append(skill)


        # -----------------------------
        # Missing Skills
        # -----------------------------
        missing_skills = []

        for skill in job_skills:
            if skill not in found_skills:
                missing_skills.append(skill)


        # -----------------------------
        # Matching Skills Display
        # -----------------------------
        st.subheader("✅ Matching Skills")

        if matching_skills:
            for skill in matching_skills:
                st.success(f"✓ {skill}")
        else:
            st.warning("No matching skills found.")


        # -----------------------------
        # Missing Skills Display
        # -----------------------------
        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.error(f"✗ {skill}")
        else:
            st.success("No required skills are missing!")


        # -----------------------------
        # Calculate Match Percentage
        # -----------------------------
        if job_skills:
            match_percentage = (
                len(matching_skills) / len(job_skills)
            ) * 100
        else:
            match_percentage = 0


        # -----------------------------
        # Analysis Summary
        # -----------------------------
        st.subheader("📈 Analysis Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Resume Skills",
            len(found_skills)
        )

        col2.metric(
            "Required Skills",
            len(job_skills)
        )

        col3.metric(
            "Matching",
            len(matching_skills)
        )

        col4.metric(
            "Missing",
            len(missing_skills)
        )


        # -----------------------------
        # Resume Match Score
        # -----------------------------
        st.subheader("📊 Resume Match Score")

        st.metric(
            label="Overall Match",
            value=f"{match_percentage:.1f}%"
        )

        st.progress(int(match_percentage))

        st.write(
            f"Your resume matches "
            f"{match_percentage:.1f}% "
            "of the job requirements."
        )


        # -----------------------------
        # Improvement Suggestions
        # -----------------------------
        st.subheader("💡 Resume Improvement Suggestions")

        if missing_skills:

            for skill in missing_skills:
                st.markdown(
                    f"• Learn or improve **{skill}**"
                )

        else:

            st.success(
                "Your resume covers all the skills "
                "mentioned in the job description!"
            )


        # -----------------------------
        # Create Analysis Report
        # -----------------------------
        report = f"""
AI RESUME ANALYZER REPORT
=========================

Resume Skills Found:
{", ".join(found_skills)}

Job Required Skills:
{", ".join(job_skills)}

Matching Skills:
{", ".join(matching_skills)}

Missing Skills:
{", ".join(missing_skills)}

Resume Match Score:
{match_percentage:.1f}%

Recommendations:
"""

        if missing_skills:

            for skill in missing_skills:
                report += (
                    f"- Learn or improve {skill}\n"
                )

        else:

            report += (
                "- Your resume covers all required skills.\n"
            )


        # -----------------------------
        # Download Report
        # -----------------------------
        st.download_button(
            label="📥 Download Analysis Report",
            data=report,
            file_name="resume_analysis_report.txt",
            mime="text/plain"
        )