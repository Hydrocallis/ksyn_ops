import importlib.util
import os


# アドオンのパスを取得
addon_path = os.path.dirname(os.path.realpath(__file__))

class_paths = [
    ("operators", "test_class", "testclass"),
    ("operators", "test_class", "testclass1"),
    ("operators", "test_class", "testclass2"),
    ("operators", "test_class", "testclass3"),

]
KSYNOPS_OT_classes = []
prefix = "KSYNOPS_OT_"

def load_classes(class_paths):
    classes = []

    for path_parts, module_name, class_name in class_paths:
        module_path = os.path.join(addon_path, *path_parts.split("/"), module_name + ".py")
        spec = importlib.util.spec_from_file_location(class_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)
        classes.append(cls)

    return classes

loaded_classes = load_classes(class_paths)
print(loaded_classes)
