from djongo import models

# Create your models here.

class Calculation(models.Model):
    source = models.CharField(max_length=255)
    source_lat = models.DecimalField(max_digits=20, decimal_places=12)
    source_long = models.DecimalField(max_digits=20, decimal_places=12)

    dest = models.CharField(max_length=255)
    dest_lat = models.DecimalField(max_digits=20, decimal_places=12)
    dest_long = models.DecimalField(max_digits=20, decimal_places=12)

    uber_price = models.DecimalField(max_digits=10, decimal_places=6)
    lyft_price = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return "source: {} @ ({}, {})\n \
                dest: {} @ ({}, {})\n \
                uber_price: {}\n \
                lyft_price: {}".format(self.source, self.source_lat, self.source_long, 
                                        self.dest, self.dest_lat, self.dest_long, 
                                        self.uber_price, self.lyft_price) 
