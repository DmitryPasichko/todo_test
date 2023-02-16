from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('shop/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template('shop/about.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def products(request):
    template = loader.get_template('shop/products.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def fashion(request):
    template = loader.get_template('shop/fashion.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def news(request):
    template = loader.get_template('shop/news.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def contacts(request):
    template = loader.get_template('shop/contact.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
