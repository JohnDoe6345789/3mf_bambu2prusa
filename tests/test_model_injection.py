import lxml.etree as ET

from bambu_to_prusa.model_injection import build_prusa_model
from bambu_to_prusa.template_paths import get_template_paths


def test_build_prusa_model_injects_objects(tmp_path):
    template_path = get_template_paths()["models_template"]
    object_xml = ET.fromstring('<object id="1" type="model"><mesh /></object>')

    tree = build_prusa_model({"1": object_xml}, template_path)
    model = tree.getroot()
    resources = model.find(".//{*}resources")
    build = model.find(".//{*}build")

    assert any(child.attrib.get("id") == "1" for child in resources)
    assert any(item.attrib.get("objectid") == "1" for item in build)
