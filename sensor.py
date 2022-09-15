class Sensor:
    def __init__(self, _sensor, _typ):

        self.prefix = str(_sensor.PREFIX)
        self.name = str(_sensor.NAME)
        self.namepl = str(_sensor.NAMEPL)
        self.typ = str(_typ)


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