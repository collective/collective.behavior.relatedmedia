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

    $(".pat-upload").on("uploadAllCompleted", function(response, path) {
      // reload relateditems patterns
      var $relitems_pattern = $("#fieldset-relatedmedia .pat-relateditems");
      if($relitems_pattern.length) {
      $.ajax({
        url: window.location.href + "?ajax_load=1",
        success:function(response) {
            $relitems_pattern.each(function() {
              var $field = $(this).closest(".field"), field_id = $field.attr("id");
              $field.replaceWith($("#" + field_id, $(response)));
            });
            registry.scan("#fieldset-relatedmedia .pat-relateditems");
          }
        });
      }
      var base_url = $(this).data("relmedia-baseurl");
      var $relimages = $("#related-images");
      if($relimages.length) {
        $.ajax({
          url: base_url + "/@@relatedImages",
          success:function(response) {
            $relimages.replaceWith($(response).siblings("#related-images"));
          }
        });
      }
      var $relatts = $("#related-attachments");
      if($relatts.length) {
        $.ajax({
          url: base_url + "/@@relatedAttachments",
          success:function(response) {
            $relatts.replaceWith($(response).find("#related-attachments"));
          }
        });
      }
    });
  });
});
