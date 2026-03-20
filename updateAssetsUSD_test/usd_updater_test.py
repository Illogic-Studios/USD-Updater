import os
import unittest
from pathlib import Path
from pxr import UsdUtils

import prism_prod_env_create
import updateAssetsUSD as UD


from qtpy import QtCore as Qtc
from qtpy import QtTest as Qtt

ENVIRONNEMENT_CONTEXT = os.path.join(os.path.dirname(__file__), "testenv")

# Use to suppress pxr logs
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()


class USDUpdaterTest(unittest.TestCase):
    def test_basic_start(self):
        UD.reload_modules()
        UD.startUpdateAssetsUSD(
            openType="prism",
            tmpfile="",
        )

    def test_main_window(self):
        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()

        main_window = UD.usd_updater.MainInterface(
            openType="prism",
            pathPrism="",
            ar_context=None,
            check_update_only=False,
            parent=None,
        )
        main_window.show()

    def test_debug(self):
        os.environ["UD_DEBUG"] = "1"

        UD.reload_modules()

        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()
        main_window = UD.usd_updater.MainInterface(
            openType="prism",
            pathPrism="",
            ar_context=None,
            check_update_only=False,
            parent=None,
        )
        main_window.show()

        self.assertTrue(hasattr(main_window, "debugbutton"))
        self.assertEqual(main_window.debugbutton.text(), "DEBUG")
        prism_prod_env_create.deleteProd()

    def test_parse(self):
        core = prism_prod_env_create.createEnv()

        layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v009/Cat_USD_v009.usda")
        ).as_posix()

        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()

        main_window = UD.usd_updater.MainInterface(
            openType="prism",
            pathPrism=layer_path,
            pcore=core,
            ar_context=None,
            check_update_only=False,
            parent=None,
        )
        # check layer widget tree
        item = main_window.layerList.item(0)
        layer_widget: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(
            item
        )
        self.assertEqual(main_window._layers[0].identifier, layer_path)
        self.assertEqual(
            layer_widget.label.text(), "<b>USD</b><br> - Cat_USD_v009.usda"
        )
        self.assertEqual(
            layer_widget.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.NOT_UPDATED.value,
        )

        # check asset item
        asset_list: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(0)
        self.assertEqual(
            asset_list.layer_type, UD.usd_updater.AssetListWidget.LayerType.CONTAINER
        )
        self.assertTrue(asset_list.can_be_updated)
        self.assertFalse(asset_list.isUpdate)
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(0)).text(),
            "Current layer : <b>r:/devmaxime/dev/python/prism/USD-Updater/updateAssetsUSD_test/"
            "Prod_test_ENV/03_Production/Assets/Characters/Cat/Export/USD/v009/Cat_USD_v009.usda</b>",
        )
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(1)).children()[2].text(),
            "<em>../../_layer_cfx_master/v004/Cat__layer_cfx_master_v004.usda</em><br>➡ <b>"
            "<span style='color: red;'>v004</span></b> → <b><span style='color: green;'>v005</span></b>",
        )

        main_window.show()

        prism_prod_env_create.deleteProd()

    def test_update(self):
        core = prism_prod_env_create.createEnv()

        layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v009/Cat_USD_v009.usda")
        ).as_posix()

        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()

        main_window = UD.usd_updater.MainInterface(
            openType="prism",
            pathPrism=layer_path,
            pcore=core,
            ar_context=None,
            check_update_only=False,
            parent=None,
        )
        # check layer widget tree
        item = main_window.layerList.item(0)
        layer_widget: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(
            item
        )
        self.assertEqual(main_window.layerList.count(), 1)
        self.assertEqual(main_window._layers[0].identifier, layer_path)
        self.assertEqual(
            layer_widget.label.text(), "<b>USD</b><br> - Cat_USD_v009.usda"
        )
        self.assertEqual(
            layer_widget.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.NOT_UPDATED.value,
        )

        # check asset item
        asset_list: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(0)
        self.assertEqual(
            asset_list.layer_type, UD.usd_updater.AssetListWidget.LayerType.CONTAINER
        )
        self.assertTrue(asset_list.can_be_updated)
        self.assertFalse(asset_list.isUpdate)
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(0)).text(),
            "Current layer : <b>r:/devmaxime/dev/python/prism/USD-Updater/updateAssetsUSD_test/"
            "Prod_test_ENV/03_Production/Assets/Characters/Cat/Export/USD/v009/Cat_USD_v009.usda</b>",
        )
        self.assertEqual(
            asset_list.itemWidget(asset_list.item(1)).children()[2].text(),
            "<em>../../_layer_cfx_master/v004/Cat__layer_cfx_master_v004.usda</em><br>➡ <b>"
            "<span style='color: red;'>v004</span></b> → <b><span style='color: green;'>v005</span></b>",
        )

        Qtt.QTest.mouseClick(main_window.runButton, Qtc.Qt.LeftButton)

        layer_path_up = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v011/Cat_USD_v011.usda")
        ).as_posix()

        item_up = main_window.layerList.item(0)
        layer_widget_up: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(
            item_up
        )
        self.assertTrue(os.path.exists(layer_path_up))
        self.assertEqual(main_window.layerList.count(), 1)
        self.assertEqual(main_window._layers[0].identifier, layer_path_up)
        self.assertEqual(
            layer_widget_up.label.text(), "<b>USD</b><br> - Cat_USD_v011.usda"
        )
        self.assertEqual(
            layer_widget_up.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.UPDATED.value,
        )

        asset_list_up: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(0)
        self.assertEqual(
            asset_list_up.layer_type, UD.usd_updater.AssetListWidget.LayerType.CONTAINER
        )
        self.assertTrue(asset_list_up.can_be_updated)
        self.assertTrue(asset_list_up.isUpdate)
        self.assertEqual(asset_list_up.count(), 0)

        main_window.show()

        prism_prod_env_create.deleteProd()

    def test_update_sublayers(self):
        core = prism_prod_env_create.createEnv()

        dpt_layer_path = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/_layer_anm_master/v002/Cat__layer_anm_master_v002.usda")
        ).as_posix()

        app = UD.usd_updater.Qt.QApplication.instance()
        if not app:
            app = UD.usd_updater.Qt.QApplication()

        main_window = UD.usd_updater.MainInterface(
            openType="prism",
            pathPrism=dpt_layer_path,
            pcore=core,
            ar_context=None,
            check_update_only=False,
            parent=None,
        )

        self.assertEqual(main_window.layerList.count(), 2)

        # DEPARTMENT ITEM
        dpt_item = main_window.layerList.item(0)
        dpt_layer_widget: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(
            dpt_item
        )
        dpt_asset_list: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(
            0
        )

        self.assertEqual(main_window._layers[0].identifier, dpt_layer_path)
        self.assertEqual(
            dpt_layer_widget.label.text(),
            "<b>_layer_anm_master</b><br> - Cat__layer_anm_master_v002.usda",
        )
        self.assertEqual(
            dpt_layer_widget.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.NOT_UPDATED.value,
        )
        self.assertEqual(
            dpt_asset_list.layer_type,
            UD.usd_updater.AssetListWidget.LayerType.DEPARTEMENT,
        )
        self.assertTrue(dpt_asset_list.can_be_updated)
        self.assertFalse(dpt_asset_list.isUpdate)
        self.assertEqual(dpt_asset_list.count(), 2)
        self.assertEqual(
            dpt_asset_list.itemWidget(dpt_asset_list.item(0)).text(),
            "Current layer : <b>r:/devmaxime/dev/python/prism/USD-Updater/updateAssetsUSD_test/"
            "Prod_test_ENV/03_Production/Assets/Characters/Cat/Export/_layer_anm_master/v002/Cat__layer_anm_master_v002.usda</b>",
        )
        self.assertEqual(
            dpt_asset_list.itemWidget(dpt_asset_list.item(1)).children()[2].text(),
            "<em>../../_layer_anm_main/v001/Cat__layer_anm_main_v001.usda</em><br>➡ <b>"
            "<span style='color: red;'>v001</span></b> → <b><span style='color: green;'>v002</span></b>",
        )

        # CONTAINER ITEM
        ctn_item = main_window.layerList.item(1)
        ctn_layer_widget: UD.usd_updater.LayerWidget = main_window.layerList.itemWidget(
            ctn_item
        )
        ctn_asset_list: UD.usd_updater.AssetListWidget = main_window.QTabLayers.widget(
            1
        )

        self.assertEqual(
            ctn_layer_widget.label.text(), "<b>USD</b><br> - Cat_USD_v010.usda"
        )
        self.assertEqual(
            ctn_layer_widget.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.UPDATED.value,
        )
        self.assertEqual(
            ctn_asset_list.layer_type,
            UD.usd_updater.AssetListWidget.LayerType.CONTAINER,
        )
        self.assertTrue(ctn_asset_list.can_be_updated)
        self.assertTrue(ctn_asset_list.isUpdate)
        self.assertEqual(ctn_asset_list.count(), 0)

        # =============
        # MANUAL UPDATE
        # =============

        Qtt.QTest.mouseClick(main_window.runButton, Qtc.Qt.LeftButton)

        dpt_layer_path_up = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/_layer_anm_master/v004/Cat__layer_anm_master_v004.usda")
        ).as_posix()

        ctn_layer_path_up = (
            Path(prism_prod_env_create.PROD_PATH)
            / Path("03_Production/Assets/Characters/Cat")
            / Path("Export/USD/v011/Cat_USD_v011.usda")
        ).as_posix()

        # Check new versions
        self.assertTrue(os.path.exists(dpt_layer_path_up))
        self.assertTrue(os.path.exists(ctn_layer_path_up))

        self.assertEqual(main_window.layerList.count(), 2)

        # DEPARTMENT ITEM
        dpt_item_up = main_window.layerList.item(1)
        dpt_layer_widget_up: UD.usd_updater.LayerWidget = (
            main_window.layerList.itemWidget(dpt_item_up)
        )
        dpt_asset_list_up: UD.usd_updater.AssetListWidget = (
            main_window.QTabLayers.widget(1)
        )

        self.assertEqual(main_window._layers[1].identifier, dpt_layer_path_up)
        self.assertEqual(
            dpt_layer_widget_up.label.text(),
            "<b>_layer_anm_master</b><br> - Cat__layer_anm_master_v004.usda",
        )
        self.assertEqual(
            dpt_layer_widget_up.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.UPDATED.value,
        )
        self.assertEqual(
            dpt_asset_list_up.layer_type,
            UD.usd_updater.AssetListWidget.LayerType.DEPARTEMENT,
        )
        self.assertTrue(dpt_asset_list_up.can_be_updated)
        self.assertTrue(dpt_asset_list_up.isUpdate)
        self.assertEqual(dpt_asset_list_up.count(), 0)

        # CONTAINER ITEM
        ctn_item_up = main_window.layerList.item(0)
        ctn_layer_widget_up: UD.usd_updater.LayerWidget = (
            main_window.layerList.itemWidget(ctn_item_up)
        )
        ctn_asset_list_up: UD.usd_updater.AssetListWidget = (
            main_window.QTabLayers.widget(0)
        )

        self.assertEqual(main_window._layers[0].identifier, ctn_layer_path_up)
        self.assertEqual(
            ctn_layer_widget_up.label.text(), "<b>USD</b><br> - Cat_USD_v011.usda"
        )
        self.assertEqual(
            ctn_layer_widget_up.update_label.text(),
            UD.usd_updater.LayerWidget.UpdateTextEnum.UPDATED.value,
        )
        self.assertEqual(
            ctn_asset_list_up.layer_type,
            UD.usd_updater.AssetListWidget.LayerType.CONTAINER,
        )
        self.assertTrue(ctn_asset_list_up.can_be_updated)
        self.assertTrue(ctn_asset_list_up.isUpdate)
        self.assertEqual(ctn_asset_list_up.count(), 0)

        main_window.show()

        prism_prod_env_create.deleteProd()


if __name__ == "__main__":
    unittest.main()
    prism_prod_env_create.deleteProd()
