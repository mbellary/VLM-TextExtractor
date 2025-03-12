import os
import typer

from typing_extensions import Annotated, List
from pdf.src.factories import InferenceFactory
from pdf.src.proc.message_proc import MessageProcessor
from pdf.src.proc.pdf_proc import PDFProcessor
from pdf.src.proc.query_proc import QueryProcessor



def run(file_path: Annotated[str, typer.Option(help="The path to file for processing")] = None,
        query_path: Annotated[str, typer.Option(help='Path to query file.')] = None,
        infer_engine: Annotated[str, typer.Option(help='Backend engine to run inference. - local/mlx/hf/cloud')] = None,
        infer_model: Annotated[str, typer.Option(help='model to perform inference.')] = None,
        infer_device: Annotated[str, typer.Option(help='type of device to run inference - cpu/gpu.')] = None):

    file_ext = os.path.splitext(file_path)[1][1:]
    pdf_processor = PDFProcessor(file_path)
    query_processor = QueryProcessor(query_path)
    query, query_schema = query_processor.process()

    if file_ext == 'pdf':
        num_images, image_descs, tempdir = pdf_processor.process()
        message_procr = MessageProcessor(image_descs, query)
        messages = message_procr.process()
        factory = InferenceFactory(infer_engine, infer_model, infer_device, messages)
        model = factory.get_instance()
        results = model.infer()
    else:
        ValueError('Supported File is - PDF')


if __name__ == "__main__" :
    typer.run(run)