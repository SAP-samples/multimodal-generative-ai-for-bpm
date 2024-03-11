from multimodalgenai.generation.meta_prompt import meta_prompt
from multimodalgenai.generation.pipeline import text_content
from multimodalgenai.io import read_ground_truth_from_index
from multimodalgenai.generation.pipeline import get_image_as_message_content
from sapsam import constants

def few_shot(LLM, message_contents):
  """Prompts the LLM to generate process models from the process documentation passed as message_contents 
  using the few-shot approach with three examples"""

  # instructions for introducing the examples
  instruction_example_1  = """### Examples ###
  Use the following image json pairs as an example
  
  ### Example 1 ###
  """

  instruction_example_2  = "### Example 2 ###\n"
  instruction_example_3  = "### Example 3 ###\n"

  instruction_user = """### User Input ###
  Now create the json based on these images
  """
  
  # Few shot examples
  image_path_example1 = constants.DATA_ROOT / "cleaned" / f"0_process_documentation_page_3.png"
  image_path_example2 = constants.DATA_ROOT / "cleaned" / f"1_process_documentation_page_3.png"
  image_path_example3 = constants.DATA_ROOT / "cleaned" / f"2_process_documentation_page_3.png"
  image_as_content_example1 = get_image_as_message_content(image_path_example1)
  image_as_content_example2 = get_image_as_message_content(image_path_example2)
  image_as_content_example3 = get_image_as_message_content(image_path_example3)
  ground_truth_example1 = str(read_ground_truth_from_index(0))
  ground_truth_example2 = str(read_ground_truth_from_index(1))
  ground_truth_example3 = str(read_ground_truth_from_index(2))
  
  messages=[
    {
      "role": "system",
      "content":   [
          text_content(meta_prompt),

          text_content(instruction_example_1),
          image_as_content_example1,
          text_content(ground_truth_example1),

          text_content(instruction_example_2),
          image_as_content_example2,
          text_content(ground_truth_example2),

          text_content(instruction_example_3),
          image_as_content_example3,
          text_content(ground_truth_example3),
        ]
    },
    {
      "role": "user",
      "content": [text_content(instruction_user)] + message_contents
    },
  ],
  
  return LLM.ask(messages)