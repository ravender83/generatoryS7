import pandas as pd
from tag import Zawor
import sys

zawory = []


def zapisz(_plik, _txt):
    try:
        with open(f'out/{_plik}', "w", encoding="utf-8") as _f:
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


def otworz(_plik):
    try:
        with open(f'templates/{_plik}', "r", encoding="utf-8") as _f:
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


def datas_parsing(_df):
    # Zmiana nazw na male litery. Sprawdzenie braku duplikatów
    _df.PREFIX = _df.PREFIX.dropna().astype(str).str.upper()
    _df.PREFIX = _df.PREFIX.dropna().astype(str).str.strip()
    _df.NAME = _df.NAME.dropna().astype(str).str.lower()
    _df.NAME = _df.NAME.dropna().astype(str).str.strip()
    _df.NAMEPL = _df.NAMEPL.dropna().astype(str).str.lower()
    _df.NAMEPL = _df.NAMEPL.dropna().astype(str).str.strip()
    _df.SIDE_HP = _df.SIDE_HP.dropna().astype(str).str.strip()
    _df.SIDE_HP = _df.SIDE_HP.dropna().astype(str).str.lower().str[0]
    _df.SIDE_WP = _df.SIDE_WP.dropna().astype(str).str.strip()
    _df.SIDE_WP = _df.SIDE_WP.dropna().astype(str).str.lower().str[0]
    _df.SENSOR_HP = _df.SENSOR_HP.dropna().astype(str).str.strip()
    _df.SENSOR_HP = _df.SENSOR_HP.dropna().astype(str).str.upper()
    _df.SENSOR_HP2 = _df.SENSOR_HP2.dropna().astype(str).str.strip()
    _df.SENSOR_HP2 = _df.SENSOR_HP2.dropna().astype(str).str.upper()
    _df.SENSOR_WP = _df.SENSOR_WP.dropna().astype(str).str.strip()
    _df.SENSOR_WP = _df.SENSOR_WP.dropna().astype(str).str.upper()
    _df.SENSOR_WP2 = _df.SENSOR_WP2.dropna().astype(str).str.strip()
    _df.SENSOR_WP2 = _df.SENSOR_WP2.dropna().astype(str).str.upper()
    _df.OUTPUT_HP = _df.OUTPUT_HP.dropna().astype(str).str.strip()
    _df.OUTPUT_HP = _df.OUTPUT_HP.dropna().astype(str).str.upper()
    _df.OUTPUT_WP = _df.OUTPUT_WP.dropna().astype(str).str.strip()
    _df.OUTPUT_WP = _df.OUTPUT_WP.dropna().astype(str).str.upper()
    _df.IDLE = _df.IDLE.dropna().astype(str).str.strip()
    _df.IDLE = _df.IDLE.dropna().astype(str).str.upper()
    _df.BRAKE_RELEASE = _df.BRAKE_RELEASE.dropna().astype(str).str.strip()
    _df.BRAKE_RELEASE = _df.BRAKE_RELEASE.dropna().astype(str).str.upper()
    print('[OK] Parsowanie tekstu')


def io_parsing(_df):
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


def check_duplicates(_df):
    if _df.NAME.is_unique:
        print('[OK] Nazwy NAME są unikalne')
    else:
        print('[NOK] Nazwy NAME nie są unikalne')
        print(_df[_df.duplicated(subset=['NAME'], keep=False)].NAME)
        input('Press enter to exit...')
        exit()

    if _df.NAMEPL.is_unique:
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


def generuj_tags_txt(_zawory):
    _txt = '----------- VALVES -----------\n'
    for i in _zawory:
        _txt = _txt + f'{i.get_name}\n'
    _txt = _txt + '\n----------- ZAWORY -----------\n'
    for i in _zawory:
        _txt = _txt + f'{i.get_namepl}\n'

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

        _txt = _txt + f'{_ihp}\n'
        if i.sensorHP2 != '%nan':
            _txt = _txt + f'{_ihp2}\n'
        _txt = _txt + f'{_iwp}\n'
        if i.sensorWP2 != '%nan':
            _txt = _txt + f'{_iwp2}\n'
        _txt = _txt + f'{_ohp}\n'
        _txt = _txt + f'{_owp}\n'
        if i.outputIDLE != '%nan':
            _txt = _txt + f'{_oidle}\n'
        if i.outputBRAKE != '%nan':
            _txt = _txt + f'{_obrake}\n'
    zapisz("1_tags.txt", _txt)


