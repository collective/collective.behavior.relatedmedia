# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.behavior import IRelatedMedia
from collective.behavior.relatedmedia.interfaces import IRelatedMediaSettings
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.registry.browser import controlpanel
from plone.event.interfaces import IOccurrence
from plone.memoize.instance import memoize


class RelatedImagesViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_images.pt')

    def gallery_css_klass(self):
        css_class = IRelatedMedia(aq_inner(self.context)).gallery_css_class
        if css_class:
            return css_class
        dflt_css_class = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.image_gallery_default_class')
        return dflt_css_class

    @memoize
    def images(self):
        context = aq_inner(self.context)
        if IOccurrence.providedBy(context):
            # support for related images on event occurrences
            context = context.aq_parent
        rm_behavior = IRelatedMedia(context)
        imgs = []
        if rm_behavior.related_media_base_path:
            rm_base = rm_behavior.related_media_base_path.to_object
            imgs = [i.getObject() for i in rm_base.restrictedTraverse('@@contentlisting')(portal_type='Image')]  # noqa
        imgs += [i.to_object for i in rm_behavior.related_images]
        tcap = rm_behavior.show_titles_as_caption
        first_img_scales = None
        further_images = []
        gallery = []

        if rm_behavior.include_leadimage and ILeadImage.providedBy(context):
            first_img_scales = context.restrictedTraverse('@@images')
            first_img_caption = ILeadImage(context).image_caption
            further_images = imgs
        elif len(imgs):
            first_img = imgs[0]
            if first_img:
                first_img_scales = first_img.restrictedTraverse(
                    '@@images')
                first_img_caption = tcap and first_img.Title() or u''
                further_images = imgs[1:]

        if first_img_scales:
            scale = first_img_scales.scale(
                'image', scale=rm_behavior.first_image_scale,
                direction=rm_behavior.first_image_scale_direction and
                'down' or 'thumbnail')
            if scale:
                large_scale_url = first_img_scales.scale(
                    'image', scale='large').url
                gallery.append(dict(
                    url=large_scale_url,
                    tag=scale.tag(
                        title=first_img_caption,
                        alt=first_img_caption,
                    ),
                    caption=tcap and first_img_caption or u'',
                    title=first_img_caption,
                ))

        for img in further_images:
            if img:
                scales = img.restrictedTraverse('@@images')
                scale = scales.scale(
                    'image', scale=rm_behavior.preview_scale,
                    direction=rm_behavior.preview_scale_direction and
                    'down' or 'thumbnail')
                if scale:
                    large_scale_url = scales.scale('image', scale='large').url
                    gallery.append(dict(
                        url=large_scale_url,
                        tag=scale.tag(),
                        caption=tcap and img.Title() or u'',
                        title=img.Title(),
                    ))

        return gallery


class RelatedAttachmentsViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_attachments.pt')

    @property
    def attachments(self):
        context = aq_inner(self.context)
        if IOccurrence.providedBy(context):
            # support for related images on event occurrences
            context = context.aq_parent
        behav = IRelatedMedia(context)
        att = []
        if behav.related_media_base_path:
            rm_base = behav.related_media_base_path.to_object
            att = [f.getObject() for f in rm_base.restrictedTraverse('@@contentlisting')(portal_type='File')]  # noqa
        att += [f.to_object for f in behav.related_attachments]
        return att

    @memoize
    def get_attachments(self):
        _target_blank = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.open_attachment_in_new_window')
        link_target = _target_blank and 'blank' or 'top'
        atts = []
        for att in self.attachments:
            if att:
                atts.append(dict(
                    url=att.absolute_url(),
                    title=att.Title(),
                    size="{:.1f} MB".format(
                        att.file.getSize() / 1024.0 / 1024.0),
                    icon=att.getIcon(),
                    target=link_target,
                ))
        return atts


class RelatedMediaControlPanelForm(controlpanel.RegistryEditForm):
    """ controlpanel """

    schema = IRelatedMediaSettings
    label = _('Related Media Settings')
    schema_prefix = "collective.behavior.relatedmedia"
    control_panel_view = "relatedmedia-controlpanel"


class RelatedMediaControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RelatedMediaControlPanelForm
