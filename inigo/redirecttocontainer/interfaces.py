from zope.interface import Interface

class IProductSpecific(Interface):
    pass

class IRedirector(Interface):
    def can_handle():
        pass

    def get_url():
        pass
