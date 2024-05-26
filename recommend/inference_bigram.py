import os
import sys
from flask import Flask, request, jsonify
import json
import pandas as pd  # Import pandas library
import csv

sys.path.append("models")
from bigram import BigramModel

app = Flask(__name__)

@app.route('/nlp-endpoint', methods=['POST'])
def nlp_endpoint():
    data = request.get_json()
    input_text = data.get('sent', '')

    input_w = input_text.split("_")[-1]
    threshold = float(request.args.get('threshold', 0.12))

    bigram_ins = BigramModel()
    model = bigram_ins.bigram_wordcount()

    recommend_ws = []

    for w in model[input_w]:
        if (model[input_w][w] > threshold) and w is not None and len(w):
            recommend_ws.append(w)

    print(recommend_ws)

    # Export DataFrame to Excel
    with open('recommendations.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(recommend_ws)

    return jsonify({'success': True, 'message': 'Recommendations exported to Excel'})

if __name__ == "__main__":
    app.run(debug=True)
