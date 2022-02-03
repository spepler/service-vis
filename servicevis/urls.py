from django.conf.urls import include, url

from views import *

urlpatterns = [
     url(r'^show/(?P<graph_id>\d+)/gv$', gv),
     url(r'^show/(?P<graph_id>\d+)/svg$', svg),
     url(r'^trace/(?P<service_id>\d+)$', trace_gv),
     url(r'^trace/(?P<service_id>\d+)/svg$', trace_svg),
     url(r'^linker/(?P<service_id>\d+)$', linker),
     url(r'^add/(?P<graph_id>\d+)$', addnode),
#     url(r'^project/(?P<project_id>\d+)/adddataproduct$', add_dataproduct),
#     url(r'^project/(?P<project_id>\d+)/show$', showproject),
#     url(r'^myprojects$', my_projects),
#     url(r'^datamad_update$', datamad_update),
#     url(r'^projectsvis$', projects_vis),
#     url(r'^projectsbyperson$', projects_by_person),
#     url(r'^grant/(?P<id>\d+)/scrape$', gotw_scrape),
#     url(r'^grant/(?P<id>\d+)/link$', link_grant_to_project),
#     url(r'^grant/(?P<id>\d+)/project_from_rss_export$', make_project_from_rss_export),
#     url(r'^vmreg$', vmreg),
]