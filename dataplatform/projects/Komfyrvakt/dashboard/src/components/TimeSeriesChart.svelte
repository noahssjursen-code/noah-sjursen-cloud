<script lang="ts">
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import type { TimeSeries } from '../lib/api';
  
  export let timeSeries: TimeSeries;
  
  let canvas: HTMLCanvasElement;
  let chart: Chart;
  
  onMount(() => {
    Chart.register(...registerables);
    renderChart();
  });
  
  $: if (timeSeries && chart) {
    updateChart();
  }
  
  function renderChart() {
    if (!canvas || !timeSeries || !timeSeries.intervals.length) {
      console.log('No time series data to render');
      return;
    }
    
    const intervals = timeSeries.intervals;
    console.log('Rendering chart with', intervals.length, 'intervals');
    
    const labels = intervals.map(i => {
      const date = new Date(i.timestamp);
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    });
    
    // Extract all numeric fields
    const fields = timeSeries.fields_tracked || [];
    const datasets = [];
    
    // Color palette
    const colors = [
      { border: 'rgb(147, 51, 234)', bg: 'rgba(147, 51, 234, 0.1)' },  // Purple
      { border: 'rgb(59, 130, 246)', bg: 'rgba(59, 130, 246, 0.1)' },   // Blue
      { border: 'rgb(234, 88, 12)', bg: 'rgba(234, 88, 12, 0.1)' },     // Orange
      { border: 'rgb(34, 197, 94)', bg: 'rgba(34, 197, 94, 0.1)' },     // Green
      { border: 'rgb(236, 72, 153)', bg: 'rgba(236, 72, 153, 0.1)' },   // Pink
    ];
    
    fields.forEach((field, idx) => {
      const values = intervals.map(i => i.data[field]?.avg || null);
      const color = colors[idx % colors.length];
      
      datasets.push({
        label: field,
        data: values,
        borderColor: color.border,
        backgroundColor: color.bg,
        borderWidth: 2,
        tension: 0.3,
        fill: true,
        pointRadius: 3,
        pointHoverRadius: 5
      });
    });
    
    // Add log count as a separate dataset (right y-axis)
    datasets.push({
      label: 'Log Count',
      data: intervals.map(i => i.log_count),
      borderColor: 'rgb(156, 163, 175)',
      backgroundColor: 'rgba(156, 163, 175, 0.1)',
      borderWidth: 2,
      tension: 0.3,
      fill: false,
      pointRadius: 2,
      pointHoverRadius: 4,
      yAxisID: 'y1'
    });
    
    chart = new Chart(canvas, {
      type: 'line',
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 15,
              font: { size: 11 }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            titleFont: { size: 12, weight: 'bold' },
            bodyFont: { size: 11 },
            callbacks: {
              label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += context.parsed.y.toFixed(2);
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: 'Data Values',
              font: { size: 11, weight: 'bold' }
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            }
          },
          y1: {
            type: 'linear',
            display: true,
            position: 'right',
            title: {
              display: true,
              text: 'Log Count',
              font: { size: 11, weight: 'bold' }
            },
            grid: {
              drawOnChartArea: false,
            }
          },
          x: {
            grid: {
              display: false
            },
            ticks: {
              font: { size: 10 }
            }
          }
        }
      }
    });
  }
  
  function updateChart() {
    if (!chart || !timeSeries) return;
    
    const intervals = timeSeries.intervals;
    chart.data.labels = intervals.map(i => {
      const date = new Date(i.timestamp);
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    });
    
    // Update datasets
    const fields = timeSeries.fields_tracked || [];
    fields.forEach((field, idx) => {
      if (chart.data.datasets[idx]) {
        chart.data.datasets[idx].data = intervals.map(i => i.data[field]?.avg || null);
      }
    });
    
    // Update log count
    const logCountIdx = fields.length;
    if (chart.data.datasets[logCountIdx]) {
      chart.data.datasets[logCountIdx].data = intervals.map(i => i.log_count);
    }
    
    chart.update();
  }
</script>

<div class="w-full h-full">
  <canvas bind:this={canvas}></canvas>
</div>

