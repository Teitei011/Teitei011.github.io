async function setup(locationName) {
    const covidCases = await getData(locationName);
  
    console.log(covidCases);
  
    graphIt(
      "myChart1",
      "Total de Casos: " + locationName,
      "line",
      covidCases.date,
      covidCases.cases
    );

    setupBoxWithData(covidCases);
}