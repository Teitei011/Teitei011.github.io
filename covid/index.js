
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
    "myChart1",
    "Total de Casos: " + locationName,
    "line",
    covidCases.date,
    covidCases.cases
  );
  graphIt(
    "myChart2",
    "Total de Mortes: " + locationName,
    "line",
    covidCases.date,
    covidCases.deaths
  );

  graphIt(
    "myChart3",
    "Casos diários: " + locationName,
    "line",
    covidCases.date,
    covidCases.daily_cases
  );
  graphIt(
    "myChart4",
    "Mortes diárias: " + locationName,
    "line",
    covidCases.date,
    covidCases.daily_deaths
  );

  graphIt(
    "myChart5",
    "Média móvel de casos: " + locationName,
    "line",
    covidCases.date,
    covidCases.cases_moving_average
  );
  graphIt(
    "myChart6",
    "Média móvel de mortes: " + locationName,
    "line",
    covidCases.date,
    covidCases.deaths_moving_average
  );


    console.log(covidCases);

  setupBoxWithData(covidCases, locationName);
}



function setupBoxWithData(covidCases, locationName){

  document.getElementById("casos").innerHTML = addCommas(covidCases.cases[covidCases.cases.length - 1]);
  document.getElementById("mortes").innerHTML = addCommas(covidCases.deaths[covidCases.deaths.length - 1]);
  document.getElementById("Titulo").innerHTML = "<h1>" + locationName + "</h1>";

  let variacao_casos =  -100*(1 - covidCases.cases_moving_average[covidCases.cases_moving_average.length - 1] / covidCases.cases_moving_average[covidCases.cases_moving_average.length - 15]);
  let variacao_mortes =  -100*(1 - covidCases.deaths_moving_average[covidCases.deaths_moving_average.length - 1] / covidCases.deaths_moving_average[covidCases.deaths_moving_average.length - 15]);
  

  if(variacao_casos > 0){
    variacao_casos = "+" + addCommas(parseFloat(variacao_casos).toFixed(2));
  } else{
    variacao_casos = addCommas(isANumber(parseFloat(variacao_casos).toFixed(2)));
  }
  if (variacao_mortes > 0){
    variacao_mortes = "+" + addCommas(parseFloat(variacao_mortes).toFixed(2));
  } else{
    variacao_mortes = addCommas(isANumber(parseFloat(variacao_mortes).toFixed(2)));
  }

  document.getElementById("variacao_casos").innerHTML =  isANumber(variacao_casos) + "%";
  document.getElementById("variacao_mortes").innerHTML =  isANumber(variacao_mortes) + "%";

  document.getElementById("novos_casos").innerHTML = addCommas( parseFloat(covidCases.sum_of_daily_cases_week[covidCases.sum_of_daily_cases_week.length -1]).toFixed(0));
  document.getElementById("novas_mortes").innerHTML = addCommas(parseFloat(covidCases.sum_of_daily_deaths_week[covidCases.sum_of_daily_deaths_week.length -1]).toFixed(0));
  //document.getElementById("DadosAtualizados").innerHTML = "<center>Esperando o Ministério da Saúde atualizar seus dados: " +"</center>" ;
 
 
  document.getElementById("DadosAtualizados").innerHTML = "<center>Dados atualizados no dia: "  + changeDateOrder(covidCases.date[covidCases.cases.length -1]) + " 20:00" +"</center>" ;

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
    date.push(cols[1]);
    cases.push(cols[2]);
    deaths.push(cols[4]);

    daily_cases.push(cols[3]);
    daily_deaths.push(cols[5]);
    cases_moving_average.push(cols[6]);
    deaths_moving_average.push(cols[7]);

    sum_of_daily_cases_week.push(cols[8]);
    sum_of_daily_deaths_week.push(cols[9]);
    });


      // Removing the undefined value
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

function addCommas(nStr){
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


 function isANumber(value){
  return  value.replace(".", ',');
 } 

 async function changeDateOrderArray(array){
  let new_array = [];
  for (let i = 0; i < array.length; i++){
    let x = array[i].split('-');
    new_array.push( x[2] + "/" + x[1] + "/" + x[0]);
  }
  return new_array;
}

 function changeDateOrder(nStr){
  let x = nStr.split('-');
  return x[2] + "/" + x[1] + "/" + x[0];
 }

//          <img src="https://profile-counter.glitch.me/Teitei011/count.svg"></img> 
