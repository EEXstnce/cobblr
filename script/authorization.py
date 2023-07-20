import pickle


def check_authorization(token):
  with open("tokens.pkl", "rb") as t:
    if token is not None:
      if token in pickle.loads(t.read()):
        return True
  return True  # Default to True for now
