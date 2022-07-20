Changelog
=========


3.2.0 (2022-07-20)
------------------

- Fixed customized `selection.xml` template for `pat-relateditems`.
  [petschki]

- CI Test setup with `mxdev`.
  [petschki]

- Remove `related-media` widget and enable "upload" for related widget.
  [petschki]


3.1.1 (2022-07-04)
------------------

- Fix moved utility. import now from `plone.base`
  [petschki]


3.1.0 (2022-04-23)
------------------

- remove requireJS from JS resource (Plone 6 compatibility)
  [petschki]


3.0.4 (2022-03-16)
------------------

- Add browserlayer for viewlets. (fixes #7)
  [petschki]


3.0.3 (2022-03-14)
------------------

- Fix related media container utility permissions
  [petschki]


3.0.2 (2022-03-09)
------------------

- Fix bug in memoized utility
  [petschki]


3.0.1 (2022-03-09)
------------------

- Fix adding leadimage to the gallery
- Fix media container determination when in language independent Assets
  [petschki]


3.0.0 (2022-01-18)
------------------

Breaking changes:

- 3.x is Plone6/py3 only version. Use 2.x for Plone5/py2/3 compatibility
  [petschki]

- Change strategy for optional media base_path container creation. This is a registry setting.
- inline title editing for related items
- Plone6 / Classic Theme updates
  [petschki]


2.1.3 (2020-07-22)
------------------

- Fix bug in util method when related base_path is missing. fixes #2
  [petschki]


2.1.2 (2020-07-02)
------------------

- Fix issue with unauthorized media folder
  [petschki]

- Update/enhance default settings in controlpanel
  [petschki]

- bugfix in workflow synchronization of related media base path
  [petschki]


2.1.1 (2020-05-27)
------------------

- Fix imports to support ``plone.app.contenttypes`` < 2.0
  [petschki]


2.1 (2020-05-27)
----------------

Features:

- global setting to always update first related image as leadimage.
  This is disabled per default.
  [petschki]


2.0.3 (2020-05-26)
------------------

- fix attachment viewlet to be hidden when no files are related
  [petschki]


2.0.2 (2019-12-13)
------------------

- Fix bug in workflow sync event when pasting objects
  [petschki]


2.0.1 (2019-11-22)
------------------

- merged HISTORY.txt and CHANGES.rst
  [petschki]


2.0.0 (2019-11-22)
------------------

- Python 3 / Plone 5.2 compatibility
  [petschki]

- Media Base Path feature
  [petschki]

- test setup and CI
  [petschki]

1.1.1 (2018-05-25)
------------------

- Update documentation.
  [petschki]


1.1 (2018-05-25)
----------------

- fix image_size vocabulary. Plone 5 compatibility.
  [petschki]


1.0 (2018-05-23)
----------------

- Fix issue with disapearing images when 'include_leadimage' was deactivated
  [petschki]

- support for Event Occurrences.
  [petschki]

- add markup for fancybox library
  [petschki]

- Separate viewlet caption and overlay caption
  [petschki]


1.0b1 (2015-07-15)
------------------

- title caption toggle for gallery images
  [petschki]


1.0a1 (2015-07-14)
------------------

- Initial release
