# Herramientas Utilizadas en el Script de Análisis Sintáctico

Este documento explica paso a paso todas las herramientas y bibliotecas empleadas en el script de análisis sintáctico `analisis_sintactico.py`.

## 1. Bibliotecas Importadas

### spaCy

```python
import spacy
```

- **Descripción**: spaCy es una biblioteca de procesamiento de lenguaje natural (NLP) de código abierto.
- **Función en el script**: Es la herramienta principal para el análisis lingüístico, proporcionando capacidades para:
  - Tokenización (separación del texto en unidades significativas)
  - Análisis morfológico (identificación de categorías gramaticales)
  - Análisis sintáctico de dependencias (relaciones entre palabras)
  - Lematización (reducción de palabras a su forma base)
- **Uso específico**: El script carga un modelo preentrenado (`en_core_web_sm`) para realizar el análisis completo del texto.

### sys

```python
import sys
```

- **Descripción**: Módulo que proporciona acceso a variables y funciones específicas del intérprete de Python.
- **Función en el script**:
  - Manejo de argumentos de línea de comandos (`sys.argv`)
  - Control de salida del programa (`sys.exit()`)
- **Uso específico**: Permite recibir el nombre del archivo a analizar como argumento y terminar la ejecución con códigos de error específicos.

### os

```python
import os
```

- **Descripción**: Módulo que proporciona una forma portable de usar funcionalidades dependientes del sistema operativo.
- **Función en el script**:
  - Manipulación de rutas de archivos (`os.path`)
  - Creación de directorios (`os.makedirs`)
  - Obtención del directorio de trabajo actual (`os.getcwd()`)
- **Uso específico**: Gestiona las rutas de entrada/salida y crea un directorio 'output' para guardar los resultados.

## 2. Funciones de Formato

### crear_recuadro()

```python
def crear_recuadro(texto, ancho=None, estilo="simple")
```

- **Descripción**: Crea un recuadro alrededor del texto utilizando caracteres ASCII.
- **Parámetros**:
  - `texto`: El texto a enmarcar
  - `ancho`: Ancho del recuadro (opcional, calculado automáticamente si no se especifica)
  - `estilo`: Estilo del recuadro ("simple" o "doble")
- **Funcionamiento**:
  1. Calcula el ancho necesario basado en la línea más larga
  2. Define los caracteres de borde según el estilo
  3. Construye el techo y piso del recuadro
  4. Procesa cada línea del texto y la enmarca con bordes verticales
  5. Une todas las partes para formar el recuadro completo
- **Tecnología subyacente**: Manipulación de strings y formato de texto en Python.

### crear_tabla()

```python
def crear_tabla(headers, rows)
```

- **Descripción**: Genera una tabla formateada en ASCII a partir de encabezados y filas de datos.
- **Parámetros**:
  - `headers`: Lista de encabezados para las columnas
  - `rows`: Lista de listas donde cada sublista representa una fila
- **Funcionamiento**:
  1. Calcula el ancho óptimo para cada columna basado en su contenido
  2. Crea líneas separadoras con caracteres '+', '-' y '|'
  3. Formatea los encabezados
  4. Formatea cada fila de datos
  5. Une todos los componentes en una representación de tabla ASCII
- **Tecnología subyacente**: String formatting de Python, especialmente la sintaxis `f"{variable:<width}"` para alineación.

### crear_seccion()

```python
def crear_seccion(titulo, contenido="")
```

- **Descripción**: Crea un formato de sección con título subrayado y contenido opcional.
- **Parámetros**:
  - `titulo`: El texto del título
  - `contenido`: Contenido opcional de la sección
- **Funcionamiento**:
  1. Añade el título con un salto de línea anterior
  2. Crea una línea de subrayado usando el carácter '=' con la misma longitud que el título
  3. Añade el contenido si se proporciona
- **Tecnología subyacente**: Manipulación básica de strings.

## 3. Funciones de Análisis

### analyze_text()

```python
def analyze_text(text)
```

- **Descripción**: Función principal que analiza lingüísticamente un texto utilizando spaCy.
- **Parámetros**:
  - `text`: El texto a analizar
- **Funcionamiento**:
  1. Carga el modelo de lenguaje de spaCy (`en_core_web_sm`)
  2. Procesa el texto completo (`nlp(text)`)
  3. Segmenta el texto en oraciones (`documento.sents`)
  4. Para cada oración:
     - Crea un recuadro con el texto de la oración
     - Extrae información de cada token (palabra o signo)
     - Genera una tabla con el análisis de los tokens
     - Crea una representación visual del árbol de dependencias
- **Tecnología subyacente**:
  - Pipeline de procesamiento de spaCy
  - Objetos `Doc`, `Span` y `Token` de spaCy
  - Atributos lingüísticos como `pos_` (categoría gramatical), `dep_` (dependencia), `head` (palabra principal) y `lemma_` (lema)

## 4. Funciones de Manejo de Archivos

### process_file()

```python
def process_file(input_path, output_path=None)
```

- **Descripción**: Gestiona la lectura del archivo de entrada, el análisis y la escritura de resultados.
- **Parámetros**:
  - `input_path`: Ruta al archivo de texto a analizar
  - `output_path`: Ruta opcional para el archivo de salida
- **Funcionamiento**:
  1. Verifica si se proporcionó un archivo de salida, si no, crea uno automáticamente
  2. Crea un directorio 'output' si no existe
  3. Lee el archivo de entrada con codificación UTF-8
  4. Llama a `analyze_text()` para realizar el análisis
  5. Escribe los resultados en el archivo de salida
  6. Maneja posibles errores como archivos no encontrados
- **Tecnología subyacente**:
  - Manejo de excepciones con bloques `try/except`
  - Operaciones de E/S con archivos utilizando el administrador de contexto `with`
  - Funciones para manejo de rutas como `os.path.splitext`, `os.path.basename` y `os.path.join`

### main()

```python
def main()
```

- **Descripción**: Punto de entrada principal para la ejecución desde línea de comandos.
- **Funcionamiento**:
  1. Verifica que se haya proporcionado al menos un argumento (la ruta del archivo)
  2. Llama a `process_file()` con el archivo de entrada
- **Tecnología subyacente**: Verificación de argumentos de línea de comandos con `sys.argv`

## 5. Ejecución del Script

```python
if __name__ == "__main__":
    main()
```

- **Descripción**: Idioma estándar de Python para garantizar que el código se ejecute solo cuando el script se invoca directamente.
- **Funcionamiento**: Llama a la función `main()` solo si el script se ejecuta como programa principal y no cuando se importa como módulo.

## Diagrama de Flujo del Procesamiento

```
[Archivo de entrada] → process_file() → [Lectura del texto]
                                      ↓
[Modelo de lenguaje spaCy] → analyze_text() → [Procesamiento del texto]
                                            ↓
                  ┌─────────────────────────┴─────────────────────────┐
                  ↓                                                   ↓
        [Análisis por oraciones]                            [Formato de salida]
                  ↓                                                   ↓
  ┌───────────────┴───────────────┐                   ┌───────────────┴───────────────┐
  ↓                               ↓                   ↓                               ↓
[Análisis por tokens]      [Árbol de dependencias]   [crear_recuadro()]        [crear_tabla()]
                                                               ↓
                                                      [Archivo de salida]
```

## Requisitos Técnicos y Consideraciones

- El modelo `en_core_web_sm` debe estar instalado (`python -m spacy download en_core_web_sm`)
- El script está optimizado para textos en inglés
- La entrada y salida utilizan codificación UTF-8
- El script maneja correctamente errores comunes como archivos no encontrados
