# Meme-Generator

Opis:
Meme Generator je preprosta spletna aplikacija, ki uporabniku omogoča ustvarjanje memov. Uporabnik izbere sliko in vnese zgornje ter spodnje besedilo. Po kliku gumba se generiran meme prikaže spodaj.

Tehnologije:

Backend: Python, Flask, Pillow

Frontend: HTML, CSS

Docker: za zagon aplikacije v kontejnerju

Namestitev in zagon

Kloniraj repozitorij:

git clone https://github.com/larapodgorsek/Meme-Generator.git

cd meme-generator


Zagon preko Dockerja:

docker build -t meme-generator .

docker run -p 5000:5000 meme-generator


Odpri aplikacijo v brskalniku:

http://127.0.0.1:5000


Zdaj lahko naložiš sliko in ustvariš svoj meme.

Struktura projekta
Meme_generator/
│
├── app.py              # Flask aplikacija
├── Dockerfile          # Docker konfiguracija
├── requirements.txt    # Python odvisnosti
├── templates/          # HTML predloge
├── static/             # CSS, slike
└── README.md           # Ta datoteka