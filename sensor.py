class Sensor:
    def __init__(self, _sensor, _typ, _lang):

        self.prefix = str(_sensor.PREFIX)
        self.name = str(_sensor.NAME)
        if _lang == 'pl':
            self.namepl = str(_sensor.NAMEPL)
        else:
            self.namepl = str(_sensor.NAME)
        self.typ = str(_typ)
        self.msg_hp = 0
        self_msg_wp = 0

        if str(_sensor.ADRES) != 'nan':
            self.adres = '%'+str(_sensor.ADRES)
        else:
            self.adres = 'nan'

        # ----- Nazwy tagów -----
    @property
    def get_sensorName(self):
        # BR-vsen_imitation
        return f'{self.prefix}_{self.name}'

    # ----- Komentarze tagów -----
    @property
    def get_sensorNameComment(self):
        #nc - [I20.5] czujnik BR IMITACJA
        return f'[{self.adres[1:]}] {self.typ} "{self.prefix}_{self.namepl}"'

    @property
    def get_sensorNameCommentSmall(self):
        #nc - [I20.5] czujnik BR IMITACJA
        return f'[{self.adres[1:]}] {self.prefix}_{self.namepl}'       

    @property
    def get_sensorNameCommentSmallEN(self):
        #nc - [I20.5] czujnik BR IMITATION
        return f'[{self.adres[1:]}] {self.prefix}_{self.name}'     

    @property
    def get_sensorNameSmall(self):
        # BR-vsen_imitation
        return f'{self.prefix}_{self.namepl}'