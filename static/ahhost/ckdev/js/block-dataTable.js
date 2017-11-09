/*
  block-dataTable.js: javascrapt control datatable block <https://datatables.net>
  Version: v1.0
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/9/28
*/

$(function(){
    var BUTTON = {};
    var table = $('#datatable').DataTable({
            ajax: '/data/load',
            deferRender: true,
            // "scrollX": true,
            "dom": "<'row'<'col-sm-6'B><'col-sm-6'f>>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'row'<'col-sm-5'i><'col-sm-7'p>>",
            "language": {
              "info": "显示第 _PAGE_／_PAGES_ 页",
              "search": "搜索：",
              "lengthMenu": "每页显示 _MENU_ 条数据"
            },
            "columnDefs": [
              {
                "targets": [2,3,4,5,6,7,8,9],
                "visible": false
              }
            ],
            buttons: [
              {
                  text: '更新',
                  action: function ( e, dt, node, config ) {
                      dt.ajax.reload();
                  }
              },
              {
                  text: '新增',
                  action: function ( e, dt, node, config ) {
                    BUTTON['type'] = 'add';
                    $('#dt_editor_modal input').val("");
                    $('#dt_editor_modal').modal('show');
                  }
              },
              {
                extend: 'selectedSingle',
                text: '编辑',
                action : function(e, dt, node, config){
                  BUTTON['type'] = 'update'
                  var data = this.row({selected: true}).data();
                  $('#dt_editor_modal input').val(function(index, value){
                    return data[index];
                  });
                  $('#dt_editor_modal input:first').prop('disabled', true);
                  $('#dt_editor_modal').modal('show');
                }
              },
              {
                extend: 'selected',
                text: '删除',
                action: function(e, dt, node, config){
                  var names = {}
                  this.rows({selected: true}).data().each(function(d, index){
                    names[index] = d[0]
                  });

                  $.ajax({
                    type: "POST",
                    url: "/data/delete",
                    data: names,
                    success: function(data){
                      console.log(data);

                    },
                    fail: function(error){
                      console.log(error);
                    }
                  });
                  this.rows({selected: true}).remove().draw();
                }
              },
              {
                extend: 'selectAll',
                text: '全选',
              },
              {
                extend: 'selectNone',
                text: '取消选择'
              },
              {
                extend: 'csv',
                text: 'CSV导出'
              },
              {
                extend: 'excel',
                text: 'Excel导出'
              }
            ],
            select: true
      });

      // datable add Listener for addition and editing
      $('#dt_editor_button').click(function(){
        var parameter = {};
        $('#dt_editor_modal input').val(function(index, value){
          parameter[index] = value;
        });
        //check data[0]
        if(!parameter[0]){
          alert('企业名称必须填写');
          return
        }

        if(BUTTON['type'] == 'update'){
          //编辑内容
          $.ajax({
            type: "POST",
            url: "/data/update",
            data: parameter,
            success: function(data){
              cleanModal();
              // $('#dt_editor_modal input:first').prop('disabled', false);
              $('#dt_editor_modal input:first').prop('disabled', false);
              console.log(data);
              //todo: datatable更新内容
            },
            fail: function(error){
              console.log(error);
            }
          });
        }else if(BUTTON['type'] == 'add'){
          //创建内容
          $.ajax({
            type: 'POST',
            url: '/data/add',
            data: parameter,
            success: function(data){
              cleanModal();
              //todo: datatable更新内容
            },
            fail: function(error){
              console.log(error);
            }
          });
        }

        function cleanModal(){
          //hidden modal and update data
          table.ajax.reload();
          $('#dt_editor_modal').modal('hide');
        }
      });

});
