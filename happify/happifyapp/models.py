from django.db import models

# UserAccount model
class UserAccount(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

# Preference model
class Preference(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    activity = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} - {self.activity}'

# AddedActivities model
class AddedActivity(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)  # Links activity to a user
    added_activity = models.CharField(max_length=100)  # Name of the activity
    datetime = models.DateTimeField()  # Date and time of the activity

    def __str__(self):
        return f"{self.user.username} - {self.added_activity} on {self.datetime}"
