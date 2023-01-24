import tkinter as tk
import argostranslate.package
import argostranslate.translate
import genanki
from janome.tokenizer import Tokenizer

def translate_sentence():
    japanese_sentence = input_sentence.get()

    # translate the sentence to english
    from_code = "ja"
    to_code = "en"
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    translatedText = argostranslate.translate.translate(japanese_sentence, from_code, to_code)

    # create an Anki deck
    my_deck = genanki.Deck(
        2059400110,
        "Japanese-English Vocab")
    my_card = genanki.Note(
        model=genanki.Model(
            1607392319,
            "Japanese-English Sentence",
            fields=[
                {"name": "Japanese"},
                {"name": "English"}
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "{{Japanese}}",
                    "afmt": "{{FrontSide}}<hr id='answer'>{{English}}"
                }
            ]
        ),
        fields=[japanese_sentence, translatedText])

    # add card to deck
    my_deck.add_note(my_card)

    # tokenizer
    t = Tokenizer()
    for token in t.tokenize(japanese_sentence):
        if token.part_of_speech.startswith('名詞') or token.part_of_speech.startswith('形容詞'):
            translated_word = argostranslate.translate.translate(token.surface, from_code, to_code)
            my_card = genanki.Note(
                model=genanki.Model(
                    1607392319,
                    "Japanese-English Word",
                    fields=[
                        {"name": "Japanese"},
                        {"name": "English"}
                    ],
                    templates=[
                        {
                            "name": "Card 1",
                            "qfmt": '<div style="text-align:center;"><br><span style="font-size: 50px; "> {{Japanese}} </span></div>',
                            "afmt": '<div style="text-align:center;"><br><span style="font-size: 50px; ">{{FrontSide}}<hr id="answer">{{English}}</span></div>'
                        }
                    ]
                ),
                fields=[token.surface, translated_word])
            my_deck.add_note(my_card)
        genanki.Package(my_deck).write_to_file("Japanese-English Vocab.apkg")


root = tk.Tk()
root.title("Japanese-English Translator")
label_sentence = tk.Label(root, text="Enter a Japanese sentence to translate:")
label_sentence.pack()
input_sentence = tk.Entry(root)
input_sentence.pack()

translate_button = tk.Button(root, text="Translate", command=translate_sentence)
translate_button.pack()

root.mainloop()
