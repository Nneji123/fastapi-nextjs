"""App helper functions"""
import os

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


lable_lang_mapping = {"Plain JS": "JavaScript", "NodeJS": "JavaScript"}


def add_examples(openapi_schema: dict, docs_dir):
    path_key = "paths"
    code_key = "x-codeSamples"

    for folder in os.listdir(docs_dir):
        base_path = os.path.join(docs_dir, folder)
        files = [
            f
            for f in os.listdir(base_path)
            if os.path.isfile(os.path.join(base_path, f))
        ]
        for f in files:
            parts = f.split("-")
            if len(parts) >= 2:
                route = "/" + "/".join(parts[:-1])
                method = parts[-1].split(".")[0]
                print(f"[{path_key}][{route}][{method}][{code_key}]")

                if route in openapi_schema[path_key]:
                    if code_key not in openapi_schema[path_key][route][method]:
                        openapi_schema[path_key][route][method].update({code_key: []})

                    openapi_schema[path_key][route][method][code_key].append(
                        {
                            "lang": lable_lang_mapping[folder],
                            "source": open(os.path.join(base_path, f), "r").read(),
                            "label": folder,
                        }
                    )
            else:
                print(f"Error in adding examples code to openapi {f}")

    return openapi_schema
