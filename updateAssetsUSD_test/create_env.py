from pxr import Sdf, UsdUtils, Ar
import os
import shutil
from pathlib import Path

path = Path("I:/intermarche/03_Production/Shots/testShot/interiorTestShot/Export/USD/v093/testShot-interiorTestShot_USD_v093.usda")
environnemnt_dir = Path("R:/devmaxime/dev/python/prism/update_assets_USD_dev/updateAssetsUSD_dev/updateAssetsUSD_test/testenv")

layer = Sdf.Layer.FindOrOpen(path.as_posix())
ar_context = Ar.DefaultResolverContext(["I:/", "R:/"])
with Ar.ResolverContextBinder(ar_context):
    layers, _, _ = UsdUtils.ComputeAllDependencies(layer.identifier)


def createCopy(source: Path, environnemnt_dir: Path):
    splitdrived = Path(*source.parts[1:])
    destination = environnemnt_dir / splitdrived
    os.makedirs(destination.parent, exist_ok=True)
    shutil.copy(source, destination)


createCopy(path, environnemnt_dir)
for path in layers:
    createCopy(Path(path.realPath), environnemnt_dir)