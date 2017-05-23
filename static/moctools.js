function populate_dropdown(menu, item_list){
   for (var i = 0; i< item_list.length; i++) {
       var item_name = item_list[i];
       var list_entry = document.createElement("option");
       list_entry.textContent = item_name;
       list_entry.value = item_name;
       menu.appendChild(list_entry);
   }
}

function draw_project_dropdown(fieldset, project_list){
    var div = document.createElement('div')
    fieldset.appendChild(div);
    var label = document.createElement('label')
    label.textContent = 'Choose a project:';
    div.appendChild(label);
    var dropdown = document.createElement("select");
    dropdown.setAttribute('name', 'choose_project');
    div.appendChild(dropdown) 
    populate_dropdown(dropdown, project_list)
}

function check_match(){
    var email = document.getElementsByName('email')[0].value;
    var confirm_email = document.getElementsByName('confirm_email')[0].value;
    var error_label = document.getElementById("match_error");
    if (email != confirm_email) {
        error_label.style.visibility = "visible";
    } else {
        error_label.style.visibility = "hidden";
    }
}

// Set the variable form correctly on page load/refresh
function first_load(project_list){
    if (document.getElementById('exists_true').checked) {
        switch_form(true, 'user_form');
    } else {
        switch_form(false, 'user_form');
    }

    if (document.getElementById('new_project').checked) {
        switch_project_form(true, proj_list);
    } else {
        switch_project_form(false, proj_list);
   }
}

// Toggle the form between OpenStack login and new user request
function switch_form(user_exists, fieldset_id){
    var fieldset = document.getElementById(fieldset_id);
    fieldset.style.visibility = "visible"
    while (fieldset.firstChild){
        fieldset.removeChild(fieldset.firstChild);
    }
    var legend = document.createElement('legend');
    legend.textContent = 'User Info'
    fieldset.appendChild(legend)
    if (user_exists) {
        field_list = [ 'openstack_username', 'openstack_password' ]
        redraw_form(fieldset, field_list);
    } else {
        field_list = [ 'email', 'confirm_email', 'phone', 'organization', 'org_role', 'sponsor', 'pin', 'comment' ]
        redraw_form(fieldset, field_list);
    }
}

// Toggle the form between existing project and new project request
function switch_project_form(project_is_new, project_list) {
    var fieldset = document.getElementById("project_form");
    fieldset.style.visibility = "visible"
    while (fieldset.firstChild){
        fieldset.removeChild(fieldset.firstChild);
    }
    var legend = document.createElement('legend');
    legend.textContent = 'Project Info'
    fieldset.appendChild(legend)
    if (project_is_new) {
        field_list = [ 'project_name', 'project_description' ]
        redraw_form(fieldset, field_list)
    } else {
        draw_project_dropdown(fieldset, project_list)
    }
}

// Redraw the form based on the provided field list
function redraw_form(fieldset, field_list) {
    for ( var i=0; i<field_list.length; i++) {
        field_name = field_list[i]
        var div = document.createElement('div')
        fieldset.appendChild(div);
        var label = document.createElement('label')
        label.textContent = field_name;
        div.appendChild(label);
        var input_box = document.createElement("input");
        input_box.setAttribute('name', field_name);
        if (field_name.indexOf('password') > -1 ) {
            input_box.setAttribute('type', 'password');
        }
        div.appendChild(input_box) 
    }
}

