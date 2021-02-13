const response = await fetch("all_cities.txt");
const data = await response.text();
console.log(data);
