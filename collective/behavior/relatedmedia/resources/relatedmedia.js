require([
  'jquery',
  'pat-registry',
], function($, registry){

  $(document).ready(function(){
    $('body').on('context-info-loaded', function (e, data) {
      // unbind toolbar reload on structure changes
      $("body").off('structure-url-changed');
      // hide unneeded stuff (breadcrumbs, action column)
      $('.fc-breadcrumbs-container, th.actions, td.actionmenu-container').remove();
    }.bind(this));
    $('input[name="form.widgets.IRelatedMedia.related_media_base_path"]').on('change', function() {
      var uuid = this.value, $field = $(this).closest('.field'), $patStructure = $('.pat-structure', $field);
      if(!uuid) {
        $patStructure.remove();
        return;
      }
      $.ajax({
        url: './edit',
        data: {
          base_path_uuid: uuid,
          ajax_load: new Date().getTime()
        },
        success: function(data) {
          var $new_pat = $('.pat-structure', data);
          if(!$new_pat) return;
          $field.append($new_pat);
          registry.scan($new_pat);
        }
      });
    });
  });
});
