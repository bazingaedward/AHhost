$(function () {
    var currentElement = 'TEM';
    var RESOLUTIONTHRESHOLD = 200;


    var targetExtent = ol.proj.transformExtent([113.516, 37.4385, 115.477, 38.7639], 'EPSG:4326', 'EPSG:3857');

    var ctlZoomToExt = new ol.control.ZoomToExtent({
        extent: targetExtent
    });
    var ctlScaleLine = new ol.control.ScaleLine();

    var mapControls = ol.control.defaults({
        attribution: false
    }).extend([
        ctlScaleLine,
        ctlZoomToExt
    ]);

    var mapInteractions = ol.interaction.defaults({altShiftDragRotate: false, pinchRotate: false});

    var lyRaster = new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: '/static/gis/tiles/{z}/{x}/{-y}.png',
            minZoom: 7,
            maxZoom: 9
        })
    });

    var lyXianline = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: '/static/gis/geojson/xian_line.geojson',
            format: new ol.format.GeoJSON(),

        }),
        style: function (feature, resolution) {
            return new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#319FD3',
                    width: 1
                })
            });
        }
    });



    var lyXianPoint = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: '/static/gis/geojson/xian_point.geojson',
            format: new ol.format.GeoJSON()
        }),
        style: function (feature, resolution) {
            if(resolution > RESOLUTIONTHRESHOLD){

                return new ol.style.Style({
                    // stroke: new ol.style.Stroke({
                    //     color: [64, 200, 200, 0.5],
                    //     width: 1
                    // }),
                    text: new ol.style.Text({
                        font: '14px Simhei',
                        text: feature.get('NAME'),
                        fill: new ol.style.Fill({
                            color: [64, 64, 64, 0.6]
                        })
                    })
                });
            }
    }});

    var lyXiangPoint = new ol.layer.Vector({
        source: new ol.source.Vector({
            url: '/static/gis/geojson/xiang_point.geojson',
            format: new ol.format.GeoJSON()
        }),
        style: function (feature, resolution) {
        if(resolution <= RESOLUTIONTHRESHOLD){
            return new ol.style.Style({
                // stroke: new ol.style.Stroke({
                //     color: [64, 200, 200, 0.5],
                //     width: 1
                // }),
                text: new ol.style.Text({
                    font: '4px Simhei',
                    text: feature.get('NAME'),
                    fill: new ol.style.Fill({
                        color: [64, 64, 64, 0.45]
                    })
                })
            });
         }
        }

    });

    function dataStyle(feature) {
        var dat = feature.get(currentElement) || '';
        if(dat=='999999'){
            dat = '';

        }
        var style = new ol.style.Style({
            text: new ol.style.Text({
                font: '10px Simhei',
                text: dat,
                fill: new ol.style.Fill({
                    color: [255, 64, 64, 0.75]
                }),
                stroke: new ol.style.Stroke({
                    color: 'rgba(255, 255, 255, 0.7)',
                    width: 2
                 })
            })
            // image: new ol.style.Circle({
            //     radius: 6,
            //     stroke: new ol.style.Stroke({
            //         color: 'white',
            //         width: 2
            //     }),
            //     fill: new ol.style.Fill({
            //         color: 'green'
            //     })
            // })
        });
        return [style];
    }

    var srcData = new ol.source.Vector();
    var lyData = new ol.layer.Vector({
        source: srcData,
        style: dataStyle
    });

    var map = new ol.Map({
        target: 'map',
        layers: [
            lyRaster,
            lyXianline,
            lyXiangPoint,
            lyXianPoint,
            lyData
        ],
        view: new ol.View({
            maxZoom: 11,
            minZoom: 7
        }),
        logo: false,
        controls: mapControls,
        interactions: mapInteractions
    });

    var view = map.getView();
    view.fit(targetExtent, map.getSize());

    $.getJSON('/zh/realtime_latest/')
        .done(function (data) {
            console.dir(data);
            var dt = data['time'];
            var ti = [dt.substr(0, 4), '年', dt.substr(4, 2), '月', dt.substr(6, 2), '日', dt.substr(8, 2), ':', dt.substr(10, 2)].join('');
            $('#timeinfo').html(ti);

            var transform = ol.proj.getTransform('EPSG:4326', 'EPSG:3857');

            srcData.clear();

            $.getJSON('/zh/realtime_data/' + data['relative_dirname'] + '/' + data['filename'])
                .done(function (realtime) {
//                    console.dir(realtime);
                    realtime.forEach(function (rt) {
                        if(rt['sjz'] == "1"){
                            var feature = new ol.Feature(rt);
                            var coordinate = transform([parseFloat(rt['Lon']), parseFloat(rt['Lat'])]);
                            var geometry = new ol.geom.Point(coordinate);
                            feature.setGeometry(geometry);
                            srcData.addFeature(feature);
                        }
                    });
                });
        });

    $('#navbar a').click(function () {
        $('#navbar a').linkbutton('unselect');
        $(this).linkbutton('select');
        switch($(this).text()){
            case '气温':
                currentElement = 'TEM';
                break;
            case '湿度':
                currentElement = 'RHU';
                break;
            case '降水':
                currentElement = 'PRE';
                break;
            case '能见度':
                currentElement = 'VIS_HOR_1MI';
                break;
            case '风':
                currentElement = 'WIN_D_Avg_1mi';
                break;
        }
        lyData.changed();
    });
    $('#navbar a:first').click();
});
