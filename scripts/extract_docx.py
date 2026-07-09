import docx
import sys

def extract_text(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

if __name__ == "__main__":
    docx_path = r"c:\Users\NC\Music\trxt nullivance v14\docs\logic_tension_synthesis.docx"
    output_path = r"c:\Users\NC\Music\trxt nullivance v14\docs\logic_tension_synthesis_extracted.txt"
    try:
        text = extract_text(docx_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully extracted text to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
