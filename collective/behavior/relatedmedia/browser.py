from Acquisition import aq_inner
from collective.behavior.relatedmedia import messageFactory as _
from collective.behavior.relatedmedia.behavior import IRelatedMediaBehavior
from collective.behavior.relatedmedia.events import update_leadimage
from collective.behavior.relatedmedia.interfaces import IRelatedMediaSettings
from collective.behavior.relatedmedia.utils import get_media_root
from collective.behavior.relatedmedia.utils import get_related_media
from operator import itemgetter
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.registry.browser import controlpanel
from plone.base.utils import human_readable_size
from plone.dexterity.utils import createContentInContainer
from plone.event.interfaces import IOccurrence
from plone.memoize.instance import memoize
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
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
        css_class = []

        if self.request.get("showGallery"):
            css_class.append("related-images-slider")

        rm_behavior = self.behavior

        if rm_behavior:
            css_class.append(rm_behavior.gallery_css_class)
        else:
            dflt_css_class = api.portal.get_registry_record(
                "collective.behavior.relatedmedia.image_gallery_default_class"
            )
            css_class.append(dflt_css_class)

        return " ".join(css_class)

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
        large_scale = getattr(rm_behavior, "large_image_scale", "large")
        gallery = {}

        def add_to_gallery(obj, **kw):
            if obj is None:
                return
            first = kw.get("first", False)
            scales = obj.restrictedTraverse("@@images")
            if obj.image is None or scales is None:
                return
            filename = obj.image.filename
            if filename in gallery:
                # deduplicate leadimage and related images
                return
            scale = scales.scale(
                "image",
                scale=(
                    rm_behavior.first_image_scale
                    if first
                    else rm_behavior.preview_scale
                ),
                mode=(
                    "cover"
                    if (
                        rm_behavior.first_image_scale_direction
                        if first
                        else rm_behavior.preview_scale_direction
                    )
                    else "contain"
                ),
            )
            uuid = obj.UID()
            title = kw.get("title", obj.Title())
            gallery[filename] = dict(
                url=scales.scale("image", scale=large_scale).url,
                tag=scale.tag(
                    title=title,
                    alt=title,
                    css_class="img-fluid",
                ),
                show_caption=show_caption,
                caption=title,
                title=title,
                description=kw.get("description", obj.Description()),
                uuid=uuid,
                order=kw.get("order", 0),
            )

        if ILeadImage.providedBy(context):
            # include leadimage
            add_to_gallery(
                context,
                first=True,
                title=ILeadImage(context).image_caption,
                description="",
            )
        elif len(imgs):
            # no leadimage there but related images
            add_to_gallery(imgs[0], first=True)

        for idx, img in enumerate(imgs, 1):
            add_to_gallery(img, order=idx)

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
                        base_url=att.absolute_url(),
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
