# Imports
import math
import random
import re
from typing import Any 


def remove_missing_values(data: list) -> list:
    """
    Elimina los valores faltantes (None, "", nan) de una lista.

    Args:
        data (list): Lista de valores, incluyendo posibles faltantes.

    Returns:
        list: Lista de valores sin los elementos faltantes.
    """

    missing_values = {None, ""}
    cleaned_data = []

    for item in data:
        # 1. Chequea si es None o ""
        if item in missing_values:
            continue

        # 2. Chequea si es nan (requiere math.isnan)
        is_nan = False
        try:
            if isinstance(item, float) and math.isnan(item):
                is_nan = True
        except TypeError:
            pass  # No era un tipo compatible con isnan

        if is_nan:
            continue

        # 3. Si no es faltante, se añade
        cleaned_data.append(item)

    return cleaned_data


def filling_missing_values(data: list, fill_value: any = 0) -> list:
    """
    Rellena los valores faltantes (None, "", nan) de una lista
    con un valor específico.

    Args:
        data (list): Lista de valores, incluyendo posibles faltantes.
        fill_value (any, optional): Valor con el que rellenar los faltantes.
                                     Por defecto es 0. [cite: 40]

    Returns:
        list: Lista con los valores faltantes reemplazados.
    """
    missing_values = {None, ""}
    cleaned_data = []

    for item in data:
        # 1. Chequea si es None o ""
        if item in missing_values:
            cleaned_data.append(fill_value)  # <-- Usamos el argumento
            continue

        # 2. Chequea si es nan (requiere math.isnan)
        is_nan = False
        try:
            if isinstance(item, float) and math.isnan(item):
                is_nan = True
        except TypeError:
            pass  # No era un tipo compatible con isnan

        if is_nan:
            cleaned_data.append(fill_value)  # <-- Usamos el argumento
        else:
            # 3. Si no es faltante, se añade el original
            cleaned_data.append(item)

    return cleaned_data


def remove_duplicated_values(data: list) -> list:
    """
    Elimina los valores duplicados de una lista, conservando el orden.

    Args:
        data (list): Lista de valores.

    Returns:
        list: Lista con valores únicos.
    """
    # dict.fromkeys() es una forma rápida de eliminar duplicados
    # y conserva el orden de aparición (en Python 3.7+).
    return list(dict.fromkeys(data))


#
#  2. FUNCIONES NUMÉRICAS (Numeric)
#


def normalize_min_max(data: list, new_min: float = 0.0, new_max: float = 1.0) -> list:
    """
    Normaliza valores numéricos usando el método min-max.

    Args:
        data (list): Lista de valores numéricos.
        new_min (float, optional): Nuevo mínimo del rango. Por defecto 0.0.
        new_max (float, optional): Nuevo máximo del rango. Por defecto 1.0.

    Returns:
        list: Lista de valores normalizados.
    """
    if not data:
        return []

    # Filtra solo valores numéricos (int/float)
    numeric_data = [x for x in data if isinstance(x, (int, float))]
    if not numeric_data:
        return []

    min_val = min(numeric_data)
    max_val = max(numeric_data)
    range_val = max_val - min_val

    if range_val == 0:
        # Si todos los valores son iguales, devuelve el nuevo mínimo
        return [new_min for _ in numeric_data]

    # Fórmula de normalización Min-Max
    # X_norm = new_min + ((X - X_min) * (new_max - new_min)) / (X_max - X_min)
    return [
        new_min + ((x - min_val) * (new_max - new_min)) / range_val
        for x in numeric_data
    ]


def standardize_z_score(data: list) -> list:
    """
    Estandariza valores numéricos usando el método z-score.

    Args:
        data (list): Lista de valores numéricos.

    Returns:
        list: Lista de valores estandarizados.
    """
    if not data:
        return []

    # Filtra solo valores numéricos
    numeric_data = [x for x in data if isinstance(x, (int, float))]
    if not numeric_data:
        return []

    n = len(numeric_data)
    if n == 0:
        return []

    # 1. Calcular la media (μ)
    mean = sum(numeric_data) / n

    # 2. Calcular la desviación estándar (σ)
    variance = sum((x - mean) ** 2 for x in numeric_data) / n
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        # Si la desviación es 0, todos los valores son iguales (a la media)
        # El Z-score es 0 para todos.
        return [0.0 for _ in numeric_data]

    # 3. Aplicar fórmula Z-score: Z = (X - μ) / σ
    return [(x - mean) / std_dev for x in numeric_data]


