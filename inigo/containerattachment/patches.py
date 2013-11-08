from logging import getLogger

logger = getLogger('inigo.containerattachment')

def _patch_redirect():
    # XXX: really ugly patch

    from Products.CMFFormController.Actions.RedirectTo import RedirectTo

    if getattr(RedirectTo, '__inigo_edit_redirect_patched', False):
        return

    logger.info('Patching CMFFormController RedirectTo')

    from Acquisition import aq_parent
    from inigo.containerattachment.interfaces import IRedirector
    from zope.component import queryAdapter

    _getArg = RedirectTo.getArg

    def getArg(self, controller_state):
        url = _getArg(self, controller_state)

        if controller_state.id not in ['atct_edit', 'update_version_on_edit']:
            return url

        context = controller_state.getContext()

        adapters = getAdapters((context,), IRedirector)

        for name, adapter in adapters:
            if adapter.can_handle():
                return adapter.get_url()

        return url

    RedirectTo.getArg = getArg
    RedirectTo.__inigo_edit_redirect_patched = True

_patch_redirect()

