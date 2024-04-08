from Acquisition import aq_inner
from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.behavior import IGalleryEditSchema
from collective.behavior.relatedmedia.behavior import IRelatedMediaBehavior
from collective.behavior.relatedmedia.events import update_leadimage
from collective.behavior.relatedmedia.interfaces import IRelatedMediaSettings
from collective.behavior.relatedmedia.utils import get_media_root
from collective.behavior.relatedmedia.utils import get_related_media
from operator import itemgetter
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.registry.browser import controlpanel
from plone.base.utils import human_readable_size
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.utils import createContentInContainer
from plone.event.interfaces import IOccurrence
from plone.memoize.instance import memoize
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.z3cform import layout
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import json


class RelatedBaseView(BrowserView):
    def __init__(self, context, request):
        super().__init__(context, request)

        if IOccurrence.providedBy(self.context):
            self.context = self.context.aq_parent

    @property
    def behavior(self):
        return IRelatedMediaBehavior(aq_inner(self.context), None)

    @property
    def can_upload(self):
        return IRelatedMediaBehavior.providedBy(
            self.context
        ) and api.user.has_permission("Modify portal content", obj=self.context)


class RelatedImagesView(RelatedBaseView):
    def gallery_css_klass(self):
        rm_behavior = self.behavior

        if not rm_behavior:
            return

        css_class = rm_behavior.gallery_css_class

        if css_class:
            return css_class

        dflt_css_class = api.portal.get_registry_record(
            "collective.behavior.relatedmedia.image_gallery_default_class"
        )
        return dflt_css_class

    @property
    def show_images_viewlet(self):
        return self.request.get("ajax_load") or (
            self.behavior and self.behavior.show_images_viewlet
        )

    def can_edit(self):
        return api.user.has_permission("Modify portal content")

    # @memoize
    def images(self):
        rm_behavior = self.behavior

        if not rm_behavior:
            return

        context = aq_inner(self.context)
        imgs = get_related_media(context, portal_type="Image")
        show_caption = rm_behavior.show_titles_as_caption
        first_img_title = ""
        first_img_scales = None
        first_img_description = ""
        first_img_uuid = ""
        further_images = []
        gallery = {}

        if rm_behavior.include_leadimage and ILeadImage.providedBy(context):
            # include leadimage if no related images are defined
            first_img_scales = context.restrictedTraverse("@@images")
            first_img_title = ILeadImage(context).image_caption
            first_img_uuid = context.UID()
            further_images = imgs

        if not first_img_scales and len(imgs):
            first_img = imgs[0]
            if first_img:
                first_img_scales = first_img.restrictedTraverse("@@images")
                first_img_title = first_img.Title()
                first_img_description = first_img.Description()
                first_img_uuid = first_img.UID()
                further_images = imgs[1:]

        if first_img_scales:
            scale = first_img_scales.scale(
                "image",
                scale=rm_behavior.first_image_scale,
                direction=rm_behavior.first_image_scale_direction
                and "down"
                or "thumbnail",
            )
            if scale:
                large_scale_url = first_img_scales.scale("image", scale="large").url
                gallery[first_img_uuid] = dict(
                    url=large_scale_url,
                    tag=scale.tag(
                        title=first_img_title,
                        alt=first_img_title,
                        css_class="img-fluid",
                    ),
                    caption=first_img_title,
                    show_caption=show_caption,
                    title=first_img_title,
                    description=first_img_description,
                    uuid=first_img_uuid,
                    order=0,
                )

        for idx, img in enumerate(further_images, 1):
            if img:
                scales = img.restrictedTraverse("@@images")
                scale = scales.scale(
                    "image",
                    scale=rm_behavior.preview_scale,
                    direction=rm_behavior.preview_scale_direction
                    and "down"
                    or "thumbnail",
                )
                uuid = img.UID()
                if scale:
                    large_scale_url = scales.scale("image", scale="large").url
                    gallery[uuid] = dict(
                        url=large_scale_url,
                        tag=scale.tag(css_class="img-fluid"),
                        caption=img.Title(),
                        show_caption=show_caption,
                        title=img.Title(),
                        description=img.Description(),
                        uuid=uuid,
                        order=idx,
                    )

        # pattern feature to filter special uuids to display with ?uuids=uuid1,uuid2,...
        uuid_filter = self.request.get("uuids")

        if uuid_filter and self.__name__ != "gallery-editor":
            # provide the order of given uuids
            ret = []
            for uuid in uuid_filter.split(","):
                if uuid in gallery:
                    ret.append(gallery[uuid])
            return ret

        return sorted(gallery.values(), key=itemgetter("order"))


class GalleryEditForm(DefaultEditForm):
    schema = IGalleryEditSchema

    @property
    def additionalSchemata(self):
        return ()


GalleryEditView = layout.wrap_form(GalleryEditForm)


class RelatedAttachmentsView(RelatedBaseView):
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
                _file = getattr(att, "file", None)
                download_url = (
                    "{}/@@download/file/{}".format(
                        att.absolute_url(), att.file.filename
                    )
                    if _file
                    else "#"
                )
                atts.append(
                    dict(
                        url=download_url,
                        title=att.Title(),
                        size=(
                            human_readable_size(att.file.getSize())
                            if _file
                            else "missing"
                        ),
                        mimetype=att.content_type() or "application",
                        target=link_target,
                    )
                )
        return atts


class RelatedMediaControlPanelForm(controlpanel.RegistryEditForm):
    """controlpanel"""

    schema = IRelatedMediaSettings
    label = _("Related Media Settings")
    schema_prefix = "collective.behavior.relatedmedia"
    control_panel_view = "relatedmedia-controlpanel"


class RelatedMediaControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RelatedMediaControlPanelForm


class Uploader(RelatedBaseView):
    def __call__(self):
        req_file = self.request.get("file")
        c_type = req_file.headers.get("content-type", "")
        file_data = req_file.read()
        file_name = safe_unicode(req_file.filename)
        media_container = get_media_root(self.context)
        behavior = self.behavior

        if not behavior:
            return json.dumps(
                dict(
                    status="error",
                    message="IRelatedMediaBehavior behavior not activated for this context",
                )
            )

        intids = getUtility(IIntIds)
        __traceback_info__ = media_container

        if c_type.startswith("image/"):
            blob = NamedBlobImage(data=file_data, filename=file_name)
            img = createContentInContainer(media_container, "Image", image=blob)
            to_id = intids.getId(img)
            imgs = behavior.related_images and list(behavior.related_images) or []
            imgs.append(RelationValue(to_id))
            behavior.related_images = imgs
            update_leadimage(self.context, None)
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
                status="done",
            )
        )


class UploadViewlet(ViewletBase):
    def render(self):
        if not IViewView.providedBy(self.view):
            return ""
        return super().render()
