$('#newCategoryModal').on('shown.bs.modal', function () {
    $('#newCategoryModal').focus();
});


$('#form_cateogry').submit(function(event) {
    event.preventDefault();

    var formData = $('#form_cateogry').serialize();
    // Get value from form
    var newCategory = $('#form_cateogry').find('input[name="name"]').val()

    $.ajax({
        type: 'POST',
        url: $('#form_cateogry').attr('action'),
        data: formData,
        success: function(categories) {
            console.log(categories);
            $('#categories').empty();

            var output = categories.map(function(category) {
                var selected =  category.name == newCategory ? 'selected="selected"' : '';
                return '<option value="'+ category.name +'" '+ selected +'>'+ category.name +'</option>';
            });
            $('#categories').html(output.join(' '));

            $('#newCategoryModal').modal('hide');
        },
        error: function(err) {
            alert(err);
        }
    });
});

function signOut() {
    console.log("will sigin out")
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut();
}

// Disable space input on category form
$("input#category").on({
    keydown: function(e) {
      if (e.which === 32)
        return false;
    },
    change: function() {
      this.value = this.value.replace(/\s/g, "");
    }
  });