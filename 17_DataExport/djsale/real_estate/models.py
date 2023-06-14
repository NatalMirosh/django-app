from django.db import models


class PropertyType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class RoomCount(models.Model):
    count = models.IntegerField()

    def __str__(self):
        return str(self.count)


class RealEstate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    room_count = models.ForeignKey(RoomCount, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title