from taiwan_geodoc_hub.infrastructure.utils.helpers.documents.pdf_text_ripper import (
    PDFTextRipper,
)
from taiwan_geodoc_hub.modules.registration_managing.exceptions.invalid_pdf import (
    InvalidPDF,
)


def validate_snapshot(pdf: bytes):
    if not pdf.startswith(b"%PDF-"):
        raise InvalidPDF()
    pdf_text_ripper = PDFTextRipper(pdf)
    for is_image, _ in pdf_text_ripper:
        if is_image:
            continue
        return
    raise InvalidPDF()
