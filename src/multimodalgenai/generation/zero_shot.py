from multimodalgenai.generation.meta_prompt import meta_prompt
from multimodalgenai.generation.pipeline import text_content

def zero_shot(LLM, message_contents):
  """Prompts the LLM to generate process models from the process documentation passed as message_contents 
  using the zero-shot approach without any examples"""
  messages=[
    {
      "role": "user",
      "content": message_contents
    },
    {
      "role": "system",
      "content":   [
          text_content(meta_prompt)
        ]
    },
  ],
  
  return LLM.ask(messages)