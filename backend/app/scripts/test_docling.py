from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions,AcceleratorOptions

# 1. Turn off the heavy enrichments that usually cause the hang
pipeline_options = PdfPipelineOptions()

pipeline_options.accelerator_options = AcceleratorOptions(device="cpu")
# 2. Initialize with restricted options
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

# 3. Try a single conversion
result = converter.convert("/home/ayman-ing/study/projects/CAIV/backend/app/scripts/FekiAymanCV.pdf")
print(result.document.export_to_markdown())