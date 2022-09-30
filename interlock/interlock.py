import pandas as pd
import sys


def otworz(_plik):
    try:
        with open(f'{_plik}', "r", encoding="utf-8-sig") as _f:
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


def df_prepare(_plik):
    _f = otworz(_plik)
    _new = _f.split('\n')
    _lista = []
    _index = 0
    _prefix = ''
    _namepl = ''
    _name = ''
    _typ = ''
    _tag = ''
    for _count, _i in enumerate(_new):
        if _i.find('TITLE = [') > -1:
            p = _i.split(' ')
            _index = int(p[2][1:-1])
            #_prefix = p[3]
            _namepl = p[4]
            if len(p) > 5:
                _typ = str(p[6]).lower()

        if _i.find('//[') > -1:
            p = _i.split(' ')
            _name = p[2]

        if _i.find('@') > -1:
            _nr = str(_i.split('@')[1])
            _tag = _i[0:_i.find('/')-len(_i)].strip().split(' ')
            _tag2 = _tag[1].split('.')
            _prefix = _tag2[1]
            _name = _tag2[2]
            _lista.append([_count, _tag[0], _tag[1], _index, _prefix, _namepl, _name, _typ, _nr])

    kolumny = ['linia', 'kod', 'tag', 'mechanizm', 'prefix', 'nazwapl', 'nazwaen', 'typ', 'nr']
    df = pd.DataFrame(_lista, columns=kolumny)
    gdf = (df.groupby(['mechanizm', 'typ']))

    return gdf


def generuj_awl(_ls, _plik):
    th = {
        'A': 'AN',
        'AN': 'A'
    }

    _outputs = otworz(_plik)
    _outputs_szablon = otworz("A-Outputs_valves_1_1.txt")

    _lista = []
    _temp = ['<No value>', '0', '<No value>', '0', 'INTERLOCK', 'True', 'none']
    _columns = ['Name', 'Alarm text [pl-PL], Alarm text', 'FieldInfo [Alarm text]', 'Class', 'Trigger tag', 'Trigger bit', 'Acknowledgement tag', 'Acknowledgement bit', 'PLC acknowledgement tag', 'PLC acknowledgement bit', 'Group', 'Report', 'Info text [pl-PL], Info text']
    
    grupy = _ls.groups
    for grupa in grupy:
        krotki = _ls.get_group(grupa)
        _txt = ''
        index = 0
        for count, i in (krotki.iterrows()):
            _valve_szablon = _outputs_szablon
            _valve_szablon = _valve_szablon.replace('{TYP}', i['typ'])
            _valve_szablon = _valve_szablon.replace('{NR}', str(index))
            _valve_szablon = _valve_szablon.replace('{INDEX}', str(i['mechanizm']))
            _valve_szablon = _valve_szablon.replace('{DBVALVE}', f'{i["prefix"]}.{i["nazwaen"]}')
            _valve_szablon = _valve_szablon.replace('{KOD}', th[i['kod']])
            _valve_szablon = _valve_szablon.replace('{TAG}', i['tag'])
            _txt += _valve_szablon 
            _lista.append([f'lock_{str(i["mechanizm"])}_{i["typ"]}_{str(index)}', f'[{i["nr"]}] {i["prefix"]} {i["nazwaen"]} ({str(i["mechanizm"])})', '', 'INTERLOCK', 'A-DBVALVES_io{'+str(i["mechanizm"])+'}_interlock_'+f'{i["typ"]}', f'{str(index)}'] + _temp)
            
            index += 1
        _tmp = '//{INTERLOCK_'+i['typ'].upper()+str(i['mechanizm'])+'}'
        _outputs = _outputs.replace(_tmp, _txt)
    
    _df = pd.DataFrame(_lista, columns=_columns)
    _df.index.name = 'ID'
    _df.index += 1000
    try:
        _df.to_excel("40_HMIInterlock.xlsx", sheet_name='DiscreteAlarms', index=True)
        print(f'[OK] Wygenerowano HMIInterlock.xlsx')
        return _lista
    except IOError as e:
        print(f'[NOK] Nie wygenerowano HMIInterlock.xlsx')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano HMIInterlock.xlsx')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def generuj_hmialarms_tagi_excel(_lista):
    _lista_gotowa = []
    _tmp = ['UInt', '2', 'Binary', 'Symbolic access', '<No Value>', 'False', '<No Value>', '<No Value>', '0', '<No Value>', '<No Value>', 'Continuous', '1 s', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'None', '<No Value>', 'False', '10', '0', '100', '0', 'False', 'None', 'False']
    _columns = ['Name', 'Path', 'Connection', 'PLC tag', 'DataType', 'Length', 'Coding', 'Access Method', 'Address', 'Indirect addressing', 'Index tag', 'Start value', 'ID tag', 'Display name [pl-PL]', 'Comment [pl-PL]', 'Acquisition mode', 'Acquisition cycle', 'Limit Upper 2 Type', 'Limit Upper 2', 'Limit Upper 1 Type', 'Limit Upper 1', 'Limit Lower 1 Type', 'Limit Lower 1', 'Limit Lower 2 Type', 'Limit Lower 2', 'Linear scaling', 'End value PLC', 'Start value PLC', 'End value HMI', 'Start value HMI', 'Gmp relevant', 'Confirmation Type', 'Mandatory Commenting']
    for i in (_lista):   
        _t = i[0].split('_')
        _lista_gotowa.append([f'{i[4]}', 'Default tag table', 'PLC', f'"A-DBVALVES".io[{_t[1]}].interlock_{_t[2]}'] + _tmp)
    _df = pd.DataFrame(_lista_gotowa, columns=_columns)
    try:
        _df.to_excel("41_HMIInterlockTags.xlsx", sheet_name='Hmi Tags', index=False)
        print(f'[OK] Wygenerowano HMIInterlockTags.xlsx')
    except IOError as e:
        print(f'[NOK] Nie wygenerowano HMIInterlockTags.xlsx')
        print(f'I/O error({e.errno}): {e.strerror}')
        return e
    except:  # handle other exceptions such as attribute errors
        print(f'[NOK] Nie wygenerowano HMIInterlockTags.xlsx')
        print('Unexpected error:', sys.exc_info()[0])
        return None


def main(args):
    ls = df_prepare('A-Outputs_valves.awl')
    lista = generuj_awl(ls, 'A-Outputs_valves.awl')
    generuj_hmialarms_tagi_excel(lista)

if __name__ == '__main__':
    #main()
    main(sys.argv)        