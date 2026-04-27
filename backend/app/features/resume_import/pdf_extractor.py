from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions
from pathlib import Path


class PDFExtractor:
    """Extract text from PDF using Docling."""

    def __init__(self):
        # Configure pipeline options for CPU
        pipeline_options = PdfPipelineOptions()
        pipeline_options.accelerator_options = AcceleratorOptions(device="cpu")

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    async def extract_text(self, pdf_path: str | Path) -> str:
        """Extract text from PDF file."""
        import asyncio

        def blocking_convert():
            result = self.converter.convert(str(pdf_path))
            return result.document.export_to_markdown()

        return await asyncio.to_thread(blocking_convert)
