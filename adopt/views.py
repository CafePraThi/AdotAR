from datetime import datetime

from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from divulgar.models import Pet, Raca

from .models import PedidoAdocao


def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status='P')
        racas = Raca.objects.all()

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        return render(request, 'listar_pets.html', {'pets': pets,
                                                    'racas': racas,
                                                    'cidade': cidade,
                                                    'raca_filter': raca_filter})


def pedido_adocao(requeest, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status='P')

    if not pet.exists():
        messages.add_message(requeest, constants.WARNING,
                             'Esse Pet não se encontra mais disponivel para adoção')
        return redirect('/adotar')

    pedido = PedidoAdocao(pet=pet.first(),
                          usuario=requeest.user,
                          data=datetime.now())

    pedido.save()
    messages.add_message(requeest, constants.SUCCESS,
                         'Pedido de adoção realizado com Sucesso.')

    return redirect('/adotar')
