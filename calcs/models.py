from djongo import models

# Create your models here.

class Calculation(models.Model):
    source = models.CharField(max_length=255)
    start_lat = models.DecimalField(max_digits=20, decimal_places=12)
    start_long = models.DecimalField(max_digits=20, decimal_places=12)

    dest = models.CharField(max_length=255)
    end_lat = models.DecimalField(max_digits=20, decimal_places=12)
    end_long = models.DecimalField(max_digits=20, decimal_places=12)

    uber_price = models.DecimalField(max_digits=10, decimal_places=6)
    lyft_price = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return "source: {} @ ({}, {})\n \
                dest: {} @ ({}, {})\n \
                uber_price: {}\n \
                lyft_price: {}".format(self.source, self.start_lat, self.start_long, 
                                        self.dest, self.end_lat, self.end_long, 
                                        self.uber_price, self.lyft_price) 

class Input(models.Model):
    start_lat = models.DecimalField(max_digits=20, decimal_places=12)
    start_long = models.DecimalField(max_digits=20, decimal_places=12)
    end_lat = models.DecimalField(max_digits=20, decimal_places=12)
    end_long = models.DecimalField(max_digits=20, decimal_places=12)

    def __str__(self):
        return "source: ({}, {})\n \
                dest: ({}, {})\n".format(self.start_lat, self.start_long,
                                        self.end_lat, self.end_long)