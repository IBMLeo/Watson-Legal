$(function() {
  var selecionado = "";

  // Show selected option
  $(".processos").change(() => {
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
});
