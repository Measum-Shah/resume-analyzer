import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
import os
import PyPDF2
import docx
import re
import nltk
from nltk.corpus import words, stopwords

# Ensure NLTK data is downloaded (run this once)
try:
    nltk.data.find('corpora/words')
except nltk.downloader.DownloadError:
    nltk.download('words')
except LookupError:
    nltk.download('words')

try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
except LookupError:
    nltk.download('stopwords')

# --- Resume Parsing Functions ---

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return None
    return text

def parse_resume(file_path):
    """Parses a resume file (PDF or DOCX) and returns text."""
    if not os.path.exists(file_path):
        return None

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        return None

# --- Analysis Functions (Simplified) ---

def calculate_ats_score(text):
    """Calculates a simplified ATS score based on text content."""
    if not text:
        return 0

    score = 0
    text_lower = text.lower()

    # Basic checks for common sections (simplified regex)
    sections = {
        "contact": r"contact|phone|email|linkedin|address",
        "summary": r"summary|objective|profile",
        "experience": r"experience|work history",
        "education": r"education|academic",
        "skills": r"skills|proficiencies|technical",
    }

    for section, pattern in sections.items():
        if re.search(pattern, text_lower):
            score += 15 # Arbitrary points for section presence

    # Check for common action verbs (simplified list)
    action_verbs = ["managed", "developed", "created", "implemented", "led", "analyzed", "designed", "built", "improved", "reduced", "increased"]
    verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    score += min(verb_count * 2, 20) # Max 20 points for verbs

    # Check for quantifiable achievements (very basic - presence of numbers near verbs)
    quantifiable_pattern = r"\b(?:managed|developed|created|implemented|led|analyzed|designed|built|improved|reduced|increased)\s+\d+"
    if re.search(quantifiable_pattern, text_lower):
         score += 10 # Arbitrary points for potential quantification

    # Check for length (simple word count)
    words_list = text.split()
    if 300 <= len(words_list) <= 800: # Ideal length range
        score += 10
    elif 200 <= len(words_list) < 300 or 800 < len(words_list) <= 1000:
        score += 5

    # Basic check for typos (using NLTK words - very basic)
    # This is computationally expensive and not very accurate for real resumes
    # We'll skip a full typo check for this simplified version, but keep the idea.
    # words_in_text = re.findall(r'\b\w+\b', text_lower)
    # english_words = set(words.words())
    # typos = [word for word in words_in_text if word not in english_words and len(word) > 1]
    # score -= min(len(typos) * 2, 10) # Deduct points for potential typos

    # Ensure score is between 0 and 100
    return max(0, min(100, score))

