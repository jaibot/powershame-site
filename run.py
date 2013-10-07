#!/usr/bin/env python
import os
os.environ['POWERSHAME_CONFIG']=os.getcwd()+'/config.py'
from powershame import app

app.run(debug=True)
