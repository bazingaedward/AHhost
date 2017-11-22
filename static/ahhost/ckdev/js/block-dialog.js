/*
  block-dialog.js: javascrapt for bootstrap modal
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/10/26
*/

$(function(){
  // modal for setting
  $('#setting_button').click(function(){

  });

  // modal for shapefile
  $('#shapefile_button').click(function(){
    var rangeIdx = $('#shapefile_modal select').val();
    var resolution = $('#resolution').val();

    $('#shapefile_modal .modal_info').empty();
    $('#shapefile_modal .modal_info').append("<div class=\"alert alert-info\" role=\"alert\">正在处理，请稍后...</div>");
    switch(rangeIdx){
      //安徽省
      case "1":
        var latlon = [28.949517145902025,112.7214002962958,35.06114891777644,121.73919504342172];
        var location = 'ah';
        // var latlon = 'test';
        break;
      //江苏省
      case "2":
        console.log(2);
        break;
      //浙江省
      case "3":
        console.log(3);
        break;
      //上海市
      case "4":
        console.log(4);
        break;
      default:
        alert("未知的shapefile范围类型码！");
    }

    if(latlon){
      $.ajax({
          type: 'POST',
          url: '/form/shapefile',
          data: {
            'location':location,
            'miny': latlon[0],
            'minx': latlon[1],
            'maxy': latlon[2],
            'maxx': latlon[3],
            'resolution': resolution
          },
          success: function (data) {
            $('#shapefile_modal .modal_info').empty();
            $('#shapefile_modal .modal_info').append("<div class=\"alert alert-success\" role=\"alert\">文件生成成功！</div>");
              // console.log(data);
          },
          fail: function (response) {
              alert('生成矢量图形时发生错误!');
              console.log(response);
          }
        });
    }
  });

  // modal for Raster Calculate
  $('#calculate_button').click(function(){
    var rasterArea = $('#rasterAreaSelect').val();
    var statisticType = $("input[name='st']:checked").val();
    var gridResolution = $('#gridResolutionSelect').val();
    var pollutionType = $('#pollutionTypeSelect').val();
    var pollutionSum = $('#pollutionSumValue').val();

    if(!pollutionSum){
      alert("区域排放总量必须输入!!!");
      return;
    }

    $('#raster_modal .modal_info').empty();
    $('#raster_modal .modal_info').append("<div class=\"alert alert-info\" role=\"alert\">正在处理，请稍后...</div>");
    $.ajax({
      url: '/form/raster',
      type: 'POST',
      data: {
        'Area': rasterArea, //'AH'
        'st'  : statisticType,//'Population'
        'resolution': gridResolution,//'10'
        'type': pollutionType,//'so2'
        'sum': pollutionSum //'100'
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
});
