import os
from pathlib import Path
import updateAssetsUSD
import updateAssetsUSD_test.prism_prod_env_create as prism_prod

core = prism_prod.createEnv()

ENVIRONNEMENT_CONTEXT = os.path.join(os.path.dirname(__file__), "testenv")

layer_path = (
    Path(prism_prod.PROD_PATH)
    / Path("03_Production/Assets/Characters/Cat")
    / Path("Export/USD/v009/Cat_USD_v009.usda")
).as_posix()

app = updateAssetsUSD.usd_updater.Qt.QApplication.instance()
if not app:
    app = updateAssetsUSD.usd_updater.Qt.QApplication()

updateAssetsUSD.startUpdateAssetsUSD(
    openType="prism",
    tmpfile=layer_path,
    prism_core=core
)

app.exec_()

prism_prod.deleteProd()

pass