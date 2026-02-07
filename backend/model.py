def generate_caption(image_path,sentiment="neutral", length="short"):
    base = " A beautiful moment captured"
    if sentiment == "happy":
        base = "A joyful moment full of happiness"
    elif sentiment == "sad":
        base ="An quiet moment filled with emotions"
    elif sentiment == "aesthetic":
        base="An aesthetic frame with calm vibes"    
    if length == "short":
        return base
    elif length =="medium":
        base + "that tells a story"
    else:
        return base + "that tells a deep and meaningful story beyond words"        