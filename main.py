import streamlit as st
import os
import datetime
import google.generativeai as genai
from github import Github
from dotenv import load_dotenv

load_dotenv()

# --- Utility Functions ---

def get_today_date():
    """Returns today's date (UTC) as a datetime.date object."""
    return datetime.datetime.utcnow().date()

def fetch_code_changes(pr):
    """Uses PyGithub to fetch the files changed in a given pull request."""
    return pr.get_files()

def review_code_with_gemini(code, filename):
    """
    Uses the Gemini API to generate code review feedback.
    The prompt instructs the model to act as a senior software engineer.
    """
    prompt = f"""
You are a senior software engineer reviewing a pull request.
Rules:
- Focus on code quality, best practices, security, and performance.
- Be specific and actionable in your feedback.

File: {filename}
Code:
{code}

Provide your feedback below:
"""
    response = gemini_model.generate_content(prompt)
    return response.text.strip() if response.text else "No feedback generated."

def get_latest_commit_id(pr):
    """Returns the SHA of the latest commit for the pull request."""
    return pr.head.sha

def post_review_comments(pr, reviews):
    """
    Posts inline review comments on the pull request.
    First, attempts to create a review with multiple comments.
    If that fails, it falls back to posting individual inline comments.
    Returns a log string with the outcome.
    """
    log = ""
    try:
        pr.create_review(
            body="Automated Code Review by VortexAI",
            event="COMMENT",
            comments=[
                {
                    "path": review["file"],
                    "body": review["feedback"],
                    "line": 1,  # Default line number; adjust if needed
                    "side": "RIGHT"  # Comment on the diff's right side
                }
                for review in reviews
            ]
        )
        log += f"✅ Successfully posted review comments on PR #{pr.number}\n"
    except Exception as e:
        log += f"Error creating review as a batch: {e}\n"
        commit_id = get_latest_commit_id(pr)
        for review in reviews:
            try:
                pr.create_comment(review["feedback"], commit_id, review["file"], 1)
                log += f"Posted individual comment on {review['file']}\n"
            except Exception as e2:
                log += f"Error posting comment on {review['file']}: {e2}\n"
    return log

def process_pr_review(pr, update_log):
    """
    Processes the given pull request:
      - Iterates through changed files (with a diff/patch).
      - Uses Gemini to generate review feedback.
      - Posts the AI-generated feedback as inline comments.
    Logs are updated live using the provided update_log function.
    """
    if not pr:
        update_log("❌ No PR provided.")
        return

    update_log(f"✅ Found PR #{pr.number} created at {pr.created_at}, starting review...")
    try:
        code_changes = fetch_code_changes(pr)
        reviews = []
        for file in code_changes:
            if not file.patch:
                continue
            update_log(f"DEBUG: Reviewing file: {file.filename}")
            feedback = review_code_with_gemini(code=file.patch, filename=file.filename)
            reviews.append({"file": file.filename, "feedback": feedback})
        if not reviews:
            update_log("No code changes with diffs found to review.")
            return
        result_log = post_review_comments(pr, reviews)
        update_log(result_log)
        update_log(f"✅ Review completed for PR #{pr.number}")
    except Exception as e:
        update_log(f"❌ Error processing PR review: {e}")

def list_open_prs(repo):
    """Returns a list of open pull requests for the repository."""
    return list(repo.get_pulls(state='open'))

def setup_repo(github_token, github_repo):
    """Initializes the GitHub object and returns the repository."""
    g = Github(github_token)
    repo = g.get_repo(github_repo)
    return repo

# --- Streamlit UI ---

st.title("PR Code Review Agent")

st.sidebar.header("GitHub Configuration")
github_token = st.sidebar.text_input("GitHub Token", type="password")
GEMINI_API_KEY = st.sidebar.text_input("Enter Gemini API Key:", type="password")
github_repo = st.sidebar.text_input("GitHub Repository (e.g., owner/repo)")

if not GEMINI_API_KEY:
    st.error("Gemini API Key is not set. Please enter it in the sidebar.")
else:
    genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")

if st.sidebar.button("Load PRs"):
    if not github_token or not github_repo:
        st.sidebar.error("Please provide both GitHub Token and Repository.")
    else:
        try:
            repo = setup_repo(github_token, github_repo)
            pr_list = list_open_prs(repo)
            if not pr_list:
                st.sidebar.info("No open PRs found.")
            else:
                pr_options = {f"PR #{pr.number}: {pr.title}": pr.number for pr in pr_list}
                st.session_state["pr_options"] = pr_options
                st.session_state["repo"] = repo
                st.sidebar.success("PRs loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error loading PRs: {e}")

if "pr_options" in st.session_state and st.session_state["pr_options"]:
    selected_display = st.selectbox("Select a PR to Review", options=list(st.session_state["pr_options"].keys()))
    selected_pr_number = st.session_state["pr_options"][selected_display]

    if st.button("Review Selected PR"):
        repo = st.session_state["repo"]
        try:
            pr = repo.get_pull(selected_pr_number)
            log_placeholder = st.empty()
            log_messages = []
            def update_log(message):
                log_messages.append(message)
                log_placeholder.text("\n".join(log_messages))

            with st.spinner("Reviewing PR... This may take a moment."):
                process_pr_review(pr, update_log)
        except Exception as e:
            st.error(f"Error reviewing PR: {e}")
