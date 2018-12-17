from django.db import models
from django.contrib.gis.db import models
from slugify import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.dispatch import receiver
import os


def validate_file_extension(value):
    if not (value.file.content_type == 'image/png' or value.file.content_type == 'image/jpeg'):
        raise ValidationError(u'File not allowed: invalid extension')

# Create your models here.
class datasets(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50,blank=True)
    epsg = models.IntegerField(default = '3857')
    extentLeft = models.FloatField(default = '-18000000.00')
    extentBottom = models.FloatField(default = '-8000000.00')
    extentRight = models.FloatField(default = '2000000.00')
    extentTop = models.FloatField(default = '15000000.00')
    baselayer = models.TextField(default = 'new ol.layer.Tile({\n    source: new ol.source.OSM()\n}),',blank=True)
    vrt = models.FileField(null=True,blank=True)
    transparency = models.BooleanField()
    #coverage = models.RasterField(blank=True,null=True)

    def publish(self):
        self.slug = slugify (self.name)
        self.save()

    def __str__(self):
        return self.name


class rasterMaps(models.Model):
    titolo = models.CharField(max_length=50)
    slug = models.CharField(max_length=50,blank=True)
    note = models.TextField(blank=True)
    dataset = models.ForeignKey('datasets',blank=True,null=True,related_name="current_dataset",on_delete="PROTECT")
    datasetRecover = models.ForeignKey('datasets',blank=True,null=True,related_name="recover_dataset",on_delete="PROTECT")
    sorgente = models.ImageField(upload_to='warp/', validators=[validate_file_extension])
    sorgente_thumbnail = ImageSpecField(source='sorgente',
                                      processors=[ResizeToFill(120, 120)],
                                      format='JPEG',
                                      options={'quality': 60})
    destinazione =  models.ImageField(upload_to='warp/', blank=True)
    webimg = models.ImageField(upload_to='warp/', blank=True)
    webimg_thumbnail = ImageSpecField(source='webimg',
                                      processors=[ResizeToFill(120, 120)],
                                      format='JPEG',
                                      options={'quality': 60})
    correlazione = models.TextField(blank=True)
    clipSorgente = models.TextField(blank=True)
    clipDestinazione = models.TextField(blank=True)

    def publish(self):
        self.slug = slugify (self.titolo)
        self.save()

    def __str__(self):
        return self.titolo

@receiver(models.signals.post_delete, sender=rasterMaps)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `mappeGeoreferenziate` object is deleted.
    """
    if instance.sorgente:
        sorgente_base, ext = os.path.splitext(instance.sorgente.path)

        if os.path.isfile(instance.sorgente.path):
            os.remove(instance.sorgente.path)

        if os.path.isfile(sorgente_base + ".geojson"):
            os.remove(sorgente_base + ".geojson")

        if os.path.isfile(sorgente_base + ".log"):
            os.remove(sorgente_base + ".log")

    elif instance.destinazione:
        destinazione_base, ext = os.path.splitext(instance.destinazione.path)

        if os.path.isfile(instance.destinazione.path):
            os.remove(instance.destinazione.path)

        if os.path.isfile(destinazione_base + ".geojson"):
            os.remove(destinazione_base + ".geojson")

    elif instance.webimg:
        webimg_base, ext = os.path.splitext(instance.webimg.path)

        if os.path.isfile(instance.webimg.path):
            os.remove(instance.webimg.path)

        if os.path.isfile(webimg_base + ".wld"):
            os.remove(webimg_base + ".wld")
