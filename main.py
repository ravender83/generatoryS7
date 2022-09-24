import pandas as pd
import math
from tag import Zawor
from sensor import Sensor
from drive import Drive
import sys

'''
DONE
2) Dodac wykrywanie unikalności w przypadku roznych prefixow - Zrobiono 2022.09.17
4) Dodać listę mechanizmów na listę obsługi panelu HMI - Zrobiono 2022.09.21
5) Sprawdzić generowanie numeru MAX dla ekranów diagnostycznych. Linia 662 - Zrobiono 2022.09.21
6) W przypadku zaworow jednocewkowych dorzucic zamiane NaN na numer wyjscia - Zrobiono 2022.09.21

TODO
1) Dodac wyswietlanie wartosci w przypadku kontroli NOK
3) Dodac generowanie tagow sensorów hmi dla wizualizacji tych sensorów
'''

zawory = []
sensory = []
safety = []
przyciski = []
inne = []
napedy = []
lista_tagow = []


def zapisz(_plik, _txt, _fold):
    try:
        with open(f'{_fold}/{_plik}', "w", encoding="utf-8") as _f:
            _f.write(_txt)
            print(f'[OK] Wygenerowano {_plik}')
    except IOError as e:
        print(f'[NOK] Nie wygenerowano {_plik}')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano {_plik}')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def otworz(_plik, _fold):
    try:
        with open(f'{_fold}/{_plik}', "r", encoding="utf-8-sig") as _f:
            print(f'[OK] Wczytano szablon {_plik}')
            return _f.read()
    except IOError as e:
        print(f'[NOK] Nie wczytano {_plik}')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wczytano {_plik}')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def df_datas_parsing(_df):
    # Zmiana nazw na male litery. Sprawdzenie braku duplikatów
    _df.PREFIX = _df.PREFIX.dropna().astype(str).str.upper().str.strip()
    _df.NAME = _df.NAME.dropna().astype(str).str.lower().str.strip()
    _df.NAMEPL = _df.NAMEPL.dropna().astype(str).str.lower().str.strip()
    _df.SIDE_HP = _df.SIDE_HP.dropna().astype(str).str.strip().str.lower().str[0]
    _df.SIDE_WP = _df.SIDE_WP.dropna().astype(str).str.strip().str.lower().str[0]
    _df.SENSOR_HP = _df.SENSOR_HP.dropna().astype(str).str.strip().str.upper()
    _df.SENSOR_HP2 = _df.SENSOR_HP2.dropna().astype(str).str.strip().str.upper()
    _df.SENSOR_WP = _df.SENSOR_WP.dropna().astype(str).str.strip().str.upper()
    _df.SENSOR_WP2 = _df.SENSOR_WP2.dropna().astype(str).str.strip().str.upper()
    _df.OUTPUT_HP = _df.OUTPUT_HP.dropna().astype(str).str.strip().str.upper()
    _df.OUTPUT_WP = _df.OUTPUT_WP.dropna().astype(str).str.strip().str.upper()
    _df.IDLE = _df.IDLE.dropna().astype(str).str.strip().str.upper()
    _df.BRAKE_RELEASE = _df.BRAKE_RELEASE.dropna().astype(str).str.strip().str.upper()
    print('[OK] Parsowanie tekstu')


def df_parsing(_df):
    if (_df.SENSOR_HP.dropna().astype(str).str[0] != 'I').any():
        print('[NOK] Parsowanie io kolumny SENSOR_HP')
        print(_df.SENSOR_HP.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.SENSOR_HP2.dropna().astype(str).str[0] != 'I').any():
        print('[NOK] Parsowanie io kolumny SENSOR_HP2')
        print(_df.SENSOR_HP2.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.SENSOR_WP.dropna().astype(str).str[0] != 'I').any():
        print('[NOK] Parsowanie io kolumny SENSOR_WP')
        print(_df.SENSOR_WP.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.SENSOR_WP2.dropna().astype(str).str[0] != 'I').any():
        print('[NOK] Parsowanie io kolumny SENSOR_WP2')
        print(_df.SENSOR_WP2.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.OUTPUT_HP.dropna().astype(str).str[0] != 'Q').any():
        print('[NOK] Parsowanie io kolumny OUTPUT_HP')
        print(_df.OUTPUT_HP.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.OUTPUT_WP.dropna().astype(str).str[0] != 'Q').any():
        print('[NOK] Parsowanie io kolumny OUTPUT_WP')
        print(_df.OUTPUT_WP.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.IDLE.dropna().astype(str).str[0] != 'Q').any():
        print('[NOK] Parsowanie io kolumny IDLE')
        print(_df.IDLE.dropna())
        input('Press enter to exit...')
        exit()
    if (_df.BRAKE_RELEASE.dropna().astype(str).str[0] != 'Q').any():
        print('[NOK] Parsowanie io kolumny BRAKE_RELEASE')
        print(_df.BRAKE_RELEASE.dropna())
        input('Press enter to exit...')
        exit()
    kierunek = ['l', 'r', 'u', 'd', 'f', 'b', 'o', 'c']
    if (_df['SIDE_HP'].isin(kierunek) == False).any():
        print(_df['SIDE_HP'])
        print('[NOK] Parsowanie io kolumny SIDE_HP')
        print(set(_df.SIDE_HP.tolist()).difference(kierunek))
        input('Press enter to exit...')
        exit()
    if (_df['SIDE_WP'].isin(kierunek) == False).any():
        print('[NOK] Parsowanie io kolumny SIDE_WP')
        print(set(_df.SIDE_WP.tolist()).difference(kierunek))
        input('Press enter to exit...')
        exit()
    print('[OK] Parsowanie io')


def df_check_duplicates(_df):
    _df['test'] = _df['PREFIX'] + _df['NAME']
    if _df['test'].is_unique:
        print('[OK] Nazwy NAME są unikalne')
    else:
        print('[NOK] Nazwy NAME nie są unikalne')
        print(_df[_df.duplicated(subset=['NAME'], keep=False)].NAME)
        input('Press enter to exit...')
        exit()

    _df['test'] = _df['PREFIX'] + _df['NAMEPL']
    if _df['test'].is_unique:
        print('[OK] Nazwy NAMEPL są unikalne')
    else:
        print('[NOK] Nazwy NAMEPL nie są unikalne')
        print(_df[_df.duplicated(subset=['NAMEPL'
                                         ''], keep=False)].NAMEPL)
        input('Press enter to exit...')
        exit()

    # Pobiera listę wszystkich adresów i sprawdza, czy nie ma błędów duplikatów
    _dfio = (_df[['SENSOR_HP', 'SENSOR_WP', 'SENSOR_HP2', 'SENSOR_WP2', 'OUTPUT_HP', 'OUTPUT_WP', 'IDLE',
                 'BRAKE_RELEASE']].stack())
    if _dfio.is_unique:
        print('[OK] Adresy I/Q są unikalne')
    else:
        print('[NOK] Adresy I/Q nie są unikalne')
        print(_dfio[_dfio.duplicated(keep=False)])
        input('Press enter to exit...')
        exit()


def io_datas_parsing(_df):
    # Zmiana nazw na male litery. Sprawdzenie braku duplikatów
    #_df.PREFIX = _df.PREFIX.dropna().astype(str).str.upper()
    _df.PREFIX = _df.PREFIX.dropna().astype(str).str.strip()
    _df.NAME = _df.NAME.dropna().astype(str).str.lower().str.strip()
    _df.NAMEPL = _df.NAMEPL.dropna().astype(str).str.lower().str.strip()
    _df.ADRES = _df.ADRES.dropna().astype(str).str.strip().str.upper()
    print('[OK] Parsowanie sensorów')


