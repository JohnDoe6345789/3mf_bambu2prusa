import lxml.etree as ET

from bambu_to_prusa.model_processing import clean_model_content, convert_model_file, extract_model_objects


SAMPLE_XML = """<?xml version='1.0' encoding='UTF-16'?>
<model xmlns="http://example.com" p:UUID="123" paint_color="abc" paint_seam="EDGE">
  <resources>
    <object id="1" type="model"><mesh /></object>
    <object id="2" type="support" />
  </resources>
</model>
"""


def test_clean_model_content_removes_bambu_attributes(tmp_path):
    content = clean_model_content(SAMPLE_XML)

    assert "paint_color" not in content
    assert "paint_seam" not in content
    assert "encoding" not in content
    assert "xmlns=\"http://example.com\"" not in content

    root = ET.fromstring(content)
    assert root.tag.endswith("model")
    assert root.attrib["{http://www.w3.org/XML/1998/namespace}lang"] == "en-US"


def test_extract_model_objects_filters_model_type(tmp_path):
    cleaned = clean_model_content(SAMPLE_XML)
    objects = extract_model_objects(cleaned)

    assert list(objects.keys()) == ["1"]
    assert objects["1"].attrib["type"] == "model"


def test_convert_model_file_reads_and_converts(tmp_path):
    model_path = tmp_path / "test.model"
    model_path.write_text(SAMPLE_XML, encoding="utf-8")

    filename, objects = convert_model_file(str(model_path))

    assert filename == "test.model"
    assert "1" in objects
    assert objects["1"].tag.endswith("object")
