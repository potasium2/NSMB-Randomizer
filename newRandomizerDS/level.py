from io import BytesIO
import random

# How complicated can it be? It's just randomizing some levels.
# I want to kill myself

def LevelRandomizer(parent, seed, rom):
    
    levelList = []
    shuffledByteList = []
    
    byteDataList = []
    
    subArea = 1
    for i, file in enumerate(rom.files):
        if file.startswith(b'p') and not rom.filenames[i].startswith(("course/I", "course/J")):
            subArea += 1
            if subArea > 1 and rom.filenames[i].endswith(f'_{subArea}.bin'):
                byteDataList.append(file)
            else:
                byteDataList = [file]
                subArea = 1
            
            levelList.append(rom.filenames[i])
        try:
            if rom.filenames[i].startswith(("course/", "course/")) and rom.filenames[i].endswith("bgdat.bin") and not rom.filenames[i].startswith(("course/I", "course/J")):
                byteDataList.append(file)
        
                levelList.append(rom.filenames[i])
                if subArea == 1:
                    shuffledByteList.append(byteDataList)
        except:
            continue

    random.seed(seed)
    random.shuffle(shuffledByteList)
    
    index = 0
    for i in range(len(shuffledByteList)):
        for j in range(len(shuffledByteList[i])):
            rom.setFileByName(levelList[index], shuffledByteList[i][j])
            index += 1