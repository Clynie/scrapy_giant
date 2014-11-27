
		    AmCharts.ready(function () {
                generateChartData();
//                generateCollectiveData();
//                createPieChart();
//                createStockChart();
//                callbackPieChart();
            });

            var pieChart;
            var stockChart;
            var chartData = [];
            var collectiveData = [];

            function generateChartData() {
                var data = [];
                // populate stock data as init
                
                    
					    data.unshift({
                            "date": new Date("2014-11-11T00:00:00"),
                            "stockopen": 98.6,
                            "stockclose": 97.7,
                            "stockhigh": 98.6,
                            "stocklow": 97.5,
                            "stockprice": 97.7,
                            "stockvolume": 22857,
                            "traderprice": 0,
                            "traderbuyvolume": 0,
                            "tradersellvolume": 0,
                            "event": ""
                        });
                    
					    data.unshift({
                            "date": new Date("2014-11-10T00:00:00"),
                            "stockopen": 95.2,
                            "stockclose": 98.3,
                            "stockhigh": 98.4,
                            "stocklow": 95.2,
                            "stockprice": 98.3,
                            "stockvolume": 35347,
                            "traderprice": 0,
                            "traderbuyvolume": 0,
                            "tradersellvolume": 0,
                            "event": ""
                        });
                    
                
                // populate trader data as update
                
            }


