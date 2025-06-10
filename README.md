# 📄 Resume Analyzer Desktop App  

A Python-based desktop application that analyzes resumes (PDF/DOCX), calculates ATS compatibility scores, and provides actionable feedback to improve your resume. Built with `tkinter`, `PyPDF2`, `python-docx`, and `nltk`.  

## ✨ Features  
- **ATS Score Calculation** (0-100) based on keywords, structure, and formatting.  
- **Strengths & Weaknesses Detection**:  
  - ✅ Highlights strong points (e.g., action verbs, quantifiable achievements).  
  - ❌ Flags issues (e.g., typos, missing sections, poor formatting).  
- **Improvement Suggestions**: Recommends fixes like adding metrics or optimizing bullet points.  
- **User-Friendly UI**: Clean, modern interface inspired by GitHub Analyzer (dark/light theme).  
- **Supports PDF/DOCX**: Parses both formats.  

## ⚙️ Installation  
1. **Prerequisites**:  
   - Python 3.10+  
   - Git (optional)  

2. **Install dependencies**:  
   ```bash
   pip install PyPDF2 python-docx nltk tkinter
   ```

3. **Run the app**:  
   ```bash
   python resume_analyzer.py
   ```  

## 🚀 Usage  
1. Upload a resume (PDF or DOCX).  
2. View your **ATS Score** and detailed feedback.  
3. Apply suggestions to improve your resume!  

## 📂 Project Structure  
```plaintext
resume_analyzer/  
├── resume_analyzer.py  # Main application (single-file)  
├── README.md  
└── samples/            # Example resumes for testing  
   ├── resume_sample.pdf  
   └── resume_sample.docx  
```  

## 🔧 Troubleshooting  
- **Installation errors?** Use `pip install --user` or a virtual environment.  
- **File not loading?** Ensure the resume is not password-protected.  

## 🤝 Contributing  
Pull requests welcome! For major changes, open an issue first.  

## 📜 License  
MIT  
