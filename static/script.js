document.addEventListener('DOMContentLoaded', () => {
    const generateButton = document.getElementById('generate_button');
    const passwordForm = document.getElementById('password_form');
    const passwordDisplay = document.getElementById('password_display');
    const lengthCustomInput = document.getElementById('length_custom');

    generateButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const charTypes = {
            uppercase: document.getElementById('char_uppercase').checked,
            lowercase: document.getElementById('char_lowercase').checked,
            numbers: document.getElementById('char_numbers').checked,
            symbols: document.getElementById('char_symbols').checked,
        };

        let length;
        const selectedLengthOption = document.querySelector('input[name="length"]:checked');

        if (!selectedLengthOption) {
            passwordDisplay.value = "エラー: 文字数を選択してください。";
            return;
        }

        if (selectedLengthOption.value === 'other') {
            const customLength = parseInt(lengthCustomInput.value, 10);
            if (isNaN(customLength) || customLength <= 0) {
                passwordDisplay.value = "エラー: 「その他」の文字数には有効な数値を入力してください。";
                return;
            }
            length = customLength;
        } else {
            length = parseInt(selectedLengthOption.value, 10);
        }

        const baseWord = document.getElementById('base_word').value;

        // Validate that at least one character type is selected
        const selectedCharTypes = Object.values(charTypes).some(type => type);
        if (!selectedCharTypes) {
            passwordDisplay.value = "エラー: 使用する文字の種類を少なくとも1つ選択してください。";
            return;
        }

        const requestData = {
            char_types: charTypes,
            length: length,
            base_word: baseWord,
        };

        try {
            const response = await fetch('/generate_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            });

            const responseData = await response.json();

            if (response.ok) {
                passwordDisplay.value = responseData.password;
            } else {
                passwordDisplay.value = `エラー: ${responseData.error || 'パスワードを生成できませんでした。'}`;
            }
        } catch (error) {
            console.error('Error during password generation:', error);
            passwordDisplay.value = 'エラー: パスワード生成中に問題が発生しました。';
        }
    });

    // Enable/disable custom length input based on radio button selection
    const lengthRadioButtons = document.querySelectorAll('input[name="length"]');
    lengthRadioButtons.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'other') {
                lengthCustomInput.disabled = false;
                lengthCustomInput.focus();
            } else {
                lengthCustomInput.disabled = true;
                lengthCustomInput.value = ''; // Clear custom input when other option is selected
            }
        });
    });
    // Initialize custom length input state
    if (document.querySelector('input[name="length"]:checked')?.value !== 'other') {
        lengthCustomInput.disabled = true;
    }
});
