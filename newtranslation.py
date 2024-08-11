# -*- coding: utf-8 -*-
"""newtranslation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uqCV3xPOWITmmxQdU2vlmnIAkse8whdk
"""

!pip install transformers torch streamlit

import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch

model_name_fr = 'Helsinki-NLP/opus-mt-en-fr'
tokenizer_fr = MarianTokenizer.from_pretrained(model_name_fr)
model_fr = MarianMTModel.from_pretrained(model_name_fr)

model_name_hi = 'Helsinki-NLP/opus-mt-en-hi'
tokenizer_hi = MarianTokenizer.from_pretrained(model_name_hi)
model_hi = MarianMTModel.from_pretrained(model_name_hi)

def translate_en_to_fr(text):
    inputs = tokenizer_fr(text, return_tensors='pt')
    with torch.no_grad():
        translated = model_fr.generate(**inputs)
    return tokenizer_fr.decode(translated[0], skip_special_tokens=True)

def translate_en_to_hi(text):
    inputs = tokenizer_hi(text, return_tensors='pt')
    with torch.no_grad():
        translated = model_hi.generate(**inputs)
    return tokenizer_hi.decode(translated[0], skip_special_tokens=True)

def main():
    st.title("Simultaneous Translation: English to French and Hindi")
    st.write("Enter a 10-letter English word to see translations:")

    text = st.text_input("English Word", "")
    if text and len(text) == 10:
        st.write("English to French:", translate_en_to_fr(text))
        st.write("English to Hindi:", translate_en_to_hi(text))
    elif text:
        st.write("Please enter exactly 10 letters.")

if __name__ == "__main__":
    main()

dataset = [
    {"en": "translate", "fr": "traduire", "hi": "अनुवाद"},
    {"en": "education", "fr": "éducation", "hi": "शिक्षा"},
    # Add more examples
]

from sklearn.metrics import accuracy_score

def evaluate_translation_model(model, tokenizer, test_data, target_lang):
    predictions = []
    ground_truth = []

    for data in test_data:
        input_text = data["en"]
        true_translation = data[target_lang]

        inputs = tokenizer(input_text, return_tensors='pt')
        with torch.no_grad():
            translated = model.generate(**inputs)
        predicted_translation = tokenizer.decode(translated[0], skip_special_tokens=True)

        predictions.append(predicted_translation.strip())
        ground_truth.append(true_translation.strip())

    return accuracy_score(ground_truth, predictions)

def evaluate_models():
    # Evaluate English to French
    accuracy_fr = evaluate_translation_model(model_fr, tokenizer_fr, dataset, "fr")
    print(f"Accuracy for English to French translation: {accuracy_fr*100:.2f}%")

    # Evaluate English to Hindi
    accuracy_hi = evaluate_translation_model(model_hi, tokenizer_hi, dataset, "hi")
    print(f"Accuracy for English to Hindi translation: {accuracy_hi*100:.2f}%")

evaluate_models()

