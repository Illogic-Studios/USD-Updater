import unittest
import os
import glob
import shutil
import tempfile
from pathlib import Path
from pxr import Sdf, UsdUtils

from updateAssetsUSD.assetitem import AssetItem
import updateAssetsUSD.usd_parser as usd_parser

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
        
        
    def test_parse_abs(self):
        os.environ["PXR_AR_DEFAULT_SEARCH_PATH"] = ENVIRONNEMENT_CONTEXT
        
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
        usdp.set_assets_to_update(item_list)
        item_list2 = usdp.get_assets_to_update()
        
        self.assertEqual(item_list, item_list2)
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
        
        usdp.update_layer(
            layer,
            mode=usd_parser.USDParser.UpdateMode.OVERWRITE
        )
        usdp.parse(layer)
        item_list: list[AssetItem] = usdp.get_assets_to_update()
        
        trashs = glob.glob(layer_copy_path+"*")
        for trash in trashs:
            os.remove(trash)
            
        self.assertEqual(item.from_version, 1)
        self.assertEqual(item.to_version, 8)
        self.assertEqual(len(item_list), 0)
        
        
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
        refs = ext_refs[1]

        usdp = usd_parser.USDParser()
        usdp.parse(layer)
        usdp.update_layer(
            layer,
            mode=usd_parser.USDParser.UpdateMode.OVERWRITE
        )
        
        new_ext_refs = UsdUtils.ExtractExternalReferences(layer.identifier)
        new_refs = new_ext_refs[1]
        
        trashs = glob.glob(layer_copy_path+"*")
        for trash in trashs:
            os.remove(trash)
        
        self.assertEqual(len(ext_refs), 3)
        self.assertEqual(len(refs), 5)
        self.assertEqual(refs[0], './v001/common.usda')
        self.assertEqual(refs[1], './v002/common.usda')
        self.assertEqual(refs[2], './v003/common.usda')
        self.assertEqual(refs[3], './v004/common.usda')
        self.assertEqual(refs[4], './v004/dummy.txt')
        self.assertEqual(len(new_ext_refs), 3)
        self.assertEqual(len(new_refs), 2)
        self.assertEqual(new_refs[0], './v004/dummy.txt')
        self.assertEqual(new_refs[1], './v008/common.usda')
        

    def test_update_version_up(self):
        import prism_prod_env_create
        core = prism_prod_env_create.createEnv()
        
        # ASSET
        asset_layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v009/Cat_USD_v009.usda")
        ).as_posix()
        asset_layer = Sdf.Layer.FindOrOpen(asset_layer_path)

        usdp = usd_parser.USDParser()
        usdp.ar_context = [ENVIRONNEMENT_CONTEXT]
        usdp.parse(asset_layer)
        
        asset_item_list: list[AssetItem] = usdp.get_assets_to_update()
        asset_item = asset_item_list[0]
        self.assertEqual(asset_item.from_version, 4)
        self.assertEqual(asset_item.to_version, 5)
        
        usdp.update_layer(
            layer=asset_layer,
            mode=usd_parser.USDParser.UpdateMode.NEW_VERSION,
            core=core
        )
        asset_layer_path_up = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v011/Cat_USD_v011.usda")
        ).as_posix()
        self.assertTrue(os.path.exists(asset_layer_path_up))
        asset_layer_up = Sdf.Layer.FindOrOpen(asset_layer_path_up)
        
        usdp.parse(asset_layer_up)
        asset_item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(asset_item_list), 0)

        # SHOT
        shot_layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Shots/SQ001/SH010")
            / Path("Export/USD/v016/SQ001-SH010_USD_v016.usda")
        ).as_posix()
        shot_layer = Sdf.Layer.FindOrOpen(shot_layer_path)
        
        usdp.parse(shot_layer)
        
        shot_item_list: list[AssetItem] = usdp.get_assets_to_update()
        shot_item = shot_item_list[0]
        self.assertEqual(shot_item.from_version, 4)
        self.assertEqual(shot_item.to_version, 5)
        
        usdp.update_layer(
            layer=shot_layer,
            mode=usd_parser.USDParser.UpdateMode.NEW_VERSION,
            core=core
        )
        shot_layer_path_up = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Shots/SQ001/SH010")
            / Path("Export/USD/v018/SQ001-SH010_USD_v018.usda")
        ).as_posix()
        self.assertTrue(os.path.exists(shot_layer_path_up))
        shot_layer_up = Sdf.Layer.FindOrOpen(shot_layer_path_up)
        
        usdp.parse(shot_layer_up)
        shot_item_list: list[AssetItem] = usdp.get_assets_to_update()
        self.assertEqual(len(shot_item_list), 0)

        prism_prod_env_create.deleteProd()


    def test_resolve_path(self):
        os.environ["PXR_AR_DEFAULT_SEARCH_PATH"] = ENVIRONNEMENT_CONTEXT
        
        abs_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "parse/v008\common.usda"
            )
        ).as_posix()
        dir_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "parse"
            )
        ).as_posix()
        rel_path = "v008/common.usda"
        ar_rel_path = "parse/v008/common.usda"
        failed_path = "v008/asdasd.usda"
        
        usdp = usd_parser.USDParser()
        usdp.dirname = dir_path
        
        expected_path = Path(abs_path).resolve()
        expected_failed_path = (Path(dir_path) / failed_path).resolve()
        
        self.assertEqual(expected_path, usdp._resolve_path(abs_path))
        self.assertEqual(expected_path, usdp._resolve_path(rel_path))
        self.assertEqual(expected_path, usdp._resolve_path(ar_rel_path))
        self.assertEqual(expected_failed_path, usdp._resolve_path(failed_path))
            

if __name__ == '__main__':
    unittest.main()
