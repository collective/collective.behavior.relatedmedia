(function($) {
  $(function(){
    $(".pat-upload").on("uploadAllCompleted", function(response, path) {
      // reload viewlets on upload
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
})(jQuery);
