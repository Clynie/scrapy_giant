


			AmCharts.ready(function () {
				generateChartData();
				createStockChart();
			});

			var chart;
			var chartData = [];
			var newPanel;
			var stockPanel;

			function generateChartData() {
                
			}

			function createStockChart() {
				chart = new AmCharts.AmStockChart();
                chart.pathToImages ="http://www.amcharts.com/lib/3/images/";
				chart.balloon.horizontalPadding = 13;

				// DATASET //////////////////////////////////////////
				var dataSet = new AmCharts.DataSet();
				dataSet.fieldMappings = [{
					fromField: "open",
					toField: "open"
				}, {
					fromField: "close",
					toField: "close"
				}, {
					fromField: "high",
					toField: "high"
				}, {
					fromField: "low",
					toField: "low"
				}, {
					fromField: "volume",
					toField: "volume"
				}, {
					fromField: "value",
					toField: "value"
				}];
				dataSet.color = "#7f8da9";
				dataSet.dataProvider = chartData;
				dataSet.categoryField = "date";

				chart.dataSets = [dataSet];

				// PANELS ///////////////////////////////////////////
				stockPanel = new AmCharts.StockPanel();
				stockPanel.title = "Value";

				// graph of first stock panel
				var graph = new AmCharts.StockGraph();
				graph.type = "candlestick";
				graph.openField = "open";
				graph.closeField = "close";
				graph.highField = "high";
				graph.lowField = "low";
				graph.valueField = "close";
				graph.lineColor = "#7f8da9";
				graph.fillColors = "#7f8da9";
				graph.negativeLineColor = "#db4c3c";
				graph.negativeFillColors = "#db4c3c";
				graph.fillAlphas = 1;
				graph.balloonText = "open:<b>[[open]]</b><br>close:<b>[[close]]</b><br>low:<b>[[low]]</b><br>high:<b>[[high]]</b>";
				graph.useDataSetColors = false;
				stockPanel.addStockGraph(graph);

				var stockLegend = new AmCharts.StockLegend();
				stockLegend.markerType = "none";
				stockLegend.markerSize = 0;
				stockLegend.valueTextRegular = undefined;
				stockLegend.valueWidth = 250;
				stockPanel.stockLegend = stockLegend;

				chart.panels = [stockPanel];


				// OTHER SETTINGS ////////////////////////////////////
				var sbsettings = new AmCharts.ChartScrollbarSettings();
				sbsettings.graph = graph;
				sbsettings.graphType = "line";
				sbsettings.usePeriod = "WW";
				chart.chartScrollbarSettings = sbsettings;

				// Enable pan events
				var panelsSettings = new AmCharts.PanelsSettings();
				panelsSettings.panEventsEnabled = true;
				chart.panelsSettings = panelsSettings;

				// CURSOR
				var cursorSettings = new AmCharts.ChartCursorSettings();
				cursorSettings.valueBalloonsEnabled = true;
				cursorSettings.fullWidth = true;
				cursorSettings.cursorAlpha = 0.1;
				chart.chartCursorSettings = cursorSettings;

				// PERIOD SELECTOR ///////////////////////////////////
				var periodSelector = new AmCharts.PeriodSelector();
				periodSelector.position = "bottom";
				periodSelector.periods = [{
					period: "DD",
					count: 10,
					label: "10 days"
				}, {
					period: "MM",
					selected: true,
					count: 1,
					label: "1 month"
				}, {
					period: "YYYY",
					count: 1,
					label: "1 year"
				}, {
					period: "YTD",
					label: "YTD"
				}, {
					period: "MAX",
					label: "MAX"
				}];
				chart.periodSelector = periodSelector;


				chart.write('chartdiv');
			}



			function addPanel() {
				newPanel = new AmCharts.StockPanel();
				newPanel.allowTurningOff = true;
				newPanel.title = "Volume";
				newPanel.showCategoryAxis = false;

				var graph = new AmCharts.StockGraph();
				graph.valueField = "volume";
				graph.fillAlphas = 0.15;
				newPanel.addStockGraph(graph);

				var legend = new AmCharts.StockLegend();
				legend.markerType = "none";
				legend.markerSize = 0;
				newPanel.stockLegend = legend;

				chart.addPanelAt(newPanel, 1);
				chart.validateNow();

				document.getElementById("addPanelButton").disabled = true;
				document.getElementById("removePanelButton").disabled = false;
			}

			function removePanel() {
				chart.removePanel(newPanel);
				chart.validateNow();

				document.getElementById("addPanelButton").disabled = false;
				document.getElementById("removePanelButton").disabled = true;
			}

