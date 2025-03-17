
from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField

# Create your models here.
class Group(models.Model):
    name = models.CharField(verbose_name="Produktų grupė", max_length=100, help_text="Įveskite produktų grupės pavadinimą")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produktų grupė"
        verbose_name_plural = "Produktų grupės"

class Product(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=100)
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
    due_back = models.DateField(verbose_name="Bus prieinama nuo", null=True, blank=True)
    product = models.ForeignKey(to="Product", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produktas", related_name="product_status")
    is_available = models.BooleanField(default=True)
    customer = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Klientas")
    reservations = models.ForeignKey(to="Reservation", on_delete=models.SET_NULL, null=True, blank=True, related_name="status_reservations")

    LOAN_STATUS = (
        ('n', 'Laikinai neprieinama'),
        ('i', 'Išnuomota'),
        ('g', 'Prekę turime sandėlyje.'),
        ('r', 'Rezervuota'),
    )

    condition = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", help_text='Būklė')

    class Meta:
        ordering = ['due_date']
        verbose_name = "Produkto būsena"
        verbose_name_plural = "Produktų būsenos"
        ordering = ['product']

    def __str__(self):
        return f"{str(self.uuid)[:6]} - {self.get_condition_display()}"


class Reservation(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reservations_product',null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='reservations_status',null=True, blank=True)
    start_date = models.DateField(verbose_name="Nuomos pradžios data", null=True, blank=True)
    end_date = models.DateField(verbose_name="Nuomos pabaigos datas", null=True, blank=True)

    class Meta:
        verbose_name = "Rezervacija"
        verbose_name_plural = "Rezervacijos"
        ordering = ['start_date']

    def is_overdue(self):
        return self.end_date and date.today() > self.end_date

    def __str__(self):
        status_uuid = self.status.uuid if self.status else "No Status"
        return f"Status UUID: {status_uuid} ({self.start_date} - {self.end_date})"


