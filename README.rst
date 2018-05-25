############################################
Dexterity Content Related Images/Attachments
############################################


What can this package do for you?
=================================

This packages adds a behavior to manage content related images and attachments.


Configure and activate
======================

You can define a path for the container (aka "Folder") where the uploaded Media is stored.
The default media container is "(site_root|nav_root)/media" and can be changed in the configuration registry.

The behavior is automatically enabled for "Documents".
Edit the data in the new tab "Related Media"

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia.png

You can also upload any image or file resource via the new upload area below the content.

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia_view.png


View
====

Images are shown in a viewlet below the content title with the selected
css class.

Attachments are also in a viewlet below the content body.

This package does not include any CSS or JS resource to enable some nice
gallery experience. You can define this in your themen package.


.. _`pat-upload`: http://plone.github.io/mockup/dev/#pattern/dropzone
