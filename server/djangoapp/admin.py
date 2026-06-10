from django.contrib import admin
from djangoapp.models import Dealer, Review, UserProfile


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'city', 'state', 'email', 'phone')
    search_fields = ('business_name', 'city', 'state')
    list_filter = ('state', 'city')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dealer', 'rating', 'user', 'sentiment', 'created_at')
    search_fields = ('dealer__business_name', 'review_text')
    list_filter = ('rating', 'sentiment', 'created_at')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone')
    search_fields = ('user__username', 'first_name', 'last_name')
