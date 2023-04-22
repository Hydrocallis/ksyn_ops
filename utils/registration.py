
import bpy,importlib,os

from bpy.utils import register_class, unregister_class

from ..operators.pie_op import AutoSommth as KSYNOPS_OT_AutoSommth
from ..operators.pie_op import Setting as KSYNOPS_OT_Setting


# クラス名を変えた場合はブレンダーを再起動する必要があるみたい。
# 一見、再読み込みで元のクラス名が読み込まれそうだが、あくまでもレジストレーションのクラス名が読み込まれるので、
# レジストレーションの設定でクラス名が決まっていればOK。で、再読み込みはあくまでもファイルだけが読み込まれる仕様

modules = [
    (["operators"],"pie_op",[KSYNOPS_OT_AutoSommth,KSYNOPS_OT_Setting])
    ]


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