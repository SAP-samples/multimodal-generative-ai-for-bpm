# Idea of the Chain-Of-Thought approach is to prompt the LLM multiple times with smaller tasks and chain them together 
# so that it can achive a bigger tasks by completing smaller tasks after each other.


### General setup #######################################################################

from multimodalgenai.generation.pipeline import user_message, system_message, text_content, get_image_as_message_content, get_images_as_message_contents, get_cleaned_response
from multimodalgenai.io import read_ground_truth_from_index, read_image_paths_from_index, write_generated_for_index
from sapsam import constants
from multimodalgenai.bpmn_schema import bpmn_schema


# instructions for introducing the fewshot examples
instruction_example_1  = """### Examples ###
Use the following image json pairs as an example

### Example 1 ###
"""

instruction_example_2  = "### Example 2 ###\n"
instruction_example_3  = "### Example 3 ###\n"
instruction_user = """### User Input ###
Now create the json based on these images
"""
  
# few shot examples
image_path_example1 = constants.DATA_ROOT / "cleaned" / f"0_process_documentation_page_3.png"
image_path_example2 = constants.DATA_ROOT / "cleaned" / f"1_process_documentation_page_3.png"
image_path_example3 = constants.DATA_ROOT / "cleaned" / f"2_process_documentation_page_3.png"
image_as_content_example1 = get_image_as_message_content(image_path_example1)
image_as_content_example2 = get_image_as_message_content(image_path_example2)
image_as_content_example3 = get_image_as_message_content(image_path_example3)
ground_truth_example1 = read_ground_truth_from_index(0)
ground_truth_example2 = read_ground_truth_from_index(1)
ground_truth_example3 = read_ground_truth_from_index(2)



### Tasks  #######################################################################
def chain_of_thoughts_tasks(LLM, message_contents):
  """Prompts the LLM to generate tasks from the process documentation passed as message_contents"""

  instruction_tasks = """### Instruction ###
  You are a BPMN expert. Your task is to extract tasks/activities out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. 
  Use numbers for the ids starting from zero. Generate json according to the following schema for extracting the task information. 
  Only include the tasks and ignore other elements like gateways, events etc.
  Only output the list of tasks as json.
  
  ### Schema ###
  """
  instruction_tasks += str(bpmn_schema["$defs"]["task"])
  
  # TODO change order
  messages=[system_message(instruction_tasks), user_message(message_contents)]

  messages=[
      system_message([
        text_content(instruction_tasks),

        text_content(instruction_example_1),
        image_as_content_example1,
        text_content(str(ground_truth_example1["tasks"])),

        text_content(instruction_example_2),
        image_as_content_example2,
        text_content(str(ground_truth_example2["tasks"])),

        text_content(instruction_example_3),
        image_as_content_example3,
        text_content(str(ground_truth_example3["tasks"])),
      ]),
      user_message([text_content(instruction_user)] + message_contents)
  ]

  return LLM.ask(messages)

### Events  #######################################################################
def chain_of_thoughts_events(LLM, message_contents):
  """Prompts the LLM to generate events from the process documentation passed as message_contents"""

  instruction_events = """### Instruction ###
  You are a BPMN expert. Your task is to extract events out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. 
  Use numbers for the ids starting from zero. Generate json according to the following schema for extracting the events. 
  Only include the events and ignore other elements like tasks, gateways etc.
  Only output the generated list of events as json.
  
  ### Schema ###
  """
  instruction_events += str(bpmn_schema["$defs"]["event"])
  
  # TODO change order
  messages=[system_message(instruction_events), user_message(message_contents)]

  messages=[
      system_message([
        text_content(instruction_events),

        text_content(instruction_example_1),
        image_as_content_example1,
        text_content(str(ground_truth_example1["events"])),

        text_content(instruction_example_2),
        image_as_content_example2,
        text_content(str(ground_truth_example2["events"])),

        text_content(instruction_example_3),
        image_as_content_example3,
        text_content(str(ground_truth_example3["events"])),
      ]),
      user_message([text_content(instruction_user)] + message_contents)
  ]

  return LLM.ask(messages)


### Gateways  #######################################################################
def chain_of_thoughts_gateways(LLM, message_contents):
  """Prompts the LLM to generate gateways from the process documentation passed as message_contents"""

  instruction_gateways = """### Instruction ###
  You are a BPMN expert. Your task is to extract gateways out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. 
  Use numbers for the ids starting from zero. Generate json according to the following schema for extracting the gateways. 
  Only include the gateways and ignore other elements like tasks, events etc.
  Only output the generated list of gateways as json.
  
  ### Schema ###
  """
  instruction_gateways += str(bpmn_schema["$defs"]["gateway"])
  
  messages=[system_message(instruction_gateways), user_message(message_contents)]

  messages=[
      system_message([
        text_content(instruction_gateways),

        text_content(instruction_example_1),
        image_as_content_example1,
        text_content(str(ground_truth_example1["gateways"])),

        text_content(instruction_example_2),
        image_as_content_example2,
        text_content(str(ground_truth_example2["gateways"])),

        text_content(instruction_example_3),
        image_as_content_example3,
        text_content(str(ground_truth_example3["gateways"])),
      ]),
      user_message([text_content(instruction_user)] + message_contents)
  ]

  return LLM.ask(messages)

