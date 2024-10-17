document.addEventListener('DOMContentLoaded', function() {
    const chartDataElement = document.getElementById('chartData');
    const chartData = JSON.parse(chartDataElement.textContent);

    const ctx = document.getElementById('receitaDespesaChart').getContext('2d');

    let receitaDespesaChart;

    function createChart(type, labels, timeInterval, primeiroReceitas, segundoReceitas, terceiroReceitas, primeiroDespesas, segundoDespesas, terceiroDespesas) {
        if (receitaDespesaChart) {
            receitaDespesaChart.destroy();  
        }
    
        let datasets;
    
        if (type === 'pie') {
            
            datasets = [{
                
                data: [
                    primeiroReceitas, 
                    segundoReceitas, 
                    terceiroReceitas, 
                    primeiroDespesas, 
                    segundoDespesas, 
                    terceiroDespesas
                ], 
                backgroundColor: ['#007bff', '#dc3545', '#28a745', '#ffc107', '#17a2b8', '#6f42c1'],
                hoverBackgroundColor: ['#0056b3', '#c82333', '#1e7e34', '#d39e00', '#138496', '#5a2e91']
            }];
        } else {
            
            datasets = [
                {
                    label: 'Receitas',
                    data: [primeiroReceitas, segundoReceitas, terceiroReceitas],
                    backgroundColor: '#007bff',  
                    hoverBackgroundColor: '#0056b3' 
                },
                {
                    label: 'Despesas',
                    data: [primeiroDespesas, segundoDespesas, terceiroDespesas],
                    backgroundColor: '#dc3545',  
                    hoverBackgroundColor: '#c82333' 
                }
            ];
        }
    
        
        if (timeInterval == 'semanal') {
            receitaDespesaChart = new Chart(ctx, {
                type: type,
                data: {
                    labels: [
                        'Receita semana 1', 
                        'Receita semana 2', 
                        'Receita semana 3', 
                        'Despesa semana 1', 
                        'Despesa semana 2', 
                        'Despesa semana 3'
                    ],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        }

         
        else if (timeInterval == 'mensal') {
            receitaDespesaChart = new Chart(ctx, {
                type: type,
                data: {
                    labels: [
                        'Receita Mês 1', 
                        'Receita Mês 2', 
                        'Receita Mês 3', 
                        'Despesa Mês 1', 
                        'Despesa Mês 2', 
                        'Despesa Mês 3'
                    ],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        }

        else if (timeInterval == 'anual') {
            receitaDespesaChart = new Chart(ctx, {
                type: type,
                data: {
                    labels: [
                        'Receita Anual', 
                        'Despesa Anual'  
                    ],
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(tooltipItem) {
                                    return tooltipItem.label + ': ' + tooltipItem.raw.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    
    

    
    function updateChart() {
        const chartType = document.getElementById('chartTypeSelect').value;
        const timeInterval = document.getElementById('timeIntervalSelect').value;

        let labels, receitas, despesas;

        
        if (timeInterval === 'semanal') {
            labels = chartData.semanas;
            receitas = chartData.receitasSemanal;
            despesas = chartData.despesasSemanal;
            console.log(chartData)
            const receitasUltimosTres = receitas.slice(-3);
            const despesasUltimosTres = despesas.slice(-3);

            for (let i = 0; i < receitasUltimosTres.length; i++) {
                primeiroReceitas = receitasUltimosTres[0]
                segundoReceitas = receitasUltimosTres[1]
                terceiroReceitas = receitasUltimosTres[2]  
            } 

            for (let i = 0; i < despesasUltimosTres.length; i++) {
                primeiroDespesas = despesasUltimosTres[0]
                segundoDespesas = despesasUltimosTres[1]
                terceiroDespesas = despesasUltimosTres[2]  
            } 

        } else if (timeInterval === 'mensal') {
            labels = chartData.meses;
            receitas = chartData.receitasMensal;
            despesas = chartData.despesasMensal;
            const receitasUltimosTres = receitas.slice(-3);
            const despesasUltimosTres = despesas.slice(-3);

            for (let i = 0; i < receitasUltimosTres.length; i++) {
                primeiroReceitas = receitasUltimosTres[0]
                segundoReceitas = receitasUltimosTres[1]
                terceiroReceitas = receitasUltimosTres[2]  
            } 

            for (let i = 0; i < despesasUltimosTres.length; i++) {
                primeiroDespesas = despesasUltimosTres[0]
                segundoDespesas = despesasUltimosTres[1]
                terceiroDespesas = despesasUltimosTres[2]  
            } 

        } else if (timeInterval === 'anual') {
            labels = ['Receitas', 'Despesas'];  
            receitas = [chartData.receitasAnual];
            despesas = [chartData.despesasAnual];
        }

        
        createChart(chartType, labels, timeInterval, primeiroReceitas, segundoReceitas, terceiroReceitas, primeiroDespesas, segundoDespesas, terceiroDespesas);
    }

    
    document.getElementById('chartTypeSelect').addEventListener('change', updateChart);
    document.getElementById('timeIntervalSelect').addEventListener('change', updateChart);

    
    updateChart();
});


document.getElementById('relatorioForm').addEventListener('submit', function(event) {
    const dataInicio = document.getElementById('data_inicio').value;
    const dataFim = document.getElementById('data_fim').value;
    const email = document.getElementById('email').value;
  
    const mensagemErro = document.getElementById('mensagemErro');
    
    if (!dataInicio || !dataFim || !email) {
      event.preventDefault();
  
      mensagemErro.innerHTML = 'Por favor, preencha todos os campos: Data Início, Data Fim e Email.';
      mensagemErro.style.display = 'block';
    } else {
      mensagemErro.style.display = 'none';
    }
  });
  