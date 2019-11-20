require([
  'jquery'
], function($){

  $(document).ready(function(){
    $('body').on('context-info-loaded', function (e, data) {
      // unbind toolbar reload on structure changes
      $("body").off('structure-url-changed');
      // hide breadcrumbs
      $('.fc-breadcrumbs-container').hide();
    }.bind(this));
  });
});
