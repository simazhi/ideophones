import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
#DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
TARGET_DIR = os.path.join(f"{PROJECT_ROOT}/segmented/")
#print(PROJECT_ROOT)
#print(TARGET_DIR)

SOURCE_DIR = os.path.join(f"{PROJECT_ROOT}/results/")

sources = []
for file in os.walk(SOURCE_DIR):  
    #for filename in files:
    sources.append(file)

print(sources)

print("take 2")

sources2 = [file for file in SOURCE_DIR]

print(sources2)

print("take 3")



print("take 4")

import os
sources = []
for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(root, file)
            sources.append(path)

print(sources)
             
print("take 5")

from pathlib import Path

Path(SOURCE_DIR).exists()
p = Path(SOURCE_DIR)
print(p.glob('*.txt'))