def io_parsing(_df):
    if (_df.ADRES.dropna().astype(str).str[0] != 'I').any():
        print('[NOK] Parsowanie io kolumny ADRES')
        print(_df.ADRES.dropna())
        input('Press enter to exit...')
        exit() 
    print('[OK] Parsowanie io')


def io_check_duplicates(_df):
    _df['test'] = _df['PREFIX'] + _df['NAME']
    if _df['test'].is_unique:
        print('[OK] Nazwy NAME są unikalne')
    else:
        print('[NOK] Nazwy NAME nie są unikalne')
        print(_df[_df.duplicated(subset=['NAME'], keep=False)].NAME)
        input('Press enter to exit...')
        exit()

    _df['test'] = _df['PREFIX'] + _df['NAMEPL']
    if _df['test'].is_unique:
        print('[OK] Nazwy NAMEPL są unikalne')
    else:
        print('[NOK] Nazwy NAMEPL nie są unikalne')
        print(_df[_df.duplicated(subset=['NAMEPL'
                                         ''], keep=False)].NAMEPL)
        input('Press enter to exit...')
        exit()

    # Pobiera listę wszystkich adresów i sprawdza, czy nie ma błędów duplikatów
    _dfio = (_df[['ADRES']].stack())
    if _dfio.is_unique:
        print('[OK] Adresy I/Q są unikalne')
    else:
        print('[NOK] Adresy I/Q nie są unikalne')
        print(_dfio[_dfio.duplicated(keep=False)])
        input('Press enter to exit...')
        exit()


def drv_datas_parsing(_df):
    _df.NAME = _df.NAME.dropna().astype(str).str.upper().str.strip()
    _df.TYPE = _df.TYPE.dropna().astype(str).str.upper().str.strip()
    _df.PROFINET = _df.PROFINET.dropna().astype(str).str.lower().str.strip()
    print('[OK] Parsowanie napędów')


def drv_check_duplicates(_df):
    if _df['NAME'].is_unique:
        print('[OK] Nazwy NAME napędów są unikalne')
    else:
        print('[NOK] Nazwy NAME napędów nie są unikalne')
        print(_df[_df.duplicated(subset=['NAME'], keep=False)].NAME)
        input('Press enter to exit...')
        exit()


def generuj_tags_txt(_zawory, _sensory, _safety, _przyciski, _inne):
    _txt = '----------- VALVES -----------\n'
    for i in _zawory:
        _txt = _txt + f'{i.get_name}\n'
    _txt = _txt + '\n----------- ZAWORY -----------\n'
    for i in _zawory:
        _txt = _txt + f'{i.get_namepl}\n'

    zapisz("10_tags.txt", _txt, 'out')
'''
    _txt = _txt + '\n----------- IO TAGS -----------\n'
    # BR-vsen_imitation_HP_front BOOL I20.5 False True True True #nc - [I20.5] czujnik IMITACJA HP front
    _tmp = '\tFalse\tTrue\tTrue\tTrue\t'
    for i in _zawory:
        _ihp = f'{i.get_sensorNameHP}\tBOOL\t{i.sensorHP}{_tmp}\t{i.get_sensorNameHPcomment}'
        _ihp2 = f'{i.get_sensorNameHP2}\tBOOL\t{i.sensorHP2}{_tmp}\t{i.get_sensorNameHP2comment}'
        _iwp = f'{i.get_sensorNameWP}\tBOOL\t{i.sensorWP}{_tmp}\t{i.get_sensorNameWPcomment}'
        _iwp2 = f'{i.get_sensorNameWP2}\tBOOL\t{i.sensorWP2}{_tmp}\t{i.get_sensorNameWP2comment}'
        _ohp = f'{i.get_outputNameHP}\tBOOL\t{i.outputHP}{_tmp}\t{i.get_outputNameHPcomment}'
        _owp = f'{i.get_outputNameWP}\tBOOL\t{i.outputWP}{_tmp}\t{i.get_outputNameWPcomment}'
        _oidle = f'{i.get_outputNameIDLE}\tBOOL\t{i.outputIDLE}{_tmp}\t{i.get_outputNameIDLEcomment}'
        _obrake = f'{i.get_outputNameBRAKE}\tBOOL\t{i.outputBRAKE}{_tmp}\t{i.get_outputNameBRAKEcomment}'

        if i.sensorHP != 'nan':
            _txt = _txt + f'{_ihp}\n'
        if i.sensorHP2 != 'nan' and i.sensorHP2 != i.sensorHP:
            _txt = _txt + f'{_ihp2}\n'
        if i.sensorWP != 'nan':
            _txt = _txt + f'{_iwp}\n'
        if i.sensorWP2 != 'nan' and i.sensorWP2 != i.sensorWP:
            _txt = _txt + f'{_iwp2}\n'
        if i.outputHP != 'nan':
            _txt = _txt + f'{_ohp}\n'
        if i.outputWP != 'nan':
            _txt = _txt + f'{_owp}\n'
        if i.outputIDLE != 'nan':
            _txt = _txt + f'{_oidle}\n'
        if i.outputBRAKE != 'nan':
            _txt = _txt + f'{_obrake}\n'

    for i in _sensory:
        _i = f'{i.get_sensorName}\tBOOL\t{i.adres}{_tmp}\t{i.get_sensorNameComment}'
        if i.adres != 'nan':
            _txt = _txt + f'{_i}\n'        
    for i in _safety:
        _i = f'{i.get_sensorName}\tBOOL\t{i.adres}{_tmp}\t{i.get_sensorNameComment}'  
        if i.adres != 'nan':
            _txt = _txt + f'{_i}\n'          
    for i in _przyciski:
        _i = f'{i.get_sensorName}\tBOOL\t{i.adres}{_tmp}\t{i.get_sensorNameComment}'            
        if i.adres != 'nan':
            _txt = _txt + f'{_i}\n'
    for i in _inne:
        _i = f'{i.get_sensorName}\tBOOL\t{i.adres}{_tmp}\t{i.get_sensorNameComment}'            
        if i.adres != 'nan':
            _txt = _txt + f'{_i}\n'

    zapisz("10_tags.txt", _txt, 'out')
'''

