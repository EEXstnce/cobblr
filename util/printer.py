def print_info(label, value, format_str=None):
    if format_str:
        print(f"{label}: {format_str.format(value)}")
    else:
        print(f"{label}: {value}")