import os
import tempfile

from pdf2image import convert_from_path
from pdf.src.Interfaces import Processor
from pdf.src.proc.image_proc import ImageProcessor


class PDFProcessor(Processor):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def process(self):
        tempdir = tempfile.mkdtemp()
        image_files = []
        images = convert_from_path(self.file_path)
        file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        image_procr = ImageProcessor(images)
        images_proc = image_procr.process()
        print(f'processed images : {len(images_proc)}')

        for i, (image, width, height) in enumerate(images_proc):
            image_filename = os.path.join(tempdir, f'{file_name}_page_{i}.jpg')
            image.save(image_filename, 'JPEG')
            image_files.append((image_filename, width, height))
        return len(images), image_files, tempdir