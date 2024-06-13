from django.contrib import admin
from blog.models import Ticket, Review, UserFollows, UserBlock


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user')


admin.site.register(UserFollows)
admin.site.register(UserBlock)
