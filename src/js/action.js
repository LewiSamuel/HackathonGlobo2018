	var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var color = Chart.helpers.color;
		var horizontalBarChartData = {
			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
			datasets: [{
				label: 'Dataset 1',
				backgroundColor: "blue",
				// borderColor: window.chartColors.red,
				borderWidth: 1,
				data: [-5]
            },
            {
				label: 'Dataset 1',
				backgroundColor: "red",
				// borderColor: window.chartColors.red,
				borderWidth: 1,
				data: [-5]
			},]

		};

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myHorizontalBar = new Chart(ctx, {
				type: 'horizontalBar',
				data: horizontalBarChartData,
				options: {
					// Elements options apply to all of the options unless overridden in a dataset
					// In this case, we are setting the border of each horizontal bar to be 2px wide
					elements: {
						rectangle: {
							borderWidth: 2,
						}
					},
					responsive: true,
					legend: {
						position: 'bottom',
					},
					title: {
						display: true,
						text: 'Top TOP'
					}
				}
			});

		};

	
