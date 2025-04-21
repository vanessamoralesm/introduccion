# Importaciones necesarias
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, UpdateView, DeleteView
from .forms import PostCreateForm  # Formulario personalizado para crear posts
from .models import Post           # Modelo de publicación (Post)
from django.urls import reverse_lazy  # Para redireccionar usando nombres de URL

# Vista para listar todos los posts del blog
class BlogListView(View):
    def get(self, request, *args, **kwargs):
        post = Post.objects.all()  # Obtiene todos los posts
        context = {
            'post': post  # Los pasa al template como contexto
        }
        return render(request, 'blog_list.html', context)  # Renderiza la lista de posts

# Vista para crear un nuevo post
class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        form = PostCreateForm()  # Instancia vacía del formulario
        context = {
            'form': form
        }
        return render(request, 'blog_create.html', context)  # Muestra el formulario al usuario

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(request.POST)  # Recibe los datos del formulario
        if form.is_valid():  # Si los datos son válidos...
            title = form.cleaned_data.get('title')    # Obtiene el título limpio
            content = form.cleaned_data.get('content')  # Obtiene el contenido limpio

            # Crea el post si no existe ya uno igual (por título y contenido)
            p, created = Post.objects.get_or_create(title=title, content=content)

            return redirect('blog:home')  # Redirige a la página principal del blog

        # Si el formulario no es válido, vuelve a mostrarlo con los errores
        context = {
            'form': form
        }
        return render(request, 'blog_create.html', context)

# Vista para mostrar el detalle de un post específico
class BlogDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)  # Obtiene el post o lanza error 404 si no existe
        context = {
            'post': post
        }
        return render(request, 'blog_detail.html', context)  # Renderiza los detalles del post

# Vista para actualizar (editar) un post existente
class BlogUpdateView(UpdateView):
    model = Post  # Modelo que se va a editar
    fields = ['title', 'content']  # Campos que el usuario puede modificar
    template_name = 'blog_update.html'  # Template que se mostrará

    def get_success_url(self):
        pk = self.kwargs.get('pk')  # Obtiene la clave primaria del post editado
        return reverse_lazy('blog:detail', kwargs={'pk': pk})  # Redirige al detalle del post actualizado

# Vista para eliminar un post
class BlogDeleteView(DeleteView):
    model = Post  # Modelo que se va a eliminar
    template_name = 'blog_delete.html'  # Template de confirmación de borrado
    success_url = reverse_lazy('blog:home')  # Redirige al home después de borrar
