<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  scores: Object
})

const labels = Object.keys(props.scores)


const chartData = computed(() => {
  const labels = Object.keys(props.scores || {})
  return {
    labels,
    datasets: [{
      label: 'Evaluation',
      data: labels.map(k => props.scores[k]),
      backgroundColor: 'cyan'
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      min: 0,
      max: 10,
      ticks: {
        stepSize: 1
      }
    }
  }
}
</script>

<template>
  <div style="height: 200px">
  <Bar :data="chartData" :options="chartOptions"/>
  </div>
</template>