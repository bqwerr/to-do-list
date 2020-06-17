from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# rest-framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ToDoListSerializer, ItemSerializer

# Create your views here.

def maintainLists(response): 
	ls = ToDoList.objects
	if response.method == "POST":
		print(response.POST.get("save"), response.POST.get("newItem"))
		if response.POST.get("save") == "save":
			for lst in ls.all():
				for item in lst.item_set.all():
					if response.POST.get("c"+str(item.id)) == "clicked":
						item.complete = True
					else:
						item.complete = False
					item.save()

		elif response.POST.get("newItem"):
			listName = response.POST.get("listName")
			itemName = response.POST.get("itemName")
			if len(itemName) >= 2:
				for lst in ls.all():
					if listName == lst.name:
						lst.item_set.create(text=itemName, complete=False)
						break

	return render(response, "main/list.html", {"ls":ls})

def home(response):
	print(response.user)
	if response.method == "POST":
		if response.POST.get("getList"):
			ls = ToDoList.objects
			return render(response, "main/list.html", {"ls":ls})

		else:
			form = CreateNewList()
			return render(response, "main/create.html", {"form":form})
		
	else:
		return render(response, "main/home.html", {})

def create(response):
	if response.method == "POST":
		form = CreateNewList(response.POST) # NON CUSTOM FORMS
		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()
			response.user.todolist.add(t)
		return render(response, "main/list.html", {"ls":ls})
	else:
		form = CreateNewList()
		return render(response, "main/create.html", {"form":form})

@api_view(['GET'])
def apiOverview(request):
	urls = {
		'List': '/api/task-list/',
		'Detail View': '/api/task-detail/<str:pk>',
		'Create': '/api/item-create/',
		'Update': '/api/item-update/<str:pk>',
		'Delete': '/api/item-delete/<str:pk>'
	}
	return Response(urls)

@api_view(['GET'])
def taskList(request):
	tasks = ToDoList.objects.all()
	serializer = ToDoListSerializer(tasks, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def detailList(request, pk):
	list = ToDoList.objects.get(id=pk)
	items = list.item_set.all()
	serializer =  ItemSerializer(items, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def itemCreate(request):
	serializer =  ItemSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def itemUpdate(request, pk):
	item = Item.objects.get(id=pk)
	serializer =  ItemSerializer(instance=item, data=request.data)
	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['DELETE'])
def itemDelete(request, pk):
	item = Item.objects.get(id=pk)
	item.delete()
	return Response('Deleted')

