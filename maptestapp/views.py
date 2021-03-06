from django.shortcuts import render
from rest_framework import permissions, viewsets,views
from maptestapp.models import Account
from maptestapp.permissions import IsAccountOwner
from maptestapp.serializers import AccountSerializer
import geocoder
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
from time import sleep

import json
import requests
import simplejson

from django.contrib import messages

def plot(request):
    msg_list = []
    coords = []
    lat_lng = []
    coordinate_pairs = []
    to_pass = []
    new_str = '['

    if request.method == 'POST':
        coords = []
        lat_lng = []
        coordinate_pairs = []
        to_pass = []

        distance_selection = request.POST.get('sortOption', None)
        subject = request.POST.get('subject', None)
        addr1 = request.POST.get('addr1', None)
        addr2 = request.POST.get('addr2', None)
        addr3 = request.POST.get('addr3', None)
        addr4 = request.POST.get('addr4', None)
        addr5 = request.POST.get('addr5', None)
        addr6 = request.POST.get('addr6', None)
        addr7 = request.POST.get('addr7', None)
        addr8 = request.POST.get('addr8', None)
        addr9 = request.POST.get('addr9', None)
        addr10 = request.POST.get('addr10', None)
        addr11 = request.POST.get('addr11', None)
        addr12 = request.POST.get('addr12', None)
        addr13 = request.POST.get('addr13', None)
        addr14 = request.POST.get('addr14', None)
        addr15 = request.POST.get('addr15', None)
        addr16 = request.POST.get('addr16', None)
        addr17 = request.POST.get('addr17', None)
        addr18 = request.POST.get('addr18', None)
        addr19 = request.POST.get('addr19', None)
        addr20 = request.POST.get('addr20', None)
        addr21 = request.POST.get('addr21', None)
        addr22 = request.POST.get('addr22', None)
        addr23 = request.POST.get('addr23', None)
        addr24 = request.POST.get('addr24', None)
        addr25 = request.POST.get('addr25', None)
        addr26 = request.POST.get('addr26', None)
        addr27 = request.POST.get('addr27', None)
        addr28 = request.POST.get('addr28', None)
        addr29 = request.POST.get('addr29', None)

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
        if addr6 != '':
            coords.append(addr6)
        if addr7 != '':
            coords.append(addr7)
        if addr8 != '':
            coords.append(addr8)
        if addr9 != '':
            coords.append(addr9)
        if addr10 != '':
            coords.append(addr10)
        if addr11 != '':
            coords.append(addr11)
        if addr12 != '':
            coords.append(addr12)
        if addr13 != '':
            coords.append(addr13)
        if addr14 != '':
            coords.append(addr14)
        if addr15 != '':
            coords.append(addr15)
        if addr16 != '':
            coords.append(addr16)
        if addr17 != '':
            coords.append(addr17)
        if addr18 != '':
            coords.append(addr18)
        if addr19 != '':
            coords.append(addr19)
        if addr20 != '':
            coords.append(addr20)
        if addr21 != '':
            coords.append(addr21)
        if addr22 != '':
            coords.append(addr22)
        if addr23 != '':
            coords.append(addr23)
        if addr24 != '':
            coords.append(addr24)
        if addr25 != '':
            coords.append(addr25)
        if addr26 != '':
            coords.append(addr26)
        if addr27 != '':
            coords.append(addr27)
        if addr28 != '':
            coords.append(addr28)
        if addr29 != '':
            coords.append(addr29)

    tmp_coord_list = []

    for address in coords:
        address = address.strip()
        address = address.replace(" ","")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=AIzaSyABF2rlCMvj-SdYYwsvKq3Wv2U0gPbGsQw"
        sleep(0.05)
        result = requests.get(url)
        data = json.loads(result.text)
     
        try:
            coded_address = data['results'][0]['geometry']['location']
            coded_lat = str(coded_address['lat']) +","
            coded_lng = str(coded_address['lng'])
            tmp_coord_list.append(coded_lat)
            tmp_coord_list.append(coded_lng)
            coordinate_pairs.append(tmp_coord_list)
            tmp_coord_list = []

        except:
            msg_str = "Sorry! There was an error geocoding:  " + address
            msg_list.append(msg_str)
            continue

####CALCULATE DISTANCE BETWEEN POINTS######

#####################################################################################################################################

    if distance_selection == "distance":
        distance_dict = {}  #HOLDS LAT LNG WITH DISTANCE TO OBTAIN SORTED LIST FOR MARKING
        subject_address = coordinate_pairs[0]
        subject_str = subject_address[0].replace(",","") + ", " + subject_address[1].replace(",","")
        target_address = 0

        for i in range(1, len(coordinate_pairs)):
                                                     ##ITERATES THROUGH COORD PAIRS PUTS DISTANCE INTO DICT
            target_address = coordinate_pairs[i]
            target_str = target_address[0].replace(",","") + ", " + target_address[1].replace(",","")
            distance = vincenty(subject_str, target_str).miles
            distance_dict[target_str] = distance

        sorted_pairs = sorted(distance_dict, key=lambda key: distance_dict[key])  ### CREATES SORTED LIST BY KEY
        sorted_pairs.insert(0,subject_str)

                                               ## APPEND SUBJECT PROPERTY AS FIRST ITEM IN SORTED LIST
        for item in sorted_pairs:
            split_coords = item.split()        ## FORMATS FOR JAVASCRIPT

            for i in range(0,len(sorted_pairs)):
                formatted = '{lat:'+split_coords[0]+' lng:'+split_coords[1] + '}'
                if formatted not in to_pass:
                    to_pass.append(formatted)

        for item in to_pass:
            new_str = new_str + item + ", "
            item = item.replace("'","")

        new_str = new_str +']'
        lat_lng = []
        coordinate_pairs = []
        to_pass = []

        return render(request, 'mapping/multiple.html', {'new_str':new_str})

#######################################################################################################################

    elif distance_selection == "order":

        sorted_pairs = []
        subject_address = coordinate_pairs[0]
        subject_str = subject_address[0].replace(",","") + ", " + subject_address[1].replace(",","")
        sorted_pairs.append(subject_str)

        for i in range(1, len(coordinate_pairs)): ##ITERATES THROUGH COORD PAIRS PUTS DISTANCE INTO DICT
            target_address = coordinate_pairs[i]
            target_str = target_address[0].replace(",","") + ", " + target_address[1].replace(",","")
            sorted_pairs.append(target_str)

        for item in sorted_pairs:
            split_coords = item.split()        ## FORMATS FOR JAVASCRIPT

            for i in range(0,len(sorted_pairs)):
                formatted = '{lat:'+split_coords[0]+' lng:'+split_coords[1] + '}'
                if formatted not in to_pass:
                    to_pass.append(formatted)

        for item in to_pass:
            new_str = new_str + item + ", "
            item = item.replace("'","")

        new_str = new_str +']'
        lat_lng = []
        coordinate_pairs = []
        to_pass = []

        return render(request, 'mapping/multiple.html', {'new_str':new_str, 'msg_list':msg_list})

def index(request):

    return render(request, 'mapping/index.html')

def signup(request):

	return render(request, 'mapping/signup.html')

def success(request):

	if request.method == 'POST':
		email_addr = request.POST.get('email')
		user_name = request.POST.get('username')
		email_list = [email_addr]
		Account.objects.create_user(email_addr, username=user_name)

	return render(request, 'mapping/success.html', {'email_list':email_list})


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


