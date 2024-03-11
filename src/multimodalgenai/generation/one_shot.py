from multimodalgenai.generation.meta_prompt import meta_prompt
from multimodalgenai.generation.pipeline import text_content
from multimodalgenai.io import read_ground_truth_from_index
from multimodalgenai.generation.pipeline import get_image_as_message_content
from sapsam import constants

def one_shot(LLM, message_contents):
  """Prompts the LLM to generate process models from the process documentation passed as message_contents 
  using the one-shot approach with one example"""

  instruction_example  = """### Example ###
  Use the following image json pair as an example
  """

  instruction_user = """### User Input ###
  Now create the json based on these images
  """
  
  # Get one shot example
  oneshot_image_path = constants.DATA_ROOT / "cleaned" / f"0_process_documentation_page_3.png"
  oneshot_image_as_content = get_image_as_message_content(oneshot_image_path)
  oneshot_ground_truth = str(read_ground_truth_from_index(0))
  
  messages=[
    {
      "role": "system",
      "content":   [
          text_content(meta_prompt),
          text_content(instruction_example),
          oneshot_image_as_content,
          text_content(oneshot_ground_truth)
        ]
    },
    {
      "role": "user",
      "content": [text_content(instruction_user)] + message_contents
    },
  ],
  
  return LLM.ask(messages)