# Imports
import click
from numpy import nan
import src.preprocessing as pp # Importamos el preprocessing
from typing import List, Any

# --- 1. Función Ayudante (Helper) ---
# La terminal solo nos da strings. Necesitamos una función que convierta
# "10.5" a 10.5 (float), "None" a None, "nan" a nan, etc.

def process_input_list(str_list: tuple) -> List[Any]:
    """Convierte una tupla de strings de la CLI a una lista con tipos."""
    processed = []
    for item in str_list:
        if item.lower() == 'none':
            processed.append(None)
        elif item.lower() == 'nan':
            processed.append(nan)
        elif item == "":
            processed.append("")
        else:
            # Intenta convertir a float o int
            try:
                val = float(item)
                # Si es un entero (ej. 10.0), conviértelo a int
                if val.is_integer():
                    processed.append(int(val))
                else:
                    processed.append(val)
            except ValueError:
                # Si falla, es un string
                processed.append(item)
    return processed

def process_input_value(str_val: str) -> Any:
    """Convierte un solo string de la CLI a su tipo Python."""
    # Reutilizamos la función de lista para procesar un solo elemento
    return process_input_list((str_val,))[0]


# --- 2. Grupo Principal 'cli' ---
@click.group()
def cli():
    """
    Herramienta CLI para ejecutar funciones de preprocesamiento de datos.
    """
    pass

# --- 3. Subgrupo 'clean' ---
@cli.group(help="Funciones relacionadas con la limpieza de datos.")
def clean():
    pass

@clean.command(help="Elimina valores faltantes (None, '', nan) de una lista.")
@click.argument("data", nargs=-1, required=True) # nargs=-1 = acepta múltiples argumentos
def remove_missing(data: tuple):
    """
    Elimina valores faltantes (None, '', nan) de una lista.

    EJEMPLO:
    uv run python src/cli.py clean remove-missing 10 20.5 None "" 30 nan text
    """
    processed_data = process_input_list(data)
    result = pp.remove_missing_values(processed_data)
    click.echo(f"Resultado: {result}")

@clean.command(help="Rellena valores faltantes con un valor específico.")
@click.argument("data", nargs=-1, required=True)#Aqui pasamos los argumentos de la funcion
@click.option(
    "--fill-value",
    default="0", # El default es 0, pero lo pasamos como string
    type=str,
    help="Valor para rellenar los faltantes."
)
def fill_missing(data: tuple, fill_value: str):
    """
    Rellena valores faltantes (None, '', nan) con un valor (default 0).

    EJEMPLO:
    uv run python src/cli.py clean fill-missing 10 20 None --fill-value -1
    uv run python src/cli.py clean fill-missing 10 20 None --fill-value "NA"
    """
    processed_data = process_input_list(data)
    processed_fill_value = process_input_value(fill_value) # Procesamos el valor de relleno
    
    result = pp.filling_missing_values(processed_data, processed_fill_value)
    click.echo(f"Resultado: {result}")

@clean.command(help="Elimina valores duplicados de una lista.")
@click.argument("data", nargs=-1, required=True)
def unique(data: tuple):
    """
    Devuelve una lista con valores únicos, conservando el orden.

    EJEMPLO:
    uv run python src/cli.py clean unique 10 20 10 30 20 10
    """
    processed_data = process_input_list(data)
    result = pp.remove_duplicated_values(processed_data)
    click.echo(f"Resultado: {result}")

# --- 4. Subgrupo 'numeric' ---
@cli.group(help="Funciones relacionadas con datos numéricos.")
def numeric():
    pass

@numeric.command(help="Normaliza valores numéricos (Min-Max).")
@click.argument("data", nargs=-1, required=True)
@click.option("--min-val", default=0.0, type=float, help="Nuevo mínimo (default: 0.0).")
@click.option("--max-val", default=1.0, type=float, help="Nuevo máximo (default: 1.0).")
def normalize(data: tuple, min_val: float, max_val: float):
    """
    Normaliza una lista de números al rango [min, max].

    EJEMPLO:
    uv run python src/cli.py numeric normalize 10 20 30 40 50 --min-val 0 --max-val 1
    """
    processed_data = process_input_list(data)
    result = pp.normalize_min_max(processed_data, min_val, max_val)
    click.echo(f"Resultado: {result}")

@numeric.command(help="Estandariza valores numéricos (Z-Score).")
@click.argument("data", nargs=-1, required=True)
def standardize(data: tuple):
    """
    Estandariza una lista de números usando Z-score.

    EJEMPLO:
    uv run python src/cli.py numeric standardize 10 20 30 40 50
    """
    processed_data = process_input_list(data)
    result = pp.standardize_z_score(processed_data)
    click.echo(f"Resultado: {result}")

@numeric.command(help="Recorta valores numéricos a un rango.")
@click.argument("data", nargs=-1, required=True)
@click.option("--min-val", default=0.0, type=float, help="Valor mínimo (default: 0.0).")
@click.option("--max-val", default=1.0, type=float, help="Valor máximo (default: 1.0).")
def clip(data: tuple, min_val: float, max_val: float):
    """
    Recorta valores numéricos a un rango [min, max].

    EJEMPLO:
    uv run python src/cli.py numeric clip 5 10 15 20 25 --min-val 10 --max-val 20
    """
    processed_data = process_input_list(data)
    result = pp.clip_values(processed_data, min_val, max_val)
    click.echo(f"Resultado: {result}")

