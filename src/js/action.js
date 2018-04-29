	var config = {
		apiKey: "AIzaSyCuGcOhIL48ul3N9O-DklZ4KKGP4gkK02U",
		authDomain: "hackathon-globo-2018.firebaseapp.com",
		databaseURL: "https://hackathon-globo-2018.firebaseio.com",
		storageBucket: "gs://hackathon-globo-2018.appspot.com",
		messagingSenderId: "542963821369",
	};
	firebase.initializeApp(config);

	var palavras = [];

	Chart.defaults.global.tooltips.enabled = false;

	var color = Chart.helpers.color;
	var horizontalBarChartData = {
		labels: [],
		datasets: [{
			label: 'Relevância',
			backgroundColor: "#ff3d00aa",
			borderColor: "#ff3d00",
			borderWidth: 1,
			data: []
		}]

	};

	var database = firebase.database();
	var starCountRef = firebase.database().ref('topico');
	starCountRef.on('value', function(snapshot) {
		if (snapshot.val() != null){
			var child = (Object.values(snapshot.val()))[0]['data'];
	
			palavras = [];
			window.myHorizontalBar.data.labels = []
			window.myHorizontalBar.data.datasets[0].data = []
			child.forEach(element => {
				window.myHorizontalBar.data.labels.push(element["word"]);
				window.myHorizontalBar.data.datasets[0].data.push(element["freq"]);
				palavras.push(element)
				window.myHorizontalBar.update();
			});

		}

	});
	

	window.onload = function() {
		var ctx = document.getElementById('canvas').getContext('2d');
		window.myHorizontalBar = new Chart(ctx, {
			type: 'horizontalBar',
			data: horizontalBarChartData,
			showTooltips: false,
			options: {
				// Elements options apply to all of the options unless overridden in a dataset
				// In this case, we are setting the border of each horizontal bar to be 2px wide
				elements: {
					rectangle: {
						borderWidth: 5,
					}
				},
				tooltips: { enabled: false },
				hover: { mode: null },
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

		$("#canvas").click(
			function (evt) {
				var activePoints = window.myHorizontalBar.getElementsAtEvent(evt);

				var firstPoint = activePoints[0];
				var label = window.myHorizontalBar.data.labels[firstPoint._index];
				var value = window.myHorizontalBar.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
				palavras.forEach(element => {
					if (element['word'] === label){
						window.myHorizontalBar.data.labels = []
						window.myHorizontalBar.data.datasets[0].data = []
						element['related'].forEach(elem => {
							window.myHorizontalBar.data.labels.push(element['word'] + ' ' + elem["word"]);
							window.myHorizontalBar.data.datasets[0].data.push(elem["freq"]);
							window.myHorizontalBar.update();
						});
					}
				});
			}
		); 

	};


