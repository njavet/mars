<script setup>
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
const data = {
  labels,
  datasets: [{
    label: 'Evaluation',
    data: labels.map(k => props.scores[k]),
    backgroundColor: 'cyan'
  }]
}
</script>

<template>
  <Bar :data="data" />
</template>