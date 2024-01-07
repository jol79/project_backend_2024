$(function(){
    $(".createTable").click(function(){
        $('.create_table_modal').show();
    })
});

$(function(){
    $(".deleteRoom").click(function(){
        $('.delete_room_modal').show();
        var id = $(this).data('id');
        $(".form-group-id #id-id").val(id);
    })
});
$(function(){
    $(".deleteGroup").click(function(){
        $('.delete_group_modal').show();
        var id = $(this).data('id');
        $(".form-group-id #id-id").val(id);
    })
});

$(function(){
    $(".inviteUser").click(function(){
        $('.invite_user_modal').show();
    })
});
