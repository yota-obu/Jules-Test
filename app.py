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

        final_password = ""

        if not transformed_base_word:
            # No base word, generate fully random password
            password_list = [random.choice(character_set) for _ in range(length)]
            final_password = "".join(password_list)
            app.logger.info(f"No base word. Generated {length} random characters: {final_password}")
        else:
            # Base word is present
            num_additional_chars = length - len(transformed_base_word)

            if num_additional_chars < 0:
                # Transformed base word is longer than desired length, truncate it
                final_password = transformed_base_word[:length]
                app.logger.info(f"Transformed base word ('{transformed_base_word}') is longer than length {length}. Truncated to: {final_password}")
            else:
                # Transformed base word is shorter or equal to length
                password_chars_list = list(transformed_base_word)
                
                if num_additional_chars > 0:
                    additional_chars = [random.choice(character_set) for _ in range(num_additional_chars)]
                    app.logger.info(f"Generated {num_additional_chars} additional characters: {additional_chars}")

                    # Insert additional characters randomly into the base word
                    for char_to_insert in additional_chars:
                        # Randomly select an insertion point (index)
                        # len(password_chars_list) + 1 possible insertion slots
                        insertion_point = random.randint(0, len(password_chars_list))
                        password_chars_list.insert(insertion_point, char_to_insert)
                    app.logger.info(f"Password list after inserting additional chars: {password_chars_list}")
                
                final_password = "".join(password_chars_list)
                # Ensure the final password does not exceed the requested length,
                # which could happen if the base_word itself was already long
                # and then more characters were added. This case should be rare
                # given the logic, but as a safeguard:
                if len(final_password) > length:
                    final_password = final_password[:length]


        app.logger.info(f"Password generated successfully: {final_password}")
        return jsonify({"password": final_password}), 200

    except Exception as e:
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "パスワードの生成中にエラーが発生しました。"}), 500

if __name__ == '__main__':
    app.run(debug=True)
