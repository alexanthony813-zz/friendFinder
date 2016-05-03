$(document).ready(function(){


  $('#search').on('click', function(){
    var zip_code = $('#zip-code').val();
    $.get('search/', {zip_code: zip_code}, function(data, err){
      if(err){
        console.error(err)
      }

      $('.module.card.title').filter(function(dog){
        return dog.val() in dogs;
      })
    })
  })
  
  $('.module-card-button').on('click',function(){
    $()
  })


});
