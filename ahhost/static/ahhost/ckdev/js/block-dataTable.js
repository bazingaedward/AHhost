/*
  block-dataTable.js: javascrapt control datatable block <https://datatables.net>
  Version: v1.0
  author: Edward Qiu<kxqiu@chinkun.cn>
  created: 2017/9/28
*/

$(function(){
    $('#datatable').DataTable({
      ajax: '/data/load'
    });

});
