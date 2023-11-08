from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import NFT


# Create your views here.
def home(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "registration/signup.html")


def login(request):
    return render(request, "registration/login.html")


def logout(request):
    return render(request, "index.html")


def main_page(request):
    nfts = NFT.objects.all()
    return render(request, 'NFTmarketplace.html', {'nfts': nfts})

def nft_detail(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    return render(request, 'NFT.html', {'nft': nft})
