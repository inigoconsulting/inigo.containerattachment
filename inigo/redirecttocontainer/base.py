from five import grok
from Acquisition import aq_parent, aq_chain
from inigo.redirecttocontainer.interfaces import IRedirector

class BaseRedirector(grok.Adapter):
    grok.baseclass()
    grok.implements(IRedirector)

    container_iface = None
    direct_parent = False

    def __init__(self, context):
        self.context = context

    def _get_parent(self):
        if self.direct_parent:
            parent = aq_parent(self.context)
            if self.container_iface.providedBy(parent):
                return parent
        else:
            for parent in aq_chain(self.context):
                if self.container_iface.providedBy(parent):
                    return parent
        return None

    def can_handle(self):
        return bool(self._get_parent())

    def get_url(self):
        return self._get_parent().absolute_url()
