print("hello cookies")
# TO COOKIES: print SOMETHING BELOW THIS LINE TO TEST IF I GET YOUR UPDATES 

import pathlib
from pathlib import Path 
import sys

venv_path = Path(r'C:\Users\YKip1\OneDrive\Desktop\cookies\.venv\Lib\site-packages')
sys.path.insert(0, str(venv_path))
print(f'Path: {pathlib.Path(__file__).parent.resolve()}')
print(f'Path: {pathlib.Path().resolve()}')
print(sys.version) 
print("hello ykip10")
    