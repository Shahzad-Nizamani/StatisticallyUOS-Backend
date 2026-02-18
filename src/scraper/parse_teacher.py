from bs4 import BeautifulSoup

def parse_teacher(card):
    teacher = {}

    name = card.find("a").text
    teacher["name"] = name
    print(teacher["name"])

    teacher["role"] = card.find("small").text.strip()
    print(teacher["role"])

    image_url = card.find("img")["src"]
    
    if image_url.startswith('http://') or image_url.startswith('https://'):
        teacher["original_image_url"] = image_url
    elif image_url.startswith('../../'):
        teacher["original_image_url"] = image_url.replace('../../', 'https://itsc.usindh.edu.pk/')
    elif image_url.startswith('../'):
        teacher["original_image_url"] = image_url.replace('../', 'https://itsc.usindh.edu.pk/')
    elif image_url.startswith('/'):
        teacher["original_image_url"] = f"https://usindh.edu.pk{image_url}"
    else:
        teacher["original_image_url"] = f"https://usindh.edu.pk/{image_url}"
    
    return teacher