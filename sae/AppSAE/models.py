from django.db import models

class Capteur(models.Model):
    id_capteur = models.CharField(primary_key=True, max_length=100, blank=True)
    endroit = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capteur'

    def __str__(self):
        chain = f"{self.id_capteur}"
        return chain

    def dico(self):
        return {"id_capteur": self.id_capteur, "endroit": self.endroit}

class Description(models.Model):
    id_capteur = models.ForeignKey(Capteur, models.DO_NOTHING, db_column='id_capteur', blank=True, null=True)
    endroit = models.CharField(max_length=40, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    temp = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'description'

    def dico(self):
        return {"id_capteur": self.id_capteur, "endroit": self.endroit, "date":self.date,"time":self.time,"temp":self.temp}