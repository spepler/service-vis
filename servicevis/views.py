from django.shortcuts import render, redirect, render_to_response, get_object_or_404

from subprocess import *
from servicevis.models import *


def vis(request):
    graph = Graph.objects.all()
    graph = graph[0]
    return render_to_response('servicevis/vis.html', {"graph" : graph})

def gv(request, graph_id, mode="doc"):
    mode = request.GET.get('mode', mode) 

    graph = Graph.objects.filter(pk=graph_id)
    graph = graph[0]
    services = graph.services()

    # find services outside of graph that are depended on.
    requires = {}   
    for s in services:
        print s
        links = s.links()
        for l in links:
            if l.dependency.graph != graph:
                if not requires.has_key(l.dependency.graph): requires[l.dependency.graph] = [l.dependency]
                else: requires[l.dependency.graph].append(l.dependency)

    # find services outside of graph that this graph is supporting.
    extralinks = []
    for s in services:  
        print s
        links = s.supporting()
        print "supporting", links
        for l in links:
            if l.service.graph != graph:
                if not requires.has_key(l.service.graph): requires[l.service.graph] = [l.service]
                else: requires[l.service.graph].append(l.service)
                extralinks.append(l)        

    return render_to_response('servicevis/servicegraph.gv', {"graph" : graph, "requires":requires, "extralinks":extralinks, 'mode':mode})

   
def svg(request, graph_id, mode="doc"):
    mode = request.GET.get('mode', 'doc') 
    x = gv(request, graph_id, mode=mode)
    p = Popen("dot -Tsvg", shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    p.stdin.write(x.content)
    p.stdin.close()
    svg = p.stdout.read()
    return render_to_response('servicevis/showgraph.html',  {"graph" : graph_id, "svg":svg, "mode":mode})




def trace_gv(request, service_id):
    services = []
    service = Service.objects.filter(pk=service_id)[0]
    (links, services) = service.trace_dependents([],[])

    return render_to_response('servicevis/servicetrace.gv', {"services" : services, "links":links})

def trace_svg(request, service_id):
    x = trace_gv(request, service_id)
    service = Service.objects.filter(pk=service_id)[0]
    p = Popen("dot -Tsvg", shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    p.stdin.write(x.content)
    p.stdin.close()
    svg = p.stdout.read()
    return render_to_response('servicevis/showgraph.html',  {"graph" : service.graph.pk, "svg":svg, "mode":"trace"})
   
def linker(request, service_id):
    delete = request.GET.get('del', '') 
    add = request.GET.get('add', '') 

    service = Service.objects.filter(pk=service_id)[0]
    current_links = service.links()

    # if delete set then remove the link
    if delete: 
        l = Link.objects.get(pk=int(delete))
        l.delete()

    # if add set then make a new link
    if add: 
        l = Link(service=service, dependency=Service.objects.get(pk=int(add)))
        l.save()

    current_links = service.links()   
    
    # limit the things that can be linked to     
    if service.type == "actor": allowed_types = ("interface", "businessservice" )    
    elif service.type == "interface": allowed_types = ("businessservice",)    
    elif service.type == "businessservice": allowed_types = ("ApplicationService","businessservice")    
    elif service.type == "ApplicationService": allowed_types = ("Application","ApplicationService","ApplicationData", "Infrastructure")    
    elif service.type == "Application": allowed_types = ("Application", "ApplicationData", "Infrastructure")    
    elif service.type == "ApplicationData": allowed_types = ("Infrastructure",)    
    elif service.type == "Infrastructure": allowed_types = []
    else: allowed_types = []
    
    # make a list of service that can be linked to  
    services = Service.objects.all()
    choices = []
    for s in services:
        if s.type not in allowed_types: continue
        for l in current_links:
            if l.dependency == s: continue
        if s == service: continue
        choices.append(s)
    return render_to_response('servicevis/linker.html',  {"service" : service, "current_links":current_links, "choices":choices})
 
def addnode(request, graph_id):
    graph = Graph.objects.get(pk=graph_id)
    s=Service(graph=graph, name="NEW SERVICE")
    s.save()
    return redirect(request.META['HTTP_REFERER'])

           
    
    
