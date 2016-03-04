# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import AccountManager, Account
# # Create your views here.
from django.shortcuts import render
from rest_framework import permissions, viewsets,views

from maptestapp.models import Account
from maptestapp.permissions import IsAccountOwner
from maptestapp.serializers import AccountSerializer
import geocoder
from .import views


def plot(request):
    coords = []
    lat_lng = []
    coordinate_pairs = []
    to_pass = []
    new_str = '['

    if request.method == 'POST':
        subject = request.POST.get('subject', None)
        addr1 = request.POST.get('addr1', None)
        addr2 = request.POST.get('addr2', None)
        addr3 = request.POST.get('addr3', None)
        addr4 = request.POST.get('addr4', None)
        addr5 = request.POST.get('addr5', None)

        if subject != '':
            coords.append(subject)

        if addr1!= '':
            coords.append(addr1)
        if addr2 != '':
            coords.append(addr2)
        if addr3 != '':    
            coords.append(addr3)
        if addr4 != '':
            coords.append(addr4)
        if addr5 != '':
            coords.append(addr5)

        print(len(coords))

    for address in coords:
        g = geocoder.google(address)
    
        coordinate_pair = str(g.latlng)
        coordinate_pair = coordinate_pair.replace('[',"")
        coordinate_pair = coordinate_pair.replace(']',"")
        coordinate_pair = coordinate_pair.split()
        coordinate_pairs.append(coordinate_pair)
     
    for item in coords:
        for i in range(0,len(coords)):
            formatted = '{lat:'+coordinate_pairs[i][0]+' lng:'+coordinate_pairs[i][1] + '}'
            if formatted not in to_pass: 
                to_pass.append(formatted)

    for item in to_pass:
        new_str = new_str + item + ", "
        item = item.replace("'","")   
    
    new_str = new_str +']'
    

    return render(request, 'multiple.html', {'new_str':new_str})

def index(request):

    return render(request, 'index.html')

def home(request):


	addresslist = ['2376 Woodward Avenue, Lakewood, OH 44107']
	return render(request, 'test.html', { 'addresslist':addresslist} )

def signup(request):

	return render(request, 'signup.html')

def success(request):

	if request.method == 'POST':
		email_addr = request.POST.get('email')
		user_name = request.POST.get('username')

		email_list = [email_addr]

	

		Account.objects.create_user(email_addr, username=user_name)

	return render(request, 'success.html', {'email_list':email_list})






class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


