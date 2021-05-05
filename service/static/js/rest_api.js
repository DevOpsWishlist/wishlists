$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wl_id").val(res.id);
        console.log(res)  //not sure if this is working 
        $("#wl_name").val(res.name);
        $("#wl_category").val(res.category);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#wl_name").val("");
        $("#wl_category").val("");
        $("#wl_id").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#wl_name").val();
        var category = $("#wl_category").val();

        var data = {
            "name": name,
            "category": category,
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });
        console.log('hey');

        ajax.done(function(res){
            console.log(res);
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        var wl_id = $("#wl_id").val();
        var name = $("#wl_name").val();
        var category = $("#wl_category").val();

        var data = {
            "name": name,
            "category": category,
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/wishlists/" + wl_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        var wl_id = $("#wl_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists/" + wl_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        var wl_id = $("#wl_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/wishlists/" + wl_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#wl_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#wl_name").val();
        var category = $("#wl_category").val();
       //  var id = $("#wl_id").val();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists?" + queryString,
            contentType: "application/json",
            data: ''
        })


        ajax.done(function(res){
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:30%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th></tr>'
            $("#search_results").append(header);
            var firstWl = "";
            for(var i = 0; i < res.data.length; i++) {
                var wl = res.data[i];
                var row = "<tr><td>"+wl.id+"</td><td>"+wl.name+"</td><td>"+wl.category+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstWl = wl;
                }
            }

            $("#search_results").append('</table>');

            //copy the first result to the form
            if (firstWl != "") {
                update_form_data(firstWl)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
