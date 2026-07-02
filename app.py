import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'biblioteca_datos.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

def cargar_datos():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f: json.dump(datos, f, indent=4)

@app.route('/')
def inicio():
    catalogo = cargar_datos()
    genero_filtro = request.args.get('genero', 'Todos')
    busqueda = request.args.get('busqueda', '').lower()
    
    lista = [{"archivo": k, **v} for k, v in catalogo.items()]
    generos = {"Todos"}
    for libro in lista: generos.add(libro.get('genero', 'Otros'))
    
    if genero_filtro != 'Todos':
        lista = [l for l in lista if l.get('genero') == genero_filtro]
    if busqueda:
        lista = [l for l in lista if busqueda in l.get('titulo', '').lower() or busqueda in l.get('autor', '').lower()]
        
    lista.sort(key=lambda x: x.get('orden', 99))
    return render_template('inicio.html', libros=lista, generos=sorted(list(generos)), filtro=genero_filtro, busqueda=busqueda)

@app.route('/subir', methods=['GET', 'POST'])
def subir():
    if request.method == 'POST':
        # Aquí luego procesaremos el archivo. Por ahora, esto evita el error:
        return "Libro recibido (lógica pendiente)"
    return render_template('subir.html')

if __name__ == '__main__':
    app.run(debug=True)