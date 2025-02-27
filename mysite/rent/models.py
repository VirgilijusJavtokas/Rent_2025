from django.db import models
import uuid

# Create your models here.
class RentGroup(models.Model):
    name_of_group = models.CharField(verbose_name="Produktų grupės", max_length=100, help_text="Įveskite produktų grupės pavadinimą")

    def __str__(self):
        return self.name_of_group

    class Meta:
        verbose_name = "Produktų grupė"
        verbose_name_plural = "Produktų grupės"

class RentProduct(models.Model):
    name_of_product = models.CharField(verbose_name="Pavadinimas", max_length=100)
    summary = (models.TextField(verbose_name="Aprašymas", max_length=1000, help_text='Trumpas produkto aprašymas'))
    inv_no = models.CharField(verbose_name="Invenorizacijos numeris", max_length=100)
    group = models. ManyToManyField(to="RentGroup", verbose_name="Produktų grupės", help_text="parinkite kokia grupei priklauso produktas")

    def __str__(self):
        return self.name_of_product

    class Meta:
        verbose_name = "Prouktas"
        verbose_name_plural = "Produktai"

class ProductInstance(models.Model):
    rent_product = models.ForeignKey(to="RentProduct", on_delete=models.CASCADE, verbose_name="Produktas", related_name="product_instance")
    due_date = models.DateField(verbose_name="Bus prieinamas", null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="a", help_text='Statusas')

    class Meta:
        ordering = ['due_date']
        verbose_name = "Produkto kopija"
        verbose_name_plural = "Produkto kopijos"

    def __str__(self):
        return f'{self.id} ({self.rent_product})'