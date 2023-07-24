from rasa.nlu.model import Interpreter

# path of your model
rasa_model_path = r"erfan\models\20230717-220036-aquamarine-assumption.tar.gz"

# create an interpreter object
interpreter = Interpreter.load(rasa_model_path)


"""
Function to get model output

Args:
  text  (string)  --  input text string to be passed)

For example: if you are interested in entities, you can just write result['entities']

Returns:
  json  --  json output to used for accessing model output

"""

def rasa_output(text):
    message = str(text).strip()
    result = interpreter.parse(message)
    return result

rasa_output("hi")