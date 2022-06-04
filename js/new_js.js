var ROOT_PATH =
  'https://cdn.jsdelivr.net/gh/apache/echarts-website@asf-site/examples';

var chartDom_left = document.getElementById('left');
var myChart_left = echarts.init(chartDom_left);
var option_left;

$.get('./data/data.json', function (data) {
  myChart_left.setOption(
    (option_left = {
      title: {
        text: '图1',
        left: '1%'
      },
      tooltip: {
        trigger: 'axis'
      },
      grid: {
        left: '5%',
        right: '15%',
        bottom: '10%'
      },
      xAxis: {
        data: data.map(function (item) {
          return item[0];
        })
      },
      yAxis: {},
      toolbox: {
        right: 10,
        feature: {
          dataZoom: {
            yAxisIndex: 'none'
          },
          restore: {},
          saveAsImage: {}
        }
      },
      dataZoom: [
        {
          startValue: '2014-06-01'
        },
        {
          type: 'inside'
        }
      ],
      visualMap: {
        top: 50,
        right: 10,
        pieces: [
          {
            gt: 0,
            lte: 50,
            color: '#93CE07'
          },
          {
            gt: 50,
            lte: 100,
            color: '#FBDB0F'
          },
          {
            gt: 100,
            lte: 150,
            color: '#FC7D02'
          },
          {
            gt: 150,
            lte: 200,
            color: '#FD0100'
          },
          {
            gt: 200,
            lte: 300,
            color: '#AA069F'
          },
          {
            gt: 300,
            color: '#AC3B2A'
          }
        ],
        outOfRange: {
          color: '#999'
        }
      },
      series: {
        name: 'Beijing AQI',
        type: 'line',
        data: data.map(function (item) {
          return item[1];
        }),
        markLine: {
          silent: true,
          lineStyle: {
            color: '#333'
          },
          data: [
            {
              yAxis: 50
            },
            {
              yAxis: 100
            },
            {
              yAxis: 150
            },
            {
              yAxis: 200
            },
            {
              yAxis: 300
            }
          ]
        }
      }
    })
  );
});
option_left && myChart.setOption(option_left);