def generuj_plc_tags_excel(_zawory, _sensory, _safety, _przyciski, _inne):
    _preparation_file = otworz("30_preparation.txt", 'out')
    _txt_hp = ''    
    _lista = []
    _adresyI = []
    _adresyQ = []
    _adresyIQ = []
    _tmp = ['True', 'True', 'True', '', '', '']
    for i in _zawory:
        _txt_hp += f'A "A-DBVALVES".{i.prefix}.{i.name}.out.in_hp\n'  
        if i.sensorHP != 'nan':
            _lista.append([i.get_sensorNameHP, 'io', 'Bool', i.sensorHP, i.get_sensorNameHPcomment]+_tmp)
            _adresyI.append(int(i.sensorHP[2:-2:]))
            _adresyIQ.append([i.sensorHP[1:], i.get_sensorNameHPsmall])
        if i.sensorHP2 != 'nan' and i.sensorHP2 != i.sensorHP:
            _lista.append([i.get_sensorNameHP2, 'io', 'Bool', i.sensorHP2, i.get_sensorNameHP2comment]+_tmp)
            _adresyI.append(int(i.sensorHP2[2:-2:]))
            _adresyIQ.append([i.sensorHP2[1:], i.get_sensorNameHP2small])
        if i.sensorWP != 'nan':
            _lista.append([i.get_sensorNameWP, 'io', 'Bool', i.sensorWP, i.get_sensorNameWPcomment]+_tmp)
            _adresyI.append(int(i.sensorWP[2:-2:]))
            _adresyIQ.append([i.sensorWP[1:], i.get_sensorNameWPsmall])
        if i.sensorWP2 != 'nan' and i.sensorWP2 != i.sensorWP:
            _lista.append([i.get_sensorNameWP2, 'io', 'Bool', i.sensorWP2, i.get_sensorNameWP2comment]+_tmp)
            _adresyI.append(int(i.sensorWP2[2:-2:]))
            _adresyIQ.append([i.sensorWP2[1:], i.get_sensorNameWP2small])
        if i.outputHP != 'nan':
            _lista.append([i.get_outputNameHP, 'io', 'Bool', i.outputHP, i.get_outputNameHPcomment]+_tmp)
            _adresyQ.append(int(i.outputHP[2:-2:]))
            _adresyIQ.append([i.outputHP[1:], i.get_outputNameHPsmall])
        if i.outputWP != 'nan':
            _lista.append([i.get_outputNameWP, 'io', 'Bool', i.outputWP, i.get_outputNameWPcomment]+_tmp)
            _adresyQ.append(int(i.outputWP[2:-2:]))
            _adresyIQ.append([i.outputWP[1:], i.get_outputNameWPsmall])
        if i.outputIDLE != 'nan':
            _lista.append([i.get_outputNameIDLE, 'io', 'Bool', i.outputIDLE, i.get_outputNameIDLEcomment]+_tmp)
            _adresyQ.append(int(i.outputIDLE[2:-2:]))
            _adresyIQ.append([i.outputIDLE[1:], i.get_outputNameIDLEsmall])
        if i.outputBRAKE != 'nan':
            _lista.append([i.get_outputNameBRAKE, 'io', 'Bool', i.outputBRAKE, i.get_outputNameBRAKEcomment]+_tmp)
            _adresyQ.append(int(i.outputBRAKE[2:-2:]))
            _adresyIQ.append([i.outputBRAKE[1:], i.get_outputNameBRAKEsmall])

    _preparation_file = _preparation_file.replace('{VALVES_HP}', _txt_hp) 
    zapisz("30_preparation.txt", _preparation_file, 'out') 

    for i in _sensory:
        if i.adres != 'nan':
            _lista.append([i.get_sensorName, 'io', 'Bool', i.adres, i.get_sensorNameComment]+_tmp)
            _adresyI.append(int(i.adres[2:-2:]))
            _adresyIQ.append([i.adres[1:], i.get_sensorNameSmall])
    for i in _safety:
        if i.adres != 'nan':
            _lista.append([i.get_sensorName, 'io', 'Bool', i.adres, i.get_sensorNameComment]+_tmp)
            _adresyI.append(int(i.adres[2:-2:]))
            _adresyIQ.append([i.adres[1:], i.get_sensorNameSmall])
    for i in _przyciski:
        if i.adres != 'nan':
            _lista.append([i.get_sensorName, 'io', 'Bool', i.adres, i.get_sensorNameComment]+_tmp) 
            _adresyI.append(int(i.adres[2:-2:]))   
            _adresyIQ.append([i.adres[1:], i.get_sensorNameSmall])      
    for i in _inne:
        if i.adres != 'nan':
            _lista.append([i.get_sensorName, 'io', 'Bool', i.adres, i.get_sensorNameComment]+_tmp) 
            if i.adres[1] == 'I':
                _adresyI.append(int(i.adres[2:-2:])) 
                _adresyIQ.append([i.adres[1:], i.get_sensorNameSmall])     
            elif i.adres[1] == 'Q':
                _adresyQ.append(int(i.adres[2:-2:]))  
                _adresyIQ.append([i.adres[1:], i.get_sensorNameSmall])    
    _adresyI = sorted(set(_adresyI), key=int)
    _adresyQ = sorted(set(_adresyQ), key=int)

    for i in _adresyI:
        _lista.append([f'I{str(i)}', 'Default tag table', 'Byte', f'IB{str(i)}', f'IB{str(i)}']+_tmp) 
    for i in _adresyQ:
        _lista.append([f'Q{str(i)}', 'Default tag table', 'Byte', f'QB{str(i)}', f'QB{str(i)}']+_tmp)         

    _df = pd.DataFrame(_lista, columns=['Name', 'Path', 'Data Type', 'Logical Address', 'Comment', 'Hmi Visible',
                                          'Hmi Accessible', 'Hmi Writeable', 'Typeobject ID', 'Version ID', 'BelongsToUnit'])
    try:
        _df.to_excel("out/10_Tags.xlsx", sheet_name='PLC Tags', index=False)
        print(f'[OK] Wygenerowano Tags.xlsx')
        return _adresyI, _adresyQ, _adresyIQ
    except IOError as e:
        print(f'[NOK] Nie wygenerowano Tags.xlsx')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano Tags.xlsx')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def generuj_dbvalves_txt(_df):
    _txt = '----------- DBVALVES datablock structs-----------\n'
    _tmp = '\tStruct\t\tFalse\tTrue\tTrue\tTrue\tFalse\t\t'
    _prefixy = sorted(set(_df.PREFIX))
    for i in _prefixy:
        _txt = _txt + f'{i}{_tmp}\n'

    for i in _prefixy:
        _pre = _df.loc[_df.PREFIX == i]
        _txt = _txt + f'\n--- {i} ---\n'
        _tmp = '\t"Tstate"\t\tFalse\tTrue\tTrue\tTrue\tFalse\t\t'
        for index, row in _pre.iterrows():
            _txt = _txt + f'{row.NAME.upper()}{_tmp}[{index+1}] {row.PREFIX}-{row.NAMEPL}\n'
    zapisz("11_dbvalves.txt", _txt, 'out')


def generuj_dbvalves_db(_df):
    _dbvalves_data = otworz("DBVALVES_db.txt", 'templates')
    _valve_data = otworz("DBVALVES_db_1_1.txt", 'templates')
    _prefixy = sorted(set(_df.PREFIX))

    _txt = ''
    for i in _prefixy:
        _pre = _df.loc[_df.PREFIX == i]
        _txt = _txt + f'{i} : Struct\n'

        for index, row in _pre.iterrows():
            _valve_szablon = _valve_data
            _valve_szablon = _valve_szablon.replace('{PREFIX}', str(i))
            _valve_szablon = _valve_szablon.replace('{DBVALVE}', row.NAME.upper())
            _valve_szablon = _valve_szablon.replace('{DBVALVEPL}', row.NAMEPL)
            _valve_szablon = _valve_szablon.replace('{INDEX}', str(index+1))
            _txt += '\t' + _valve_szablon + '\n'
        _txt = _txt + 'END_STRUCT;\n'

    _dbvalves_data = _dbvalves_data.replace('{STRUCT}', _txt)
    _dbvalves_data = _dbvalves_data.replace('{ILOSC}', str(len(_df)))
    zapisz("11_DBVALVES_n.db", _dbvalves_data, 'out')


def zliczaj(_lduzy, _lmaly):
    _lmaly += 1
    if _lmaly >= 16:
        _lmaly = 0
        _lduzy += 1
    return _lduzy, _lmaly


