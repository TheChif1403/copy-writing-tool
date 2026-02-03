import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile

# ===== FONT TIẾNG VIỆT =====
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

# ===== STYLE PDF =====
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='UnitTitle', fontName='DejaVu', fontSize=18, alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name='VocabTitle', fontName='DejaVu', fontSize=14, spaceAfter=6))
styles.add(ParagraphStyle(name='DotLine', fontName='DejaVu', fontSize=13, leading=19.5))

# ===== TẠO DÒNG CHẤM =====
def dot_groups(word, per_line, space_count):
    clean_word = word.replace(" ", "")
    length = len(clean_word) * 3
    one_group = "." * length
    spaces = " " * space_count
    return spaces.join([one_group] * per_line)

# ===== GIAO DIỆN =====
st.title("📘 Tạo File Luyện Viết Từ Vựng Cho Bé")

unit_name = st.text_input("Tên Unit")
num_words = st.number_input("Số từ vựng", min_value=1, step=1)

preview_data = []

for i in range(int(num_words)):
    st.markdown(f"### Từ {i+1}")
    col1, col2 = st.columns(2)
    eng = col1.text_input(f"Tiếng Anh {i+1}")
    vie = col2.text_input(f"Nghĩa {i+1}")

    col3, col4 = st.columns(2)
    lines = col3.number_input(f"Số dòng viết từ {i+1}", min_value=1, step=1, value=3)
    per_line = col4.number_input(f"Mỗi dòng có mấy cụm từ {i+1}", min_value=1, step=1, value=3)

    space_count = st.number_input(f"Số khoảng trắng giữa các cụm của từ {i+1}", min_value=1, step=1, value=5)

    preview_data.append((eng, vie, lines, per_line, space_count))

# ===== XEM TRƯỚC =====
st.markdown("---")
st.subheader("👀 Xem trước nội dung")

for word, meaning, lines, per_line, space_count in preview_data:
    if word.strip():
        st.markdown(f"**{word}: {meaning}**")
        for _ in range(lines):
            st.text(dot_groups(word, per_line, space_count))

# ===== TẠO PDF =====
if st.button("📄 Tạo và tải file PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        doc_pdf = SimpleDocTemplate(tmp_pdf.name, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)

        story = []
        story.append(Paragraph(f"Unit: {unit_name}", styles['UnitTitle']))
        story.append(Paragraph("<b>VOCABULARY</b>", styles['Heading2']))
        story.append(Spacer(1, 12))

        for word, meaning, lines, per_line, space_count in preview_data:
            if word.strip():
                story.append(Paragraph(f"<b>{word}: {meaning}</b>", styles['VocabTitle']))
                for _ in range(lines):
                    story.append(Paragraph(dot_groups(word, per_line, space_count), styles['DotLine']))
                story.append(Spacer(1, 12))

        doc_pdf.build(story)

    with open(tmp_pdf.name, "rb") as f:
        st.download_button("⬇ Tải PDF", f, file_name=f"{unit_name}_CopyWriting.pdf")