from flask import Flask, request, jsonify
import google.generativeai as genai
import logging
from transformers import pipeline # for using model in huggingface
from transformers import AutoTokenizer

app = Flask(__name__)

# Configure logging for error messages
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(logging.StreamHandler())

GOOGLE_API_KEY = "AIzaSyCRcJ6YC861PuxbT0VFPwWCU_3e8nKP6MA"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/generate', methods=['POST'])
def generate_content():
#   tokenizer = AutoTokenizer.from_pretrained(
#     'bmd1905/vietnamese-correction'
# )
  # Get the message from the request body
  try:
    data = request.get_json()
    if not data or 'message' not in data:
      return jsonify({'error': 'Missing message in request body'}), 400

    message = data['message']
  except Exception as e:
    app.logger.error(f"Error parsing request body: {e}")
    return jsonify({'error': 'Error processing request'}), 500
  
  # corrector = pipeline("text2text-generation", model="D:\\HMI_Lab\\vietnamese-correct-als\\models\\my-vietnamese-correct-als\\checkpoint-1000", tokenizer=tokenizer)
  # corrected_message = corrector(message)[0]['generated_text']
  # print(corrected_message)
  # Process the message for summarization
  text = message + ". Tóm tắt kết quả thành 1 đoạn ngắn bằng tiếng việt, liền mạch, không có ký tự đặc biệt."
  
  try:
    response = model.generate_content(text)
  except Exception as e:
    app.logger.error(f"Error during summarization: {e}")
    return jsonify({'error': 'Error generating summary'}), 500
  
  print(response.text)
  # Return the summarized text
  return response.text

  # print(corrected_message)
  # return corrected_message

if __name__ == '__main__':
  app.run(debug=True)
