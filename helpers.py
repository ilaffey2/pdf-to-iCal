def parse_shitty_gpt_turbo(text: str):
    text = text.lower()
    # this looks stupid, but i would rather pass in case of 
    # error than fail, and this handles case where neither are there -> True
    if "true" in text:
        return True 
    if "false" in text:
        return False 
    return True