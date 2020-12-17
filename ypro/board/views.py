from .models import Player, Nation, Club
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

# Create your views here.
def signup(request):
  if request.method == 'POST':
    input_username = request.POST['username']
    input_email = request.POST['email']
    input_password = request.POST['password']

    try:
      User.objects.filter(username=input_username,password=input_password)
      return render(request, 'board/signup.html', {'message':'These username,emailaddress has already been used.'})
    except:
      User.objects.create_user(input_username, input_email, input_password)
      return render(request, 'board/signup.html', {'message':'complete!!!'})

  return render(request, 'board/signup.html', {'message': 'Please make your accounts!'})

def login(request):
  if request.method == 'POST':
    input_username = request.POST['username']
    input_password = request.POST['password']
    input_email = request.POST['email']

    user = authenticate(username=input_username, email=input_email, password=input_password)

    if user is not None:
      dj_login(request, user)
      return redirect('board:list_liga')
    else:
      return render(request, 'board/signup.html')

  return render(request, 'board/login.html')

def logout(request):
  logout(request)
  return redirect('login')



class LigaBoardList(ListView):
  template_name = 'board/list.html'
  model = Player
  queryset = Player.objects.filter(league='Liga')
  context_object_name = 'player_list'
  def get_context_data(self, **kwargs):
    params = super(LigaBoardList, self).get_context_data(**kwargs)
    params['league'] = 'Liga Española'
    return params


  # paginate_by = 3

  # 他モデル参照方法
  # def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        # context['book_list'] = Book.objects.all()
        # return context
  # dataを軽くする foreignkey不可
  # def get_queryset(self):
  #   qs = self.model.objects.prefetch_related(Player)
  #   return qs

class PremierBoardList(ListView):
  template_name = 'board/list.html'
  model = Player
  context_object_name = 'player_list'
  queryset = Player.objects.filter(league='Premier')



class SerieBoardList(ListView):
  template_name = 'board/list.html'
  model = Player
  context_object_name = 'player_list'
  queryset = Player.objects.filter(league='Serie A')



class BundesBoardList(ListView):
  template_name = 'board/list.html'
  model = Player
  context_object_name = 'player_list'
  queryset = Player.objects.filter(league='Bundes')



class LigueBoardList(ListView):
  template_name = 'board/list.html'
  model = Player
  context_object_name = 'player_list'
  queryset = Player.objects.filter(league='Ligue 1')



class BoardDetail(DetailView):
  template_name = 'board/detail.html'
  model = Player
  context_object_name = 'player'
  # login_url = '/login/'



class BoardUpdate(UpdateView):
  template_name = 'board/update.html'
  model = Player
  fields = ('name', 'age', 'league', 'club', 'position', 'feature')
  success_url = reverse_lazy('board:list_liga')
  context_object_name = 'player'



class BoardCreate(CreateView):
  template_name = 'board/create.html'
  model = Player
  fields = ('name', 'age', 'league', 'club', 'position', 'image', 'feature')
  success_url = reverse_lazy('board:list_liga')
  context_object_name = 'player'



class BoardDelete(DeleteView):
  template_name = 'board/delete.html'
  model = Player
  success_url = reverse_lazy('board:list_liga')
