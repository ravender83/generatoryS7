from files import otworz
from zmien import string_na_clean_list
from tag import Zawor

# parametry
valve_start = 10
inst_block = 900
# ----

kierunek = {'l': 'left', 'r': 'right', 'u': 'up', 'd': 'down', 'f': 'front', 'b': 'back', 'o': 'open', 'c': 'close'}
typ = {'I': 'VSEN', 'Q': 'VALVE'}
zawory = []

def checkDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def pwrite(txt):
    print (txt)
    f.write(f'{txt}\n')
    
allparts = string_na_clean_list(otworz('mech.csv'))
parts_list = [i for i in allparts if i[0] == '#']
allparts.clear()
parts = []

for i in parts_list:
    parts.append(i.split(','))
parts_list.clear()

l_nazwy = []
l_tagi = []

for i in parts:
    l_nazwy.append(i[2].lower())

for i in parts:
    l_tagi.append(i[3].upper())
    l_tagi.append(i[4].upper())
    l_tagi.append(i[5].upper())
    l_tagi.append(i[6].upper())
    if len(i)==10:
        l_tagi.append(i[9].upper())

if checkDuplicates(l_nazwy):
    print('Duplikaty w nazwach')
else:
    print('Brak duplikatow nazw')
          
if checkDuplicates(l_tagi):
    print('Duplikaty w tagach')
else:
    print('Brak duplikatow tagow')

for i in parts:
    print(i)
print()

l_nazwy.clear()
l_tagi.clear()

for i in range(0,len(parts)):
    zawory.append(Zawor(parts[i][1], parts[i][2], parts[i][3], parts[i][4], parts[i][5], parts[i][6], kierunek[parts[i][7][0].lower()], kierunek[parts[i][8][0].lower()], parts[i][9]))

f = open("out/tags.txt", "w")

msg = '----------- TAGS -----------'
pwrite(msg)
tags = []
for i in range(0,len(zawory)):   
    
    tmp = '\tFalse\tTrue\tTrue\tTrue\t'
    i_HP = f'{zawory[i].rsenNameHP(1)}\tBOOL\t{zawory[i].sensorHP}{tmp}\t#nc - {zawory[i].rsenNameHP(1)}' #sensor HP
    i_WP = f'{zawory[i].rsenNameWP(1)}\tBOOL\t{zawory[i].sensorWP}{tmp}\t#no - {zawory[i].rsenNameWP(1)}' #sensor WP
    o_HP = f'{zawory[i].rvalveNameHP(1)}\tBOOL\t{zawory[i].valveHP}{tmp}\t[{i+1}] {zawory[i].rvalveNameHP(1)} [{zawory[i].sensorHP}]' #ez HP
    o_WP = f'{zawory[i].rvalveNameWP(1)}\tBOOL\t{zawory[i].valveWP}{tmp}\t[{i+1}] {zawory[i].rvalveNameWP(1)} [{zawory[i].sensorWP}]' #ez WP

    pwrite(i_HP)
    tags.append([zawory[i].rsenNameHP(1), zawory[i].sensorHP, f'#nc - {zawory[i].rsenNameHP(1)}'])
    pwrite(i_WP)
    tags.append([zawory[i].rsenNameWP(1), zawory[i].sensorWP, f'#nc - {zawory[i].rsenNameWP(1)}'])
    pwrite(o_HP)
    tags.append([zawory[i].rvalveNameHP(1), zawory[i].valveHP, f'[{i+1}] {zawory[i].rvalveNameHP(1)} [{zawory[i].sensorHP}]'])
    pwrite(o_WP)
    tags.append([zawory[i].rvalveNameWP(1), zawory[i].valveWP, f'[{i+1}] {zawory[i].rvalveNameWP(1)} [{zawory[i].sensorWP}]'])

    if zawory[i].idle != 'NONE':
        idle = f'{zawory[i].rvalveNameIDLE(1)}\tBOOL\t{zawory[i].idle}{tmp}\t[{i+1}] {zawory[i].rvalveNameIDLE(1)}' #IDLE
        pwrite(idle)
        tags.append([zawory[i].rvalveNameIDLE(1), zawory[i].idle, f'[{i+1}] {zawory[i].rvalveNameIDLE(1)}'])
           
pwrite('')
msg = '----------- VALVES -----------'
pwrite(msg)

for i in range(0,len(zawory)):
    valve = f'[{i+1}] {zawory[i].rname}'
    pwrite(valve)
pwrite('')

f.close()


# ==================  Edycja szablonu DB FLAGI =============================
dbvalves = open("xml/db_valves_tmp.xml", "r", encoding="utf-8")
dbvalves_data = dbvalves.read()
print('Wczytano szablon imp_valves_tmp.xml')
dbvalves.close()

