from io import BytesIO
import random

# How complicated can it be? It's just randomizing some levels.
# I want to kill myself

# Filter Secret Exits
SECRET_EXIT_LEVELS = [
    "A02", # 1-2
    "A07", # 1-Tower
    "B03", # 2-3
    "B04", # 2-4
    "B07", # 2-A
    "C02", # 3-2
    "C07", # 3-Ghost
    "D01", # 4-1
    "D08", # 4-Ghost
    "E02", # 5-2
    "E06", # 5-B
    "E08", # 5-Ghost
    "G04", # 7-4
    "G05", # 7-5
    "G06", # 7-6
    "G09", # 7-Ghost
]

# Filter Castles
CASTLE_LEVELS = [
    "A08", # World 1 Castle
    "B09", # World 2 Castle
    "C09", # World 3 Castle
    "D10", # World 4 Castle
    "E10", # World 5 Castle
    "F11", # World 6 Castle
    "G11", # World 7 Castle
    "H11", # World 8 Castle
    "H12", # Final Castle
]

# Filter Canons
CANON_LEVELS = [
    "A09", # World 1 Canon
    "B10", # World 2 Canon
    "C10", # World 3 Canon
    "D11", # World 4 Canon
    "E11", # World 5 Canon
    "F12", # World 6 Canon
]

def LevelRandomizer(parent, seed, rom):
    # Non-Secret Exit Levels
    levelList = []
    shuffledByteList = []
    
    # For Levels that contain Secret Exits
    secretList = []
    shuffledSecretByteList = []
    
    # For Castle Levels
    castleList = []
    shuffledCastleList = []
    
    # To ensure that exits stay within their respective Levels
    byteDataList = []
    secretByteDataList = []
    castleByteDataList = []
    
    subArea = 0
    for i, file in enumerate(rom.files): # Awesome
        if file.startswith(b'p'):
            if not (any(string in rom.filenames[i] for string in CANON_LEVELS) or "I" in rom.filenames[i] or "J" in rom.filenames[i]):
                
                subArea += 1
                
                hasSecret = False
                castleLevel = False
                for string in SECRET_EXIT_LEVELS:
                    if string in rom.filenames[i]:
                        secretByteDataList.append(file)
                        secretList.append(rom.filenames[i])
                        hasSecret = True
                
                for string in CASTLE_LEVELS:
                    if string in rom.filenames[i]:
                        castleByteDataList.append(file)
                        castleList.append(rom.filenames[i])
                        castleLevel = True
                
                if not hasSecret and not castleLevel:
                    byteDataList.append(file)
                    levelList.append(rom.filenames[i])
        try:
            if rom.filenames[i].endswith("bgdat.bin") and not (any(string in rom.filenames[i] for string in CANON_LEVELS) or "I" in rom.filenames[i] or "J" in rom.filenames[i]):
                hasUpcomingSubArea = rom.filenames[i + 2].endswith(f'_{subArea + 1}_bgdat.bin')
                if hasSecret: # We can't shuffle Secret Exits in with Normal levels as it would softlock logic and risk game crashes
                    secretByteDataList.append(file)
                    secretList.append(rom.filenames[i])
                    
                    if not hasUpcomingSubArea:
                        shuffledSecretByteList.append(secretByteDataList)
                        secretByteDataList = []
                        subArea = 0
                elif castleLevel: # We can't shuffle Castles in with Normal Levels for the same reason as Secret Exits
                    castleByteDataList.append(file)
                    castleList.append(rom.filenames[i])
                    
                    if not hasUpcomingSubArea:
                        shuffledCastleList.append(castleByteDataList)
                        castleByteDataList = []
                        subArea = 0
                elif not hasSecret and not castleLevel:
                    byteDataList.append(file)
                    levelList.append(rom.filenames[i])
                    
                    if not hasUpcomingSubArea:
                        shuffledByteList.append(byteDataList)
                        byteDataList = []
                        subArea = 0
        except Exception as e:
            print(f"Error: {e}")
            continue

    random.seed(seed)
    random.shuffle(shuffledByteList)
    random.shuffle(shuffledSecretByteList)
    random.shuffle(shuffledCastleList)
    
    # Randomize
    index = 0
    for i in range(len(shuffledByteList)):
        for j in range(len(shuffledByteList[i])):
            rom.setFileByName(levelList[index], shuffledByteList[i][j])
            index += 1
            
    index = 0
    for i in range(len(shuffledSecretByteList)):
        for j in range(len(shuffledSecretByteList[i])):
            rom.setFileByName(secretList[index], shuffledSecretByteList[i][j])
            index += 1
            
    index = 0
    for i in range(len(shuffledCastleList)):
        for j in range(len(shuffledCastleList[i])):
            rom.setFileByName(castleList[index], shuffledCastleList[i][j])
            index += 1