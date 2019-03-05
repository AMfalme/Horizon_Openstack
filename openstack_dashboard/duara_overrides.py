from django.utils.translation import ugettext_lazy as _

import horizon


panels_to_remove = [
	'overview',
	'routers',
	'networks',
	'cgroups',
	'cg_snapshots',
	'network_topology',
	'containers',

	]
settings = horizon.get_dashboard('settings')
settings.name = _("Account")
project = horizon.get_dashboard('project')
project.name = _('Dashboard')

# remove user settings
x1 = settings.get_panel("user")
settings.unregister(x1.__class__)
# settings.default_panel = ""
def remove_panels_from_dashboard(list):
	project.default_panel = "instances"
	for panel in list:
		x = project.get_panel(panel)
		project.unregister(x.__class__)
remove_panels_from_dashboard(panels_to_remove)


