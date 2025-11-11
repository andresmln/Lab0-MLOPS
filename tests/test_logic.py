# tests/test_logic.py
import pytest
from numpy import nan # Importamos nan para los casos de prueba
from src.preprocessing import * # Importamos todas las funciones que vamos a probar
# Usamos @pytest.mark.parametrize para probar múltiples casos
# Aquí probamos con 'input_list' y 'expected_output'
# --- 1. Fixture Requerido  ---
@pytest.fixture
def sample_numeric_list():
    """
    Fixture que proporciona una lista numérica estándar para varias pruebas.
    """
    return [10, 20, 30, 40, 50]

@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        # Caso 1: Lista estándar con todos los tipos de faltantes
        ([10, None, 20.5, "", "text", nan, 30, float('nan'), 40, " "], [10, 20.5, "text", 30, 40, " "]),
        
        # Caso 2: Lista sin valores faltantes
        ([1, 2, 3, "hello"], [1, 2, 3, "hello"]),
        
        # Caso 3: Lista solo con valores faltantes
        ([None, "", nan, float('nan')], []),
        
        # Caso 4: Lista vacía
        ([], []),
        
        # Caso 5: Lista con ceros y Falses (que no deben eliminarse)
        ([0, False, 1, True], [0, False, 1, True])
    ]
)
def test_remove_missing_values(input_list, expected_output):
    """
    Prueba unitaria para la función remove_missing_values.
    Comprueba varios escenarios definidos en parametrize.
    """
    # Llama a la función que se está probando
    result = remove_missing_values(input_list)
    
    # Comprueba que el resultado es el esperado
    assert result == expected_output, f"Falló para la entrada {input_list}"


# ... (El test de remove_missing_values va aquí) ...

@pytest.mark.parametrize(
    "input_list, fill_value, expected_output",
    [
        # Caso 1: Relleno con 0 (comportamiento por defecto)
        ([10, None, 20.5, "", "text", nan], 0, [10, 0, 20.5, 0, "text", 0]),
        
        # Caso 2: Relleno con un string "REPLACED"
        ([10, None, "text", nan], "REPLACED", [10, "REPLACED", "text", "REPLACED"]),
        
        # Caso 3: Relleno con un número diferente (e.g., -1)
        ([10, None, 20, ""], -1, [10, -1, 20, -1]),

        # Caso 4: Relleno en una lista vacía
        ([], "test", []),

        # Caso 5: Relleno en una lista sin faltantes
        ([1, 2, 3], 0, [1, 2, 3]),

        # Caso 6: Relleno con None (raro, pero debe funcionar)
        ([10, None, ""], None, [10, None, None])
    ]
)
def test_filling_missing_values(input_list, fill_value, expected_output):
    """
    Prueba unitaria para la función filling_missing_values.
    Comprueba varios escenarios con diferentes valores de relleno.
    """
    # Llama a la función que se está probando con los dos argumentos
    result = filling_missing_values(input_list, fill_value)
    
    # Comprueba que el resultado es el esperado
    assert result == expected_output, f"Falló para la entrada {input_list} con fill_value={fill_value}"

@pytest.mark.parametrize(
    "data, new_min, new_max, expected",
    [
        # Caso 1: Normalización 0-1 (defecto) [cite: 99]
        ([10, 20, 30, 40, 50], 0.0, 1.0, [0.0, 0.25, 0.5, 0.75, 1.0]),
        # Caso 2: Normalización 1-2
        ([10, 20, 30, 40, 50], 1.0, 2.0, [1.0, 1.25, 1.5, 1.75, 2.0]),
        # Caso 3: Con valores no numéricos (deben ser ignorados)
        ([10, "skip", 20, 30, 40, 50], 0.0, 1.0, [0.0, 0.25, 0.5, 0.75, 1.0]),
        # Caso 4: Todos los valores iguales
        ([5, 5, 5], 0.0, 1.0, [0.0, 0.0, 0.0]),
    ]
)
def test_normalize_min_max(data, new_min, new_max, expected):
    """Prueba la normalización min-max."""
    # pytest.approx es necesario para comparar floats
    assert normalize_min_max(data, new_min, new_max) == pytest.approx(expected)

def test_standardize_z_score(sample_numeric_list):
    """Prueba la estandarización z-score usando el fixture."""
    data = sample_numeric_list # [10, 20, 30, 40, 50]
    # Media = 30
    # StdDev = sqrt( ((10-30)**2 + ... + (50-30)**2) / 5 ) = sqrt( (400+100+0+100+400) / 5 ) = sqrt(200)
    std_dev = math.sqrt(200)
    expected = [
        (10 - 30) / std_dev,
        (20 - 30) / std_dev,
        (30 - 30) / std_dev,
        (40 - 30) / std_dev,
        (50 - 30) / std_dev,
    ]
    # expected approx: [-1.414, -0.707, 0.0, 0.707, 1.414]
    assert standardize_z_score(data) == pytest.approx(expected)

