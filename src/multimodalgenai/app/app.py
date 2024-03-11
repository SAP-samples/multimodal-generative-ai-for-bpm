from flask import Flask, render_template, request
import json
import time
from multimodalgenai.generation.LLM import ChatGPT_private_subscription
from multimodalgenai.generation.few_shot import few_shot
from multimodalgenai.generation.pipeline import get_images_as_message_contents, get_cleaned_response
import pypdfium2 as pdfium
import os
from pathlib import Path

app = Flask(__name__)
LLM = ChatGPT_private_subscription()

# Placeholder function for your JSON generation logic
def generate_json_from_document(file):

    # transforming document into images
    pdf = pdfium.PdfDocument(file)
    n_pages = len(pdf)
    print(f"Extracting {n_pages} pages from entry")
    image_paths = []
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        pil_image = page.render(scale=300/72).to_pil()
        filename = Path(os.getcwd()) / "src" / "multimodalgenai" / "app" / "tmp" / f"process_documentation_page_{page_number}.png"
        image_paths.append(filename)
        pil_image.save(filename)

    
    # generate json, takes up to one minute
    images_as_message_contents = get_images_as_message_contents(image_paths)
    response = few_shot(LLM, images_as_message_contents)
    cleaned_response = get_cleaned_response(response)
    return cleaned_response

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if (request.method == 'POST') and ('file' in request.files) and (request.files['file']):
        file =  request.files['file']
        # Call your function to process the file
        json_result = generate_json_from_document(file)
        return render_template('upload.html', json_result=json.dumps(json_result, indent=4))
    return render_template('upload.html', json_result=None)

if __name__ == '__main__':
    app.run(debug=True)