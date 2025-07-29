import unittest
import os
import shutil
from pathlib import Path
from pxr import UsdUtils

import updateAssetsUSD as UD

ENVIRONNEMENT_CONTEXT = "R:/devmaxime/environnement/testenv"

# Use to suppress pxr logs
DELEGATE = UsdUtils.CoalescingDiagnosticDelegate()

class USDParserTest(unittest.TestCase):
    
    
    def test_package(self):
        layer_path = (Path(ENVIRONNEMENT_CONTEXT) / Path(
                "Illogic_Training/03_Production/Shots/seq_01"
                "/sh_010/Export/USD/v017/seq_01-sh_010_USD_v017.usda"
            )
        ).as_posix()
        UD.startUpdateAssetsUSD('prism', layer_path)
        pass
        
        

if __name__ == '__main__':
    unittest.main()