@pytest.mark.parametrize(
    "data, min_val, max_val, expected",
    [
        ([5, 10, 15, 20, 25], 10, 20, [10, 10, 15, 20, 20]),
        ([10, 20, 30], 0, 1, [1, 1, 1]), # Rango por defecto [cite: 100] (Oops, el PDF dice 0 y 1, pero 10,20,30 están fuera. El test debe ser realista)
        ([0.5, 1.5, 2.5], 1.0, 2.0, [1.0, 1.5, 2.0]), # Test realista
        ([10, "skip", 20], 0, 15, [10, 15]), # Ignora no numéricos
    ]
)
def test_clip_values(data, min_val, max_val, expected):
    """Prueba el recorte (clipping) de valores."""
    assert clip_values(data, min_val, max_val) == pytest.approx(expected)

@pytest.mark.parametrize(
    "data, expected",
    [
        (["10", "20.5", "texto", "30.0", nan, None], [10, 20, 30]),
        (["-5", "0", "1.9"], [-5, 0, 1]),
    ]
)
def test_convert_to_integers(data, expected):
    """Prueba la conversión de strings a enteros[cite: 63]."""
    assert convert_to_integers(data) == expected

@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 10, 100], [math.log(1), math.log(10), math.log(100)]),
        # Ignora 0, negativos y no numéricos [cite: 67]
        ([-10, 0, 5, "texto", 20], [math.log(5), math.log(20)]),
    ]
)
def test_logarithmic_transform(data, expected):
    """Prueba la transformación logarítmica."""
    assert logarithmic_transform(data) == pytest.approx(expected)

# --- 4. Tests para Funciones de Texto (Text) ---

@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hello, world! 123.", "hello world 123"),
        ("Test... con acentos?", "test con acentos"), # \w+ incluye acentos
        ("Puntuación!!!", "puntuación"),
    ]
)
def test_tokenize_text(text, expected):
    """Prueba la tokenización (alfanuméricos y minúsculas)[cite: 68]."""
    assert tokenize_text(text) == expected

@pytest.mark.parametrize(
    "text, expected",
    [
        ("Hi! This is test #1.", "Hi This is test 1"),
        ("Texto con @símbolos$ y \t tabs.", "Texto con smbolos y \t tabs"), # \s incluye tabs
    ]
)
def test_select_alphanumeric_spaces(text, expected):
    """Prueba la selección de alfanuméricos y espacios[cite: 71]."""
    assert select_alphanumeric_spaces(text) == expected

@pytest.mark.parametrize(
    "text, stop_words, expected",
    [
        ("este es un texto de prueba", ["un", "de"], "este es texto prueba"),
        ("MAYÚSCULAS y minúsculas", ["y"], "mayúsculas minúsculas"), # Debe convertir a minúsculas [cite: 74]
    ]
)
def test_remove_stop_words(text, stop_words, expected):
    """Prueba la eliminación de stop-words."""
    assert remove_stop_words(text, stop_words) == expected

# --- 5. Tests para Funciones de Estructura (Struct) ---

@pytest.mark.parametrize(
    "data, expected",
    [
        ([[1, 2], [3, 4], [5]], [1, 2, 3, 4, 5]),
        ([1, [2, 3], 4], [1, 2, 3, 4]), # Testeando la implementación (no es lista de listas)
        ([[1], [], [2, 3]], [1, 2, 3]),
    ]
)
def test_flatten_list(data, expected):
    """Prueba el aplanamiento de listas[cite: 82]."""
    # Nota: Tu implementación maneja listas mixtas, 
    # si la práctica exigía [[1], [2]] -> [1, 2] y fallar con [1, [2]],
    # la implementación y el test deberían cambiar.
    assert flatten_list(data) == expected

def test_shuffle_list_reproducibility():
    """Prueba la mezcla aleatoria y la reproducibilidad con seed[cite: 87]."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 1. Con la misma seed, el resultado es idéntico
    shuffled_1 = shuffle_list(data, seed=42)
    shuffled_2 = shuffle_list(data, seed=42)
    assert shuffled_1 == shuffled_2
    
    # 2. Con diferente seed, el resultado es diferente
    shuffled_3 = shuffle_list(data, seed=101)
    assert shuffled_1 != shuffled_3
    
    # 3. La lista original no debe ser modificada
    assert data == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # 4. Sin seed, el resultado debe ser (muy probablemente) diferente
    shuffled_4 = shuffle_list(data, seed=None)
    shuffled_5 = shuffle_list(data, seed=None)
    # Esto podría fallar 1 en N! veces, pero es una prueba razonable
    if data == shuffled_4: # Si no mezcló, intenta de nuevo
        shuffled_4 = shuffle_list(data, seed=None)
    assert data != shuffled_4
    assert shuffled_4 != shuffled_5 # Probabilidad muy alta de ser cierto