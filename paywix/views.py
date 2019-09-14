from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payu_success(request):
    return JsonResponse(request.POST)


@csrf_exempt
def payu_failure(request):
    return JsonResponse(request.POST)