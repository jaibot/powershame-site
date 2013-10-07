#!/usr/bin/env python
import os
from powershame import app

os.environ['POWERSHAME_CONFIG']=os.getcwd+'config.py'
app.run(debug=True)
