############################################
Dexterity Content Related Images/Attachments
############################################


What can this package do for you?
=================================

This packages adds a behavior to manage content related images and attachments.
This is done with a RelationList field. If `plone.app.widgets`_ is installed,
the RelationList is finally usable ;)


Configure and activate
======================

You can define a container path for the uploaded Media in the registry.
The default media container is "<site_root|nav_root>/media"

The behavior is automatically enabled for Dexterity "Documents" (aka Page).
Edit the data in the new tab "Related Media"

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia.png

If `pat-upload`_ (mockup) is installed, you can drag'n'drop images and files to your
content easily.


View
====

Images are shown in a viewlet (activated in IBelowContentTitle) with the selected
css class. Right now there is no definition for the css classes in this package.
You have to define it in your theme package.

Attachments are also shown in a viewlet (activated in IBelowContentBody)


.. _`plone.app.widgets`: https://pypi.python.org/pypi/plone.app.widgets
.. _`pat-upload`: http://plone.github.io/mockup/dev/#pattern/dropzone
