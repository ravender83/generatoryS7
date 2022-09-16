class Zawor:
    def __init__(self, _index, _zawor):
        kierunek = {'l': 'left', 'r': 'right', 'u': 'up', 'd': 'down', 'f': 'front', 'b': 'back', 'o': 'open',
                    'c': 'close'}

        self.index = _index
        self.prefix = str(_zawor.PREFIX)
        self.name = str(_zawor.NAME)
        self.namepl = str(_zawor.NAMEPL)
        self.byteHP = 0
        self.bitHP = 0
        self.byteHP2 = 0
        self.bitHP2 = 0        
        self.byteWP = 0
        self.bitWP = 0  
        self.byteWP2 = 0
        self.bitWP2 = 0 
        self.msg_hp = 0
        self.msg_hp2 = 0
        self.msg_wp = 0
        self.msg_wp2 = 0

        if str(_zawor.SENSOR_HP) != 'nan':
            self.sensorHP = '%'+str(_zawor.SENSOR_HP)
        else:
            self.sensorHP = 'nan'

        if str(_zawor.SENSOR_HP2) != 'nan':
            self.sensorHP2 = '%'+str(_zawor.SENSOR_HP2)
        else:
            self.sensorHP2 = self.sensorHP

        if str(_zawor.SENSOR_WP) != 'nan':
            self.sensorWP = '%'+str(_zawor.SENSOR_WP)
        else:
            self.sensorWP = 'nan'

        if str(_zawor.SENSOR_WP2) != 'nan':
            self.sensorWP2 = '%'+str(_zawor.SENSOR_WP2)
        else:
            self.sensorWP2 = self.sensorWP

        if str(_zawor.OUTPUT_HP) != 'nan':
            self.outputHP = '%'+str(_zawor.OUTPUT_HP)
        else:
            self.outputHP = 'nan'

        if str(_zawor.OUTPUT_WP) != 'nan':
            self.outputWP = '%'+str(_zawor.OUTPUT_WP)
        else:
            self.outputWP = 'nan'

        if str(_zawor.IDLE) != 'nan':
            self.outputIDLE = '%'+str(_zawor.IDLE)
        else:
            self.outputIDLE = 'nan'

        if str(_zawor.BRAKE_RELEASE) != 'nan':
            self.outputBRAKE = '%'+str(_zawor.BRAKE_RELEASE)
        else:
            self.outputBRAKE = 'nan'

        self.sideHP = kierunek[_zawor.SIDE_HP]
        self.sideWP = kierunek[_zawor.SIDE_WP]


    @property
    def get_name(self):
        # [9] ST1 TAU_HOLDFAST_MOVEMENT
        return f'[{self.index}] {self.prefix} {self.name.replace("_", " ")}'.upper()


    @property
    def get_namepl(self):
        # [9] ST1 PRZESUW_DOCISKU_TAU
        return f'[{self.index}] {self.prefix} {self.namepl.replace("_", " ")}'.upper()

    # ----- Nazwy tagów -----

    @property
    def get_sensorNameHP(self):
        # BR-vsen_imitation_HP_front
        return f'{self.prefix}-vsen_{self.name}_HP_{self.sideHP}'


    @property
    def get_sensorNameHP2(self):
        # BR-vsen_imitation_HP_front
        return f'{self.prefix}-vsen_{self.name}_HP2_{self.sideHP}'


    @property
    def get_sensorNameWP(self):
        # BR-vsen_imitation_WP_front
        return f'{self.prefix}-vsen_{self.name}_WP_{self.sideWP}'


    @property
    def get_sensorNameWP2(self):
        # BR-vsen_imitation_HP_front
        return f'{self.prefix}-vsen_{self.name}_WP2_{self.sideWP}'


    @property
    def get_outputNameHP(self):
        # BR-ez_imitation_HP_front
        return f'{self.prefix}-ez_{self.name}_HP_{self.sideHP}'


    @property
    def get_outputNameWP(self):
        # BR-ez_imitation_WP_front
        return f'{self.prefix}-ez_{self.name}_WP_{self.sideWP}'


    @property
    def get_outputNameIDLE(self):
        # BR-ez_imitation_IDLE
        return f'{self.prefix}-ez_{self.name}_IDLE'


    @property
    def get_outputNameBRAKE(self):
        # BR-ez_imitation_BRAKE_RELEASE
        return f'{self.prefix}-ez_{self.name}_BRAKE_RELEASE'

    # ----- Komentarze tagów -----


    @property
    def get_sensorNameHPcomment(self):
        #nc - [I20.5] czujnik BR IMITACJA HP front
        #return f'#nc - [{self.sensorHP[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'
        return f'[{self.sensorHP[1:]}] czujnik "{self.prefix}-{self.namepl}" HP {self.sideHP}'


    @property
    def get_sensorNameHP2comment(self):
        #nc - [I20.5] czujnik BR IMITACJA HP front
        #return f'#nc - [{self.sensorHP2[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'
        return f'[{self.sensorHP2[1:]}] czujnik "{self.prefix}-{self.namepl}" HP {self.sideHP}'


    @property
    def get_sensorNameWPcomment(self):
        #nc - [I20.5] czujnik BR IMITACJA WP front
        #return f'#no - [{self.sensorWP[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'
        return f'[{self.sensorWP[1:]}] czujnik "{self.prefix}-{self.namepl}" WP {self.sideWP}'


    @property
    def get_sensorNameWP2comment(self):
        #nc - [I20.5] czujnik BR IMITACJA WP front
        #return f'#no - [{self.sensorWP2[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'
        return f'[{self.sensorWP2[1:]}] czujnik "{self.prefix}-{self.namepl}" WP {self.sideWP}'

    @property
    def get_sensorNameHPcommentSmall(self):
        #nc - [I20.5] czujnik BR IMITACJA HP
        #return f'#nc - [{self.sensorHP[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'
        return f'[{self.sensorHP[1:]}] czujnik "{self.prefix}-{self.namepl}" HP'


    @property
    def get_sensorNameHP2commentSmall(self):
        #nc - [I20.5] czujnik BR IMITACJA HP
        #return f'#nc - [{self.sensorHP2[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'
        return f'[{self.sensorHP2[1:]}] czujnik "{self.prefix}-{self.namepl}" HP'


    @property
    def get_sensorNameWPcommentSmall(self):
        #nc - [I20.5] czujnik BR IMITACJA WP
        #return f'#no - [{self.sensorWP[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'
        return f'[{self.sensorWP[1:]}] czujnik "{self.prefix}-{self.namepl}" WP'


    @property
    def get_sensorNameWP2commentSmall(self):
        #nc - [I20.5] czujnik BR IMITACJA WP
        #return f'#no - [{self.sensorWP2[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'
        return f'[{self.sensorWP2[1:]}] czujnik "{self.prefix}-{self.namepl}" WP'

    @property
    def get_outputNameHPcomment(self):
        # [1] BR-imitation HP FRONT [I20.5]
        if self.sensorHP2 != 'nan' and self.sensorHP2 != self.sensorHP:
            _tmp = f', {self.sensorHP2[1:]}'
        else:
            _tmp = ''
        return f'[{self.index}] {self.prefix}-{self.namepl} HP {self.sideHP} [{self.sensorHP[1:]}{_tmp}]'


    @property
    def get_outputNameWPcomment(self):
        # [1] BR-imitation WP FRONT [I20.5]
        if self.sensorWP2 != 'nan' and self.sensorWP2 != self.sensorWP:
            _tmp = f', {self.sensorWP2[1:]}'
        else:
            _tmp = ''
        return f'[{self.index}] {self.prefix}-{self.namepl} WP {self.sideWP} [{self.sensorWP[1:]}{_tmp}]'


    @property
    def get_outputNameIDLEcomment(self):
        # [1] BR-imitation IDLE
        return f'[{self.index}] {self.prefix}-{self.namepl} IDLE'


    @property
    def get_outputNameBRAKEcomment(self):
        # [1] BR-imitation IDLE
        return f'[{self.index}] {self.prefix}-{self.namepl} BRAKE RELEASE'
