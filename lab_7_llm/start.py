"""
Starter for demonstration of laboratory work.
"""
# pylint: disable= too-many-locals, undefined-variable, unused-import
from pathlib import Path

from config.constants import PROJECT_ROOT
from config.lab_settings import LabSettings
from lab_7_llm.main import (
    LLMPipeline,
    RawDataImporter,
    RawDataPreprocessor,
    report_time,
    TaskDataset,
    TaskEvaluator,
)


@report_time
def main() -> None:
    """
    Run the translation pipeline.
    """
    settings = LabSettings(PROJECT_ROOT / "lab_7_llm" / "settings.json")

    importer = RawDataImporter(settings.parameters.dataset)
    importer.obtain()

    if importer.raw_data is None:
        return None

    preprocessor = RawDataPreprocessor(importer.raw_data)
    preprocessor.transform()

    if preprocessor.data is None:
        return None

    dataset = TaskDataset(preprocessor.data.head(100))

    device = "cpu"
    batch_size = 64
    max_length = 120

    pipeline = LLMPipeline(settings.parameters.model, dataset, max_length, batch_size, device)
    pipeline.analyze_model()

    inference = pipeline.infer_dataset()
    output_path = Path(__file__).parent / "dist" / "predictions.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    inference.to_csv(output_path, index=False)

    evaluator = TaskEvaluator(output_path, settings.parameters.metrics)
    result = evaluator.run()
    print(result)
    assert result is not None, "Demo does not work correctly"

    return None


if __name__ == "__main__":
    main()