dbmembers = open("xml/db_member_tmp.xml", "r", encoding="utf-8")
dbmembers_data = dbmembers.read()
print('Wczytano szablon members_tmp.xml')
dbmembers.close()

dbmembers_szablon = ''
for i in range(0, len(zawory)):
    szablon = dbmembers_data
    szablon = szablon
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    szablon = szablon.replace("{NRNAME}", f'[{i+1}] {zawory[i].rname}')
    szablon += '\n\n'
    dbmembers_szablon += szablon

dbvalves_data = dbvalves_data.replace("{MEMBERS}", dbmembers_szablon)

print('Wygenerowano imp_valves.xml')
f = open("out/db_valves.xml", "w", encoding="utf-8")
f.write(dbvalves_data)
f.close()

# ==================  Edycja szablonu IO TAGI =============================
iotags = open("xml/io_tags_tmp.xml", "r", encoding="utf-8")
iotags_data = iotags.read()
print('Wczytano szablon io_tags_tmp.xml')
iotags.close()

iotag = open("xml/io_tag_tmp.xml", "r", encoding="utf-8")
iotag_data = iotag.read()
print('Wczytano szablon io_tag_tmp.xml')
iotag.close()

iotags_szablon = ''
k = 1
for i in enumerate(tags):
    szablon = iotag_data
    szablon = szablon.replace("{NAME}", i[1][0])
    szablon = szablon.replace("{ADDRESS}", i[1][1])
    szablon = szablon.replace("{COMMENT}", i[1][2])
    szablon = szablon.replace("{NR1}", str(k))
    szablon = szablon.replace("{NR2}", str(k+1))
    szablon = szablon.replace("{NR3}", str(k+2))
    szablon = szablon.replace("{NR4}", str(k+3))
    k += 4
    szablon += '\n\n'
    iotags_szablon += szablon

iotags_data = iotags_data.replace("{TAGS}", iotags_szablon)

print('Wygenerowano io_tags.xml')
f = open("out/io_tags.xml", "w", encoding="utf-8")
f.write(iotags_data)
f.close()

# ==================  Edycja szablonu OUTPUTS =============================
outputs = open("xml/func_outputs_tmp.xml", "r", encoding="utf-8")
outputs_data = outputs.read()
print('Wczytano szablon func_outputs_tmp.xml')
outputs.close()

header = open("xml/output_header_tmp.xml", "r", encoding="utf-8")
header_data = header.read()
print('Wczytano szablon output_header_tmp.xml')
header.close()

commHP = open("xml/output_HP_tmp.xml", "r", encoding="utf-8")
commHP_data = commHP.read()
print('Wczytano szablon output_HP_tmp.xml')
commHP.close()

commWP = open("xml/output_WP_tmp.xml", "r", encoding="utf-8")
commWP_data = commWP.read()
print('Wczytano szablon output_WP_tmp.xml')
commWP.close()

commYESIDLE = open("xml/output_YESIDLE_tmp.xml", "r", encoding="utf-8")
commYESIDLE_data = commYESIDLE.read()
print('Wczytano szablon output_YESIDLE_tmp.xml')
commYESIDLE.close()

commNOIDLE = open("xml/output_NOIDLE_tmp.xml", "r", encoding="utf-8")
commNOIDLE_data = commNOIDLE.read()
print('Wczytano szablon output_NOIDLE_tmp.xml')
commNOIDLE.close()

valve = open("xml/output_VALVE_tmp.xml", "r", encoding="utf-8")
valve_data = valve.read()
print('Wczytano szablon output_VALVE_tmp.xml')
valve.close()

valvetag = open("xml/output_VALVE_tag_tmp.xml", "r", encoding="utf-8")
valvetag_data = valvetag.read()
print('Wczytano szablon output_VALVE_tag_tmp.xml')
valvetag.close()

valvedbtag = open("xml/output_VALVE_dbtag_tmp.xml", "r", encoding="utf-8")
valvedbtag_data = valvedbtag.read()
print('Wczytano szablon output_VALVE_dbtag_tmp.xml')
valvedbtag.close()

test = open("xml/output_TEST_tmp.xml", "r", encoding="utf-8")
test_data = test.read()
print('Wczytano szablon output_TEST_tmp.xml')
test.close()

