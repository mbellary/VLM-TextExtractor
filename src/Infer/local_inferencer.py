
from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from pdf.src.Interfaces import VisionLangInferencer


class LocalInferencer(VisionLangInferencer):
    def __init__(self, model_name, device_type, messages):
        super().__init__()
        self.model_name  = model_name
        self.device_type = device_type
        self.messages = messages
        self._configure()

    def _configure(self):
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(self.model_name, torch_dtype=torch.float16, device_map="cuda")
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        print(f'loaded model and processor.')

    def infer(self):
        results = []
        print(f'starting inference...')
        for message in self.messages:
            print(type(message))
            print(f'message format : {message}')
            text = self.processor.apply_chat_template(
                        message, tokenize=False, add_generation_prompt=True)

            image_inputs, video_inputs = process_vision_info(message)

            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            ).to(self.device_type)
            #inputs = inputs.to(self.device_type)
            print(f'read inputs...')

            generated_ids = self.model.generate(**inputs, max_new_tokens=4096)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            raw_output = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )

            results.append(raw_output[0])

        return results