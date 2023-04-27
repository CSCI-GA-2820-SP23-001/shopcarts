$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#shopcart_id").val(res.id);
        $("#shopcart_name").val(res.name);
        $("#shopcart_email").val(res.email);
        $("#shopcart_phone_number").val(res.phone_number);
        $("#shopcart_date_joined").val(res.date_joined);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#shopcart_name").val("");
        $("#shopcart_email").val("");
        $("#shopcart_phone_number").val("");
        $("#shopcart_date_joined").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Create a Shopcart
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#shopcart_name").val();
        let email = $("#shopcart_email").val();
        let phone_number = $("#shopcart_phone_number").val();
        let date_joined = $("#shopcart_date_joined").val();

        let data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "date_joined": date_joined,
            "items": []
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/shopcarts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

   

    // ****************************************
    // Update a Shopcart
    // ****************************************

    $("#update-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();
        let name = $("#shopcart_name").val();
        let email = $("#shopcart_email").val();
        let phone_number = $("#shopcart_phone_number").val();
        let date_joined = $("#shopcart_date_joined").val();
        
        let data = {
            "name": name,
            "email": email,
            "phone_number": phone_number,
            "date_joined": date_joined,
            "items": []
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/shopcarts/${shopcart_id}`,
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
    // Retrieve a Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}`,
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
    // Delete a Shopcart
    // ****************************************

    $("#delete-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Shopcart has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#shopcart_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Shopcart
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#shopcart_name").val();
        let email = $("#shopcart_email").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        else if (email) {
            queryString += 'email=' + email
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Phone Number</th>'
            table += '<th class="col-md-2">Date Joined</th>'
            table += '</tr></thead><tbody>'
            let firstShopcart = "";
            for(let i = 0; i < res.length; i++) {
                let shopcart = res[i];
                table +=  `<tr id="row_${i}"><td>${shopcart.id}</td><td>${shopcart.name}</td><td>${shopcart.email}</td><td>${shopcart.phone_number}</td><td>${shopcart.date_joined}</td></tr>`;
                if (i == 0) {
                    firstShopcart = shopcart;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstShopcart != "") {
                update_form_data(firstShopcart)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

 })



 $(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#shopcart_item_id").val(res.id);
        $("#shopcart_shopcart_id").val(res.shopcart_id);
        $("#shopcart_item_name").val(res.name);
        $("#shopcart_item_quantity").val(res.quantity);
        $("#shopcart_item_color").val(res.color);
        $("#shopcart_item_size").val(res.size);
        $("#shopcart_item_price").val(res.price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#shopcart_item_id").val("");
        $("#shopcart_item_name").val("");
        $("#shopcart_item_quantity").val("");
        $("#shopcart_item_color").val("");
        $("#shopcart_item_size").val("");
        $("#shopcart_item_price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Retrieve a list of items for a given shopcart
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}/items`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_item_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Item Name</th>'
            table += '<th class="col-md-2">Item Quantity</th>'
            table += '<th class="col-md-2">Item Color</th>'
            table += '<th class="col-md-2">Item Size</th>'
            table += '<th class="col-md-2">Item Price</th>'
            table += '</tr></thead><tbody>'
            let firstItem = "";
            for(let i = 0; i < res.length; i++) {
                let item = res[i];
                table +=  `<tr id="row_${i}"><td>${item.id}</td><td>${item.name}</td><td>${item.quantity}</td><td>${item.color}</td><td>${item.size}</td><td>${item.price}</td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#search_item_results").append(table);

            // copy the first result to the form
            if (firstItem != "") {
                update_form_data(firstItem)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
        

    });


    // ****************************************
    // Create an Item
    // ****************************************

    $("#create-item-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();
        let item_id = $("#shopcart_item_id").val();
        let name = $("#shopcart_item_name").val();
        let quantity = $("#shopcart_item_quantity").val();
        let color = $("#shopcart_item_color").val();
        let size = $("#shopcart_item_size").val();
        let price = $("#shopcart_item_price").val();

        let data = {
            "id": item_id,
            "shopcart_id": shopcart_id,
            "name": name,
            "quantity": quantity,
            "color": color,
            "size": size,
            "price": price
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${shopcart_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete an item
    // ****************************************

    $("#delete-item-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();
        let item_id = $("#shopcart_item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Item has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-item-btn").click(function () {
        $("#shopcart_shopcart_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Increment an Item
    // ****************************************

    $("#increase-quantity-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();
        let item_id = $("#shopcart_item_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${shopcart_id}/items/${item_id}/increment`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Item has been Incremented!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });
    
    // ****************************************
    // Decrement an Item
    // ****************************************

    $("#decrease-quantity-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();
        let item_id = $("#shopcart_item_id").val();

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${shopcart_id}/items/${item_id}/decrement`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Item has been Decremented!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Update an item
    // ****************************************

    $("#update-item-btn").click(function () {

        let shopcart_id = $("#shopcart_shopcart_id").val();
        let item_id = $("#shopcart_item_id").val();
        let name = $("#shopcart_item_name").val();
        let quantity = $("#shopcart_item_quantity").val();
        let color = $("#shopcart_item_color").val();
        let size = $("#shopcart_item_size").val();
        let price = $("#shopcart_item_price").val();
        
        let data = {
            "id": item_id,
            "shopcart_id": shopcart_id,
            "name": name,
            "quantity": quantity,
            "color": color,
            "size": size,
            "price": price
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/shopcarts/${shopcart_id}/items/${item_id}`,
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

})