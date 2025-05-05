Changelog
=========


## 3.7.5 (2025-05-05)


- Do not break if the lead image adapter cannot be initialized (fixes [#25](https://github.com/collective/collective.behavior.relatedmedia/issues/25)). @ale-rt


## 3.7.4 (2025-04-03)


- Fix "display" templates of RelatedMediaWidgets -> use FormBrowserLayer to override p.a.z3cform.  @petschki


## 3.7.3 (2025-03-21)


- Refactor default settings value lookup.  @petschki
- Fix REQUEST during object removal.  @petschki


## 3.7.2 (2025-03-05)

Bug fixes:

- Fix SelectedItem component "unselect"
  [petschki]


## 3.7.1 (2025-02-28)


Bug fixes:

- Cleanup obsolete pattern templates and upload viewlet. Upload is done now only in Contentbrowser.
- Add CSS for TinyMCE to make inline galleries better editable.
  [petschki]


## 3.7.0 (2025-02-20)


- Use `ContentBrowserWidget` if Plone 6.1.
  [petschki]


## 3.6.6 (2024-11-13)


- Configurable large overlay images scale
  [petschki]


## 3.6.5 (2024-10-28)


- Inject slickSliderOptions via data-attributes.
  [petschki]


## 3.6.4 (2024-10-28)


- Fix Fancybox initialization problems.
  [petschki]


## 3.6.3 (2024-10-25)


- Initialize "slick-slider" automatically inside TinyMCE image gallery.
  [petschki]


## 3.6.2 (2024-06-14)


- Fix broken attachments.
  [petschki]


## 3.6.1 (2024-06-14)

- Hide image/attachment viewlet when no content available.
  [petschki]
- update JS resources.
  [petschki]

## 3.6.0 (2024-05-14)

- Enhanced Attachment viewlet.
  [petschki]


## 3.5.4 (2024-04-08)

- Fixed upgrade step for TinyMCE gallery tool.
  Cleanup settings for old template.
  [petschki]


## 3.5.3 (2024-03-22)

- Fixed upgrade step for migrating "base_path" relations.
  [petschki]


## 3.5.2 (2024-02-29)

- Remove old obsolete JS resource from upload viewlet.
  [petschki]


## 3.5.1 (2024-02-27)

- packaging updates.
  [petschki]


## 3.5.0 (2024-02-27)

Features:

- New gallery editor plugin for TinyMCE replacing the gallery template and adds
  possibility to select/reorder gallery images inside TinyMCE.
  [petschki]


## 3.4.0 (2024-01-25)

Features:

- Outputfilter and pattern for related image gallery.
- TinyMCE template for gallery placement inside richtext.
  [petschki]


## 3.3.5 (2023-11-16)

- Do not fail in update script when broken catalog brains exists.
  [petschki]


## 3.3.4 (2023-10-09)

- Fix syncing review_state of (deprecated) related media container.
  [petschki]


## 3.3.3 (2023-09-27)

- Fix error when invalid attachment is uploaded.
  [petschki]


## 3.3.2 (2023-09-21)

- Added upgrade tep for renamed behavior.
  [petschki]


## 3.3.1 (2023-07-19)

- Fix default behavior assignment for "Page".
  [petschki]


## 3.3.0 (2023-07-17)
------------------

Feature:

- Mark `base_path` concept as deprecated and add a migration script for it.
  [petschki]

- Convenience short name for behavior.
  [petschki]

- Use `plone.base.utils.human_readable_size` for attachment size and implement
  mimetype icons for attachment list.
  [petschki]


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

- Fix issue with disappearing images when 'include_leadimage' was deactivated
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
