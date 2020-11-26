from exercise_one import ExerciseOne
from exercise_two import ExerciseTwo
import json


def import_data(file_name: str):
    """
    Method handles data importation for exercises

    Important: File name must be correct, and this module import data from the
    same execution path, se be sure json data is inside the folder of this file.

    :param file_name: File name to get data
    :type file_name: str
    :return: Json Formatter data from file
    :rtype: dict
    """
    try:
        with open(file_name) as data_file:
            data_content = json.load(data_file)
    except FileNotFoundError:
        raise Exception(f"Por favor tener el archivo {file_name} an la ruta de trabajo")

    return data_content


def main():
    """
    Main Function to call both exercises.
    """
    print("Hello! Vamos a ejecutar los codigos de ambos ejercicios :)")

    # Exercise 1 responses
    input(
        "Por Favor, Presiona una tecla para mostrar los resultados del ejercicio 1..."
    )
    print()
    exercise_one_data = import_data("data1.json")
    exercise_one = ExerciseOne(exercise_one_data)
    print(
        f"El promedio de la variable 1 es un total de: {exercise_one.get_var_1_avg()}"
    )
    print(
        f"La suma de variable 2 para la provincia 2 es de: {exercise_one.get_prov_2_sum_var_2()}"
    )
    print(
        f"El maximo de la variable 1 en la region 4 es: {exercise_one.get_reg_4_var_1_max()}"
    )
    print()

    # Exercise 2 responses
    input(
        "Por Favor, Presiona una tecla para mostrar los resultados del ejercicio 2..."
    )
    print()
    exercise_two_data = import_data("data2.json")
    exercise_two = ExerciseTwo(exercise_two_data)
    print("El promedio de tiempo de espera en zonas A y B")
    print(json.dumps(exercise_two.get_zones_a_b_avg(), indent=4))
    print()
    print(
        f"El porcentaje de ciclos de faena que incluyeron alguna area de trabajo tipo 2 es:"
        f" {exercise_two.get_w_zones_percentage_on_cycles()}%"
    )
    print()
    asset, percent = exercise_two.get_asset_w_higher_percent_of_entering_both_w_zones()
    print(
        f"El camion con el mayor porcentaje de entrada en zonas 'AW' y 'BW', "
        f"incluyendo todos los ciclos, es {asset}, con un porcentaje del {percent}%"
    )


main()
