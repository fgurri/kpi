import nautilus.plots as p
from django.shortcuts import render


def plotpm(request):
    return render(request, 'base.html', {'plotdiv': p.generate_pm()})


def plotpepm(request):
    return render(request, 'base.html', {'plotdiv': p.generate_pepm(13)})


def plotpcpe(request):
    return render(request, 'base.html', {'plotdiv': p.generate_pcpe()})
