#osnovna slika
FROM python:3.12-slim

#mapa tnotraj kontejnera
WORKDIR /app  

#kopiranje datotek 
COPY . .

#namestitev vseh potrebnih knjižnic
RUN pip install --no-cache-dir -r requirements.txt

#--no-cache-dri zmanjsa velikost slike

#definira vrednosti ki jih app lahko uporablja
ENV PORT=5000

#odpre port
EXPOSE 5000

#zažene aplikacijo
CMD ["python", "app.py"]

