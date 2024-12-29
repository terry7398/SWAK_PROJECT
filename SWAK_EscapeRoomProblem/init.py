import pandas as pd
import json
import toml

chat_load = False
materials_chat_load = False

material_data = pd.read_csv("material.csv")
material_df = material_data
material_df.fillna("",inplace=True)

with open("./data.json","r",encoding="utf-8") as f:
    a_Data = json.load(f)

def load_ChatData():
    with open("./chat_data.json", encoding="utf-8") as f:
        chatData = json.load(f)
    return chatData

def save(choice, data_ = a_Data):
    if choice == 1:
        with open("./data.json","w",encoding="UTF-8") as f:
            json.dump(data_,f,ensure_ascii=False, indent=4)
    elif choice == 2:
        with open("./chat_data.json","w", encoding="utf-8") as f:
            json.dump(data_,f,ensure_ascii=False, indent=4)
    elif choice == 3:
        with open("./Materials_chat_data.json","w", encoding="utf-8") as f:
            json.dump(data_,f,ensure_ascii=False, indent=4)

with open("./.streamlit/secrets.toml", "r",encoding="utf-8") as f:
        secrets = toml.load(f)

with open("./data.json","r",encoding="utf-8") as f:
    a_DataRaw = f.read()
with open("./chat_data.json", encoding="utf-8") as f:
    ChatDataRaw = f.read()