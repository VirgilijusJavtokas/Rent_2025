from django.db import models
import uuid

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
    description = (models.TextField(verbose_name="Aprašymas", max_length=1000, help_text='Trumpas produkto aprašymas'))
    inv_no = models.CharField(verbose_name="Invenorizacijos numeris", max_length=100, null=True, blank=True, unique=True,
                              help_text="Veskite invenorizacijos numerį")
    quantity = models.IntegerField(verbose_name="Kiekis", null=True, blank=True, help_text="Kiekis")
    group = models. ForeignKey(to="Group", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Produktų grupės", help_text="Parinkite kokia grupei priklauso produktas")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Prouktas"
        verbose_name_plural = "Produktai"
        ordering = ['inv_no']


class Status(models.Model):
    product = models.ForeignKey(to="Product", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Produktas", related_name="product_status")
    due_date = models.DateField(verbose_name="Bus prieinamas", null=True, blank=True)
    is_available = models.BooleanField(default=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    condition = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", help_text='Būklė')

    class Meta:
        ordering = ['due_date']
        verbose_name = "Produkto būsena"
        verbose_name_plural = "Produktų būsenos"
        ordering = ['product']

    def __str__(self):
        return f'Inv. nr.: {self.product.inv_no} - {self.get_condition_display()}'

