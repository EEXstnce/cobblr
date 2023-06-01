def print_state(state):
  if state is None:
    print("No state to print.")
    return

  # Print the timestamp
  timestamp = state.get("timestamp")
  if timestamp:
    print("Timestamp:", timestamp)

  # Print the extracted data from the state
  for key, value in state.items():
    if key != "timestamp":
      print(f"{key.capitalize()}:")
      if isinstance(value, list):
        for item in value:
          print("---")
          for sub_key, sub_value in item.items():
            print(f"{sub_key.capitalize()}: {sub_value}")
      else:
        print(value)

  print("\n")
