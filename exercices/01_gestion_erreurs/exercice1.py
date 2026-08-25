"""Exercise 1: structured error handling with try/except."""


def convertir_prix(value: str | float | int | None) -> float | None:
    """Convert a raw price value from the POS export into a float.

    Handles common dirty-data formats: French decimal comma ("4,20"),
    euro symbol ("4.20€"), missing values, and already-numeric input.

    Args:
        value: Raw price as returned by the CSV export. Can be a string
            (typical case), an int/float (e.g. from a JSON/API source),
            or None (missing value).

    Returns:
        The parsed price as a float, or None if the value could not
        be converted.
    """
    if isinstance(value, (int, float)):
        return float(value)
    else:
        try:
            return float(value.replace(",", ".").replace("€", ""))
        except (ValueError, TypeError, AttributeError):
            print(f"Invalid Value : {value!r}")
            return None




if __name__ == "__main__":
    print(convertir_prix("4.20"))
    print(convertir_prix("4,20"))
    print(convertir_prix("4.20€"))
    print(convertir_prix(""))
    print(convertir_prix(None))
    print(convertir_prix("abc"))
    print(convertir_prix(4.5))      # déjà un float