import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    takes the path of a pdf file and returns all the text found inside it
    """

    all_text = ""

    pdf_file = open(pdf_path, "rb")
    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            all_text = all_text + page_text + "\n"

    pdf_file.close()

    return all_text