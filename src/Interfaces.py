from abc import ABC, abstractmethod


class Inferencer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _configure(self):
        pass

class VisionLangInferencer(Inferencer):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def infer(self):
        pass

class Processor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self):
        pass