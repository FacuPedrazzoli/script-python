import spacy
import sys
import os

def crear_recuadro(texto, ancho=None, estilo="simple"):
    if not ancho:
        ancho = max(len(linea) for linea in texto.split('\n')) + 4
    
    if estilo == "simple":
        borde_h = "-"
        borde_v = "|"
        esquina_tl = "+"
        esquina_tr = "+"
        esquina_bl = "+"
        esquina_br = "+"
    elif estilo == "doble":
        borde_h = "="
        borde_v = "|"
        esquina_tl = "+"
        esquina_tr = "+"
        esquina_bl = "+"
        esquina_br = "+"
    
    techo = esquina_tl + borde_h * (ancho - 2) + esquina_tr
    piso = esquina_bl + borde_h * (ancho - 2) + esquina_br
    
    resultado = [techo]
    for linea in texto.split('\n'):
        resultado.append(f"{borde_v} {linea:<{ancho-4}} {borde_v}")
    resultado.append(piso)
    
    return '\n'.join(resultado)

def crear_tabla(headers, rows):
    # Calcular el ancho de cada columna
    anchos = [max(len(str(h)), 10) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            anchos[i] = max(anchos[i], len(str(cell)))
    
    # Crear decoradores para la tabla
    linea_superior = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"
    linea_media = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"
    linea_inferior = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"
    
    # Crear el encabezado
    header_str = "|"
    for i, h in enumerate(headers):
        header_str += f" {h:<{anchos[i]}} |"
    
    # Crear las filas
    rows_str = []
    for row in rows:
        row_str = "|"
        for i, cell in enumerate(row):
            row_str += f" {str(cell):<{anchos[i]}} |"
        rows_str.append(row_str)
    
    # Unir todo
    tabla = [linea_superior, header_str, linea_media] + rows_str + [linea_inferior]
    return '\n'.join(tabla)

def crear_seccion(titulo, contenido=""):
    resultado = []
    resultado.append(f"\n{titulo}")
    resultado.append("=" * len(titulo))
    if contenido:
        resultado.append(contenido)
    return '\n'.join(resultado)

def analyze_text(text):
    nlp = spacy.load("en_core_web_sm")
    documento = nlp(text)

    resultados = []

    # Texto original
    resultados.append(crear_seccion("TEXTO ORIGINAL"))

    for i, sent in enumerate(documento.sents):
        # Encabezado de la oración
        resultados.append(f"\n{'=' * 25} ORACIÓN {i+1} {'=' * 25}")
        resultados.append(crear_recuadro(str(sent), estilo="simple"))

        # Análisis de tokens con mejor formato
        token_rows = []
        for token in sent:
            token_rows.append([token.text, token.pos_, token.dep_, token.head.text, token.lemma_])

        if token_rows:
            resultados.append(crear_seccion("ANÁLISIS POR TOKENS"))
            headers = ["TOKEN", "CATEGORÍA", "DEPENDENCIA", "PRINCIPAL", "LEMA"]
            resultados.append(crear_tabla(headers, token_rows))

            # Crear un árbol de dependencias
            resultados.append(crear_seccion("ÁRBOL DE DEPENDENCIAS"))
            for token in sent:
                resultados.append(f"{token.text} ({token.dep_}) --> {token.head.text}")

    return "\n".join(resultados)

# Ensure output files are saved in the 'output' directory
def process_file(input_path, output_path=None):
    try:
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_dir = os.path.join(os.getcwd(), "output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{base_name}_output.txt")

        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        analysis = analyze_text(text)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(analysis)
        
        print(f"Análisis completado. Resultado guardado en {output_path}")
    
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_path}' no fue encontrado.")
        sys.exit(1)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Uso: python analisis_sintactico.py <archivo_entrada>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    process_file(input_path)

if __name__ == "__main__":
    main()