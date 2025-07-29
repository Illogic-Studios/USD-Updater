import cProfile
import pstats

PROFILER = cProfile.Profile()

from pxr import Sdf, UsdUtils
import updateAssetsUSD.usd_parser as usd_parser

ENVIRONNEMENT_CONTEXT = [
    "R:/", "I:/"
]
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()


def test_parse():
    layer_path = (
        "i:/intermarche/03_Production/Assets/Environment/river/Export/_layer_mod_mayaLayout/v058/river__layer_mod_mayaLayout_v058.usda.20250729_144917.bak.usda"
    )
    layer = Sdf.Layer.FindOrOpen(layer_path)

    usdp = usd_parser.USDParser()
    usdp.ar_context = ENVIRONNEMENT_CONTEXT
    usdp.set_assets_to_update([])
    
    PROFILER.enable()
    usdp.parse(layer)
    PROFILER.disable()
    usdp.update_layer(layer)
    usdp.parse(layer)
    
    return usdp.get_assets_to_update()


if __name__ == '__main__':
    asset_item = test_parse()
    print('.')
    item = asset_item[0]
    print(item.original_path)
    print(item.updated_path)
    print(f"{item.from_version} -> {item.to_version}")

    stats = pstats.Stats(PROFILER)
    stats.dump_stats('stats.prof')
