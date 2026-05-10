import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image

class ObjectFinder:
    """
    YOLOv8 object detection for accessibility.
    Finds objects in a scene and reports their relative positions.
    """
    def __init__(self, model_name="yolov8n.pt", device="cuda"):
        self.device = device
        self.model = YOLO(model_name)
        self.model.to(device)
        # COCO classes we care about for daily accessibility
        self.priority_classes = [
            "person", "bottle", "cup", "chair", "couch", "bed",
            "dining table", "door", "laptop", "mouse", "remote",
            "keyboard", "cell phone", "book", "clock", "vase",
            "scissors", "teddy bear", "hair drier", "toothbrush",
            "knife", "spoon", "bowl", "refrigerator", "microwave",
            "oven", "toaster", "sink", "handbag", "suitcase",
            "backpack", "umbrella", "shoe"
        ]

    def find(self, image_path_or_pil, query=None):
        if isinstance(image_path_or_pil, str):
            img = Image.open(image_path_or_pil).convert("RGB")
        else:
            img = image_path_or_pil

        results = self.model(img, verbose=False)
        detections = []
        w, h = img.size

        for box in results[0].boxes:
            cls_id = int(box.cls)
            name = self.model.names[cls_id]
            conf = float(box.conf)
            if conf < 0.5:
                continue
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            position = self._describe_position(cx, cy, w, h)
            detections.append({
                "name": name,
                "confidence": round(conf, 3),
                "position": position,
                "bbox": [round(x1), round(y1), round(x2), round(y2)]
            })

        if query:
            query_lower = query.lower()
            detections = [d for d in detections if query_lower in d["name"].lower()]

        return {
            "total": len(detections),
            "query": query,
            "objects": detections
        }

    def _describe_position(self, cx, cy, w, h):
        h_pos = "left" if cx < w * 0.35 else "right" if cx > w * 0.65 else "center"
        v_pos = "top" if cy < h * 0.35 else "bottom" if cy > h * 0.65 else "middle"
        return f"{v_pos} {h_pos}"

if __name__ == "__main__":
    finder = ObjectFinder()
    # General scan
    print(finder.find("test_room.jpg"))
    # Query scan
    print(finder.find("test_room.jpg", query="keys"))
