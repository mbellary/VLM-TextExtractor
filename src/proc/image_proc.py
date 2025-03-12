from typing import List
from pdf.src.Interfaces import Processor


class ImageProcessor(Processor):
    def __init__(self, images):
        super().__init__()
        self.images = images

    def process(self) -> List[tuple]:
        max_width = 1250
        max_height = 1750
        images = []
        images_resized = []
        for image in self.images:
            width, height = image.size

            if width > max_width or height > max_height:
                aspect_ratio = width / height
                new_width = min(max_width, int(max_height * aspect_ratio))
                new_height = min(max_height, int(max_width / aspect_ratio))
                images.append((image, new_width, new_height))
            else:
                images.append((image, width, height))
        return images