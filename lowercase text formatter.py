import customtkinter as ctk
import re

try:
    import spacy

    try:
        nlp = spacy.load("en_core_web_sm")
        NLP_AVAILABLE = True
    except OSError:
        NLP_AVAILABLE = False
except ImportError:
    NLP_AVAILABLE = False

class ModernTextFormatter(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Lowercase Text Formatter")
        self.geometry("900x750")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.setup_ui()

    def setup_ui(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="Lowercase Text Formatter",
            font=("Roboto Medium", 24),
        )
        self.lbl_title.pack(side="left")

        status_color = "#2CC985" if NLP_AVAILABLE else "#E5B800"
        status_text = "NLP ACTIVE" if NLP_AVAILABLE else "BASIC MODE"

        self.lbl_status = ctk.CTkLabel(
            self.header_frame,
            text=status_text,
            text_color="white",
            fg_color=status_color,
            corner_radius=10,
            padx=10,
            pady=2,
            font=("Roboto", 11, "bold"),
        )
        self.lbl_status.pack(side="right")

        self.lbl_input = ctk.CTkLabel(
            self, text="Input Text", font=("Roboto", 14), text_color="#aaaaaa"
        )
        self.lbl_input.grid(row=1, column=0, padx=20, sticky="w")

        self.input_text = ctk.CTkTextbox(
            self,
            font=("Consolas", 12),
            corner_radius=10,
            border_width=1,
            border_color="#404040",
            fg_color="#1E1E1E",
        )
        self.input_text.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_process = ctk.CTkButton(
            self.btn_frame,
            text="FORMAT TEXT",
            command=self.process_text,
            font=("Roboto", 12, "bold"),
            height=40,
            fg_color="#3B8ED0",
            hover_color="#36719F",
        )
        self.btn_process.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_clear = ctk.CTkButton(
            self.btn_frame,
            text="CLEAR",
            command=self.clear_text,
            font=("Roboto", 12, "bold"),
            height=40,
            fg_color="#C0392B",
            hover_color="#922B21",
            width=100,
        )
        self.btn_clear.pack(side="right")

        self.lbl_output = ctk.CTkLabel(
            self, text="Formatted Output", font=("Roboto", 14), text_color="#aaaaaa"
        )
        self.lbl_output.grid(row=4, column=0, padx=20, sticky="w")

        self.output_text = ctk.CTkTextbox(
            self,
            font=("Consolas", 12),
            corner_radius=10,
            border_width=1,
            border_color="#404040",
            fg_color="#1E1E1E",
        )
        self.output_text.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.lbl_stats = ctk.CTkLabel(
            self.footer_frame,
            text="Words: 0  |  Chars: 0",
            text_color="#808080",
            font=("Roboto", 12),
        )
        self.lbl_stats.pack(side="left")

        self.btn_copy = ctk.CTkButton(
            self.footer_frame,
            text="COPY TO CLIPBOARD",
            command=self.copy_to_clipboard,
            font=("Roboto", 12, "bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            width=200,
        )
        self.btn_copy.pack(side="right")

    def process_text(self):
        raw_text = self.input_text.get("1.0", "end").rstrip()
        if not raw_text:
            return

        lines = raw_text.split("\n")
        processed_lines = []

        for line in lines:
            indent_match = re.match(r"^(\s*)", line)
            indent = indent_match.group(1) if indent_match else ""

            content = line.strip()

            if not content:
                processed_lines.append(line)
                continue

            content = re.sub(r"\s*—\s*|\s*--\s*", " - ", content)
            content = re.sub(r"\s+", " ", content)

            if NLP_AVAILABLE:
                formatted_content = self.logic_nlp(content)
            else:
                formatted_content = self.logic_basic(content)

            processed_lines.append(indent + formatted_content)

        final_text = "\n".join(processed_lines)

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", final_text)
        self.update_stats(final_text)

    def logic_nlp(self, text):
        doc = nlp(text)
        result_tokens = []

        for token in doc:
            word = token.text
            whitespace = token.whitespace_

            if word.lower() == "i":
                result_tokens.append("I" + whitespace)
            elif token.pos_ == "PROPN" or token.ent_type_:
                result_tokens.append(word + whitespace)
            else:
                result_tokens.append(word.lower() + whitespace)

        return "".join(result_tokens)

    def logic_basic(self, text):
        sentences = re.split(r"(?<=[.!?]) +", text)
        formatted_sentences = []

        for sentence in sentences:
            words = sentence.split(" ")
            formatted_words = []

            for index, word in enumerate(words):
                clean_word = word.strip(".,!?;:\"'()[]")

                if clean_word.lower() == "i":
                    formatted_w = re.sub(r"\bi\b", "I", word, flags=re.IGNORECASE)
                    formatted_words.append(formatted_w)
                    continue

                if word.istitle():
                    formatted_words.append(word)
                elif word.isupper() and len(clean_word) > 1:
                    formatted_words.append(word)
                else:
                    formatted_words.append(word.lower())

            formatted_sentences.append(" ".join(formatted_words))

        return " ".join(formatted_sentences)

    def clear_text(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.lbl_stats.configure(text="Words: 0  |  Chars: 0")

    def copy_to_clipboard(self):
        text = self.output_text.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.btn_copy.configure(text="COPIED!", fg_color="#2ECC71")
            self.after(
                2000,
                lambda: self.btn_copy.configure(
                    text="COPY TO CLIPBOARD", fg_color="#27AE60"
                ),
            )

    def update_stats(self, text):
        word_count = len(text.split())
        char_count = len(text)
        self.lbl_stats.configure(text=f"Words: {word_count}  |  Chars: {char_count}")


if __name__ == "__main__":
    app = ModernTextFormatter()
    app.mainloop()
