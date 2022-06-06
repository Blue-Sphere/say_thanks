import json

def get_point_template_flexMassage():
    with open("files/get_point_template_FlexMessage.json","r",encoding="utf-8") as file:
        return json.load(file)
def thanks_type_template_flexMessage():
    with open("files/thanks_type_template_FlexMessage.json","r",encoding="utf-8") as file:
        return json.load(file)