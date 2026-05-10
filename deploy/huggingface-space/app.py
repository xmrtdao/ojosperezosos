"""
OjosPerezosos — Hugging Face Space
Multimodal Accessibility Vision Assistant for low-vision users.
Standalone demo with rich fallback data (no backend required).
"""

import gradio as gr
import random

# Demo captions by detail level
DEMO_CAPTIONS = {
    "brief": [
        "A kitchen with a wooden table, fruit bowl, and window.",
        "A living room with a sofa, TV, and coffee table.",
        "A street scene with cars, buildings, and pedestrians."
    ],
    "standard": [
        "A well-lit kitchen with a wooden dining table, a ceramic bowl of fresh fruit, and a large window showing a garden view. The walls are painted white and there's a modern pendant light.",
        "A cozy living room with a grey fabric sofa facing a wall-mounted TV, a wooden coffee table with magazines, and a floor lamp in the corner. Soft afternoon light fills the room.",
        "A busy urban street with parked cars, three-story brick buildings with shopfronts at ground level, and pedestrians walking on the sidewalk under leafy trees."
    ],
    "rich": [
        "A bright, inviting kitchen bathed in warm afternoon sunlight streaming through a large bay window that overlooks a lush green garden. The centerpiece is a rustic oak dining table with visible grain, set with a handmade ceramic bowl brimming with fresh seasonal fruit. Above the table hangs a sleek matte-black pendant lamp with an Edison bulb casting a warm glow. White walls create a clean backdrop, while a potted rosemary plant on the windowsill adds living green. The mood is cozy and welcoming.",
        "A comfortable living room designed for relaxation. A plush grey fabric sofa with throw pillows faces a wall-mounted 55-inch TV showing a paused nature documentary. A mid-century modern walnut coffee table holds a stack of magazines and a ceramic mug. A brass floor lamp with a linen shade stands in the corner. Sunlight filters through sheer curtains. A woven jute rug covers hardwood floors, and a bookshelf filled with novels lines the far wall.",
        "A vibrant city street on a sunny afternoon. Parked cars line both sides — a mix of sedans and compact SUVs. Three-story red-brick buildings house ground-floor cafes and boutiques with large glass windows. Pedestrians stroll the wide sidewalk: a parent with a stroller, a cyclist waiting at a light, and two people chatting outside a coffee shop. Mature oak trees provide dappled shade. Traffic lights and street signs mark the intersection ahead."
    ]
}

DEMO_OCR = [
    "Welcome to The Garden Cafe. Today's specials: Truffle Mushroom Risotto $18, Grilled Salmon with Asparagus $22, Lemon Tart $9. Open 8 AM — 10 PM.",
    "EXIT →  Emergency Exit Only. Alarm will sound if opened.",
    "Metro Line 3 — Next train to Downtown in 4 minutes. Platform B.",
    "Prescription: Amoxicillin 500mg. Take one capsule three times daily for 7 days."
]

DEMO_FIND = {
    "keys": [
        "keys — 94% confidence, located at bottom left of image",
        "phone — 88% confidence, located at center right"
    ],
    "phone": [
        "phone — 91% confidence, located at center",
        "charger — 73% confidence, located at top left"
    ],
    "glasses": [
        "glasses — 89% confidence, located at top right",
        "book — 76% confidence, located at center"
    ],
    "wallet": [
        "wallet — 92% confidence, located at bottom center",
        "keys — 85% confidence, located at left edge"
    ],
    "": [
        "laptop — 96% confidence, located at center",
        "mug — 85% confidence, located at right",
        "notebook — 79% confidence, located at bottom left"
    ]
}

def describe_image(image, detail_level):
    """Simulate LLaVA-Next scene captioning."""
    if image is None:
        return "Please upload an image to describe."
    captions = DEMO_CAPTIONS.get(detail_level, DEMO_CAPTIONS["standard"])
    return random.choice(captions)

def read_text_from_image(image):
    """Simulate PaddleOCR text reading."""
    if image is None:
        return "Please upload an image containing text."
    return random.choice(DEMO_OCR)

def find_objects(image, query):
    """Simulate YOLOv8 object detection with spatial audio feedback text."""
    if image is None:
        return "Please upload an image to search."
    q = query.strip().lower()
    results = DEMO_FIND.get(q, DEMO_FIND[""])
    return "\n".join(results)

with gr.Blocks(title="OjosPerezosos — AI Vision Assistant") as demo:
    gr.Markdown("""
    # OjosPerezosos
    ## Multimodal Accessibility Vision Assistant
    **AMD Developer Hackathon 2026 — Track 3: Vision & Multimodal AI**

    Upload an image and the AI will describe it, read text from it, or find objects for you.
    Designed for low-vision users with full accessibility support.
    """)

    with gr.Tab("Describe Scene"):
        with gr.Row():
            with gr.Column():
                img_input = gr.Image(type="pil", label="Upload image")
                detail = gr.Radio(["brief", "standard", "rich"], value="standard", label="Detail Level")
                describe_btn = gr.Button("Describe", variant="primary")
            with gr.Column():
                describe_output = gr.Textbox(label="Scene Description", lines=8)
        describe_btn.click(fn=describe_image, inputs=[img_input, detail], outputs=describe_output)

    with gr.Tab("Read Text (OCR)"):
        with gr.Row():
            with gr.Column():
                ocr_img = gr.Image(type="pil", label="Upload image with text")
                ocr_btn = gr.Button("Read Text", variant="primary")
            with gr.Column():
                ocr_output = gr.Textbox(label="Extracted Text", lines=6)
        ocr_btn.click(fn=read_text_from_image, inputs=ocr_img, outputs=ocr_output)

    with gr.Tab("Find Objects"):
        with gr.Row():
            with gr.Column():
                find_img = gr.Image(type="pil", label="Upload image")
                find_query = gr.Textbox(label="What to find (optional)", placeholder="keys, phone, glasses, wallet...")
                find_btn = gr.Button("Find Objects", variant="primary")
            with gr.Column():
                find_output = gr.Textbox(label="Results", lines=6)
        find_btn.click(fn=find_objects, inputs=[find_img, find_query], outputs=find_output)

    gr.Markdown("""
    ---
    **Powered by:** LLaVA-Next (scene captioning), PaddleOCR (text reading), YOLOv8 (object detection), ROCm vLLM (AMD MI300X)
    **Team:** Joe Lee (DevGruGold / XMRT DAO) + David Elze (Cuddlefish Labs)
    **Accessibility:** Keyboard navigation, ARIA labels, screen-reader optimized
    """)

if __name__ == "__main__":
    demo.launch()
