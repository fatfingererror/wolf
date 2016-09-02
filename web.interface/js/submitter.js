$(function() {
	function submitRule() {
		$.ajax({
			url: "http://192.168.99.100:5002/",
			type: "POST",
			ContentType: "application/json",
			data: {"data": JSON.stringify({
				"symbol":"NZDUSD",
				"modifier":"ASK",
				"comparator":">",
				"threshold":0.001,
				"url":"http://192.168.99.100:5002/"})
			},
			success: function(msg) { console.log("rule sent") }
		})

		setTimeout(submitRule, 500)
	}

	submitRule()

});
