// document.getElementById('applyFilter').addEventListener('click', function() {
//     const question = document.getElementById('questionSelect').value;
//     const answer = document.getElementById('answerSelect').value;
//
//     fetch(`/analytics_data?question=${question}&answer=${answer}`)
//         .then(response => response.json())
//         .then(data => updateBarChart(data));
//
//     fetch(`/heatmap_data?question=${question}`)
//         .then(response => response.json())
//         .then(data => updateHeatmap(data));
//
//     fetch(`/correlation_data?question=${question}`)
//         .then(response => response.json())
//         .then(data => updateCorrelationGraph(data));
//
//     fetch(`/pie_chart_data?question=${question}`)
//         .then(response => response.json())
//         .then(data => updatePieChart(data));
// });
//
// function updateBarChart(data) {
//     let ctx = document.getElementById('hesitancyBarChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: data.labels,
//             datasets: [{
//                 label: 'Hesitancy Score',
//                 data: data.values,
//                 backgroundColor: 'rgba(75, 192, 192, 0.5)'
//             }]
//         }
//     });
// }
//
// function updateHeatmap(data) {
//     let ctx = document.getElementById('hesitancyHeatmap').getContext('2d');
//     new Chart(ctx, {
//         type: 'heatmap',
//         data: data
//     });
// }
//
// function updateCorrelationGraph(data) {
//     let ctx = document.getElementById('correlationGraph').getContext('2d');
//     new Chart(ctx, {
//         type: 'scatter',
//         data: data
//     });
// }
//
// function updatePieChart(data) {
//     let ctx = document.getElementById('responsePieChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'pie',
//         // data: data
//     })
// }
