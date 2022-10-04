import datetime
import json
import logging
import os

import jsonschema
# Command line parsing
import yaml

from build.libs.dataloaders import load_wikidata_sparql_data
from build.libs.postprocess import postprocess_data
from build.libs.utils import clear_dir


def generate(descriptor_path: str, dest_path: str, clear_directory: bool):
    # Descriptor file loading
    logging.info("Loading and validating %s...", descriptor_path)
    with open(descriptor_path) as descriptor_file:
        descriptor = json.load(descriptor_file)

    # Descriptor validation
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "schemas",
                           ".descriptor.schema.json")) as schema_file:
        schema = json.load(schema_file)
        jsonschema.validate(descriptor, schema)

    # A report object with info about what's been generated
    report_date = datetime.datetime.now()
    report = {
        "date": report_date.isoformat(timespec="seconds"),
        "title": descriptor["title"],
        "description": descriptor["description"],
        "files": []
    }

    langs = [descriptor["language"]] + descriptor["variantLanguages"]

    if clear_directory:
        clear_dir(dest_path)

    # For each language
    for lang in langs:

        # First, query the data
        logging.info("Querying data for language \"%s\"...", lang)

        # current directory for the main language, variant/[lang] for the other languages
        lang_dir_path = "." if lang == descriptor["language"] else os.path.join("variant", lang)
        data_dir_path = os.path.join(dest_path, lang_dir_path)

        source_type = descriptor["source"]["type"]
        source_file_path = os.path.join(os.path.dirname(descriptor_path), descriptor["source"]["file"])

        if source_type == "wikidata/sparql":
            logging.info("Querying data from Wikidata SPARQL service...")
            data = load_wikidata_sparql_data(source_file_path, lang)
        else:
            raise ValueError("Not supported source type:" + source_type)

        if "postProcesses" in descriptor:
            postprocess_data(data, descriptor["postProcesses"])

        for format in descriptor["formats"]:
            if format == "json":
                data_content = json.dumps(data, indent=4, ensure_ascii=False)

            elif format == "yaml":
                data_content = yaml.dump(data, default_flow_style=False, sort_keys=False)

            else:
                raise Exception("Unsupported file format: " + format)

            # Write the data content
            data_file_path = os.path.join(data_dir_path, descriptor["name"] + "." + format)
            logging.info("Writing %s...", data_file_path)
            os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
            with open(data_file_path, "w", encoding='utf-8') as data_file:
                data_file.write(data_content)

            report["files"].append({
                "main": lang == descriptor["language"],
                "language": lang,
                "format": format,
                "path": os.path.relpath(data_file_path, dest_path).replace("\\", "/"),
                "size": len(data_content),
                "itemCount": len(data)
            })

    with open(os.path.join(dest_path, ".report.json"), "w", encoding='utf-8') as report_file:
        json.dump(report, report_file, indent=4)


def generate_all(source_tree_dir_path: str, dest_tree_dir_path: str, clear_directory: bool):
    """
    Walks through a directory tree and laucnh mock data fil generation for each ".descriptor.json" file encountered
    """
    list_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(source_tree_dir_path):
        for filename in filenames:
            if filename == ".descriptor.json" :
                descriptor_file_path = os.path.join(dirpath, filename)
                dest_directory_path = os.path.join(dest_tree_dir_path, os.path.relpath(dirpath, source_tree_dir_path))
                logging.info("Generating '%s' into '%s'...", descriptor_file_path, dest_directory_path)
                generate(descriptor_file_path, dest_directory_path, clear_directory)
            