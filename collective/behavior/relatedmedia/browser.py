from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFCore.interfaces import IFolderish
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets.common import ViewletBase
from plone.dexterity.utils import createContentInContainer
from plone.dexterity.utils import safe_unicode
from plone.dexterity.utils import safe_utf8
from plone.event.interfaces import IOccurrence
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from z3c.relationfield import RelationValue
from zope.intid.interfaces import IIntIds
from zope.component import getUtility

from .behavior import IRelatedMedia

import json


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


class UploaderViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_uploader.pt')

    @property
    def is_admin(self):
        sm = getSecurityManager()
        return sm.checkPermission('Modify portal content', self.context)


class Uploader(BrowserView):

    def __init__(self, context, request):
        super(Uploader, self).__init__(context, request)
        self.intids = getUtility(IIntIds)
        if IOccurrence.providedBy(context):
            # support for related images on event occurrences
            self.context = aq_inner(context).aq_parent

    def __call__(self):
        req_file = self.request.get('file')
        c_type = req_file.headers.get('content-type', '')
        file_data = req_file.read()
        file_name = safe_unicode(req_file.filename)
        media_container = self.get_media_container()
        behavior = IRelatedMedia(self.context)
        if c_type.startswith("image/"):
            blob = NamedBlobImage(data=file_data, filename=file_name)
            img = createContentInContainer(
                media_container, "Image", image=blob)
            # safe image as leadImage if none exists
            if ILeadImage.providedBy(self.context) and \
               ILeadImage(self.context).image is None:
                ILeadImage(self.context).image = blob
            else:
                to_id = self.intids.getId(img)
                imgs = behavior.related_images and \
                    list(behavior.related_images) or []
                imgs.append(RelationValue(to_id))
                behavior.related_images = imgs
        else:
            blob = NamedBlobFile(data=file_data, filename=file_name)
            att = createContentInContainer(media_container, "File", file=blob)
            to_id = self.intids.getId(att)
            atts = behavior.related_attachments and \
                list(behavior.related_attachments) or []
            atts.append(RelationValue(to_id))
            behavior.related_attachments = atts
        return json.dumps(dict(
            status=u"done",
        ))

    def get_media_container(self):
        container = None
        config_media_path = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.media_container_path')
        nav_root = api.portal.get_navigation_root(self.context)
        media_path = "{}{}".format(
            '/'.join(nav_root.getPhysicalPath()), config_media_path)
        try:
            container = self.context.restrictedTraverse(safe_utf8(media_path))
        except:
            # try to create media folder
            container = nav_root
            for f_id in config_media_path.split('/'):
                if not f_id:
                    continue
                if not hasattr(container, f_id):
                    container = createContentInContainer(
                        container, 'Folder', id=f_id, title=f_id,
                        exclude_from_nav=True, checkConstraints=False)
                else:
                    container = container[f_id]
        if container is None:
            container = aq_inner(self.context)
            while not IFolderish.providedBy(container):
                container = aq_parent(container)
        return container
