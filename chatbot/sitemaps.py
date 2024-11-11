from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shop_app.models import Product  # Assuming you have a Product model

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.all()  # Adjust based on your model

    def location(self, item):
        return reverse('product_detail', args=[item.id])  # Adjust based on your URL patterns