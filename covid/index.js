setup("Botucatu");
createAllCitiesOptions();
let covidGraphs = [];

//console.log(covidGraphs);

async function createAllCitiesOptions() {
  const response = await fetch("all_cities.txt");
  const data = await response.text();
  const table = data.split("\n");

  console.log("Passei por aqui!");
  table.forEach(function (row) {
    let dropdown = document.createElement("li");   // Create a <li> element
    dropdown.innerHTML = `<a class="dropdown-item" onclick="myFunction(this, '` +
    row +
    `')">` +
    row +
    `</a>`;                   // Insert text
    document.getElementById("myInput").appendChild(dropdown);
  });
}

function removeGraphs() {
  for (let i = 0; i < 6; i++) {
    covidGraphs[i].destroy();
  }
  covidGraphs = [];
}

function myFunction(elmnt, answer) {
  removeGraphs();
  setup(answer);
  console.log("Changing to " + answer);
  //console.log(covidGraphs);
}

async function setup(locationName) {
  const covidCases = await getData(locationName);

  console.log(covidCases);

  graphIt(
    "myChart1",
    "Total de Casos " + locationName,
    covidCases.date,
    covidCases.cases
  );
  graphIt(
    "myChart2",
    "Total de Mortes " + locationName,
    covidCases.date,
    covidCases.deaths
  );

  graphIt(
    "myChart3",
    "Casos diários " + locationName,
    covidCases.date,
    covidCases.daily_cases
  );
  graphIt(
    "myChart4",
    "Mortes diárias " + locationName,
    covidCases.date,
    covidCases.daily_deaths
  );

  graphIt(
    "myChart5",
    "Média móvel de casos " + locationName,
    covidCases.date,
    covidCases.cases_moving_average
  );
  graphIt(
    "myChart6",
    "Média móvel de mortes " + locationName,
    covidCases.date,
    covidCases.deaths_moving_average
  );

  document.getElementById("casos").innerHTML =
    covidCases.cases[covidCases.cases.length - 2];
  document.getElementById("mortes").innerHTML =
    covidCases.deaths[covidCases.deaths.length - 2];
  document.getElementById("Titulo").innerHTML = "<h1>" + locationName + "</h1>";
}

async function graphIt(chartId, label, date, data_covid) {
  const ctx = document.getElementById(chartId).getContext("2d");
  covidGraphs.push(
    new Chart(ctx, {
      type: "line",
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
  });

  return {
    date,
    cases,
    deaths,
    daily_cases,
    daily_deaths,
    cases_moving_average,
    deaths_moving_average,
  };
}
