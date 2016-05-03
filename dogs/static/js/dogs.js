$(document).ready(function(){


  $('#search').on('click', function(){
    var zip_code = $('#zip-code').val();
    $.get('search/', {zip_code: zip_code}, function(data, err){
      if(err){
        console.error(err);
      }
      dogs = data.dogs;
      var dogNames = dogs.map(function(dog){
        return dog.name;
      });
      var self = this;
      self.dogNames = dogNames;

      $('.module-card-title').each(function(dog){
        var name = $(this).text();
        if(self.dogNames.indexOf(name) === -1){
          // console.log($(this).parent())
          $(this).parent().remove();
        }
      });
  });

  });
  
  $('.module-card-button').on('click',function(){
    $();
  });


});
