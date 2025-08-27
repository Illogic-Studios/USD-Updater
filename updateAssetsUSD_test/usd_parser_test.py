import unittest
import os
import shutil
from pathlib import Path
from pxr import Sdf, UsdUtils

from updateAssetsUSD.assetitem import AssetItem
import updateAssetsUSD.usd_parser as usd_parser

ENVIRONNEMENT_CONTEXT = "R:/devmaxime/environnement/testenv"


# LOCAL ENVIRONNEMENT (Faster, especially for recursive parse)
# TODO Need to find a workaround to avoid wasting time on network
ENVIRONNEMENT_CONTEXT = "C:/Users/m.beldjilali/Documents/environnement/testenv"
ENVIRONNEMENT_CONTEXT = os.path.join(os.path.dirname(__file__), "testenv")

# Use to suppress pxr logs
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()

class USDParserTest(unittest.TestCase):
    
    
    def test_parse(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "parse/single_ref.usda"
            )
        ).as_posix()
        layer = Sdf.Layer.FindOrOpen(layer_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.parse(layer)
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        item = item_list[0]
        original_path = './v001/common.usda'
        updated_path = './v008/common.usda'
        
        self.assertEqual(item.original_path, original_path)
        self.assertEqual(item.updated_path, updated_path)
        self.assertEqual(item.from_version, 1)
        self.assertEqual(item.to_version, 8)
        self.assertEqual(item.layer_path, layer_path)
        self.assertEqual(item.can_be_updated, True)
        self.assertEqual(item.should_be_updated, True)
        

    def test_recursive_parse(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "recursive_refs/recursive_refs.usda"
            )
        ).as_posix()
        layer = Sdf.Layer.FindOrOpen(layer_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.parse(layer, True)
        
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(item_list), 3)
        for item in item_list:
            self.assertEqual(item.can_be_updated, False)
        self.assertEqual(item_list[0].from_version, 1)
        self.assertEqual(item_list[0].to_version, 3)


    def test_update(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "update/single_ref.usda"
            )
        ).as_posix()
        layer_root, layer_ext = os.path.splitext(layer_path)
        layer_copy_path = layer_root + "_test_update" + layer_ext

        shutil.copy(layer_path, layer_copy_path)
        
        layer = Sdf.Layer.FindOrOpen(layer_copy_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.parse(layer)
        
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        item = item_list[0]
        self.assertEqual(item.from_version, 1)
        self.assertEqual(item.to_version, 8)
        
        usdp.update_layer(layer)
        usdp.parse(layer)
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(item_list), 0)

        os.remove(layer_copy_path)
        
        
    def test_update_multiples_refs(self):
        # Test update when the same references occured multiples times
        # It this USD, common v002 appears twice and also in v003 and v004
        # while the latest version is v008
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "multiples_refs/multiple_refs.usda"
            )
        ).as_posix()
        layer_root, layer_ext = os.path.splitext(layer_path)
        layer_copy_path = layer_root + "_test_update" + layer_ext

        shutil.copy(layer_path, layer_copy_path)
        layer = Sdf.Layer.FindOrOpen(layer_copy_path)

        ext_refs = UsdUtils.ExtractExternalReferences(layer.identifier)
        self.assertEqual(len(ext_refs), 3)
        refs = ext_refs[1]
        self.assertEqual(len(refs), 4)
        self.assertEqual(refs[0], './v001/common.usda')
        self.assertEqual(refs[1], './v002/common.usda')
        self.assertEqual(refs[2], './v003/common.usda')
        self.assertEqual(refs[3], './v004/common.usda')

        usdp = usd_parser.USDParser()
        usdp.parse(layer)
        usdp.update_layer(layer)
        
        new_ext_refs = UsdUtils.ExtractExternalReferences(layer.identifier)
        self.assertEqual(len(new_ext_refs), 3)
        new_refs = new_ext_refs[1]
        self.assertEqual(len(new_refs), 1)
        self.assertEqual(new_refs[0], './v008/common.usda')
        
        os.remove(layer_copy_path)
        

if __name__ == '__main__':
    unittest.main()
