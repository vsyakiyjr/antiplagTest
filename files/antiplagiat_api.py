from fastapi import FastAPI,HTTPException
import spacy
import language_tool_python  
import uvicorn
import json
import os
import codecs

app = FastAPI()


@app.get("/tca/orig/{orig}/test/{test}")
async def read_tca_item(orig: str, test: str):
    orig_f = orig + '.txt'
    test_f = test + '.txt'
    orig_1 = ''
    test_1 = ''
    if not os.path.isfile(orig_f):
        raise HTTPException(status_code=400, detail=f"{orig_f} not found")
    if not os.path.isfile(test_f):
        raise HTTPException(status_code=400, detail=f"{test_f} not found")
    try:
        with open(orig_f,encoding='UTF-8') as f:
            orig_1 = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while reading {orig_f} file")
    try:
        with open(test_f,encoding='UTF-8') as f:
            test_1 = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while reading {test_f} file")
    lang = 'ru'
    if lang  == 'ru':
        nlp = spacy.load('ru_core_news_lg')
    else:
        nlp = spacy.load('en_core_web_trf')
    doc1 = nlp(orig_1)
    doc2 = nlp(test_1)
    percentage = round(doc1.similarity(doc2) * 100,2)
    data = {
        "result": f"{percentage}%",
        "percentage": percentage
    }
    return data

@app.get("/tcs/orig/{orig}/test/{test}")
async def read_tcs_item(orig: str, test: str):
    orig_f = orig + '.txt'
    test_f = test + '.txt'
    orig_1 = ''
    test_1 = ''
    with open(orig_f,encoding='UTF-8') as f:
        orig_1 = f.read()
        
    with open(test_f,encoding='UTF-8') as f:
        test_1 = f.read()
    lang = 'ru'

    if lang  == 'ru':
        nlp = spacy.load('ru_core_news_sm')
    else:
        nlp = spacy.load('en_core_web_sm')
    
    doc1 = nlp(orig_1)
    doc2 = nlp(test_1)

    result = str(round(doc1.similarity(doc2) * 100,2)) + '%'
    return {"result": result}

@app.get("/avd/{av_text}")
async def avoid(av_text: str):
    my_tool = language_tool_python.LanguageTool('ru-RU')  
    text = av_text + ".txt"
    with codecs.open(text,encoding='UTF-8', errors='ignore') as f:
        final_text = f.read()

    my_matches = my_tool.check(final_text)
    my_tool.close()
    return my_matches

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
