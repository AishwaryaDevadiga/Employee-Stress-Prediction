// Analytics visualization charts using Chart.js

document.addEventListener('DOMContentLoaded', () => {
    const stressDistCtx = document.getElementById('stressDistChart');
    const genderStressCtx = document.getElementById('genderStressChart');
    const deptStressCtx = document.getElementById('deptStressChart');
    const monthlyTrendsCtx = document.getElementById('monthlyTrendsChart');

    if (!stressDistCtx) return; // Only run on pages containing analytics canvas

    // Fetch metrics from API
    fetch('/admin/analytics-data')
        .then(response => response.json())
        .then(data => {
            // Update Totals KPIs if present in page
            document.getElementById('total-users-val').innerText = data.total_users;
            document.getElementById('total-predictions-val').innerText = data.total_predictions;
            document.getElementById('high-stress-val').innerText = data.high_stress_cases;

            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const textCol = isDark ? '#9ca3af' : '#475569';
            const gridCol = isDark ? 'rgba(75, 85, 99, 0.2)' : 'rgba(226, 232, 240, 0.8)';

            // 1. Stress Distribution (Doughnut Chart)
            new Chart(stressDistCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Low Stress', 'Medium Stress', 'High Stress'],
                    datasets: [{
                        data: [
                            data.stress_distribution.Low || 0,
                            data.stress_distribution.Medium || 0,
                            data.stress_distribution.High || 0
                        ],
                        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                        borderWidth: 0,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: textCol, font: { family: 'Plus Jakarta Sans', weight: '600' } }
                        }
                    }
                }
            });

            // 2. Gender-wise Stress Analysis (Stacked/Grouped Bar Chart)
            new Chart(genderStressCtx, {
                type: 'bar',
                data: {
                    labels: ['Male', 'Female'],
                    datasets: [
                        {
                            label: 'Low Stress',
                            data: [data.gender_stress.Male.Low, data.gender_stress.Female.Low],
                            backgroundColor: '#10b981'
                        },
                        {
                            label: 'Medium Stress',
                            data: [data.gender_stress.Male.Medium, data.gender_stress.Female.Medium],
                            backgroundColor: '#f59e0b'
                        },
                        {
                            label: 'High Stress',
                            data: [data.gender_stress.Male.High, data.gender_stress.Female.High],
                            backgroundColor: '#ef4444'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: textCol } },
                        y: { grid: { color: gridCol }, ticks: { color: textCol } }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: textCol, font: { family: 'Plus Jakarta Sans' } }
                        }
                    }
                }
            });

            // 3. Department-wise Stress Analysis (Horizontal Bar Chart)
            const depts = Object.keys(data.department_stress);
            const deptLow = depts.map(d => data.department_stress[d].Low);
            const deptMed = depts.map(d => data.department_stress[d].Medium);
            const deptHigh = depts.map(d => data.department_stress[d].High);

            new Chart(deptStressCtx, {
                type: 'bar',
                data: {
                    labels: depts,
                    datasets: [
                        { label: 'Low Stress', data: deptLow, backgroundColor: '#10b981' },
                        { label: 'Medium Stress', data: deptMed, backgroundColor: '#f59e0b' },
                        { label: 'High Stress', data: deptHigh, backgroundColor: '#ef4444' }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    scales: {
                        x: { stacked: true, grid: { color: gridCol }, ticks: { color: textCol } },
                        y: { stacked: true, grid: { display: false }, ticks: { color: textCol } }
                    },
                    plugins: {
                        legend: { position: 'bottom', labels: { color: textCol } }
                    }
                }
            });

            // 4. Monthly Prediction Trends (Line Chart)
            const trendMonths = Object.keys(data.monthly_trends);
            const trendCounts = Object.values(data.monthly_trends);

            new Chart(monthlyTrendsCtx, {
                type: 'line',
                data: {
                    labels: trendMonths,
                    datasets: [{
                        label: 'Predictions Made',
                        data: trendCounts,
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#4f46e5',
                        pointHoverRadius: 7
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: textCol } },
                        y: { grid: { color: gridCol }, ticks: { color: textCol, stepSize: 1 } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        })
        .catch(err => console.error('Error fetching analytics:', err));
});
