import logging
from pathlib import Path

from bambu_to_prusa.converter import BambuToPrusaConverter


def convert_file(input_path: str, output_path: str) -> str:
    converter = BambuToPrusaConverter()
    return converter.convert_archive(input_path, output_path)


def main():
    input_path = Path("input.3mf")
    output_path = Path("output.3mf")
    converter = BambuToPrusaConverter()
    converter.convert_archive(str(input_path), str(output_path))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