def generuj_hmialarms_excel(_zawory, _sensory, _safety, _przyciski):
    _txt_hp = ''
    _msg = 1000
    _index = 1

    _lista = []
    _lista_tagow = []
    # ===== Mechanizmy =======
    _tmp = ['<No value>', '0', '<No value>', '0', 'VALVE', 'True', 'none']
    _columns = ['Name', 'Alarm text [pl-PL], Alarm text', 'FieldInfo [Alarm text]', 'Class', 'Trigger tag', 'Trigger bit', 'Acknowledgement tag', 'Acknowledgement bit', 'PLC acknowledgement tag', 'PLC acknowledgement bit', 'Group', 'Report', 'Info text [pl-PL], Info text']
    lduzy = 0
    lmaly = 0
    for i in _zawory:
        if i.sensorHP != 'nan':
            _lista.append([f'valve_{i.sensorHP[1:]}_hp', f'{i.get_sensorNameHPcommentSmall[0:]} ({i.index}) jest nieaktywny', '', 'VALVE',
                           'A-ALARMS_VALVES_err'+str(lduzy), f'{str(lmaly)}'] + _tmp)
            i.byteHP = lduzy
            i.bitHP = lmaly
            lduzy, lmaly = zliczaj(lduzy, lmaly)
            _lista_tagow.append('A-ALARMS_VALVES_err'+str(lduzy))
            i.msg_hp = _msg + _index
            _txt_hp += f'{str(i.msg_hp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1

        if i.sensorHP2 != 'nan' and i.sensorHP2 != i.sensorHP:
            _lista.append([f'valve_{i.sensorHP2[1:]}_hp2', f'{i.get_sensorNameHP2commentSmall[0:]} ({i.index}) jest nieaktywny', '', 'VALVE',
                           'A-ALARMS_VALVES_err' + str(lduzy), f'{str(lmaly)}'] + _tmp)
            i.byteHP2 = lduzy
            i.bitHP2 = lmaly            
            lduzy, lmaly = zliczaj(lduzy, lmaly)
            _lista_tagow.append('A-ALARMS_VALVES_err'+str(lduzy))
            i.msg_hp2 = _msg + _index
            _txt_hp += f'{str(i.msg_hp2)}\t{_lista[-1:][0][1]}\n'            
            _index += 1        

        if i.sensorWP != 'nan':
            _lista.append([f'valve_{i.sensorWP[1:]}_wp', f'{i.get_sensorNameWPcommentSmall[0:]} ({i.index}) jest nieaktywny', '', 'VALVE',
                           'A-ALARMS_VALVES_err'+str(lduzy), f'{str(lmaly)}'] + _tmp)
            i.byteWP = lduzy
            i.bitWP = lmaly            
            lduzy, lmaly = zliczaj(lduzy, lmaly)
            _lista_tagow.append('A-ALARMS_VALVES_err'+str(lduzy))
            i.msg_wp = _msg + _index
            _txt_hp += f'{str(i.msg_wp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1            

        if i.sensorWP2 != 'nan' and i.sensorWP2 != i.sensorWP:
            _lista.append([f'valve_{i.sensorWP2[1:]}_wp2', f'{i.get_sensorNameWP2commentSmall[0:]} ({i.index}) jest nieaktywny', '', 'VALVE',
                           'A-ALARMS_VALVES_err' + str(lduzy), f'{str(lmaly)}'] + _tmp)
            i.byteWP2 = lduzy
            i.bitWP2 = lmaly            
            lduzy, lmaly = zliczaj(lduzy, lmaly)  
            _lista_tagow.append('A-ALARMS_VALVES_err'+str(lduzy))  
            i.msg_wp2 = _msg + _index
            _txt_hp += f'{str(i.msg_wp2)}\t{_lista[-1:][0][1]}\n'            
            _index += 1       

    # ===== Sensory =======
    _tmp = ['<No value>', '0', '<No value>', '0', 'SENSOR', 'True', 'none']
    _columns = ['Name', 'Alarm text [pl-PL], Alarm text', 'FieldInfo [Alarm text]', 'Class', 'Trigger tag', 'Trigger bit', 'Acknowledgement tag', 'Acknowledgement bit', 'PLC acknowledgement tag', 'PLC acknowledgement bit', 'Group', 'Report', 'Info text [pl-PL], Info text']
    lduzy_sensor = 0
    lmaly_sensor = 0
    for i in _sensory:
        if i.adres != 'nan':
            _lista.append([f'sen_{i.adres[1:]}_hp', f'{i.get_sensorNameComment} jest aktywny', '', 'SENSOR',
                           'A-ALARMS_SENSORS_sen'+str(lduzy_sensor), f'{str(lmaly_sensor)}'] + _tmp)
            i.byteHP = lduzy_sensor
            i.bitHP = lmaly_sensor            
            lduzy_sensor, lmaly_sensor = zliczaj(lduzy_sensor, lmaly_sensor)
            _lista_tagow.append('A-ALARMS_SENSORS_sen'+str(lduzy_sensor))
            i.msg_hp = _msg + _index
            _txt_hp += f'{str(i.msg_hp)}\t{_lista[-1:][0][1]}\n'
            _index += 1                

        if i.adres != 'nan':
            _lista.append([f'sen_{i.adres[1:]}_wp', f'{i.get_sensorNameComment} jest nieaktywny', '', 'SENSOR',
                           'A-ALARMS_SENSORS_sen'+str(lduzy_sensor), f'{str(lmaly_sensor)}'] + _tmp)
            i.byteWP = lduzy_sensor
            i.bitWP = lmaly_sensor              
            lduzy_sensor, lmaly_sensor = zliczaj(lduzy_sensor, lmaly_sensor)
            _lista_tagow.append('A-ALARMS_SENSORS_sen'+str(lduzy_sensor))
            i.msg_wp = _msg + _index
            _txt_hp += f'{str(i.msg_wp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1 

    # ===== Safety =======
    _tmp = ['<No value>', '0', '<No value>', '0', 'SAFETY', 'True', 'none']
    _columns = ['Name', 'Alarm text [pl-PL], Alarm text', 'FieldInfo [Alarm text]', 'Class', 'Trigger tag', 'Trigger bit', 'Acknowledgement tag', 'Acknowledgement bit', 'PLC acknowledgement tag', 'PLC acknowledgement bit', 'Group', 'Report', 'Info text [pl-PL], Info text']
    lduzy_safety = 0
    lmaly_safety = 0
    for i in _safety:
        if i.adres != 'nan':
            _lista.append([f'safe_{i.adres[1:]}_hp', f'{i.get_sensorNameComment} jest nieaktywny', '', 'SAFETY',
                           'A-ALARMS_SAFETY_sft'+str(lduzy_safety), f'{str(lmaly_safety)}'] + _tmp)
            i.byteWP = lduzy_safety
            i.bitWP = lmaly_safety              
            lduzy_safety, lmaly_safety = zliczaj(lduzy_safety, lmaly_safety)
            _lista_tagow.append('A-ALARMS_SAFETY_sft'+str(lduzy_safety))
            i.msg_hp = _msg + _index
            _txt_hp += f'{str(i.msg_hp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1 
    # ===== Przyciski =======
    _tmp = ['<No value>', '0', '<No value>', '0', 'BUTTON', 'True', 'none']
    _columns = ['Name', 'Alarm text [pl-PL], Alarm text', 'FieldInfo [Alarm text]', 'Class', 'Trigger tag', 'Trigger bit', 'Acknowledgement tag', 'Acknowledgement bit', 'PLC acknowledgement tag', 'PLC acknowledgement bit', 'Group', 'Report', 'Info text [pl-PL], Info text']
    lduzy_button = 0
    lmaly_button = 0
    for i in _przyciski:
        if i.adres != 'nan':
            _lista.append([f'btn_{i.adres[1:]}_hp', f'{i.get_sensorNameComment} jest aktywny', '', 'BUTTON',
                           'A-ALARMS_BUTTONS_btn'+str(lduzy_button), f'{str(lmaly_button)}'] + _tmp)
            i.byteHP = lduzy_button
            i.bitHP = lmaly_button               
            lduzy_button, lmaly_button = zliczaj(lduzy_button, lmaly_button)
            _lista_tagow.append('A-ALARMS_BUTTONS_btn'+str(lduzy_button))
            i.msg_hp = _msg + _index
            _txt_hp += f'{str(i.msg_hp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1 
        if i.adres != 'nan':
            _lista.append([f'btn_{i.adres[1:]}_wp', f'{i.get_sensorNameComment} jest nieaktywny', '', 'BUTTON',
                           'A-ALARMS_BUTTONS_btn'+str(lduzy_button), f'{str(lmaly_button)}'] + _tmp)
            i.byteWP = lduzy_button
            i.bitWP = lmaly_button              
            lduzy_button, lmaly_button = zliczaj(lduzy_button, lmaly_button)
            _lista_tagow.append('A-ALARMS_BUTTONS_btn'+str(lduzy_button))
            i.msg_wp = _msg + _index
            _txt_hp += f'{str(i.msg_wp)}\t{_lista[-1:][0][1]}\n'            
            _index += 1 
    zapisz("31_hmi_messages.txt", _txt_hp, 'out')            
    _df = pd.DataFrame(_lista, columns=_columns)
    _df.index.name = 'ID'
    _df.index += 1
    _lista_tagow = list(set(_lista_tagow))
    lista_tagow.extend(_lista_tagow)
    try:
        _df.to_excel("out/15_HMIAlarms.xlsx", sheet_name='DiscreteAlarms', index=True)
        print(f'[OK] Wygenerowano HMIAlarms.xlsx')
        return [lduzy, lduzy_sensor, lduzy_safety, lduzy_button]
    except IOError as e:
        print(f'[NOK] Nie wygenerowano HMIAlarms.xlsx')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano HMIAlarms.xlsx')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def generuj_hmialarms_tagi_excel(_lista):
    _lista_gotowa = []
    _tmp = ['UInt', '2', 'Binary', 'Symbolic access', '<No Value>', 'False', '<No Value>', '<No Value>', '0', '<No Value>', '<No Value>', 'Continuous', '1 s', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'False', '10', '0', '100', '0', 'False', 'None', 'False']
    _columns = ['Name', 'Path', 'Connection', 'PLC tag', 'DataType', 'Length', 'Coding', 'Access Method', 'Address', 'Indirect addressing', 'Index tag', 'Start value', 'ID tag', 'Display name [pl-PL]', 'Comment [pl-PL]', 'Acquisition mode', 'Acquisition cycle', 'Limit Upper 2 Type', 'Limit Upper 2', 'Limit Upper 1 Type', 'Limit Upper 1', 'Limit Lower 1 Type', 'Limit Lower 1', 'Limit Lower 2 Type', 'Limit Lower 2', 'Linear scaling', 'End value PLC', 'Start value PLC', 'End value HMI', 'Start value HMI', 'Gmp relevant', 'Confirmation Type', 'Mandatory Commenting']
    for i in (_lista):
        _txt = i[8:].replace('_', '.')
        _lista_gotowa.append([f'A-ALARMS{i[8:]}', 'Default tag table', 'PLC', f'"A-ALARMS"{_txt}'] + _tmp)
    _tmp = ['Bool', '1', 'Binary', 'Symbolic access', '<No Value>', 'False', '<No Value>', '<No Value>', '0', '<No Value>', '<No Value>', 'Cyclic in operation', '1 s', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'False', '10', '0', '100', '0', 'False', 'None', 'False']
    _lista_gotowa.append(['A-ALARMS_error', 'Default tag table', 'PLC', '"A-ALARMS.error"'] + _tmp)
    _lista_gotowa.append(['A-ALARMS_OTHER_error', 'Default tag table', 'PLC', '"A-ALARMS.OTHER.error"'] + _tmp)
    _lista_gotowa.append(['A-ALARMS_DRIVES_error', 'Default tag table', 'PLC', '"A-ALARMS.DRIVES.error"'] + _tmp)
    _lista_gotowa.append(['A-ALARMS_SAFETY_error', 'Default tag table', 'PLC', '"A-ALARMS.SAFETY.error"'] + _tmp)
    _lista_gotowa.append(['A-ALARMS_SENSORS_error', 'Default tag table', 'PLC', '"A-ALARMS.SENSORS.error"'] + _tmp)
    _lista_gotowa.append(['A-ALARMS_VALVES_error', 'Default tag table', 'PLC', '"A-ALARMS.VALVES.error"'] + _tmp)

    _df = pd.DataFrame(_lista_gotowa, columns=_columns)
    try:
        _df.to_excel("out/14_HMIAlarmsTags.xlsx", sheet_name='Hmi Tags', index=False)
        print(f'[OK] Wygenerowano HMIAlarmsTags.xlsx')
    except IOError as e:
        print(f'[NOK] Nie wygenerowano HMIAlarmsTags.xlsx')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano HMIAlarmsTags.xlsx')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def generuj_alarms_db(_licznik, _zawory, _sensory, _safety, _buttons, _adresyI, _adresyQ):
    _dbvalves_data = otworz("A-ALARMS_db.txt", 'templates')
    _valve_data = otworz("A-ALARMS_db_1.txt", 'templates')

    # --- Valves 0 ---
    _txt = ''
    for i in range(_licznik[0]+1):
        _txt = _txt + f'err{i} : UInt;\n'
    _dbvalves_data = _dbvalves_data.replace('{VALVES_STRUCT}', _txt)

    # --- Sensors 1 ---
    _txt = ''
    for i in range(_licznik[1]+1):
        _txt = _txt + f'sen{i} : UInt;\n'
    _dbvalves_data = _dbvalves_data.replace('{SENSORS_STRUCT}', _txt)

    # --- Safety 2 ---
    _txt = ''
    for i in range(_licznik[2]+1):
        _txt = _txt + f'sft{i} : UInt;\n'
    _dbvalves_data = _dbvalves_data.replace('{SAFETY_STRUCT}', _txt)

    # --- Buttons 2 ---
    _txt = ''
    for i in range(_licznik[3]+1):
        _txt = _txt + f'btn{i} : UInt;\n'
    _dbvalves_data = _dbvalves_data.replace('{BUTTONS_STRUCT}', _txt)

    _txt = ''
    for i in _sensory:
        _valve_szablon = _valve_data
        _valve_szablon = _valve_szablon.replace('{SENSOR}', i.get_sensorName)
        _valve_szablon = _valve_szablon.replace('{COMMENT}', i.get_sensorNameCommentSmall)
        _txt += _valve_szablon + '\n'
    _dbvalves_data = _dbvalves_data.replace('{SENSORS2_STRUCT}', _txt)

    _txt = ''
    for i in _safety:
        _valve_szablon = _valve_data
        _valve_szablon = _valve_szablon.replace('{SENSOR}', i.get_sensorName)
        _valve_szablon = _valve_szablon.replace('{COMMENT}', i.get_sensorNameCommentSmall)
        _txt += _valve_szablon + '\n'
    _dbvalves_data = _dbvalves_data.replace('{SAFETY2_STRUCT}', _txt)    

    _txt = ''
    for i in _buttons:
        _valve_szablon = _valve_data
        _valve_szablon = _valve_szablon.replace('{SENSOR}', i.get_sensorName)
        _valve_szablon = _valve_szablon.replace('{COMMENT}', i.get_sensorNameCommentSmall)
        _txt += _valve_szablon + '\n'
    _dbvalves_data = _dbvalves_data.replace('{BUTTONS2_STRUCT}', _txt)       

    _dbvalves_data = _dbvalves_data.replace('{DRIVES_STRUCT}', 'drv0 : UInt;\n')
    _dbvalves_data = _dbvalves_data.replace('{IN}', str(len(_adresyI)))
    _dbvalves_data = _dbvalves_data.replace('{OUT}', str(len(_adresyQ)))
    _dbvalves_data = _dbvalves_data.replace('{IN_MAX}', str(math.ceil(len(_adresyI) / 9)))
    _dbvalves_data = _dbvalves_data.replace('{OUT_MAX}', str(math.ceil(len(_adresyQ) / 9)))
    zapisz("13_ALARMS_n.db", _dbvalves_data, 'out')


