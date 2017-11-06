/*
  block-dataTable.js: javascrapt control datatable block <https://datatables.net>
  Version: v1.0
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/9/28
*/

$(function(){
    $('#datatable').DataTable({
      ajax: '/data/load',
      deferRender: true,
      "dom": "<'row'<'col-sm-6'B><'col-sm-6'f>>" +
              "<'row'<'col-sm-12'tr>>" +
              "<'row'<'col-sm-5'i><'col-sm-7'p>>",
      "language": {
        "info": "显示第 _PAGE_／_PAGES_ 页",
        "search": "搜索：",
        "lengthMenu": "每页显示 _MENU_ 条数据"
      },
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
                dt.ajax.reload();
            }
        },
        {
          extend: 'selectedSingle',
          text: '编辑',
          action : function(e, dt, node, config){
            console.log(this.row({selected: true}).data().toArray());
          }
        },
        {
          extend: 'selected',
          text: '删除'
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

});