comm_szablon = ''
valves_szablon = ''
tests_szablon = ''
# ------------------------- triggery -----------------------------
for i in range(0,len(zawory)):
    # naglowek
    szablon = header_data
    szablon = szablon.replace("{NAME}", zawory[i].name)
    szablon = szablon.replace("{NRNAME}", f'[{i+1}] {zawory[i].rname}')
    szablon += '\n\n'
    
    comm_szablon += szablon

    # command HP
    szablon = commHP_data
    szablon = szablon.replace("{VALVENR}", str(valve_start)) #10
    szablon = szablon.replace("{NRNAME}", zawory[i].rsenNameHP(0)) #[1] NAZWA HP LEFT
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    valve_start += 1
    szablon += '\n\n'
    comm_szablon += szablon

    # command WP
    szablon = commWP_data
    szablon = szablon.replace("{VALVENR}", str(valve_start)) #10
    szablon = szablon.replace("{NRNAME}", zawory[i].rsenNameWP(0)) #[1] NAZWA WP RIGHT
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    valve_start += 1
    szablon += '\n\n'
    comm_szablon += szablon

    # command IDLE
    if zawory[i].idle == 'NONE':
        szablon = commNOIDLE_data
        szablon = szablon.replace("{NRNAME}", f'{zawory[i].name} IDLE') #NAZWA IDLE
        szablon = szablon.replace("{NAME}", zawory[i].rname)
    else:
        szablon = commYESIDLE_data
        szablon = szablon.replace("{NRNAME}", zawory[i].rvalveNameIDLE(0)) #[1] NAZWA IDLE
        szablon = szablon.replace("{VALVENR}", str(valve_start)) #10
        szablon = szablon.replace("{NAME}", zawory[i].rname)
        valve_start += 1
            
    szablon += '\n\n'
    comm_szablon += szablon

blocknr = inst_block
# ------------------------- funkcje -----------------------------
for i in range(0,len(zawory)):
    # valve
    szablon = valve_data
    szablon = szablon.replace("{NRNAME}", f'[{i+1}] {zawory[i].rname}') #[1] NAZWA HP LEFT
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    szablon = szablon.replace("{BLOCKNR}", str(blocknr))
    szablon = szablon.replace("{SENSORHP}", zawory[i].rsenNameHP(1))
    szablon = szablon.replace("{SENSORWP}", zawory[i].rsenNameWP(1))
    szablon = szablon.replace("{VALVEHP}", zawory[i].rvalveNameHP(1))
    szablon = szablon.replace("{VALVEWP}", zawory[i].rvalveNameWP(1))

    if zawory[i].idle == 'NONE':
        szablon = szablon.replace("{SYMBOLIDLE}", valvedbtag_data) 
        szablon = szablon.replace("{ADDRESS}", zawory[i].rname)
    else:
        szablon = szablon.replace("{SYMBOLIDLE}", valvetag_data)
        szablon = szablon.replace("{ADDRESS}", zawory[i].rvalveNameIDLE(1))                       

    blocknr += 1
    szablon += '\n\n'
    valves_szablon += szablon

# ------------------------- testy  -----------------------------
for i in range(0,len(zawory)):
    # valve
    szablon = test_data
    szablon = szablon.replace("{NRNAME}", f'[{i+1}] {zawory[i].rname}') #[1] NAZWA HP LEFT
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    szablon = szablon.replace("{NR}", str(i+1))

    szablon += '\n\n'
    tests_szablon += szablon    
    
outputs_data = outputs_data.replace("{COMMAND}", comm_szablon)
outputs_data = outputs_data.replace("{VALVES}", valves_szablon)
outputs_data = outputs_data.replace("{TESTS}", tests_szablon)

# ====== Generowanie numerów ID ======
k = 4
while '{ID}' in outputs_data:
    outputs_data = outputs_data.replace("{ID}", str(k), 1)
    k += 1    

print('Wygenerowano func_outputs.xml')
f = open("out/func_outputs.xml", "w", encoding="utf-8")
f.write(outputs_data)
f.close()

# ===================== BLOKI INSTANCYJNE ======================
instance = open("xml/output_instance_tmp.xml", "r", encoding="utf-8")
instance_data = instance.read()
print('Wczytano szablon output_instance_tmp.xml')
instance.close()

instance_block = open("xml/output_instance_block_tmp.xml", "r", encoding="utf-8")
instance_block_data = instance_block.read()
print('Wczytano szablon output_instance_block_tmp.xml')
instance_block.close()

instance_block_szablon = ''
blocknr = inst_block
# ------------------------- triggery -----------------------------
for i in range(0,len(zawory)):
    # bloki instancyjne
    szablon = instance_block_data
    szablon = szablon.replace("{NAME}", zawory[i].rname)
    szablon = szablon.replace("{BLOCKNR}", str(blocknr))
    szablon += '\n\n'
    blocknr += 1
    instance_block_szablon += szablon

instance_data = instance_data.replace("{BLOCKS}", instance_block_szablon)    

# ====== Generowanie numerów ID ======
k = 0
while '{ID}' in instance_data:
    instance_data = instance_data.replace("{ID}", str(k), 1)
    k += 1    

print('Wygenerowano func_instances.xml')
f = open("out/func_instances.xml", "w", encoding="utf-8")
f.write(instance_data)
f.close()














