$(function () {
    var selecionado = "";
    $('.arquivos').hide()
    $('.boxes').show()
    $('.titulos-box').show()
    $(".processos").change(() => {
        $('.arquivos').show()
        $('.titulos-box').hide()
        $('.boxes').hide()
        selecionado = $(".processos option:selected").val();
        if (selecionado != 'selecionar') {
            var dataset = $('#tabelao tbody').find('tr');
            dataset.show();
            // filter the rows that should be hidden
            dataset.filter(function (index, item) {
                return $(item).find('td:first-child').text().split(',').indexOf(selecionado) === -1;
            }).hide();
        } else {
            $('.arquivos').hide()
            $('.titulos-box').show()
            var rows = $('#tabelao tbody tr');
            rows.show();
        }
    });

    $('.json1').on('click', () => {
        if (selecionado != "") {
            let link = 'http://localhost:5000/arquivos/Oi/1movimentacao/' + selecionado + '.json'
            window.open(link)
        } else {
            alert('Nenhum processo selecionado!')
        }
    });

    $('.pdf1').on('click', () => {
        if (selecionado != "") {
            let link = 'http://localhost:5000/arquivos/Oi/3inicial/' + selecionado + '.txt'
            window.open(link)
        } else {
            alert('Nenhum processo selecionado!')
        }
    });

    $('.json2').on('click', () => {
        if (selecionado != "") {
            let link = 'http://localhost:5000/arquivos/Oi/2processo/' + selecionado + '.json'
            window.open(link)
        } else {
            alert('Nenhum processo selecionado!')
        }
    });

    $('.pdf2').on('click', () => {
        if (selecionado != "") {
            let link = 'http://localhost:5000/arquivos/Oi/4sentenca/' + selecionado + '.txt'
            window.open(link)
        } else {
            alert('Nenhum processo selecionado!')
        }
    });

    var CPF = [];
    var Movi = [];

    $('tr .labelCPF').each(function(index, element) {
        CPF[index] = element.innerHTML;
        element.innerHTML = "Ver mais";
    });

    $('tr .labelMovi').each(function(index, element) {
        Movi[index] = element.innerHTML;
        element.innerHTML = "Ver mais"
    });

    $('tr').mouseenter(function(){
        let ind = $(this).find('.labelCPF').attr('id');
        $(this).find('.labelCPF').text(CPF[ind]);
        $(this).find('.labelMovi').text(Movi[ind]);
    });

    $('tr').mouseleave(function(){
     let ind = $(this).find('.labelCPF').attr('id');
     $(this).find('.labelCPF').text("Ver mais");
     $(this).find('.labelMovi').text("Ver mais");
 });
});





