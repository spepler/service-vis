from django.db import models

# Create your models here.



class Graph(models.Model):
    name = models.CharField(max_length=256, help_text="Name of service graph")

    def services(self):
        return Service.objects.filter(graph=self)
        

    def __unicode__(self):
        return u'%s' % self.name
        


class Service(models.Model):
    name = models.CharField(max_length=256, help_text="Name of service component")
    url = models.CharField(max_length=256, blank=True, null=True, help_text="URL of documentation")
    type = models.CharField(max_length=200, blank=True, null=True,
            choices=(("actor","actor"),
                 ("interface","interface"),
                 ("businessservice","businessservice"),
                 ("BusinessProcess","BusinessProcess"),
                 ("ApplicationService","ApplicationService"),
                 ("Application","Application"),
                 ("ApplicationData","ApplicationData"),
                 ("Infrastructure","Infrastructure")))
    level = models.CharField(max_length=200, default="implied",
            choices=( ("alpha","alpha"),
                 ("beta","beta"),
                 ("live","live"),
                 ("deprecated","deprecated"),
                 ("implied","implied")))
    graph = models.ForeignKey(Graph, help_text="Graph to which the service belongs")

    def links(self):
        return Link.objects.filter(service=self)        

    def supporting(self):
        return Link.objects.filter(dependency=self)

    def __unicode__(self):
        return u'%s' % self.name

    def style(self):
        if self.type == "actor": style = 'shape=oval, fillcolor=pink, color=pink' 
        elif self.type == "interface": style = 'shape=box, fillcolor=gray, color=gray'  
        elif self.type == "businessservice": style = 'shape=oval, fillcolor=blue, color=blue' 
        elif self.type == "ApplicationService": style = 'shape=box,  fillcolor=green, color=green' 
        elif self.type == "Application": style = 'shape=component, fillcolor=purple, color=purple' 
        elif self.type == "ApplicationData": style = 'shape=note, fillcolor=orange, color=orange' 
        elif self.type == "Infrastructure": style = 'shape=box, fillcolor=black, color=black' 
        else: style = 'color=green, shape=egg'
        if self.level == "alpha": style += ", style=dotted"
        elif self.level == "beta": style += ", style=dashed"
        elif self.level == "live": style += ", style=bold"
        elif self.level == "deprecated": style += ", style=dotted"
        else: pass
        if self.url: style += ", fontcolor=black"
        else: style += ", fontcolor=lightgray"
        return style

    def edit_gv(self):
        return u'"%s" [%s, URL="/services/linker/%s"];' % (self.name, self.style(), self.pk)

    def doc_gv(self):
        return u'"%s" [%s, URL="%s"];' % (self.name, self.style(), self.url)

    def trace_gv(self):
        return u'"%s" [%s, URL="/services/trace/%s/svg"];' % (self.name, self.style(), self.pk)

    def trace_dependents(self, links, services):
        if self in services: return (links, services)   # been here before
        services.append(self)
        my_links =self.links()
        for l in my_links:
            links.append(l)
            (links, services) = l.dependency.trace_dependents(links, services)
        return (links, services)    

class Link(models.Model):
    service = models.ForeignKey(Service, related_name="services", help_text="Service that has a dependency")
    dependency = models.ForeignKey(Service, related_name="dependents", help_text="service that is depended on")

    def edit_gv(self):
        return u'"%s" -> "%s" [color=blue, URL="/admin/servicevis/link/%s"];' % (self.service, self.dependency, self.pk)

    def doc_gv(self):
        return u'"%s" -> "%s" [color=black];' % (self.service, self.dependency)

    def trace_gv(self):
        return u'"%s" -> "%s" [color=red];' % (self.service, self.dependency)



    def __unicode__(self):
        return u'%s -> %s' % (self.service, self.dependency)