def clip_values(data: list, min_val: float, max_val: float) -> list:
    """
    Recorta valores numéricos a un rango (clipping).

    Args:
        data (list): Lista de valores numéricos.
        min_val (float): Valor mínimo para recortar.
        max_val (float): Valor máximo para recortar.

    Returns:
        list: Lista de valores recortados.
    """
    if min_val > max_val:
        raise ValueError(
            "El valor mínimo (min_val) no puede ser mayor que el valor máximo (max_val)."
        )

    clipped_data = []
    for item in data:
        if not isinstance(item, (int, float)):
            continue  # Ignora valores no numéricos

        if item < min_val:
            clipped_data.append(min_val)
        elif item > max_val:
            clipped_data.append(max_val)
        else:
            clipped_data.append(item)

    return clipped_data


def convert_to_integers(data: list) -> list:
    """
    Convierte una lista de strings a enteros.

    Args:
        data (list): Lista de strings.

    Returns:
        list: Lista de valores convertidos a enteros.
              Los no numéricos se excluyen.
    """
    int_values = []
    for item in data:
        try:
            # Intenta convertir el string a float primero (para "10.0")
            # y luego a int.
            int_val = int(float(item))
            int_values.append(int_val)
        except (ValueError, TypeError):
            # Si falla (ej. "texto" o None), se excluye
            continue
    return int_values


def logarithmic_transform(data: list) -> list:
    """
    Aplica una transformación logarítmica (log natural).

    Args:
        data (list): Lista de valores.

    Returns:
        list: Lista de valores transformados (solo números positivos originales).
    """
    transformed_data = []
    for item in data:
        # Comprueba si es numérico (int o float) Y positivo
        if isinstance(item, (int, float)) and item > 0:
            transformed_data.append(math.log(item))
    return transformed_data


#
# 3. FUNCIONES DE TEXTO (Text)
#


def tokenize_text(text: str) -> str:
    """
    Tokeniza texto en palabras, seleccionando solo alfanuméricos y
    convirtiendo a minúsculas.

    Args:
        text (str): Texto a procesar.

    Returns:
        str: Texto procesado (palabras alfanuméricas en minúsculas unidas por espacio).
    """
    if not isinstance(text, str):
        return ""

    # 1. Convertir a minúsculas
    text = text.lower()
    # 2. Buscar todas las secuencias de caracteres alfanuméricos (palabras)
    words = re.findall(r"\b\w+\b", text)
    # 3. Unir de nuevo como "Texto procesado"
    return " ".join(words)


def select_alphanumeric_spaces(text: str) -> str:
    """
    Selecciona solo caracteres alfanuméricos y espacios del texto.

    Args:
        text (str): Texto a procesar.

    Returns:
        str: Texto procesado.
    """
    if not isinstance(text, str):
        return ""
    # Reemplaza todo lo que NO sea alfanumérico o espacio
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


def remove_stop_words(text: str, stop_words: list) -> str:
    """
    Elimina stop-words de un texto (debe estar en minúsculas).

    Args:
        text (str): Texto a procesar.
        stop_words (list): Lista de stop words a eliminar.

    Returns:
        str: Texto procesado sin las stop words.
    """
    if not isinstance(text, str):
        return ""

    words = text.lower().split()
    stop_words_set = set(stop_words)
    cleaned_words = [word for word in words if word not in stop_words_set]
    return " ".join(cleaned_words)


#
# --- 4. FUNCIONES DE ESTRUCTURA (Struct) ---
#


def flatten_list(data: list) -> list:
    """
    Aplana una lista de listas.

    Args:
        data (list): Una lista de listas.

    Returns:
        list: Una lista aplanada.
    """
    flattened = []
    for item in data:
        # Comprueba si el item es una lista
        if isinstance(item, list):
            # Si es lista, AÑADE CADA ELEMENTO (extend)
            flattened.extend(item)
        else:
            # Si no es lista, AÑADE EL ITEM (append)
            flattened.append(item)

    return flattened


def shuffle_list(data: list, seed: int | None = None) -> list:
    """
    Mezcla aleatoriamente una lista de valores.

    Args:
        data (list): Lista de valores.
        seed (int | None, optional): Semilla para asegurar reproducibilidad.
                                      Por defecto es None.

    Returns:
        list: Lista de valores mezclados.
    """
    if seed is not None:
        random.seed(seed)

    shuffled_list = data.copy()
    random.shuffle(shuffled_list)
    return shuffled_list
