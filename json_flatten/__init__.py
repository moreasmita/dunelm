import json
from datetime import datetime

flatten_json_val = {}


def flatten(json_data, prefix=''):
    # print(type(json_data))
    # handle nested dictionary inside json values here
    if type(json_data) is dict:
        for val in json_data:
            flatten(json_data[val], prefix + val + '.')
            # print(json_data[val], prefix + val + '.')
    elif type(json_data) is list:
        i = 0
        for val in json_data:
            # handle dictionary inside list values here
            if type(val) is dict:
                for val_flt in val:
                    # print(val_flt)
                    flatten(val[val_flt], prefix + val_flt + '.')
                    # print(val[val_flt], prefix + val_flt + '.')
            else:
                flatten(val, prefix)
            i += 1
    else:
        flatten_json_val[prefix[:-1]] = json_data
    return flatten_json_val


def json_flatten(json_file_path: str, keys: [str], output_file_path: str) -> bool:
    """
:param keys:
:param json_file_path: Nested json input file (i.e. product_example.json) :param keys: A list of json key paths to be flattened
:param output_file_path: the flatten json output file path
:return True if json_flatten completed without error
"""
    try:
        with open(json_file_path, 'r') as file_handler:
            json_data = json.load(file_handler)
            output = flatten(json_data)
            print(output)
            output_subset = {}
            try:
                output_subset = {key: output[key] for key in keys}
            except KeyError as e:
                print("Keys are not matching for {}".format(e))
                return False

        try:
            with open(output_file_path, 'w') as outfile:
                json.dump(output_subset, outfile, indent=True)
        except IOError:
            print("File write fail please check...")
            return False

        return True
    except IOError:
        print("Unable to open Json File")
        return False


search_keys = [
    "attributes.primaryAttributes.skuName", "attributes.feedSkuBaseAttributeSet.skuCode",
    "attributes.primaryAttributes.productName", "attributes.feedProductBaseAttributeSet.productCode",
    "attributes.primaryAttributes.supplier",
    "attributes.productDescriptiveAttributes.Brand", "attributes.primaryAttributes.ean",
    "attributes.FormattedDimensions.BoxDimensions.height",
    "attributes.FormattedDimensions.BoxDimensions.length", "attributes.FormattedDimensions.BoxDimensions.quantity",
    "attributes.FormattedDimensions.BoxDimensions.weight", "attributes.FormattedDimensions.BoxDimensions.width"
    , "attributes.FormattedDimensions.NumberOfBoxes", "hierarchicalCategories.lvl0", "hierarchicalCategories.lvl1",
    "hierarchicalCategories.lvl2",
    "hierarchicalCategories.lvl3"]
input_file = "input_data/product_example.json"

# For file versioning add date here
now = datetime.now()
date_now = now.strftime("%Y%m%d_%H%M%S")
output_file = "output_data/product_example_flatten_{}.json".format(date_now)

if json_flatten(input_file, search_keys, output_file) is True:
    print("Data flatten successfully and written in file {}".format(output_file))
else:
    print("Something Wrong while flattening data please check...")
