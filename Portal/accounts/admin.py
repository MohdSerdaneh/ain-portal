from django.contrib import admin
from .models import Contact, Profile, Student, Teacher, User

# Register custom user model for Django admin interface
admin.site.register(User)

# Register profile model to manage user details/extension data
admin.site.register(Profile)

# Register teacher model (inherits from or related to user)
admin.site.register(Teacher)

# Register student model (inherits from or related to user)
admin.site.register(Student)

# Register contact model for managing contact/feedback forms
admin.site.register(Contact)
