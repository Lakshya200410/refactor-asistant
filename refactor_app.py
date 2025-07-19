# refactor_app.py
import streamlit as st
import os
import shutil
import tempfile
from git import Repo
from refactor_assistant import analyze_repository

st.set_page_config(page_title="AI Code Refactor & Vulnerability Detector", layout="wide")
st.title("🛠️ Generative Code Refactoring & Vulnerability Detection Assistant")

st.markdown("""
This assistant takes a **GitHub repository URL**, analyzes the code for:
- Code smells (e.g. long functions, duplication)
- Performance issues
- Security vulnerabilities (e.g. OWASP Top 10)

It uses **AI models locally** (no API key needed) to generate suggestions.
""")

repo_url = st.text_input("🔗 Enter GitHub repository URL")
run_analysis = st.button("Analyze Repository")

if run_analysis and repo_url:
    with st.spinner("Cloning and analyzing the repository..."):
        try:
            temp_dir = tempfile.mkdtemp()
            Repo.clone_from(repo_url, temp_dir)
            result = analyze_repository(temp_dir)

            st.success("✅ Analysis complete!")

            if not result:
                st.info("✅ Repository analyzed, but no issues were detected.")
            else:
                for file, suggestions in result.items():
                    with st.expander(f"📄 {file}"):
                        if not suggestions:
                            st.markdown("✅ No issues found in this file.")
                        else:
                            for s in suggestions:
                                st.markdown(f"**Issue:** {s['issue']}")
                                st.code(s['code'], language='python')
                                st.markdown(f"**Fix:** {s['suggested_fix']}")
                                st.markdown("---")

        except Exception as e:
            st.error(f"❌ Error: {e}")

        finally:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
