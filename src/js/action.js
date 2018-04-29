	var config = {
		apiKey: "AIzaSyCuGcOhIL48ul3N9O-DklZ4KKGP4gkK02U",
		authDomain: "hackathon-globo-2018.firebaseapp.com",
		databaseURL: "https://hackathon-globo-2018.firebaseio.com",
		storageBucket: "gs://hackathon-globo-2018.appspot.com",
		messagingSenderId: "542963821369",
	};
	firebase.initializeApp(config);

	var palavras = [];
	var frequencia = [];

	var color = Chart.helpers.color;
	var horizontalBarChartData = {
		labels: palavras,
		datasets: [{
			label: 'Relevância',
			backgroundColor: "#ff3d00aa",
			borderColor: "#ff3d00",
			borderWidth: 1,
			data: frequencia
		}]

	};

	var database = firebase.database();
	var starCountRef = firebase.database().ref('topico');
	starCountRef.on('value', function(snapshot) {
		var child = snapshot.val();

		palavras = [];
		frequencia = [];
		window.myHorizontalBar.data.labels = []
		window.myHorizontalBar.data.datasets[0].data = []
		child.forEach(element => {
			window.myHorizontalBar.data.labels.push(element["palavra"]);
			window.myHorizontalBar.data.datasets[0].data.push(element["frequencia"]);
			window.myHorizontalBar.update();
		});

	});
	

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
						borderWidth: 5,
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
					text: 'Assuntos mais falados',
					color: "white"
				}
			}
		});

	};


