import unittest
import os
import shutil
from pathlib import Path
from pxr import Sdf, UsdUtils

from updateAssetsUSD.assetitem import AssetItem
import updateAssetsUSD.usd_parser as usd_parser

ENVIRONNEMENT_CONTEXT = "R:/devmaxime/environnement/testenv"

# Use to suppress pxr logs
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()

class USDParserTest(unittest.TestCase):
    
    
    def test_parse(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "Illogic_Training/03_Production/Shots/seq_01"
                "/sh_010/Export/USD/v017/seq_01-sh_010_USD_v017.usda"
            )
        ).as_posix()
        layer = Sdf.Layer.FindOrOpen(layer_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.set_assets_to_update([])
        usdp.parse(layer)
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        item = item_list[0]
        original_path = '../v003/seq_01-sh_010_USD_v003.usda'
        updated_path = '../v027/seq_01-sh_010_USD_v027.usdc'
        
        self.assertEqual(item.original_path, original_path)
        self.assertEqual(item.updated_path, updated_path)
        self.assertEqual(item.from_version, 3)
        self.assertEqual(item.to_version, 27)
        self.assertEqual(item.layer_path, layer_path)
        self.assertEqual(item.can_be_updated, True)
        self.assertEqual(item.should_be_updated, True)
        
    def test_recursive_parse(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "intermarche/03_Production/Shots/testShot/interiorTestShot"
                "/Export/USD/v093/testShot-interiorTestShot_USD_v093.usda"
            )
        ).as_posix()
        layer = Sdf.Layer.FindOrOpen(layer_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.set_assets_to_update([])
        usdp.parse(layer, True)
        
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(item_list), 9)
        for item in item_list:
            self.assertEqual(item.can_be_updated, False)
        self.assertEqual(item_list[0].from_version, 9)
        self.assertEqual(item_list[0].to_version, 13)
        
    def test_update(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "Illogic_Training/03_Production/Shots/seq_01/sh_010/Export"
                "/USD/v017/seq_01-sh_010_USD_v017.usda"
            )
        ).as_posix()
        layer_root, layer_ext = os.path.splitext(layer_path)
        layer_copy_path = layer_root + "_test_update" + layer_ext

        shutil.copy(layer_path, layer_copy_path)
        
        layer = Sdf.Layer.FindOrOpen(layer_copy_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.set_assets_to_update([])
        usdp.parse(layer)
        
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        item = item_list[0]
        self.assertEqual(item.from_version, 3)
        self.assertEqual(item.to_version, 27)
        
        usdp.update_layer(layer)
        usdp.parse(layer)
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(item_list), 0)

        os.remove(layer_copy_path)
        

if __name__ == '__main__':
    unittest.main()