@numeric.command(help="Convierte strings a enteros.")
@click.argument("data", nargs=-1, required=True)
def to_integers(data: tuple):
    """
    Convierte una lista de strings a enteros, ignorando no numéricos.

    EJEMPLO:
    uv run python src/cli.py numeric to-integers 10.5 "20" 30.0 "texto"
    """
    # La función 'convert_to_integers' espera strings,
    # así que no usamos el helper 'process_input_list'.
    result = pp.convert_to_integers(list(data))
    click.echo(f"Resultado: {result}")

@numeric.command(help="Aplica transformación logarítmica.")
@click.argument("data", nargs=-1, required=True)
def log_transform(data: tuple):
    """
    Aplica logaritmo natural a números positivos.

    EJEMPLO:
    uv run python src/cli.py numeric log-transform 1 10 100 -5 0
    """
    processed_data = process_input_list(data)
    result = pp.logarithmic_transform(processed_data)
    click.echo(f"Resultado: {result}")

# --- 5. Subgrupo 'text' ---
@cli.group(help="Funciones para procesar información textual.")
def text():
    pass

@text.command(help="Tokeniza texto (alfanuméricos y minúsculas).")
@click.argument("text_input", type=str)
def tokenize(text_input: str):
    """
    Tokeniza texto: solo alfanuméricos y convierte a minúsculas.

    EJEMPLO:
    uv run python src/cli.py text tokenize "Hola, mundo! Esto es 1 prueba."
    """
    result = pp.tokenize_text(text_input)
    click.echo(f"Resultado: {result}")

@text.command(help="Selecciona solo alfanuméricos y espacios.")
@click.argument("text_input", type=str)
def remove_punctuation(text_input: str):
    """
    Elimina puntuación, conservando solo alfanuméricos y espacios.
    (Nota: El lab nombra este comando 'Remove punctuation')

    EJEMPLO:
    uv run python src/cli.py text remove-punctuation "Test... con acentos? Sí!"
    """
    result = pp.select_alphanumeric_spaces(text_input)
    click.echo(f"Resultado: {result}")

@text.command(help="Elimina stop-words de un texto.")
@click.argument("text_input", type=str)
@click.option(
    "--stop-word",
    "stop_words", # Nombre de la variable en la función
    multiple=True, # Permite usar la opción varias veces
    help="Palabra a eliminar (usar varias veces para una lista)."
)
def remove_stops(text_input: str, stop_words: tuple):
    """
    Elimina una lista de stop-words de un texto.

    EJEMPLO:
    uv run python src/cli.py text remove-stops "este es un texto de prueba" --stop-word "un" --stop-word "de"
    """
    # 'stop_words' es una tupla, la convertimos a lista para la lógica
    result = pp.remove_stop_words(text_input, list(stop_words))
    click.echo(f"Resultado: {result}")


# --- 6. Subgrupo 'struct' ---
@cli.group(help="Funciones relacionadas con la estructura de datos.")
def struct():
    pass

@struct.command(help="Aplana una lista de listas.")
@click.argument("data", nargs=-1, required=True)
def flatten(data: tuple):
    """
    Aplana una lista mixta de elementos y listas.
    
    NOTA: Para pasar una lista anidada, usamos una sintaxis
    especial de 'click' o la simulamos. Click no soporta
    listas anidadas fácilmente. Este comando asume que la entrada
    ya es una lista (procesada por nuestro helper).
    Para probarlo, simulamos la estructura desde la lógica.
    
    Este comando es difícil de probar desde CLI.
    La función 'process_input_list' aplana la entrada por defecto.
    uv run python src/cli.py struct flatten 1 2 3
    """
    # Este comando es problemático para un CLI simple, ya que
    # 'click' no puede recibir una "lista de listas" fácilmente.
    # El test de integración (test_cli.py) será clave aquí.
    # Simulamos el aplanamiento de lo que recibimos.
    processed_data = process_input_list(data)
    # Como process_input_list ya aplana, llamamos a flatten
    # con una lista que *contiene* la lista procesada, para simular
    # una lista anidada.
    simulated_nested_list = [processed_data[:2], processed_data[2:]]
    click.echo(f"(Entrada simulada: {simulated_nested_list})")
    
    result = pp.flatten_list(simulated_nested_list)
    click.echo(f"Resultado: {result}")


@struct.command(help="Mezcla aleatoriamente una lista.")
@click.argument("data", nargs=-1, required=True)
@click.option(
    "--seed",
    default=None, # El default es None
    type=int,
    help="Semilla para reproducibilidad (default: None)."
)
def shuffle(data: tuple, seed: int):
    """
    Mezcla aleatoriamente una lista, con una semilla opcional.

    EJEMPLO:
    uv run python src/cli.py struct shuffle 1 2 3 4 5 --seed 42
    """
    processed_data = process_input_list(data)
    result = pp.shuffle_list(processed_data, seed)
    click.echo(f"Resultado: {result}")


# --- 7. Punto de Entrada ---
if __name__ == '__main__':
    cli()