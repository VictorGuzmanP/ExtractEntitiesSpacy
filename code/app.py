from flask import Flask, render_template, request
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import json

UPLOAD_FOLDER = 'textos'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_lang_detector(nlp, name):
    return LanguageDetector()

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/process', methods = ['POST', ])
def process_text():
    NO_VALID_TEXT = "No se ha proporcionado un texto válido."
    if request.method == 'POST' and 'rawtext' in request.form:
        text = request.form.get('rawtext')
        taskoption = request.form.get('taskoption')

        nlp = spacy.load("es_core_news_md")
        Language.factory("language_detector", func=get_lang_detector)
        nlp.add_pipe('language_detector', last=True)
        
        #SALVAR TEXTO EN TXT

        #texto.sa.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        #img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        
        doc = nlp(text)

        if (doc._.language["language"] == "es"):
            print("Lenguaje seleccionado Español: es_core_news_md ")
        else:
            if (doc._.language["language"] == "ca"):
                nlp = spacy.load("ca_core_news_md")
                print("Lenguaje seleccionado catalán: ca_core_news_md ")
                doc = nlp(text)
            else:
                nlp = spacy.load("en_core_web_md")
                print("Lenguaje seleccionado otro: en_core_web_md ")
                doc = nlp(text)

        opt = ''
        print ("taskoption: " + taskoption)
        if  taskoption == "":
            opt = ""
        else:
            if  taskoption == "organization":
                opt = "ORG"
            else:
                if  taskoption == "person":
                    opt = "PER"
                else:
                    if  taskoption == "location":
                        opt = "LOC"
                    else:
                        if taskoption == "nounproper":
                           opt = "NNP"
                        else:
                            if  taskoption == "miscellane":
                                opt = "MISC" 

        entidades = []
        
        print ("opt: " + opt)
        if opt == '':
            for ent in doc.ents:
                entidades.append(ent.text + ' - ' + ent.label_)
        else:
            for ent in doc.ents:
                if ent.label_ == opt:
                    entidades.append(ent.text + ' - ' + ent.label_)

    print ('Valor de entidades: ' )
    for i in entidades:
        print ('valor entidades: ' + i)

    return render_template('index.html', results=entidades)

if __name__ == '__main__':
    app.run(debug = True)