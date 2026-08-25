"""Exercise 2 bis: Handling LOGGING destination(s)"""

import logging

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("pipeline-exo2.log")
file_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)

"""
logger.info("Pipeline started")
logger.warning("Missing value found, using default")
logger.error("Failed to parse row 42")
logger.debug("Technical details for dev, ex: intermediate values, internal steps")
logger.critical("Program had to stop")
"""

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
            logger.warning(f"Invalid Value : {value!r}")
            return None




if __name__ == "__main__":
    logger.info("Pipeline started")
    print(convertir_prix("4.20"))
    print(convertir_prix("4,20"))
    print(convertir_prix("4.20€"))
    print(convertir_prix(""))
    print(convertir_prix(None))
    print(convertir_prix("abc"))
    print(convertir_prix(4.5))      # already a float