import pytest
from click.testing import CliRunner
from src.cli import cli # Importamos el grupo principal 'cli' de tu archivo

# 1. Fixture Requerido
@pytest.fixture
def runner():
    """
    Fixture para instanciar el CliRunner 
    y compartirlo entre todos los tests.
    """
    return CliRunner()

# 2. Tests de Integracion 

def test_cli_main_help(runner):
    """
    Prueba que el comando principal 'cli' responde y muestra la ayuda.
    """
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    # Comprueba que los subgrupos están listados en la ayuda
    assert "clean" in result.output
    assert "numeric" in result.output
    assert "text" in result.output
    assert "struct" in result.output

#  Tests para el grupo 'clean' 

def test_clean_remove_missing(runner):
    """
    Prueba el comando: 'cli clean remove-missing ...'
    """
    # Argumentos que simulan la línea de comandos:
    # ... clean remove-missing 10 20.5 None "" 30 nan text
    args = [
        'clean',
        'remove-missing',
        '10', '20.5', 'None', '""', '30', 'nan', 'text'
    ]
    
    # Invocamos el comando 
    result = runner.invoke(cli, args)
    
    # 1. Comprobar que el comando se ejecuto sin errores
    assert result.exit_code == 0
    
    # 2. Comprobar la salida del CLI
    # Tu cli.py imprime "Resultado: [10, 20.5, 'text']"
    # click.echo añade un salto de linea (\n) al final.
    expected_output = "Resultado: [10, 20.5, 'text']\n"
    
    assert expected_output in result.output

def test_clean_fill_missing_with_option(runner):
    """
    Prueba el comando: 'cli clean fill-missing ... --fill-value ...'
    """
    # ... clean fill-missing 10 None --fill-value -1
    args = [
        'clean',
        'fill-missing',
        '10', 'None', 'nan',
        '--fill-value', '-1' # Probamos la opcion
    ]
    
    result = runner.invoke(cli, args)
    
    assert result.exit_code == 0
    # El helper 'process_input_value' convertira "-1" (str) a -1 (int)
    expected_output = "Resultado: [10, -1, -1]\n"
    assert expected_output in result.output

def test_clean_unique(runner):
    """
    Prueba el comando: 'cli clean unique ...'
    """
    # ... clean unique 10 20 10 30 20
    args = [
        'clean',
        'unique',
        '10', '20', '10', '30', '20'
    ]
    
    result = runner.invoke(cli, args)
    
    assert result.exit_code == 0
    expected_output = "Resultado: [10, 20, 30]\n"
    assert expected_output in result.output


def test_numeric_normalize_with_options(runner):
    """
    Prueba el comando: 'cli numeric normalize ... --min-val ... --max-val ...'
    """
    # ... numeric normalize 10 20 30 --min-val 0 --max-val 1
    args = [
        'numeric',
        'normalize',
        '10', '20', '30',
        '--min-val', '0',
        '--max-val', '1'
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert "Resultado: [0.0, 0.5, 1.0]\n" in result.output

def test_numeric_standardize(runner):
    """
    Prueba el comando: 'cli numeric standardize ...'
    """
    # ... numeric standardize 10 20 30
    args = [
        'numeric',
        'standardize',
        '10', '20', '30'
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert "Resultado: [-1.414, 0.0, 1.414]\n" in result.output

def test_numeric_clip(runner):
    """
    Prueba el comando: 'cli numeric clip ... --min-val ... --max-val ...'
    """
    # ... numeric clip 5 15 25 --min-val 10 --max-val 20
    args = [
        'numeric',
        'clip',
        '5', '15', '25',
        '--min-val', '10',
        '--max-val', '20'
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert "Resultado: [10, 15, 20]\n" in result.output

def test_numeric_to_integers(runner):
    """
    Prueba el comando: 'cli numeric to-integers ...'
    """
    # ... numeric to-integers 
    args = [
        'numeric',
        'to-integers',
        '10.5', "20", '30.0', "texto"
    ]
    assert result.exit_code == 0
    assert "Resultado: [10, 20, 30]\n" in result.output

def test_numeric_log_transform(runner):
    """
    Prueba el comando: 'cli numeric log-transform ...'
    """
    # ... numeric log-transform log-transform 1 10 100 -5 0
    args = [
        'numeric',
        'log-transform',
        '1', '10', '100', '-5', '0'
    ]
    assert result.exit_code == 0
    assert "Resultado: [0.0, 2.302, 4.6052]\n" in result.output


def test_text_remove_stops_with_options(runner):
    """
    Prueba el comando: 'cli text remove-stops ... --stop-word ...'
    """
    # ... text remove-stops "este es un texto" --stop-word "un" --stop-word "es"
    args = [
        'text',
        'remove-stops',
        'este es un texto de prueba',
        '--stop-word', 'un',
        '--stop-word', 'de'
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert "Resultado: este es texto prueba\n" in result.output

def test_text_tokenize(runner):
    """Prueba: cli text tokenize ..."""
    args = ['text', 'tokenize', 'Hola, mundo! Esto es 1 prueba.']
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    assert "Resultado: hola mundo esto es 1 prueba\n" in result.output

def test_text_remove_punctuation(runner):
    """Prueba: cli text remove-punctuation ..."""
    args = ['text', 'remove-punctuation', 'Test... con @símbolos! Sí.']
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    # Basado en la lógica anterior, 'í' y '!' se eliminan
    assert "Resultado: Test con smbolos S\n" in result.output

# --- Tests para 'struct' (Completos) ---

def test_struct_flatten(runner):
    """
    Prueba: cli struct flatten ...
    (Prueba el comportamiento de simulación del CLI)
    """
    # ... struct flatten 1 2 3 4
    args = ['struct', 'flatten', '1', '2', '3', '4']
    result = runner.invoke(cli, args)
    
    assert result.exit_code == 0
    # Prueba la salida de simulación de tu CLI
    assert "(Entrada simulada: [[1, 2], [3, 4]])\n" in result.output
    # Prueba el resultado final
    assert "Resultado: [1, 2, 3, 4]\n" in result.output

def test_struct_shuffle_with_seed(runner):
    """Prueba: cli struct shuffle ... --seed ..."""
    args = [
        'struct',
        'shuffle',
        '1', '2', '3', '4', '5',
        '--seed', '42' # Usamos una seed para un resultado predecible
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    # La seed 42 siempre dará este orden para [1, 2, 3, 4, 5]
    assert "Resultado: [3, 5, 2, 4, 1]\n" in result.output