from AccessControl import getSecurityManager
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.interfaces import IFolderish
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.app.layout.viewlets.common import ViewletBase
from plone.dexterity.utils import safe_unicode, safe_utf8, \
    createContentInContainer
from plone.namedfile.file import NamedBlobImage, NamedBlobFile
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility, getMultiAdapter

from .behavior import IRelatedMedia

import transaction


class RelatedImagesViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_images.pt')

    def gallery_css_klass(self):
        return IRelatedMedia(aq_inner(self.context)).gallery_css_class

    def images(self):
        context = aq_inner(self.context)
        rm_behavior = IRelatedMedia(context)
        imgs = rm_behavior.related_images
        tcap = rm_behavior.show_titles_as_caption
        first_img_scales = None
        gallery = []

        if rm_behavior.include_leadimage and ILeadImage.providedBy(context):
            first_img_scales = context.restrictedTraverse('@@images')
            first_img_caption = ILeadImage(context).image_caption
        elif len(imgs):
            first_img = imgs.pop(0)
            first_img_obj = first_img.to_object
            if first_img_obj:
                first_img_scales = first_img_obj.restrictedTraverse(
                    '@@images')
                first_img_caption = tcap and first_img_obj.Title() or u''

        if first_img_scales:
            scale = first_img_scales.scale('image',
                scale=rm_behavior.first_image_scale,
                direction=rm_behavior.first_image_scale_direction and 'down' \
                or 'thumbnail')
            if scale:
                large_scale_url = first_img_scales.scale('image',
                    scale='large').url
                gallery.append(dict(
                    url=large_scale_url,
                    tag=scale.tag(),
                    title=first_img_caption))

        for img in imgs:
            img_obj = img.to_object
            if img_obj:
                scales = img_obj.restrictedTraverse('@@images')
                scale = scales.scale('image', scale=rm_behavior.preview_scale,
                    direction=rm_behavior.preview_scale_direction and 'down' \
                    or 'thumbnail')
                if scale:
                    large_scale_url = scales.scale('image', scale='large').url
                    gallery.append(dict(
                        url=large_scale_url,
                        tag=scale.tag(),
                        title=tcap and img_obj.Title() or u'',
                    ))

        return gallery


class RelatedAttachmentsViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_attachments.pt')

    @property
    def available(self):
        return len(IRelatedMedia(aq_inner(self.context)).related_attachments)

    def attachments(self):
        atts = IRelatedMedia(aq_inner(self.context)).related_attachments
        for att in atts:
            att_obj = att.to_object
            if att_obj:
                yield dict(
                    url=att_obj.absolute_url(),
                    title=att_obj.Title(),
                    size="{:.1f} MB".format(
                        att_obj.file.getSize() / 1024.0 / 1024.0),
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

    def __call__(self):
        req_file = self.request.get('file')
        c_type = req_file.headers.get('content-type', '')
        file_data = req_file.read()
        file_name = safe_unicode(req_file.filename)
        media_container = self.get_media_container()
        behavior = IRelatedMedia(self.context)
        if c_type.startswith("image/"):
            blob = NamedBlobImage(data=file_data, filename=file_name)
            img = createContentInContainer(media_container, "Image",
                image=blob)
            # safe image as leadImage if none exists
            if ILeadImage.providedBy(self.context) and \
            ILeadImage(self.context).image is None:
                ILeadImage(self.context).image = blob
            else:
                transaction.commit()
                to_id = self.intids.getId(img)
                imgs = list(behavior.related_images)
                imgs.append(RelationValue(to_id))
                behavior.related_images = imgs
        else:
            blob = NamedBlobFile(data=file_data, filename=file_name)
            att = createContentInContainer(media_container, "File", file=blob)
            to_id = self.intids.getId(att)
            atts = list(behavior.related_attachments)
            atts.append(RelationValue(to_id))
            behavior.related_attachments = atts
        return u"done"

    def get_media_container(self):
        container = None
        config_media_path = api.portal.get_registry_record(
            'collective.behavior.relatedmedia.media_container_path')
        pstate = getMultiAdapter((self.context, self.request),
            name='plone_portal_state')
        nav_root = pstate.navigation_root()
        media_path = "{}{}".format('/'.join(nav_root.getPhysicalPath()),
            config_media_path)
        try:
            container = self.context.restrictedTraverse(safe_utf8(media_path))
        except:
            # try to create media folder
            container = nav_root
            for f_id in config_media_path.split('/'):
                if not f_id:
                    continue
                if not hasattr(container, f_id):
                    container = createContentInContainer(container, 'Folder',
                        id=f_id, title=f_id, exclude_from_nav=True,
                        checkConstraints=False)
                else:
                    container = container[f_id]
        if container is None:
            container = aq_inner(self.context)
            while not IFolderish.providedBy(container):
                container = aq_parent(container)
        return container
