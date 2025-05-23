from pymupdf import Document
from unicodedata import normalize
from re import sub
from typing import Generator, Tuple


class PDFTextRipper:
    _pdf: bytes

    def __init__(self, pdf: bytes):
        self._pdf = pdf

    def __iter__(self) -> Generator[Tuple[bool, str], None, None]:
        doc = Document(stream=self._pdf)
        for page in doc:
            page_data = page.get_text("dict")
            blocks = page_data["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for content in self._process_text_block(block):
                        yield False, content
                if block["type"] == 1:
                    yield True, block["image"]

    def _from_fullwidth_to_halfwidth(self, content: str):
        table = {
            **{
                ord(f): ord(t)
                for f, t in zip(
                    map(chr, range(0xFF01, 0xFF5F)), map(chr, range(0x21, 0x7F))
                )
            },
            0x3000: 0x20,  # 全形空白
            0x2027: ord("."),  # 中點符號 ‧
            0x30FB: ord("."),  # 日文中點 ・
        }
        return content.translate(table)

    def _process_text_block(self, block):
        for line in block["lines"]:
            for span in line["spans"]:
                text: str = span["text"]
                normalized = sub(r"\((.)\)", r"\1", normalize("NFKD", text))
                halfwidthed = self._from_fullwidth_to_halfwidth(normalized)
                content = halfwidthed.strip()
                if content:
                    yield content
