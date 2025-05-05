from .models import BorrowCart

def cart_item_count(request):
    if request.user.is_authenticated:
        count = BorrowCart.objects.filter(user=request.user, is_active=True).count()
    else:
        count = 0
    return {'cart_item_count': count}