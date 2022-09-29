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


def myFunc(x):
    if x.find('@i') > -1:
        return True
    else:
        return False


def main(args):
    lista = []
    f = otworz('A-Outputs_valves.awl')

    new = f.split('\n')
    index = 0
    prefix = ''
    namepl = ''
    typ = ''

    for count, i in enumerate(new):        
        if (i.find('TITLE = [') > -1):
            p = i.split(' ')
            index = int(p[2][1:-1])
            prefix = str(p[3])
            namepl = str(p[4])
            if len(p) > 5:
                typ = str(p[6]).lower()

        if (i.find('@i') > -1):            
            lista.append([count+1, i.strip(), index, prefix, namepl, typ])

    for i in lista:
        print(i)


if __name__ == '__main__':
    #main()
    main(sys.argv)        