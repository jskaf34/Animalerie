from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import *

def base_ini(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    message = 'Bienvenue à l\'animalerie !'
    return  render(request, 'animalerie/base_ini.html', {'animaux': animaux,'equipements':equipements,'bienvenue':message})

def base(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    message = 'Bienvenue à l\'animalerie !'
    return  render(request, 'animalerie/base.html', {'animaux': animaux,'equipements':equipements,'bienvenue':message})

def animal_detail(request, id_animal, error = 0, message = ''):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form=MoveForm()
    if request.method == "POST":
        form = MoveForm(request.POST)
    else:
        form = MoveForm()
    if form.is_valid():
        lieu = form.cleaned_data['lieu'].id_equip
        if lieu == 'Mangeoire':
            error,message = nourrir(animal.id_animal)
        elif lieu == 'Roue':
            error,message = divertir(animal.id_animal)
        elif lieu == 'Nid':
            error,message = coucher(animal.id_animal)
        else:
            error,message = réveiller(animal.id_animal)
        return render(request, 'animalerie/animal_detail.html', {'id_animal':id_animal,'animaux': animaux,'equipements':equipements,'message':message, 'error':error})
    else:
        form = MoveForm()
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})

def litière(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return  render(request, 'animalerie/litière.html', {'animaux': animaux,'equipements':equipements})

def nourrir(id_animal):
    if vérifie_disponibilité('Mangeoire') == 'occupé':
        animal = cherche_occupant('Mangeoire')
        return 1, f'Impossible, le mangeoire est actuellement occupé par {animal[0]}'
    elif lit_état(id_animal) != 'affamé':
        return 1, f'Désolé, {id_animal} n\'a pas faim!'
    else :
        change_lieu(id_animal, 'Mangeoire')
        change_état(id_animal, 'repus')
        return 2, f"Félicitations, {id_animal} a rejoint le mangeoire et est maintenant repus."


def divertir(id_animal):
    if vérifie_disponibilité('Roue') == 'occupé':
        animal = cherche_occupant('Roue')
        return 1, f'Impossible, la roue est actuellement occupée par {animal[0]}'
    elif lit_état(id_animal) != 'repus':
        return 1, f'Désolé, {id_animal} n\'est pas en état de faire du sport!'
    else :
        change_lieu(id_animal, 'Roue')
        change_état(id_animal, 'fatigué')
        return 2, f"Félicitations, {id_animal} a rejoint la roue et est maintenant fatigué."


def coucher(id_animal):
    if vérifie_disponibilité('Nid') == 'occupé':
        animal = cherche_occupant('Nid')
        return 1,f'Impossible, le nid est actuellement occupé par {animal[0]}'
    elif lit_état(id_animal) != 'fatigué':
        return 1, f'Désolé, {id_animal} n\'est pas fatigué!'
    else :
        change_lieu(id_animal, 'Nid')
        change_état(id_animal, 'endormi')
        return 2, f"Félicitations, {id_animal} a rejoint le nid et est maintenant endormi."

def réveiller(id_animal):
    if lit_état(id_animal) != 'endormi':
        return 1 , f'Désolé, {id_animal} ne dort pas!!'
    else :
        change_lieu(id_animal, 'Litière')
        change_état(id_animal, 'affamé')
        return 2, f"Félicitations, {id_animal} a rejoint la litière et est maintenant affamé."

