import os
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

class TextReader:
    """
    PaddleOCR-based text extraction optimized for AMD ROCm.
    Reads text from images for accessibility TTS pipeline.
    """
    def __init__(self, lang="en", use_gpu=True):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang=lang,
            use_gpu=use_gpu,
            show_log=False
        )

    def read(self, image_path_or_pil):
        if isinstance(image_path_or_pil, str):
            img = Image.open(image_path_or_pil).convert("RGB")
        else:
            img = image_path_or_pil

        # Convert PIL to numpy array
        img_np = np.array(img)
        result = self.ocr.ocr(img_np, cls=True)

        lines = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                confidence = line[1][1]
                if confidence > 0.75:
                    lines.append(text)

        return {
            "full_text": " ".join(lines),
            "lines": lines,
            "line_count": len(lines)
        }

if __name__ == "__main__":
    reader = TextReader(use_gpu=True)
    result = reader.read("test_menu.jpg")
    print(f"Detected {result['line_count']} lines:")
    print(result["full_text"])
