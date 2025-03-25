
from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image, ImageOps, ImageDraw


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")
    is_employee = models.BooleanField(verbose_name="Ar darbuotojas", default=False)

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height != img.width:
            min_dimension = min(img.height, img.width)
            img = ImageOps.fit(img, (min_dimension, min_dimension))

        output_size = (300, 300)
        img = img.resize(output_size)
        mask = Image.new("L", output_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + output_size, fill=255)
        img = img.convert("RGBA")
        img.putalpha(mask)
        img.save(self.photo.path, format='PNG')

    class Meta:
        verbose_name = "Profilis"
        verbose_name_plural = "Profiliai"


class Group(models.Model):
    name = models.CharField(verbose_name="Produktų grupė", max_length=100, help_text="Įveskite produktų grupės pavadinimą")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produktų grupė"
        verbose_name_plural = "Produktų grupės"

class Product(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
    price = models.IntegerField(verbose_name="Kaina", null=True, blank=True, help_text="Paros nuomos kaina")
    description = HTMLField(verbose_name="Aprašymas", max_length=1000, help_text='Trumpas produkto aprašymas', null=True, blank=True, default="")
    inv_no = models.CharField(verbose_name="Invenorizacijos numeris", max_length=100, null=True, blank=True, unique=True,
                              help_text="Veskite invenorizacijos numerį")
    quantity = models.IntegerField(verbose_name="Kiekis", null=True, blank=True, help_text="Kiekis")
    group = models. ForeignKey(to="Group", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Produktų grupės", help_text="Parinkite kokia grupei priklauso produktas")
    cover = models.ImageField(verbose_name="Paveikslėlis", upload_to='covers', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Prouktas"
        verbose_name_plural = "Produktai"
        ordering = ['inv_no']


class Status(models.Model):
    uuid = ShortUUIDField(help_text='Unikalus ID vienodams produktams')
    product = models.ForeignKey(to="Product", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produktas", related_name="product_status")
    customer = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Klientas")
    reservations = models.ForeignKey(to="Reservation", on_delete=models.SET_NULL, null=True, blank=True, related_name="status_reservations")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Sukurta")

    LOAN_STATUS = (
        ('n', 'Laikinai neprieinama'),
        ('i', 'Išnuomota'),
        ('g', 'Prekę turime sandėlyje.'),
        ('r', 'Rezervuota'),
    )

    condition = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", verbose_name="Būsena")

    class Meta:
        ordering = ['due_date']
        verbose_name = "Produkto būsena"
        verbose_name_plural = "Produktų būsenos"
        ordering = ['-pk']

    def __str__(self):
        return f"{str(self.uuid)[:6]} - {self.get_condition_display()}"


class Reservation(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='reservations_status',null=True, blank=True)
    start_date = models.DateField(verbose_name="Nuomos pradžios data", null=True, blank=True)
    end_date = models.DateField(verbose_name="Nuomos pabaigos datas", null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Klientas")
    is_approved = models.BooleanField(default=False, verbose_name="Ar patvirtinta", null=True, blank=True)


    class Meta:
        verbose_name = "Rezervacija"
        verbose_name_plural = "Rezervacijos"
        ordering = ['start_date']

    def is_overdue(self):
        return self.end_date and date.today() > self.end_date

    def __str__(self):
        status_uuid = self.status.uuid if self.status else "No Status"
        return f"Status UUID: {status_uuid} ({self.start_date} - {self.end_date} - {self.customer})"





