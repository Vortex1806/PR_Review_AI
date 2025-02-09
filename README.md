# PR_Review_AI – AI-Powered Pull Request Reviewer 🚀

**PR_Review_AI** is an AI-driven pull request review agent that automates code analysis using Gemini AI and GitHub API. It provides inline feedback on pull requests, ensuring better code quality, security, and adherence to best practices before merging.

---

## 🛠 Features

- ✅ **AI-Powered Code Reviews** – Uses Gemini AI to analyze and provide detailed feedback.
- ✅ **Automated PR Comments** – Posts inline review comments directly on GitHub pull requests.
- ✅ **Security & Best Practices Checks** – Ensures adherence to coding standards and security guidelines.
- ✅ **Streamlit-Powered UI** – User-friendly dashboard to manage and review PRs effortlessly.
- ✅ **Seamless GitHub Integration** – Fetches PRs and commits using GitHub API for smooth automation.

---

## 🚀 Installation & Setup

### 1️⃣ Install Dependencies

#### For Linux/macOS:

```bash
git clone https://github.com/YOUR_USERNAME/PR_Review_AI.git
cd PR_Review_AI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### For Windows:

```bash
git clone https://github.com/YOUR_USERNAME/PR_Review_AI.git
cd PR_Review_AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Run the PR Review Agent

#### For Linux/macOS:

```bash
python3 main.py
```

#### For Windows

```bash
python main.py
```

## 📂 Repository Structure

```bash
PR_Review_AI/
│── main.py              # Main application file
│── requirements.txt     # Required Python dependencies
│── README.md            # Project documentation
```

## 🔥 How It Works

1. **Enter Credentials** – Input your GitHub OAuth token and Gemini API key in the Streamlit sidebar.
2. **Load Open PRs** – Select a pull request from the list.
3. **AI Analysis** – PR_Review_AI analyzes the code changes using Gemini AI.
4. **Post Feedback** – Inline comments are automatically added to the PR.
5. **Improve Code** – Developers get actionable feedback before merging.


## ⚡ Contributing

We welcome contributions! Feel free to fork this repository, submit issues, and create pull requests. 🙌

---

## 📜 License

MIT License. See LICENSE for details.

---

Enjoy automated PR reviews with **PR_Review_AI**! 🚀

