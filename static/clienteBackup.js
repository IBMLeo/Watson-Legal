$(function() {
  var selecionado = "";
  var CPF = [];
  var Desc = [];
  $(".arquivos").hide();
  $(".boxes").show();
  $(".titulos-box").show();

  // Open JSON
  $(".json1").on("click", () => {
    if (selecionado != "") {
      let link =
      "http://localhost:5000/arquivos/Oi/1Descmentacao/" +
      selecionado +
      ".json";
      window.open(link);
    } else {
      alert("Nenhum processo selecionado!");
    }
  });

  // Open PDF
  $(".pdf1").on("click", () => {
    if (selecionado != "") {
      let link =
      "http://localhost:5000/arquivos/Oi/3inicial/" + selecionado + ".txt";
      window.open(link);
    } else {
      alert("Nenhum processo selecionado!");
    }
  });

  // Open JSON 2
  $(".json2").on("click", () => {
    if (selecionado != "") {
      let link =
      "http://localhost:5000/arquivos/Oi/2processo/" + selecionado + ".json";
      window.open(link);
    } else {
      alert("Nenhum processo selecionado!");
    }
  });

  // Open PDF2
  $(".pdf2").on("click", () => {
    if (selecionado != "") {
      let link =
      "http://localhost:5000/arquivos/Oi/4sentenca/" + selecionado + ".txt";
      window.open(link);
    } else {
      alert("Nenhum processo selecionado!");
    }
  });

// HIDE CPF
$('tr .labelCPF').each(function(index, element) {
  CPF[index] = element.innerHTML;
  element.innerHTML = "Ver mais";
});

// HIDE DESCRICAO
$('tr .labelDescricao').each(function(index, element) {
  Desc[index] = element.innerHTML;
  element.innerHTML = "Ver mais"
});

$('tr').mouseenter(function(){
  let ind = $(this).find('.labelCPF').attr('id');
  let and = $(this).find('.labelDescricao').attr('id');
  $(this).find('.labelCPF').text(CPF[ind]);
  $(this).find('.labelDescricao').text(Desc[and]);
  console.log($(this).find('.labelDescricao').text(Desc[and]));
});


$('tr').mouseleave(function(){
 let ind = $(this).find('.labelCPF').attr('id');
 let and = $(this).find('.labelDescricao').attr('id');
 $(this).find('.labelCPF').text("Ver mais");
 $(this).find('.labelDescricao').text("Ver mais");
});

  // Show selected option
  $(".processos").change(() => {
    $(".arquivos").show();
    $(".titulos-box").hide();
    $(".boxes").hide();
    selecionado = $(".processos option:selected").val();
    console.log(selecionado);

    if (selecionado != "selecionar") {
      var dataset = $("tbody").find("tr");
      dataset.show();
      // filter the rows that should be hidden
      dataset
      .filter(function(index, item) {
        return (
          $(item)
          .find("td:first-child")
          .text()
          .split(",")
          .indexOf(selecionado) === -1
          );
      })
      .hide();
    } else {
      $(".arquivos").hide();
      $(".titulos-box").show();
      var rows = $("tbody tr");
      rows.show();
    }
  });

  // Show Modal
});
