# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.behavior import IRelatedMedia
from collective.behavior.relatedmedia.interfaces import IRelatedMediaSettings
from collective.behavior.relatedmedia.utils import get_media_root
from collective.behavior.relatedmedia.utils import get_related_media
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.registry.browser import controlpanel
from plone.dexterity.utils import createContentInContainer
from plone.memoize.instance import memoize
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import json


class RelatedImagesView(BrowserView):
    def gallery_css_klass(self):
        css_class = IRelatedMedia(aq_inner(self.context)).gallery_css_class
        if css_class:
            return css_class
        dflt_css_class = api.portal.get_registry_record(
            "collective.behavior.relatedmedia.image_gallery_default_class"
        )
        return dflt_css_class

    @memoize
    def images(self):
        context = aq_inner(self.context)
        imgs = get_related_media(context, portal_type="Image")
        rm_behavior = IRelatedMedia(context)
        show_caption = rm_behavior.show_titles_as_caption
        first_img_scales = None
        further_images = []
        gallery = []

        if rm_behavior.include_leadimage and ILeadImage.providedBy(context):
            first_img_scales = context.restrictedTraverse("@@images")
            first_img_caption = ILeadImage(context).image_caption
            further_images = imgs
        elif len(imgs):
            first_img = imgs[0]
            if first_img:
                first_img_scales = first_img.restrictedTraverse("@@images")
                first_img_caption = first_img.Title()
                further_images = imgs[1:]

        if first_img_scales:
            scale = first_img_scales.scale(
                "image",
                scale=rm_behavior.first_image_scale,
                direction=rm_behavior.first_image_scale_direction
                and "down"
                or "thumbnail",
            )  # noqa: E501
            if scale:
                large_scale_url = first_img_scales.scale("image", scale="large").url
                gallery.append(
                    dict(
                        url=large_scale_url,
                        tag=scale.tag(
                            title=first_img_caption,
                            alt=first_img_caption,
                        ),
                        caption=first_img_caption,
                        show_caption=show_caption,
                        title=first_img_caption,
                    )
                )

        for img in further_images:
            if img:
                scales = img.restrictedTraverse("@@images")
                scale = scales.scale(
                    "image",
                    scale=rm_behavior.preview_scale,
                    direction=rm_behavior.preview_scale_direction
                    and "down"
                    or "thumbnail",
                )  # noqa: E501
                if scale:
                    large_scale_url = scales.scale("image", scale="large").url
                    gallery.append(
                        dict(
                            url=large_scale_url,
                            tag=scale.tag(),
                            caption=img.Title(),
                            show_caption=show_caption,
                            title=img.Title(),
                        )
                    )

        return gallery


class RelatedAttachmentsView(BrowserView):
    @property
    def attachments(self):
        context = aq_inner(self.context)
        return get_related_media(context, portal_type="File")

    @memoize
    def get_attachments(self):
        _target_blank = api.portal.get_registry_record(
            "collective.behavior.relatedmedia.open_attachment_in_new_window"
        )
        link_target = _target_blank and "blank" or "top"
        atts = []
        for att in self.attachments:
            if att:
                download_url = u"{}/@@download/file/{}".format(
                    att.absolute_url(), att.file.filename
                )  # noqa
                atts.append(
                    dict(
                        url=download_url,
                        title=att.Title(),
                        size="{:.1f} MB".format(att.file.getSize() / 1024.0 / 1024.0),
                        icon=att.getIcon(),
                        target=link_target,
                    )
                )
        return atts


class RelatedMediaControlPanelForm(controlpanel.RegistryEditForm):
    """ controlpanel """

    schema = IRelatedMediaSettings
    label = _("Related Media Settings")
    schema_prefix = "collective.behavior.relatedmedia"
    control_panel_view = "relatedmedia-controlpanel"


class RelatedMediaControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RelatedMediaControlPanelForm


class Uploader(BrowserView):
    def __call__(self):
        req_file = self.request.get("file")
        c_type = req_file.headers.get("content-type", "")
        file_data = req_file.read()
        file_name = safe_unicode(req_file.filename)
        media_container = get_media_root(self.context)
        behavior = IRelatedMedia(self.context)
        intids = getUtility(IIntIds)

        if c_type.startswith("image/"):
            blob = NamedBlobImage(data=file_data, filename=file_name)
            img = createContentInContainer(media_container, "Image", image=blob)
            # safe image as leadImage if none exists
            if (
                ILeadImage.providedBy(self.context)
                and ILeadImage(self.context).image is None
            ):
                ILeadImage(self.context).image = blob
            else:
                to_id = intids.getId(img)
                imgs = behavior.related_images and list(behavior.related_images) or []
                imgs.append(RelationValue(to_id))
                behavior.related_images = imgs
        else:
            blob = NamedBlobFile(data=file_data, filename=file_name)
            att = createContentInContainer(media_container, "File", file=blob)
            to_id = intids.getId(att)
            atts = (
                behavior.related_attachments
                and list(behavior.related_attachments)
                or []
            )
            atts.append(RelationValue(to_id))
            behavior.related_attachments = atts

        return json.dumps(
            dict(
                status=u"done",
            )
        )
