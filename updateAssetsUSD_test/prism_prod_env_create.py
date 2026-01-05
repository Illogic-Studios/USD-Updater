import os
import sys
import json
import shutil

PRISM_PATH = os.getenv("PRISM_ROOT")
PCORE_PATH = os.path.join(PRISM_PATH, "Scripts")

PROD_CONFIG = os.path.join(os.path.dirname(__file__), "configs", "prod_data.json")
PROD_NAME = "Prod_test_ENV"
PROD_PATH = os.path.join(os.path.dirname(__file__), PROD_NAME)
PROD_PRESET = "R:/pipeline/pipe/prism/defaultProjectPreset"
if not PCORE_PATH in sys.path:
    sys.path.insert(0, PCORE_PATH)

import PrismCore


def createProd(prod_name= PROD_NAME, prod_path=PROD_PATH, prod_preset=PROD_PRESET):
    pcore = PrismCore.create(prismArgs=['noUI', 'silent'])
    config_path = pcore.configs.getProjectConfigPath(prod_preset)
    config_settings = pcore.configs.getConfig(configPath=config_path)
    default_settings = pcore.projects.getDefaultProjectSettings()
    settings = pcore.configs.updateNestedDicts(default_settings, config_settings)
    project_structure = pcore.projects.getFolderStructureFromPath(prod_preset, simple=True)
    pcore.projects.createProject(
        name=prod_name,
        path=prod_path,
        settings=settings,
        structure=project_structure,
    )
    pcore.changeProject(prod_path)
    return pcore


def getProdDatas(prod_data_path: str):
    with open(prod_data_path, "r") as prod_data_file:
        prod_data = json.load(prod_data_file)
    return prod_data


def initializeUSD(entity: dict, data: dict, usd_api):
    usd_api.createEntityUsd(entity=entity)
    departments = data.get("departments", [])
    for department_data in departments:
        department_name = department_data.get("name")
        if department_name is None:
            continue
        usd_api.createDepartmentLayerForEntity(
            entity=entity,
            department=department_name
        )
        
        sublayers = department_data.get("sublayers", [])
        for sublayer in sublayers:
            usd_api.createSublayerLayerForDepartment(
                entity=entity,
                department=department_name,
                sublayer=sublayer
            )
        
        
def initializeAssets(pcore, assets: dict, usd_api):
    for asset in assets:
        asset_path = asset.get("path")
        if asset_path is None:
            continue
        entity = {
            "type": "asset",
            "asset_path": asset_path
        }
        print(f"--Create Asset : \"{asset_path}\"--")
        pcore.entities.createAsset(entity)
        print("--Initialize USD--")
        initializeUSD(entity, asset, usd_api)


def initializeShots(pcore, shots: dict, usd_api):
    for shot_data in shots:
        sequence = shot_data.get("sequence")
        shot = shot_data.get("shot")
        if sequence is None or shot is None:
            continue
        entity = {
            "type": "shot",
            "sequence": sequence,
            "shot": shot
        }
        print(f"--Create Shot : \"{sequence}/{shot}\"--")
        pcore.entities.createShot(entity)
        print("--Initialize USD--")
        initializeUSD(entity, shot_data, usd_api)


def initializeProd(pcore: PrismCore.PrismCore, prod_data: dict):
    assets = prod_data.get("assets", [])
    shots = prod_data.get("shots", [])
    
    usd_plugin = pcore.getPlugin("USD")
    if usd_plugin is None:
        return
    usd_api = usd_plugin.api
    
    initializeAssets(pcore, assets, usd_api)
    initializeShots(pcore, shots, usd_api)


def createEnv():
    deleteProd()
    prod_data = getProdDatas(PROD_CONFIG)
    prod_name = prod_data["prod_name"]
    prod_preset = prod_data["prod_preset"]
    pcore = createProd(
        prod_name=prod_name,
        prod_path=PROD_PATH,
        prod_preset=prod_preset
    )
    initializeProd(pcore, prod_data)
    return pcore


def deleteProd():
    try:
        shutil.rmtree(PROD_PATH)
    except Exception as e:
        print(e)
    
    
if __name__ == "__main__":
    createEnv()