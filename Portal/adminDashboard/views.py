from django.shortcuts import render

# Renders the main admin dashboard page
def admin(request):
    """
    View for the admin dashboard.

    Renders the 'admin.html' template located in:
    templates/adminDashboard/admin.html
    """
    return render(request, "adminDashboard/admin.html")
