from sapsam import constants
import json
import base64
import os
import pandas as pd

def read_image_b64encoded(image_path):
  """ Reads the image and returns it base64 encoded """
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def read_ground_truth_from_index(i):
    """ Returns the ground truth model from index i"""
    with open(constants.DATA_ROOT / "cleaned" / f"{i}_ground_truth.json") as f:
      return json.loads(f.read())
    
def read_generated_from_index(i, method):
    """ Returns the generated model from index i"""
    with open(constants.DATA_ROOT / "generated" / f"{i}_generated_{method}.json") as f:
      return json.loads(f.read())
    
def read_image_paths_from_index(i):
    """ Returns all image paths of the process documentation from index i"""
    image_paths = []
    page_number = 0
    while os.path.exists(constants.DATA_ROOT / "cleaned" / f"{i}_process_documentation_page_{page_number}.png"):
        print("")
        image_paths.append(constants.DATA_ROOT / "cleaned" / f"{i}_process_documentation_page_{page_number}.png")
        page_number = page_number + 1
    return image_paths

def write_generated_for_index(generated, i, method):
    """ Saves the generated model for an index and a method name in a file"""
    filename = constants.DATA_ROOT / "generated" / f"{i}_generated_{method}.json"
    with open(filename, 'w') as f:
        json.dump(generated, f, indent=4)

def write_evaluations(df_results, method):
   """ Saves the evaluations in a pickle for a method name"""
   df_results.to_pickle(constants.DATA_ROOT / "evaluations" / f"{method}_evaluation.pkl")

def read_evaluations(method):
   """ Reads the evaluations from a pickle for a method name"""
   return pd.read_pickle(constants.DATA_ROOT / "evaluations" / f"{method}_evaluation.pkl")