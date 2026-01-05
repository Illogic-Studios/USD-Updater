import sys
import glob
import updateAssetsUSD

PRISM_MODULE_PATH = "C:/ILLOGIC_APP/Prism/2.0.18/app/Scripts"

if not PRISM_MODULE_PATH in sys.path:
    sys.path.insert(0, PRISM_MODULE_PATH)

import PrismCore

core = PrismCore.create(prismArgs=["noUI", "loadProject"])

example_pattern = "I:/intermarche/03_Production/Shots/testShot/fred/Export/USD/*/testShot-fred_USD_*.usda"
example_usd = sorted(glob.glob(example_pattern))[-1]

updateAssetsUSD.startUpdateAssetsUSD(
    openType="prism",
    tmpfile=example_usd,
    prism_core=core
)
sys.exit(PrismCore.qapp.exec_())

pass