def szablon_nan(aktualny_szablon, co, na_co, alternatywa):
    if na_co == 'nan' or na_co == 'an':
        aktualny_szablon = aktualny_szablon.replace(co, alternatywa)
    else:
        aktualny_szablon = aktualny_szablon.replace(co, na_co)
    return aktualny_szablon


def generuj_valves_outputs_scl(_zawory):
    _valves_data = otworz("VALVES_outputs_scl.txt", 'templates')
    _members_data = otworz("VALVES_outputs_scl_1.txt", 'templates')

    _members_szablon = ''
    for i in _zawory:
        _szablon = _members_data
        _szablon = _szablon.replace('{DBVALVE_TITLE}', f'{i.prefix} {i.namepl.upper()}')
        _szablon = _szablon.replace('{DBVALVE}', f'{i.prefix}.{i.namepl.upper()}')
        _szablon = _szablon.replace('{INDEX}', f'{i.index}')
        _szablon = szablon_nan(_szablon, '{in_sensor_hp}', i.sensorHP, 'nan')
        _szablon = szablon_nan(_szablon, '{in_sensor_hp2}', i.sensorHP2, 'nan')
        _szablon = szablon_nan(_szablon, '{in_sensor_wp}', i.sensorWP, 'nan')
        _szablon = szablon_nan(_szablon, '{in_sensor_wp2}', i.sensorWP2, 'nan')
        _szablon = szablon_nan(_szablon, '{in_ez_hp}', i.outputHP, f'"DBVALVES".{i.prefix}.{i.namepl.upper()}.test.dummy_HP')
        _szablon = szablon_nan(_szablon, '{in_ez_wp}', i.outputWP, f'"DBVALVES".{i.prefix}.{i.namepl.upper()}.test.dummy_WP')
        _szablon = szablon_nan(_szablon, '{in_ez_idle}', i.outputIDLE, f'"DBVALVES".{i.prefix}.{i.namepl.upper()}.test.dummy_IDLE')
        _szablon = szablon_nan(_szablon, '{in_Ipw1}', i.sensorHP[1:], ' ')
        if i.sensorHP2 != i.sensorHP:
            _szablon = szablon_nan(_szablon, '{in_Ipw2}', i.sensorHP2[1:], ' ')
        else:
            _szablon = _szablon.replace('{in_Ipw2}', ' ')
        _szablon = szablon_nan(_szablon, '{in_Ipr1}', i.sensorWP[1:], ' ')
        if i.sensorWP2 != i.sensorWP:
            _szablon = szablon_nan(_szablon, '{in_Ipr2}', i.sensorWP2[1:], ' ')
        else:
            _szablon = _szablon.replace('{in_Ipr2}', ' ')
        _szablon = szablon_nan(_szablon, '{in_Qpw}', i.outputHP[1:], ' ')
        _szablon = szablon_nan(_szablon, '{in_Qpr}', i.outputWP[1:], ' ')
        _members_szablon += _szablon

    _valves_data = _valves_data.replace('{ALL_STRUCTS}', _members_szablon)
    zapisz("19_valve_outputs.scl", _valves_data, 'out')


