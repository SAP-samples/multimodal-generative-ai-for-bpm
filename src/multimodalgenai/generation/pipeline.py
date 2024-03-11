# functions that make the generation part more easily and scalable


from multimodalgenai.io import read_image_b64encoded
import json
from json.decoder import JSONDecodeError 
from jsonschema import validate, ValidationError
from multimodalgenai.bpmn_schema import bpmn_schema
from multimodalgenai.io import read_image_paths_from_index, write_generated_for_index
import re

  
def get_image_as_message_content(image_path):
    """Reads image from image_path and returns it as a message-content"""
    base64_image = read_image_b64encoded(image_path)
    return {
       "type": "image_url",
       "image_url": {
       "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }

def get_images_as_message_contents(images_paths):
    """Reads multiple images from image_paths and returns them as message-contents"""
    message_contents = []
    for image_path in images_paths:
        message_contents.append(get_image_as_message_content(image_path))
    return message_contents


def get_cleaned_response(LLM_response, validate_to_schema = True):
    """Parses a response from an LLM into a JSON structure and validates it to the BPMN schema if validate_to_schema is true"""
    cleaned_json_string = LLM_response.replace('```json', '').replace('```', '').strip()
    try:
        generated_json = json.loads(cleaned_json_string)
        if validate_to_schema: validate(instance=generated_json, schema=bpmn_schema)
    except ValidationError as e:
        print("Validation Error", e)
        return generated_json
    except JSONDecodeError as e:
        print("JSONDecodeError Error", e)
        print(cleaned_json_string)
        return cleaned_json_string
    
    return generated_json

def generate_for_index(LLM, LLM_method, i, save_as_file=False):
    """Generates a model for a given index. Loads the images from that index, calls the LLM_method with it,
    cleanes the response and saves it as a file if the flag is true"""
    image_paths = read_image_paths_from_index(i)
    images_as_message_contents = get_images_as_message_contents(image_paths)
    response = LLM_method(LLM, images_as_message_contents)
    cleaned_response = get_cleaned_response(response)
    if save_as_file: write_generated_for_index(cleaned_response, i, f"{LLM_method.__name__}")
    return cleaned_response

def text_content(text):
    """Transforms the text into a text-content"""
    return {"type": "text", "text": text}

def user_message(contents):
  """Transforms the contents into a user message"""
  return {
      "role": "user",
      "content": contents
    }

def system_message(contents):
  """Transforms the contents into a system message"""
  return {
      "role": "system",
      "content": contents
    }