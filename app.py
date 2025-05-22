from flask import Flask, render_template, request, jsonify
import random
import string
import logging

app = Flask(__name__)

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password_route():
    app.logger.info("Received request for /generate_password")
    try:
        data = request.get_json()
        if not data:
            app.logger.error("No JSON data received")
            return jsonify({"error": "リクエストが空です。"}), 400

        app.logger.info(f"Request data: {data}")

        char_types = data.get('char_types', {})
        length = data.get('length')
        base_word = data.get('base_word', '')

        if not isinstance(length, int) or length <= 0:
            app.logger.error(f"Invalid length: {length}")
            return jsonify({"error": "文字数は正の整数である必要があります。"}), 400

        if not isinstance(char_types, dict):
            app.logger.error(f"Invalid char_types format: {char_types}")
            return jsonify({"error": "文字の種類は正しい形式で指定してください。"}), 400

        # Character transformation mapping
        transform_map = {
            'l': '1', 'L': '1',
            'o': '0', 'O': '0',
            's': '5', 'S': '5',
            'q': '9', 'Q': '9',
            'b': '8', 'B': '8',
        }

        transformed_base_word = "".join(transform_map.get(char, char) for char in base_word)
        app.logger.info(f"Base word transformed: '{base_word}' -> '{transformed_base_word}'")

        character_set = ""
        if char_types.get('uppercase'):
            character_set += string.ascii_uppercase
        if char_types.get('lowercase'):
            character_set += string.ascii_lowercase
        if char_types.get('numbers'):
            character_set += string.digits
        if char_types.get('symbols'):
            character_set += string.punctuation

        if not character_set:
            app.logger.error("No character types selected")
            return jsonify({"error": "使用する文字の種類を少なくとも1つ選択してください。"}), 400

        app.logger.info(f"Character set constructed with length: {len(character_set)}")

        password_list = []

        if transformed_base_word:
            if len(transformed_base_word) >= length:
                password_list = list(transformed_base_word[:length])
                app.logger.info(f"Base word is longer than or equal to desired length. Using truncated base word: {''.join(password_list)}")
            else:
                password_list = list(transformed_base_word)
                remaining_length = length - len(password_list)
                for _ in range(remaining_length):
                    password_list.append(random.choice(character_set))
                app.logger.info(f"Base word used. Filled remaining {remaining_length} characters randomly.")
        else:
            for _ in range(length):
                password_list.append(random.choice(character_set))
            app.logger.info(f"No base word. Generated {length} random characters.")

        random.shuffle(password_list)
        final_password = "".join(password_list)

        app.logger.info(f"Password generated successfully: {final_password}")
        return jsonify({"password": final_password}), 200

    except Exception as e:
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "パスワードの生成中にエラーが発生しました。"}), 500

if __name__ == '__main__':
    app.run(debug=True)