def generuj_valves_outputs_stl(_zawory):
    _valves_data = otworz("A-Outputs_valves.txt", 'templates')
    _members_data = otworz("A-Outputs_valves_1.txt", 'templates')

    _members_szablon = ''
    for i in _zawory:
        _szablon = _members_data
        _szablon = _szablon.replace('{DBVALVE_TITLE}', f'{i.prefix} {i.namepl.upper()}')
        _szablon = _szablon.replace('{DBVALVE_TITLE_EN}', f'{i.prefix} {i.name.upper()}')
        _szablon = _szablon.replace('{DBVALVE}', f'{i.prefix}.{i.name.upper()}')
        _szablon = _szablon.replace('{INDEX}', f'{i.index}')
        _szablon = szablon_nan(_szablon, '{in_sensor_hp}', i.sensorHP[1:], i.outputHP[1:])
        _szablon = szablon_nan(_szablon, '{in_sensor_hp2}', i.sensorHP2[1:], i.outputHP[1:])
        _szablon = szablon_nan(_szablon, '{in_sensor_wp}', i.sensorWP[1:], i.outputWP[1:])
        _szablon = szablon_nan(_szablon, '{in_sensor_wp2}', i.sensorWP2[1:], i.outputWP[1:])
        _szablon = szablon_nan(_szablon, '{in_ez_hp}', i.outputHP[1:], f'"A-DBVALVES".{i.prefix}.{i.name.upper()}.test.HP_DUMMY')
        _szablon = szablon_nan(_szablon, '{in_ez_wp}', i.outputWP[1:], f'"A-DBVALVES".{i.prefix}.{i.name.upper()}.test.WP_DUMMY')
        _szablon = szablon_nan(_szablon, '{in_ez_idle}', i.outputIDLE[1:], f'"A-DBVALVES".{i.prefix}.{i.name.upper()}.test.IDLE_DUMMY')
        _szablon = szablon_nan(_szablon, '{brake}', i.outputBRAKE[1:], '#brake')
        _szablon = szablon_nan(_szablon, '{in_Ipw1}', i.sensorHP[1:], ' ')
        _szablon = _szablon.replace('{byteHP}', str(i.byteHP))
        _szablon = _szablon.replace('{bitHP}', str(i.bitHP))
        _szablon = _szablon.replace('{byteWP}', str(i.byteWP))
        _szablon = _szablon.replace('{bitWP}', str(i.bitWP))        
        if i.sensorHP2 != i.sensorHP:
            _szablon = szablon_nan(_szablon, '{in_Ipw2}', i.sensorHP2[1:], ' ')
        else:
            _szablon = _szablon.replace('{in_Ipw2}', ' ')
        _szablon = szablon_nan(_szablon, '{in_Ipr1}', i.sensorWP[1:], ' ')
        if i.sensorWP2 != i.sensorWP:
            _szablon = szablon_nan(_szablon, '{in_Ipr2}', i.sensorWP2[1:], ' ')
        else:
            _szablon = _szablon.replace('{in_Ipr2}', ' ')
        _szablon = szablon_nan(_szablon, '{in_Qpw}', i.outputHP[1:], ' ')
        _szablon = szablon_nan(_szablon, '{in_Qpr}', i.outputWP[1:], ' ')
        _members_szablon += _szablon

    _valves_data = _valves_data.replace('{ALL_STRUCTS}', _members_szablon)
    zapisz("19_valve_outputs_n.awl", _valves_data, 'out')


def generuj_valves_instances(_zawory):
    _valves_data = otworz("DBVALVES_INST.db", 'templates')

    _members_szablon = ''
    for i in _zawory:
        _szablon = _valves_data
        _szablon = _szablon.replace('{DBVALVE_TITLE}', f'{i.prefix} {i.namepl.upper()}')
        #_members_szablon += _szablon
        _members_szablon="{}{}".format(_members_szablon,_szablon)

    zapisz("20_valve_instance_n.db", _members_szablon, 'out')    


def generuj_hmialarms_class():
    _txt = 'VALVE\tVALVE\tAlarm without acknowledgment\n'
    _txt = _txt + 'SENSOR\tSENSOR\tAlarm without acknowledgment\n'
    _txt = _txt + 'SAFETY\tSAFETY\tAlarm without acknowledgment\n'
    _txt = _txt + 'BUTTON\tBUTTON\tAlarm without acknowledgment\n'
    _txt = _txt + 'OTHER\tOTHER\tAlarm without acknowledgment\n'
    _txt = _txt + 'DRIVES\tDRIVES\tAlarm without acknowledgment\n'
    zapisz("12_alarm_class.txt", _txt, 'out')


