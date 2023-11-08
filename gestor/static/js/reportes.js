const getOptionChart = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/gestor/get_chart/");
    return await response.json();
  } catch (ex) {
    alert(ex);
  }
};

const getOptionChart1 = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/gestor/get_chart2/");
    return await response.json();
  } catch (ex) {
    alert(ex);
  }
};

const initChart = async () => {
  const myChart = echarts.init(document.getElementById("chart"));

  myChart.setOption(await getOptionChart());

  myChart.resize();
};

const initChart1 = async () => {
  const myChart1 = echarts.init(document.getElementById("chart1"));

  myChart1.setOption(await getOptionChart1());

  myChart1.resize();
};



window.addEventListener("load", async () => {
  await initChart();
  await initChart1();
});
