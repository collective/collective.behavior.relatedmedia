# -*- coding: utf-8 -*-
from collective.behavior.relatedmedia import messageFactory as _
from z3c.form.interfaces import ITextWidget
from zope import schema
from zope.interface import Interface


class IRelatedMediaWidget(ITextWidget):
    """ marker for widget """


class IRelatedMediaSettings(Interface):
    """ various settings """

    media_container_path = schema.TextLine(
        title=_(u'Media Container'),
        description=_('Traversable path to media container. '
                      'We respect IPloneSiteRoot, INavigationRoot '
                      'and IChildSite (lineage) as "/"'),
        required=True,
    )

    media_container_in_assets_folder = schema.Bool(
        title=_('Create Media Container in Assets Folder '
                '(language independent)?'),
        description=_('If True, the Media Container path defined above is '
                      'generated in the language independend Assets folder. '
                      'This requires plone.app.multilingual.'),
        default=False,
        required=False,
    )

    image_gallery_cssclass = schema.List(
        title=_('Gallery CSS classes'),
        value_type=schema.TextLine(title='CSS Class'),
        required=False,
    )

    image_gallery_default_class = schema.TextLine(
        title=_('Default gallery class for new articles'),
        required=True,
    )

    image_gallery_default_preview_scale_direction = schema.Bool(
        title=_('Default setting for cropping gallery images'),
        default=False,
        required=False,
    )

    open_attachment_in_new_window = schema.Bool(
        title=_('Open Attachment links in new window'),
        default=True,
        required=False,
    )
