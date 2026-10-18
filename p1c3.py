from pathlib import Path

from docling.datamodel import asr_model_specs
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import AsrPipelineOptions
from docling.document_converter import AudioFormatOption, DocumentConverter
from docling.pipeline.asr_pipeline import AsrPipeline

DATA_DIR = Path("data")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
asr_options = AsrPipelineOptions()
asr_options.asr_options = asr_model_specs.WHISPER_TURBO

converter = DocumentConverter(
    format_options={
        InputFormat.AUDIO: AudioFormatOption(
            pipeline_cls=AsrPipeline,
            pipeline_options=asr_options,
        )
    }
)


for path in DATA_DIR.rglob("*"):
    if path.is_file():
        source = path
        try:
            result = converter.convert(source)
            markdown = result.document.export_to_markdown()
        except Exception as e:
            print(
                f"Erreur lors de la conversion du fichier {source}: {e}")
            continue

        relative = path.relative_to(DATA_DIR)
        output_file = output_dir / relative.with_name(f"{source.name}.md")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown, encoding="utf-8")
        print(f"Fait: {output_file}")
