from multimodalgenai.bpmn_schema import bpmn_schema

## Meta prompt which is used as a basis in zero, one and few shot prompting.

meta_prompt = """### Instruction ###
  You are a BPMN expert. Your task is to extract process information out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. Make sure that you include the sequence and message flow. 
  Use numbers for the ids starting from zero. Generate json according to the following schema for extracting the process information. 
  Only output the generated json.
  
  ### Schema ###
  """ + str(bpmn_schema)