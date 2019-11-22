############################################
Dexterity Content Related Images/Attachments
############################################


What can this package do for you?
=================================

This packages adds a dexterity behavior to manage content related images and attachments.


Configure and activate
======================

You have to define a Media Root Path where the uploaded Media is stored.
The default media container is ``(site_root|nav_root)/media`` and can be changed in the Related Media Controlpanel.

The behavior is automatically enabled for "Documents".
Edit the data in the new tab "Related Media"


Media Base Path Strategy
========================

When a Document is created we generate a ``Related Media Base Path`` in the background to store all the uploaded Media.
This base path is located in the configured Media Root Path above.

The Edit form renders a structure pattern from the base path where you can upload/rearrange/sort/rename and delete the
related media inplace.

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia_basepath.png

Further settings (for gallery css classes handling the images) as well as additional Images and Files (located somewhere else as the base path) are below

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia_settings.png



View
====

Images are displayed in a viewlet below the content title with the selected
css class.

Attachments are displayed in a viewlet below the content body.

.. image:: https://raw.githubusercontent.com/kombinat/collective.behavior.relatedmedia/master/docs/collective.behavior.relatedmedia_view.png

This package does not include any CSS or JS resource to enable some nice
gallery experience. You can define this in your themen package.



Author
======

- Peter Mathis [petschki]