import json


### Pools  #######################################################################
schema_pools = {
    "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "lanes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string" },
                    "name": { "type": "string" },
                    "elemRefs": {
                        "type": "array",
                        "items": { "type": "string" }
                    }
                },
                "required": ["id", "name", "elemRefs"],
                "description": "Lanes subdivide pools hierarchically for example different roles or departements.",
            }
        }
    },
    "required": ["id", "name", "lanes"],
    "description": "Organization or role who performs the tasks",
}

def get_tasks_events_gateways_only(bpmn_instance):
  return {
    "tasks": bpmn_instance["tasks"],
    "events": bpmn_instance["events"],
    "gateways" : bpmn_instance["gateways"]
  }

  
instruction_example_1_triplet  = """### Examples ###
Use the following triplets of extracted information, image and ground truth json as an example

### Example 1 ###
"""

instruction_user_incl_extracted = """### User Input ###
Now create the json based on this extracted information and these images
"""

def chain_of_thoughts_pools(LLM, message_contents, extracted_tasks_events_gateways):
  """Prompts the LLM to generate pools from the process documentation passed as message_contents and the already extracted elements"""

  instruction_pools = """### Instruction ###
  You are a BPMN expert. Your task is to extract pools with lanes and element references out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. 
  For the ids use numbers starting from zero. For the references use the already extracted information and assign their ids to the lanes.
  Generate json according to the following schema for extracting the pools. 
  Only output the generated list of pools with lanes and references as json.
  
  ### Schema ###
  """
  instruction_pools += str(schema_pools)

  extracted_infos = str(extracted_tasks_events_gateways)
  
  messages=[
      system_message([
        text_content(instruction_pools),

        text_content(instruction_example_1_triplet),
        text_content(str(get_tasks_events_gateways_only(ground_truth_example1))),
        image_as_content_example1,
        text_content(str(ground_truth_example1["pools"])),

        text_content(instruction_example_2),
        text_content(str(get_tasks_events_gateways_only(ground_truth_example2))),
        image_as_content_example2,
        text_content(str(ground_truth_example2["pools"])),

        text_content(instruction_example_3),
        text_content(str(get_tasks_events_gateways_only(ground_truth_example3))),
        image_as_content_example3,
        text_content(str(ground_truth_example3["pools"])),
      ]),
      user_message([text_content(instruction_user_incl_extracted), text_content(extracted_infos)] + message_contents)
  ]

  return LLM.ask(messages)

### Sequence and Message Flow  #######################################################################
from multimodalgenai.bpmn_schema_helper import get_tasks_events_gateways_pools_only, get_seq_and_mes_flow_only
schema_seq_mes_flow = {
    "properties": {
        "sequenceFlows": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string" },
                    "sourceRef": { "type": "string" },
                    "targetRef": { "type": "string" },
                    "condition": { "type": "string" },
                },
                "required": ["id", "sourceRef", "targetRef"],
                "description": "Defines the execution order of activities. Activities, events and gateways within a pool must be connected with sequence flow. They can not stand alone. Pictured as an solid arrow",
            }
        },
        "messageFlows": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": { "type": "string" },
                    "sourceRef": { "type": "string" },
                    "targetRef": { "type": "string" },
                    "label": { "type": "string" }
                },
                "required": ["id", "sourceRef", "targetRef"],
                "description": "Messages flow between different pools. Pictured as a an dotted arrow",
          },
        }
    },
    "required": ["sequenceFlows", "messageFlows"],
}

instruction_example_1_triplet  = """### Examples ###
Use the following triplets of extracted information, image and ground truth json as an example

### Example 1 ###
"""

instruction_user_incl_extracted = """### User Input ###
Now create the json based on this extracted information and these images
"""

def chain_of_thoughts_seq_mes_flow(LLM, message_contents, extracted_tasks_events_gateways_pools):
  """Prompts the LLM to generate flows from the process documentation passed as message_contents and the already extracted elements"""


  instruction_seq_mes_flow = """### Instruction ###
  You are a BPMN expert. Your task is to extract sequence and message flow with element references out of the passed documents which
  are parsed as a list of images where each image represents one page of the document. 
  For the ids use numbers starting from zero. For the references use the already extracted information and assign their ids to the flows.
  Generate json according to the following schema for extracting the flows. 
  Only output the generated lists of sequence and message flows with their references as json.
  
  ### Schema ###
  """
  instruction_seq_mes_flow += str(schema_seq_mes_flow)

  extracted_infos = str(extracted_tasks_events_gateways_pools)
  
  messages=[
      system_message([
        text_content(instruction_seq_mes_flow),

        text_content(instruction_example_1_triplet),
        text_content(str(get_tasks_events_gateways_pools_only(ground_truth_example1))),
        image_as_content_example1,
        text_content(str(get_seq_and_mes_flow_only(ground_truth_example1))),

        text_content(instruction_example_2),
        text_content(str(get_tasks_events_gateways_pools_only(ground_truth_example2))),
        image_as_content_example2,
        text_content(str(get_seq_and_mes_flow_only(ground_truth_example2))),

        text_content(instruction_example_3),
        text_content(str(get_tasks_events_gateways_pools_only(ground_truth_example3))),
        image_as_content_example3,
        text_content(str(get_seq_and_mes_flow_only(ground_truth_example3))),
      ]),
      user_message([text_content(instruction_user_incl_extracted), text_content(extracted_infos)] + message_contents)
  ]

  return LLM.ask(messages)


