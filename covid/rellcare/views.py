from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login as Dlogin, logout as Dlogout
from django.db.models import Count

# Sherelle logout ne fonctionne pas
# d'accord 
# J'ai trouvé tu appellez logout de django et tu avais un fonction logout (donc recursion infini)
#han je vois lool sorry

#Sherelle le truc la ne calcul pas bien hein

# J'ai mis oui partout on me dis que je n'ai rien de grave lol
#euuch

#Regarde je vais te laisser pour la priere du soir
# je reviens apres
#dacc pense a moi :-) stp
def logout(request):
    if request.method == 'POST':
        Dlogout(request)
        return redirect('home')
    return render(request, "rellcare/home.html")

def register(request):
    if request.method == 'POST':
        pays = request.POST['pays']
        name = request.POST['name']
        email= request.POST['email']
        password  = request.POST['password']

        user = User.objects.create_user(pays=pays, name=name, email=email, password=password)
        Dlogin(request, user)
        return redirect('ask')
    return render(request,"rellcare/register.html")

def myReponses(request):
    if not request.user.is_authenticated:
         return redirect('login')
    reponses = Reponse.objects.filter(user_id=request.user.id)
    user = User.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1).order_by('-reponses')[:10]
    us =  sorted(list(set(user)), key=lambda k: k.reponses.count(), reverse=True )
    ctx = {'reponses':reponses, 'users':us}
    return render(request,"rellcare/ask/answers.html",ctx)

def question(request, id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            reponse = request.POST['reponse']
            user = request.user
            question = Question.objects.get(pk=id)

            res = Reponse.objects.create(user=user, reponses=reponse, question=question)
            return redirect('question', id=id)
    question = Question.objects.get(pk=id)
  
    user = User.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1).order_by('-reponses')[:10]
    us =  sorted(list(set(user)), key=lambda k: k.reponses.count(), reverse=True )
    ctx = {'question':question, 'users':us}
    return render(request, "rellcare/ask/question.html", ctx)

def unanswered(request):
      question = Question.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count=0)
      user = User.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1).order_by('-reponses')[:10]
      us =  sorted(list(set(user)), key=lambda k: k.reponses.count(), reverse=True )
      ctx = {'questions':question, 'users':us}
        

      return render(request, "rellcare/ask/unanswered.html",ctx)

def login(request):
    confirmed = False
    ctx = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            Dlogin(request, user)
            return redirect('ask.me')
        else:
            print("user is not authenticated")
        return redirect('login')
    else:
        ctx

    return render(request, "rellcare/login.html",ctx)


def ask(request):
    ctx = {}
        # Voici sa
    # if request.user.is_authenticated():
    #    user = request.user
    # sa verifie si l'utilisateur est connecté et sa le recupere
    # Tu connaissais deja? J'esper que tu apprend c'est important d'apprendre fait vite
    #non non :-)
    # Maintenant creer la question avec le user
    # Attention la variable question est deja utilisé non c'est text
    # Good girl Maintenant si il n'est pas connecté tu creer juste la question sans user

    #han ok ok
    # NOn je doute que ce sois sa
    #ce que tu as dis norh han je vois 
    #quel user? c'est pas le user que  tu as mis dans le else?
    #C EST DEJA GRAVE  :-(
    # Ok va te reposer alors je vais continuer mais deja c'est pas encore sa
    # avant d'aller ajoute un autre terminal juste au cas ou et relance le port 8000 chez moi
    # et le port 8080 comme sa j'ai tout en double
    #C EST BON? oui
    # tu peux pas supporter encore ?
    # D'accord
    # Good night
    # Meri Bonne nuit
    #demain je vais quelque part le matin :-(
    #j ai regler l'ecran de veille tu peux woork jusqu'a xh
    if request.method == 'POST':
        question = request.POST['question']
        anonyme = request.POST.get('anonyme','off')

        if request.user.is_authenticated:
            user = request.user
            ques = Question.objects.create(user = user, text = question, anonyme = True if anonyme=='on' else False)
        else:
            ques = Question.objects.create(text = question, anonyme = True)
        return redirect('question', id=ques.id)
        

        
        
        
    
    else:
        question = Question.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1)
        user = User.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1).order_by('-reponses')[:10]
        us =  sorted(list(set(user)), key=lambda k: k.reponses.count(), reverse=True )
        print(us) #JE VAIS UN PEU REGARDER DISTINCT EN DJANGO SUR GOOGLE, METS distinct(). ON PEUT FAIRE EN DEUX REQUETES? ON SELECTIONNE D ABORD 
        ctx = {'questions':question, 'users':us}
        return render(request, "rellcare/ask/ask.html",ctx)