def generuj_dbvalves_txt(_df):
    _txt = '----------- DBVALVES datablock structs-----------\n'
    _tmp = '\tStruct\t\tFalse\tTrue\tTrue\tTrue\tFalse\t\t'
    _prefixy = sorted(set(_df.PREFIX))
    for i in _prefixy:
        _txt = _txt + f'{i}{_tmp}\n'

    for i in _prefixy:
        _pre = _df.loc[_df.PREFIX == i]
        _txt = _txt + f'\n--- {i} ---\n'
        _tmp = '\t"3state"\t\tFalse\tTrue\tTrue\tTrue\tFalse\t\t'
        for index, row in _pre.iterrows():
            _txt = _txt + f'{row.NAME.upper()}{_tmp}[{index+1}] {row.PREFIX}-{row.NAMEPL}\n'
    zapisz("2_dbvalves.txt", _txt)


def szablon_nan(aktualny_szablon, co, na_co, alternatywa, procent):
    if procent:
        _nan = '%nan'
    else:
        _nan = 'nan'
    if na_co == _nan:
        aktualny_szablon = aktualny_szablon.replace(co, alternatywa)
    else:
        aktualny_szablon = aktualny_szablon.replace(co, na_co)
    return aktualny_szablon


def generuj_valves_outputs_scl(_zawory):
    _valves_data = otworz("VALVES_outputs.txt")
    _members_data = otworz("VALVES_outputs_interior.txt")

    _members_szablon = ''
    for i in _zawory:
        _szablon = _members_data
        _szablon = _szablon.replace('{DBVALVE_TITLE}', f'{i.prefix} {i.name.upper()}')
        _szablon = _szablon.replace('{DBVALVE}', f'{i.prefix}.{i.name.upper()}')
        _szablon = _szablon.replace('{INDEX}', f'{i.index}')
        _szablon = szablon_nan(_szablon, '{in_sensor_hp}', i.sensorHP, 'I1000.0', True)
        _szablon = szablon_nan(_szablon, '{in_sensor_hp2}', i.sensorHP2, i.sensorHP, True)
        _szablon = szablon_nan(_szablon, '{in_sensor_wp}', i.sensorWP, 'I1000.0', True)
        _szablon = szablon_nan(_szablon, '{in_sensor_wp2}', i.sensorWP2, i.sensorWP, True)
        _szablon = szablon_nan(_szablon, '{in_ez_hp}', i.outputHP, f'"DBVALVES".{i.prefix}.{i.name.upper()}.test.HP_DUMMY', True)
        _szablon = szablon_nan(_szablon, '{in_ez_wp}', i.outputWP, f'"DBVALVES".{i.prefix}.{i.name.upper()}.test.WP_DUMMY', True)
        _szablon = szablon_nan(_szablon, '{in_ez_idle}', i.outputIDLE, f'"DBVALVES".{i.prefix}.{i.name.upper()}.test.IDLE_DUMMY', True)
        _szablon = szablon_nan(_szablon, '{in_Ipw1}', i.sensorHP[1:], ' ', False)
        _szablon = szablon_nan(_szablon, '{in_Ipw2}', i.sensorHP2[1:], ' ', False)
        _szablon = szablon_nan(_szablon, '{in_Ipr1}', i.sensorWP[1:], ' ', False)
        _szablon = szablon_nan(_szablon, '{in_Ipr2}', i.sensorWP2[1:], ' ', False)
        _szablon = szablon_nan(_szablon, '{in_Qpw}', i.outputHP[1:], ' ', False)
        _szablon = szablon_nan(_szablon, '{in_Qpr}', i.outputWP[1:], ' ', False)
        _members_szablon += _szablon

    _valves_data = _valves_data.replace('{VALVES}', _members_szablon)
    zapisz("3_dbvalve_outputs.scl", _valves_data)


def main(args):
    df = pd.read_excel(args, header=0)
    datas_parsing(df)   # Zmiana tekstu na małe/duże litery, usuwanie białych spacji
    io_parsing(df)  # Sprawdzenie, czy kolumny zawierają prawidłowe I oraz Q
    check_duplicates(df)    # Sprawdzenie duplikatów adresów

    # Generowanie listy obiektów mechanizmow
    for index, row in df.iterrows():
        zawory.append(Zawor(index+1, row))

    generuj_tags_txt(zawory)
    generuj_dbvalves_txt(df)

    generuj_valves_outputs_scl(zawory)

    print('===== Koniec =====')
    return 0


if __name__ == '__main__':
    main('PZ03.xlsx')
    # main(sys.argv)

