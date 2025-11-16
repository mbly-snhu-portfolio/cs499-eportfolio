/**
 * Breed analytics chart component using ECharts.
 */
import { useState } from 'react';
import ReactECharts from 'echarts-for-react';
import './BreedChart.css';

const CHART_TYPES = [
  { value: 'bar', label: 'Bar' },
  { value: 'pie', label: 'Pie' },
  { value: 'treemap', label: 'Treemap' },
];

const BreedChart = ({ data }) => {
  const [chartType, setChartType] = useState('bar');

  const getChartOption = () => {
    const breedNames = data.map((item) => item.breed || 'Unknown');
    const breedCounts = data.map((item) => item.count || 0);

    if (chartType === 'bar') {
      return {
        title: {
          text: 'Top Breeds',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: breedNames,
          axisLabel: {
            rotate: 45,
            interval: 0,
          },
        },
        yAxis: {
          type: 'value',
          name: 'Count',
        },
        series: [
          {
            data: breedCounts,
            type: 'bar',
            itemStyle: {
              color: '#667eea',
            },
          },
        ],
      };
    } else if (chartType === 'pie') {
      return {
        title: {
          text: 'Top Breeds',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
        },
        series: [
          {
            type: 'pie',
            radius: '60%',
            data: data.map((item) => ({
              value: item.count || 0,
              name: item.breed || 'Unknown',
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      };
    } else if (chartType === 'treemap') {
      return {
        title: {
          text: 'Top Breeds',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
        },
        series: [
          {
            type: 'treemap',
            data: data.map((item) => ({
              value: item.count || 0,
              name: item.breed || 'Unknown',
            })),
            label: {
              show: true,
              formatter: '{b}: {c}',
            },
          },
        ],
      };
    }
    return {};
  };

  return (
    <div className="breed-chart-container">
      <div className="chart-header">
        <h2>Breed Analytics</h2>
        <div className="chart-type-selector">
          {CHART_TYPES.map((type) => (
            <button
              key={type.value}
              className={`chart-type-btn ${chartType === type.value ? 'active' : ''}`}
              onClick={() => setChartType(type.value)}
            >
              {type.label}
            </button>
          ))}
        </div>
      </div>
      {data.length === 0 ? (
        <div className="no-chart-data">No breed data available</div>
      ) : (
        <ReactECharts
          option={getChartOption()}
          style={{ height: '400px', width: '100%' }}
          opts={{ renderer: 'svg' }}
        />
      )}
    </div>
  );
};

export default BreedChart;

