$(document).ready(function() {


	var options = {
		allow_empty: true,

		filters: [
			{
				id: 'name',
				label: 'Name',
				type: 'string',
				// optgroup: 'core',
				default_value: 'John',
				size: 30,
				description: 'This filter is <b>awesome</b> !',
				unique: true
			},
			{
				id: 'age',
				label: 'Age',
				type: 'integer',
				// optgroup: 'core',
				default_value: 20,
				size: 30,
				unique: true
			},
			{
				id: 'smoker_y_n',
				label: 'Smoker',
				type: 'boolean',
				// optgroup: 'core',
				default_value: true,
				size: 30,
				unique: true
			},
			{
				id: 'phrase',
				label: 'Containing Phrase',
				type: 'string',
				// optgroup: 'core',
				default_value: "Lives alone",
				size: 200,
				unique: true
			}


		]
	};


	$('#builder').queryBuilder(options);

	$('.parse-json').on('click', function() {
		console.log(JSON.stringify(
			$('#builder').queryBuilder('getSQL'),
			undefined, 2
		));
		$('#result_p').text(JSON.stringify(
			$('#builder').queryBuilder('getSQL'),
			undefined, 2
		))
	});



});