def generuj_sensors(_licznik, _sensory, _safety, _buttons, _adresyI, _adresyQ):
    _sensors_data = otworz("A-Sensors.txt", 'templates')
    _sensors1_data = otworz("A-Sensors_1.txt", 'templates')
    _sensors2_data = otworz("A-Sensors_2.txt", 'templates')  
    _sensors3_data = otworz("A-Sensors_3.txt", 'templates')

    # VALVES 0
    _error_szablon = ''
    for i in range(_licznik[0]+1):
        _szablon = _sensors1_data
        _szablon = _szablon.replace('{bytebit}', f'"A-ALARMS".VALVES.err{str(i)}')
        _error_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{VALVES_error}', _error_szablon)

    # SENSORS 1
    _error_szablon = ''
    for i in range(_licznik[1]+1):
        _szablon = _sensors1_data
        _szablon = _szablon.replace('{bytebit}', f'"A-ALARMS".SENSORS.sen{str(i)}')
        _error_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{SENSORS_error}', _error_szablon)    

    # SAFETY 2
    _error_szablon = ''
    for i in range(_licznik[2]+1):
        _szablon = _sensors1_data
        _szablon = _szablon.replace('{bytebit}', f'"A-ALARMS".SAFETY.sft{str(i)}')
        _error_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{SAFETY_error}', _error_szablon)      

    # BUTTONS 3
    _error_szablon = ''
    for i in range(_licznik[3]+1):
        _szablon = _sensors1_data
        _szablon = _szablon.replace('{bytebit}', f'"A-ALARMS".BUTTONS.btn{str(i)}')
        _error_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{BUTTONS_error}', _error_szablon)     

    # Generowanie networków sensorów
    _preparation_file = otworz("30_preparation.txt", 'out')
    _txt_hp = ''
    _signals_szablon = 'NETWORK\nTITLE = ======== SENSORS =========\n'    
    for i in _sensory:
        _szablon = _sensors2_data
        _szablon = _szablon.replace('{TYP}', 'SENSORS')
        _szablon = _szablon.replace('{TITLE_PL}', i.get_sensorNameCommentSmall)
        _szablon = _szablon.replace('{TITLE_EN}', i.get_sensorNameCommentSmallEN)   
        _szablon = _szablon.replace('{ADRES}', i.adres)  
        _szablon = _szablon.replace('{SENSOR_EN}', i.get_sensorName)   
        _szablon = _szablon.replace('{byteHP}', str(i.byteHP))  
        _szablon = _szablon.replace('{bitHP}', str(i.bitHP))  
        _szablon = _szablon.replace('{byteWP}', str(i.byteWP))  
        _szablon = _szablon.replace('{bitWP}', str(i.bitWP))   
        _szablon = _szablon.replace('{typ}', 'sen') 
        _txt_hp += f'A "A-ALARMS".SENSORS."{i.get_sensorName}".ok\n'      
        _signals_szablon += _szablon + '\n'
    _signals_szablon = _signals_szablon + '\n' 
    _preparation_file = _preparation_file.replace('{SENSORS_HP}', _txt_hp) 
    zapisz("30_preparation.txt", _preparation_file, 'out')  

    # Generowanie networków przyciskow
    _preparation_file = otworz("30_preparation.txt", 'out')
    _txt_hp = ''
    _signals_szablon += 'NETWORK\nTITLE = ======== BUTTONS =========\n'    
    for i in _buttons:
        _szablon = _sensors2_data
        _szablon = _szablon.replace('{TYP}', 'BUTTONS')
        _szablon = _szablon.replace('{TITLE_PL}', i.get_sensorNameCommentSmall)
        _szablon = _szablon.replace('{TITLE_EN}', i.get_sensorNameCommentSmallEN)   
        _szablon = _szablon.replace('{ADRES}', i.adres)  
        _szablon = _szablon.replace('{SENSOR_EN}', i.get_sensorName)   
        _szablon = _szablon.replace('{byteHP}', str(i.byteHP))  
        _szablon = _szablon.replace('{bitHP}', str(i.bitHP))  
        _szablon = _szablon.replace('{byteWP}', str(i.byteWP))  
        _szablon = _szablon.replace('{bitWP}', str(i.bitWP))   
        _szablon = _szablon.replace('{typ}', 'btn')
        _txt_hp += f'A "A-ALARMS".BUTTONS."{i.get_sensorName}".ok\n'      
        _signals_szablon += _szablon + '\n'      
    _preparation_file = _preparation_file.replace('{BUTTONS_HP}', _txt_hp) 

    _preparation_file = _preparation_file.replace('{DRIVES_HP}', '// ')
    _preparation_file = _preparation_file.replace('{OTHERS_HP}', '// ')

    zapisz("30_preparation.txt", _preparation_file, 'out')  

    _sensors_data = _sensors_data.replace('{SIGNALS}', _signals_szablon)

    # Przypisanie bajtów diagnostycznych
    _diag_szablon = '' 
    _licznik = 1
    for i in _adresyI:
            _szablon = _sensors3_data
            _szablon = _szablon.replace('{TYP}', 'in')
            _szablon = _szablon.replace('{NR}', str(_licznik))
            _szablon = _szablon.replace('{TAG}', 'I'+str(i))
            _licznik += 1
            _diag_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{DIAGIN}', _diag_szablon)

    _diag_szablon = ''
    _licznik = 1
    for i in _adresyQ:
            _szablon = _sensors3_data
            _szablon = _szablon.replace('{TYP}', 'out')
            _szablon = _szablon.replace('{NR}', str(_licznik))
            _szablon = _szablon.replace('{TAG}', 'Q'+str(i))
            _licznik += 1
            _diag_szablon += _szablon + '\n'
    _sensors_data = _sensors_data.replace('{DIAGOUT}', _diag_szablon)         

    zapisz("21_sensors_n.awl", _sensors_data, 'out')


