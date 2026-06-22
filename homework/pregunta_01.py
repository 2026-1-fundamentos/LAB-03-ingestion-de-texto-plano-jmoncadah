"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd

    # Cargar el archivo línea por línea
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Limpiar líneas: quitar vacías y separadores
    lines = [line.rstrip() for line in lines if line.strip() != ""]
    lines = [line for line in lines if not set(line) == {"-"}]  # quitar línea de -----

    # Nombres de columnas en minúsculas con guiones bajos
    columns = ["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"]

    # Separar encabezado y datos
    data_lines = lines[2:]  # las dos primeras líneas son encabezados visuales

    clusters = []
    current_row = []

    for line in data_lines:
        # Si la línea empieza con número => nueva fila
        if line.lstrip()[0].isdigit():
            # Guardar la fila anterior si existe
            if current_row:
                clusters.append(current_row)
            # Dividir en partes
            parts = line.split()
            cluster = parts[0]
            cantidad = parts[1]
            porcentaje = parts[2] + " " + parts[3]  # número + %
            palabras = " ".join(parts[4:])
            current_row = [cluster, cantidad, porcentaje, palabras]
        else:
            # Continuación de las palabras clave
            current_row[3] += " " + line.strip()

    # Agregar última fila
    if current_row:
        clusters.append(current_row)

    # Crear DataFrame
    df = pd.DataFrame(clusters, columns=columns)

    # Limpiar palabras clave: un solo espacio y comas con espacio
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)      # limpiar espacios extra
        .str.replace(",\s*", ", ", regex=True)      # coma + espacio correcto
        .str.strip()                                # quitar espacios al inicio/fin
        .str.rstrip(".")                            # quitar punto final si existe
    )


    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)
    df["porcentaje_de_palabras_clave"] = df["porcentaje_de_palabras_clave"].str.replace("%", "").str.replace(",", ".").astype(float)
    return df


if __name__ == "__main__":
    df = pregunta_01()
    print(df.columns)