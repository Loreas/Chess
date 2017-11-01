class Schaakstuk:
    def __init__(self, kleur):
        self.color = kleur



class Pion(Schaakstuk):
    def __init__(self, kleur):
        Schaakstuk.__init__(self, kleur)
