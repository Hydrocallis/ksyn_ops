
import bpy,importlib,os

from bpy.utils import register_class, unregister_class

from ..operators.pie_op import AutoSommth as KSYNOPS_OT_AutoSommth
from ..operators.pie_op import Setting as KSYNOPS_OT_Setting
try:
    from ..operators.pie_op import pie4 as KSYNOPS_OT_pie4
    from ..operators.pie_op import pie8 as KSYNOPS_OT_pie8
    from ..operators.pie_op import pie9 as KSYNOPS_OT_pie9
    from ..operators.pie_op import pie18 as KSYNOPS_OT_pie18
    from ..operators.pie_op import pie19 as KSYNOPS_OT_pie19
    from ..operators.pie_op import pie20 as KSYNOPS_OT_pie20
except ImportError:
    pass


# クラス名を変えた場合はブレンダーを再起動する必要があるみたい。
# 一見、再読み込みで元のクラス名が読み込まれそうだが、あくまでもレジストレーションのクラス名が読み込まれるので、
# レジストレーションの設定でクラス名が決まっていればOK。で、再読み込みはあくまでもファイルだけが読み込まれる仕様
try:
    modules = [
        (["operators"],"pie_op",[
        KSYNOPS_OT_AutoSommth,
        KSYNOPS_OT_Setting,
        KSYNOPS_OT_pie4,
        KSYNOPS_OT_pie8,
        KSYNOPS_OT_pie9,
        KSYNOPS_OT_pie18,
        KSYNOPS_OT_pie19,
        KSYNOPS_OT_pie20,
        ])
        ]
except NameError:
    pass


clases = []
for path, modu ,cls in modules:
    for cs in cls:
        clases.append(cs)

# オンにした場合は最初のレジストレーションでプリントされる
debug=False


def register_classes():
    for c in clases:
        if debug:
            print("REGISTERING", c)
        register_class(c)

def unregister_classes():
    for c in clases:
        if debug:
            print("UN-REGISTERING", c)

        unregister_class(c)