import os
import uvicorn

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import markdown
from pathlib import Path

from pydantic import BaseModel
from typing import List
from transformers import pipeline

from check_numeric import check_numeric
from check_rules import check_rules

header_classifier = pipeline("text-classification", model="./sensitive-header")
content_classifier = pipeline("text-classification", model="./sensitive-content")

app = FastAPI()

class SingleModelInput(BaseModel):
    header: List[str]

class DualModelInput(BaseModel):
    header: List[str]
    content: List[List[str]]

class OutputData(BaseModel):
    labels: List[str]

def count_digits_space(s):
    return sum(1 for char in s if char.isdigit()), sum(1 for char in s if char.isspace())

def classify_advanced(input_data):
    classifications = []
    
    for item in input_data:
        classification = content_classifier(item)
        classifications.append(classification[0]['label'])
    
    counts = {}
    for classification in classifications:
        if classification in counts:
            counts[classification] += 1
        else:
            counts[classification] = 1
    
    max_count = max(counts.values())
    candidates = [key for key, value in counts.items() if value == max_count]
    
    if len(candidates) > 1:
        result = max(candidates)
    else:
        result = candidates[0]
    return result

@app.post("/classify", response_model=OutputData)
async def classify_single(data: SingleModelInput):
    predictions = header_classifier(data.header)
    labels = [pred["label"] for pred in predictions]
    return OutputData(labels=labels)

@app.post("/classify_advanced", response_model=OutputData)
async def classify_dual(data: DualModelInput):
    prediction1 = header_classifier(data.header)
    labels = [pred["label"] for pred in prediction1]
    predictions = []
    for i in range(len(labels)):
        if labels[i] == "LABEL_0" or labels[i] == "LABEL_2":
            columnData = set()
            for item in data.content[i]:
                if item != '' or item != None:
                    columnData.add(item)
                    if len(columnData) > 3:
                        break
            columnData1 = list(columnData)[0]
            numeric = check_numeric(columnData1)
            rules = check_rules(columnData1)
            if count_digits_space(columnData)[1] == 0 and count_digits_space(columnData)[0] >= 5:
                prediction = numeric
            elif rules != -1:
                prediction = rules
            else:
                prediction = classify_advanced(columnData)

            predictions.append(prediction)
        else:
            predictions.append(labels[i])
    return OutputData(labels=predictions)

def get_readme_html():
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
            return markdown.markdown(markdown_content)
    return "<h1>README.md not found</h1>"

def get_readme_html():
    with open("README.md", "r", encoding="utf-8") as md_file:
        md_content = md_file.read()
    
    html_content = markdown.markdown(
        md_content, 
        extensions=["fenced_code", "codehilite"]
    )
    
    with open("styles.css", "r", encoding="utf-8") as css_file:
        css_content = css_file.read()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>API Documentation</title>
        <style>{css_content}</style>
        <script>hljs.highlightAll();</script>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def readme():
    html_content = get_readme_html()
    return HTMLResponse(content=html_content, status_code=200)

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run(app, host="0.0.0.0", port=port)