//acionamos o jquery para iniciar a paginação quando o documento estiver "pronto"
$(document).ready(function() {
    //Pegamos o valor selecionado default no select id="qtd"
     var mostrar_por_pagina = 10;
     console.log(mostrar_por_pagina); 
    //quantidade de divs
     var numero_de_itens = ($('#data').children('.content').length) / 2;
     console.log(numero_de_itens);
     //fazemos uma calculo simples para saber quantas paginas existiram
      var numero_de_paginas = Math.ceil(numero_de_itens / mostrar_por_pagina)
    //Colocamos a div class controls dentro da div id pagi
    $('#pagi').append('<div class=controls></div><input id=current_page type=hidden><input id=mostrar_por_pagina type=hidden>');
      $('#current_page').val(0);
      $('#mostrar_por_pagina').val(mostrar_por_pagina);
      //Criamos os links de navegação
      var nevagacao = '<li><a class="prev" onclick="anterior()">Prev</a></li>';
      var link_atual = 0;
      while (numero_de_paginas > link_atual) {
          nevagacao += '<li><a class="page" onclick="ir_para_pagina(' + link_atual + ')" longdesc="' 
          + link_atual + '">' + (link_atual + 1) + '</a></li>';
          link_atual++;
      }
      nevagacao += '<li><a class="proxima" onclick="proxima()">proxima</a></li>';
      //colocamos a nevegação dentro da div class controls
      $('.controls').html("<div class='paginacao'>\
        <ul class='pagination pagination-sm'>"+nevagacao+"</ul></div>");
      //atribuimos ao primeiro link a class active
      $('.controls .page:first').addClass('active');
      $('#data').children().css('display', 'none');
      $('#data').children().slice(0, mostrar_por_pagina).css('display', 'block');
  });