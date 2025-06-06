from django.contrib import admin
from .models import AssetType, Assets, DamagedAssets

admin.site.register(AssetType)
admin.site.register(Assets)
admin.site.register(DamagedAssets)  # 👈 This is required
