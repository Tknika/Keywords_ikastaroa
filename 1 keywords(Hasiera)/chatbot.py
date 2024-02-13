
import re
import input_data as data
from flask import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)




def clean_text(query):

    sentence = query.lower()
  
    #Azkenengo puntua, koma, punto y koma edo bi puntu kendu
    if sentence.endswith('.') or sentence.endswith(',') or sentence.endswith(';') or sentence.endswith(':'):
        sentence = sentence[:-1]

    #Esaldiari azkenengo ? kendu
    if sentence.endswith('?'):
        sentence = sentence[:-1]
    
    #Esaldiari hasierako ¿ kendu
    if sentence.startswith('¿'):
        sentence = sentence[1:]
    
    tildes = ['á','é','í','ó','ú']
    vocales = ['a','e','i','o','u']
   
    for idx, vocal in enumerate(vocales):        
        sentence = re.sub(tildes[idx], vocal, sentence)

    sentence_array = sentence.split()
     
    return sentence_array



def flow_chart(query_array):

    response_bot = ''
    for word in query_array:
        if word in data.keywords:
            print(word)
            request = data.keywords[word]
            response_bot = data.answer[request]

    if response_bot:
        return response_bot
    else:
        return data.answer['request_unknown']



@app.route('/', methods=["GET"])
def index_get():
    return render_template('base.html')


@app.route("/predict", methods=["POST"])
def engine():
    query = request.get_json().get('message')
    # Clean text
    query_array = clean_text(query)
    # Flow chart
    response = flow_chart(query_array)
    message = {'answer': response}
    return jsonify(message)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
