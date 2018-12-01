(function () {
	$('form#login-form').on('submit', function(e) {
		e.preventDefault();

		$('#login-message, #device-list').html('');

		var $this = $(this);

		var username = $this.find('input[name=username]').val().trim();
		var password = $this.find('input[name=password]').val().trim();
		
		var action = $this.attr('action');

		var data = JSON.stringify({
			username: username, 
			password: password
		});

		$.ajax({
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			url: action,
			data: data,
			success: function (res) {
				if (res.error) {
					$("#login-message").html(res.error);
				} else {
					$("#login-message").html(res.message);

					if (res.devices) {
						var template = $("#device-template").html();
						var html = '<h5>Select an existing device to delete.<h5>';
						(res.devices).forEach(function(device) {
							html += Mustache.render(template, {
								device: device['device'],
								mac: device['mac']
							});
						});
						$('#device-list').html(html);
					}
				}
			},
			dataType: 'json'
		});
	});

	$("body").on('click', "#device-list button", function() {
		var $this = $(this);
		$(this).attr('disabled', 'disabled');

		var data = JSON.stringify({
			mac: $this.data('mac')
		});

		$.ajax({
			type: 'POST',
			contentType: 'application/json; charset=utf-8',
			url: '/deleteDevice',
			data: data,
			success: function (res) {
				console.log(res);
			},
			dataType: 'json'
		});
	});

})();