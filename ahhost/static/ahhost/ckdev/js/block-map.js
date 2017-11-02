/*
  block-map.js: javascrapt control map block with openlayers-4.2<https://openlayers.org/>
  License: https://raw.githubusercontent.com/openlayers/openlayers/master/LICENSE.md
  Version: v1.0
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/9/23
*/
$(function() {

  var MapSources = {
    'openstreetmap': new ol.source.XYZ({
      url: 'http://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    }),
    'GaoDe': new ol.source.XYZ({
      url: 'http://webst0{1-4}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
    }),
    // english
    'Bing_en': new ol.source.BingMaps({
      imagerySet: 'Road',
      culture: 'zh-Hans',
      key: 'As-OX-1S7VEWejqyGtfUTt4ipr6hLYBJqM4taigxfKb2yT_15JkHPtiNDTsktrBP'
    }),
    'Bing_cn': new ol.source.XYZ({
            tileUrlFunction: function(tileCoord){
              var z = tileCoord[0];
              var x = tileCoord[1];
              var y = -tileCoord[2] - 1;
              var result='', zIndex=0;
              for(; zIndex<z; zIndex++) {
                  result = ((x&1)+2*(y&1)).toString() + result;
                  x >>= 1;
                  y >>= 1;
              }
              return 'http://dynamic.t0.tiles.ditu.live.com/comp/ch/' + result + '?it=G,VE,BX,L,LA&mkt=zh-cn,syr&n=z&og=111&ur=CN';
            }
        }),
    // english
    'Yahoo': new ol.source.XYZ({
        tileSize: 512,
        url:'https://{0-3}.base.maps.api.here.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/512/png8?lg=ENG&ppi=250&token=TrLJuXVK62IQk0vuXFzaig%3D%3D&requestid=yahoo.prod&app_id=eAdkWGYRoc4RfxVo0Z4B'
    }),
    'Baidu': new ol.source.TileImage({
      projection: 'EPSG:3857',
      tileGrid: new ol.tilegrid.TileGrid({
          origin: [0,0], // 设置原点坐标
          resolutions: (function(){  // 设置分辨率
            var resolutions = [];
            var maxZoom = 18;
            // 计算百度使用的分辨率
            for(var i=0; i<=maxZoom; i++){
                resolutions[i] = Math.pow(2, maxZoom-i);
            }
            return resolutions;
          })()
      }),
      tileUrlFunction: function(tileCoord, pixelRatio, proj){
          var z = tileCoord[0];
          var x = tileCoord[1];
          var y = tileCoord[2];

          // 百度瓦片服务url将负数使用M前缀来标识
          if(x<0){
              x = 'M' + (-x);
          }
          if(y<0){
              y = 'M' + (-y);
          }

          return "http://online0.map.bdimg.com/onlinelabel/?qt=tile&x="+x+"&y="+y+"&z="+z+"&styles=pl&udt=20160426&scaler=1&p=0";
      }
    }),
    'google': new ol.source.XYZ({
            url:'http://www.google.cn/maps/vt/pb=!1m4!1m3!1i{z}!2i{x}!3i{y}!2m3!1e0!2sm!3i345013117!3m8!2szh-CN!3scn!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e0'
        })
  };
  var lyRaster = new ol.layer.Tile({
        preload: Infinity,
        source: MapSources['google']
      });

  var map = new ol.Map({
    target: 'map',
    logo: false,
    loadTilesWhileInteracting: true,
    layers: [
      lyRaster
    ],
    view: new ol.View({
        center: ol.proj.transform([117.282699, 31.866942], 'EPSG:4326', 'EPSG:3857'),
        zoom: 7
    }),
    controls: ol.control.defaults().extend([
            new ol.control.FullScreen(),
            new ol.control.ScaleLine(),
            new ol.control.ZoomToExtent()
        ]),
  });
});
