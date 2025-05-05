# Documentación: Analizador Sintáctico

## Descripción General

Este script utiliza la biblioteca spaCy para realizar análisis sintáctico y morfológico de textos. Es capaz de procesar archivos de texto, analizar cada oración y mostrar información detallada sobre los tokens, sus categorías gramaticales, dependencias sintácticas y lemas.

## Requisitos

- Python 3.6 o superior
- Biblioteca spaCy
- Modelo de lenguaje "en_core_web_sm" para spaCy

## Instalación

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Uso Básico

```bash
python analisis_sintactico.py <ruta_del_archivo_de_entrada>
```

El script procesará el archivo de entrada y guardará los resultados en un directorio 'output' en la carpeta de trabajo actual, con el nombre `<nombre_archivo>_output.txt`.

## Funciones Principales

### `analyze_text(text)`

Analiza el texto proporcionado utilizando spaCy y genera un informe detallado.

**Parámetros:**

- `text` (str): El texto a analizar.

**Retorna:**

- String formateado con todos los resultados del análisis.

### `process_file(input_path, output_path=None)`

Procesa un archivo de texto y guarda el análisis en un archivo de salida.

**Parámetros:**

- `input_path` (str): Ruta al archivo de entrada.
- `output_path` (str, opcional): Ruta al archivo de salida. Si no se proporciona, se crea automáticamente en la carpeta 'output'.

### `crear_recuadro(texto, ancho=None, estilo="simple")`

Crea un recuadro alrededor del texto proporcionado.

**Parámetros:**

- `texto` (str): El texto a enmarcar.
- `ancho` (int, opcional): El ancho del recuadro. Por defecto se calcula automáticamente.
- `estilo` (str, opcional): Estilo del recuadro ("simple" o "doble").

**Retorna:**

- String formateado con el texto enmarcado.

### `crear_tabla(headers, rows)`

Genera una tabla ASCII a partir de los encabezados y filas proporcionados.

**Parámetros:**

- `headers` (list): Lista con los nombres de las columnas.
- `rows` (list): Lista de listas donde cada sublista representa una fila.

**Retorna:**

- String formateado con la representación de la tabla.

### `crear_seccion(titulo, contenido="")`

Crea una sección formateada con un título y opcionalmente contenido.

**Parámetros:**

- `titulo` (str): El título de la sección.
- `contenido` (str, opcional): El contenido de la sección.

**Retorna:**

- String formateado con la sección.

## Estructura del Análisis

Por cada texto analizado, el script genera:

1. **Texto Original**: Muestra el texto completo antes del análisis.
2. **Oraciones**: Para cada oración:
   - Muestra la oración enmarcada en un recuadro.
   - **Análisis por Tokens**: Tabla con información de cada token:
     - TOKEN: El texto del token.
     - CATEGORÍA: La categoría gramatical (POS).
     - DEPENDENCIA: La relación de dependencia sintáctica.
     - PRINCIPAL: El token del que depende.
     - LEMA: La forma base o lema del token.
   - **Árbol de Dependencias**: Representación simplificada de las relaciones sintácticas.

## Ejemplos de Salida

### Ejemplo de una Oración Analizada

```
========================= ORACIÓN 1 =========================
+------------------------------------------+
| This is a sample sentence for analysis.  |
+------------------------------------------+

ANÁLISIS POR TOKENS
===================
+----------+------------+-------------+------------+----------+
| TOKEN    | CATEGORÍA  | DEPENDENCIA | PRINCIPAL  | LEMA     |
+----------+------------+-------------+------------+----------+
| This     | DET        | nsubj       | is         | this     |
| is       | AUX        | ROOT        | is         | be       |
| a        | DET        | det         | sentence   | a        |
| sample   | ADJ        | amod        | sentence   | sample   |
| sentence | NOUN       | attr        | is         | sentence |
| for      | ADP        | prep        | sentence   | for      |
| analysis | NOUN       | pobj        | for        | analysis |
| .        | PUNCT      | punct       | is         | .        |
+----------+------------+-------------+------------+----------+

ÁRBOL DE DEPENDENCIAS
=====================
This (nsubj) --> is
is (ROOT) --> is
a (det) --> sentence
sample (amod) --> sentence
sentence (attr) --> is
for (prep) --> sentence
analysis (pobj) --> for
. (punct) --> is
```

## Notas Adicionales

- El script está configurado para trabajar con textos en inglés por defecto.
- Los resultados se guardan automáticamente en una carpeta 'output' que se crea si no existe.