### Chaining it all together  #######################################################################
def generate_chain_of_thoughts_step1_for_index(LLM, i):
    """Prompts the LLM to generate tasks, events and gateways"""
    # load images
    image_paths = read_image_paths_from_index(i)
    images_as_message_contents = get_images_as_message_contents(image_paths)

    # generate tasks
    response_tasks = chain_of_thoughts_tasks(LLM, images_as_message_contents)
    cleaned_response_tasks = get_cleaned_response(response_tasks, validate_to_schema=False)
    write_generated_for_index(cleaned_response_tasks, i, f"generated_chain_of_thoughts_tasks")

    # generate events
    response_events = chain_of_thoughts_events(LLM, images_as_message_contents)
    cleaned_response_events = get_cleaned_response(response_events, validate_to_schema=False)
    write_generated_for_index(cleaned_response_events, i, f"generated_chain_of_thoughts_events")

    # generate gateways
    response_gateways = chain_of_thoughts_gateways(LLM, images_as_message_contents)
    cleaned_response_gateways = get_cleaned_response(response_gateways, validate_to_schema=False)
    write_generated_for_index(cleaned_response_gateways, i, f"generated_chain_of_thoughts_gateways")

def combine_tasks_events_gateways(tasks, events, gateways):
  """Combining the generated tasks, events and gateways to an intermediate model"""
  # assign unqiue ids 
  id_i = 0
  for elem in tasks + events + gateways:
    elem["id"] = id_i
    id_i = id_i + 1

  return{
    "tasks": tasks,
    "events": events,
    "gateways" : gateways
  }

def get_tasks_events_gateways_for_index(i):
    """Loads generated tasks, events, gateways for index i"""
    with open(constants.DATA_ROOT / "generated" / f"{i}_generated_chain_of_thoughts_tasks.json") as f:
      tasks = json.loads(f.read())
    with open(constants.DATA_ROOT / "generated" / f"{i}_generated_chain_of_thoughts_events.json") as f:
      events = json.loads(f.read())
    with open(constants.DATA_ROOT / "generated" / f"{i}_generated_chain_of_thoughts_gateways.json") as f:
      gateways = json.loads(f.read())
    return combine_tasks_events_gateways(tasks, events, gateways)

def generate_chain_of_thoughts_step2_for_index(LLM, i):
    """Prompts the LLM to generate pools"""
    # load images
    image_paths = read_image_paths_from_index(i)
    images_as_message_contents = get_images_as_message_contents(image_paths)

    # load generated files from step 1
    tasks_events_gateways = get_tasks_events_gateways_for_index(i)

    # generate pools
    pools = chain_of_thoughts_pools(LLM, images_as_message_contents, tasks_events_gateways)
    cleaned_pools = get_cleaned_response(pools, validate_to_schema=False)

    tasks_events_gateways_pools = tasks_events_gateways
    tasks_events_gateways_pools["pools"] = cleaned_pools

    write_generated_for_index(tasks_events_gateways_pools, i, f"generated_chain_of_thoughts_pools")

def get_tasks_events_gateways_pools_for_index(i):
   with open(constants.DATA_ROOT / "generated" / f"{i}_generated_chain_of_thoughts_pools.json") as f:
      return json.loads(f.read())

def generate_chain_of_thoughts_step3_for_index(LLM, i):
    """Prompts the LLM to generate flows"""
    # load images
    image_paths = read_image_paths_from_index(i)
    images_as_message_contents = get_images_as_message_contents(image_paths)

    # load generated files from step 2
    tasks_events_gateways_pools = get_tasks_events_gateways_pools_for_index(i)

    # generate message and sequence flow
    mes_seq_flows = chain_of_thoughts_seq_mes_flow(LLM, images_as_message_contents, tasks_events_gateways_pools)
    cleaned_mes_seq_flows = get_cleaned_response(mes_seq_flows, validate_to_schema=False)

    complete = tasks_events_gateways_pools
    complete["sequenceFlows"] = cleaned_mes_seq_flows["sequenceFlows"]
    complete["messageFlows"] = cleaned_mes_seq_flows["messageFlows"]

    write_generated_for_index(complete, i, f"generated_chain_of_thoughts_complete")

def generate_chain_of_thoughts_allsteps_for_index(LLM, i):
    """Prompts the LLM to process models by using the chain of though approach"""
    generate_chain_of_thoughts_step1_for_index(LLM, i)
    generate_chain_of_thoughts_step2_for_index(LLM, i)
    generate_chain_of_thoughts_step3_for_index(LLM, i)