def generuj_hp_messages(_valves, _sensory, _przyciski):
    _messages_data = otworz("A-HP_Messages.txt", 'templates')
    _message = otworz("A-HP_Messages_1.txt", 'templates')

    # VALVES 0
    _msg_szablon = ''
    for i in _valves:
        if i.msg_hp != 0:
            _szablon = _message
            _szablon = _szablon.replace('{NR}', str(i.msg_hp))
            _szablon = _szablon.replace('{TYP}', 'VALVES')
            _szablon = _szablon.replace('{TYP2}', 'err')
            _szablon = _szablon.replace('{BYTE}', str(i.byteHP))
            _szablon = _szablon.replace('{BIT}', str(i.bitHP))
            _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameHPcommentSmall[0:]} ({i.index}) jest nieaktywny')  
            _msg_szablon += _szablon + '\n'

        if i.msg_hp2 != 0:
            _szablon = _message
            _szablon = _szablon.replace('{NR}', str(i.msg_hp2))
            _szablon = _szablon.replace('{TYP}', 'VALVES')
            _szablon = _szablon.replace('{TYP2}', 'err')
            _szablon = _szablon.replace('{BYTE}', str(i.byteHP2))
            _szablon = _szablon.replace('{BIT}', str(i.bitHP2))
            _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameHP2commentSmall[0:]} ({i.index}) jest nieaktywny')  
            _msg_szablon += _szablon + '\n'

        if i.msg_wp != 0:
            _szablon = _message
            _szablon = _szablon.replace('{NR}', str(i.msg_wp))
            _szablon = _szablon.replace('{TYP}', 'VALVES')
            _szablon = _szablon.replace('{TYP2}', 'err')
            _szablon = _szablon.replace('{BYTE}', str(i.byteWP))
            _szablon = _szablon.replace('{BIT}', str(i.bitWP))
            _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameWPcommentSmall[0:]} ({i.index}) jest nieaktywny')  
            _msg_szablon += _szablon + '\n'

        if i.msg_wp2 != 0:
            _szablon = _message
            _szablon = _szablon.replace('{NR}', str(i.msg_wp2))
            _szablon = _szablon.replace('{TYP}', 'VALVES')
            _szablon = _szablon.replace('{TYP2}', 'err')
            _szablon = _szablon.replace('{BYTE}', str(i.byteWP2))
            _szablon = _szablon.replace('{BIT}', str(i.bitWP2))
            _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameWP2commentSmall[0:]} ({i.index}) jest nieaktywny')  
            _msg_szablon += _szablon + '\n'

    # SENSORS 1
    for i in _sensory:
        _szablon = _message
        _szablon = _szablon.replace('{NR}', str(i.msg_hp))
        _szablon = _szablon.replace('{TYP}', 'SENSORS')
        _szablon = _szablon.replace('{TYP2}', 'sen')
        _szablon = _szablon.replace('{BYTE}', str(i.byteHP))
        _szablon = _szablon.replace('{BIT}', str(i.bitHP))
        _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameComment} jest aktywny')        
        _msg_szablon += _szablon + '\n'
        _szablon = _message
        _szablon = _szablon.replace('{NR}', str(i.msg_wp))
        _szablon = _szablon.replace('{TYP}', 'SENSORS')
        _szablon = _szablon.replace('{TYP2}', 'sen')
        _szablon = _szablon.replace('{BYTE}', str(i.byteWP))
        _szablon = _szablon.replace('{BIT}', str(i.bitWP))
        _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameComment} jest nieaktywny')        
        _msg_szablon += _szablon + '\n'

    # SENSORS 3
    for i in _przyciski:
        _szablon = _message
        _szablon = _szablon.replace('{NR}', str(i.msg_hp))
        _szablon = _szablon.replace('{TYP}', 'BUTTONS')
        _szablon = _szablon.replace('{TYP2}', 'btn')
        _szablon = _szablon.replace('{BYTE}', str(i.byteHP))
        _szablon = _szablon.replace('{BIT}', str(i.bitHP))
        _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameComment} jest aktywny')        
        _msg_szablon += _szablon + '\n'
        _szablon = _message
        _szablon = _szablon.replace('{NR}', str(i.msg_wp))
        _szablon = _szablon.replace('{TYP}', 'BUTTONS')
        _szablon = _szablon.replace('{TYP2}', 'btn')
        _szablon = _szablon.replace('{BYTE}', str(i.byteWP))
        _szablon = _szablon.replace('{BIT}', str(i.bitWP))
        _szablon = _szablon.replace('{MESSAGE}', f'{i.get_sensorNameComment} jest nieaktywny')        
        _msg_szablon += _szablon + '\n'

    _messages_data = _messages_data.replace('{MSG}', _msg_szablon)
    zapisz("32_messages_n.awl", _messages_data, 'out')


def generuj_hmi_diag_msg(_adresyI, _adresyQ, _adresyIQ):
    _dictIQ = {}
    _txt = ''

    for i in _adresyIQ:
        _dictIQ[i[0]] = i[1]

    for i in _adresyI:
        for k in range(8):
            _tag = f'I{i}.{k}'
            if _tag in _dictIQ:
                _opis = _dictIQ[_tag]
            else:
                _opis = ''

            _txt += f'{_tag}: {_opis}\n'
        _txt += '\n'

    for i in _adresyQ:
        for k in range(8):
            _tag = f'Q{i}.{k}'
            if _tag in _dictIQ:
                _opis = _dictIQ[_tag]
            else:
                _opis = ''

            _txt += f'{_tag}: {_opis}\n'
        _txt += '\n'
    zapisz("33_hmi_diag_msg.txt", _txt, 'out')


def main(args):
    adresyI = []
    adresyQ = []
    adresyIQ = []

    df = pd.read_excel(args, header=0, sheet_name='Mechanizmy')
    df_datas_parsing(df)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    df_parsing(df)  # Sprawdzenie, czy kolumny zawierają prawidłowe I oraz Q
    df_check_duplicates(df)    # Sprawdzenie duplikatów adresów
    io = pd.read_excel(args, header=0, sheet_name='Sensory')
    io_datas_parsing(io)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    io_parsing(io)  # Sprawdzenie, czy kolumny zawierają prawidłowe I oraz Q
    io_check_duplicates(io)    # Sprawdzenie duplikatów adresów
    sft = pd.read_excel(args, header=0, sheet_name='Safety')
    io_datas_parsing(sft)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    io_parsing(sft)  # Sprawdzenie, czy kolumny zawierają prawidłowe I oraz Q
    io_check_duplicates(sft)    # Sprawdzenie duplikatów adresów
    btn = pd.read_excel(args, header=0, sheet_name='Przyciski')
    io_datas_parsing(btn)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    io_parsing(btn)  # Sprawdzenie, czy kolumny zawierają prawidłowe I oraz Q
    io_check_duplicates(btn)    # Sprawdzenie duplikatów adresów    
    iq = pd.read_excel(args, header=0, sheet_name='IQ')
    io_datas_parsing(iq)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    #TUTAJ DODAC PARSOWANIE DLA I oraz Q
    #CHECK powinno uwzględniać też prefix
    #io_check_duplicates(iq)    # Sprawdzenie duplikatów adresów
    drv = pd.read_excel(args, header=0, sheet_name='Drives')
    drv_datas_parsing(drv)
    drv_check_duplicates(drv)

    # Generowanie listy obiektów mechanizmow
    for index, row in df.iterrows():
        zawory.append(Zawor(index+1, row))

    # Generowanie listy obiektów sensorów
    for index, row in io.iterrows():
        sensory.append(Sensor(row, 'czujnik'))    
    for index, row in sft.iterrows():
        safety.append(Sensor(row, ''))   
    for index, row in btn.iterrows():
        przyciski.append(Sensor(row, 'przycisk')) 
    for index, row in iq.iterrows():
        inne.append(Sensor(row, ''))

    # Generowanie listy obiektów napędów
    for index, row in drv.iterrows():
        napedy.append(Drive(row))

    _preparation_file = otworz("30_preparation.txt", 'templates')
    zapisz("30_preparation.txt", _preparation_file, 'out') 

    generuj_tags_txt(zawory, sensory, safety, przyciski, inne)
    adresyI, adresyQ, adresyIQ = generuj_plc_tags_excel(zawory, sensory, safety, przyciski, inne)

    generuj_dbvalves_txt(df)
    generuj_dbvalves_db(df)

    generuj_hmialarms_class()

    licznik = generuj_hmialarms_excel(zawory, sensory, safety, przyciski)
    generuj_hmialarms_tagi_excel(lista_tagow)
    generuj_alarms_db(licznik, zawory, sensory, safety, przyciski, adresyI, adresyQ)

    #generuj_valves_outputs_scl(zawory)
    generuj_valves_outputs_stl(zawory)
    generuj_valves_instances(zawory)

    generuj_sensors(licznik, sensory, safety, przyciski, adresyI, adresyQ)
    generuj_hp_messages(zawory, sensory, przyciski) 
    generuj_hmi_diag_msg(adresyI, adresyQ, adresyIQ)   

    print('===== Koniec =====')
    return 0


if __name__ == '__main__':
    main('LK03.xlsx')
    # main(sys.argv)

