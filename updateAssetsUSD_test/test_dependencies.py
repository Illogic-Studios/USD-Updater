from pxr import Sdf, UsdUtils

import updateAssetsUSD.usd_parser as usd_parser

import cProfile
import pstats

ENVIRONNEMENT_CONTEXT = [
    "R:/devmaxime/dev/python/prism/update_assets_USD_dev"
    "/updateAssetsUSD_test/testenv"
]
PROFILER = cProfile.Profile()
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()


def test_recursive_parse():
    layer_path = (
        "R:/devmaxime/dev/python/prism/update_assets_USD_dev"
        "/updateAssetsUSD_test/testenv/intermarche/03_Production/Shots"
        "/testShot/interiorTestShot/Export/USD/v093/"
        "testShot-interiorTestShot_USD_v093.usda"
    )
    layer = Sdf.Layer.FindOrOpen(layer_path)

    usdp = usd_parser.USDParser()
    usdp.ar_context = ENVIRONNEMENT_CONTEXT
    usdp.set_assets_to_update([])
    
    PROFILER.enable()
    usdp.parse(layer, True)
    PROFILER.disable()


if __name__ == '__main__':
    test_recursive_parse()
    stats = pstats.Stats(PROFILER)
    stats.strip_dirs().sort_stats("cumtime").print_stats(20)
    