def me(request):
    if not request.user.is_authenticated:
        return redirect('login')
    question = Question.objects.filter(user_id=request.user.id)
    user = User.objects.annotate(reponse_count=Count('reponses')).filter(reponse_count__gte=1).order_by('-reponses')[:10]
    us =  sorted(list(set(user)), key=lambda k: k.reponses.count(), reverse=True )
    ctx = {'questions':question, 'users':us}
    return render(request, "rellcare/ask/me.html",ctx)
def statistics(request):
    ctx = {}
    return render(request, "rellcare/statistics.html",ctx)

def us(request):
    ctx = {}
    return render(request, "rellcare/us.html",ctx)

def consultation(request):
    
    if request.method == 'POST':
        body = json.loads(request.body)
      
        
        answers = body.get('answers')

        #print(answers)
        #Sherelle ooh ? tfk ?
        #rien suis la te regarde te deplacer
        #Envoie les question dans le template de ask.html les question qui sont repondu
        #tu peut norh ?
        #La tu comprend ?
        #han je vois ca va
        # Mets les question dans le context
        #Dans le template de Ask.html j'ai besion des question de la bd (les question qui ont aumoin une reponse)
        #comprends pas bien
        point = 0
        for el in answers:
            
            if el.get('id') == 'q_1' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_2' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_3' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_4' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_5' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_6' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_7' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_8' and el.get('answer') == True:
                point = point + 2
            if el.get('id') == 'q_9' and el.get('answer') == True:
                point = point + 2
            if el.get('id') == 'q_10' and el.get('answer') == True:
                point = point + 1
            if el.get('id') == 'q_11' and el.get('answer') == True:
                point = point + 3
            if el.get('id') == 'q_12' and el.get('answer') == True:
                point = point + 3
            if el.get('id') == 'q_13' and el.get('answer') == True:
                point = point + 3
        if point in range(0,3):
            response =  {
                'resume' : 'Vous êtes en santé',
                'appercue': 'Il y\'a rien a signaler!',
                'conseil' : [
                    {
                        'titre': 'Respectez les mésures barrieres',
                        'description': 'A ce stade de la maladie toute personne est considéré comme asymptomatiques c\'est à dire potentiel malade ne présentant aucun symptôme'
                    },
                    {
                        'titre': 'Refaite le test',
                        'description': 'Refaite le test apres 2 jours, Si vos symptômes s\'aggravent, appellez le centre d\'urgence (1510 au Cameroon) et faite vous diagnostiquer'
                    },
                    {
                        'titre': 'Prenez des précautions',
                        'description': 'Vous devez pratiquer l\'hygiene au quotidient, pensez a utiliser les mouchoir a usage unique et a les jeter quand ils sont usée.'
                    },
                ]
            }
        elif  point in range(3,6):
            response =  {
                'resume' : 'Vous n\avez rien de grave',
                'appercue': 'Vous devez vous hydrater et refaire le test',
                'conseil' : [
                    {
                        'titre': 'Hydratez vous',
                        'description': 'Nous vous conseillons de boire beaucoup d\'eau et des boissons chaudes'
                    },
                    {
                        'titre': 'Pratiqué l\'hygiene',
                        'description': 'Vous devez pratiquer l\'hygiene au quotidient, pensez a utiliser les mouchoir a usage unique et a les jeter quand ils sont usée.'
                    },
                    {
                        'titre': 'Restez confiner',
                        'description': 'Evitez de sortir et vous baladez pour votre sécurité et la sécurité de votre entourage, si possible ayez un chambre et un douche uniquemnet pour vous'
                    },
                    {
                        'titre': 'Refaite le test',
                        'description': 'Refaite le test apres 2 jours, Si vos symptômes s\'aggravent, appellez le centre d\'urgence (1510 au Cameroon) et faite vous diagnostiquer'
                    },
                    {
                        'titre': 'Respectez les mésures barrieres',
                        'description': 'Vous devez pratiquer l\'hygiene au quotidient, pensez a utiliser les mouchoir a usage unique et a les jeter quand ils sont usée.'
                    },
                    
                ]
            }
        elif  point in range(6,13):
            response =  {
                'resume' : 'Contactez votre médecin ou appelez le 1510',
                'appercue': 'Votre situation est assez délicat et vous devez consultez un spécialiste de santé',
                'conseil' : [
                    {
                        'titre': 'Consultez un medecin',
                        'description': 'Vous devez appeler votre médecin au plus vite pour vous faire diagnostiquer. Si cela est impossible, appellez le centre spécialisé (1510 au Cameroon)'
                    },
                     {
                        'titre': 'Restez en quarantaine',
                        'description': 'Evitez de sortir et vous baladez pour votre sécurité et la sécurité de votre entourage, si possible ayez un chambre et un douche uniquemnet pour vous'
                    },
                    {
                        'titre': 'Hydratez vous',
                        'description': 'Nous vous conseillons de boire beaucoup d\'eau et des boissons chaudes'
                    },
                    {
                        'titre': 'Pratiqué l\'hygiene',
                        'description': 'Vous devez pratiquer l\'hygiene au quotidient, pensez a utiliser les mouchoir a usage unique et a les jeter quand ils sont usée.'
                    },
                   
                    {
                        'titre': 'Refaite le test',
                        'description': 'Refaite le test apres 2 jours, Si vos symptômes s\'aggravent, appellez le centre d\'urgence (1510 au Cameroon) et faite vous diagnostiquer'
                    },
                   
                    
                ]
            }
        else: 
            response =  {
                'resume' : 'Vous avez besion d\'assistance médicale',
                'appercue': 'Gardez votre calme, restez isolé et appellez le 1510',
                'conseil' : [
                    {
                        'titre': 'Appelez les service d\'urgence 1510',
                        'description': 'Contacter immédiatement le service spécialisé et faites vous soigner'
                    },
                     {
                        'titre': 'Restez en quarantaine',
                        'description': 'Evitez de sortir et vous baladez pour votre sécurité et la sécurité de votre entourage, si possible ayez un chambre et un douche uniquemnet pour vous'
                    },
                    {
                        'titre': 'Hydratez vous',
                        'description': 'Nous vous conseillons de boire beaucoup d\'eau et des boissons chaudes'
                    },
                    {
                        'titre': 'Pratiqué l\'hygiene',
                        'description': 'Vous devez pratiquer l\'hygiene au quotidient, pensez a utiliser les mouchoir a usage unique et a les jeter quand ils sont usée.'
                    },
                   
                   
                    
                ]
            }

       
        return JsonResponse(response)
    else:

        QUESTIONS = [
            {
                'question': 'Avez vous une toux ?',
                'id': 'q_1'
            },
            {
                'question': 'Avez vous un rhume?',
                'id': 'q_2'
            },
            {
                'question': 'Avez vous une diahrree?',
                'id': 'q_3'
            },
            {
                'question': 'Avez vous une perte de l\'odorat?',
                'id': 'q_4'
            },
            {
                'question': 'Avez vous des maux de tête?',
                'id': 'q_5'
            },
            {
                'question': 'Avez vous une température supérieur a 37.8°C ?',
                'id': 'q_6'
            },
            {
                'question': 'Avez vous des maux de gorge?',
                'id': 'q_7'
            },
            {
                'question': 'Ressentez vous une gene respiratoire?',
                'id': 'q_8'
            },
            {
                'question': 'Ressentez vous une fatigue?',
                'id': 'q_9'
            },
            {
                'question': 'Ressentez vous des douleurs musculaires?',
                'id': 'q_10'
            },
            {
                'question': 'Avez-vous été à l\'étranger au cours du dernier mois?',
                'id': 'q_11',
            },
            {
                'question': 'Avez-vous voyagé dans un pays touché par la pandémie de Covid-19?',
                'id': 'q_12'
            },
            {
                'question': 'Avez-vous été en contact avec un cas confirmé de Covid-19?',
                'id': 'q_13'
            }
        ]
        ctx = {'questions': QUESTIONS}
        return render(request,"rellcare/consultation.html",ctx)


def home(request):
    return render(request,"rellcare/home.html")