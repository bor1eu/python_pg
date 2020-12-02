import os
import tempfile
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--key", type=str, help="key")
parser.add_argument("--val", type=str, help="value")
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
if not(os.path.isfile(storage_path)):
    with open(storage_path, 'w', encoding='utf-8') as f:
        pass
if not(args.key is None):
    with open(storage_path, 'r', encoding='utf-8') as f:
        try:
            storage_data = json.load(f)
        except:
            storage_data = {}
    if not(args.val is None):
        if not(args.key in storage_data):
            storage_data[args.key] = []
        storage_data[args.key] += [args.val]
        with open(storage_path, 'w', encoding='utf-8') as f:
            json.dump(storage_data, f, ensure_ascii=False)
        # with open(storage_path, 'r') as f:
        #     storage_data = json.load(f)
        #     result = [x[args.val] for x in storage_data if x[args.key] == args.key]
        #     print(', '.join(result))
    else:
        if args.key in storage_data:
            result = storage_data[args.key]
        else:
            result = []
        print(', '.join(result))
else:
    pass

