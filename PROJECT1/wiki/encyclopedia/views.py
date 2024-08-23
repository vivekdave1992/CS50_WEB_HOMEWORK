from django.shortcuts import render
from random import choice
from . import util


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