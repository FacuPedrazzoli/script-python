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

def traducir_pos(pos):
    traducciones_pos = {
        "ADJ": "ADJETIVO",
        "ADP": "PREPOSICIÓN",
        "ADV": "ADVERBIO",
        "AUX": "AUXILIAR",
        "CCONJ": "CONJUNCIÓN COORD",
        "DET": "DETERMINANTE",
        "INTJ": "INTERJECCIÓN",
        "NOUN": "SUSTANTIVO",
        "NUM": "NÚMERO",
        "PART": "PARTÍCULA",
        "PRON": "PRONOMBRE",
        "PROPN": "NOMBRE PROPIO",
        "PUNCT": "PUNTUACIÓN",
        "SCONJ": "CONJUNCIÓN SUB",
        "SYM": "SÍMBOLO",
        "VERB": "VERBO",
        "X": "OTRO"
    }
    return traducciones_pos.get(pos, pos)

def traducir_dep(dep):
    traducciones_dep = {
        "ROOT": "RAÍZ",
        "nsubj": "sujeto nominal",
        "obj": "objeto",
        "dobj": "objeto directo",
        "iobj": "objeto indirecto",
        "det": "determinante",
        "amod": "modificador adjetival",
        "advmod": "modificador adverbial",
        "compound": "compuesto",
        "prep": "preposición",
        "pobj": "objeto de preposición",
        "aux": "auxiliar",
        "attr": "atributo",
        "cc": "coordinación",
        "conj": "conjunción",
        "mark": "marcador",
        "punct": "puntuación",
        "npadvmod": "modificador adverbial nominal"
    }
    return traducciones_dep.get(dep, dep)

def traducir_ent(ent):
    traducciones_ent = {
        "PERSON": "PERSONA",
        "LOC": "LUGAR",
        "GPE": "ENTIDAD GEOPOLÍTICA",
        "ORG": "ORGANIZACIÓN",
        "DATE": "FECHA",
        "TIME": "HORA",
        "MONEY": "DINERO",
        "PERCENT": "PORCENTAJE",
        "PRODUCT": "PRODUCTO",
        "EVENT": "EVENTO",
        "WORK_OF_ART": "OBRA DE ARTE",
        "LAW": "LEY",
        "LANGUAGE": "IDIOMA"
    }
    return traducciones_ent.get(ent, ent)

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
            pos_traducido = traducir_pos(token.pos_)
            dep_traducido = traducir_dep(token.dep_)
            token_rows.append([token.text, pos_traducido, dep_traducido, token.head.text, token.lemma_])
        
        if token_rows:
            resultados.append(crear_seccion("ANÁLISIS POR TOKENS"))
            headers = ["TOKEN", "CATEGORÍA", "DEPENDENCIA", "PRINCIPAL", "LEMA"]
            resultados.append(crear_tabla(headers, token_rows))
            
            # Identificación de componentes gramaticales
            sujetos = [t.text for t in sent if "subj" in t.dep_]
            verbos = [t.text for t in sent if t.pos_ == "VERB" or t.pos_ == "AUX"]
            objetos = [t.text for t in sent if "obj" in t.dep_]
            
            # Crear un diagrama visual simplificado de la oración
            diagrama = []
            diagrama.append("DIAGRAMA DE ESTRUCTURA:")
            
            if sujetos or verbos or objetos:
                max_len = max(
                    len(" + ".join(sujetos)) if sujetos else 0,
                    len(" + ".join(verbos)) if verbos else 0,
                    len(" + ".join(objetos)) if objetos else 0,
                    10
                ) + 2
                
                if sujetos:
                    suj_str = " + ".join(sujetos)
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
                    diagrama.append(f"| SUJETO: {suj_str:<{max_len-8}} |")
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
                    diagrama.append(f"        |        ")
                    diagrama.append(f"        V        ")
                
                if verbos:
                    verb_str = " + ".join(verbos)
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
                    diagrama.append(f"| VERBO: {verb_str:<{max_len-7}} |")
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
                    if objetos:
                        diagrama.append(f"        |        ")
                        diagrama.append(f"        V        ")
                
                if objetos:
                    obj_str = " + ".join(objetos)
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
                    diagrama.append(f"| OBJETO: {obj_str:<{max_len-8}} |")
                    diagrama.append(f"+{'-' * (max_len + 2)}+")
            
            resultados.append("\n" + "\n".join(diagrama))
    return "\n".join(resultados)

def process_file(input_path, output_path=None):
    try:
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_output.txt"

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