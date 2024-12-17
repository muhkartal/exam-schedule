import pandas as pd
import streamlit as st
from fpdf import FPDF
import os

# PDF Creation Function
def create_pdf(course_details_list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_top_margin(20)

    # Font setup
    font_path = "Github/exam-schedule/data/DejaVuSans.ttf"
    pdf.set_font("Arial", size=10)


    # Header with University Name
    pdf.set_font("Sans", size=14)
    pdf.cell(0, 10, txt="Halic Üniversitesi - Sınav Programı", ln=True, align="C")
    pdf.ln(5)

    # Table Header Styling
    pdf.set_fill_color(0, 51, 102)  # University official blue
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Sans", size=10)
    pdf.cell(35, 10, "Tarih", 1, 0, 'C', 1)
    pdf.cell(25, 10, "Başlangıç", 1, 0, 'C', 1)
    pdf.cell(25, 10, "Bitiş", 1, 0, 'C', 1)
    pdf.cell(45, 10, "Ders Kodu", 1, 0, 'C', 1)
    pdf.cell(60, 10, "Ders Adı", 1, 1, 'C', 1)

    # Table Rows
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Sans", size=10)
    for details in course_details_list:
        pdf.cell(35, 10, details['Tarih'], 1, 0, 'C')
        pdf.cell(25, 10, details['Saat Başlangıç'], 1, 0, 'C')
        pdf.cell(25, 10, details['Saat Bitiş'], 1, 0, 'C')
        pdf.cell(45, 10, details['Ders Kodu'].split(';')[0], 1, 0, 'C')
        pdf.multi_cell(60, 10, details['Ders Adı'].split(';')[0], 1, 'C')  # Multi-cell for clean display

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Sans", size=8)
    pdf.cell(0, 10, "Halic Üniversitesi - Sınav Programı", 0, 0, 'L')
    pdf.cell(0, 10, f"Sayfa {pdf.page_no()}", 0, 0, 'R')

    output_file = "sinav_programi.pdf"
    pdf.output(output_file)
    return output_file

# Streamlit App Configuration
st.set_page_config(page_title="Halic Üniversitesi Sınav Programı", layout="wide")

# CSS Styling
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            color: #004080;
            font-size: 36px;
            margin-top: 0;
        }
        .subtitle {
            color: #4F8BF9;
            text-align: center;
            font-size: 20px;
            margin-bottom: 30px;
        }
        .instructions {
            font-size: 16px;
            margin: 10px auto;
            text-align: center;
            color: #FFFFFF; /* White text color for clarity */
        }
        .card {
            padding: 20px;
            margin: 15px 0;
            background: #252526;
            color: #f4f4f9;
            border-radius: 8px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .card h4 {
            color: #4F8BF9;
            font-size: 18px;
        }
        .card p {
            margin: 5px 0;
            font-size: 14px;
        }
        .pdf-button-container {
            text-align: center;
            margin-top: 20px;
        }
        .pdf-success {
            color: green;
            text-align: center;
            margin-top: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.markdown("<h1 class='title'>Halic Üniversitesi Sınav Programı</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Sınav tarihlerinizi görüntüleyin ve PDF olarak kaydedin.</p>", unsafe_allow_html=True)

# Instructions for Users
st.markdown("<p class='instructions'>1. Tüm sınav programını görmek için aşağıdaki tabloyu inceleyin.<br>"
            "2. Yalnızca seçili derslerin programını görmek için dersleri seçin.<br>"
            "3. PDF oluştur butonu ile seçili dersleri PDF formatında indirebilirsiniz.</p>", unsafe_allow_html=True)

# File Loading
file_path = "Github/exam-schedule/data/exam_schedule.xlsx"
if os.path.exists(file_path):
    df = pd.read_excel(file_path)

    # Show Full Exam Schedule
    st.write("### Tüm Sınav Programı")
    st.dataframe(df)

    # Clean Ders Kodu
    df['Ders Kodu Clean'] = df[df.columns[3]].apply(lambda x: x.split(";")[0])

    # Course Selection
    unique_courses = df[['Ders Kodu Clean', df.columns[4]]].drop_duplicates()
    course_options = unique_courses.apply(
        lambda row: f"{row['Ders Kodu Clean']} - {row[df.columns[4]]}", axis=1
    ).tolist()

    st.write("### Derslerinizi Seçin")
    selected_courses = st.multiselect("Bir veya birden fazla ders seçin:", course_options, help="Seçilen derslere ait program PDF olarak kaydedilebilir.")

    if selected_courses:
        selected_course_codes = [course.split(" - ")[0] for course in selected_courses]
        filtered_courses = df[df['Ders Kodu Clean'].isin(selected_course_codes)]
        course_details_list = []

        for _, row in filtered_courses.iterrows():
            course_details_list.append({
                "Tarih": str(row[0]),
                "Saat Başlangıç": str(row[1]),
                "Saat Bitiş": str(row[2]),
                "Ders Kodu": str(row[3]),
                "Ders Adı": str(row[4]),
            })

        # Display Selected Courses as Cards
        st.write("### Seçili Derslerin Programı")
        for details in course_details_list:
            st.markdown(
                f"""
                <div class='card'>
                    <h4>{details['Ders Adı']} ({details['Ders Kodu'].split(';')[0]})</h4>
                    <p><strong>Tarih:</strong> {details['Tarih']}</p>
                    <p><strong>Başlangıç:</strong> {details['Saat Başlangıç']}</p>
                    <p><strong>Bitiş:</strong> {details['Saat Bitiş']}</p>
                </div>
                """, unsafe_allow_html=True
            )

        # Generate PDF
        st.markdown("<div class='pdf-button-container'>", unsafe_allow_html=True)
        if st.button("📄 PDF Oluştur ve İndir"):
            pdf_path = create_pdf(course_details_list)
            st.markdown("<p class='pdf-success'>PDF başarıyla oluşturuldu!</p>", unsafe_allow_html=True)
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 PDF'yi indir",
                    data=file,
                    file_name="sinav_programi.pdf",
                    mime="application/pdf"
                )
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error(f"Dosya bulunamadı: {file_path}. Lütfen dosya yolunu kontrol edin.")
