class Zawor:
    def __init__(self, _index, _zawor):
        kierunek = {'l': 'left', 'r': 'right', 'u': 'up', 'd': 'down', 'f': 'front', 'b': 'back', 'o': 'open',
                    'c': 'close'}

        self.index = _index
        self.prefix = str(_zawor.PREFIX)
        self.name = str(_zawor.NAME)
        self.namepl = str(_zawor.NAMEPL)
        self.sensorHP = '%'+str(_zawor.SENSOR_HP)
        self.sensorHP2 = '%'+str(_zawor.SENSOR_HP2)
        self.sensorWP = '%'+str(_zawor.SENSOR_WP)
        self.sensorWP2 = '%'+str(_zawor.SENSOR_WP2)
        self.outputHP = '%'+str(_zawor.OUTPUT_HP)
        self.outputWP = '%'+str(_zawor.OUTPUT_WP)
        self.outputIDLE = '%'+str(_zawor.IDLE)
        self.outputBRAKE = '%'+str(_zawor.BRAKE_RELEASE)
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
        if self.sensorHP == '%nan':
            _adres = '%I1000.0'
        else:
            _adres = self.sensorHP
        return f'{self.prefix}-vsen_{self.name}_HP_{self.sideHP}'

    @property
    def get_sensorNameHP2(self):
        # BR-vsen_imitation_HP_front
        return f'{self.prefix}-vsen_{self.name}_HP2_{self.sideHP}'

    @property
    def get_sensorNameWP(self):
        # BR-vsen_imitation_WP_front
        if self.sensorWP == '%nan':
            _adres = '%I1000.0'
        else:
            _adres = self.sensorWP
        return f'{self.prefix}-vsen_{self.name}_WP_{self.sideWP}'

    @property
    def get_sensorNameWP2(self):
        # BR-vsen_imitation_HP_front
        return f'{self.prefix}-vsen_{self.name}_WP2_{self.sideWP}'

    @property
    def get_outputNameHP(self):
        # BR-ez_imitation_HP_front
        if self.outputHP == '%nan':
            _adres = 'Q1000.0'
        else:
            _adres = self.outputHP
        return f'{self.prefix}-ez_{self.name}_HP_{self.sideHP}'

    @property
    def get_outputNameWP(self):
        # BR-ez_imitation_WP_front
        if self.outputWP == '%nan':
            _adres = 'Q1000.0'
        else:
            _adres = self.outputWP
        return f'{self.prefix}-ez_{self.name}_WP_{self.sideWP}'

    @property
    def get_outputNameIDLE(self):
        # BR-ez_imitation_IDLE
        if self.outputIDLE == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputIDLE
        return f'{self.prefix}-ez_{self.name}_IDLE'

    @property
    def get_outputNameBRAKE(self):
        # BR-ez_imitation_BRAKE_RELEASE
        if self.outputBRAKE == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputBRAKE
        return f'{self.prefix}-ez_{self.name}_BRAKE_RELEASE'

    # ----- Komentarze tagów -----

    @property
    def get_sensorNameHPcomment(self):
        #nc - [I20.5] czujnik BR IMITACJA HP front
        if self.sensorHP == '%nan':
            _adres = '%I1000.0'
        else:
            _adres = self.sensorHP
        return f'#nc - [{_adres[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'

    @property
    def get_sensorNameHP2comment(self):
        #nc - [I20.5] czujnik BR IMITACJA HP front
        return f'#nc - [{self.sensorHP2[1:]}] czujnik {self.prefix}-{self.namepl} HP {self.sideHP}'

    @property
    def get_sensorNameWPcomment(self):
        #nc - [I20.5] czujnik BR IMITACJA WP front
        if self.sensorWP == '%nan':
            _adres = '%I1000.0'
        else:
            _adres = self.sensorWP
        return f'#no - [{_adres[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'

    @property
    def get_sensorNameWP2comment(self):
        #nc - [I20.5] czujnik BR IMITACJA WP front
        return f'#no - [{self.sensorWP2[1:]}] czujnik {self.prefix}-{self.namepl} WP {self.sideWP}'

    @property
    def get_outputNameHPcomment(self):
        # [1] BR-imitation HP FRONT [I20.5]
        if self.outputHP == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputHP
        if self.sensorHP2 != '%nan':
            _tmp = f', {self.sensorHP2[1:]}'
        else:
            _tmp = ''
        return f'[{self.index}] {self.prefix}-{self.namepl} HP {self.sideHP} [{self.sensorHP[1:]}{_tmp}]'

    @property
    def get_outputNameWPcomment(self):
        # [1] BR-imitation WP FRONT [I20.5]
        if self.outputWP == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputWP
        if self.sensorWP2 != '%nan':
            _tmp = f', {self.sensorWP2[1:]}'
        else:
            _tmp = ''
        return f'[{self.index}] {self.prefix}-{self.namepl} WP {self.sideWP} [{self.sensorWP[1:]}{_tmp}]'

    @property
    def get_outputNameIDLEcomment(self):
        # [1] BR-imitation IDLE
        if self.outputIDLE == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputIDLE
        return f'[{self.index}] {self.prefix}-{self.namepl} IDLE'

    @property
    def get_outputNameBRAKEcomment(self):
        # [1] BR-imitation IDLE
        if self.outputBRAKE == '%nan':
            _adres = '%Q1000.0'
        else:
            _adres = self.outputBRAKE
        return f'[{self.index}] {self.prefix}-{self.namepl} BRAKE RELEASE'
