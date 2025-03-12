


class InferenceFactory:
    def __init__(self, engine_name, model_name, device_type, messages):
        self.engine_name = engine_name
        self.model_name  = model_name
        self.device_type = device_type
        self.messages = messages

    def get_instance(self):
        if self.engine_name.lower() == 'local':
            return LocalInferencer(self.model_name, self.device_type, self.messages)