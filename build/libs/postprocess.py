import datetime
import logging

from dateutil import parser


def _postprocess_add_id(item: dict, property: str, parameters: dict, item_number: int):
    old = item.copy();
    item.clear()
    item[property] = item_number
    item.update(old)


def _postprocess_format_as_iso_date(item: dict, property: str, parameters: dict, item_number: int):
    old_value = item[property]
    new_value = parser.parse(old_value).date().isoformat()
    item[property] = new_value
    logging.debug("Post-processed property '%s' from '%s' to ISO0601 date formatted value '%s'", property, old_value, new_value)


def _postprocess_split(item: dict, property: str, parameters: dict, item_number: int):
    if not "separator" in parameters :
        raise ValueError("Expected 'separator' parameter")
    item[property] =  item[property].split(parameters["separator"])
    logging.debug("Post-processed property '%s' splitting it with seperator '%s' to an %s item list", property, parameters["separator"], len(item[property]))


def _postprocess_item(item: dict, postprocesses: dict, item_number: int):
    """
    Post-processes the properties of an object
    """
    postprocess: dict
    for postprocess in postprocesses:
        postprocess_name = postprocess["name"]
        postprocess_property = postprocess["property"]
        postprocess_parameters = postprocess.get("parameters", {})
        if postprocess_name == "addId":
            _postprocess_add_id(item, postprocess_property, postprocess_parameters, item_number)

        if postprocess_name == "formatAsIsoDate":
            _postprocess_format_as_iso_date(item, postprocess_property, postprocess_parameters, item_number)

        if postprocess_name == "split":
            _postprocess_split(item, postprocess_property, postprocess_parameters, item_number)


def postprocess_data(data: dict, postprocesses: dict):
    item_number = 0
    for item in data:
        _postprocess_item(item, postprocesses, item_number)
        item_number += 1
