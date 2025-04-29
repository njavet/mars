from pathlib import Path
from docx import Document

# project imports
from mars.service.bot import Bot


def run_eval():
    bot = Bot()


def read_docx(docx_path: Path):
    doc = Document(docx_path.name)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


if __name__ == '__main__':
    run_eval()
