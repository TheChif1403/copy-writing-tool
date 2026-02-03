import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from docx import Document
import tempfile

# ===== Style PDF =====
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='VocabTitle', fontSize=14, spaceAfter=6))
styles.add(ParagraphStyle(name='DotLine', fontSize=13, leading=19.5))  # line spacing 1.5

# ===== Hàm tạo dòng chấm =====
def dot_groups(word, per_line, space_count):
    clean_word = word.replace(" ", "")
    length = len(clean_word) * 3
    one_group = "." * length
    spaces = " " * space_count
    return spaces.join([one_group] * per_line)

# ===== Block PDF =====
def vocab_block_pdf(word, meaning, lines, per_line, space_count):
    elements = []
    title = f"<b>{word}: {meaning}</b>"
    elements.append(Paragraph(title, styles['VocabTitle']))

    for _ in range(lines):
        elements.append(Paragraph(dot_groups(word, per_line, space_count), styles['DotLine']))

    elements.append(Spacer(1, 12))
    return elements

# ===== Block Word =====
def vocab_block_word(doc, word, meaning, lines, per_line, space_count):
    doc.add_paragraph(f"{word}: {meaning}").runs[0].bold = True
    for _ in range(lines):
        p = doc.add_paragraph(dot_groups(word, per_line, space_count))
        p.paragraph_format.line_spacing = 1.5

# ===== Giao diện =====
st.title("📘 Tạo File Luyện Viết Từ Vựng Cho Bé")

unit_name = st.text_input("Tên Unit")
num_words = st.number_input("Số từ vựng", min_value=1, step=1)

vocab_list = []

for i in range(int(num_words)):
    st.markdown(f"### Từ {i+1}")
    col1, col2 = st.columns(2)
    eng = col1.text_input(f"Tiếng Anh {i+1}")
    vie = col2.text_input(f"Nghĩa {i+1}")

    col3, col4 = st.columns(2)
    lines = col3.number_input(f"Số dòng viết từ {i+1}", min_value=1, step=1, value=3)
    per_line = col4.number_input(f"Mỗi dòng có mấy lần viết từ {i+1}", min_value=1, step=1, value=3)

    space_count = st.number_input(f"Số khoảng trắng giữa các cụm của từ {i+1}", min_value=1, step=1, value=5)

    vocab_list.append((eng, vie, lines, per_line, space_count))

# ===== TẠO FILE =====
if st.button("📄 Tạo file PDF & Word"):
    # ===== PDF =====
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        doc_pdf = SimpleDocTemplate(tmp_pdf.name, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)

        story = []
        story.append(Paragraph(f"<b>Unit: {unit_name}</b>", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>VOCABULARY</b>", styles['Heading2']))
        story.append(Spacer(1, 12))

        for word, meaning, lines, per_line, space_count in vocab_list:
            if word.strip():
                story.extend(vocab_block_pdf(word, meaning, lines, per_line, space_count))

        doc_pdf.build(story)

    # ===== WORD =====
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_word:
        doc_word = Document()
        doc_word.add_heading(f"Unit: {unit_name}", level=1)
        doc_word.add_paragraph("VOCABULARY").runs[0].bold = True

        for word, meaning, lines, per_line, space_count in vocab_list:
            if word.strip():
                vocab_block_word(doc_word, word, meaning, lines, per_line, space_count)

        doc_word.save(tmp_word.name)

    # ===== Nút tải =====
    with open(tmp_pdf.name, "rb") as f:
        st.download_button("⬇ Tải PDF", f, file_name=f"{unit_name}_CopyWriting.pdf")

    with open(tmp_word.name, "rb") as f:
        st.download_button("⬇ Tải Word (.docx)", f, file_name=f"{unit_name}_CopyWriting.docx")
