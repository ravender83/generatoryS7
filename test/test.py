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
            _prefix = p[3]
            _namepl = p[4]
            if len(p) > 5:
                _typ = str(p[6]).lower()
        if _i.find('//[') > -1:
            p = _i.split(' ')
            _name = p[2]

        if _i.find('@i') > -1:
            _tag = _i[0:_i.find('/')-len(_i)].strip().split(' ')

            _lista.append([_count, _tag[0], _tag[1], _index, _prefix, _namepl, _name, _typ])

    kolumny = ['linia', 'kod', 'tag', 'mechanizm', 'prefix', 'nazwapl', 'nazwaen', 'typ']
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
            _txt += _valve_szablon + '\n'
            index += 1
        print(_txt)
    '''
    for i in _ls:
        _mech = list(filter(lambda score: score[3] == i, _ls))
        print(_mech)
        _txt = ''
        for count, k in enumerate(_mech):
            _valve_szablon = _outputs_szablon
            _valve_szablon = _valve_szablon.replace('{TYP}', k[6])
            _valve_szablon = _valve_szablon.replace('{NR}', str(count))
            _valve_szablon = _valve_szablon.replace('{INDEX}', str(k[3]))
            _tmp = k[2].split('.')
            _valve_szablon = _valve_szablon.replace('{DBVALVE}}', f'{_tmp[1]}.{_tmp[2]}')

    #print(_dbvalves_data)

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
    zapisz("11_DBVALVES.db", _dbvalves_data, 'out')
'''


def main(args):
    ls = df_prepare('A-Outputs_valves.awl')
    generuj_awl(ls, 'A-Outputs_valves.awl')


'''
    nr_new = 0
    nr_old = 0
    _txt = ''
    for i in lista:
        nr_new = i[2]
        if nr_new != nr_old:
            nr_old = nr_new
            
'''

if __name__ == '__main__':
    #main()
    main(sys.argv)        