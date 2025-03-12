import copy

from pdf.src.Interfaces import Processor
from pdf.src.util import is_valid_json


class MessageProcessor(Processor):
    def __init__(self, image_descs, query):
        super().__init__()
        self.image_descs = image_descs
        self.query = query

    def process(self):
        messages = []
        json_data = is_valid_json('messages.json')

        if not json_data['is_valid']:
            error_msg = json_data['error_msg']
            raise ValueError(f'JSON is not formatted properly:{error_msg}')

        for image_path, width, height in self.image_descs:
            data = copy.deepcopy(json_data)
            data['data']['qwen_2.5_VL_72B_msgs'][1]['content'][1]['text'] = self.query
            data['data']['qwen_2.5_VL_72B_msgs'][1]['content'][0]['image'] = image_path
            data['data']['qwen_2.5_VL_72B_msgs'][1]['content'][0]['resized_height'] = width
            data['data']['qwen_2.5_VL_72B_msgs'][1]['content'][0]['resized_width'] = height
            messages.append(data['data']['qwen_2.5_VL_72B_msgs'])
        return messages