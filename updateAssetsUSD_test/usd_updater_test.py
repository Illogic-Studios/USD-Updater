import os
import unittest
from pathlib import Path
from pxr import UsdUtils

import prism_prod_env_create
import updateAssetsUSD as UD

from qtpy import QtWidgets as Qt
from qtpy import QtCore as Qtc
from qtpy import QtGui as Qtg
from qtpy import QtTest as Qtt

ENVIRONNEMENT_CONTEXT = os.path.join(os.path.dirname(__file__), "testenv")

# Use to suppress pxr logs
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()


class USDParserTest(unittest.TestCase):
    
    
    def test_basic_start(self):
        core = prism_prod_env_create.createEnv()
        
        layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v006/Cat_USD_v006.usda")
        ).as_posix()
        UD.reload_modules()
        UD.startUpdateAssetsUSD(
            openType="prism",
            tmpfile=layer_path,
            prism_core=core
        )
        
        prism_prod_env_create.deleteProd()


    def test_main_window(self):
        core = prism_prod_env_create.createEnv()
        
        layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v006/Cat_USD_v006.usda")
        ).as_posix()
        
        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()
            
        main_window = UD.usd_updater.MainInterface(
            openType='prism',
            pathPrism=layer_path,
            pcore=core,
            ar_context=None,
            check_update_only=False,
            parent=None
        )
        main_window.show()
        prism_prod_env_create.deleteProd()


    def test_parse(self):
        core = prism_prod_env_create.createEnv()

        layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v006/Cat_USD_v006.usda")
        ).as_posix()
        
        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()
            
        main_window = UD.usd_updater.MainInterface(
            openType='prism',
            pathPrism=layer_path,
            pcore=core,
            ar_context=None,
            check_update_only=False,
            parent=None
        )
        # check layer widget tree
        item = main_window.layerList.item(0)
        layer_widget: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(item)
        self.assertEqual(main_window._layers[0].identifier, layer_path)
        self.assertEqual(layer_widget.label.text(), '<b>USD</b><br> - Cat_USD_v006.usda')
        self.assertEqual(layer_widget.update_label.text(), UD.usd_updater.LayerWidget.UpdateTextEnum.NOT_UPDATED.value)

        # check asset item
        asset_list: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(0)
        self.assertEqual(
            asset_list.layer_type,
            UD.usd_updater.AssetListWidget.LayerType.CONTAINER
        )
        self.assertTrue(asset_list.can_be_updated)
        self.assertFalse(asset_list.isUpdate)
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(0)).text(),
            'Current layer : <b>r:/devmaxime/dev/python/prism/USD-Updater/updateAssetsUSD_test/'
            'Prod_test_ENV/03_Production/Assets/Characters/Cat/Export/USD/v006/Cat_USD_v006.usda</b>'
        )
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(1)).children()[2].text(),
            "<em>../../_layer_cfx_master/v002/Cat__layer_cfx_master_v002.usda</em><br>➡ <b>"
            "<span style='color: red;'>v002</span></b> → <b><span style='color: green;'>v003</span></b>"
        )
        
        main_window.show()
        
        prism_prod_env_create.deleteProd()
        
        
    def test_debug(self):
        os.environ["UD_DEBUG"] = "1"

        UD.reload_modules()

        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()            
        main_window = UD.usd_updater.MainInterface(
            openType='prism',
            pathPrism='',
            ar_context=None,
            check_update_only=False,
            parent=None
        )
        main_window.show()
        
        self.assertTrue(hasattr(main_window, "debugbutton"))
        self.assertEqual(main_window.debugbutton.text(), 'DEBUG')
        prism_prod_env_create.deleteProd()
        

if __name__ == '__main__':
    unittest.main()
    prism_prod_env_create.deleteProd()
