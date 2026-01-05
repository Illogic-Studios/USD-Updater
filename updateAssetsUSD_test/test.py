from pathlib import Path
import prism_prod_env_create
import updateAssetsUSD as UD

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
app.exec()

prism_prod_env_create.deleteProd()