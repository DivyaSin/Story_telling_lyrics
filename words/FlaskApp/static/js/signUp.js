$(function() {
	$("select").hide();
	var form = $('#generateForm');
	var i = $('#generateForm').size() + 1;
	generateRhymes();
});

function generateRhymes(){
	$("select").hide();
	var content= $('#inputName').val();
	console.log(content);
	$('#btnSignUp').click(function() {
    	$.ajax({
        	url: '/signUp',
        	data: $('form').serialize(),
        	type: 'POST',
        	success: function(response) {
        		console.log(response);
        		// check if previous value is same as this value --> no need to check, my dropdown list should be different each time
        		// if there is response then show dropdownlist after populating the list
				populateDropdown(response);
        	},
        	error: function(error) {
            	$("select").hide();
            	console.log(error);
        	}
    	});
    });
}

function populateDropdown(response){
	var selectOne = document.getElementById("states");
	while (selectOne.hasChildNodes()) {
    	selectOne.removeChild(selectOne.lastChild);
	}
	for(var i = 0; i < response.length; i++) {
    	var dropdownValue = response[i];
    	var dropdownElement = document.createElement("option");
    	dropdownElement.textContent = dropdownValue;
    	dropdownElement.value = dropdownValue;
    	selectOne.appendChild(dropdownElement);
	}
	$("select").show();
	dropdownSelect();
}

function dropdownSelect(){
	$("#states").change(function () {
        // remove dropdown
		removeDropdown($(this).val());
		generateMoreOptions();
	});
}

function removeDropdown(value){
	// replace dropDown with editText containing the value
	var figurativeLineTextBox = document.getElementById('figurativeLine');
    figurativeLineTextBox.value = value;
	$("#states").replaceWith(jQuery("#figurativeLine"));
	$("button").hide();
	figurativeLineTextBox.style.display = '';
	// document.getElementById('btnSignUp').style.display= '';
}

function generateMoreOptions(){
	$('<form class="form-inline" id = "generateForm"><div class="form-group"><label for="inputName" class="sr-only">Story line</label><input type="name" name="inputName" id='inputName"+i+"' class="form-control" placeholder =  "Next sentence of lyrics..." style="width: 300px; text-align: center" required autofocus="true"> </div><button id="btnSignUp" class = "btn btn-primary" style=" padding: 8px 15px;font-size: 14px" type="button">Generate</button><select name="states" id="states" style=" background-color: #3BB415; color: white; padding: 8px 15px; font-size: 14px; width: 300px"><option>Select One</option></select><div class="form-group"><label for="inputName" class="sr-only">Figurative line</label><input type="name" name="figurativeLine" id="figurativeLine" class="form-control" style = "width: 300px; display: none" required autofocus="true"></div></form>').appendTo(form);
	i++;
	generateRhymes();
}








