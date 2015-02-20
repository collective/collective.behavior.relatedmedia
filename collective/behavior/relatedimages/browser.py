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
from plone.namedfile.file import NamedBlobImage
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.component.hooks import getSite

from .behavior import IRelatedImages


class RelatedImagesViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet.pt')

    @property
    def is_admin(self):
        sm = getSecurityManager()
        return sm.checkPermission('Modify portal content', self.context)

    def images(self):
        context = aq_inner(self.context)
        imgs = IRelatedImages(aq_inner(context)).related_images
        include_leadimage = api.portal.get_registry_record(
            'collective.behavior.relatedimages.include_leadimage')
        first_img_scale = api.portal.get_registry_record(
            'collective.behavior.relatedimages.first_image_scale')
        img_scale = api.portal.get_registry_record(
            'collective.behavior.relatedimages.preview_scale')
        img_scale_dir = api.portal.get_registry_record(
            'collective.behavior.relatedimages.preview_scale_direction')
        gallery = []

        if include_leadimage:
            first_img_scales = context.restrictedTraverse('@@images')
        elif len(imgs):
            first_img = imgs.pop(0)
            first_img_scales = first_img.to_object.restrictedTraverse(
                '@@images')
        else:
            first_img_scales = None

        if first_img_scales:
            scale = first_img_scales.scale('image', scale=first_img_scale,
                direction=img_scale_dir)
            if scale:
                large_scale_url = first_img_scales.scale('image',
                    scale='large').url
                gallery.append(dict(url=large_scale_url, tag=scale.tag()))

        for img in imgs:
            img_obj = img.to_object
            if img_obj:
                scales = img_obj.restrictedTraverse('@@images')
                scale = scales.scale('image', scale=img_scale,
                    direction=img_scale_dir)
                if scale:
                    large_scale_url = scales.scale('image', scale='large').url
                    gallery.append(dict(url=large_scale_url, tag=scale.tag()))

        return gallery


class Uploader(BrowserView):

    def __init__(self, context, request):
        super(Uploader, self).__init__(context, request)
        self.intids = getUtility(IIntIds)

    def __call__(self):
        req_file = self.request.get('file')
        media_container = self.get_media_container()
        if req_file.headers.get('content-type', '').startswith("image/"):
            blob = NamedBlobImage(data=req_file.read(),
                filename=safe_unicode(req_file.filename))
            img = createContentInContainer(media_container, "Image",
                image=blob)
            # safe image as leadImage if none exists
            if ILeadImage.providedBy(self.context) and \
            ILeadImage(self.context).image is None:
                ILeadImage(self.context).image = blob
            else:
                to_id = self.intids.getId(img)
                imgs = IRelatedImages(self.context).related_images
                imgs.append(RelationValue(to_id))
                IRelatedImages(self.context).related_images = imgs
        return u"done"

    def get_media_container(self):
        container = None
        try:
            container_path = api.portal.get_registry_record(
                'collective.behavior.relatedimages.media_container_path')
            portal = getSite()
            container = portal.restrictedTraverse(safe_utf8(container_path))
        except:
            pass
        if container is None:
            container = aq_inner(self.context)
            while not IFolderish.providedBy(container):
                container = aq_parent(container)
        return container
