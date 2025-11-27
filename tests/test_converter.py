import os
import zipfile

import lxml.etree as ET

from bambu_to_prusa.converter import BambuToPrusaConverter

SAMPLE_XML = """<?xml version='1.0' encoding='UTF-16'?>
<model xmlns="http://example.com" p:UUID="123" paint_color="abc" paint_seam="EDGE">
  <resources>
    <object id="1" type="model"><mesh /></object>
  </resources>
</model>
"""


def create_sample_archive(tmp_path):
    input_dir = tmp_path / "input"
    objects_dir = input_dir / "3D" / "Objects"
    objects_dir.mkdir(parents=True)
    (objects_dir / "test.model").write_text(SAMPLE_XML, encoding="utf-8")

    archive_path = tmp_path / "sample.3mf"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for folder, _, files in os.walk(input_dir):
            for filename in files:
                file_path = os.path.join(folder, filename)
                arcname = os.path.relpath(file_path, input_dir)
                archive.write(file_path, arcname)
    return archive_path


def test_convert_archive_produces_prusa_zip(tmp_path):
    archive_path = create_sample_archive(tmp_path)
    output_path = tmp_path / "output.3mf"

    converter = BambuToPrusaConverter()
    converter.convert_archive(str(archive_path), str(output_path))

    assert output_path.exists()
    with zipfile.ZipFile(output_path, "r") as output_zip:
        names = output_zip.namelist()
        assert any(name.endswith("3D/Objects/test.model") for name in names)
        assert "_rels/.rels" in names

        with output_zip.open("3D/Objects/test.model") as model_file:
            model_content = model_file.read()
            model_root = ET.fromstring(model_content)
            assert model_root.findall(".//{*}object")
