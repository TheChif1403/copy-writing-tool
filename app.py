import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='VocabTitle', fontSize=14, spaceAfter=6))
styles.add(ParagraphStyle(name='DotLine', fontSize=12, leading=18))

def dot_line_by_word(word):
    length = len(word.replace(" ", "")) * 3
    one_group = "." * length
    return f"{one_group}     {one_group}     {one_group}"


def vocab_block(word, meaning, repeat):
    elements = []
    title = f"<b>{word}: {meaning}</b>"
    elements.append(Paragraph(title, styles['VocabTitle']))

    for _ in range(repeat):
        elements.append(Paragraph(dot_line_by_word(word), styles['DotLine']))

    elements.append(Spacer(1, 12))
    return elements


st.title("📘 Tạo File Luyện Viết Từ Vựng Cho Bé")

unit_name = st.text_input("Tên Unit")
num_words = st.number_input("Số từ vựng", min_value=1, step=1)
repeat_count = st.number_input("Mỗi từ copy bao nhiêu dòng?", min_value=1, step=1, value=3)


vocab_list = []

for i in range(int(num_words)):
    col1, col2 = st.columns(2)
    eng = col1.text_input(f"Tiếng Anh {i+1}")
    vie = col2.text_input(f"Nghĩa {i+1}")
    vocab_list.append((eng, vie))

if st.button("📄 Tạo file PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        doc = SimpleDocTemplate(tmp.name, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        story = []
        story.append(Paragraph(f"<b>Unit: {unit_name}</b>", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>VOCABULARY</b>", styles['Heading2']))
        story.append(Spacer(1, 12))

        for word, meaning in vocab_list:
            story.extend(vocab_block(word, meaning, repeat_count))


        doc.build(story)

        with open(tmp.name, "rb") as f:
            st.download_button("⬇ Tải PDF", f, file_name=f"{unit_name}_CopyWriting.pdf")
