from http.client import HTTPResponse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import encyclopedia
import random

# Create new page form
class NewPageForm(forms.Form):
    title = forms.CharField(label="New Page Title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view(request, title):
    page = util.convert(title)
    if page == None:
        return render(request, "encyclopedia/error.html", {
            "error" : "The page you are trying to find does not exist"
        })
    else:
        return render(request, "encyclopedia/view.html", {
            "content" : page,
            "title" : title
        })

def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        page = util.convert(query)
        if page is not None:
            return render(request, "encyclopedia/view.html", {
            "content" : page,
            "title" : query
        })
        else:
            docs = []
            allEntries = util.list_entries()
            for entry in allEntries:
                if query.lower() in entry.lower():
                    docs.append(entry)
            return render(request, "encyclopedia/search.html", {
                "docs" : docs
            })

def add(request):
    if request.method == "POST":

        # Get form from submission
        form = NewPageForm(request.POST)

        # Check form is valid
        if form.is_valid():

            # See if page already exists
            allEntries = util.list_entries()
            title = form.cleaned_data["title"] 
            content = form.cleaned_data["content"]
            for entry in allEntries:
                if title == entry:
                    return render(request, "encyclopedia/error.html", {
                        "error" : "The page you tried to create already exists"
                    })
            
            # Save form data to a new page
            util.save_entry(title, content)

            # Go to new page
            return render(request, "encyclopedia/view.html", {
                "title" : title,
                "content" : content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error" : "Invalid Form"
            })

    else:
        return render(request, "encyclopedia/add.html", {
            "form" : NewPageForm()
        })

def edit(request):
    if request.method == "POST":
        title = request.POST["view_title"]
        content = util.get_entry(title)
        form = NewPageForm(initial={'title': title, 'content': content})
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "form" : form,
        })

def change(request):
    if request.method == 'POST':

        # Get form from submission
        form = NewPageForm(request.POST)

        # Check form is valid
        if form.is_valid():
            title = form.cleaned_data["title"] 
            content = form.cleaned_data["content"]

            # Save form data to a new page
            util.save_entry(title, content)

            # Go to new page
            content = util.convert(title)
            return render(request, "encyclopedia/view.html", {
                "title" : title,
                "content" : content
            })
        
        else:
            return render(request, "encyclopedia/error.html", {
                "error" : "Invalid Form"
            })

def get_random(request):
    pages = util.list_entries()
    random_page = random.choice(pages)
    content = util.convert(random_page)
    return render(request, "encyclopedia/view.html", {
        "title" : random_page,
        "content" : content
    })