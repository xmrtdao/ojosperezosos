import torch
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
from PIL import Image

class SceneDescriber:
    """
    LLaVA-NeXT scene captioning optimized for AMD ROCm MI300X.
    Generates rich, accessibility-friendly descriptions.
    """
    def __init__(self, model_name="liuhaotian/llava-v1.6-vicuna-7b", device="cuda"):
        self.device = device
        self.processor = LlavaNextProcessor.from_pretrained(model_name)
        self.model = LlavaNextForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        if device == "cuda":
            self.model = torch.compile(self.model)

    def describe(self, image_path_or_pil, detail="standard"):
        if isinstance(image_path_or_pil, str):
            image = Image.open(image_path_or_pil).convert("RGB")
        else:
            image = image_path_or_pil

        prompts = {
            "brief": "USER: \u003cimage\u003e\nDescribe this scene in one sentence for a blind person.\nASSISTANT:",
            "standard": "USER: \u003cimage\u003e\nDescribe this scene in detail, including objects, colors, lighting, and spatial layout. Be helpful for someone with low vision.\nASSISTANT:",
            "rich": "USER: \u003cimage\u003e\nProvide a rich, vivid description of this scene. Mention colors, textures, lighting, objects, their positions, and the overall mood. Help a visually impaired person build a mental picture.\nASSISTANT:"
        }

        prompt = prompts.get(detail, prompts["standard"])
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=256, do_sample=False)

        caption = self.processor.decode(output[0], skip_special_tokens=True)
        # Extract assistant response
        if "ASSISTANT:" in caption:
            caption = caption.split("ASSISTANT:")[-1].strip()
        return caption

if __name__ == "__main__":
    describer = SceneDescriber()
    print(describer.describe("test_scene.jpg", detail="rich"))
