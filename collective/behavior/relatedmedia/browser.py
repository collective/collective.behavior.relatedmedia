# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.behavior.relatedmedia.behavior import IRelatedMedia
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.registry.browser import controlpanel
from plone.event.interfaces import IOccurrence


class RelatedImagesViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_images.pt')

    def gallery_css_klass(self):
        css_class = IRelatedMedia(aq_inner(self.context)).gallery_css_class
        if css_class:
            return css_class
        dflt_css_class = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.image_gallery_default_class')
        return dflt_css_class

    def images(self):
        context = aq_inner(self.context)
        if IOccurrence.providedBy(context):
            # support for related images on event occurrences
            context = context.aq_parent
        rm_behavior = IRelatedMedia(context)
        imgs = rm_behavior.related_images or []
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
            first_img_obj = first_img.to_object
            if first_img_obj:
                first_img_scales = first_img_obj.restrictedTraverse(
                    '@@images')
                first_img_caption = tcap and first_img_obj.Title() or u''
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
            img_obj = img.to_object
            if img_obj:
                scales = img_obj.restrictedTraverse('@@images')
                scale = scales.scale(
                    'image', scale=rm_behavior.preview_scale,
                    direction=rm_behavior.preview_scale_direction and
                    'down' or 'thumbnail')
                if scale:
                    large_scale_url = scales.scale('image', scale='large').url
                    gallery.append(dict(
                        url=large_scale_url,
                        tag=scale.tag(),
                        caption=tcap and img_obj.Title() or u'',
                        title=img_obj.Title(),
                    ))

        return gallery


class RelatedAttachmentsViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_attachments.pt')

    @property
    def available(self):
        att = IRelatedMedia(aq_inner(self.context)).related_attachments or []
        return len(att)

    def attachments(self):
        context = aq_inner(self.context)
        if IOccurrence.providedBy(context):
            # support for related images on event occurrences
            context = context.aq_parent
        atts = IRelatedMedia(context).related_attachments
        _target_blank = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.open_attachment_in_new_window')
        link_target = _target_blank and 'blank' or 'top'
        for att in atts:
            att_obj = att.to_object
            if att_obj:
                yield dict(
                    url=att_obj.absolute_url(),
                    title=att_obj.Title(),
                    size="{:.1f} MB".format(
                        att_obj.file.getSize() / 1024.0 / 1024.0),
                    icon=att_obj.getIcon(),
                    target=link_target,
                )


class RelatedMediaControlPanel(controlpanel.RegistryEditForm):
    """ TODO: configlet """
