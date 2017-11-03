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
              console.log(data);
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
        console.log(data);
      },
      fail: function(response){
        alert('计算网格数据时发生错误!');
        console.log(response);
      }
    });
  });

});