//            function generateCollectiveData(){
//                for (var x in chartData) {
//                    var dataPoint = chartData[x];
//                    if (0 == x) {
//                        for (var y in dataPoint.data) {
//                            collectiveData.push({
//                                "date": dataPoint.data[y].date,
//                                    "traderbuyvolume": dataPoint.data[y].traderbuyvolume,
//                                    "tradersellvolume": dataPoint.data[y].tradersellvolume,
//                                    "tradersumvolume": dataPoint.data[y].tradersumvolume,
//                                    "traderprice": dataPoint.data[y].traderprice * dataPoint.data[y].tradersumvolume,
//                                    "stockvolume": dataPoint.data[y].stockvolume,
//                                    "stockprice": dataPoint.data[y].stockprice
//                            });
//                        }
//                    } else {
//                        for (var y in dataPoint.data) {
//                            collectiveData[y].traderbuyvolume += dataPoint.data[y].traderbuyvolume;
//                            collectiveData[y].tradersellvolume += dataPoint.data[y].tradersellvolume;
//                            collectiveData[y].tradersumvolume += dataPoint.data[y].tradersumvolume;
//                            collectiveData[y].traderprice += dataPoint.data[y].traderprice * dataPoint.data[y].tradersumvolume;
//                        }
//                    }
//                }
//                for (var x in collectiveData) {
//                    collectiveData[x].traderprice = Math.floor(collectiveData[x].traderprice / collectiveData[x].tradersumvolume);
//                }
//            }
//
//
//            function createPieChart() {
//                pieChart = AmCharts.makeChart("chartdiv1", {
//                    "type": "pie",
//                        "dataProvider": chartData,
//                        "valueField": "tradervolume",
//                        "titleField": "traderid",
//                        "labelText": "[[title]]: [[value]]",
//                        "legend": {
//                        "markerType": "circle",
//                            "position": "right",
//                            "marginRight": 80,
//                            "autoMargins": false
//                    },
//                        "pullOutOnlyOne": true
//                });
//            }
//
//
//            function createStockChart() {
//                stockChart = AmCharts.makeChart("chartdiv2", {
//                    "type": "serial",
//                        "theme": "none",
//                        "pathToImages": "http://www.amcharts.com/lib/3/images/",
//                        "dataProvider": collectiveData,
//                        "legend": {
//                        "equalWidths": false,
//                            "useGraphSettings": true
//                        },
//                        "valueAxes": [{
//                            "id": "volumeAxis",
//                            "axisAlpha": 0,
//                            "gridAlpha": 0,
//                            "position": "left",
//                            "title": "volume",
//                            "stackType": "regular"
//                            }, {
//                            "id": "priceAxis",
//                            "axisAlpha": 0,
//                            "gridAlpha": 0,
//                            "inside": true,
//                            "position": "right",
//                            "title": "price"
//                        }],
//                        "graphs": [{
//                            "balloonText": "[[value]]",
//                            "dashLengthField": "dashLength",
//                            "fillAlphas": 0.7,
//                            "legendPeriodValueText": "[[value]]",
//                            "legendValueText": "v: [[value]]",
//                            "title": "traderbuyvolume",
//                            "type": "column",
//                            "valueField": "traderbuyvolume",
//                            "valueAxis": "volumeAxis"
//                            }, {
//                            "balloonText": "[[value]]",
//                            "dashLengthField": "dashLength",
//                            "fillAlphas": 0.7,
//                            "legendPeriodValueText": "[[value]]",
//                            "legendValueText": "v: [[value]]",
//                            "title": "tradersellvolume",
//                            "type": "column",
//                            "valueField": "tradersellvolume",
//                            "valueAxis": "volumeAxis"
//                            }, {
//                            "balloonText": "[[value]]",
//                            "dashLengthField": "dashLength",
//                            "fillAlphas": 0.7,
//                            "legendPeriodValueText": "[[value]]",
//                            "legendValueText": "v: [[value]]",
//                            "title": "stockvolume",
//                            "type": "column",
//                            "newStack": true,
//                            "valueField": "stockvolume",
//                            "valueAxis": "volumeAxis"
//                            }, {
//                            "balloonText": "p:[[value]]",
//                            "bullet": "round",
//                            "bulletBorderAlpha": 1,
//                            "useLineColorForBulletBorder": true,
//                            "bulletColor": "#FFFFFF",
//                            "bulletSizeField": "townSize",
//                            "dashLengthField": "dashLength",
//                            "descriptionField": "event",
//                            "labelPosition": "right",
//                            "labelText": "[[event]]",
//                            "legendValueText": "p: [[value]]",
//                            "title": "traderprice",
//                            "fillAlphas": 0,
//                            "valueField": "traderprice",
//                            "valueAxis": "priceAxis"
//                            }, {
//                            "balloonText": "p: [[value]]",
//                            "bullet": "round",
//                            "bulletBorderAlpha": 1,
//                            "useLineColorForBulletBorder": true,
//                            "bulletColor": "#FFFFFF",
//                            "bulletSizeField": "townSize",
//                            "dashLengthField": "dashLength",
//                            "descriptionField": "event",
//                            "labelPosition": "right",
//                            "labelText": "[[event]]",
//                            "legendValueText": "p: [[value]]",
//                            "title": "stockprice",
//                            "fillAlphas": 0,
//                            "valueField": "stockprice",
//                            "valueAxis": "priceAxis"
//                        }],
//                        "chartCursor": {
//                        "categoryBalloonDateFormat": "WW",
//                            "cursorAlpha": 0.1,
//                            "cursorColor": "#000000",
//                            "fullWidth": true,
//                            "valueBalloonsEnabled": false,
//                            "zoomable": false
//                        },
//                        "dataDateFormat": "YYYY-MM-DD",
//                        "categoryField": "date",
//                        "categoryAxis": {
//                        "dateFormats": [{
//                            "period": "DD",
//                                "format": "DD"
//                        }, {
//                            "period": "WW",
//                                "format": "MMM DD"
//                        }, {
//                            "period": "MM",
//                                "format": "MMM"
//                        }, {
//                            "period": "YYYY",
//                                "format": "YYYY"
//                        }],
//                            "parseDates": true,
//                            "autoGridCount": false,
//                            "axisColor": "#555555",
//                            "gridAlpha": 0.1,
//                            "gridColor": "#FFFFFF",
//                            "gridCount": 50
//                        },
//                        "exportConfig": {
//                        "menuBottom": "20px",
//                            "menuRight": "22px",
//                            "menuItems": [{
//                            "icon": 'http://www.amcharts.com/lib/3/images/export.png',
//                                "format": 'png'
//                        }]
//                        },
//                        "chartScrollbar": {},
//                        "chartCursor": {
//                        "cursorPosition": "mouse"
//                        },
//                });
//            }
//
//            function callbackPieChart() {
//                pieChart.addListener("pullOutSlice", function (event) {
//                    stockChart.dataProvider = event.dataItem.dataContext.data;
//                    stockChart.validateData();
//                    stockChart.animateAgain();
//                });
//
//                PieChart.addListener("pullInSlice", function (event) {
//                    stockChart.dataProvider = collectiveData;
//                    stockChart.validateData();
//                    stockChart.animateAgain();
//                });
//            }
        