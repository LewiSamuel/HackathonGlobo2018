	var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var color = Chart.helpers.color;
		var horizontalBarChartData = {
			labels: ['Fora Diego', 'Fora Glavy', 'Top Top', 'Pithon em Python', 'Quero café', 'Meditar', 'Mãe to na globo'],
			datasets: [{
				label: 'Relevância',
				backgroundColor: "#ff8a65aa",
				borderColor: "#ff8a65",
				borderWidth: 1,
				data: [90,40,30,20,10,10,9]
            }]

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
                    scaleFontColor: "#FFFFFF",
                    color: "white",
					legend: {
                        position: 'bottom',
                        color: "white",
                        display: false
					},
					title: {
						display: true,
                        text: 'Top TOP',
                        color: "white"
					}
				}
			});

		};

	