def analyze_resume_elements(text):
    """Analyzes text for good and bad elements (simplified)."""
    strengths = []
    weaknesses = []
    suggestions = []

    if not text:
        weaknesses.append("No text extracted from the resume.")
        suggestions.append("Ensure the file is a readable PDF or DOCX.")
        return strengths, weaknesses, suggestions

    text_lower = text.lower()

    # --- Strengths ---
    sections_found = []
    sections_patterns = {
        "Contact Information": r"contact|phone|email|linkedin|address",
        "Summary/Objective": r"summary|objective|profile",
        "Experience Section": r"experience|work history",
        "Education Section": r"education|academic",
        "Skills Section": r"skills|proficiencies|technical",
    }
    for name, pattern in sections_patterns.items():
        if re.search(pattern, text_lower):
            strengths.append(f"Includes a {name}.")
            sections_found.append(name)

    action_verbs = ["managed", "developed", "created", "implemented", "led", "analyzed", "designed", "built", "improved", "reduced", "increased"]
    found_verbs = [verb for verb in action_verbs if verb in text_lower]
    if found_verbs:
        strengths.append(f"Uses action verbs like: {', '.join(list(set(found_verbs))[:5])}...") # Show a few examples

    quantifiable_pattern = r"\b(?:managed|developed|created|implemented|led|analyzed|designed|built|improved|reduced|increased)\s+\d+"
    if re.search(quantifiable_pattern, text_lower):
         strengths.append("Potentially includes quantifiable achievements (e.g., 'increased sales by 15%').")

    # --- Weaknesses ---
    if "Contact Information" not in sections_found:
        weaknesses.append("Missing or unclear Contact Information.")
        suggestions.append("Add clear contact details (phone, email, LinkedIn).")

    if "Experience Section" not in sections_found and "Education Section" not in sections_found:
         weaknesses.append("Missing both Experience and Education sections.")
         suggestions.append("Include relevant Experience and/or Education sections.")
    elif "Experience Section" not in sections_found:
         weaknesses.append("Missing Experience section.")
         suggestions.append("Add your work experience.")
    elif "Education Section" not in sections_found:
         weaknesses.append("Missing Education section.")
         suggestions.append("Add your educational background.")

    if "Skills Section" not in sections_found:
        weaknesses.append("Missing Skills section.")
        suggestions.append("Add a dedicated section for your relevant skills.")

    # Basic typo check (simplified - just check for very short words not in dictionary)
    # This is still very basic and prone to errors
    words_in_text = re.findall(r'\b\w+\b', text_lower)
    english_words = set(words.words())
    stop_words = set(stopwords.words('english'))
    potential_typos = [word for word in words_in_text if word not in english_words and word not in stop_words and len(word) > 1 and not word.isdigit()]
    if potential_typos:
        weaknesses.append(f"Potential typos detected (e.g., '{', '.join(list(set(potential_typos))[:5])}').")
        suggestions.append("Read carefully for spelling and grammar errors.")

    # Check for very long paragraphs (simple line break check)
    if "\n\n\n" in text: # More than two consecutive newlines might indicate poor formatting
         weaknesses.append("Potential formatting issues (e.g., large gaps or long paragraphs).")
         suggestions.append("Use bullet points for experience and education details. Ensure consistent spacing.")

    # --- Suggestions (based on weaknesses) ---
    # Suggestions are already added when weaknesses are detected in this simplified version

    if not strengths and not weaknesses:
        suggestions.append("Could not analyze the resume effectively. Ensure the text is readable.")


    return strengths, weaknesses, suggestions

# --- Tkinter App ---

class ResumeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Analyzer")
        self.root.geometry("800x700") # Initial window size

        # Configure style for a cleaner look (optional, requires ttk)
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0")
        style.configure("TButton", padding=6)
        style.configure("TProgressbar", thickness=20)
        style.configure("Card.TFrame", background="#ffffff", relief="raised", borderwidth=1) # Simulate cards

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for responsiveness
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1) # Allow results area to expand

        # --- File Upload Section ---
        self.upload_frame = ttk.Frame(self.main_frame, padding="5")
        self.upload_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.file_label = ttk.Label(self.upload_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.upload_button = ttk.Button(self.upload_frame, text="Upload Resume (PDF/DOCX)", command=self.upload_file)
        self.upload_button.pack(side=tk.RIGHT)

        # --- Results Section ---
        self.results_frame = ttk.Frame(self.main_frame, padding="5")
        self.results_frame.grid(row=1, column=0, sticky="nsew")
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1) # Allow content frame to expand

        self.score_frame = ttk.Frame(self.results_frame, padding="5")
        self.score_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.score_frame.columnconfigure(1, weight=1) # Allow progress bar to expand

        self.score_label = ttk.Label(self.score_frame, text="ATS Score: N/A", font=('Arial', 14, 'bold'))
        self.score_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.progress_bar = ttk.Progressbar(self.score_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=0, column=1, sticky="ew")

        # Content Frame for Strengths, Weaknesses, Suggestions
        self.content_frame = ttk.Frame(self.results_frame, padding="5")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1) # Allow the notebook to expand

        # Using ttk.Notebook for sections (simulates expandable/collapsible visually)
        # True expandable sections are more complex in pure Tkinter
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Strengths Tab
        self.strengths_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding="10")
        self.notebook.add(self.strengths_frame, text="✅ Strengths")
        self.strengths_text = scrolledtext.ScrolledText(self.strengths_frame, wrap=tk.WORD, state=tk.DISABLED, height=8)
        self.strengths_text.pack(fill=tk.BOTH, expand=True)

        # Weaknesses Tab
        self.weaknesses_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding="10")
        self.notebook.add(self.weaknesses_frame, text="⚠️ Weaknesses")
        self.weaknesses_text = scrolledtext.ScrolledText(self.weaknesses_frame, wrap=tk.WORD, state=tk.DISABLED, height=8)
        self.weaknesses_text.pack(fill=tk.BOTH, expand=True)

        # How to Improve Tab
        self.improve_frame = ttk.Frame(self.notebook, style="Card.TFrame", padding="10")
        self.notebook.add(self.improve_frame, text="💡 How to Improve")
        self.improve_text = scrolledtext.ScrolledText(self.improve_frame, wrap=tk.WORD, state=tk.DISABLED, height=8)
        self.improve_text.pack(fill=tk.BOTH, expand=True)

    def upload_file(self):
        """Opens file dialog and processes the selected file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Resume Files", "*.pdf *.docx"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.analyze_resume(file_path)
        else:
            self.file_label.config(text="No file selected")
            self.clear_results()

    def analyze_resume(self, file_path):
        """Parses, analyzes, and displays results."""
        self.clear_results()
        self.score_label.config(text="Analyzing...")
        self.progress_bar['value'] = 0
        self.root.update_idletasks() # Update UI

        text = parse_resume(file_path)

        if text:
            # Simulate analysis progress (optional)
            self.progress_bar['value'] = 20
            self.root.update_idletasks()

            ats_score = calculate_ats_score(text)
            self.progress_bar['value'] = 60
            self.root.update_idletasks()

            strengths, weaknesses, suggestions = analyze_resume_elements(text)
            self.progress_bar['value'] = 90
            self.root.update_idletasks()

            self.display_results(ats_score, strengths, weaknesses, suggestions)
            self.progress_bar['value'] = 100
        else:
            messagebox.showerror("Error", "Could not read the selected file.")
            self.score_label.config(text="ATS Score: N/A")
            self.progress_bar['value'] = 0


    def display_results(self, score, strengths, weaknesses, suggestions):
        """Displays the analysis results in the UI."""
        self.score_label.config(text=f"ATS Score: {score}/100")
        self.progress_bar['value'] = score # Set progress bar to score

        # Display Strengths
        self.strengths_text.config(state=tk.NORMAL)
        self.strengths_text.delete(1.0, tk.END)
        if strengths:
            self.strengths_text.insert(tk.END, "\n".join([f"- {s}" for s in strengths]))
        else:
            self.strengths_text.insert(tk.END, "No specific strengths detected by this analysis.")
        self.strengths_text.config(state=tk.DISABLED)

        # Display Weaknesses
        self.weaknesses_text.config(state=tk.NORMAL)
        self.weaknesses_text.delete(1.0, tk.END)
        if weaknesses:
            self.weaknesses_text.insert(tk.END, "\n".join([f"- {w}" for w in weaknesses]))
        else:
            self.weaknesses_text.insert(tk.END, "No specific weaknesses detected by this analysis.")
        self.weaknesses_text.config(state=tk.DISABLED)

        # Display Suggestions
        self.improve_text.config(state=tk.NORMAL)
        self.improve_text.delete(1.0, tk.END)
        if suggestions:
            self.improve_text.insert(tk.END, "\n".join([f"- {s}" for s in suggestions]))
        else:
            self.improve_text.insert(tk.END, "Based on the analysis, no specific improvement suggestions are available at this time.")
        self.improve_text.config(state=tk.DISABLED)

    def clear_results(self):
        """Clears the results display areas."""
        self.score_label.config(text="ATS Score: N/A")
        self.progress_bar['value'] = 0

        self.strengths_text.config(state=tk.NORMAL)
        self.strengths_text.delete(1.0, tk.END)
        self.strengths_text.config(state=tk.DISABLED)

        self.weaknesses_text.config(state=tk.NORMAL)
        self.weaknesses_text.delete(1.0, tk.END)
        self.weaknesses_text.config(state=tk.DISABLED)

        self.improve_text.config(state=tk.NORMAL)
        self.improve_text.delete(1.0, tk.END)
        self.improve_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeAnalyzerApp(root)
    root.mainloop()