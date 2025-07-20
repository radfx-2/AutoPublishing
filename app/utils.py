
from pyrogram import filters, types
import json
from app.values import DATA_DANTIC, DATA_PATH


def getData():
    with open(DATA_PATH, 'r', encoding='utf-8') as ioFile:
        return json.load(ioFile)

def updateData(newData: dict):
    with open(DATA_PATH, 'w', encoding='utf-8') as ioFile:
        json.dump(newData, ioFile, indent=3)


def IS_SPLIT(data):
    def func(flt, _, Q: types.CallbackQuery):
        return flt.data == Q.data.split("|")[0]
    return filters.create(func=func, data=data)