$(function () {
    $('.create_workspace').on('click', () => {
        let data = $('.workspace_name').val();
        let json = { 'text': data }
        $.post('/cria', json, (res) => {
            alert(res);
        });
    });
});