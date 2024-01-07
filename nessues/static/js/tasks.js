// open close task modal
$(function(){
    $(".completeTask").click(function(){
        $('.close_task_modal').show();
        var id = $(this).data('id');
        $(".form-group-id #id_id").val(id);
    })
});
