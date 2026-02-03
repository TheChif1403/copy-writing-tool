import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import tempfile

# ===== Style =====
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='VocabTitle', fontSize=14, spaceAfter=6))
styles.add(ParagraphStyle(name='DotLine', fontSize=12, leading=18))

# ===== Hàm tạo 1 dòng chấm theo số lần lặp trong dòng =====
def dot_groups(word, per_line):
    clean_word = word.replace(" ", "")
    length = len(clean_word) * 3
    one_group = "." * length
    return (" " * 5).join([one_group] * per_line)

# ===== Block cho 1 từ =====
def vocab_block(word, meaning, lines, per_line):
    elements = []
    title = f"<b>{word}: {meaning}</b>"
    elements.append(Paragraph(title, styles['VocabTitle']))

    for _ in range(lines):
        elements.append(Paragraph(dot_groups(word, per_line), styles['DotLine']))

    elements.append(Spacer(1, 12))
    return elements

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

    vocab_list.append((eng, vie, lines, per_line))

# ===== Nút tạo PDF =====
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

        for word, meaning, lines, per_line in vocab_list:
            if word.strip():  # bỏ qua dòng trống
                story.extend(vocab_block(word, meaning, lines, per_line))

        doc.build(story)

        with open(tmp.name, "rb") as f:
            st.download_button("⬇ Tải PDF", f, file_name=f"{unit_name}_CopyWriting.pdf")