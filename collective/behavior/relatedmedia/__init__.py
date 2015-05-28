from zope.i18nmessageid.message import MessageFactory

messageFactory = MessageFactory('collective.behavior.relatedmedia')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
