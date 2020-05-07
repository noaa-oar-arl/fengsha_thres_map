import monetio as mio


def get_sand_clay(path):
    tile = path.split('/')[-1].split('tile')[-1]
    clay = mio.prepchem.open_dataset("{}/clay.dat".format(path),tile=tile)
    sand = mio.prepchem.open_dataset("{}/sand.dat".format(path),tile=tile)
    return clay,sand


def calc_soil_type(clay,sand):
    from numpy import zeros,where
    silt = 100 - clay - sand
    stype = zeros(clay.shape)
    stype[where((silt + clay*1.5 < 15.) & (clay < 100))] = 1.  #SAND
    stype[where((silt + 1.5*clay >= 15.) & (silt + 1.5*clay <30) & (clay < 100))] = 2. #Loamy Sand
    stype[where((clay >= 7.) & (clay < 20) & (sand >52) & (silt + 2* clay >=30) & (clay <100))] = 3. #Sandy Loam (cond 1)
    stype[where((clay <   7) & (silt < 50) & (silt+2*clay >= 30) & (clay < 100))]   = 3      # sandy loam (cond 2)
    stype[where((silt >= 50) & (clay >= 12) & (clay < 27 ) & (clay < 100))] = 4      # silt loam (cond 1)
    stype[where((silt >= 50) & (silt < 80) & (clay < 12) & (clay < 100))] = 4      # silt loam (cond 2)
    stype[where((silt >= 80) & (clay < 12) & (clay < 100))]     = 5      # silt
    stype[where((clay >= 7 ) & (clay < 27) &(silt >= 28) & (silt < 50) & (sand <= 52) & (clay < 100))] = 6      # loam
    stype[where((clay >= 20) & (clay < 35) & (silt < 28) & (sand > 45) & (clay < 100))] = 7      # sandy clay loam
    stype[where((clay >= 27) & (clay < 40.) & (sand < 20) & (clay < 100))] =  8      # silt clay loam
    stype[where((clay >= 27) & (clay < 40.) & (sand >= 20) & (sand <= 45) & (clay < 100))] = 9      # clay loam
    stype[where((clay >= 35) & (sand > 45) & (clay < 100))] = 10     # sandy clay
    stype[where((clay >= 40) & (silt >= 40) & (clay < 100))] = 11     # silty clay
    stype[where((clay >= 40) & (sand <= 45) & (silt < 40) & (clay < 100))] = 12     # clay
    stype[where(stype == 0)] = 13
    return stype


def get_soil_type(path):
    clay,sand = get_sand_clay(path)
    st = clay.copy()
    st.data = calc_soil_type(clay*100,sand*100)
    return st
