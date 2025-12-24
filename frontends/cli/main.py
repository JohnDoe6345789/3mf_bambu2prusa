"""Command-line interface implementation for Bambu2Prusa converter."""

import argparse
import logging
import sys
from pathlib import Path

from bambu_to_prusa.converter import BambuToPrusaConverter


def main():
    """Main CLI entrypoint for Bambu2Prusa converter."""
    parser = argparse.ArgumentParser(
        description="Convert Bambu Studio 3mf files to PrusaSlicer-compatible 3mf files."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to input Bambu Studio 3mf file",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to output PrusaSlicer 3mf file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s"
    )
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix.lower() == ".3mf":
        print(f"Error: Input file must be a .3mf file: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Validate output path
    output_path = Path(args.output)
    if not output_path.suffix.lower() == ".3mf":
        print(f"Error: Output file must have .3mf extension: {args.output}", file=sys.stderr)
        sys.exit(1)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"Converting: {input_path} -> {output_path}")
        converter = BambuToPrusaConverter()
        converter.convert_archive(str(input_path), str(output_path))
        print(f"Success! Output file created: {output_path}")
        sys.exit(0)
    except Exception as exc:
        logging.error("Conversion failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
