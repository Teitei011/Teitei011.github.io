
let covidGraphs = [];
setup("Brasil");
//console.log(covidGraphs);



function removeGraphs() {
  for (let i = 0; i < covidGraphs.length; i++) {
    covidGraphs[i].destroy();
  }
  covidGraphs = [];
}

function updateGraphs(answer) {
  removeGraphs();
  setup(answer);
  console.log("Changing to " + answer);
  //console.log(covidGraphs);
}

async function setup(locationName) {
  const covidCases = await getData(locationName);

  graphIt(
    "TotalDeCasos",
    "Total de Casos: " + locationName,
    "line",
    covidCases.date,
    covidCases.cases
  );
  graphIt(
    "TotalDeMortes",
    "Total de Mortes: " + locationName,
    "line",
    covidCases.date,
    covidCases.deaths
  );

  graphIt(
    "CasosDiarios",
    "Casos diários: " + locationName,
    "line",
    covidCases.date,
    covidCases.daily_cases
  );
  graphIt(
    "MortesDiarias",
    "Mortes diárias: " + locationName,
    "line",
    covidCases.date,
    covidCases.daily_deaths
  );

  graphIt(
    "MovelCasos",
    "Média móvel de casos: " + locationName,
    "line",
    covidCases.date,
    covidCases.cases_moving_average
  );
  graphIt(
    "MovelMortes",
    "Média móvel de mortes: " + locationName,
    "line",
    covidCases.date,
    covidCases.deaths_moving_average
  );


    console.log(covidCases);

  setupBoxWithData(covidCases, locationName);
}



function setupBoxWithData(covidCases, locationName){

  document.getElementById("casos").innerHTML = change2Dot(covidCases.cases[covidCases.cases.length - 1]);
  document.getElementById("mortes").innerHTML = change2Dot(covidCases.deaths[covidCases.deaths.length - 1]);
  document.getElementById("Titulo").innerHTML = "<h1>" + locationName + "</h1>";

  let variacao_casos =  -100*(1 - covidCases.cases_moving_average[covidCases.cases_moving_average.length - 1] / covidCases.cases_moving_average[covidCases.cases_moving_average.length - 15]);
  let variacao_mortes =  -100*(1 - covidCases.deaths_moving_average[covidCases.deaths_moving_average.length - 1] / covidCases.deaths_moving_average[covidCases.deaths_moving_average.length - 15]);
  

  if(variacao_casos > 0){
    variacao_casos = "+" + change2Dot(parseFloat(variacao_casos).toFixed(2));
  } else{
    variacao_casos = change2Dot(changeSymbol(parseFloat(variacao_casos).toFixed(2)));
  }
  if (variacao_mortes > 0){
    variacao_mortes = "+" + change2Dot(parseFloat(variacao_mortes).toFixed(2));
  } else{
    variacao_mortes = change2Dot(changeSymbol(parseFloat(variacao_mortes).toFixed(2)));
  }

  document.getElementById("variacao_casos").innerHTML =  changeSymbol(variacao_casos) + "%";
  document.getElementById("variacao_mortes").innerHTML =  changeSymbol(variacao_mortes) + "%";

  document.getElementById("novos_casos").innerHTML = change2Dot( parseFloat(covidCases.cases_moving_average[covidCases.sum_of_daily_cases_week.length -1]).toFixed(0));
  document.getElementById("novas_mortes").innerHTML = change2Dot(parseFloat(covidCases.deaths_moving_average[covidCases.sum_of_daily_deaths_week.length -1]).toFixed(0));
  //document.getElementById("DadosAtualizados").innerHTML = "<center>Esperando o Ministério da Saúde atualizar seus dados: " +"</center>" ;
 
  document.getElementById("DadosAtualizados").innerHTML = "<center>Dados atualizados no dia: "  + covidCases.date[covidCases.cases.length -1] + " 21:00" +"</center>" ;
  // document.getElementById("DadosAtualizados").innerHTML = "<center>Dados atualizados no dia: "  + "24/02/2021" + " 09:53" +"</center>" ;
}


async function graphIt(chartId, label, type, date, data_covid) {
  const ctx = document.getElementById(chartId).getContext("2d");
  covidGraphs.push(
    new Chart(ctx, {
      type: type,
      data: {
        labels: date,
        datasets: [
          {
            label: label,
            data: data_covid,
            fill: true,
            borderColor: "rgba(0, 125, 255, 1)",
            backgroundColor: "rgba(0, 0, 255, 0.5)",
            borderWidth: 1,
          },
        ],
      },
      options: {},
    })
  );
}

async function getData(locationName) {

  let fixer = 1;
  if (name === "Brasil") {
    fixer = 0;
  }

  const response = await fetch("brazil/" + locationName + ".csv");
  const data = await response.text();

  const date = [];
  const cases = [];
  const deaths = [];
  const daily_cases = [];
  const daily_deaths = [];
  const cases_moving_average = [];
  const deaths_moving_average = [];
  const sum_of_daily_cases_week = [];
  const sum_of_daily_deaths_week = [];
  const table = data.split("\n").slice(1);


 table.forEach((row) => {
    const cols = row.split(",");
    date.push(convertString2Date(cols[1 + fixer]));
    cases.push(Number(cols[2 + fixer]));
    dailyCases.push(Number(cols[3 + fixer]));
    deaths.push(Number(cols[4 + fixer]));
    dailyDeaths.push(Number(cols[5 + fixer]));

    casesMovingAverage.push(Number(cols[6 + fixer]));
    deathsMovingAverage.push(Number(cols[7 + fixer]));

  });



        // Brasil dataset is different than the rest 
      date.pop();
      cases.pop();
      deaths.pop();
      daily_cases.pop();
      daily_deaths.pop();
      cases_moving_average.pop();
      deaths_moving_average.pop();
      sum_of_daily_cases_week.pop();
      sum_of_daily_deaths_week.pop();


   // date = await changeDateOrderArray(date);


  return {
    date,
    cases,
    daily_cases,
    deaths,
    daily_deaths,
    cases_moving_average,
    deaths_moving_average,
    sum_of_daily_cases_week,
    sum_of_daily_deaths_week
  };
}

function change2Dot(nStr){
  nStr += '';
  let x = nStr.split('.');
  let x1 = x[0];
  let x2 = x.length > 1 ? '.' + x[1] : '';
  let rgx = /(\d+)(\d{3})/;
  while (rgx.test(x1)) {
   x1 = x1.replace(rgx, '$1' + '.' + '$2');
  }
  return x1 + x2;
 }


 function changeSymbol(value){
  return  value.replace(".", ',');

 } 
