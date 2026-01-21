#!/usr/bin/env python
""" Python script to manage status labels for SAFESTART project"""

import status
from datetime import datetime

__author__ = "Andreu Bofill"
__copyright__ = "Copyright 2025, ISGlobal Maternal, Child and Reproductive Health"
__credits__ = ["Andreu Bofill"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "20260621"
__maintainer__ = "Andreu Bofill"
__email__ = "andreu.bofill@isglobal.org"
__status__ = "Dev"


if __name__ == '__main__':
    status.generate_redcap_labels()
    
    print("\n FINISHED:\t",datetime.today())

