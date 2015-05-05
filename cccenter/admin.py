from django.contrib import admin

# Register your models here.
from .models import UserProfile, Challenge, Comment, Cipher, Notification

class UserProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)

class ChallengeAdmin(admin.ModelAdmin):
	class Meta:
		model = Challenge

admin.site.register(Challenge, ChallengeAdmin)

class CommentAdmin(admin.ModelAdmin):
	class Meta:
		model = Comment

admin.site.register(Comment, CommentAdmin)

class CipherAdmin(admin.ModelAdmin):
	class Meta:
		model = Cipher

admin.site.register(Cipher, CipherAdmin)

class NotificationAdmin(admin.ModelAdmin):
	class Meta:
		model = Notification

admin.site.register(Notification, NotificationAdmin)