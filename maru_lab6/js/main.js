function main() {
	$('.content').hide();
	$('.content').fadeIn(2000);

	$('.text').hide();
	$('.click').on('click', function()
	{
		$('.text').toggle();
	});
};

$(document).ready(main);