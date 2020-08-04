$('#downloadPDFButton').click(function () {
	var button = $('#downloadPDFButton')[0];

	if (!button.hasAttribute('disabled'))
	{
		button.setAttribute('disabled', 'disabled');
		button.style.cursor = 'progress';

		html2canvas($('#ivan-resume')[0]).then(function(canvas) {	
			var width = canvas.width;
			var height = canvas.height;
			
			var millimeters = {
				width: Math.floor(width * 0.264583),
				height: Math.floor(height * 0.264583)
			};

			var img = canvas.toDataURL('image/png');

			var doc = new jsPDF('p', 'mm', 'a4');
			doc.deletePage(1);
			doc.addPage(millimeters.width, millimeters.height);
			doc.addImage(img, 'PNG', 0, 0, millimeters.width, millimeters.height, undefined, 'FAST');
			doc.save('ivan-zdravkov-resume.pdf');

			setTimeout(function() { 
				button.removeAttribute('disabled');
				button.style.cursor = 'default';
			}, 500);
		});
	}
});