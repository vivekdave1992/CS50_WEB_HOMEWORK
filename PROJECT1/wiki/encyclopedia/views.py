from django.shortcuts import render
from random import choice
from . import util
from django.http import HttpResponseRedirect,HttpResponse
from django import forms
from django.urls import reverse




class New_entry(forms.Form):
    entry_title= forms.CharField(label="entry_title")
    entry_content = forms.CharField(
        label="entry_content",
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 20 ,'value': 'Default Content'})  # Customize size
    )

# def add_entry(request):
#     if request.method == "POST":
#         form = New_entry(request.POST)
#         if form.is_valid():
#             entry_title = form.cleaned_data["entry_title"]
#             entry_content = form.cleaned_data["entry_content"]
#             util.save_entry(entry_title,entry_content)
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             # this Shows Error when submiting the form if there was one as error message
#             return render(request,"encyclopedia/add.html",{
#                 "form":form
#                 })
    
#     return render(request,"encyclopedia/add.html",{
#             "form":New_entry()
#             })



def add_entry(request):
    if request.method == "POST":
        entry_title = request.POST.get('entry_title')
        entry_content = request.POST.get('entry_content')
        if entry_title and entry_content:
            # Save the new entry
            util.save_entry(entry_title,entry_content)
            return HttpResponseRedirect(reverse("index"))  # Redirect to the index page after saving
        else:
            # Handle case where title or content is missing
            return HttpResponse("Both title and content are required.", status=400)
    
    return render(request, 'encyclopedia/add.html')



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    a = util.get_entry(title)
    if a:
        return render(request, "encyclopedia/entry.html", {
            "entry_title": title,
            "entry_content":a,
        })
    else:
        return render(request,"encyclopedia/error.html")

def random(request):
    e_lists = util.list_entries()
    e_title = choice(e_lists)
    return entry(request, e_title)

def search(request):
    if request.method == "POST":
        search_query = request.POST.get('q', '').lower()  # Rename the search variable
        e_lists = util.list_entries()

        for entry_name in e_lists:  # Rename the loop variable
            if search_query == entry_name.lower():  # Convert each entry to lowercase for comparison
                return entry(request, entry_name)  # Pass the original entry (with correct case) to the view
        
        return render(request, "encyclopedia/error.html")  # If no match found
    else:
        return render(request, "encyclopedia/error.html")
