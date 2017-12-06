/*
  block-dialog.js: javascrapt for bootstrap modal
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/10/26
*/

$(function(){
  // modal for setting
  $('#setting_button').click(function(){

  });

  // modal for province and city shapefile creation
  // --- init ----
  var PROVINCES = [];
  var CITIES = [];
  var SELECTRANGE = {};
  $.ajax({
      type: 'POST',
      url: '/gis/province/get',
      success: function (data) {
          PROVINCES = $.map(data, function(value){
            return value;
          });
          var elements = $.map(data, function(value){
          return "<option value=\""+value['ID']+"\">"+value['name']+'</option>';
        });
        // province modal select
        $('#province_shapefile_modal select').html(elements.join(""));
        //raster area select
        $('#rasterAreaSelect').html(elements.join(""));
      },
      fail: function (err) {
          console.log(err);
      }
    });
    $.ajax({
        type: 'POST',
        url: '/gis/city/get',
        success: function (data) {
            CITIES = $.map(data, function(value){
              return value;
            });
            var elements = $.map(data, function(value){
            return "<option value=\""+value['ID']+"\">"+value['name']+'</option>';
          });
          $('#city_shapefile_modal select').html(elements.join(""));
        },
        fail: function (err) {
            console.log(err);
        }
      });
  // --- submit button ----
  $('#province_shapefile_button').click(function(){
    var provinceIdx = PROVINCES.findIndex(function(item){
      return item['ID'] == $('#province_shapefile_modal select').val();
    });
    var resolution = $('#province_shapefile_modal .resolution').val();
    // loading label
    $('#province_shapefile_modal .modal_info').empty();
    $('#province_shapefile_modal .modal_info').append("<div class=\"alert alert-info\" \
    role=\"alert\">正在处理，请稍后...</div>");
    // register global variable: SELECTRANGE
    SELECTRANGE = PROVINCES[provinceIdx];
    // running ajax
    $.ajax({
        type: 'POST',
        url: '/form/shapefile',
        data: {
          'miny': PROVINCES[provinceIdx]['miny'],
          'minx': PROVINCES[provinceIdx]['minx'],
          'maxy': PROVINCES[provinceIdx]['maxy'],
          'maxx': PROVINCES[provinceIdx]['maxx'],
          'resolution': resolution
        },
        success: function (data) {
          // console.log(data);
          // complete label
          $('#province_shapefile_modal .modal_info').empty();
          $('#province_shapefile_modal .modal_info').append("<div class=\"alert alert-success\" role=\"alert\">文件生成成功！</div>");
        },
        fail: function (response) {
            alert('生成矢量图形时发生错误!');
            console.log(response);
        }
      });
  });
  $('#city_shapefile_button').click(function(){
    var cityIdx = CITIES.findIndex(function(item){
      return item['ID'] == $('#city_shapefile_modal select').val();
    });
    var resolution = $('#city_shapefile_modal .resolution').val();
    // loading label
    $('#city_shapefile_modal .modal_info').empty();
    $('#city_shapefile_modal .modal_info').append("<div class=\"alert alert-info\" \
    role=\"alert\">正在处理，请稍后...</div>");
    // register global variable: SELECTRANGE
    SELECTRANGE = CITIES[cityIdx];
    // running ajax
    $.ajax({
        type: 'POST',
        url: '/form/shapefile',
        data: {
          'miny': CITIES[cityIdx]['miny'],
          'minx': CITIES[cityIdx]['minx'],
          'maxy': CITIES[cityIdx]['maxy'],
          'maxx': CITIES[cityIdx]['maxx'],
          'resolution': resolution
        },
        success: function (data) {
          // console.log(data);
          // complete label
          $('#city_shapefile_modal .modal_info').empty();
          $('#city_shapefile_modal .modal_info').append("<div class=\"alert alert-success\" role=\"alert\">文件生成成功！</div>");
        },
        fail: function (response) {
            alert('生成矢量图形时发生错误!');
            console.log(response);
        }
      });
  });

  // modal for Raster Calculate
  $('#calculate_button').click(function(){
    //form elements values
    var provinceIdx = PROVINCES.findIndex(function(item){
      return item['ID'] == $('#rasterAreaSelect').val();
    });//!important 省级区域
    var statisticType = $("input[name='st']:checked").val();
    var gridResolution = $('#gridResolutionSelect').val();
    var pollutionType = $('#pollutionTypeSelect').val();
    var pollutionSum = $('#pollutionSumValue').val();
    // check required input
    if(!pollutionSum){
      alert("区域排放总量必须输入!!!");
      return;
    }
    //loading label
    $('#raster_modal .modal_info').empty();
    $('#raster_modal .modal_info').append("<div class=\"alert alert-info\" \
      role=\"alert\">正在处理，请稍后...</div>");
    // running ajax
    $.ajax({
      url: '/form/raster',
      type: 'POST',
      data: {
        'AreaID': PROVINCES[provinceIdx]['ID'], //'340100'
        'st'  : statisticType,//'Population'
        'resolution': gridResolution,//'10'
        'type': pollutionType,//'so2'
        'sum': pollutionSum, //'100'
        'minx': SELECTRANGE['minx'],
        'miny': SELECTRANGE['miny'],
        'maxx': SELECTRANGE['maxx'],
        'maxy': SELECTRANGE['maxy'],
      },
      success: function(data){
        $('#raster_modal .modal_info').empty();
        $('#raster_modal .modal_info').append("<div class=\"alert alert-success\" role=\"alert\">计算完成，导出文件！</div>");
        window.open('media/netcdf4/data.nc');
        // console.log(data);
      },
      fail: function(response){
        alert('计算网格数据时发生错误!');
        console.log(response);
      }
    });
  });

  // modal for file upload
  $('#upload_button').click(function(){
    console.log($('#file_upload_modal input:file').val())
  });

  // modal for myFilter
  var SQLITE_MAP = {
		sStart:'sw',
		sContain:'ct',
		sNotContain:'nct',
		sFinish:'fw',
		sInList:'in',
		sIsNull:'null',
		sIsNotNull:'nn',
		sBetween:'bw',
		sNotBetween:'nbw'
  }
  $("#myFilter").structFilter({
      fields: [
          {id:"ahhost_pointsource.areaId", type:"text", label:"行政区划代码"},
          {id:"ahhost_pointsourcedata.SO2", type:"number", label:"SO2"},
          {id:"ahhost_pointsourcedata.NOX", type:"number", label:"NOx"},
          {id:"ahhost_pointsourcedata.CO", type:"number", label:"CO"},
          {id:"ahhost_pointsourcedata.PM", type:"number", label:"PM"},
          {id:"ahhost_pointsourcedata.PM10", type:"number", label:"PM10"},
          {id:"ahhost_pointsourcedata.PM25", type:"number", label:"PM2.5"},
          {id:"ahhost_pointsourcedata.NMVOC", type:"number", label:"NMVOC"},
          {id:"ahhost_pointsourcedata.NH3", type:"number", label:"NH3"},
      ],
      buttonLabels: true,
      submitButton: true,
      clearButton: true
  });
  $("#myFilter").on("submit.search", function(event){
    var conditions = $("#myFilter").structFilter('val');
    var sql = [];
    conditions.forEach(function(item){
      // areaId
      switch(item['operator']['value']){
        case 'eq':
          sql.push(item['field']['value']+"="+item['value']['label']);
          break;
        case 'ne':
          sql.push(item['field']['value']+"!="+item['value']['value']);
          break;
        case 'gt':
          sql.push(item['field']['value']+">"+item['value']['value']);
          break;
        case 'lt':
          sql.push(item['field']['value']+"<"+item['value']['value']);
          break;
        case 'sw': break;
        case 'ct': break;
        case 'nct': break;
        case 'fw': break;
        case 'in': break;
        case 'null': break;
        case 'nn': break;
        case 'bw': break;
        case 'nbw': break;
        default:
          console.log('filter operator not found!');
      }
    });
    $.ajax({
      type: "POST",
      url: "/data/filter",
      data: {
        'sql': sql.join(' AND ')
      },
      success: function(res){
        console.log(res);
        if(res['status'] == 'OK'){
          filterTable
            .clear()
            .rows.add(res['data'])
            .draw();

          if(res['total']){
            var json = $.parseJSON(res['total']);

            $('#dt-statistics tfoot th').slice(2, 10).each(function(index, element){
              $(element).text(json[(index+2).toString()]);
            });
          }
        }
      },
      fail: function(error){
        console.log('Filter:', error);
      }
    })
});


  var filterTable = $('#dt-statistics').DataTable({
        "dom": "<'row'<'col-sm-3'f><'col-sm-9'p>>" +
                "<'row'<'col-sm-12'tr>>",
        "language": {
          "search": "搜索："
        },
        fixedHeader: {
          header: true,
          footer: true
        }
      });

  // interpolation modal
  $('#interpolation_button').click(function(){
    // get form elements values
    var variables = $('input[name=variables]:checked').map(function(){
      return this.value;
    }).toArray();
    var method = $('#interpolation_modal select.method').val();
    var resolution = $('#interpolation_modal select.resolution').val();
    //loading label
    $('#interpolation_modal .modal_info').empty();
    $('#interpolation_modal .modal_info').append("<div class=\"alert alert-info\" \
      role=\"alert\">正在插值，请稍后...</div>");
    //running ajax
    $.ajax({
      type: "POST",
      url: "/form/interpolate",
      data: {
        'var': JSON.stringify(variables),
        'method': method,
        'resolution': resolution
      },
      success: function(data){
        $('#interpolation_modal .modal_info').empty();
        $('#interpolation_modal .modal_info').append(
          "<div class=\"alert alert-success\" role=\"alert\">计算完成，导出文件！</div>");
        // console.log(data);
        window.open('media/netcdf4/Interpolate.nc');
      },
      fail: function(error){
        console.log('hello');
      }
    })
  });

  // help modal
  $('#tab-help').tab()
});
