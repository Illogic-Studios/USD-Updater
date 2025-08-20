import os
import shutil
from pathlib import Path

from pxr import Sdf, UsdUtils
import updateAssetsUSD.usd_parser as usd_parser

ENVIRONNEMENT_CONTEXT = [
    "R:/", "I:/"
]
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()


def test_parse():
    layer_path = (
        "updateAssetsUSD_test/river__layer_mod_mayaLayout_v058.usda"
    )
    layer = Sdf.Layer.FindOrOpen(layer_path)

    usdp = usd_parser.USDParser()
    usdp.ar_context = ENVIRONNEMENT_CONTEXT
    usdp.set_assets_to_update([])
    
    usdp.parse(layer)
    usdp.update_layer(layer)
    usdp.parse(layer)
    
    return usdp.get_assets_to_update()


def test_update(self):
    layer_path = (
        "R:/devmaxime/environnement/testenv/multiples_refs/multiple_refs.usda"
    )
    layer_root, layer_ext = os.path.splitext(layer_path)
    layer_copy_path = layer_root + "_test_update" + layer_ext

    shutil.copy(layer_path, layer_copy_path)
    
    layer = Sdf.Layer.FindOrOpen(layer_copy_path)

    usdp = usd_parser.USDParser()
    usdp.set_assets_to_update([])
    usdp.parse(layer)
    
    
    
    item_list = usdp.get_assets_to_update()

    print('.')
    item = item_list[0]
    print(item.original_path)
    print(item.updated_path)
    print(f"{item.from_version} -> {item.to_version}")
    
    usdp.update_layer(layer)
    usdp.parse(layer)
    updated_item_list = usdp.get_assets_to_update()
    
    os.remove(layer_copy_path)
        
        
if __name__ == '__main__':
    # This USD file hold multiples references 
    # to plantGrass v011 while a v012 exists
    # Therefore, it will update every singles references
    layer_path = (
        "updateAssetsUSD_test/river__layer_mod_mayaLayout_v058.usda"
    )
    asset_item = test_update()