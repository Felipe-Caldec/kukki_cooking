from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import codecs
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def entrada_view(request):
    return render (request, 'entrada.html')

def catalogo_view(request):
    return render (request, 'catalogo.html')

@csrf_exempt
def procesar_carrito(request):
    if request.method == 'POST':
        items_json = request.POST.get('items')
        items = json.loads(items_json)

        # Aquí puedes guardar en base de datos, enviar por correo, etc.
        for item in items:
            print(f"Producto: {item['titulo']} - Precio: {item['precio']}")

        return render(request, 'pedido_exitoso.html', {'items': items})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get('items')
        items = json.loads(items_json)
        total = sum(
            int(item['precio'].replace('.', '')) for item in items
            )
        return render(request, 'checkout.html', {'items': items, 'items_json': items_json, 'total': total})
    return redirect('catalogo')

def procesar_pedido(request):
    if request.method == 'POST':
        items_raw = request.POST.get('items')
        items_unescaped = codecs.decode(items_raw, 'unicode_escape') #Decodificamos los caracteres unicode escapados
        items = json.loads(items_unescaped)
        nombre = request.POST.get("nombre")
        direccion = request.POST.get("direccion")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")

        mensaje = f"Nuevo pedido de: {nombre}\n"
        mensaje += f"Dirección: {direccion}\nCorreo: {correo}\nTeléfono: {telefono}\n\n"
        mensaje += "Productos solicitados:\n"

        for item in items:
            mensaje += f"- {item['titulo']} (${item['precio']})\n"

        mensaje += f"\nTotal: ${sum(int(item['precio'].replace('.', '')) for item in items)}"

        send_mail(
            subject="Nuevo Pedido",
            message=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  
            fail_silently=False,
        )

        return render(request, 'pedido_exitoso.html', {'nombre': nombre})
    return redirect('portada')

def catalogo_view(request):
    cards = [
        {"titulo": "Torta Charlotte frambuesa", "descripcion": "Lindo corazon para regalo", "Precio": "2.000", "imagen": static("charlotte_frambuesa.png"), "categoria":"Torta", "adicional":"Corazon hecho de yeso sin pintar"},
        {"titulo": "Cheescake frutos rojos", "descripcion": "Texto 2", "Precio": "2.000", "imagen": static("cheescake_frutosrojos.png"), "categoria":"Cheesecake"},
        {"titulo":"Torta 3 leches", "descripcion": "Texto 3", "Precio": "2.000", "imagen": static("torta_3leches.png"), "categoria":"Torta"},
        {"titulo": "Torta amor", "descripcion": "Texto 4", "Precio": "2.000", "imagen": static("torta_amor.png"), "categoria":"Torta"},
        {"titulo": "Torta personalizada", "descripcion": "Texto 5", "Precio": "2.000", "imagen": static("torta_personalizada.png"), "categoria":"Torta"},
        {"titulo": "Torta plátano manjar", "descripcion": "Texto 6", "Precio": "2.000", "imagen": static("torta_platanomanjar.png"), "categoria":"Torta"},
        {"titulo": "Torta selva negra", "descripcion": "Texto 7", "Precio": "2.000", "imagen": static("torta_selvanegra.png"), "categoria":"Torta"},
        {"titulo": "Card 8", "descripcion": "Texto 8", "Precio": "2.000", "imagen": static("cheescake_frutosrojos.png"),"categoria":"Cheesecake"},
        {"titulo": "Torta zanahoria", "descripcion": "Texto 9", "Precio": "2.000", "imagen": static("torta_zanahoria.png"), "categoria":"Torta"},
        {"titulo": "Vintage cake", "descripcion": "Texto 10", "Precio": "2.000", "imagen": static("vintage_cake.png"), "categoria":"Torta"},
        {"titulo": "Berlines", "descripcion": "Texto 11", "Precio": "2.000", "imagen": static("berlines.png"), "categoria":"Alfajores"},
        {"titulo": "Card 12", "descripcion": "Texto 12", "Precio": "2.000", "imagen": static("img6.png"), "categoria":"Infantil"},
        {"titulo": "Card 13", "descripcion": "Texto 13", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Infantil"},
        {"titulo":"Card 14", "descripcion": "Texto 14", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Limpieza"},
        {"titulo": "Card 15", "descripcion": "Texto 15", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Limpieza"},
        {"titulo": "Card 16", "descripcion": "Texto 16", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Limpieza"},
        {"titulo": "Card 17", "descripcion": "Texto 17", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Limpieza"},
        {"titulo": "Card 18", "descripcion": "Texto 18", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Hogar"},
        {"titulo": "Card 19", "descripcion": "Texto 19", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Hogar"},
        {"titulo": "Card 20", "descripcion": "Texto 20", "Precio": "2.000","imagen": static("images.jpg"), "categoria":"Hogar"}
      
    ]

    categorias = ["Torta", "Alfajores", "Galletas", "Cheesecake"]

    categoria = request.GET.get('categoria')
    if categoria:
        cards = [card for card in cards if card['categoria'] == categoria]
    
    paginator = Paginator(cards, 16)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalogo.html', {'page_obj': page_obj, "categoria_activa": categoria, 
                                             'cards':cards, "categorias": categorias})